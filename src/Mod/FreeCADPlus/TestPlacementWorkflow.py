# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native placement styles and active-component destination acceptance."""
import unittest
from unittest.mock import patch
import FreeCAD as App, FreeCADGui as Gui
from PySide6 import QtCore, QtGui, QtWidgets, QtTest
from pivy import coin
from freecad_plus import component_add, document, editing, hierarchy, instance_task, panel
from TestInstanceQuantity import TestInstanceQuantity


class TestPlacementWorkflow(unittest.TestCase):
    setUp = TestInstanceQuantity.setUp
    tearDown = TestInstanceQuantity.tearDown
    snapshot = TestInstanceQuantity.snapshot

    def prompt(self, accept=False, during=None):
        seen = []
        def answer(dialog):
            seen.append(dialog.text())
            self.assertEqual(dialog.defaultButton(), dialog.cancel)
            if during: during()
            (dialog.make_active if accept else dialog.cancel).click()
            return 0
        return patch.object(component_add.ActiveAssemblyPrompt, 'exec_', answer), seen

    def test_nested_and_top_level_destinations_ignore_selected_source(self):
        child = hierarchy.create_definition(self.doc, 'Bracket')
        link = hierarchy.add_instance(self.owner, child)
        for destination, route in ((self.owner, (self.top,)), (child, (self.top, link))):
            editing.edit(route); self.dock.refresh()
            Gui.Selection.clearSelection(); Gui.Selection.addSelection(self.part)
            before = self.snapshot()
            with patch.object(component_add.ActiveAssemblyPrompt, 'exec_', side_effect=AssertionError('Unexpected prompt')):
                task = component_add.add_selected(self.dock, [self.part])
            self.assertEqual(task.owner, destination)
            self.assertEqual(self.snapshot(), before)
            self.assertTrue(task.accept())
            self.assertEqual(task.created[0].LinkedObject, self.part)
            self.assertIn(task.created[0], destination.Group)
            self.doc.undo(); QtTest.QTest.qWait(80)
            self.assertEqual(self.snapshot()[0], before[0])
            self.assertEqual(component_add.active_assembly(), self.owner)

    def test_outside_cancel_leaves_context_geometry_and_undo_unchanged(self):
        editing.edit_unused(self.doc, self.part); self.dock.refresh()
        before = self.snapshot(); mock, seen = self.prompt()
        with mock:
            self.assertIsNone(component_add.add_selected(self.dock, [self.owner]))
        self.assertEqual(len(seen), 1)
        self.assertEqual(self.snapshot(), before)
        self.assertIsNone(instance_task._active)

    def test_outside_accept_switches_assembly_and_creates_one_undo(self):
        editing.edit_unused(self.doc, self.part); self.dock.refresh()
        before = self.snapshot(); mock, seen = self.prompt(True)
        with mock:
            task = component_add.add_selected(self.dock, [self.owner])
        self.assertEqual(len(seen), 1)
        self.assertEqual(component_add.active_assembly(), self.part)
        self.assertEqual(editing.context_path(self.doc), before[2])
        self.assertEqual(self.doc.UndoCount, before[1])
        self.assertTrue(task.accept())
        self.assertIn(task.created[0], self.part.Group)
        self.assertEqual(self.doc.UndoCount, before[1] + 1)
        self.doc.undo(); self.assertEqual(self.snapshot()[0], before[0])

    def test_stale_prompt_does_not_switch_or_add(self):
        editing.edit_unused(self.doc, self.part); self.dock.refresh()
        before = self.snapshot()[0]
        mock, _ = self.prompt(True, lambda: editing.edit((self.top,)))
        with mock, self.assertRaisesRegex(ValueError, 'changed'):
            component_add.ensure_destination(self.dock)
        self.assertEqual(component_add.active_assembly(), self.owner)
        self.assertEqual(self.snapshot()[0], before)

    def test_parts_menu_routes_checked_source_to_active_component(self):
        self.dock.tabs.setCurrentIndex(0); tree = self.dock.trees[0]
        item = next(i for i in self.dock._maps[0].values()
                    if i.data(0, panel._ROLE).kind == 'model' and i.data(0, panel._ROLE).ref == panel.identity(self.part))
        tree.setCurrentItem(item); tree.scrollToItem(item)
        seen = []
        def choose(menu, *args):
            action = next(a for a in menu.actions() if a.text() == 'Add to active component…')
            seen.append(action.text()); action.trigger()
        with patch.object(QtWidgets.QMenu, 'exec_', choose):
            self.dock._menu(tree, tree.visualItemRect(item).center())
        self.assertEqual(seen, ['Add to active component…'])
        task = instance_task._active
        self.assertIsNotNone(task); self.assertEqual(task.owner, self.owner)
        self.assertEqual(task.parts, (panel.identity(self.part),))
        task.reject()

    def test_ribbon_existing_and_new_use_active_child(self):
        child = hierarchy.create_definition(self.doc, 'Bracket')
        link = hierarchy.add_instance(self.owner, child)
        editing.edit((self.top, link)); self.dock.refresh()
        button = component_add.make_button(self.dock, Gui.getMainWindow())
        try:
            for new, action in zip((False, True), button.menu().actions()):
                before = self.snapshot()
                def choose(dialog):
                    self.assertEqual(dialog.owner, child)
                    if new: dialog.name.setText('Created pin')
                    else:
                        it = QtWidgets.QTreeWidgetItemIterator(dialog.choices)
                        while it.value():
                            if it.value().data(0, QtCore.Qt.UserRole) == panel.identity(self.part):
                                it.value().setCheckState(0, QtCore.Qt.Checked)
                            it += 1
                    dialog.accept(); return dialog.result()
                with patch.object(component_add.Picker, 'exec_', choose): action.trigger()
                task = instance_task._active
                self.assertIsNotNone(task); self.assertEqual(task.owner, child)
                self.assertTrue(task.accept())
                self.assertIn(task.created[0], child.Group)
                self.assertEqual(task.created[0].LinkedObject.Label, 'Created pin' if new else self.part.Label)
                self.doc.undo(); self.assertEqual(self.snapshot()[0], before[0])
        finally: button.deleteLater()

    def test_cycle_rejected_before_prompt_or_mutation(self):
        child = hierarchy.create_definition(self.doc, 'Child')
        link = hierarchy.add_instance(self.owner, child)
        editing.edit((self.top, link)); self.dock.refresh()
        before = self.snapshot()
        with self.assertRaises(ValueError): component_add.add_selected(self.dock, [self.owner])
        self.assertEqual(self.snapshot(), before)

    def test_all_native_styles_refresh_translucent_copy_without_source_writes(self):
        self.shape.ViewObject.ShapeColor = (.25, .6, .85)
        self.shape.ViewObject.Transparency = 0
        self.doc.recompute()
        before = self.snapshot(); source = self.shape.ViewObject
        original = (source.ShapeColor, source.Transparency, source.DisplayMode)
        task = instance_task.open_task([self.part])
        actions = ['AsIs', 'Points', 'Wireframe', 'HiddenLine', 'NoShading', 'Shaded', 'FlatLines']
        for suffix in actions:
            previous = task.overlay
            action = Gui.getMainWindow().findChild(QtGui.QAction, 'Std_DrawStyle' + suffix)
            self.assertIsNotNone(action); action.trigger(); QtTest.QTest.qWait(120)
            self.assertNotEqual(task.overlay, previous)
            self.assertFalse(task.form.status.error, task.form.status.text())
            view = Gui.activeDocument().activeView()
            view.viewAxonometric(); view.fitAll(); Gui.updateGui()
            view.getViewer().grabFramebuffer().save(str(self.out / (suffix + '.png')))
            materials = self.materials(task.overlay)
            self.assertTrue(materials)
            self.assertTrue(all(float(m.transparency[0]) >= .5 for m in materials))
            self.assertEqual((source.ShapeColor, source.Transparency, source.DisplayMode), original)
            self.assertEqual(self.snapshot(), before)
        source.Transparency = 80; task.refresh()
        self.assertTrue(any(float(m.transparency[0]) >= .79 for m in self.materials(task.overlay)))
        snapshot = self.snapshot()
        task.form.preview.setChecked(False); task.refresh(); self.assertIsNone(task.overlay)
        task.form.preview.setChecked(True); task.refresh(); self.assertIsNotNone(task.overlay)
        task.reject(); self.assertEqual(self.snapshot(), snapshot)
        self.assertEqual(source.Transparency, 80)
        Gui.getMainWindow().findChild(QtGui.QAction, 'Std_DrawStyleAsIs').trigger()

    def materials(self, node):
        search = coin.SoSearchAction(); search.setType(coin.SoMaterial.getClassTypeId())
        search.setInterest(coin.SoSearchAction.ALL); search.setSearchingAll(True); search.apply(node)
        return [path.getTail() for path in search.getPaths() if str(path.getTail().getName()) == 'ShapeMaterial']

    def test_preview_matches_committed_native_link_with_rotated_frames(self):
        self.part.Placement = App.Placement(App.Vector(3, 4, 5), App.Rotation(App.Vector(0, 0, 1), 35))
        self.top.LinkPlacement = App.Placement(App.Vector(20, 30, 40), App.Rotation(App.Vector(1, 0, 0), 25))
        self.part.Origin.Visibility = False
        self.doc.recompute()
        task = instance_task.open_task([self.part])
        task.form.positions['quantity'][0].setProperty('rawValue', 12)
        task.refresh(); frame = task.frame()
        def bounds(node):
            action = coin.SoGetBoundingBoxAction(coin.SbViewportRegion(800, 600)); action.apply(node)
            box = action.getBoundingBox()
            return tuple(box.getMin().getValue()) + tuple(box.getMax().getValue())
        before = bounds(task.overlay)
        self.assertTrue(task.accept()); self.doc.recompute()
        graph = coin.SoSeparator(); transform = coin.SoTransform()
        transform.translation.setValue(*tuple(frame.Base)); transform.rotation.setValue(*frame.Rotation.Q)
        graph.addChild(transform); graph.addChild(task.created[0].ViewObject.RootNode)
        for preview, committed in zip(before, bounds(graph)):
            self.assertAlmostEqual(preview, committed, places=4)

    def test_parts_multiselection_creates_one_batch_and_undo(self):
        another = hierarchy.create_definition(self.doc, 'Second source')
        before = self.snapshot()
        self.dock.refresh()
        rows = [i.data(0, panel._ROLE) for i in self.dock._maps[0].values()
                if i.data(0, panel._ROLE).kind == 'model'
                and i.data(0, panel._ROLE).ref in (panel.identity(self.part), panel.identity(another))]
        task = self.dock.add_component_rows(rows)
        self.assertTrue(task.accept())
        self.assertEqual({link.LinkedObject for link in task.created}, {self.part, another})
        self.assertEqual(self.doc.UndoCount, before[1] + 1)
        self.doc.undo(); self.assertEqual(self.snapshot()[0], before[0])
