# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *   Copyright (c) 2017 Shai Seger <shaise at gmail>                       *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************
"""
Command and task window handler for the OpenGL based CAM simulator
"""

import math
import os
import FreeCAD
import Path.Base.Util as PathUtil
import Path.Dressup.Utils as PathDressup
from PathScripts import PathUtils
import CAMSimulator
from Path.Main import SimulationReview

from FreeCAD import Vector, Placement, Rotation

# lazily loaded modules
from lazy_loader.lazy_loader import LazyLoader

Mesh = LazyLoader("Mesh", globals(), "Mesh")
Part = LazyLoader("Part", globals(), "Part")

if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtGui, QtCore, QtWidgets
    from PySide.QtGui import QDialogButtonBox

_filePath = os.path.dirname(os.path.abspath(__file__))


def IsSame(x, y):
    """Check if two floats are the same within an epsilon"""
    return abs(x - y) < 0.0001


def RadiusAt(edge, p):
    """Find the tool radius within a point on its circumference"""
    x = edge.valueAt(p).x
    y = edge.valueAt(p).y
    return math.sqrt(x * x + y * y)


class CAMSimTaskUi:
    """Handles the simulator task panel"""

    def __init__(self, parent):
        # this will create a Qt widget from our ui file
        self.form = FreeCADGui.PySideUic.loadUi(":/panels/TaskCAMSimulator.ui")
        self.parent = parent

    def autoClosedOnDeletedDocument(self):
        self.parent.cancel()

    def getStandardButtons(self, *_args):
        """Task panel needs only Close button"""
        return QDialogButtonBox.Close

    def reject(self):
        """User Pressed the Close button"""
        self.parent.cancel()
        FreeCADGui.Control.closeDialog()


def TSError(msg):
    """Display error message"""
    QtGui.QMessageBox.information(None, "Path Simulation", msg)


