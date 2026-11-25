# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native format saves, non-destructive conversion and actual GUI entry points."""
import hashlib
import os
from pathlib import Path
import shutil
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets, QtTest
from freecad_plus import document, hierarchy, editing, external, panel, component_add, document_import
from freecad_plus import file_workflows as files


class TestFileWorkflows(unittest.TestCase):
    def setUp(self):
        self.before = set(App.listDocuments())
        self.out = Path(os.environ['PLUS_TEST_DIR']) / ('fw-' + hashlib.sha256(self._testMethodName.encode()).hexdigest()[:10])
        self.out.mkdir(exist_ok=True)
        App.ParamGet('User parameter:BaseApp/Preferences/Dialog').SetBool('DontUseNativeDialog', True)
        App.ParamGet('User parameter:BaseApp/Preferences/Document').SetBool('DisableVersionCheckOnSave', True)
        self.plus = document.new_document('Machine')
        self.owner = document.validate(self.plus).Definitions[0]
        self.owner.newObject('Part::Box', 'Box')
        self.plus.recompute()
        self.callbacks = []

    def tearDown(self):
        for widget in QtWidgets.QApplication.topLevelWidgets():
            if isinstance(widget, QtWidgets.QDialog) and widget.isVisible():
                widget.reject()
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)
        QtTest.QTest.qWait(50)

    def classic(self):
        doc = App.newDocument('ClassicFixture')
        obj = doc.addObject('Part::Box', 'Box'); obj.Length = 4
        doc.recompute()
        path = self.out / 'original.FCStd'
        doc.saveAs(str(path))
        return doc, path

    def digest(self, path):
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()

    def dialog_action(self, action):
        """Run bounded automation while the actual native command owns its modal dialog."""
        state = {'done': False, 'error': None}
        def act():
            dialog = QtWidgets.QApplication.activeModalWidget()
            try:
                if dialog is None:
                    raise AssertionError('No modal dialog opened')
                dialog.grab().save(str(self.out / ('dialog-' + str(len(self.callbacks)) + '.png')))
                action(dialog)
                if (isinstance(dialog, files.ConversionDialog)
                        and dialog.result() != QtWidgets.QDialog.Accepted and not dialog.status.isHidden()):
                    dialog.grab().save(str(self.out / 'conversion-error.png'))
                    raise AssertionError(dialog.status.text())
            except BaseException as error:
                state['error'] = error
                if dialog: dialog.reject()
            state['done'] = True
        QtCore.QTimer.singleShot(150, act)
        self.callbacks.append(act)
        return state

    def assert_action(self, state):
        self.assertTrue(state['done'])
        if state['error']: raise state['error']

    def choose_file(self, dialog, name):
        dialog.setDirectory(str(self.out))
        QtWidgets.QApplication.processEvents()
        dialog.findChild(QtWidgets.QLineEdit, 'fileNameEdit').setText(name)
        dialog.accept()

    def test_native_plus_save_as_copy_and_reopen(self):
        for supplied, expected in [('first', 'first.cadprt'), ('second.FCStd', 'second.cadprt'),
                                   ('UPPER.CADPRT', 'UPPER.CADPRT')]:
            self.plus.saveAs(str(self.out / supplied))
            self.assertEqual(Path(self.plus.FileName).name, expected)
            self.assertEqual(files.archive_kind(self.plus.FileName), 'plus')
        filename = self.plus.FileName
        self.plus.saveCopy(str(self.out / 'copy.FCStd'))
        self.assertTrue((self.out / 'copy.cadprt').exists())
        self.assertEqual(self.plus.FileName, filename)
        self.plus.save()
        App.closeDocument(self.plus.Name)
        reopened = document.open_document(filename)
        self.assertEqual(len(document.validate(reopened).Definitions), 1)
        self.assertAlmostEqual(reopened.getObject('Box').Shape.Volume, 1000)

    def test_native_classic_cannot_save_as_cadprt(self):
        classic, source = self.classic()
        classic.saveAs(str(self.out / 'renamed.cadprt'))
        self.assertEqual(Path(classic.FileName).name, 'renamed.FCStd')
        classic.saveCopy(str(self.out / 'copy.cadprt'))
        self.assertTrue((self.out / 'copy.FCStd').exists())
        self.assertFalse((self.out / 'copy.cadprt').exists())

    def test_direct_save_rejects_wrong_extension_even_with_preference_disabled(self):
        prefs = App.ParamGet('User parameter:BaseApp/Preferences/Document')
        previous = prefs.GetBool('CheckExtension', True)
        prefs.SetBool('CheckExtension', False)
        try:
            self.plus.FileName = str(self.out / 'wrong.FCStd')
            with self.assertRaises(Exception): self.plus.save()
            self.assertFalse(Path(self.plus.FileName).exists())
            self.plus.saveAs(str(self.out / 'correct.FCStd'))
            self.assertTrue((self.out / 'correct.cadprt').exists())
        finally:
            prefs.SetBool('CheckExtension', previous)

    def test_gui_save_as_plus_filter_and_filename(self):
        App.setActiveDocument(self.plus.Name)
        def choose(dialog):
            self.assertIsInstance(dialog, QtWidgets.QFileDialog)
            self.assertEqual(dialog.nameFilters(), [files.PLUS_FILTER])
            self.choose_file(dialog, 'gui.cadprt')
        state = self.dialog_action(choose)
        Gui.runCommand('Std_SaveAs', 0)
        self.assert_action(state)
        self.assertEqual(Path(self.plus.FileName).name, 'gui.cadprt')
        self.assertTrue((self.out / 'gui.cadprt').exists())

    def test_gui_save_copy_classic_filter(self):
        classic, source = self.classic()
        def choose(dialog):
            self.assertEqual(dialog.nameFilters(), [files.CLASSIC_FILTER])
            self.choose_file(dialog, 'gui-copy.FCStd')
        state = self.dialog_action(choose)
        Gui.runCommand('Std_SaveCopy', 0)
        self.assert_action(state)
        self.assertEqual(Path(classic.FileName), source)
        self.assertTrue((self.out / 'gui-copy.FCStd').exists())

    def test_gui_open_filters_keep_geometry_importers(self):
        def inspect(dialog):
            filters = dialog.nameFilters()
            self.assertEqual(filters[:3], [files.NATIVE_FILTER, files.PLUS_FILTER, files.CLASSIC_FILTER])
            self.assertEqual(dialog.selectedNameFilter(), files.NATIVE_FILTER)
            self.assertTrue(any('*.step' in f.lower() for f in filters))
            dialog.reject()
        state = self.dialog_action(inspect)
        Gui.runCommand('Std_Open', 0)
        self.assert_action(state)

    def test_native_import_defaults_to_both_formats_even_after_single_format(self):
        prefs = App.ParamGet('User parameter:BaseApp/Preferences/General')
        previous = prefs.GetString('FileImportFilter')
        prefs.SetString('FileImportFilter', files.PLUS_FILTER)
        def inspect(dialog):
            self.assertEqual(dialog.selectedNameFilter(), files.NATIVE_FILTER)
            self.assertTrue(any('*.step' in f.lower() for f in dialog.nameFilters()))
            dialog.reject()
        try:
            state = self.dialog_action(inspect)
            Gui.runCommand('Std_Import', 0)
            self.assert_action(state)
        finally:
            prefs.SetString('FileImportFilter', previous)

    def test_component_source_chooser_shows_both_formats(self):
        _, source = self.classic()
        document.save_document(self.plus, self.out / 'machine.cadprt')
        def inspect(dialog):
            dialog.setDirectory(str(self.out))
            QtTest.QTest.qWait(100)
            self.assertEqual(dialog.selectedNameFilter(), files.NATIVE_FILTER)
            model = dialog.findChild(QtWidgets.QFileSystemModel)
            parent = model.index(str(self.out))
            visible = {model.fileName(model.index(row, 0, parent)) for row in range(model.rowCount(parent))}
            self.assertIn(source.name, visible)
            self.assertIn('machine.cadprt', visible)
            dialog.reject()
        attribute = QtCore.Qt.AA_DontUseNativeDialogs
        previous = QtWidgets.QApplication.testAttribute(attribute)
        QtWidgets.QApplication.setAttribute(attribute, True)
        try:
            state = self.dialog_action(inspect)
            self.assertIsNone(files.choose_source(Gui.getMainWindow(), 'Import file', 'import'))
        finally:
            QtWidgets.QApplication.setAttribute(attribute, previous)
        self.assert_action(state)

    def test_conversion_cursor_restores_after_error_cancel_and_success(self):
        _, source = self.classic()
        app = QtWidgets.QApplication
        app.setOverrideCursor(QtCore.Qt.CrossCursor)
        try:
            def choose(dialog):
                self.assertEqual(app.overrideCursor().shape(), QtCore.Qt.ArrowCursor)
                convert = files.conversion.convert_file
                def checked_convert(*args, **kwargs):
                    self.assertEqual(app.overrideCursor().shape(), QtCore.Qt.WaitCursor)
                    return convert(*args, **kwargs)
                with patch.object(files.conversion, 'convert_file', side_effect=checked_convert):
                    existing = self.out / 'existing.cadprt'
                    existing.write_bytes(b'existing output')
                    dialog.destination.setText(str(existing))
                    dialog.accept()
                    self.assertFalse(dialog.status.isHidden())
                    self.assertEqual(app.overrideCursor().shape(), QtCore.Qt.ArrowCursor)
                    dialog.destination.setText(str(self.out / 'copy.cadprt'))
                    dialog.accept()
                self.assertEqual(app.overrideCursor().shape(), QtCore.Qt.ArrowCursor)
            state = self.dialog_action(choose)
            result = files.prepare_source(source)
            self.assert_action(state)
            self.assertTrue(result)
            self.assertEqual(app.overrideCursor().shape(), QtCore.Qt.CrossCursor)
            state = self.dialog_action(lambda dialog: dialog.reject())
            self.assertIsNone(files.prepare_source(source))
            self.assert_action(state)
            self.assertEqual(app.overrideCursor().shape(), QtCore.Qt.CrossCursor)
        finally:
            app.restoreOverrideCursor()

    def test_native_open_repair_cursor_idle_until_save_copy(self):
        document.save_document(self.plus, self.out / 'machine.cadprt')
        source = self.out / 'mislabelled.FCStd'
        shutil.copy2(self.plus.FileName, source)
        app = QtWidgets.QApplication
        prior = app.overrideCursor().shape() if app.overrideCursor() else None
        second = []
        def repair(dialog):
            self.assertEqual(dialog.primary.text(), 'Save .cadprt copy')
            self.assertEqual(app.overrideCursor().shape(), QtCore.Qt.ArrowCursor)
            original = files.repair_copy
            def checked_repair(*args):
                self.assertEqual(app.overrideCursor().shape(), QtCore.Qt.WaitCursor)
                return original(*args)
            with patch.object(files, 'repair_copy', side_effect=checked_repair):
                dialog.accept()
        def choose(dialog):
            self.assertEqual(dialog.selectedNameFilter(), files.NATIVE_FILTER)
            second.append(self.dialog_action(repair))
            self.choose_file(dialog, source.name)
        first = self.dialog_action(choose)
        Gui.runCommand('Std_Open', 0)
        self.assert_action(first); self.assert_action(second[0])
        self.assertEqual(app.overrideCursor().shape() if app.overrideCursor() else None, prior)
        self.assertTrue(source.with_suffix('.cadprt').exists())

    def test_convert_dialog_preserves_source_and_live_unsaved_edits(self):
        classic, source = self.classic()
        digest = self.digest(source)
        classic.getObject('Box').Length = 9
        App.setActiveDocument(self.plus.Name)
        before = set(App.listDocuments())
        dialog = files.ConversionDialog(None, source)
        dialog.accept()
        self.assertEqual(dialog.result(), QtWidgets.QDialog.Accepted, dialog.status.text())
        self.assertEqual(set(App.listDocuments()), before)
        self.assertEqual(App.ActiveDocument, self.plus)
        self.assertEqual(self.digest(source), digest)
        self.assertEqual(classic.getObject('Box').Length.Value, 9)
        converted = document.open_document(dialog.result_path)
        self.assertEqual(converted.getObject('Box').Length.Value, 4)
        self.assertNotEqual(str(converted.Uid), str(classic.Uid))
        dialog.deleteLater()

    def test_conversion_cancel_and_existing_destination(self):
        _, source = self.classic()
        target = source.with_suffix('.cadprt'); target.write_bytes(b'existing')
        dialog = files.ConversionDialog(None, source)
        dialog.accept()
        self.assertEqual(dialog.result(), QtWidgets.QDialog.Rejected)
        self.assertEqual(target.read_bytes(), b'existing')
        dialog.reject(); dialog.deleteLater()
        target.unlink()
        with patch.object(files.ConversionDialog, 'exec', return_value=QtWidgets.QDialog.Rejected):
            self.assertIsNone(files.prepare_source(source))
        self.assertFalse(target.exists())

    def test_conversion_preserves_another_documents_pending_transaction(self):
        _, source = self.classic()
        self.plus.openTransaction('Unfinished user edit')
        self.plus.getObject('Box').Length = 17
        pending = App.getActiveTransaction()
        try:
            dialog = files.ConversionDialog(None, source)
            dialog.accept()
            self.assertEqual(dialog.result(), QtWidgets.QDialog.Rejected)
            self.assertIn('Finish the current operation', dialog.status.text())
            self.assertTrue(self.plus.HasPendingTransaction)
            self.assertEqual(App.getActiveTransaction(), pending)
            self.assertEqual(self.plus.getObject('Box').Length.Value, 17)
            self.assertFalse(source.with_suffix('.cadprt').exists())
            dialog.deleteLater()
        finally:
            self.plus.abortTransaction()

    def test_open_classic_choice_does_not_convert(self):
        classic, source = self.classic()
        App.closeDocument(classic.Name)
        def choose(dialog): dialog.open_classic()
        state = self.dialog_action(choose)
        opened = files.open_file(source)
        self.assert_action(state)
        self.assertFalse(any('PlusFormat' in o.PropertiesList for o in opened.Objects))
        self.assertFalse(source.with_suffix('.cadprt').exists())

    def test_native_open_command_converts_and_opens_plus(self):
        classic, source = self.classic()
        App.closeDocument(classic.Name)
        second = []
        def choose(dialog):
            self.assertEqual(dialog.selectedNameFilter(), files.NATIVE_FILTER)
            second.append(self.dialog_action(lambda conversion_dialog: conversion_dialog.accept()))
            self.choose_file(dialog, source.name)
        first = self.dialog_action(choose)
        Gui.runCommand('Std_Open', 0)
        self.assert_action(first); self.assert_action(second[0])
        self.assertEqual(Path(App.ActiveDocument.FileName), source.with_suffix('.cadprt'))
        document.validate(App.ActiveDocument)

    def test_panel_import_converts_without_placing_children(self):
        _, source = self.classic()
        App.setActiveDocument(self.plus.Name)
        document.save_document(self.plus, self.out / 'machine.cadprt')
        editing.edit((document.validate(self.plus).Group[0],))
        dock = panel.show_panel(); dock.refresh()
        count = len(self.owner.Group)
        state = self.dialog_action(lambda dialog: dialog.accept())
        with patch.object(QtWidgets.QFileDialog, 'getOpenFileName', return_value=(str(source), files.CLASSIC_FILTER)):
            dock.import_models()
        self.assert_action(state)
        self.assertEqual(len(document.validate(self.plus).Imports), 1)
        self.assertEqual(len(self.owner.Group), count)

    def test_gui_save_cancel_retains_filename_and_modified_state(self):
        App.setActiveDocument(self.plus.Name)
        old = self.plus.FileName
        state = self.dialog_action(lambda dialog: dialog.reject())
        self.assertFalse(Gui.getDocument(self.plus.Name).saveAs())
        self.assert_action(state)
        self.assertEqual(self.plus.FileName, old)
        self.assertTrue(Gui.getDocument(self.plus.Name).Modified)

    def test_save_on_close_uses_cadprt(self):
        App.setActiveDocument(self.plus.Name)
        name = self.plus.Name
        second = []
        def confirm(dialog):
            self.assertIsInstance(dialog, QtWidgets.QMessageBox)
            second.append(self.dialog_action(lambda chooser: self.choose_file(chooser, 'closed.cadprt')))
            dialog.button(QtWidgets.QMessageBox.Save).click()
        first = self.dialog_action(confirm)
        Gui.runCommand('Std_CloseActiveWindow', 0)
        self.assert_action(first); self.assert_action(second[0])
        self.assertTrue((self.out / 'closed.cadprt').exists())
        QtTest.QTest.qWait(100)
        self.assertNotIn(name, App.listDocuments())

    def test_unsupported_conversion_reports_error_without_output(self):
        classic, source = self.classic()
        classic.addObject('Part::Box', 'Other'); classic.recompute(); classic.save()
        before = set(App.listDocuments())
        dialog = files.ConversionDialog(None, source)
        dialog.accept()
        self.assertEqual(dialog.result(), QtWidgets.QDialog.Rejected)
        self.assertEqual(set(App.listDocuments()), before)
        self.assertFalse(source.with_suffix('.cadprt').exists())
        self.assertFalse(dialog.status.isHidden())
        dialog.deleteLater()

    def test_mislabelled_plus_repair_preserves_links_and_source(self):
        source_doc = document.new_document('Hardware')
        definition = document.validate(source_doc).Definitions[0]
        definition.Label = 'Hardware component'
        document.save_document(source_doc, self.out / 'hardware.cadprt')
        document.save_document(self.plus, self.out / 'machine.cadprt')
        hierarchy.add_child(self.owner, definition)
        document.save_document(self.plus)
        wrong = self.out / 'old.FCStd'; shutil.copy2(self.plus.FileName, wrong)
        digest = self.digest(wrong)
        target_dir = self.out / 'elsewhere'; target_dir.mkdir()
        corrected = files.repair_copy(wrong, target_dir / 'corrected.cadprt')
        document.inspect_archive(corrected.FileName)
        self.assertEqual(self.digest(wrong), digest)
        self.assertNotEqual(str(corrected.Uid), str(self.plus.Uid))
        self.assertEqual(len(document.validate(corrected).Imports), 1)

    def test_native_save_as_and_copy_keep_external_links_in_other_directory(self):
        source = document.new_document('Hardware')
        definition = document.validate(source).Definitions[0]
        definition.Label = 'Hardware component'
        document.save_document(source, self.out / 'hardware.cadprt')
        document.save_document(self.plus, self.out / 'machine.cadprt')
        hierarchy.add_child(self.owner, definition)
        self.plus.save()
        other = self.out / 'elsewhere'; other.mkdir()
        self.plus.saveCopy(str(other / 'copy.cadprt'))
        document.inspect_archive(other / 'copy.cadprt')
        self.plus.saveAs(str(other / 'moved.FCStd'))
        document.inspect_archive(other / 'moved.cadprt')

    def test_gui_save_repairs_mislabelled_filename(self):
        self.plus.FileName = str(self.out / 'wrong.FCStd')
        state = self.dialog_action(lambda dialog: self.choose_file(dialog, 'correct.cadprt'))
        self.assertTrue(Gui.getDocument(self.plus.Name).save())
        self.assert_action(state)
        self.assertTrue((self.out / 'correct.cadprt').exists())
        self.assertFalse((self.out / 'wrong.FCStd').exists())

    def test_gui_save_all_uses_document_specific_extensions(self):
        # Save the Plus document first, then have Save All name an unsaved Classic doc.
        document.save_document(self.plus, self.out / 'machine.cadprt')
        self.plus.getObject('Box').Length = 12
        classic = App.newDocument('UnsavedClassic'); classic.addObject('Part::Box', 'Box')
        state = self.dialog_action(lambda dialog: self.choose_file(dialog, 'classic.FCStd'))
        Gui.runCommand('Std_SaveAll', 0)
        self.assert_action(state)
        self.assertTrue((self.out / 'classic.FCStd').exists())
        self.assertEqual(Path(self.plus.FileName).suffix, '.cadprt')
        self.assertFalse(Gui.getDocument(self.plus.Name).Modified)

    def test_classic_data_cannot_open_as_cadprt(self):
        _, source = self.classic()
        wrong = source.with_suffix('.cadprt'); shutil.copy2(source, wrong)
        with self.assertRaisesRegex(ValueError, 'Classic data'):
            files.open_file(wrong)

    def test_native_import_converts_to_catalog_without_placement(self):
        _, source = self.classic()
        App.setActiveDocument(self.plus.Name)
        document.save_document(self.plus, self.out / 'machine.cadprt')
        count = len(self.owner.Group)
        second = []
        def convert(dialog):
            self.assertEqual(QtWidgets.QApplication.overrideCursor().shape(), QtCore.Qt.ArrowCursor)
            dialog.accept()
        def choose(dialog):
            self.assertEqual(dialog.selectedNameFilter(), files.NATIVE_FILTER)
            second.append(self.dialog_action(convert))
            self.choose_file(dialog, source.name)
        first = self.dialog_action(choose)
        Gui.runCommand('Std_Import', 0)
        self.assert_action(first); self.assert_action(second[0])
        root = document.validate(self.plus)
        self.assertEqual(len(root.Imports), 1)
        self.assertEqual(len(self.owner.Group), count)
        self.assertTrue(source.with_suffix('.cadprt').exists())

    def test_combined_filter_opens_and_imports_plus_documents(self):
        source = document.new_document('Hardware')
        document.validate(source).Definitions[0].Label = 'HardwarePart'
        path = document.save_document(source, self.out / 'hardware.cadprt')
        App.closeDocument(source.Name)
        App.setActiveDocument(self.plus.Name)
        first = self.dialog_action(lambda dialog: self.choose_file(dialog, 'hardware.cadprt'))
        Gui.runCommand('Std_Open', 0)
        self.assert_action(first)
        self.assertEqual(Path(App.ActiveDocument.FileName), Path(path))
        App.closeDocument(App.ActiveDocument.Name)
        document.save_document(self.plus, self.out / 'machine.cadprt')
        App.setActiveDocument(self.plus.Name)
        second = self.dialog_action(lambda dialog: self.choose_file(dialog, 'hardware.cadprt'))
        Gui.runCommand('Std_Import', 0)
        self.assert_action(second)
        self.assertEqual(len(document.validate(self.plus).Imports), 1)

    def test_add_existing_converts_without_changing_edit_context(self):
        _, source = self.classic()
        App.setActiveDocument(self.plus.Name)
        document.save_document(self.plus, self.out / 'machine.cadprt')
        editing.edit((document.validate(self.plus).Group[0],))
        before_context = component_add.target()[1]
        dialog = component_add.Picker(None)
        state = self.dialog_action(lambda conversion_dialog: conversion_dialog.accept())
        with patch.object(QtWidgets.QFileDialog, 'getOpenFileName', return_value=(str(source), files.CLASSIC_FILTER)):
            dialog.open_source()
        self.assert_action(state)
        self.assertEqual(component_add.target()[1], before_context)
        self.assertEqual(len(document.validate(self.plus).Imports), 0)
        self.assertTrue(source.with_suffix('.cadprt').exists())
        self.assertTrue(dialog.opened)
        dialog.reject(); dialog.deleteLater()
