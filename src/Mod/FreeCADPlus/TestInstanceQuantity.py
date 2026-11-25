# SPDX-License-Identifier: LGPL-2.1-or-later
import json, os, unittest
from pathlib import Path
from unittest.mock import patch
import FreeCAD as App, FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets, QtTest
from freecad_plus import document, hierarchy, editing, panel, constraints, movement, part_transfer_ops
from freecad_plus import instance_patterns as patterns, instance_task, component_add


def config(mode='Linear', count=3, **values):
    result = dict(mode=mode, count=count, position=[1, 2, 3], direction=[1, 0, 0], spacing=10,
                  columns=3, rows=2, row_direction=[0, 1, 0], row_spacing=20,
                  radius=25, angle=0, angular_spacing=60, full=True, rotate=False)
    result.update(values); return result


class TestInstanceQuantity(unittest.TestCase):
    def setUp(self):
        self.before = set(App.listDocuments())
        self.out = Path(os.environ['PLUS_TEST_DIR']) / self._testMethodName; self.out.mkdir(exist_ok=True)
        Gui.Selection.clearSelection()
        self.doc = document.new_document('Quantity')
        self.root = document.validate(self.doc); self.owner = self.root.Definitions[0]; self.owner.Label = 'Machine'
        self.part = hierarchy.create_definition(self.doc, 'Bolt')
        with document.transaction(self.doc, 'Geometry'): self.shape = self.part.newObject('Part::Box', 'Solid')
        self.top = self.root.Group[0]; editing.edit((self.top,))
        self.dock = panel.show_panel(); QtTest.QTest.qWait(100); self.dock.activate_assembly(self.owner, (self.top,))
        self.dock.tabs.setCurrentIndex(1)

    def tearDown(self):
        if instance_task._active: instance_task._active.reject()
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments()) - self.before: App.closeDocument(name)
        QtTest.QTest.qWait(100)

    def snapshot(self):
        return ([(o.Name, o.ID, tuple(x.Name for x in o.OutList),
                  tuple(o.Placement.toMatrix().A) if hasattr(o, 'Placement') else None) for o in self.doc.Objects],
                self.doc.UndoCount, editing.context_path(self.doc), self.dock._assembly_context(self.dock._binding))

    def test_quantity_and_new_component_are_atomic_shared_and_independent(self):
        before = self.snapshot(); undo = self.doc.UndoCount
        links, feature = patterns.create(self.owner, [self.part], config('Quantity', 4))
        self.assertIsNone(feature); self.assertEqual(len(links), 4)
        self.assertTrue(all(link.LinkedObject == self.part for link in links))
        self.assertEqual(self.doc.UndoCount, undo + 1); movement.movable(links[0], self.owner)
        self.doc.undo(); self.assertEqual(self.snapshot()[0], before[0])
        self.doc.redo(); document.validate(self.doc)
        definitions = len(self.root.Definitions); undo = self.doc.UndoCount
        links, _ = patterns.create(self.owner, [], config('Quantity', 5), label='New pin')
        self.assertEqual(len(self.root.Definitions), definitions + 1)
        self.assertEqual(len({link.LinkedObject for link in links}), 1)
        self.assertEqual(self.doc.UndoCount, undo + 1)

    def test_linear_grid_circular_math_and_invalid_inputs(self):
        self.assertTrue(patterns.placements(config(reverse=True))[2].Base.isEqual(App.Vector(-19, 2, 3), 1e-8))
        grid = patterns.placements(config('Grid'))
        self.assertEqual(len(grid), 6); self.assertTrue(grid[-1].Base.isEqual(App.Vector(21, 22, 3), 1e-8))
        circle = patterns.placements(config('Circular', 4, direction=[0, 0, 1], position=[0, 0, 0], rotate=True))
        self.assertTrue(circle[1].Base.isEqual(App.Vector(0, 25, 0), 1e-8))
        self.assertTrue(circle[1].Rotation.multVec(App.Vector(1, 0, 0)).isEqual(App.Vector(0, 1, 0), 1e-8))
        self.assertFalse(circle[0].Base.isEqual(circle[-1].Base, 1e-8))
        for bad in (config(count=0), config(direction=[0, 0, 0]), config(spacing=float('nan')),
                    config('Grid', row_direction=[1, 0, 0]), config('Grid', columns=1000, rows=1000),
                    config('Circular', radius=0), config('Circular', 4, full=False, angular_spacing=120)):
            with self.assertRaises((ValueError, OverflowError)): patterns.placements(bad)

    def test_older_schema_upgrades_only_for_pattern_and_undo_restores_it(self):
        with document.transaction(self.doc, 'Older schema fixture'): self.root.PlusSchema = 6
        document.validate(self.doc)
        patterns.create(self.owner, [self.part], config('Quantity', 2))
        self.assertEqual(self.root.PlusSchema, 6)
        links, feature = patterns.create(self.owner, [self.part], config())
        self.assertEqual(self.root.PlusSchema, 7); document.validate(self.doc)
        self.doc.undo(); self.assertEqual(self.root.PlusSchema, 6); document.validate(self.doc)
        self.doc.redo(); self.assertEqual(self.root.PlusSchema, 7); document.validate(self.doc)

    def test_pattern_edit_preserves_ids_undo_and_movement_constraint_guards(self):
        links, feature = patterns.create(self.owner, [self.part], config())
        identities = [(o.Name, o.ID) for o in links]; undo = self.doc.UndoCount
        changed = patterns.update(feature, config(count=5, spacing=7))
        self.assertEqual([(o.Name, o.ID) for o in changed[:3]], identities)
        self.assertEqual(self.doc.UndoCount, undo + 1)
        with self.assertRaisesRegex(ValueError, 'pattern'): movement.movable(changed[0], self.owner)
        with self.assertRaisesRegex(ValueError, 'pattern'): hierarchy.move_instance(changed[0], App.Placement())
        with self.assertRaisesRegex(ValueError, 'pattern'):
            constraints.create(self.owner, 'Fixed', [(self.owner.Origin, ['', '']), (changed[0], ['', ''])])
        self.doc.undo(); self.doc.recompute(); self.assertEqual(len(feature.Members), 3)
        self.doc.redo(); self.doc.recompute(); self.assertEqual(len(feature.Members), 5)
        self.assertEqual([(o.Name, o.ID) for o in feature.Members[:3]], identities)

    def test_reference_updates_and_dependency_reduction_block(self):
        with document.transaction(self.doc, 'Reference line'):
            line = self.owner.newObject('Part::Feature', 'Direction')
            import Part
            line.Shape = Part.makeLine(App.Vector(), App.Vector(0, 10, 0))
        cfg = config(reference_keys=['direction'])
        links, feature = patterns.create(self.owner, [self.part], cfg, refs=[(line, ['Edge1'])])
        self.assertTrue(links[2].LinkPlacement.Base.isEqual(App.Vector(1, 22, 3), 1e-8))
        with document.transaction(self.doc, 'Rotate reference'):
            line.Placement.Rotation = App.Rotation(App.Vector(0, 0, 1), -90)
        self.assertTrue(links[2].LinkPlacement.Base.isEqual(App.Vector(21, 2, 3), 1e-8))
        document.save_document(self.doc, self.out / 'Referenced.cadprt')
        (self.out / 'reopen.json').write_text(json.dumps(dict(host=self.doc.FileName,
            pattern=feature.Name, line=line.Name)))
        with document.transaction(self.doc, 'Dependent fixture'):
            dependent = self.owner.newObject('Part::Feature', 'Consumer')
            dependent.addProperty('App::PropertyLink', 'Source'); dependent.Source = links[-1]
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'used by'): patterns.update(feature, config(count=2))
        self.assertEqual(self.snapshot(), before)
        with self.assertRaisesRegex(ValueError, 'own members'):
            patterns.update(feature, cfg, [(links[0], [self.shape.Name + '.Edge1'])])

    def test_cycles_invalid_batches_and_rollback_leave_no_definition_or_import(self):
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'cycle'): patterns.create(self.owner, [self.owner], config())
        with patch.object(hierarchy, '_place_instance', side_effect=RuntimeError('Injected')):
            with self.assertRaisesRegex(RuntimeError, 'Injected'):
                patterns.create(self.owner, [], config(), label='Rolled back')
        self.assertEqual(self.snapshot(), before)

    def test_task_create_preview_cancel_edit_and_stale_context(self):
        before = self.snapshot(); task = instance_task.open_task([self.part])
        task.form.mode.setCurrentText('Grid'); task.form.rows.setValue(3); task.refresh()
        self.assertFalse(task.form.status.error, task.form.status.text()); self.assertIsNotNone(task.overlay)
        self.assertEqual(self.snapshot(), before); task.form.grab().save(str(self.out / 'grid.png'))
        task.reject(); self.assertEqual(self.snapshot(), before)
        task = instance_task.open_task([self.part]); task.form.mode.setCurrentText('Linear'); task.form.count.setValue(4)
        accepted = task.accept(); self.assertTrue(accepted, task.form.status.text() if not accepted else '')
        feature = task.created_pattern; identities = [o.ID for o in feature.Members]
        task = instance_task.open_task(pattern=feature)
        self.assertEqual(task.form.mode.currentText(), 'Linear'); self.assertEqual(task.form.count.value(), 4)
        task.form.count.setValue(5); accepted = task.accept()
        self.assertTrue(accepted, task.form.status.text() if not accepted else '')
        self.assertEqual([o.ID for o in feature.Members[:4]], identities)
        task = instance_task.open_task([self.part]); editing.edit((self.top, feature.Members[0]))
        count = len(self.doc.Objects); self.assertFalse(task.accept()); self.assertEqual(len(self.doc.Objects), count)
        task.reject()

    def test_navigator_next_and_new_component_cancel_never_mutate(self):
        dialog = component_add.Picker(None, True); dialog.name.setText('New component')
        before = self.snapshot(); self.assertEqual(dialog.submit.text(), 'Next'); dialog.accept()
        self.assertEqual(dialog.result(), QtWidgets.QDialog.Accepted); self.assertEqual(self.snapshot(), before)
        task = instance_task.open_task(dialog.selected_definitions, dialog.new_label, dialog.opened)
        task.form.count.setValue(6); task.reject(); dialog.deleteLater(); self.assertEqual(self.snapshot(), before)

    def test_external_patterns_export_and_saved_fixtures(self):
        source = document.new_document('Library'); part = document.validate(source).Definitions[0]; part.Label = 'External pin'
        document.save_document(source, self.out / 'Library.cadprt')
        document.save_document(self.doc, self.out / 'Machine.cadprt'); App.setActiveDocument(self.doc.Name)
        links, feature = patterns.create(self.owner, [self.part, part], config('Circular', 4, direction=[0, 0, 1]))
        self.assertEqual(len(links), 8); self.assertEqual(len(feature.Seeds), 2); document.save_document(self.doc)
        exported = self.out / 'Export.cadprt'; part_transfer_ops.export_parts([self.owner], exported)
        copied = document.open_document(exported); new_pattern = next(o for o in copied.Objects if patterns.is_pattern(o))
        self.assertEqual(len(new_pattern.Members), 8); self.assertTrue(all(o.Document == copied for o in new_pattern.Members))
        patterns.update(new_pattern, config('Grid', columns=2, rows=2)); document.save_document(copied)
        (self.out / 'reopen.json').write_text(json.dumps(dict(host=self.doc.FileName, export=str(exported),
            pattern=feature.Name, members={o.Name:o.ID for o in feature.Members})))

    def test_real_navigator_next_change_parts_and_quantity_commit(self):
        errors = []
        def next_step():
            dialog = QtWidgets.QApplication.activeModalWidget()
            try:
                it = QtWidgets.QTreeWidgetItemIterator(dialog.choices)
                while it.value():
                    if it.value().data(0, QtCore.Qt.UserRole) == panel.identity(self.part):
                        it.value().setCheckState(0, QtCore.Qt.Checked)
                    it += 1
                dialog.submit.click()
            except BaseException as error: errors.append(error); dialog.reject()
        before = self.snapshot(); QtCore.QTimer.singleShot(100, next_step)
        task = component_add.open_picker(self.dock)
        self.assertFalse(errors); self.assertIsNotNone(task); self.assertEqual(self.snapshot(), before)
        task.form.count.setValue(6)
        with patch.object(component_add, 'open_picker') as chooser:
            task.change_parts(); QtTest.QTest.qWait(100)
            self.assertEqual(chooser.call_args.kwargs['initial'][0]['count'], 6)
        QtCore.QTimer.singleShot(100, next_step)
        task = component_add.open_picker(self.dock, initial=(config('Quantity', 6), []))
        self.assertTrue(task.accept()); self.assertEqual(len(task.created), 6)
        self.assertEqual(self.doc.UndoCount, before[1] + 1)

    def test_ui_reference_pick_and_context_menu_edit(self):
        import Part
        with document.transaction(self.doc, 'Reference line'):
            line = self.owner.newObject('Part::Feature', 'Direction')
            line.Shape = Part.makeLine(App.Vector(), App.Vector(0, 8, 0))
        task = instance_task.open_task([self.part]); task.form.mode.setCurrentText('Linear')
        task.form.count.setValue(3); task.form.directions['linear'].setCurrentText('Pick edge / axis')
        task.collect('linear'); Gui.Selection.addSelection(line.Document.Name, line.Name, 'Edge1')
        QtTest.QTest.qWait(100); self.assertIn('linear', task.refs, task.form.status.text())
        self.assertTrue(task.accept()); feature = task.created_pattern
        self.dock.refresh(); row = next(item for item in self.dock._maps[1].values()
            if item.data(0, panel._ROLE).kind == 'occurrence' and item.data(0, panel._ROLE).path[-1] == panel.identity(feature.Members[1]))
        self.dock.tabs.setCurrentIndex(1); tree = self.dock.trees[1]; tree.scrollToItem(row)
        seen = []
        def choose():
            menu = QtWidgets.QApplication.activePopupWidget()
            try:
                action = next(a for a in menu.actions() if a.text() == 'Edit instance pattern')
                seen.append(True); action.trigger(); menu.close()
            except BaseException as error: seen.append(error); menu.close()
        QtCore.QTimer.singleShot(100, choose)
        self.dock._menu(tree, tree.visualItemRect(row).center())
        self.assertEqual(seen, [True]); edit = instance_task._active; self.assertIsNotNone(edit)
        self.assertEqual(edit.form.directions['linear'].currentText(), 'Pick edge / axis')
        before = self.snapshot(); edit.form.count.setValue(2); edit.reject(); self.assertEqual(self.snapshot(), before)

    def test_ui_all_arrangements_previews_and_errors_preserve_model(self):
        task = instance_task.open_task([self.part]); before = self.snapshot()
        for mode in ('Quantity', 'Linear', 'Grid', 'Circular'):
            task.form.mode.setCurrentText(mode); task.form.count.setValue(6); task.refresh()
            QtTest.QTest.qWait(100)
            self.assertFalse(task.form.status.error, task.form.status.text())
            task.form.grab().save(str(self.out / (mode.lower() + '.png')))
            self.assertEqual(self.snapshot(), before)
        self.assertEqual(task.form.units['angular_spacing'].property('rawValue'), 60)
        task.form.full.setChecked(False); task.form.units['angular_spacing'].setProperty('rawValue', 80)
        task.refresh(); self.assertTrue(task.form.status.error)
        self.assertFalse(task.accept()); self.assertEqual(self.snapshot(), before); task.reject()

    def test_indirect_member_reference_blocks_reduction(self):
        links, feature = patterns.create(self.owner, [self.part], config())
        consumer_part = hierarchy.create_definition(self.doc, 'Consumer part')
        with document.transaction(self.doc, 'Indirect reference'):
            consumer = consumer_part.newObject('Part::Feature', 'Consumer')
            consumer.addProperty('App::PropertyLinkSub', 'Source')
            consumer.Source = (self.owner, links[-1].Name + '.' + self.shape.Name + '.Face1')
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'used by'): patterns.update(feature, config(count=2))
        self.assertEqual(self.snapshot(), before)

    def test_reduction_preserves_edited_occurrence(self):
        links, feature = patterns.create(self.owner, [self.part], config())
        editing.edit((self.top, links[-1])); self.dock.refresh(); before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'being edited'): patterns.update(feature, config(count=2))
        self.assertEqual(self.snapshot(), before)

    def test_external_parent_pattern_shared_across_occurrences(self):
        source = document.new_document('Subsystem')
        owner = document.validate(source).Definitions[0]; owner.Label = 'External subsystem'
        child = hierarchy.create_definition(source, 'External fastener')
        document.save_document(source, self.out / 'Subsystem.cadprt')
        document.save_document(self.doc, self.out / 'Host.cadprt')
        App.setActiveDocument(self.doc.Name); QtTest.QTest.qWait(100)
        instances, _ = patterns.create(self.owner, [owner], config('Quantity', 2))
        editing.edit((self.top, instances[0])); self.dock.refresh()
        before = self.snapshot(); undo = source.UndoCount
        task = instance_task.open_task([child]); task.form.mode.setCurrentText('Grid')
        task.form.columns.setValue(3); task.form.rows.setValue(2)
        accepted = task.accept(); self.assertTrue(accepted, task.form.status.text() if not accepted else '')
        feature = task.created_pattern
        self.assertEqual(feature.Document, source); self.assertEqual(patterns.owner_of(feature), owner)
        self.assertEqual(len(feature.Members), 6); self.assertEqual(source.UndoCount, undo + 1)
        after = self.snapshot()
        self.assertEqual(after[0], before[0]); self.assertEqual(after[2:], before[2:])
        # Native linked-document recompute contributes one corresponding host Undo entry.
        self.assertEqual(after[1], before[1] + 1)
        self.assertEqual(instances[0].LinkedObject, instances[1].LinkedObject)
        self.assertTrue(all(member in instances[1].LinkedObject.Group for member in feature.Members))
        document.save_document(source); document.save_document(self.doc)
