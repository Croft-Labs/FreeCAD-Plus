# SPDX-License-Identifier: LGPL-2.1-or-later
import unittest
import FreeCAD as App, FreeCADGui as Gui
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, editing, panel, display, assembly_ui, assembly_visibility as eyes
from TestInstanceDisplay import TestInstanceDisplay, settle


class TestAssemblyEyes(unittest.TestCase):
    setUp = TestInstanceDisplay.setUp
    tearDown = TestInstanceDisplay.tearDown
    menu = TestInstanceDisplay.menu

    def row(self, link):
        return next(i for i in self.dock._maps[1].values() if i.data(0, panel._ROLE).kind == 'occurrence'
                    and i.data(0, panel._ROLE).path[-1] == panel.identity(link))

    def click(self, item):
        tree = self.dock.trees[1];tree.scrollToItem(item);settle()
        rect = eyes.eye_rect(tree, item);self.assertIsNotNone(rect)
        QtTest.QTest.mouseClick(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, rect.center());settle()

    def test_inline_eyes_toggle_without_selection_edit_or_expansion_changes(self):
        tree = self.dock.trees[1];tree.expandAll();settle()
        root = tree.topLevelItem(0);parent = self.row(self.gears[0]);child = parent.child(0)
        self.assertIsNone(eyes.eye_rect(tree, root))
        self.assertGreater(eyes.eye_rect(tree, child).left(), eyes.eye_rect(tree, parent).left())
        context = editing.context_path(self.doc);selected = tuple(tree.selectedItems());undo = self.doc.UndoCount
        self.click(child)
        self.assertFalse(display.state(self.bolts[0])[1]);self.assertTrue(parent.isExpanded())
        self.assertEqual(editing.context_path(self.doc), context);self.assertEqual(tuple(tree.selectedItems()), selected)
        self.assertEqual(self.doc.UndoCount, undo+1)
        self.doc.undo();settle();self.assertTrue(display.state(self.bolts[0])[1])
        rect = eyes.eye_rect(tree, parent)
        arrow = QtCore.QPoint(rect.left()-tree.indentation()//2, rect.center().y())
        QtTest.QTest.mouseClick(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, arrow);settle()
        self.assertFalse(parent.isExpanded())
        QtTest.QTest.mouseClick(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, arrow);settle()
        self.assertTrue(parent.isExpanded())
        self.dock.grab().save(str(self.output/'expanded-eyes.png'))

    def test_condensed_mixed_group_atomic_toggle_and_excluded_guard(self):
        display.set_state(self.owner, self.motors[1], shown=False)
        assembly_ui.set_all(self.dock, True);settle()
        group = next(i for i in self.dock._maps[1].values() if i.data(0, panel._ROLE).kind == 'instance_group'
                     and i.data(0, panel._ROLE).ref == panel.identity(self.motor))
        self.assertEqual(group.data(0, panel._ROLE+4)[0], 'mixed')
        self.assertEqual(group.childIndicatorPolicy(), QtWidgets.QTreeWidgetItem.DontShowIndicator)
        undo = self.doc.UndoCount;self.click(group)
        self.assertTrue(all(display.state(o)[1] for o in self.motors));self.assertEqual(self.doc.UndoCount, undo+1)
        self.click(group);self.assertTrue(all(not display.state(o)[1] for o in self.motors))
        self.doc.undo();settle();self.assertTrue(all(display.state(o)[1] for o in self.motors))
        display.set_state(self.owner, self.motors[1], part_type='Excluded');self.dock.refresh()
        before = [display.state(o) for o in self.motors];undo = self.doc.UndoCount
        with self.assertRaisesRegex(ValueError, 'Excluded'):eyes.toggle(self.dock, group.data(0, panel._ROLE))
        self.assertEqual([display.state(o) for o in self.motors], before);self.assertEqual(self.doc.UndoCount, undo)
        self.dock.grab().save(str(self.output/'condensed-eyes.png'))

    def test_active_assembly_cannot_be_hidden_in_root_or_parts_menu(self):
        root = self.dock.trees[1].topLevelItem(0);row = root.data(0, panel._ROLE)
        for values in ({'shown':False}, {'part_type':'Excluded'}):
            with self.assertRaisesRegex(ValueError, 'must remain visible'):self.dock.set_display(row, **values)
        parts = next(i.data(0,panel._ROLE) for i in self.dock._maps[0].values()
                     if i.data(0,panel._ROLE).ref==panel.identity(self.owner))
        with self.assertRaisesRegex(ValueError, 'must remain visible'):self.dock.set_display(parts, shown=False)
        menu = self.menu(root)
        options = next(children for title, enabled, children in menu if title == 'Visibility')
        self.assertFalse(next(enabled for title, enabled, _ in options if title == 'Hidden'))
        tree = self.dock.trees[1];tree.setCurrentItem(root);undo = self.doc.UndoCount
        QtTest.QTest.keyClick(tree, QtCore.Qt.Key_Space);settle();self.assertEqual(self.doc.UndoCount,undo)

    def test_chosen_hidden_assembly_is_shown_without_rewriting_saved_setting(self):
        display.set_state(self.owner, self.gears[0], shown=False)
        self.dock.activate_assembly(self.gear, (self.top,self.gears[0]));settle()
        owner, path = eyes.protection(self.doc, Gui.activeDocument().activeView())
        hidden = display.hidden_paths(self.doc,self.owner,(self.top,),protected_path=path)
        from freecad_plus import hierarchy
        self.assertFalse(any(hierarchy.subname(path).startswith(p) for p in hidden))
        self.assertFalse(display.state(self.gears[0])[1])
        display.set_state(self.gear, shown=False)
        editing.edit_in_assembly(self.doc,self.gear);self.dock.refresh();settle()
        from freecad_plus import isolation
        from pivy import coin
        self.assertEqual(isolation.current(Gui.activeDocument().activeView()).preview.whichChild.getValue(),coin.SO_SWITCH_ALL)
        self.assertFalse(display.state(self.gear)[1])

    def test_imported_nested_eye_changes_defining_parent_and_persists(self):
        from freecad_plus import external, hierarchy
        source=document.new_document('ExternalSource');owner=document.validate(source).Definitions[0]
        owner.Label='External assembly'
        leaf=hierarchy.create_definition(source,'External fastener')
        child=hierarchy.add_instance(owner,leaf)
        document.save_document(source,self.output/'ExternalSource.cadprt')
        App.setActiveDocument(self.doc.Name)
        document.save_document(self.doc,self.output/'Host.cadprt')
        external.import_file(self.doc,source);link=hierarchy.add_instance(self.owner,owner)
        self.dock.refresh();settle()
        row=self.row(child);context=editing.context_path(self.doc);undo=source.UndoCount
        self.click(row)
        self.assertFalse(display.state(child)[1]);self.assertEqual(source.UndoCount,undo+1)
        self.assertEqual(editing.context_path(self.doc),context)
        self.assertTrue(display.state(link)[1])
        source.undo();settle();self.assertTrue(display.state(child)[1])
        source.redo();document.save_document(source)
        self.assertFalse(display.state(child)[1])
