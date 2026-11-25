# SPDX-License-Identifier: LGPL-2.1-or-later
"""Batch insertion, self-contained editable export, rollback and native dialogs."""
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import (document, hierarchy, external, editing, constraints, panel,
                         component_add, part_transfer, part_transfer_ops, document_import)


class TestPartTransfer(unittest.TestCase):
    def setUp(self):
        self.before = set(App.listDocuments())
        self.out = Path(os.environ['PLUS_TEST_DIR']) / self._testMethodName
        self.out.mkdir(exist_ok=True)
        self.doc = document.new_document('Machine')
        self.root = document.validate(self.doc)
        self.owner = self.root.Definitions[0]; self.owner.Label = 'Machine'
        self.drive = hierarchy.create_definition(self.doc, 'Drive unit')
        self.plate = hierarchy.create_definition(self.doc, 'Mounting plate')
        self.cover = hierarchy.create_definition(self.doc, 'Cover')
        self.link = hierarchy.add_instance(self.owner, self.drive)
        self.nested = hierarchy.add_instance(self.drive, self.plate)
        hierarchy.add_instance(self.owner, self.cover)
        with document.transaction(self.doc, 'Geometry'):
            self.box = self.plate.newObject('Part::Box', 'Box')
            self.box.Length = 2; self.box.Width = 3; self.box.Height = 4
        editing.edit((self.root.Group[0], self.link))
        self.dock = panel.show_panel(); self.dock.refresh(); self.dock.activate_assembly(self.owner)
        self.dock.tabs.setCurrentIndex(0)
        QtTest.QTest.qWait(80)

    def tearDown(self):
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)
        QtTest.QTest.qWait(80)

    def state(self, doc=None):
        doc = doc or self.doc
        return (doc.UndoCount, {o.Name: (o.ID, tuple((x.Document.Name, x.Name) for x in o.OutList),
                str(o.Placement) if hasattr(o, 'Placement') else '', o.Visibility) for o in doc.Objects})

    def library(self, close=False):
        document.save_document(self.doc, self.out/'Machine.cadprt')
        source = document.new_document('Hardware')
        first = document.validate(source).Definitions[0]; first.Label = 'Bracket'
        second = hierarchy.create_definition(source, 'Locator')
        document.save_document(source, self.out/'Hardware.cadprt')
        if close: App.closeDocument(source.Name)
        App.setActiveDocument(self.doc.Name); QtTest.QTest.qWait(80); self.dock.refresh()
        return (self.out/'Hardware.cadprt') if close else (source, first, second)

    def row(self, picker, part):
        it = QtWidgets.QTreeWidgetItemIterator(picker.choices)
        while it.value():
            if it.value().data(0, QtCore.Qt.UserRole) == panel.identity(part): return it.value()
            it += 1
        self.fail('Missing part row')

    def test_batch_one_undo_preserves_source_and_context(self):
        source, a, b = self.library(); before = self.state(); src = self.state(source)
        context = editing.context_path(self.doc)
        links = component_add.add_many(component_add.target()[1], [a, self.cover, b])
        self.assertEqual([x.LinkedObject for x in links], [a, self.cover, b])
        self.assertTrue(all(x in self.drive.Group for x in links))
        self.assertEqual(self.root.Imports, [document.validate(source)])
        self.assertEqual(self.doc.UndoCount, before[0] + 1)
        self.assertEqual(self.state(source), src); self.assertEqual(editing.context_path(self.doc), context)
        names = [x.Name for x in links]
        self.doc.undo(); self.assertEqual(self.state(), before)
        self.doc.redo(); document.validate(self.doc)
        self.assertEqual([self.doc.getObject(n).LinkedObject for n in names], [a, self.cover, b])
        document.save_document(self.doc)

    def test_batch_cycle_and_file_cycle_leave_no_partial_changes(self):
        source, a, b = self.library(); before = self.state()
        with self.assertRaisesRegex(ValueError, 'Circular'):
            hierarchy.add_children(self.drive, [a, self.owner])
        self.assertEqual(self.state(), before)
        external.import_file(self.doc, source)
        src = self.state(source)
        with self.assertRaisesRegex(ValueError, 'Circular file'):
            hierarchy.add_children(a, [b, self.cover])
        self.assertEqual(self.state(source), src)

    def test_batch_creation_failure_rolls_back_catalog_and_all_links(self):
        source, a, b = self.library(); before = self.state()
        original = hierarchy._place_instance
        def fail(owner, part, *args):
            if part == b: raise RuntimeError('Injected placement failure')
            return original(owner, part, *args)
        with patch.object(hierarchy, '_place_instance', side_effect=fail):
            with self.assertRaisesRegex(RuntimeError, 'Injected'):
                hierarchy.add_children(self.drive, [a, b])
        self.assertEqual(self.state(), before)

    def test_picker_open_cancel_closes_only_new_files(self):
        filename = self.library(close=True); before = self.state(); opened = set(App.listDocuments())
        dialog = component_add.Picker(self.dock)
        try:
            with patch.object(QtWidgets.QFileDialog, 'getOpenFileName', return_value=(str(filename), '')):
                dialog.open_source()
            self.assertFalse(dialog.status.isVisible())
            self.assertGreater(len(App.listDocuments()), len(opened))
            self.assertEqual(self.state(), before)
            dialog.reject()
            self.assertEqual(set(App.listDocuments()), opened)
            self.assertEqual(self.state(), before)
        finally: dialog.deleteLater()

    def test_picker_open_and_batch_accept_real_native_widgets(self):
        filename = self.library(close=True); dialog = component_add.Picker(self.dock)
        try:
            dialog.show(); QtTest.QTest.qWait(80)
            with patch.object(QtWidgets.QFileDialog, 'getOpenFileName', return_value=(str(filename), '')):
                dialog.open_source()
            source = next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName) == filename)
            a, b = document.validate(source).Definitions
            group = self.row(dialog, a).parent()
            self.assertFalse(group.isExpanded())
            group.setCheckState(0, QtCore.Qt.Checked); group.setExpanded(True)
            self.assertEqual(len(dialog.checked_parts()), 2)
            QtTest.QTest.qWait(80)  # Let native button-box sizing settle before capture.
            dialog.grab().save(str(self.out/'add-existing.png'))
            dialog.submit.click()
            self.assertEqual(dialog.result(), QtWidgets.QDialog.Accepted)
            self.assertTrue(all(any(x.TypeId == 'App::Link' and x.LinkedObject == p for x in self.drive.Group) for p in (a, b)))
            self.assertIn(source.Name, App.listDocuments())
        finally: dialog.deleteLater()

    def test_picker_stale_context_and_self_ancestor_are_blocked(self):
        dialog = component_add.Picker(self.dock)
        try:
            self.assertFalse(self.row(dialog, self.owner).flags() & QtCore.Qt.ItemIsEnabled)
            self.assertFalse(self.row(dialog, self.drive).flags() & QtCore.Qt.ItemIsEnabled)
            self.row(dialog, self.cover).setCheckState(0, QtCore.Qt.Checked)
            editing.edit((self.root.Group[0], self.link, self.nested))
            before = self.state(); dialog.accept()
            self.assertNotEqual(dialog.result(), QtWidgets.QDialog.Accepted)
            self.assertEqual(self.state(), before)
        finally: dialog.reject(); dialog.deleteLater()

    def test_native_file_import_is_catalog_only(self):
        filename = self.library(close=True); links = tuple(self.drive.Group)
        # Gui::Application::importFrom wraps module.insert in a lazy command.
        self.doc.openTransaction('Import')
        try:
            imported = document_import.insert(str(filename), self.doc.Name)
        finally:
            self.doc.commitTransaction()
        self.assertIn(imported, self.root.Imports)
        self.assertEqual(tuple(self.drive.Group), links)
        self.doc.undo(); self.assertEqual(self.root.Imports, [])

    def export(self, parts=None, name='Selected parts.cadprt'):
        return part_transfer_ops.export_parts(parts or [self.drive, self.cover], self.out/name)

    def test_export_shared_child_once_and_editable_geometry(self):
        hierarchy.add_instance(self.cover, self.plate)
        context = editing.context_path(self.doc); before = self.state(); docs = set(App.listDocuments())
        path = self.export()
        self.assertEqual(set(App.listDocuments()), docs); self.assertEqual(App.ActiveDocument, self.doc)
        self.assertEqual(editing.context_path(self.doc), context); self.assertEqual(self.state(), before)
        copied = document.open_document(path, hidden=True); root = document.validate(copied)
        self.assertEqual(len(root.Definitions), 3); self.assertEqual(len(root.Group), 2); self.assertEqual(root.Imports, [])
        drive, plate, cover = root.Definitions
        self.assertEqual(next(o for o in drive.Group if o.TypeId == 'App::Link').LinkedObject, plate)
        self.assertEqual(next(o for o in cover.Group if o.TypeId == 'App::Link').LinkedObject, plate)
        box = next(o for o in plate.Group if o.TypeId == 'Part::Box')
        self.assertAlmostEqual(box.Shape.Volume, 24)
        box.Length = 7; copied.recompute(); self.assertAlmostEqual(box.Shape.Volume, 84)
        self.assertEqual(self.box.Length.Value, 2); self.assertEqual(self.state(), before)

    def test_export_nested_constraints_save_reopen_and_solve(self):
        refs = lambda a, b: [(a, ['', '']), (b, ['', ''])]
        constraints.create(self.owner, 'Fixed', refs(self.owner.Origin, self.link))
        constraints.create(self.drive, 'Fixed', refs(self.drive.Origin, self.nested))
        before = self.state(); path = self.export([self.owner])
        self.assertEqual(self.state(), before)
        copied = document.open_document(path, hidden=True); root = document.validate(copied)
        self.assertEqual(len(root.Definitions), 4)
        owners = [p for p in root.Definitions if constraints.joints(p)]
        self.assertEqual(len(owners), 2)
        for owner in owners:
            solver = constraints.solver_for(owner)
            self.assertEqual(solver.PlusAssemblyOwner, owner)
            self.assertEqual(solver.solve(), 0)
            for joint in constraints.joints(owner):
                self.assertEqual(joint.Reference1[0], owner.Origin)
                self.assertEqual(joint.Reference2[0].Document, copied)
        self.assertTrue(all(x.Document == copied for o in copied.Objects for x in o.OutList))
        (self.out/'expected.json').write_text(json.dumps({'file': str(path), 'ids': {o.Name:o.ID for o in copied.Objects},
            'uid':str(copied.Uid), 'collectors':len(owners)}))

    def test_export_external_children_domesticates_and_deduplicates_labels(self):
        source, a, b = self.library()
        a.Label = 'Cover'; b.Label = 'Mounting plate'
        hierarchy.add_children(self.drive, [a, b]); before = self.state(source)
        path = self.export([self.drive, self.cover])
        self.assertEqual(self.state(source), before)
        copied = document.open_document(path, hidden=True); root = document.validate(copied)
        self.assertEqual(len(root.Definitions), 5)
        self.assertEqual(len({p.Label for p in root.Definitions}), 5)
        self.assertEqual(root.Imports, [])
        self.assertTrue(all(o.LinkedObject.Document == copied for o in copied.Objects if o.TypeId == 'App::Link'))

    def test_export_duplicate_roots_and_selected_descendant(self):
        path = self.export([self.drive, self.plate, self.drive])
        copied = document.open_document(path, hidden=True); root = document.validate(copied)
        self.assertEqual(len(root.Definitions), 2); self.assertEqual(len(root.Group), 2)

    def test_export_native_sketch_pad_history_expression_and_display(self):
        import Sketcher
        from freecad_plus import display
        sketch = editing.new_sketch(self.doc)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2), False)
        sketch.addConstraint(Sketcher.Constraint('Radius', 0, 2))
        sketch.renameConstraint(0, 'Radius')
        self.doc.recompute()
        pad = editing.pad(self.doc, sketch, 4)
        pad.setExpression('Length', sketch.Name + '.Constraints.Radius * 2')
        self.doc.recompute()
        display.set_state(self.drive, self.nested, part_type='Reference', shown=False)
        source_volume = pad.Shape.Volume; before = self.state()
        path = self.export([self.drive])
        self.assertEqual(self.state(), before)
        copied = document.open_document(path, hidden=True); root = document.validate(copied)
        drive = root.Definitions[0]
        history = document.history(copied, drive)
        copy_sketch = next(o for o in history if o.TypeId == 'Sketcher::SketchObject')
        copy_pad = next(o for o in history if o.TypeId == 'PartDesign::Pad')
        self.assertEqual(copy_pad.Profile[0], copy_sketch)
        self.assertTrue(copy_pad.ExpressionEngine)
        self.assertAlmostEqual(copy_pad.Shape.Volume, source_volume)
        link = next(o for o in drive.Group if o.TypeId == 'App::Link')
        self.assertEqual(display.state(link), ('Reference', False))
        copy_sketch.setDatum(0, App.Units.Quantity('3 mm')); copied.recompute()
        self.assertEqual(copy_pad.Length.Value, 6)
        self.assertEqual(pad.Length.Value, 4)

    def test_open_invalid_file_keeps_existing_selection_and_documents(self):
        document.save_document(self.doc, self.out/'Machine.cadprt')
        dialog = component_add.Picker(self.dock)
        try:
            self.row(dialog, self.cover).setCheckState(0, QtCore.Qt.Checked)
            before = self.state(); docs = set(App.listDocuments())
            bad = self.out/'Bad.cadprt'; bad.write_bytes(b'not a native archive')
            with patch.object(QtWidgets.QFileDialog, 'getOpenFileName', return_value=(str(bad), '')):
                dialog.open_source()
            self.assertTrue(dialog.status.error)
            self.assertIn('Cannot open component file', dialog.status.text())
            self.assertEqual(dialog.checked_parts(), [panel.identity(self.cover)])
            self.assertEqual(self.state(), before); self.assertEqual(set(App.listDocuments()), docs)
        finally: dialog.reject(); dialog.deleteLater()

    def test_parts_context_menu_exports_multiple_selected_parts(self):
        tree = self.dock.trees[0]; tree.clearSelection(); rows = []
        for i in range(tree.topLevelItemCount()):
            row = tree.topLevelItem(i)
            if row.text(0) in ('Drive unit', 'Cover'):
                row.setSelected(True); rows.append(row)
        self.assertEqual(len(rows), 2)
        path = self.out/'From menu.cadprt'; errors = []
        def accept_dialog():
            dialog = QtWidgets.QApplication.activeModalWidget()
            try:
                self.assertIsInstance(dialog, part_transfer.ExportDialog)
                self.assertEqual(len(dialog.definitions), 2)
                dialog.filename.setText(str(path)); dialog.submit.click()
                self.assertEqual(dialog.result(), QtWidgets.QDialog.Accepted)
            except BaseException as error:
                errors.append(str(error))
                if dialog: dialog.reject()
        def select_export():
            menu = QtWidgets.QApplication.activePopupWidget()
            try:
                action = next(a for a in menu.actions() if a.text() == 'Export parts to file…')
                menu.grab().save(str(self.out/'parts-menu.png'))
                QtCore.QTimer.singleShot(100, accept_dialog); action.trigger()
            except BaseException as error: errors.append(str(error))
            finally:
                if menu: menu.close()
        QtCore.QTimer.singleShot(100, select_export)
        self.dock._menu(tree, tree.visualItemRect(rows[0]).center())
        self.assertEqual(errors, []); self.assertTrue(path.is_file())

    @unittest.skipUnless(os.name == 'nt', 'Windows atomic rename publication')
    def test_export_target_created_during_copy_is_not_overwritten(self):
        rename = os.rename; path = self.out/'Selected parts.cadprt'
        def race(source, target):
            Path(target).write_bytes(b'Concurrent owner file')
            return rename(source, target)
        with patch.object(part_transfer_ops.os, 'rename', side_effect=race):
            with self.assertRaises(FileExistsError): self.export()
        self.assertEqual(path.read_bytes(), b'Concurrent owner file')
        self.assertFalse(any(p.name.startswith('.part-export-') for p in self.out.iterdir()))

    def test_export_refuses_existing_file_and_preserves_source(self):
        path = self.out/'Selected parts.cadprt'; path.write_bytes(b'Owner file')
        before = self.state(); docs = set(App.listDocuments())
        with self.assertRaisesRegex(ValueError, 'already exists'): self.export()
        self.assertEqual(path.read_bytes(), b'Owner file'); self.assertEqual(self.state(), before)
        self.assertEqual(set(App.listDocuments()), docs)

    def test_export_write_failure_cleans_private_files_and_document(self):
        before = self.state(); docs = set(App.listDocuments()); files = set(self.out.iterdir())
        original = document.save_document
        calls = []
        def fail(doc, filename=None):
            calls.append(filename)
            if len(calls) == 2: raise OSError('Injected save failure')
            return original(doc, filename)
        with patch.object(document, 'save_document', side_effect=fail):
            with self.assertRaisesRegex(OSError, 'Injected'): self.export()
        self.assertEqual(set(self.out.iterdir()), files)
        self.assertEqual(set(App.listDocuments()), docs); self.assertEqual(self.state(), before)
        self.assertEqual(App.ActiveDocument, self.doc)

    def test_export_dialog_cancel_and_accept(self):
        before = self.state(); path = self.out/'Dialog export.cadprt'
        dialog = part_transfer.ExportDialog(self.dock, [self.drive, self.cover])
        dialog.filename.setText(str(path)); dialog.reject(); dialog.deleteLater()
        self.assertFalse(path.exists()); self.assertEqual(self.state(), before)
        dialog = part_transfer.ExportDialog(self.dock, [self.drive, self.cover])
        try:
            dialog.filename.setText(str(path)); dialog.show(); QtTest.QTest.qWait(80)
            dialog.grab().save(str(self.out/'export-parts.png'))
            dialog.submit.click()
            self.assertEqual(dialog.result(), QtWidgets.QDialog.Accepted)
            self.assertTrue(path.is_file()); self.assertEqual(self.state(), before)
        finally: dialog.deleteLater()

    def test_export_pending_operation_rejected(self):
        self.doc.openTransaction('Pending')
        self.box.Length = 5
        try:
            with self.assertRaisesRegex(ValueError, 'Finish'): self.export()
        finally: self.doc.abortTransaction()


def verify_fresh_process(folder):
    folder = Path(folder)/'test_export_nested_constraints_save_reopen_and_solve'
    expected = json.loads((folder/'expected.json').read_text())
    doc = document.open_document(expected['file'])
    root = document.validate(doc)
    assert str(doc.Uid) == expected['uid']
    assert {o.Name:o.ID for o in doc.Objects} == expected['ids']
    assert len([p for p in root.Definitions if constraints.joints(p)]) == expected['collectors']
    for part in root.Definitions:
        if constraints.joints(part): assert constraints.solver_for(part).solve() == 0
    assert root.Imports == []
    return {'saved_ids_uid_collectors_and_native_solve':True, 'objects':len(doc.Objects)}
