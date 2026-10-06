# SPDX-License-Identifier: LGPL-2.1-or-later
"""Exercise compact forms in the native Tasks scroller, without source overlays."""
import hashlib
import importlib
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import ComponentModel as Model
import ComponentSketch as Sketch
import Part
from PySide import QtCore, QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest


class TestComponentTaskWidth(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartDesignWorkbench")
        self.doc = Model.new_document("Compact task acceptance")
        self.component = Model.metadata(self.doc).RootComponent
        self.sketch = Sketch.create(self.component)
        self.sketch.Label = "A profile with a deliberately very long descriptive name " * 3
        self.sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 10))
        self.doc.recompute()
        self.task = None

    def tearDown(self):
        if self.task:
            self.task.reject()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    @staticmethod
    def settle():
        Gui.updateGui()
        QtTest.QTest.qWait(200)

    def launch(self, name, **kwargs):
        module = importlib.import_module("freecad.gui.Component" + name + "Task")
        source = Path(os.environ["FREECAD_PLUS_SOURCE"]) / "src/Gui" / Path(module.__file__).name
        self.assertEqual(hashlib.sha256(source.read_bytes()).digest(),
                         hashlib.sha256(Path(module.__file__).read_bytes()).digest())
        self.task = module.launch(**kwargs)
        if hasattr(self.task, "auto_preview"):
            self.task.auto_preview.setChecked(False)
        if hasattr(self.task, "sections") and name != "Sketch":
            for button, body, layout in self.task.sections:
                button.setChecked(True)
        return self.task

    def check_width(self, name, height=560):
        form = self.task.form
        parent, scroll, dock = form, None, None
        while parent:
            if isinstance(parent, QtWidgets.QScrollArea):
                scroll = parent
            if isinstance(parent, QtWidgets.QDockWidget):
                dock = parent
            parent = parent.parentWidget()
        self.assertIsNotNone(scroll)
        self.assertIsNotNone(dock)
        dock.setFloating(True)
        dock.resize(360, height)
        self.settle()
        print(name, "dock", dock.size(), "form", form.size(), "minimum", form.minimumSizeHint(),
              "viewport", scroll.viewport().size(), "vertical", scroll.verticalScrollBar().maximum())
        # Native floating-dock chrome is outside the logical Tasks scroller.
        self.assertLessEqual(scroll.width(), 360)
        self.assertEqual(scroll.horizontalScrollBarPolicy(), QtCore.Qt.ScrollBarAlwaysOff)
        self.assertLessEqual(scroll.widget().width(), scroll.viewport().width())
        self.assertGreater(scroll.verticalScrollBar().maximum(), 0)
        for collector in form.findChildren(QtWidgets.QListWidget):
            self.assertFalse(collector.horizontalScrollBar().isVisible())
        # All visible form controls must remain inside the horizontal viewport;
        # scrolling vertically must bring each full field into view.
        fields = form.findChildren(QtWidgets.QWidget)
        for field in fields:
            if not field.isVisibleTo(form) or not isinstance(field, (
                    QtWidgets.QAbstractSpinBox, QtWidgets.QComboBox, QtWidgets.QAbstractButton)):
                continue
            with self.subTest(field=field.objectName() or field.metaObject().className()):
                # ensureWidgetVisible follows a spin box's line-edit focus proxy,
                # which does not include its full frame and arrow buttons.
                center = field.mapTo(scroll.widget(), field.rect().center())
                scroll.ensureVisible(center.x(), center.y(), field.width() // 2 + 1,
                                     field.height() // 2 + 1)
                QtWidgets.QApplication.processEvents()
                point = field.mapTo(scroll.viewport(), QtCore.QPoint())
                self.assertGreaterEqual(point.x(), 0)
                self.assertLessEqual(point.x() + field.width(), scroll.viewport().width())
                self.assertGreaterEqual(field.height(), field.minimumSizeHint().height())
                self.assertGreaterEqual(point.y(), 0)
                self.assertLessEqual(point.y() + field.height(), scroll.viewport().height())
        output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        scroll.verticalScrollBar().setValue(0)
        self.settle()
        dock.grab().save(str(output / (name + "-top.png")))
        scroll.verticalScrollBar().setValue(scroll.verticalScrollBar().maximum())
        self.settle()
        dock.grab().save(str(output / (name + "-bottom.png")))

    def testExtrudeTwoSidesAndDirection(self):
        task = self.launch("Extrude")
        task.profile.setCurrentIndex(task.profile.findData(self.sketch.Name))
        task.sides.setCurrentIndex(task.sides.findData("Two sides"))
        task.custom.setChecked(True)
        self.check_width("Extrude")
        self.assertGreaterEqual(task.limit.width(), 120)
        self.assertGreaterEqual(task.start_reference.width(), 120)
        task.length.setProperty("rawValue", 12.)
        self.assertEqual(task.values()[1], 12.)

    def testPrimitiveDynamicWedgeAndAttachment(self):
        task = self.launch("Primitive")
        task.kind.setCurrentIndex(task.kind.findData("Wedge"))
        self.check_width("Primitive")
        self.assertEqual(len(task.fields), len(task.backend.PARAMETERS["Wedge"]))

    def testRevolve(self):
        self.launch("Revolve")
        self.check_width("Revolve")

    def testHelix(self):
        self.launch("Helix")
        self.check_width("Helix")

    def testLoft(self):
        self.launch("Loft")
        self.check_width("Loft")

    def testPipe(self):
        self.launch("Pipe")
        self.check_width("Pipe")

    def testSketchProjectedPlane(self):
        self.launch("Sketch", datum_only=True)
        self.check_width("ProjectedPlane")

    def testSketchAxisDirections(self):
        task = self.launch("Sketch", datum_only=True)
        task.mode.setCurrentIndex(task.mode.findData("Enter values"))
        self.check_width("Sketch")

    def testSketchIndependentFrames(self):
        task = self.launch("Sketch")
        task.plane.setCurrentIndex(task.plane.findData("Independent plane"))
        for mode in ("Rotation angles", "Axis directions"):
            task.orientation_mode.setCurrentIndex(task.orientation_mode.findData(mode))
            self.check_width("Independent-" + mode.replace(" ", "-"), height=400)
