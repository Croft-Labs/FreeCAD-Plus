# SPDX-License-Identifier: LGPL-2.1-or-later
"""Assembly grouping is presentation only; occurrence actions keep native identity."""
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import constraints, document, editing, external, hierarchy, movement, panel, assembly_ui


def settle():
    QtTest.QTest.qWait(100)


class TestInstanceDisplay(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:
            self.skipTest('An isolated validation directory is required')
        self.before = set(App.listDocuments())
        self.output = Path(os.environ['PLUS_TEST_DIR']) / self._testMethodName
        self.output.mkdir(exist_ok=True)
        self.prefs = App.ParamGet('User parameter:BaseApp/Preferences/Mod/FreeCADPlus')
        self.old_mode = self.prefs.GetBool('CondensedInstances', False)
        self.prefs.SetBool('CondensedInstances', False)
        Gui.Selection.clearSelection(); settle()
        self.doc = document.new_document('Instances')
        self.root = document.validate(self.doc)
        self.owner = self.root.Definitions[0]; self.owner.Label = 'Machine'
        self.motor = hierarchy.create_definition(self.doc, 'Motor')
        self.gear = hierarchy.create_definition(self.doc, 'Gearbox')
        self.bolt = hierarchy.create_definition(self.doc, 'Bolt')
        self.frame = hierarchy.create_definition(self.doc, 'Frame')
        with document.transaction(self.doc, 'Geometry'):
            self.motor.newObject('Part::Box', 'MotorSolid')
            self.bolt.newObject('Part::Box', 'BoltSolid')
        self.motors = [hierarchy.add_instance(self.owner, self.motor,
                       App.Placement(App.Vector(i * 20, 0, 0), App.Rotation())) for i in range(3)]
        self.gears = [hierarchy.add_instance(self.owner, self.gear) for _ in range(2)]
        self.bolts = [hierarchy.add_instance(self.gear, self.bolt) for _ in range(2)]
        self.frame_link = hierarchy.add_instance(self.owner, self.frame)
        self.top = self.root.Group[0]
        editing.edit((self.top,))
        self.dock = panel.show_panel()
        assembly_ui.set_all(self.dock, False)
        self.dock.activate_assembly(self.owner, (self.top,))
        self.dock.tabs.setCurrentIndex(1)
        Gui.getMainWindow().resizeDocks([self.dock], [370], QtCore.Qt.Horizontal)
        settle(); self.dock.refresh()

    def tearDown(self):
        if movement._active:
            movement._active.finish()
        Gui.Selection.clearSelection()
        assembly_ui.set_all(self.dock, self.old_mode)
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)
        self.prefs.SetBool('CondensedInstances', self.old_mode)
        settle()

    def mode(self, value):
        assembly_ui.set_all(self.dock, value == 'Condensed'); settle()

    def menu(self, item, choose=None):
        tree=self.dock.trees[1];tree.scrollToItem(item);settle();result=[]
        def drive():
            menu=QtWidgets.QApplication.activePopupWidget()
            if not isinstance(menu,QtWidgets.QMenu):return
            def entries(menu):
                return [(a.text(),a.isEnabled(),entries(a.menu()) if a.menu() else [])
                        for a in menu.actions() if not a.isSeparator()]
            result.extend(entries(menu))
            menu.grab().save(str(self.output/('group-menu.png' if item.data(0,panel._ROLE).kind=='instance_group' else 'instance-menu.png')))
            if choose:
                action=next(a for a in menu.actions() if a.text()==choose)
                action.trigger()
            menu.close()
        QtCore.QTimer.singleShot(100,drive)
        self.dock._menu(tree,tree.visualItemRect(item).center())
        return result

    def test_group_menu_parity_and_copy_move_target_all_members(self):
        expanded=self.menu(self.row(self.motors[0]))
        key,_=assembly_ui.group_key(self.row(self.motors[0]))
        assembly_ui.set_group(self.dock,key,True)
        group=self.groups(self.motor)[0]
        condensed=self.menu(group)
        self.assertEqual(condensed,[(name.replace('Condense instances','Expand instances'),enabled,children)
                                   for name,enabled,children in expanded])
        self.assertFalse(self.groups(self.gear))
        with patch.object(self.dock,'copy_rows') as copy:
            self.menu(group,'Copy')
            self.assertEqual([r.path[-1] for r in copy.call_args.args[0]], [panel.identity(o) for o in self.motors])
        with patch.object(self.dock,'move_rows') as move:
            self.menu(group,'Move Components')
            self.assertEqual(len(move.call_args.args[0]),3)
        self.menu(group,'Expand instances');self.assertFalse(self.groups(self.motor))
        self.dock.grab().save(str(self.output/'assembly-controls.png'))

    def test_group_display_is_atomic_and_single_instance_action_is_explicit(self):
        from freecad_plus import display
        self.mode('Condensed');group=self.groups(self.motor)[0].data(0,panel._ROLE)
        before=[display.state(obj) for obj in self.motors]
        assembly_ui.group_display(self.dock,group,shown=False)
        self.assertTrue(all(not display.state(obj)[1] for obj in self.motors))
        self.doc.undo();settle()
        self.assertEqual([display.state(obj) for obj in self.motors],before)
        group=self.groups(self.motor)[0].data(0,panel._ROLE)
        with patch.object(QtWidgets.QInputDialog,'getItem',return_value=(group.children[1].label,True)):
            calls=[];assembly_ui.choose_member(self.dock,group,calls.append)
            self.assertEqual(calls[0].path[-1],panel.identity(self.motors[1]))
        with patch.object(QtWidgets.QInputDialog,'getItem',return_value=('',False)):
            calls=[];assembly_ui.choose_member(self.dock,group,calls.append);self.assertEqual(calls,[])

    def test_condensed_groups_never_disclose_but_real_assemblies_do(self):
        self.mode('Condensed'); before = self.snapshot()
        tree = self.dock.trees[1]; group = self.groups(self.motor)[0]
        self.assertEqual(group.childIndicatorPolicy(), QtWidgets.QTreeWidgetItem.DontShowIndicator)
        root = tree.topLevelItem(0)
        self.assertEqual(root.childIndicatorPolicy(), QtWidgets.QTreeWidgetItem.DontShowIndicatorWhenChildless)
        tree.setCurrentItem(group); tree.setFocus(); tree.scrollToItem(group); settle()
        for key in (QtCore.Qt.Key_Right, QtCore.Qt.Key_Plus, QtCore.Qt.Key_Asterisk):
            QtTest.QTest.keyClick(tree, key); settle()
            self.assertFalse(group.isExpanded())
        QtTest.QTest.mouseDClick(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                                tree.visualItemRect(group).center()); settle()
        self.assertFalse(group.isExpanded())
        tree.expandAll(); settle()
        self.assertTrue(all(not entry.isExpanded() for entries in (self.groups(self.motor), self.groups(self.gear), self.groups(self.bolt)) for entry in entries))
        self.dock.refresh(); self.assertFalse(group.isExpanded())
        self.menu(self.groups(self.gear)[0], 'Expand instances')
        gear = self.row(self.gears[0]); tree.setCurrentItem(gear)
        gear.setExpanded(False); QtTest.QTest.keyClick(tree, QtCore.Qt.Key_Right); settle()
        self.assertTrue(gear.isExpanded())
        self.assertEqual(gear.childIndicatorPolicy(), QtWidgets.QTreeWidgetItem.DontShowIndicatorWhenChildless)
        self.assertEqual(self.snapshot(), before)

    def test_condensed_menu_remains_available_when_editing_one_member(self):
        self.mode('Condensed')
        self.dock.edit_row(self.row(self.motors[0]).data(0,panel._ROLE)); settle()
        group = self.groups(self.motor)[0]
        entries = self.menu(group)
        names = [name for name, enabled, children in entries]
        self.assertIn('Expand instances', names)
        self.assertIn('Copy', names)
        self.assertIn('Remove instance\u2026', names)
        self.assertFalse(group.isExpanded())
        self.menu(group, 'Expand instances')
        self.assertFalse(self.groups(self.motor), self.dock.message.text())

    def row(self, *links):
        key = ('occurrence', tuple(panel.identity(o) for o in (self.top, *links)))
        return self.dock._maps[1][key]

    def groups(self, definition):
        return [item for item in self.dock._maps[1].values()
                if item.data(0, panel._ROLE).kind == 'instance_group'
                and item.data(0, panel._ROLE).ref == panel.identity(definition)]

    def snapshot(self):
        return ([(o.Name, o.ID, o.Label, tuple(x.Name for x in o.OutList),
                  tuple(o.Placement.toMatrix().A) if hasattr(o, 'Placement') else None,
                  o.Visibility) for o in self.doc.Objects], self.doc.UndoCount,
                editing.context_path(self.doc), self.dock._assembly_context(self.dock._binding))

    def select(self, *links):
        row = self.row(*links).data(0, panel._ROLE)
        Gui.Selection.addSelection(*row.selection); settle()

    def test_modes_preserve_model_selection_and_occurrence_items(self):
        before = self.snapshot()
        first, second = self.row(self.motors[0]), self.row(self.motors[1])
        self.assertEqual([self.row(link).text(0) for link in self.motors],
                         ['Motor (1)', 'Motor (2)', 'Motor (3)'])
        self.assertEqual(self.row(self.frame_link).text(0), 'Frame')
        self.select(self.motors[0]); self.select(self.motors[1])
        selected = [(s.ObjectName, tuple(s.SubElementNames)) for s in Gui.Selection.getSelectionEx('', 0)]
        self.dock.grab().save(str(self.output / 'expanded.png'))
        self.mode('Condensed')
        group = self.groups(self.motor)[0]
        self.assertEqual(group.text(0), 'Motor \u00d73')
        self.assertIs(self.row(self.motors[0]), first)
        self.assertIs(self.row(self.motors[1]), second)
        self.assertTrue(first.isSelected() and second.isSelected())
        self.assertFalse(group.isExpanded())
        self.assertEqual([(s.ObjectName, tuple(s.SubElementNames)) for s in Gui.Selection.getSelectionEx('', 0)], selected)
        self.mode('Expanded')
        self.assertFalse(self.groups(self.motor))
        self.assertIs(self.row(self.motors[0]), first)
        self.assertTrue(first.isSelected() and second.isSelected())
        self.assertEqual(self.snapshot(), before)

    def test_nested_groups_collapsed_and_constraint_collectors_first(self):
        constraints.create(self.owner, 'Fixed', [(self.owner.Origin, ['', '']), (self.frame_link, ['', ''])])
        constraints.create(self.gear, 'Fixed', [(self.gear.Origin, ['', '']), (self.bolts[0], ['', ''])])
        self.dock.refresh(); before = self.snapshot()
        self.mode('Condensed')
        self.assertEqual(len(self.groups(self.bolt)), 2)
        self.assertNotEqual(*(group.data(0, panel._ROLE).key for group in self.groups(self.bolt)))
        for definition in (self.motor, self.gear, self.bolt):
            self.assertTrue(all(not group.isExpanded() for group in self.groups(definition)))
        root = self.dock.trees[1].topLevelItem(0)
        self.assertEqual(root.child(0).text(0), 'Assembly constraints')
        self.assertFalse(root.child(0).isExpanded())
        for gear in self.gears:
            self.assertTrue(self.row(gear).isExpanded())
            collector = self.row(gear).child(0)
            self.assertEqual(collector.text(0), 'Assembly constraints')
            self.assertFalse(collector.isExpanded())
        self.dock.grab().save(str(self.output / 'condensed.png'))
        for group in self.groups(self.motor) + self.groups(self.gear): group.setExpanded(True)
        self.assertTrue(all(not group.isExpanded() for group in self.groups(self.motor) + self.groups(self.gear)))
        self.mode('Expanded')
        self.row(self.gears[1]).setExpanded(False)
        self.dock.grab().save(str(self.output / 'individuals.png'))
        self.assertEqual(self.snapshot(), before)

    def test_hidden_selection_preserves_condensed_groups_and_exact_instance(self):
        self.mode('Condensed')
        item = self.row(self.gears[1], self.bolts[1])
        self.select(self.gears[1], self.bolts[1])
        self.assertTrue(item.isSelected())
        parent = item.parent()
        while parent:
            self.assertEqual(parent.isExpanded(), parent.data(0, panel._ROLE).kind != 'instance_group')
            parent = parent.parent()
        self.assertFalse(self.row(self.gears[0], self.bolts[1]).isSelected())
        group = self.groups(self.gear)[0]; group.setExpanded(False)
        self.dock.refresh()
        self.assertFalse(group.isExpanded())  # Refresh respects a manual fold.
        self.assertIs(self.row(self.gears[1], self.bolts[1]), item)
        Gui.Selection.clearSelection(); self.select(self.gears[1], self.bolts[1])
        self.assertFalse(group.isExpanded())
        self.mode('Expanded')
        self.assertIs(self.row(self.gears[1], self.bolts[1]), item)
        self.assertTrue(item.isSelected())
        self.assertFalse(self.dock.trees[1].visualItemRect(item).isEmpty())

    def test_group_has_no_component_action_or_native_selection(self):
        self.mode('Condensed'); group = self.groups(self.motor)[0]
        before = self.snapshot(); group.setSelected(True); settle()
        self.assertFalse(Gui.Selection.getSelectionEx('', 0))
        row = group.data(0, panel._ROLE)
        self.assertFalse(row.path or row.selection)
        self.assertFalse(group.flags() & QtCore.Qt.ItemIsUserCheckable)
        for action in (self.dock.edit_row, self.dock.rename_row, self.dock.open_row, self.dock.paste_row):
            with self.assertRaises(ValueError): action(row)
        with patch.object(self.dock, 'edit_row') as edit:
            self.dock._edit_clicked(group)
            edit.assert_called_once_with(row.children[0])
        # Menu dispatch now offers component actions; the presentation row itself
        # still cannot masquerade as one individual occurrence in backend calls.
        self.assertEqual(self.snapshot(), before)

    def test_individual_edit_copy_and_move_keep_exact_route(self):
        self.mode('Condensed')
        item = self.row(self.motors[1]); group = item.parent()
        self.menu(group, 'Expand instances')
        tree = self.dock.trees[1]; tree.scrollToItem(item); settle()
        QtTest.QTest.mouseClick(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, tree.visualItemRect(item).center())
        settle()
        self.assertTrue(item.isSelected())
        self.dock.copy_rows((item.data(0, panel._ROLE),))
        self.assertEqual(self.dock._clipboard[0][0], panel.identity(self.motor))
        with patch.object(movement, 'open_task') as start:
            self.dock.move_selected()
            self.assertEqual(start.call_args.args[1][0].path,
                             (panel.identity(self.top), panel.identity(self.motors[1])))
        pasted = self.dock.paste_row(tree.topLevelItem(0).data(0, panel._ROLE))
        settle()
        self.assertEqual(len(pasted), 1)
        self.assertEqual(pasted[0].LinkedObject, self.motor)
        self.assertFalse(self.groups(self.motor))
        self.assertTrue(all(self.row(link).parent() == tree.topLevelItem(0) for link in (*self.motors, pasted[0])))
        self.assertTrue(self.row(pasted[0]).isSelected())
        QtTest.QTest.mouseClick(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, tree.visualItemRect(item).center())
        QtTest.QTest.mouseDClick(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, tree.visualItemRect(item).center())
        settle()
        self.assertEqual(editing.context_path(self.doc), (self.motor, (self.top, self.motors[1])))
        self.assertEqual(self.dock._assembly_context(self.dock._binding)[0], self.owner)

    def test_counts_rename_singleton_transition_and_undo(self):
        self.mode('Condensed')
        item = self.row(self.motors[0]); key = self.groups(self.motor)[0].data(0, panel._ROLE).key
        hierarchy.rename_definition(self.motor, 'Motor renamed'); settle()
        self.assertEqual(self.groups(self.motor)[0].text(0), 'Motor renamed \u00d73')
        self.assertEqual(self.groups(self.motor)[0].data(0, panel._ROLE).key, key)
        with document.transaction(self.doc, 'Remove fixture occurrences'):
            for link in self.motors[1:]: self.doc.removeObject(link.Name)
        settle(); self.dock.refresh()
        self.assertFalse(self.groups(self.motor))
        self.assertIs(self.row(self.motors[0]), item)
        self.assertEqual(item.text(0), 'Motor renamed')
        self.doc.undo(); settle()
        self.assertEqual(self.groups(self.motor)[0].childCount(), 3)
        self.assertIs(self.row(self.motors[0]), item)

    def test_grouping_identity_never_merges_equal_labels_or_different_parents(self):
        # Imported name conflicts are now rejected before loading; the presentation
        # layer still must never use a label as identity.
        rows = tuple(panel.Row(('occurrence', i), 'occurrence', 'Same label', ref, (i,))
                     for i, ref in enumerate((('fileA', 'part'), ('fileB', 'part'), ('fileA', 'part'))))
        shown = panel.instance_rows(rows, True, ('parent', 1))
        self.assertEqual([r.kind for r in shown], ['instance_group', 'occurrence'])
        self.assertEqual([r.key for r in shown[0].children], [rows[0].key, rows[2].key])
        self.assertNotEqual(shown[0].key, panel.instance_rows(rows, True, ('parent', 2))[0].key)

    def test_external_qualification_preference_and_save_reopen(self):
        source = document.new_document('Library')
        part = document.validate(source).Definitions[0]; part.Label = 'Imported motor'
        document.save_document(source, self.output / 'Library.cadprt')
        document.save_document(self.doc, self.output / 'Machine.cadprt')
        external.import_file(self.doc, source)
        imported = [hierarchy.add_instance(self.owner, part) for _ in range(2)]
        App.setActiveDocument(self.doc.Name); self.mode('Condensed'); self.dock.refresh()
        label = self.groups(part)[0].text(0)
        self.assertIn('Library', label); self.assertTrue(label.endswith('\u00d72'))
        self.assertTrue(self.prefs.GetBool('CondensedInstances', False))
        document.save_document(self.doc)
        info = dict(host=self.doc.FileName, owner=self.owner.Name, top=self.top.Name,
                    uid=str(self.doc.Uid), ids={o.Name: o.ID for o in self.doc.Objects},
                    selected=[self.top.Name, imported[1].Name])
        (self.output / 'reopen.json').write_text(json.dumps(info))
        other = panel.ComponentPanel(Gui.getMainWindow())
        try:
            other.refresh()
            self.assertTrue(assembly_ui.state(other)[None])
        finally: other.dispose(); other.deleteLater()
