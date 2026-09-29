# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Qt event regressions for #32717, #32718 and #32700; no rebuild needed."""
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets


def key(widget, code, text="", modifiers=QtCore.Qt.NoModifier):
    for kind in (QtCore.QEvent.KeyPress, QtCore.QEvent.KeyRelease):
        QtWidgets.QApplication.sendEvent(widget, QtGui.QKeyEvent(kind, code, modifiers, text))


class TestIssueQuantityInput(unittest.TestCase):
    def setUp(self):
        self.schema = App.Units.getSchema()
        App.Units.setSchema(0)
        self.doc = App.newDocument("IssueQuantityInput")
        self.doc.UnitSystem = 0
        self.box = self.doc.addObject("Part::Box", "Box")
        self.box.Length = 10
        self.panel = QtWidgets.QWidget()
        self.panel.setAttribute(QtCore.Qt.WA_DontShowOnScreen, True)
        layout = QtWidgets.QVBoxLayout(self.panel)
        self.spin = Gui.UiLoader().createWidget("Gui::QuantitySpinBox")
        self.spin.setProperty("unit", "mm")
        self.spin.setProperty("singleStep", 1.0)
        self.spin.setProperty("rawValue", 10.0)
        self.other = QtWidgets.QLineEdit()
        layout.addWidget(self.spin)
        layout.addWidget(self.other)
        self.panel.show()
        self.panel.activateWindow()
        self.spin.setFocus()
        Gui.updateGui()

    def tearDown(self):
        self.panel.close()
        self.panel.deleteLater()
        App.closeDocument(self.doc.Name)
        App.Units.setSchema(self.schema)

    def loseFocus(self):
        self.other.setFocus()
        # Explicit native focus event also covers a headless platform without WM focus.
        QtWidgets.QApplication.sendEvent(self.spin, QtGui.QFocusEvent(QtCore.QEvent.FocusOut))
        Gui.updateGui()

    def testArrowChangesSurviveFocusLoss(self):
        key(self.spin, QtCore.Qt.Key_Up)
        self.assertAlmostEqual(self.spin.property("rawValue"), 11)
        self.loseFocus()
        self.assertAlmostEqual(self.spin.property("rawValue"), 11)

    def testWheelChangesSurviveFocusLoss(self):
        center = self.spin.rect().center()
        event = QtGui.QWheelEvent(QtCore.QPointF(center),
            QtCore.QPointF(self.spin.mapToGlobal(center)), QtCore.QPoint(), QtCore.QPoint(0, 120),
            QtCore.Qt.NoButton, QtCore.Qt.NoModifier, QtCore.Qt.NoScrollPhase, False)
        QtWidgets.QApplication.sendEvent(self.spin, event)
        self.assertAlmostEqual(self.spin.property("rawValue"), 11)
        self.loseFocus()
        self.assertAlmostEqual(self.spin.property("rawValue"), 11)

    def testDocumentInchesApplyToImplicitInput(self):
        self.doc.UnitSystem = 3  # Imperial decimal: inches, unlike global mm schema.
        self.spin.setProperty("binding", self.doc.Name + "#Box.Length")
        self.spin.setProperty("rawValue", 25.4)
        editor = self.spin.findChild(QtWidgets.QLineEdit)
        self.assertIn("in", editor.text())
        editor.selectAll()
        key(editor, QtCore.Qt.Key_2, "2")
        self.loseFocus()
        self.assertAlmostEqual(self.spin.property("rawValue"), 50.8)

    def testBoundValueCommitUsesDisplayedUnits(self):
        self.spin.setProperty("binding", self.doc.Name + "#Box.Length")
        editor = self.spin.findChild(QtWidgets.QLineEdit)
        editor.selectAll()
        for char in "17 mm":
            key(editor, 0, char)
        key(self.spin, QtCore.Qt.Key_Return)
        self.loseFocus()
        self.assertAlmostEqual(self.spin.property("rawValue"), 17)
