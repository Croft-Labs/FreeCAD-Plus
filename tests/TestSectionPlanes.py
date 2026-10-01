# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native clipping controls and portable section-plane definitions."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtWidgets


def make_fixture():
    doc = App.newDocument("SectionInspection")
    doc.UndoMode = 1
    outer = doc.addObject("App::Part", "Assembly")
    inner = doc.addObject("App::Part", "Subassembly")
    outer.addObject(inner)
    body = doc.addObject("Part::Feature", "Housing")
    body.Shape = Part.makeBox(30, 20, 16).cut(
        Part.makeBox(22, 12, 14, App.Vector(4, 4, 4)))
    inner.addObject(body)
    outer.Placement.Base = App.Vector(10, 5, 0)
    occurrence = doc.addObject("App::Link", "SecondHousing")
    occurrence.setLink(body)
    occurrence.Placement.Base = App.Vector(50, 5, 0)
    doc.recompute()
    return doc


class TestSectionPlanes(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.path = Path(self.directory.name) / "inspection.fcsection"
        self.doc = make_fixture()
        Gui.activeDocument().activeView().viewAxonometric()
        Gui.activeDocument().activeView().fitAll()
        self.openPanel()

    def openPanel(self):
        Gui.runCommand("Std_ToggleClipPlane")
        Gui.updateGui()
        self.panel = Gui.getMainWindow().findChild(QtWidgets.QDialog, "Gui__Dialog__Clipping")
        self.assertIsNotNone(self.panel)
        for axis in "XYZ":
            field = self.widget(QtWidgets.QDoubleSpinBox, "dir" + axis)
            self.assertGreaterEqual(field.height(), field.sizeHint().height())
            parent = field.parentWidget()
            while parent is not self.panel:
                top = field.mapTo(parent, QtCore.QPoint(0, 0))
                self.assertGreaterEqual(top.y(), 0)
                self.assertLessEqual(top.y() + field.height(), parent.height())
                parent = parent.parentWidget()

    def closePanel(self):
        if self.panel is not None:
            self.panel.reject()
            QtWidgets.QApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)
            Gui.updateGui()
            self.panel = None

    def tearDown(self):
        self.closePanel()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()
        self.directory.cleanup()

    def widget(self, kind, name):
        result = self.panel.findChild(kind, name)
        self.assertIsNotNone(result, name)
        return result

    def spin(self, name, value):
        self.widget(QtWidgets.QDoubleSpinBox, name).setValue(value)

    def enable(self, name, checked=True):
        self.widget(QtWidgets.QGroupBox, name).setChecked(checked)

    def call(self, method, path=None):
        self.assertTrue(QtCore.QMetaObject.invokeMethod(
            self.panel, method, QtCore.Qt.DirectConnection,
            QtCore.Q_ARG(str, str(path or self.path))))
        Gui.updateGui()

    def saved(self):
        self.call("saveSection")
        return json.loads(self.path.read_text())

    def status(self):
        return self.widget(QtWidgets.QLabel, "sectionStatus").text()

    def planes(self):
        graph = Gui.activeDocument().activeView().getSceneGraph()
        return [graph.getChild(i) for i in range(graph.getNumChildren())
                if graph.getChild(i).getTypeId().getName() == "ClipPlane"]

    def testAxisPlanesFlipAndPersistenceWithoutModelChanges(self):
        original = self.doc.Housing.Shape.copy()
        names = [o.Name for o in self.doc.Objects]
        self.enable("groupBoxX")
        self.enable("groupBoxZ")
        self.spin("clipX", 25)
        self.spin("clipZ", 8)
        self.widget(QtWidgets.QPushButton, "flipClipX").click()
        data = self.saved()
        self.assertEqual(data["planes"][0], {"enabled": True, "normal": [-1, 0, 0], "offsetMm": -25})
        self.assertTrue(data["planes"][2]["enabled"])
        model = Path(self.directory.name) / "Housing.FCStd"
        self.doc.saveAs(str(model))
        self.closePanel()
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(model))
        self.openPanel()
        self.call("loadSection")
        self.assertIn("loaded", self.status())
        self.assertEqual(self.saved(), data)
        self.assertEqual([o.Name for o in self.doc.Objects], names)
        self.assertAlmostEqual(self.doc.Housing.Shape.Volume, original.Volume)
        self.assertAlmostEqual(self.doc.Housing.Shape.common(original).Volume, original.Volume)
        self.assertFalse(self.doc.HasPendingTransaction)

    def testCameraDirectionAndZeroRecovery(self):
        self.enable("groupBoxView")
        Gui.activeDocument().activeView().viewFront()
        self.widget(QtWidgets.QPushButton, "fromView").click()
        expected = Gui.activeDocument().activeView().getViewDirection()
        shown = [self.widget(QtWidgets.QDoubleSpinBox, "dir" + axis).value() for axis in "XYZ"]
        for got, want in zip(shown, expected):
            self.assertAlmostEqual(got, want, places=6)
        for axis in "XYZ":
            self.spin("dir" + axis, 0)
        self.assertIn("cannot be zero", self.status())
        self.assertFalse(any(node.on.getValue() for node in self.planes()))
        self.call("saveSection")
        self.assertFalse(self.path.exists())
        self.spin("dirX", 1)
        self.spin("dirY", 1)
        data = self.saved()
        self.assertTrue(data["planes"][3]["enabled"])
        self.assertAlmostEqual(sum(x*x for x in data["planes"][3]["normal"]), 1, places=6)

    def testCameraFollowPresetRestoresFixedPlane(self):
        self.enable("groupBoxView")
        self.widget(QtWidgets.QCheckBox, "adjustViewdirection").setChecked(True)
        data = self.saved()
        Gui.activeDocument().activeView().viewTop()
        self.call("loadSection")
        self.assertFalse(self.widget(QtWidgets.QCheckBox, "adjustViewdirection").isChecked())
        self.assertEqual(self.saved(), data)
        self.assertTrue(data["planes"][3]["enabled"])

    def testInvalidPresetDoesNotPartiallyChangeView(self):
        self.enable("groupBoxY")
        self.spin("clipY", 9)
        valid = self.saved()
        bad = Path(self.directory.name) / "bad.fcsection"
        variants = []
        changed = copy.deepcopy(valid)
        changed["version"] = 2
        variants.append(changed)
        changed = copy.deepcopy(valid)
        changed["planes"][0]["offsetMm"] = 123
        changed["planes"][3]["normal"] = [0, 0, 0]
        variants.append(changed)
        changed = copy.deepcopy(valid)
        changed["planes"][3]["enabled"] = True
        variants.append(changed)
        for data in variants:
            bad.write_text(json.dumps(data))
            self.call("loadSection", bad)
            self.assertIn("unchanged", self.status())
            self.assertEqual(self.saved(), valid)
        bad.write_text("not JSON")
        self.call("loadSection", bad)
        self.assertIn("unchanged", self.status())
        self.assertEqual(self.saved(), valid)
        self.call("saveSection", Path(self.directory.name) / "missing" / "file.fcsection")
        self.assertIn("Could not save", self.status())

    def testCloseRemovesClippingAndPreservesUndoAndWholeExport(self):
        self.doc.openTransaction("Owner edit")
        self.doc.Housing.Label = "Owner housing"
        self.enable("groupBoxZ")
        self.spin("clipZ", 8)
        self.call("saveSection")
        self.call("loadSection")
        self.assertTrue(self.doc.HasPendingTransaction)
        self.assertEqual(len(self.planes()), 4)
        brep = Path(self.directory.name) / "whole.brep"
        self.doc.Housing.Shape.exportBrep(str(brep))
        exported = Part.Shape()
        exported.read(str(brep))
        self.assertAlmostEqual(exported.Volume, self.doc.Housing.Shape.Volume)
        self.closePanel()
        self.assertEqual(len(self.planes()), 0)
        self.doc.commitTransaction()
        self.doc.undo()
        self.assertEqual(self.doc.Housing.Label, "Housing")

    def testFlatGeometryKeepsUsableOffsets(self):
        self.closePanel()
        App.closeDocument(self.doc.Name)
        self.doc = App.newDocument("FlatSection")
        face = self.doc.addObject("Part::Feature", "FlatFace")
        face.Shape = Part.makePlane(10, 10)
        self.doc.recompute()
        self.openPanel()
        for name in ["clipX", "clipY", "clipZ", "clipView"]:
            self.assertGreater(self.widget(QtWidgets.QDoubleSpinBox, name).singleStep(), 0)
            self.assertEqual(self.widget(QtWidgets.QDoubleSpinBox, name).suffix(), " mm")
