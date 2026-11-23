# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native watcher, shared command routing and creation navigation regression checks."""
import os
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtWidgets, QtTest
from freecad_plus import document, editing, modeling, hierarchy, panel, ui_modes, extrude_task, sketch_task


def settle():
    QtTest.QTest.qWait(250)


def action_boxes():
    return [(w, [a.text().replace('&', '') for a in w.actions()])
            for w in Gui.getMainWindow().findChildren(QtWidgets.QWidget)
            if w.isVisible() and 'TaskBox' in w.metaObject().className() and w.actions()]


class TestTaskEntryWorkflows(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:
            self.skipTest('Requires an isolated native profile')
        self.before = set(App.listDocuments())
        self.prefs = App.ParamGet('User parameter:BaseApp/Preferences/General')
        self.old = [self.prefs.GetInt(key, 0) for key in ui_modes.KEYS]
        for key in ui_modes.KEYS:self.prefs.SetInt(key, 0)
        Gui.activateWorkbench('PartWorkbench');Gui.activateWorkbench('PartDesignWorkbench')
        self.doc = document.new_document('TaskEntryFixture')
        self.owner = document.validate(self.doc).Definitions[0]
        self.widget = panel._panel
        self.profile = modeling.new_sketch(self.doc)
        self.profile.addGeometry(Part.Circle(App.Vector(5, 0, 0), App.Vector(0, 0, 1), 2), False)
        self.doc.recompute();settle()

    def tearDown(self):
        if extrude_task._active:extrude_task._active.reject()
        if sketch_task._active:sketch_task._active.reject()
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments()) - self.before:App.closeDocument(name)
        for key, value in zip(ui_modes.KEYS, self.old):self.prefs.SetInt(key, value)
        ui_modes.apply_modes();settle()

    def select(self, obj=None):
        Gui.Selection.clearSelection()
        if obj is not None:Gui.Selection.addSelection(obj)
        settle()

    def state(self):
        return {o.Name:(o.ID, tuple(x.Name for x in o.OutList), o.Visibility) for o in self.doc.Objects}

    def test_idle_never_offers_new_body_in_either_mode_or_context(self):
        for mode in (0, 1):
            self.prefs.SetInt('TaskPanelUIMode', mode)
            for active in (False, True):
                if active:editing.edit(document.validate(self.doc).Group[0])
                else:editing.edit_file(self.doc)
                # A real panel Edit selects its context before the user clears it.
                self.select(self.profile)
                self.select()
                lists = [labels for _, labels in action_boxes()]
                self.assertFalse(any('New Body' in labels for labels in lists), lists)
                if mode == 0 and active:
                    self.assertIn(['New Sketch', 'Datum Plane', 'Datum Line', 'Datum Point'], lists)
        empty = App.newDocument('EmptyTaskEntry');self.select()
        for mode in (0, 1):
            self.prefs.SetInt('TaskPanelUIMode', mode)
            Gui.activateWorkbench('PartWorkbench');Gui.activateWorkbench('PartDesignWorkbench');settle()
            self.assertFalse(any('New Body' in labels for _, labels in action_boxes()))
        App.closeDocument(empty.Name)

    def test_sketch_watchers_switch_without_workbench_reactivation(self):
        for task_mode, toolbar_mode in ((0, 1), (1, 0), (0, 0), (1, 1)):
            self.prefs.SetInt('TaskPanelUIMode', task_mode)
            self.prefs.SetInt('ToolbarUIMode', toolbar_mode);ui_modes.apply_modes()
            self.select(self.profile)
            lists = [labels for _, labels in action_boxes()]
            self.assertEqual(len(lists), 1, lists)
            labels = lists[0]
            if task_mode == 0:
                self.assertEqual(labels[:4], ['New Sketch', 'Extrude', 'Hole', 'Revolve'])
                self.assertNotIn('Pocket', labels);self.assertNotIn('Groove', labels)
            else:
                self.assertEqual(labels[:6], ['New Sketch', 'Pad', 'Pocket', 'Hole', 'Revolve', 'Groove'])
            self.assertEqual(labels[-6:], ['Additive Loft', 'Subtractive Loft', 'Additive Pipe',
                                         'Subtractive Pipe', 'Additive Helix', 'Subtractive Helix'])
            self.select()
            self.assertFalse(any('Hole' in labels for _, labels in action_boxes()))

    def test_actual_task_actions_share_panels_and_cancel_preserves_document(self):
        original = self.state()
        for mode in (0, 1):
            self.prefs.SetInt('TaskPanelUIMode', mode)
            entries = [('Extrude', 'Extrude', 'New Solid'), ('Revolve', 'Revolve', 'New Solid')] if mode == 0 else [
                ('Pad', 'Extrude', 'New Solid'), ('Pocket', 'Extrude', 'Subtract'),
                ('Revolve', 'Revolve', 'New Solid'), ('Groove', 'Revolve', 'Subtract')]
            for label, title, operation in entries:
                self.widget.tabs.setCurrentIndex(0);self.select(self.profile)
                box = next(w for w, labels in action_boxes() if label in labels)
                action = next(a for a in box.actions() if a.text().replace('&', '') == label)
                self.assertTrue(action.isEnabled());action.trigger();settle()
                task = extrude_task._active
                self.assertIsNotNone(task);self.assertEqual(task.title, title)
                self.assertEqual(task.mode(), operation);self.assertEqual(task.refs[0][0], self.profile)
                self.assertEqual(self.widget.tabs.currentIndex(), 2)
                task.reject();settle()
                self.assertEqual(self.widget.tabs.currentIndex(), 0)
                self.assertEqual(self.state(), original)

    def test_creation_navigation_factories_and_task_restoration(self):
        self.widget.tabs.setCurrentIndex(1)
        original = editing.context(self.doc)[0]
        hierarchy.create_definition(self.doc, 'Catalog only');settle()
        self.assertEqual(editing.context(self.doc)[0], original)
        self.assertEqual(self.widget.tabs.currentIndex(), 1)
        created = hierarchy.new_part();settle()
        self.assertEqual(editing.context(self.doc)[0], created)
        self.assertEqual(self.widget.tabs.currentIndex(), 2)
        links = tuple(document.validate(self.doc).Group)
        task = sketch_task.show();settle()
        with self.assertRaises(ValueError):hierarchy.new_part()
        self.assertEqual(editing.context(self.doc)[0], created)
        task.reject();settle()
        self.assertEqual(self.widget.tabs.currentIndex(), 2)
        self.assertEqual(tuple(document.validate(self.doc).Group), links)
