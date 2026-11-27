# SPDX-License-Identifier: LGPL-2.1-or-later
"""History entry points, explicit targets and face-only native highlights."""
import os
import unittest
from pathlib import Path
from unittest.mock import patch
import FreeCAD as App, FreeCADGui as Gui, Part
from PySide6 import QtCore, QtGui, QtTest, QtWidgets
from freecad_plus import document, hierarchy, editing, panel, appearance, appearance_task
from TestAppearance import TestAppearance, colors, settle


class TestHistoryAppearance(unittest.TestCase):
    def setUp(self):
        TestAppearance.setUp(self)
        body=self.owner.newObject('PartDesign::Body','Body')
        self.old=body.newObject('PartDesign::Feature','Pad');self.old.Shape=Part.makeBox(10,10,10)
        self.tip=body.newObject('PartDesign::Feature','Fillet');self.tip.Shape=Part.makeBox(12,12,12)
        body.Tip=self.tip;self.old.Visibility=False
        self.doc.recompute();editing.edit((document.validate(self.doc).Group[0],))
        panel._panel.refresh();panel._panel.tabs.setCurrentIndex(2);settle()

    tearDown=TestAppearance.tearDown

    def menu(self, obj, initial=()):
        w=panel._panel;w.refresh();w.tabs.setCurrentIndex(2);settle()
        tree=w.trees[2];tree.expandAll()
        item=next(i for i in w._maps[2].values() if i.data(0,panel._ROLE).ref==panel.identity(obj))
        Gui.Selection.clearSelection()
        for target,sub in initial:Gui.Selection.addSelection(target,sub)
        settle();point=tree.visualItemRect(item).center();point.setX(min(point.x(),tree.columnWidth(0)-20))
        press=QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress,QtCore.QPointF(point),QtCore.Qt.RightButton,QtCore.Qt.RightButton,QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(tree.viewport(),press)
        actions=[]
        def choose():
            menu=QtWidgets.QApplication.activePopupWidget()
            if menu is None:return
            actions.extend('---' if a.isSeparator() else a.text() for a in menu.actions())
            action=next((a for a in menu.actions() if a.text()=='Appearance\u2026'),None)
            if action:action.trigger()
            menu.close()
        QtCore.QTimer.singleShot(100,choose);w._menu(tree,point);settle()
        self.assertEqual(w.tabs.currentIndex(),2)
        return appearance_task._active,actions

    def test_part_menu_preserves_faces_and_no_selection(self):
        undo=self.doc.UndoCount;before=colors(self.box)
        task,actions=self.menu(self.owner,[(self.box,'Face2'),(self.lid,'Face3')])
        self.assertEqual(actions,['Rename','---','Appearance\u2026'])
        self.assertEqual(task.form.targets,[(panel.identity(self.box),'Face2'),(panel.identity(self.lid),'Face3')])
        self.assertEqual(task.form.mode,'face');task.reject()
        task,_=self.menu(self.owner)
        self.assertFalse(task.form.targets);self.assertFalse(task.form.apply.isEnabled());task.reject()
        self.assertEqual(self.doc.UndoCount,undo);self.assertEqual(colors(self.box),before)

    def test_explicit_body_empty_edge_and_hover_inputs(self):
        Gui.Selection.clearSelection();Gui.Selection.setPreselection(self.box,'Face1',tp=0)
        task=appearance_task.open_task(self.owner)
        self.assertFalse(task.form.targets);task.reject();Gui.Selection.clearPreselection()
        task=appearance_task.open_task(self.owner,((panel.identity(self.box),'Edge1'),))
        self.assertFalse(task.form.targets);task.reject()
        task,_=self.menu(self.owner,[(self.box,'')])
        self.assertEqual(task.form.targets,[(panel.identity(self.box),None)])
        task.form.face.setChecked(True);self.assertEqual(len(task.form.targets),6)
        task.form.body.setChecked(True);self.assertEqual(task.form.targets,[(panel.identity(self.box),None)])

    def test_historical_feature_apply_reset_cancel_undo(self):
        before=colors(self.old);tip=colors(self.tip);box=colors(self.box)
        state=[(o.Name,o.ID,str(getattr(o,'Placement','')),getattr(o,'Visibility',None)) for o in self.doc.Objects]
        undo=self.doc.UndoCount
        task,actions=self.menu(self.old,[(self.box,'Face2')])
        self.assertEqual(actions,['Appearance\u2026'])
        self.assertEqual(task.form.targets,[(panel.identity(self.old),None)])
        task.form.color_value=QtGui.QColor('#f04020');task.form.color_changed=True;task.form.value.setValue(40)
        self.assertTrue(task.apply());self.assertEqual(self.doc.UndoCount,undo+1)
        after=colors(self.old);self.assertNotEqual(before,after)
        self.assertTrue(all(alpha==.4 for _,alpha in after))
        self.assertFalse(task.form.targets);self.assertEqual(task.form.value.value(),0)
        task.pick(self.old);task.form.value.setValue(75);task.reject()
        self.assertEqual(colors(self.old),after);self.assertEqual(colors(self.tip),tip);self.assertEqual(colors(self.box),box)
        self.assertEqual(state,[(o.Name,o.ID,str(getattr(o,'Placement','')),getattr(o,'Visibility',None)) for o in self.doc.Objects])
        self.doc.undo();self.assertEqual(colors(self.old),before)
        self.doc.redo();self.assertEqual(colors(self.old),after)

    def test_history_face_apply_and_saved_material(self):
        before=colors(self.old)
        task,_=self.menu(self.old);task.form.face.setChecked(True)
        task.form.targets=[(panel.identity(self.old),'Face2')];task.form.refresh_targets();task.load_values()
        task.form.value.setValue(65);self.assertTrue(task.accept())
        expected=colors(self.old);self.assertEqual(expected[1][1],.65)
        self.assertEqual(expected[:1]+expected[2:],before[:1]+before[2:])
        path=Path(os.environ['PLUS_TEST_DIR'])/'history-appearance.cadprt'
        document.save_document(self.doc,path);App.closeDocument(self.doc.Name);settle()
        self.doc=document.open_document(path);restored=colors(self.doc.getObject('Pad'))
        for (c,a),(want,alpha) in zip(restored,expected):
            self.assertAlmostEqual(a,alpha,places=4)
            for channel,value in zip(c,want):self.assertAlmostEqual(channel,value,delta=1/255)

    def test_historical_geometry_stale_and_child_rejection(self):
        task,_=self.menu(self.old);before=colors(self.old);undo=self.doc.UndoCount
        self.old.Shape=Part.makeBox(15,15,15);self.doc.recompute();task.form.value.setValue(65)
        self.assertFalse(task.apply());self.assertEqual(colors(self.old),before);self.assertEqual(self.doc.UndoCount,undo)
        task.reject()
        child=hierarchy.create_definition(self.doc,'Child');other=child.newObject('Part::Box','Other')
        hierarchy.add_child(self.owner,child);self.doc.recompute()
        with self.assertRaises(ValueError):appearance.apply(self.owner,[(other,None)],transparency=80)
        with self.assertRaises(ValueError):appearance.resolve_pick(self.owner,other,'Face1')

    def test_non_geometry_history_has_no_appearance(self):
        sketch=self.owner.newObject('Sketcher::SketchObject','Sketch');self.doc.recompute()
        task,actions=self.menu(sketch)
        self.assertIsNone(task);self.assertFalse(actions)

    def test_imported_history_feature_edits_source_with_linked_undo(self):
        from freecad_plus import external
        document.save_document(self.doc,Path(os.environ['PLUS_TEST_DIR'])/'history-source.cadprt')
        source=self.doc
        host=document.new_document('HistoryHost');host_owner=document.validate(host).Definitions[0]
        host_owner.Label='Host component'
        document.save_document(host,Path(os.environ['PLUS_TEST_DIR'])/'history-host.cadprt')
        external.import_file(host,source);link=hierarchy.add_child(host_owner,self.owner)
        editing.edit((document.validate(host).Group[0],link));settle()
        before=colors(self.old);tip=colors(self.tip);host_undo=host.UndoCount;source_undo=source.UndoCount
        task,_=self.menu(self.old);self.assertEqual(task.form.targets,[(panel.identity(self.old),None)])
        task.form.value.setValue(55);self.assertTrue(task.apply());task.reject()
        self.assertTrue(all(a==.55 for _,a in colors(self.old)));self.assertEqual(colors(self.tip),tip)
        self.assertEqual(host.UndoCount,host_undo+1);self.assertEqual(source.UndoCount,source_undo+1)
        Gui.runCommand('Std_Undo');settle();self.assertEqual(colors(self.old),before)

    def test_highlight_extracts_only_selected_and_hovered_face(self):
        from freecad_plus import appearance_highlight
        root=document.validate(self.doc);sub=hierarchy.subname((root.Group[0],self.box))+'Face6'
        before=colors(self.box);undo=self.doc.UndoCount
        task=appearance_task.open_task(self.owner,((panel.identity(root),sub),))
        prefs=App.ParamGet('User parameter:BaseApp/Preferences/View')
        saved=(prefs.GetBool('EnableSelection',True),prefs.GetBool('EnablePreselection',True))
        prefs.SetBool('EnableSelection',True);prefs.SetBool('EnablePreselection',True)
        original=Part.getShape;shapes=[]
        def shape(*args,**kwargs):
            value=original(*args,**kwargs);shapes.append(value);return value
        try:
            with patch.object(appearance_highlight.Part,'getShape',shape):
                task.refresh_highlights();task.setPreselection(self.doc.Name,self.box.Name,'Face2');settle()
            self.assertTrue(shapes)
            self.assertTrue(all(s.ShapeType=='Face' and len(s.Faces)==1 for s in shapes))
            self.assertEqual(colors(self.box),before);self.assertEqual(self.doc.UndoCount,undo)
            task.form.clear_targets();task.removePreselection();settle();self.assertIsNone(task.highlights.node)
        finally:
            prefs.SetBool('EnableSelection',saved[0]);prefs.SetBool('EnablePreselection',saved[1])

    def test_native_history_face_screenshot(self):
        self.lid.Visibility=False;self.tip.Visibility=False
        Gui.activeDocument().activeView().setAnimationEnabled(False)
        Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll();settle()
        task,_=self.menu(self.owner,[(self.box,'Face6')]);settle()
        out=Path(os.environ['PLUS_TEST_DIR'])
        Gui.activeDocument().activeView().saveImage(str(out/'history-face.png'),800,650,'Current')
        Gui.getMainWindow().findChild(QtWidgets.QDockWidget,'Tasks').grab().save(str(out/'history-face-task.png'))
        task.reject();task,_=self.menu(self.old)
        Gui.getMainWindow().findChild(QtWidgets.QDockWidget,'Tasks').grab().save(str(out/'history-feature-task.png'))
        self.assertEqual(task.form.targets,[(panel.identity(self.old),None)])
