# SPDX-License-Identifier: LGPL-2.1-or-later
from pathlib import Path
import tempfile
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest
import ComponentModel as Model
from freecad.gui import MoveComponents as Move
from freecad.gui import MoveComponentsTask as UI
from freecad.gui import DesignSelection
import TestMoveComponentsRotate as Fixtures
import TestComponentTaskWidth as Width


class TestMoveComponentsIntegration(unittest.TestCase):
    setUp = Fixtures.TestMoveComponentsRotate.setUp
    tearDown = Fixtures.TestMoveComponentsRotate.tearDown
    session = Fixtures.TestMoveComponentsRotate.session
    vector = Fixtures.TestMoveComponentsRotate.vector
    settle = staticmethod(Width.TestComponentTaskWidth.settle)
    check_width = Width.TestComponentTaskWidth.check_width

    def test_compact_native_tasks_all_six_methods(self):
        self.task = UI.open_task(self.root, self.paths)
        task = self.task
        try:
            for mode in range(6):
                task.workflow.setCurrentIndex(mode)
                if mode == 4:
                    for button in task.frame_fields.findChildren(QtWidgets.QToolButton):
                        button.setChecked(True)
                self.check_width("Move-"+Move.WORKFLOWS[mode].replace(" ","_"),height=420)
        finally:
            parent = task.form
            while parent and not isinstance(parent,QtWidgets.QDockWidget):
                parent = parent.parentWidget()
            if parent:
                parent.setFloating(False)
            task.reject()

    def test_mode_exit_removes_native_handle_without_document_change(self):
        task = UI.open_task(self.root,self.paths)
        task.workflow.setCurrentIndex(5)
        scene = task.manipulator.scene
        child_count = scene.getNumChildren()
        signature = task.session.signature()
        DesignSelection.parameters().SetBool("Active",False)
        task.check_context()
        self.assertTrue(task.closed)
        self.assertIsNone(task.manipulator)
        # Avoid dereferencing a deleted node: the scene count is the lifecycle oracle.
        self.assertEqual(scene.getNumChildren(), child_count-1)
        self.assertEqual(signature,task.session.signature())
        DesignSelection.parameters().SetBool("Active",True)

    def test_actual_viewport_point_collectors_outside_active_parent(self):
        source, target = App.Vector(-10,-6,-4), App.Vector(8,4,2)
        for name,point in (("NativeMoveSource",source),("NativeMoveTarget",target)):
            obj = self.doc.addObject("Part::Feature",name)
            obj.Shape = Part.Vertex(point)
            obj.ViewObject.PointSize = 8.
            Model.register_object(self.root,obj)
        self.doc.recompute()
        task = UI.open_task(self.root,self.paths)
        task.workflow.setCurrentIndex(2)
        view = Gui.activeDocument().activeView()
        view.viewFront()
        view.fitAll()
        self.settle()
        widgets = [w for w in task.window.findChildren(QtWidgets.QWidget)
                   if "GL" in w.metaObject().className() and w.width()>100 and w.height()>100]
        widget = max(widgets,key=lambda w:w.width()*w.height())
        ratio = widget.devicePixelRatioF()
        signature = task.session.signature()
        for button,point,role in ((task.source_pick,source,"source_point"),
                                  (task.destination_pick,target,"destination_point")):
            button.click()
            x,y = view.getPointOnScreen(point)
            pixel = QtCore.QPoint(round(x/ratio),widget.height()-round(y/ratio)-1)
            QtTest.QTest.mouseMove(widget,pixel)
            self.settle()
            QtTest.QTest.mouseClick(widget,QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,pixel)
            self.settle()
            value = getattr(task.session,role)
            self.assertIsNotNone(value,task.status.text())
            self.vector(task.session.frame().multVec(value),point)
        self.assertEqual(signature,task.session.signature())
        expected = task.session.frame().Rotation.inverted().multVec(target-source)
        next(button for button in Gui.getMainWindow().findChildren(QtWidgets.QPushButton)
             if button.text().replace("&","")=="Apply" and button.isVisible()).click()
        self.vector(self.first.LinkPlacement.Base,expected)

    def test_active_document_switch_and_owning_document_close_clean_native_handles(self):
        task = UI.open_task(self.root,self.paths)
        task.workflow.setCurrentIndex(5)
        scene = task.manipulator.scene
        count = scene.getNumChildren()
        signature = task.session.signature()
        Model.new_document("Move tab transition")
        self.settle()
        self.assertTrue(task.closed)
        self.assertIsNone(UI._task)
        self.assertEqual(scene.getNumChildren(),count-1)
        self.assertEqual(signature,task.session.signature())
        App.setActiveDocument(self.doc.Name)
        self.settle()
        task = UI.open_task(self.root,self.paths)
        task.workflow.setCurrentIndex(5)
        self.assertIsNotNone(task.manipulator)
        App.closeDocument(self.doc.Name)
        self.settle()
        self.assertTrue(task.closed)
        self.assertIsNone(task.manipulator)
        self.assertIsNone(UI._task)

    def test_external_parent_requires_owning_file_and_works_there(self):
        folder = Path(tempfile.mkdtemp(prefix="move-external-"))
        self.doc.saveAs(str(folder/"assembly.cadprt"))
        external = Model.new_document("External parent")
        parent = Model.metadata(external).RootComponent
        first = Model.add_component(parent,label="External child")
        second = Model.add_component(parent,first.LinkedObject)
        external.saveAs(str(folder/"parent.cadprt"))
        link = Model.add_component(self.root,parent)
        with self.assertRaisesRegex(ValueError,"owning file"):
            session = Move.Session(self.root)
            session.add([(link.ObjectId,first.ObjectId)])
        App.setActiveDocument(external.Name)
        session = Move.Session(parent)
        session.add([(first.ObjectId,),(second.ObjectId,)])
        session.direction,session.distance = App.Vector(1,0,0),3.
        self.assertTrue(session.commit(session.translation()))
        self.vector(first.LinkPlacement.Base,App.Vector(3,0,0))
        self.vector(second.LinkPlacement.Base,App.Vector(3,0,0))
        external.save()
        self.doc.save()
