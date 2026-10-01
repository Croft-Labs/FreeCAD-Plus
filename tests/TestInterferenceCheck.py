# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native pair inspection, explicit scope, occurrence placement and GUI lifecycle."""
from pathlib import Path
import tempfile
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtWidgets
import InterferenceCheck as Check
import InterferenceCheckGui as Editor


def make_fixture():
    doc = App.newDocument("InterferenceWorkflow")
    doc.UndoMode = 1
    for name, x in (("First", 0), ("Overlap", 8), ("Contact", 18), ("SmallGap", 28.25)):
        box = doc.addObject("Part::Box", name)
        box.Length = box.Width = box.Height = 10
        box.Placement.Base.x = x
    doc.recompute()
    return doc


class TestInterferenceCheck(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = make_fixture()
        Gui.Selection.clearSelection()

    def tearDown(self):
        for dialog in list(Editor._dialogs):
            dialog.close()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()

    def refs(self):
        return [Check.Reference(self.doc.getObject(name))
                for name in ("First", "Overlap", "Contact", "SmallGap")]

    def launch(self):
        Gui.Selection.clearSelection()
        for ref in self.refs():
            Gui.Selection.addSelection(self.doc.getObject(ref.root))
        Gui.runCommand("Part_InterferenceCheck")
        Gui.updateGui()
        return Editor._dialogs[-1]

    def testAnalyticOverlapContactGapAndReadOnly(self):
        self.doc.Contact.Visibility = False
        before = [(o.Name, o.Shape.exportBrepToString(), o.Visibility) for o in self.doc.Objects]
        rows = Check.inspect(self.refs())
        self.assertEqual(len(rows), 6)
        pairs = {(r["a"], r["b"]): r for r in rows}
        self.assertEqual(pairs[0, 1]["status"], "Overlap")
        self.assertAlmostEqual(pairs[0, 1]["volume"], 200)
        self.assertEqual(pairs[1, 2]["status"], "Contact / within tolerance")
        self.assertAlmostEqual(pairs[1, 2]["volume"], 0)
        self.assertEqual(pairs[2, 3]["status"], "Below clearance")
        self.assertAlmostEqual(pairs[2, 3]["distance"], 0.25)
        self.assertEqual(pairs[0, 3]["status"], "Clear")
        self.assertEqual(before, [(o.Name, o.Shape.exportBrepToString(), o.Visibility) for o in self.doc.Objects])
        self.assertFalse(self.doc.HasPendingTransaction)

    def testToleranceAndClearanceBoundary(self):
        refs = self.refs()[2:]
        self.assertEqual(Check.inspect(refs, 0.25)[0]["status"], "Clear")
        self.assertEqual(Check.inspect(refs, 1, 0.3)[0]["status"], "Contact / within tolerance")
        with self.assertRaises(ValueError):
            Check.inspect(refs, 0.1, 0.2)
        with self.assertRaises(ValueError):
            Check.inspect(refs, float("nan"))

    def testStructuralPartAndDirectLinkWorldGeometry(self):
        group = self.doc.addObject("App::Part", "Assembly")
        group.Placement = App.Placement(App.Vector(100, 20, 5), App.Rotation(App.Vector(0, 0, 1), 90))
        for name, x in (("InstanceA", 0), ("InstanceB", 8)):
            link = self.doc.addObject("App::Link", name)
            link.setLink(self.doc.First)
            group.addObject(link)
            link.LinkPlacement.Base.x = x
        self.doc.recompute()
        refs = [Check.Reference(group, name + ".") for name in ("InstanceA", "InstanceB")]
        center = refs[0].shape().CenterOfMass
        self.assertAlmostEqual(center.x, 95)
        self.assertAlmostEqual(center.y, 25)
        self.assertAlmostEqual(center.z, 10)
        result = Check.inspect(refs)[0]
        self.assertEqual(result["status"], "Overlap")
        self.assertAlmostEqual(result["volume"], 200)
        before = group.Placement
        with tempfile.TemporaryDirectory() as directory:
            file = str(Path(directory) / "Interference.FCStd")
            self.doc.saveAs(file)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(file)
            refs = [Check.Reference(self.doc.Assembly, name + ".") for name in ("InstanceA", "InstanceB")]
            self.assertEqual(Check.inspect(refs)[0]["status"], "Overlap")
            self.assertAlmostEqual(Check.inspect(refs)[0]["volume"], 200)
            self.assertEqual(self.doc.Assembly.Placement, before)

    def testUnresolvedInputsAreNeverSilentlyOmitted(self):
        missing = self.doc.addObject("App::Link", "Unavailable")
        self.doc.recompute()
        rows = Check.inspect(self.refs() + [Check.Reference(missing)])
        self.assertEqual(len(rows), 10)
        self.assertEqual(sum(r["status"] == "Unresolved" for r in rows), 4)
        mixed = self.doc.addObject("Part::Feature", "Mixed")
        mixed.Shape = Part.makeCompound([Part.makeBox(2, 2, 2), Part.makeLine(App.Vector(), App.Vector(4, 4, 4))])
        self.doc.recompute()
        self.assertEqual(Check.inspect([self.refs()[0], Check.Reference(mixed)])[0]["status"], "Unresolved")
        self.doc.First.Length = 12
        self.assertEqual(Check.inspect(self.refs()[:2])[0]["status"], "Unresolved")
        self.doc.recompute()
        self.assertEqual(Check.inspect(self.refs()[:2])[0]["status"], "Overlap")

    def testIdentityAndUnsupportedScope(self):
        refs = self.refs()[:2]
        self.doc.removeObject("Overlap")
        replacement = self.doc.addObject("Part::Box", "Overlap")
        self.doc.recompute()
        self.assertEqual(replacement.Name, "Overlap")
        self.assertEqual(Check.inspect(refs)[0]["status"], "Unresolved")
        with self.assertRaises(ValueError):
            Check.Reference(self.doc.First, "Face1")
        with self.assertRaises(ValueError):
            Check.inspect([refs[0], refs[0]])
        self.doc.openTransaction("Pending edit")
        self.doc.First.Label = "In progress"
        with self.assertRaises(ValueError):
            Check.inspect(refs)
        self.doc.abortTransaction()

    def testInstalledCommandExclusionsNavigationAndInvalidation(self):
        dialog = self.launch()
        actions = [action.text().replace("&", "")
                   for menu in Gui.getMainWindow().menuBar().findChildren(QtWidgets.QMenu)
                   for action in menu.actions()]
        self.assertIn("Interference and clearance...", actions)
        dialog.checkButton.click()
        self.assertEqual(len(dialog.rows), 6)
        dialog.table.selectRow(0)
        before = [o.Visibility for o in self.doc.Objects]
        dialog.selectPair.click()
        self.assertEqual({o.Name for o in Gui.Selection.getSelection()}, {"First", "Overlap"})
        self.assertEqual([o.Visibility for o in self.doc.Objects], before)
        self.assertEqual(len(dialog.references), 4)
        dialog.inputs.item(1).setCheckState(QtCore.Qt.Unchecked)
        self.assertFalse(dialog.rows)
        dialog.checkButton.click()
        self.assertEqual(len(dialog.rows), 3)
        self.assertIn("excluded inputs: 1", dialog.status.text())
        self.assertNotIn("Overlap", [r["status"] for r in dialog.rows])
        dialog.clearance.setValue(0.1)
        self.assertFalse(dialog.rows)
        dialog.checkButton.click()
        self.doc.SmallGap.Placement.Base.x = 27
        self.assertFalse(dialog.rows)
        self.assertFalse(dialog.selectPair.isEnabled())
        self.doc.recompute()
        dialog.checkButton.click()
        self.assertIn("Overlap", [r["status"] for r in dialog.rows])
        dialog.close()
        self.assertTrue(dialog._closed)
        self.assertFalse(self.doc.HasPendingTransaction)

    def testMissingParticipantIsIncompleteAndDocumentCloseDetaches(self):
        dialog = self.launch()
        self.doc.removeObject("SmallGap")
        dialog.checkButton.click()
        self.assertEqual(len(dialog.rows), 6)
        self.assertIn("Incomplete", dialog.status.text())
        self.assertEqual(sum(r["status"] == "Unresolved" for r in dialog.rows), 3)
        App.closeDocument(self.doc.Name)
        self.assertTrue(dialog._closed)
        self.assertNotIn(dialog, Editor._dialogs)
