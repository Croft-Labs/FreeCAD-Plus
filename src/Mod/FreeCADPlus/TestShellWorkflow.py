# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Shell collector, atomic persistence and shared dress-up interaction."""
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtGui, QtTest, QtWidgets
from freecad_plus import document, editing, extrude_task, shell_task
from TestFeatureCenteredModeling import TestFeatureCenteredModeling
from TestComponentModeling import messages


class TestShellWorkflow(unittest.TestCase):
    setUp = TestFeatureCenteredModeling.setUp
    snapshot = TestFeatureCenteredModeling.snapshot

    def tearDown(self):
        if extrude_task._active:extrude_task._active.reject()
        TestFeatureCenteredModeling.tearDown(self)

    def solid(self):
        body = self.owner.newObject('PartDesign::Body', 'Body')
        box = body.newObject('PartDesign::AdditiveBox', 'Box')
        box.Length = 20; box.Width = 12; box.Height = 10
        self.doc.recompute()
        return box

    def open(self, obj=None, sub=''):
        Gui.activateWorkbench('PartDesignWorkbench')
        Gui.Selection.clearSelection()
        if obj:Gui.Selection.addSelection(obj, sub)
        with messages() as errors:Gui.runCommand('PartDesign_Thickness')
        self.assertFalse(errors, errors)
        QtTest.QTest.qWait(100)
        task = extrude_task._active
        self.assertIsInstance(task, shell_task.ShellTask)
        self.assertFalse(self.doc.HasPendingTransaction)
        self.assertIsNone(Gui.activeDocument().getInEdit())
        return task

    def pick(self, task, obj, sub):
        QtTest.QTest.mouseClick(task.faces.viewport(), QtCore.Qt.LeftButton)
        Gui.Selection.addSelection(obj, sub)
        QtTest.QTest.qWait(50)

    def test_empty_curve_and_sheet_entry_are_recoverable(self):
        solid = self.solid()
        sheet = self.owner.newObject('PartDesign::Feature', 'Sheet')
        sheet.Shape = Part.makePlane(10, 8)
        for obj, sub in ((None, ''), (solid, 'Edge1'), (sheet, 'Face1')):
            before = self.snapshot()
            task = self.open(obj, sub)
            self.assertFalse(task.refs); self.assertFalse(task.valid)
            if obj:self.assertTrue(task.status.error)
            self.pick(task, solid, 'Face6')
            self.assertTrue(task.valid, task.status.text())
            task.reject(); self.assertEqual(before, self.snapshot())

    def test_list_delete_remove_clear_and_parameter_focus(self):
        solid = self.solid(); task = self.open()
        self.pick(task, solid, 'Face6'); self.pick(task, solid, 'Face6')
        self.assertEqual(len(task.refs), 1)
        task.thickness.setFocus(); QtTest.QTest.qWait(20)
        self.assertIsNone(task.pick)
        Gui.Selection.addSelection(solid, 'Face1'); self.assertEqual(len(task.refs), 1)
        Gui.Selection.clearSelection()
        self.pick(task, solid, 'Face1'); self.assertEqual(len(task.refs), 2)
        task.faces.setCurrentRow(1)
        QtTest.QTest.keyClick(task.faces, QtCore.Qt.Key_Delete)
        self.assertEqual([sub for _, sub in task.refs], ['Face6'])
        task.faces.setCurrentRow(0); task.remove_button.click(); self.assertFalse(task.refs)
        self.pick(task, solid, 'Face6'); task.clear_button.click()
        self.assertFalse(task.refs); self.assertFalse(task.links); self.assertFalse(task.valid)
        self.assertIsNotNone(self.doc.getObject(solid.Name))

    def test_implicit_owner_rejects_mixed_solids_until_cleared(self):
        first = self.solid(); second = self.solid()
        task = self.open(first, 'Face6')
        self.pick(task, second, 'Face6')
        self.assertEqual(task.refs, [(first, 'Face6')])
        self.assertIn('Clear faces', task.status.text())
        task.clear_button.click(); self.pick(task, second, 'Face6')
        self.assertEqual(task.refs, [(second, 'Face6')]); self.assertTrue(task.valid)

    def test_native_accept_edit_cancel_undo_and_save(self):
        first = self.solid(); second = self.solid()
        other_body = second.getParentGeoFeatureGroup()
        view = Gui.activeDocument().activeView(); view.setActiveObject('pdbody', other_body)
        task = self.open(first, 'Face6')
        expected = task.result_shape.Volume
        self.assertTrue(task.accept())
        feature = task.result; identity = feature.ID; name = feature.Name
        self.assertEqual(feature.TypeId, 'PartDesign::Thickness')
        self.assertAlmostEqual(feature.Shape.Volume, expected, places=5)
        self.assertEqual(feature.Base, (first, ['Face6']))
        self.assertEqual(other_body.Tip, second)
        self.assertEqual(view.getActiveObject('pdbody'), other_body)
        self.doc.undo(); self.assertIsNone(self.doc.getObject(name))
        self.doc.redo(); feature = self.doc.getObject(name); self.assertEqual(feature.ID, identity)
        before = self.snapshot()
        task = editing.edit_feature(self.doc, feature)
        task.thickness.setValue(2); task.commit_value(); self.assertTrue(task.valid)
        task.reject(); self.assertEqual(before, self.snapshot()); self.assertAlmostEqual(feature.Value.Value, 1)
        task = editing.edit_feature(self.doc, feature)
        task.thickness.setValue(2); task.commit_value(); self.assertTrue(task.accept())
        self.assertEqual(feature.ID, identity); self.assertAlmostEqual(feature.Value.Value, 2)
        document.save_document(self.doc, self.output/'Shell.cadprt')

    def test_preview_controls_and_blur_commit(self):
        solid = self.solid(); task = self.open(solid, 'Face6')
        revisions = task.revisions
        task.thickness.setFocus(); task.thickness.selectAll(); QtTest.QTest.keyClicks(task.thickness, '2')
        self.assertEqual(task.revisions, revisions)
        task.faces.setFocus(); QtTest.QTest.qWait(20)
        self.assertEqual(task.value, 2); self.assertGreater(task.revisions, revisions)
        task.final.click(); self.assertTrue(task.showing_result)
        task.visible.click(); self.assertFalse(task.showing_result)
        task.visible.click(); self.assertTrue(task.valid)
        Gui.getMainWindow().findChild(QtWidgets.QDockWidget, 'Tasks').grab().save(str(self.output/'shell.png'))

    def test_later_input_rejected_when_editing(self):
        first = self.solid(); task = self.open(first, 'Face6'); self.assertTrue(task.accept())
        feature = task.result; later = self.solid()
        task = editing.edit_feature(self.doc, feature); task.clear_faces()
        self.pick(task, later, 'Face6')
        self.assertFalse(task.refs); self.assertIn('before', task.status.text().lower())

    def test_native_dressup_list_focus_and_duplicate_add(self):
        from TestComponentModeling import accept_task
        solid = self.solid(); other = self.solid()
        Gui.activeDocument().activeView().setActiveObject('pdbody', other.getParentGeoFeatureGroup())
        Gui.activateWorkbench('PartDesignWorkbench')
        for command in ('PartDesign_Fillet', 'PartDesign_Chamfer', 'PartDesign_Draft'):
            Gui.Selection.clearSelection(); Gui.Selection.addSelection(solid.getParentGeoFeatureGroup())
            with messages() as errors:Gui.runCommand(command)
            self.assertFalse(errors, errors); QtTest.QTest.qWait(100)
            feature = Gui.activeDocument().getInEdit().Object
            self.assertEqual(feature.getParentGeoFeatureGroup(), solid.getParentGeoFeatureGroup())
            main = Gui.getMainWindow()
            refs = next(w for w in main.findChildren(QtWidgets.QListWidget, 'listWidgetReferences') if w.isVisible())
            toggle = refs.parentWidget().findChild(QtWidgets.QToolButton, 'buttonRefSel')
            self.assertFalse(toggle.isVisible())
            clear = refs.parentWidget().findChild(QtWidgets.QPushButton, 'clearReferences')
            clear.click(); self.assertFalse(feature.Base[1])
            QtTest.QTest.mouseClick(refs.viewport(), QtCore.Qt.LeftButton)
            sub = 'Face1' if command.endswith('Draft') else 'Edge1'
            Gui.Selection.addSelection(solid, sub); Gui.Selection.addSelection(solid, sub)
            self.assertEqual(feature.Base[1], [sub])
            refs.setCurrentRow(0); QtTest.QTest.keyClick(refs, QtCore.Qt.Key_Delete)
            self.assertFalse(feature.Base[1])
            all_edges = refs.parentWidget().findChild(QtWidgets.QCheckBox, 'checkBoxUseAllEdges')
            if all_edges:
                all_edges.setChecked(True); self.assertTrue(feature.UseAllEdges)
                clear.click(); self.assertFalse(feature.UseAllEdges); self.assertFalse(feature.Base[1])
            box = next(w for w in main.findChildren(QtWidgets.QDialogButtonBox) if w.isVisible() and w.button(QtWidgets.QDialogButtonBox.Cancel))
            box.button(QtWidgets.QDialogButtonBox.Cancel).click(); QtTest.QTest.qWait(50)

    def test_actual_viewport_face_pick_after_clear(self):
        solid = self.solid(); task = self.open()
        view = Gui.activeDocument().activeView()
        view.setCameraType('Orthographic'); view.setAnimationEnabled(False)
        view.viewTop(); view.fitAll(); view.getCameraNode().height = 30
        QtTest.QTest.qWait(100)
        widget = view.graphicsView().viewport(); ratio = widget.devicePixelRatioF()
        screen = view.getPointOnScreen(App.Vector(10,6,10))
        position = QtCore.QPoint(round(screen[0]/ratio), widget.height()-1-round(screen[1]/ratio))
        for _ in range(2):
            task.clear_button.click(); QtTest.QTest.mouseClick(task.faces.viewport(), QtCore.Qt.LeftButton)
            event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(position),
                QtCore.QPointF(widget.mapToGlobal(position)), QtCore.Qt.NoButton,
                QtCore.Qt.NoButton, QtCore.Qt.NoModifier)
            QtWidgets.QApplication.sendEvent(widget,event)
            QtTest.QTest.mouseClick(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, position)
            QtTest.QTest.qWait(100)
            self.assertEqual(task.refs, [(solid,'Face6')]); self.assertTrue(task.valid)
        Gui.getMainWindow().findChild(QtWidgets.QDockWidget,'Tasks').grab().save(str(self.output/'shell-picked.png'))

    def test_history_restore_eyes_and_scrollable_list(self):
        from freecad_plus import panel
        body = self.owner.newObject('PartDesign::Body', 'Body')
        solid = body.newObject('PartDesign::Feature', 'HexPrism')
        points = [App.Vector(x,y,0) for x,y in ((0,0),(20,0),(25,10),(20,20),(0,20),(-5,10),(0,0))]
        solid.Shape = Part.Face(Part.makePolygon(points)).extrude(App.Vector(0,0,10))
        self.doc.recompute(); panel.show_panel(); widget = panel._panel
        widget.tabs.setCurrentIndex(1)
        task = self.open(solid, 'Face6'); self.assertEqual(widget.tabs.currentIndex(), 2)
        route = document.owned_path(self.owner, solid)
        task.presentation.toggle_many([route], False, solid.Label)
        task.refresh_visibility(); self.assertFalse(solid.Visibility)
        self.assertIsNotNone(task.target_overlay)
        for index in range(1,9):self.pick(task, solid, 'Face'+str(index))
        self.assertEqual(task.faces.count(), 8)
        self.assertGreater(task.faces.verticalScrollBar().maximum(), 0)
        task.reject(); self.assertEqual(widget.tabs.currentIndex(), 1)
        self.assertFalse(solid.Visibility)
