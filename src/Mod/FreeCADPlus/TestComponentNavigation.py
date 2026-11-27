# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component activation stays in place; saved assembly choices belong to the file."""
import json
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtTest
from freecad_plus import assembly, document, panel
from TestComponentPanel import TestComponentPanel, settle


class TestComponentNavigation(unittest.TestCase):
    setUp = TestComponentPanel.setUp
    tearDown = TestComponentPanel.tearDown
    rows = TestComponentPanel.rows
    model = TestComponentPanel.model

    def test_activation_retains_tab_and_parent_expansion(self):
        self.widget.tabs.setCurrentIndex(0)
        self.widget.activate_assembly(self.parent, (self.first,))
        self.assertEqual(self.widget.tabs.currentIndex(), 0)
        self.widget.edit_row(self.model(self.parent).data(0, panel._ROLE))
        self.assertEqual(self.widget.tabs.currentIndex(), 0)
        self.widget.tabs.setCurrentIndex(1)
        tree = self.widget.trees[1]
        root = tree.topLevelItem(0)
        root.setExpanded(True)
        QtTest.QTest.mouseDClick(tree.viewport(), QtCore.Qt.LeftButton,
                                QtCore.Qt.NoModifier, tree.visualItemRect(root).center())
        settle()
        self.assertTrue(root.isExpanded())
        self.assertEqual(self.widget.tabs.currentIndex(), 1)

    def test_saved_choice_beats_later_unsaved_choice_and_preferences(self):
        self.widget.activate_assembly(self.parent, (self.second,))
        path = self.output / 'Saved.cadprt'
        document.save_document(self.doc, path)
        uid, name, object_id = str(self.doc.Uid), self.parent.Name, self.parent.ID
        route = [o.Name for o in (self.second,)]
        self.widget.activate_assembly(self.unused)
        prefs = App.ParamGet('User parameter:BaseApp/Preferences/FreeCADPlus/Assembly')
        prefs.SetString(uid, json.dumps([uid, self.unused.Name, self.unused.ID]))
        App.closeDocument(self.doc.Name)
        self.doc = document.open_document(path)
        part = assembly.recalled(self.doc)
        self.assertEqual((part.Name, part.ID), (name, object_id))
        self.assertEqual([o.Name for o in assembly.recalled_path(self.doc, part)], route)
        # Save As carries the same host metadata and stable native identities.
        document.save_document(self.doc, self.output / 'SavedAs.cadprt')
        App.closeDocument(self.doc.Name)
        self.doc = document.open_document(self.output / 'SavedAs.cadprt')
        self.assertEqual(assembly.recalled(self.doc).Name, name)

    def test_invalid_bookmark_does_not_fall_back_to_preference(self):
        assembly.remember(self.doc, self.parent)
        meta = dict(self.doc.Meta)
        data = json.loads(meta[assembly.BOOKMARK]); data['part'][2] += 10000
        meta[assembly.BOOKMARK] = json.dumps(data); self.doc.Meta = meta
        prefs = App.ParamGet('User parameter:BaseApp/Preferences/FreeCADPlus/Assembly')
        prefs.SetString(str(self.doc.Uid), json.dumps([str(self.doc.Uid), self.unused.Name, self.unused.ID]))
        self.assertIsNone(assembly.recalled(self.doc))

    def test_native_save_uses_active_view_and_preserves_geometry_undo(self):
        self.widget.activate_assembly(self.parent, (self.first,))
        before = [(obj.Name, obj.ID, tuple(obj.OutList)) for obj in self.doc.Objects]
        undo = self.doc.UndoCount
        self.doc.FileName = str(self.output / 'Native.cadprt')
        self.doc.save()
        self.assertEqual(before, [(obj.Name, obj.ID, tuple(obj.OutList)) for obj in self.doc.Objects])
        self.assertEqual(undo, self.doc.UndoCount)
        self.assertEqual(assembly.recalled(self.doc), self.parent)
