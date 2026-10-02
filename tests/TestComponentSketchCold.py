# SPDX-License-Identifier: LGPL-2.1-or-later
"""Reopen authored sketch workflows in a separate native GUI process."""
import math
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import ComponentModel as Model
import ComponentSketch as Sketch
from freecad.gui import ComponentNavigator as Navigator
from freecad.gui import ComponentSketchTask as Task
from PySide import QtCore, QtWidgets


class TestComponentSketchCold(unittest.TestCase):
    def setUp(self):
        os.write(2, ("Cold sketch check: " + self._testMethodName + "\n").encode())

    def tearDown(self):
        if Task._task:
            Task._task.reject()
        for doc in list(App.listDocuments().values()):
            gui = Gui.getDocument(doc.Name)
            if gui.getInEdit():
                gui.resetEdit()
        for name in reversed(list(App.listDocuments())):
            App.closeDocument(name)
        Gui.updateGui()
        loop=QtCore.QEventLoop()
        QtCore.QTimer.singleShot(150,loop.quit)
        loop.exec_()
        QtWidgets.QApplication.sendPostedEvents(None,QtCore.QEvent.DeferredDelete)

    def fixture(self, name):
        return Path(os.environ['FREECAD_PLUS_SKETCH_FIXTURES']) / name

    def test_standard_open_edit_constraints_and_plane_recompute(self):
        path = self.fixture('constrained-workflow.cadprt')
        App.ParamGet('User parameter:BaseApp/Preferences/Dialog').SetBool('DontUseNativeDialog', True)
        chosen=[]
        attempts=[0]
        def choose():
            attempts[0]+=1
            dialog=QtWidgets.QApplication.activeModalWidget()
            if attempts[0] <= 3:
                os.write(2,("Open chooser: " + str(type(dialog)) + " / " +
                            (dialog.windowTitle() if dialog else "none") + "\n").encode())
            if isinstance(dialog, QtWidgets.QFileDialog):
                dialog.setAttribute(QtCore.Qt.WA_DontShowOnScreen,True)
                dialog.selectFile(str(path))
                chosen.append(True)
                dialog.accept()
            elif attempts[0]<100:
                QtCore.QTimer.singleShot(50,choose)
            elif dialog:
                dialog.reject()
        QtCore.QTimer.singleShot(50,choose)
        os.write(2,b'Standard Open begins\n')
        Gui.runCommand('Std_Open')
        os.write(2,b'Standard Open completed\n')
        self.assertTrue(chosen)
        doc=App.ActiveDocument
        root=Model.metadata(doc).RootComponent
        obj=next(o for o in Model.history(root) if o.TypeId=='Sketcher::SketchObject')
        plane=obj.AttachmentSupport[0][0]
        result=next(o for o in doc.Objects if getattr(o,'ComponentRole','')=='Result')
        self.assertTrue(obj.FullyConstrained)
        self.assertEqual(plane.Label,'Plane001')
        self.assertAlmostEqual(result.Shape.Volume,1500)
        refs=[c for c in obj.Constraints if not c.Driving]
        self.assertEqual(len(refs),1)
        self.assertAlmostEqual(refs[0].Value,math.sqrt(1000))
        self.assertTrue(Gui.activeDocument().setEdit(obj.Name))
        Gui.updateGui()
        Gui.activeDocument().resetEdit()
        Gui.updateGui()
        before=result.Shape.BoundBox.ZMin
        with Model.transaction(doc,'Move sketch support plane'):
            plane.AttachmentOffset=App.Placement(App.Vector(0,0,9),App.Rotation())
        self.assertAlmostEqual(result.Shape.BoundBox.ZMin,before+5)
        self.assertAlmostEqual(result.Shape.Volume,1500)
        doc.undo()
        doc.recompute()
        self.assertAlmostEqual(result.Shape.BoundBox.ZMin,before)
        doc.redo()
        doc.recompute()
        self.assertAlmostEqual(result.Shape.BoundBox.ZMin,before+5)
        panel=Navigator.show(doc)
        panel.refresh()
        self.assertEqual(panel.tabs.tabText(2),'History')

    def test_cold_curve_families_and_reference_flags(self):
        doc=App.openDocument(str(self.fixture('curve-families.cadprt')))
        root=Model.metadata(doc).RootComponent
        obj=next(o for o in Model.history(root) if o.TypeId=='Sketcher::SketchObject')
        self.assertEqual(obj.GeometryCount,10)
        self.assertEqual([obj.getConstruction(i) for i in range(10)],[False,True]*5)
        self.assertEqual(len(obj.Shape.Edges),5)
        self.assertEqual(str(obj.MapMode),'ObjectXY')
        self.assertTrue(Gui.activeDocument().setEdit(obj.Name))
        Gui.updateGui()
        Gui.activeDocument().resetEdit()
        Gui.updateGui()

    def test_new_sketch_command_reuses_saved_plane(self):
        doc=App.openDocument(str(self.fixture('constrained-workflow.cadprt')))
        root=Model.metadata(doc).RootComponent
        Navigator.show(doc)
        plane=Sketch.user_planes(root)[0]
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(plane)
        Gui.runCommand('Sketcher_NewSketch')
        task=Task._task
        self.assertIsNotNone(task)
        self.assertEqual(task.plane.currentData(),'User plane')
        self.assertEqual(task.user_plane.currentData(),plane.Name)
        before=[o.Name for o in doc.Objects]
        task.reject()
        self.assertEqual([o.Name for o in doc.Objects],before)
