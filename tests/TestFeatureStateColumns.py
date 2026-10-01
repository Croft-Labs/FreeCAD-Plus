# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native state columns in the feature organizer; no geometry evaluation."""
from pathlib import Path
import tempfile
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore
from freecad.gui import FeatureOrganizer as Organizer
from TestFeatureOrganizer import make_fixture


class TestFeatureStateColumns(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = make_fixture()
        self.dialog = Organizer.OrganizerDialog(self.doc, Gui.getMainWindow())
        self.dialog.show()
        Gui.updateGui()

    def tearDown(self):
        if not self.dialog.closed:
            self.dialog.reject()
        for dialog in list(Organizer._dialogs):
            dialog.reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()
        QtCore.QCoreApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)

    def snapshot(self):
        return ([o.Name for o in self.doc.Objects], self.doc.UndoCount,
                [(o.Name, o.Visibility, tuple(o.Placement.toMatrix().A), o.Shape.exportBrepToString())
                 for o in self.doc.Objects if hasattr(o, "Shape")])

    def item(self, name):
        for i in range(self.dialog.table.topLevelItemCount()):
            item = self.dialog.table.topLevelItem(i)
            if item.text(1) == name:
                return item
        self.fail("Missing row " + name)

    def testVisibilitySuppressionAndMissingLinkAreSeparate(self):
        body = self.doc.addObject("PartDesign::Body", "Body")
        feature = body.newObject("PartDesign::AdditiveBox", "Block")
        self.doc.recompute()
        feature.Suppressed = True
        self.doc.recompute()
        missing = self.doc.addObject("App::Link", "Unresolved")
        self.doc.recompute()
        hidden = Organizer.state_record(self.doc.Stock)
        self.assertIn("hidden", hidden["flags"])
        self.assertNotIn("suppressed", hidden["flags"])
        suppressed = Organizer.state_record(feature)
        self.assertIn("suppressed", suppressed["flags"])
        self.assertEqual(suppressed["suppression"], "Suppressed")
        unresolved = Organizer.state_record(missing)
        self.assertIn("unresolved", unresolved["flags"])
        self.assertEqual(unresolved["source"], "Unresolved link")
        self.assertIsNone(missing.LinkedObject)

    def testNativeFailureAndRecomputeStateRemainDistinct(self):
        self.doc.Stock.Length = 35
        state = Organizer.state_record(self.doc.Stock)
        self.assertIn("stale", state["flags"])
        self.assertEqual(state["status"], "Needs recompute")
        self.doc.recompute()
        self.doc.MountingHole.Tool = None
        self.doc.recompute()
        state = Organizer.state_record(self.doc.MountingHole)
        self.assertIn("error", state["flags"])
        self.assertEqual(state["status"], "Error")
        self.assertIn(self.doc.MountingHole.getStatusString(), state["detail"])
        self.doc.MountingHole.Tool = self.doc.Drill
        self.doc.recompute()
        self.assertEqual(Organizer.state_record(self.doc.MountingHole)["status"], "No native error")

    def testFilterColumnsSortAndInspectAreReadOnly(self):
        before = self.snapshot()
        Gui.Selection.clearSelection()
        self.dialog.stateFilter.setCurrentIndex(self.dialog.stateFilter.findData("hidden"))
        self.assertEqual(self.dialog.table.topLevelItemCount(), 2)
        self.dialog.table.setCurrentItem(self.item("Stock"))
        self.assertIn("Local: ", self.dialog.stateDetails.text())
        actions = self.dialog.columnsMenu.actions()
        actions[0].setChecked(False)
        self.assertTrue(self.dialog.table.isColumnHidden(4))
        self.dialog.table.sortByColumn(7, QtCore.Qt.DescendingOrder)
        self.dialog.refresh()
        self.assertTrue(self.dialog.table.isColumnHidden(4))
        self.assertEqual(self.dialog.stateFilter.currentData(), "hidden")
        self.assertEqual(Gui.Selection.getSelection(), [])
        self.assertEqual(before, self.snapshot())

    def testNativeVisibilityAndRecomputeInvalidateSnapshot(self):
        self.assertTrue(self.dialog.fresh)
        self.doc.Stock.ViewObject.Visibility = True
        Gui.updateGui()
        self.assertFalse(self.dialog.fresh)
        self.assertEqual(self.dialog.table.topLevelItemCount(), 0)
        self.dialog.refresh()
        self.assertEqual(self.item("Stock").text(4), "Visible flag")
        self.doc.Stock.Length = 35
        self.dialog.refresh()
        self.assertEqual(self.item("Stock").text(6), "Needs recompute")
        self.doc.recompute()
        self.assertFalse(self.dialog.fresh)
        self.dialog.refresh()
        self.assertEqual(self.item("Stock").text(6), "No native error")

    def testReadonlyMetadataDisablesApplyAndIsFilterable(self):
        self.doc.Stock.setPropertyStatus("Label2", "ReadOnly")
        self.assertFalse(self.dialog.fresh)
        self.dialog.refresh()
        self.dialog.stateFilter.setCurrentIndex(self.dialog.stateFilter.findData("readonly"))
        self.assertEqual(self.dialog.table.topLevelItemCount(), 1)
        self.dialog.table.setCurrentItem(self.item("Stock"))
        self.assertEqual(self.item("Stock").text(8), "Read-only")
        self.assertFalse(self.dialog.applyButton.isEnabled())
        self.doc.Stock.setPropertyStatus("Label2", "-ReadOnly")
        self.assertFalse(self.dialog.fresh)
        self.dialog.refresh()
        self.assertEqual(self.dialog.table.topLevelItemCount(), 0)

    def testExternalSourceFileAndChangesInvalidateWithoutLoading(self):
        with tempfile.TemporaryDirectory() as folder:
            other = App.newDocument("ExternalSource")
            source = other.addObject("Part::Box", "Source")
            other.recompute()
            source_file = str(Path(folder) / "Source.FCStd")
            other.saveAs(source_file)
            App.setActiveDocument(self.doc.Name)
            local_file = str(Path(folder) / "Assembly.FCStd")
            self.doc.saveAs(local_file)
            link = self.doc.addObject("App::Link", "ExternalOccurrence")
            link.setLink(source)
            self.doc.recompute()
            self.dialog.refresh()
            row = self.item(link.Name)
            self.assertIn("ExternalSource#Source", row.text(7))
            self.assertIn("Source.FCStd", row.toolTip(7))
            before = list(App.listDocuments())
            source.Length = 17
            self.assertFalse(self.dialog.fresh)
            self.assertEqual(list(App.listDocuments()), before)
            other.recompute()
            self.doc.recompute()
            self.dialog.refresh()
            self.doc.save()
            self.assertFalse(self.dialog.fresh)
            self.dialog.reject()
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(local_file)
            self.dialog = Organizer.OrganizerDialog(self.doc, Gui.getMainWindow())
            self.assertIn("Source.FCStd", self.item("ExternalOccurrence").toolTip(7))

    def testSaveUndoAndRedoInvalidateWithoutChangingGeometry(self):
        with tempfile.TemporaryDirectory() as folder:
            self.doc.saveAs(str(Path(folder) / "State.FCStd"))
            self.assertFalse(self.dialog.fresh)
            self.dialog.refresh()
            self.assertIn("State.FCStd", self.item("Stock").toolTip(7))
            self.doc.openTransaction("Owner label")
            self.doc.Stock.Label = "Owner edit"
            self.doc.commitTransaction()
            self.dialog.refresh()
            self.doc.undo()
            self.assertFalse(self.dialog.fresh)
            self.dialog.refresh()
            self.doc.redo()
            self.assertFalse(self.dialog.fresh)

    def testCloseDetachesObserversAndDocumentClosureClosesDialog(self):
        class UnattachedView:
            @property
            def Object(self):
                raise RuntimeError("No attached object")
        self.dialog.viewObserver.slotChangedObject(UnattachedView(), "Visibility")
        self.dialog.slotChangePropertyEditor(self.doc.Stock.ViewObject, "ShapeColor")
        self.dialog.reject()
        self.doc.Stock.ViewObject.Visibility = True
        self.doc.Stock.Length = 35
        self.doc.recompute()
        self.assertTrue(self.dialog.closed)
        self.dialog = Organizer.OrganizerDialog(self.doc, Gui.getMainWindow())
        App.closeDocument(self.doc.Name)
        self.assertTrue(self.dialog.closed)
