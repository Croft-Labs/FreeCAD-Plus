# SPDX-License-Identifier: LGPL-2.1-or-later
"""#32706: use the real Part Mirror task to pick a face inside a moved Body."""
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtWidgets


class TestIssueMirrorGui(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("IssueMirrorGui")
        self.body = self.doc.addObject("PartDesign::Body", "Body")
        self.box = self.body.newObject("PartDesign::AdditiveBox", "Box")
        self.box.Length = self.box.Width = 10
        self.box.Height = 15
        self.doc.recompute()
        self.top = max(enumerate(self.box.Shape.Faces, 1),
                       key=lambda item: item[1].CenterOfMass.z)[0]
        Gui.activateWorkbench("PartWorkbench")

    def tearDown(self):
        if Gui.Control.activeDialog():
            Gui.Control.activeTaskDialog().reject()
        Gui.Selection.clearSelection()
        App.closeDocument(self.doc.Name)

    def widget(self, kind, name):
        for panel in Gui.Control.activeTaskDialog().getDialogContent():
            found = panel.findChild(kind, name)
            if found is not None:
                return found
        self.fail("Missing Mirror task widget " + name)

    def checkReference(self, rotation):
        self.body.Placement = App.Placement(App.Vector(3, 4, 2), rotation)
        self.doc.recompute()
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.body)
        Gui.runCommand("Part_Mirror")
        Gui.updateGui()
        self.assertTrue(Gui.Control.activeDialog())
        tree = self.widget(QtWidgets.QTreeWidget, "shapes")
        matches = tree.findItems(self.body.Label, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
        self.assertTrue(matches)
        tree.clearSelection()
        matches[0].setSelected(True)
        self.widget(QtWidgets.QComboBox, "comboBox").setCurrentIndex(3)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.box, f"Face{self.top}")
        Gui.updateGui()
        self.assertTrue(Gui.Selection.getSelectionEx())
        Gui.Control.activeTaskDialog().accept()
        Gui.updateGui()
        self.assertFalse(Gui.Control.activeDialog())
        mirrors = [obj for obj in self.doc.Objects if obj.TypeId == "Part::Mirroring"]
        self.assertEqual(len(mirrors), 1)
        mirror = mirrors[0]
        self.assertEqual(mirror.Source, self.body)
        self.assertIsNotNone(mirror.MirrorPlane[0])
        expected = Part.makeBox(10, 10, 15, App.Vector(0, 0, 15))
        expected.Placement = self.body.Placement
        self.assertTrue(mirror.Shape.isValid())
        self.assertAlmostEqual(mirror.Shape.Volume, expected.Volume, places=6)
        self.assertAlmostEqual(mirror.Shape.common(expected).Volume, expected.Volume, places=6)

    def testTranslatedBodyFaceFromTask(self):
        self.checkReference(App.Rotation())

    def testRotatedBodyFaceFromTask(self):
        self.checkReference(App.Rotation(App.Vector(1, 1, 0), 37))
