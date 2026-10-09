# SPDX-License-Identifier: LGPL-2.1-or-later
"""New File owns an ordinary initial part beneath a pinned file context."""
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
import ComponentModel as Model
import CadDocument
from freecad.gui import ComponentNavigator as Navigator
from freecad.gui import ComponentExtrudeTask as ExtrudeTask


class TestComponentFileWorkspace(unittest.TestCase):
    def setUp(self):
        Navigator.Command(True).Activated()
        self.doc = App.ActiveDocument
        self.root = Model.metadata(self.doc).RootComponent
        self.link = Model.children(self.root)[0]
        self.part = self.link.LinkedObject
        self.panel = Navigator._dock
        Gui.updateGui()
        self.panel.refresh()

    def tearDown(self):
        Gui.Selection.clearSelection()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def testNewFileActivatesOrdinaryPartAndPinsFile(self):
        self.assertTrue(Model.is_file_container(self.root))
        self.assertEqual(self.part.Label, "Part001")
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.part))
        self.assertEqual(self.panel.active_path, [self.link.ObjectId])
        self.assertEqual(ExtrudeTask.active_component(), self.part)
        self.assertEqual(self.panel.structure.topLevelItemCount(), 1)
        file_row = self.panel.structure.topLevelItem(0)
        self.assertEqual(file_row.text(0), self.doc.Label)
        self.assertFalse(file_row.icon(0).isNull())
        self.assertFalse(file_row.flags() & QtCore.Qt.ItemIsDragEnabled)
        self.assertTrue(file_row.child(0).font(0).bold())
        self.assertEqual(self.panel.models.topLevelItemCount(), 1)
        self.assertEqual(self.panel.models.topLevelItem(0).text(0), "Part001")
        self.assertTrue(self.panel.models.topLevelItem(0).font(0).bold())
        self.assertEqual(self.panel.history.topLevelItem(0).data(0, QtCore.Qt.UserRole),
                         Navigator.object_key(self.part.Origin))
        self.assertEqual(self.doc.UndoCount, 0)

    def testFileEditDoesNotOpenTabAndRequiresComponentForModeling(self):
        windows = len(self.panel.mdi.subWindowList())
        row = self.panel.structure.topLevelItem(0)
        row.setSelected(True)
        self.panel.select_structure()
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.part))
        self.panel.activate_item(row)
        self.panel.refresh()
        self.assertEqual(len(self.panel.mdi.subWindowList()), windows)
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.root))
        self.assertEqual(self.panel.active_path, [])
        self.assertEqual(self.panel.history.topLevelItemCount(), 1)
        self.assertEqual(self.panel.history.topLevelItem(0).data(0, QtCore.Qt.UserRole),
                         Navigator.object_key(self.root.Origin))
        with self.assertRaises(ValueError):
            ExtrudeTask.active_component()
        self.assertEqual(ExtrudeTask.active_component(allow_file=True), self.root)
        menu = self.panel.build_menu(self.panel.history, None)
        self.assertNotIn("New Sketch", [action.text() for action in menu.actions()])
        self.panel.activate_item(self.panel.structure.topLevelItem(0).child(0))
        self.panel.refresh()
        self.assertEqual(ExtrudeTask.active_component(), self.part)

    def testFirstOccurrenceCanBeRemovedAndUndoRestoresIt(self):
        self.panel.delete_instances(self.panel.structure.topLevelItem(0).child(0))
        self.panel.refresh()
        self.assertEqual(Model.children(self.root), [])
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.root))
        self.assertEqual(self.panel.structure.topLevelItem(0).childCount(), 0)
        self.assertEqual(self.panel.models.topLevelItemCount(), 1)
        Model.validate(self.doc)
        self.doc.undo()
        self.panel.refresh()
        self.assertEqual(Model.children(self.root)[0].LinkedObject, self.part)
        self.assertEqual(self.panel.structure.topLevelItem(0).childCount(), 1)

    def testRenameFileAndPartHaveSeparateNames(self):
        with patch.object(QtWidgets.QInputDialog, "getText", return_value=("Assembly file", True)):
            self.panel.rename_item(Navigator.object_key(self.root))
        self.assertEqual(self.doc.Label, "Assembly file")
        self.assertEqual(self.part.Label, "Part001")
        with patch.object(QtWidgets.QInputDialog, "getText", return_value=("Bracket", True)):
            self.panel.rename_item(Navigator.object_key(self.part))
        self.panel.refresh()
        self.assertEqual(self.panel.structure.topLevelItem(0).text(0), "Assembly file")
        self.assertEqual(self.panel.models.topLevelItem(0).text(0), "Bracket")

    def testNewFileSaveReopenKeepsPartAndFileIdentities(self):
        ids = self.root.ObjectId, self.part.ObjectId, self.link.ObjectId
        box = self.doc.addObject("Part::Box", "Box")
        Model.register_object(self.part, box, "Operation")
        self.doc.recompute()
        filename = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "new-file.cadprt"
        self.doc.saveAs(str(filename))
        App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(str(filename))
        self.root = Model.metadata(self.doc).RootComponent
        link = Model.children(self.root)[0]
        self.assertEqual((self.root.ObjectId, link.LinkedObject.ObjectId, link.ObjectId), ids)
        self.assertEqual(Model.owner(self.doc.getObject("Box")), link.LinkedObject)
        self.panel.refresh()
        self.assertEqual(self.panel.models.topLevelItemCount(), 1)

    def testNativeNewCommandUsesFileContainer(self):
        Gui.runCommand("Std_New")
        Gui.updateGui()
        doc = App.ActiveDocument
        self.assertNotEqual(doc, self.doc)
        root = Model.metadata(doc).RootComponent
        self.assertTrue(Model.is_file_container(root))
        self.assertEqual(Model.children(root)[0].LinkedObject.Label, "Part001")
        self.assertEqual(ExtrudeTask.active_component(), Model.children(root)[0].LinkedObject)

    def testImportedFileListsOnlyItsModels(self):
        output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        self.doc.saveAs(str(output / "assembly.cadprt"))
        source = Model.new_file_document("Hardware")
        source.saveAs(str(output / "Hardware.cadprt"))
        Model.import_file(self.doc, source)
        App.setActiveDocument(self.doc.Name)
        self.panel.set_document(self.doc, [self.link.ObjectId])
        self.panel.refresh()
        self.assertEqual(self.panel.models.topLevelItemCount(), 2)
        group = self.panel.models.topLevelItem(1)
        self.assertEqual(group.text(0), "Hardware")
        self.assertEqual(group.childCount(), 1)
        self.assertEqual(group.child(0).text(0), "Part001 (Hardware)")

    def testPinnedFileCannotBeDeletedFromNativeSelection(self):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.root)
        Gui.updateGui()
        Gui.runCommand("Std_Delete")
        self.assertEqual(Model.metadata(self.doc).RootComponent, self.root)
        Navigator.delete_selected_instances()
        self.assertEqual(Gui.Selection.getSelection(), [])
        self.assertEqual(Model.children(self.root)[0].LinkedObject, self.part)