class CAMSimulation:
    """Handles and prepares CAM jobs for simulation"""

    def __init__(self):
        self.debug = False
        self.stdrot = FreeCAD.Rotation(Vector(0, 0, 1), 0)
        self.iprogress = 0
        self.numCommands = 0
        self.simperiod = 20
        self.quality = 10
        self.resetSimulation = False
        self.jobs = []
        self.initdone = False
        self.taskForm = None
        self.disableAnim = False
        self.firstDrill = True
        self.millSim = None
        self.job = None
        self.activeOps = []
        self.ioperation = 0
        self.stock = None
        self.busy = False
        self.operations = []
        self.baseShape = None
        self.review = None
        self.observing = False
        self.document = None

    def Connect(self, but, sig):
        """Connect task panel buttons"""
        QtCore.QObject.connect(but, QtCore.SIGNAL("clicked()"), sig)

    def FindClosestEdge(self, edges, px, pz):
        """Convert tool shape to tool profile needed by GL simulator"""
        for edge in edges:
            p1 = edge.FirstParameter
            p2 = edge.LastParameter
            rad1 = RadiusAt(edge, p1)
            z1 = edge.valueAt(p1).z
            if IsSame(px, rad1) and IsSame(pz, z1):
                return edge, p1, p2
            rad2 = RadiusAt(edge, p2)
            z2 = edge.valueAt(p2).z
            if IsSame(px, rad2) and IsSame(pz, z2):
                return edge, p2, p1
            # sometimes a flat circle is without edge, so return edge with
            # same height and later a connecting edge will be interpolated
            if IsSame(pz, z1):
                return edge, p1, p2
            if IsSame(pz, z2):
                return edge, p2, p1
        return None, 0.0, 0.0

    def FindTopMostEdge(self, edges):
        """Examine tool solid edges and find the top most one"""
        maxz = -99999999.0
        topedge = None
        top_p1 = 0.0
        top_p2 = 0.0
        for edge in edges:
            p1 = edge.FirstParameter
            p2 = edge.LastParameter
            z = edge.valueAt(p1).z
            if z > maxz:
                topedge = edge
                top_p1 = p1
                top_p2 = p2
                maxz = z
            z = edge.valueAt(p2).z
            if z > maxz:
                topedge = edge
                top_p1 = p2
                top_p2 = p1
                maxz = z
        return topedge, top_p1, top_p2

    def GetToolProfile(self, tool, resolution):
        """Get the edge profile of a tool solid. Basically locating the
        side edge that OCC creates on any revolved object
        """
        shape = tool.Shape.copy()
        shape.Placement = Placement()
        sideEdgeList = []
        for _i, edge in enumerate(shape.Edges):
            if not edge.isClosed():
                # v1 = edge.firstVertex()
                # v2 = edge.lastVertex()
                # tp = "arc" if type(edge.Curve) is Part.Circle else "line"
                sideEdgeList.append(edge)

        # sort edges as a single 3d line on the x-z plane

        # first find the topmost edge
        edge, p1, p2 = self.FindTopMostEdge(sideEdgeList)
        profile = [RadiusAt(edge, p1), edge.valueAt(p1).z]
        endrad = 0.0
        # one by one find all connecting edges
        while edge is not None:
            sideEdgeList.remove(edge)
            if isinstance(edge.Curve, Part.Circle):
                # if edge is curved, approximate it with lines based on resolution
                nsegments = int(edge.Length / resolution) + 1
                step = (p2 - p1) / nsegments
                location = p1 + step
                while nsegments > 0:
                    endrad = RadiusAt(edge, location)
                    endz = edge.valueAt(location).z
                    profile.append(endrad)
                    profile.append(endz)
                    location += step
                    nsegments -= 1
            else:
                endrad = RadiusAt(edge, p2)
                endz = edge.valueAt(p2).z
                profile.append(endrad)
                profile.append(endz)
            edge, p1, p2 = self.FindClosestEdge(sideEdgeList, endrad, endz)
            if edge is None:
                break
            startrad = RadiusAt(edge, p1)
            if not IsSame(startrad, endrad):
                profile.append(startrad)
                startz = edge.valueAt(p1).z
                profile.append(startz)

        return profile

    def Activate(self):
        """Invoke the simulator task panel"""
        self.initdone = False
        self.document = FreeCAD.ActiveDocument
        self.taskForm = CAMSimTaskUi(self)
        form = self.taskForm.form
        self.reviewText = QtWidgets.QPlainTextEdit()
        self.reviewText.setReadOnly(True)
        self.reviewText.setMinimumHeight(170)
        self.reviewButton = QtWidgets.QPushButton(SimulationReview.tr("Review inputs"))
        self.scopeText = QtWidgets.QLabel(SimulationReview.tr(
            "Uses selected job toolpaths and cutter profiles, before postprocessing. "
            "Holder, fixture and machine-envelope clearance are not checked by this review. "
            "The simulator view reflects inputs sent at Play; restart after edits. "
            "This display is not proof of safe machine motion."))
        self.scopeText.setWordWrap(True)
        form.layout().addWidget(self.reviewText)
        form.layout().addWidget(self.reviewButton)
        form.layout().addWidget(self.scopeText)
        self.reviewButton.clicked.connect(self.refreshReview)
        self.Connect(form.toolButtonPlay, self.SimPlay)
        form.sliderAccuracy.valueChanged.connect(self.onAccuracyBarChange)
        self.onAccuracyBarChange()

        prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/CAM")
        if prefs.GetBool("SimulatorFollowsVisibility"):
            form.followsVisibility.setCheckState(QtCore.Qt.CheckState.Checked)
        form.followsVisibility.clicked.connect(self.followsVisibilityChange)

        self._populateJobSelection(form)
        form.comboJobs.currentIndexChanged.connect(self.onJobChange)
        self.onJobChange()
        form.listOperations.itemChanged.connect(self.onOperationItemChange)
        dialog = FreeCADGui.Control.showDialog(self.taskForm)
        dialog.setAutoCloseOnDeletedDocument(True)
        self.disableAnim = False
        self.firstDrill = True
        self.millSim = CAMSimulator.PathSim()
        self.initdone = True
        self.job = self.jobs[self.taskForm.form.comboJobs.currentIndex()]
        FreeCAD.addDocumentObserver(self)
        self.observing = True
        self.refreshReview()

    def _populateJobSelection(self, form):
        """Make Job selection combobox"""
        # Get list of Job objects in active document
        jobList = FreeCAD.ActiveDocument.findObjects("Path::FeaturePython", "Job.*")

        # Get name of selected Job
        jobName = ""
        selection = FreeCADGui.Selection.getSelection()
        if selection:  #  Identify job selected by user
            job = PathUtils.findParentJob(selection[0])
            if job:
                jobName = job.Name

        # Prepare combobox
        form.comboJobs.blockSignals(True)
        form.comboJobs.clear()
        form.comboJobs.blockSignals(False)

        # Get index of selected Job
        setJobIdx = 0
        for i, job in enumerate(jobList):
            # Populate the job selection combobox
            form.comboJobs.addItem(job.ViewObject.Icon, job.Label)
            self.jobs.append(job)
            if job.Name == jobName:
                setJobIdx = i

        # Preselect GUI-selected job in the combobox
        form.comboJobs.setCurrentIndex(setJobIdx)

    def SetupSimulation(self):
        """Prepare all selected job operations for simulation"""
        form = self.taskForm.form
        self.activeOps = []
        self.numCommands = 0
        self.ioperation = 0
        for i in range(form.listOperations.count()):
            if form.listOperations.item(i).checkState() == QtCore.Qt.CheckState.Checked:
                self.firstDrill = True
                self.activeOps.append(self.operations[i])
                self.numCommands += len(self.operations[i].Path.Commands)

        self.stock = self.job.Stock.Shape
        self.busy = False

    def onJobChange(self):
        """When a new job is selected from the drop-down, update job operation list"""
        prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/CAM")
        followsVisibility = prefs.GetBool("SimulatorFollowsVisibility")
        form = self.taskForm.form
        j = self.jobs[form.comboJobs.currentIndex()]
        self.job = j
        form.listOperations.blockSignals(True)
        form.listOperations.clear()
        self.operations = []
        allhidden = all(
            not op.Visibility for op in j.Operations.Group if PathUtil.opProperty(op, "Active")
        )
        for op in j.Operations.Group:
            if PathUtil.opProperty(op, "Active"):
                listItem = QtGui.QListWidgetItem(op.ViewObject.Icon, op.Label)
                listItem.setFlags(listItem.flags() | QtCore.Qt.ItemIsUserCheckable)
                if followsVisibility and not op.Visibility and not allhidden:
                    listItem.setCheckState(QtCore.Qt.CheckState.Unchecked)
                else:
                    listItem.setCheckState(QtCore.Qt.CheckState.Checked)
                self.operations.append(op)
                form.listOperations.addItem(listItem)
        form.listOperations.blockSignals(False)
        if self.initdone:
            self.refreshReview()

    def onAccuracyBarChange(self):
        """Update simulation quality"""
        form = self.taskForm.form
        self.quality = form.sliderAccuracy.value()
        qualText = QtCore.QT_TRANSLATE_NOOP("CAM_Simulator", "High")
        if self.quality < 4:
            qualText = QtCore.QT_TRANSLATE_NOOP("CAM_Simulator", "Low")
        elif self.quality < 9:
            qualText = QtCore.QT_TRANSLATE_NOOP("CAM_Simulator", "Medium")
        form.labelAccuracy.setText(qualText)
        if self.initdone:
            self.refreshReview()

    def followsVisibilityChange(self):
        """Update job list in accordance with operations visibility"""
        form = self.taskForm.form
        state = form.followsVisibility.isChecked()
        prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/CAM")
        prefs.SetBool("SimulatorFollowsVisibility", state)
        self.onJobChange()

    def onOperationItemChange(self, _item):
        self.refreshReview()

    def selectedOperations(self):
        form = self.taskForm.form
        return [self.operations[i] for i in range(form.listOperations.count())
                if form.listOperations.item(i).checkState() == QtCore.Qt.CheckState.Checked]

    def refreshReview(self):
        self.review = None
        self.taskForm.form.toolButtonPlay.setEnabled(False)
        try:
            self.review = SimulationReview.prepare(
                self.job, self.selectedOperations(), self.quality, self.GetToolProfile)
            self.reviewText.setPlainText(SimulationReview.describe(self.review))
            self.taskForm.form.toolButtonPlay.setEnabled(True)
        except Exception as error:
            self.reviewText.setPlainText(str(error))

    def SimPlay(self):
        """Validate every cutter/path before resetting or feeding the native session."""
        previous = self.review
        self.refreshReview()
        prepared = self.review
        if prepared is None:
            return
        if previous is None or previous["fingerprint"] != prepared["fingerprint"]:
            self.reviewText.appendPlainText(SimulationReview.tr("Inputs changed. Review the updated values, then press Play."))
            return
        try:
            self.millSim.ResetSimulation(FreeCADGui.getDocument(self.job.Document))
            tools = {tool["number"]: tool for tool in prepared["tools"]}
            for entry in prepared["operations"]:
                # Native AddTool also inserts a T command, so retain operation order.
                tool = tools[entry["tool"]]
                self.millSim.AddTool(tool["profile"], tool["number"], tool["diameter"], 1)
                for command in entry["commands"]:
                    self.millSim.AddCommand(command)
            self.millSim.BeginSimulation(prepared["stock"], prepared["quality"])
            if prepared["model"] is not None:
                self.millSim.SetBaseShape(prepared["model"], 1)
        except Exception as error:
            self.reviewText.appendPlainText(SimulationReview.tr("Simulation could not start: ") + str(error))

    def slotChangedObject(self, obj, prop):
        if obj.Document == self.document:
            self.invalidateReview()

    def slotDeletedObject(self, obj):
        if obj.Document == self.document:
            self.invalidateReview()

    def slotDeletedDocument(self, doc):
        if self.document == doc:
            self.cancel()

    def invalidateReview(self):
        self.review = None
        self.taskForm.form.toolButtonPlay.setEnabled(False)
        self.reviewText.setPlainText(SimulationReview.tr("Inputs changed. Recompute the job if needed, then Review inputs before restarting simulation."))

    def cancel(self):
        """Remove only this task's input observer; native simulator owns its view."""
        if self.observing:
            FreeCAD.removeDocumentObserver(self)
            self.observing = False



class CommandCAMSimulate:
    """FreeCAD invoke simulation task panel command"""

    def GetResources(self):
        """Command info"""
        return {
            "Pixmap": "CAM_SimulatorGL",
            "MenuText": QtCore.QT_TRANSLATE_NOOP("CAM_Simulator", "CAM Simulator"),
            "Accel": "P, N",
            "ToolTip": QtCore.QT_TRANSLATE_NOOP("CAM_Simulator", "Simulates G-code on stock"),
        }

    def IsActive(self):
        """Command is active if at least one CAM job exists"""
        if FreeCAD.ActiveDocument is not None:
            for o in FreeCAD.ActiveDocument.Objects:
                if o.Name[:3] == "Job":
                    return True
        return False

    def Activated(self):
        """Activate the simulation"""
        CamSimulation = CAMSimulation()
        CamSimulation.Activate()


if FreeCAD.GuiUp:
    # register the FreeCAD command
    FreeCADGui.addCommand("CAM_SimulatorGL", CommandCAMSimulate())
    FreeCAD.Console.PrintLog("Loading PathSimulator Gui… done\n")
