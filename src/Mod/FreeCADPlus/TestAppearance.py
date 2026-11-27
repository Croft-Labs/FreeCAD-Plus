# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native component appearance, selection, transactions and persistence."""
import os
import unittest
from pathlib import Path
import FreeCAD as App, FreeCADGui as Gui, Part, Mesh
from PySide6 import QtCore, QtGui, QtTest, QtWidgets
from freecad_plus import document, hierarchy, editing, panel, appearance, appearance_task, external


def settle():Gui.updateGui();QtTest.QTest.qWait(100)


def colors(obj):
    return [(tuple(round(c,5) for c in m.DiffuseColor[:3]),round(m.Transparency,5)) for m in appearance.materials(obj)]


class TestAppearance(unittest.TestCase):
    def setUp(self):
        self.doc=document.new_document('AppearanceTest');self.owner=document.validate(self.doc).Definitions[0]
        self.owner.Label='Enclosure'
        self.box=self.owner.newObject('Part::Box','Housing');self.box.Length=10
        self.lid=self.owner.newObject('Part::Box','Lid');self.lid.Placement.Base.z=12
        self.doc.recompute();settle()
        panel.show_panel();panel._panel.refresh();settle()

    def tearDown(self):
        if appearance_task._active:appearance_task._active.reject()
        for name in list(App.listDocuments()):App.closeDocument(name)
        settle()

    def test_whole_and_faces_preserve_other_material_fields_and_children(self):
        child=hierarchy.create_definition(self.doc,'Child');obj=child.newObject('Part::Box','ChildBox');hierarchy.add_child(self.owner,child)
        mats=[App.Material(DiffuseColor=(.2,.3,.4),Shininess=.7,AmbientColor=(.1,.2,.3)) for _ in range(6)]
        self.box.ViewObject.ShapeAppearance=mats;before=colors(obj)
        appearance.apply(self.owner,[(self.box,None),(self.lid,None)],(.9,.2,.1),50)
        self.assertEqual(colors(self.box),[((.9,.2,.1),.5)]*6)
        self.assertEqual(colors(obj),before)
        self.assertAlmostEqual(self.box.ViewObject.ShapeAppearance[2].Shininess,.7,places=5)
        appearance.apply(self.owner,[(self.box,2),(self.box,5)],(.1,.8,.2),75)
        values=colors(self.box);self.assertEqual(values[1],((.1,.8,.2),.75));self.assertEqual(values[4],values[1])
        self.assertEqual(values[0],((.9,.2,.1),.5))

    def test_transparency_only_preserves_face_colors(self):
        appearance.apply(self.owner,[(self.box,1)],(.1,.8,.2))
        before=[v[0] for v in colors(self.box)]
        appearance.apply(self.owner,[(self.box,None)],transparency=35)
        self.assertEqual([v[0] for v in colors(self.box)],before)
        self.assertTrue(all(v[1]==.35 for v in colors(self.box)))

    def test_undo_redo_and_geometry_identity(self):
        before=colors(self.box);identity=self.box.ID;shape=self.box.Shape;undo=self.doc.UndoCount
        appearance.apply(self.owner,[(self.box,3)],(.8,.1,.2),60)
        after=colors(self.box);self.assertEqual(self.doc.UndoCount,undo+1)
        self.doc.undo();self.assertEqual(colors(self.box),before)
        self.doc.redo();self.assertEqual(colors(self.box),after)
        self.assertEqual(self.box.ID,identity);self.assertTrue(shape.isSame(self.box.Shape))

    def test_mesh_body_tip_and_rejected_child(self):
        mesh=self.owner.newObject('Mesh::Feature','Mesh')
        mesh.Mesh=Mesh.Mesh([((0,0,0),(1,0,0),(0,1,0))])
        body=self.owner.newObject('PartDesign::Body','Body')
        old=body.newObject('PartDesign::Feature','Old');old.Shape=Part.makeBox(1,1,1)
        tip=body.newObject('PartDesign::Feature','Tip');tip.Shape=Part.makeBox(2,2,2);body.Tip=tip
        self.doc.recompute();before=colors(old)
        self.assertNotIn(old,appearance.results(self.owner));self.assertIn(tip,appearance.results(self.owner))
        appearance.apply(self.owner,[(mesh,None),(tip,None)],(.2,.4,.8),20)
        self.assertEqual(colors(mesh)[0],((.2,.4,.8),.2));self.assertEqual(colors(old),before)
        self.assertEqual(appearance.resolve_pick(self.owner,body,'Face1'),(tip,1))
        with self.assertRaises(ValueError):appearance.apply(self.owner,[(mesh,1)],(.2,.1,.4))

    def test_native_task_modes_and_slider(self):
        t=appearance_task.open_task(self.owner,((panel.identity(self.box),''),(panel.identity(self.lid),'')));f=t.form;settle()
        QtTest.QTest.mouseClick(f.face,QtCore.Qt.LeftButton);self.assertEqual(len(f.targets),12)
        f.targets=[(panel.identity(self.box),'Face1'),(panel.identity(self.box),'Face3'),(panel.identity(self.lid),'Face2')]
        QtTest.QTest.mouseClick(f.body,QtCore.Qt.LeftButton);self.assertEqual(len(f.targets),2)
        f.slider.setValue(37);self.assertEqual(f.value.value(),37)
        f.value.setValue(64);self.assertEqual(f.slider.value(),64)
        self.assertTrue(t.alpha_changed)

    def test_apply_cancel_done_and_mixed_preservation(self):
        appearance.apply(self.owner,[(self.box,1)],(.1,.8,.2),25)
        t=appearance_task.open_task(self.owner,((panel.identity(self.box),''),));f=t.form;settle()
        self.assertIsNone(f.color_value);self.assertEqual(f.value.value(),-1)
        original=colors(self.box);undo=self.doc.UndoCount
        self.assertTrue(t.apply());self.assertEqual(self.doc.UndoCount,undo)
        self.assertFalse(f.targets);self.assertEqual(f.mode,'body');self.assertEqual(f.value.value(),0)
        t.pick(self.box);t.pick(self.lid)
        f.value.setValue(40);self.assertTrue(t.apply());self.assertIs(appearance_task._active,t)
        self.assertEqual([c for c,a in colors(self.box)],[c for c,a in original])
        applied=colors(self.box);f.value.setValue(80);t.reject();self.assertEqual(colors(self.box),applied)
        t=appearance_task.open_task(self.owner,((panel.identity(self.box),''),));t.form.value.setValue(20);self.assertTrue(t.accept())
        self.assertIsNone(appearance_task._active);self.assertTrue(all(a==.2 for c,a in colors(self.box)))

    def test_occurrence_face_picks_and_toggle(self):
        root=document.validate(self.doc);link=root.Group[0]
        sub=link.Name+'.'+self.box.Name+'.Face2'
        initial=((panel.identity(root),sub),)
        t=appearance_task.open_task(self.owner,initial)
        self.assertEqual(t.form.mode,'face');self.assertEqual(t.form.targets,[(panel.identity(self.box),'Face2')])
        t.pick(root,sub);self.assertEqual(len(t.form.targets),1)
        t.pick(root,sub,True);self.assertFalse(t.form.targets)
        t.pick(root,sub,True);self.assertFalse(t.form.targets)
        t.pick(root,sub);self.assertEqual(len(t.form.targets),1)
        child=hierarchy.create_definition(self.doc,'Child');other=child.newObject('Part::Box','Other')
        self.doc.recompute()
        with self.assertRaises(ValueError):t.pick(other,'Face1')

    def test_cancel_and_stale_geometry(self):
        before=colors(self.box);undo=self.doc.UndoCount
        t=appearance_task.open_task(self.owner,());t.form.value.setValue(70);t.reject()
        self.assertEqual(colors(self.box),before);self.assertEqual(self.doc.UndoCount,undo)
        t=appearance_task.open_task(self.owner,((panel.identity(self.box),'Face1'),));self.box.Length=30;self.doc.recompute()
        t.form.value.setValue(70);self.assertFalse(t.apply());self.assertTrue(t.form.status.error)
        self.assertEqual(colors(self.box),before)

    def test_parts_context_menu_retains_selected_faces(self):
        w=panel._panel;w.tabs.setCurrentIndex(0);w.refresh();settle()
        tree=w.trees[0]
        item=next(i for i in w._maps[0].values() if i.data(0,panel._ROLE).ref==panel.identity(self.owner))
        Gui.Selection.clearSelection();Gui.Selection.addSelection(self.box,'Face2');settle()
        point=tree.visualItemRect(item).center()
        # The right press precedes Qt's catalog-row selection change.
        press=QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress,QtCore.QPointF(point),QtCore.Qt.RightButton,QtCore.Qt.RightButton,QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(tree.viewport(),press)
        states=[]
        def choose():
            menu=QtWidgets.QApplication.activePopupWidget()
            states.extend('---' if a.isSeparator() else a.text() for a in menu.actions())
            action=next(a for a in menu.actions() if a.text()=='Appearance\u2026');action.trigger();menu.close()
        QtCore.QTimer.singleShot(100,choose);w._menu(tree,point);settle()
        self.assertEqual(states,['---','Edit within assembly','Edit in isolation','Make active assembly','Add to active component\u2026','Open in new window','Rename','---','Appearance\u2026','Part Type','Visibility','---','Create new part file\u2026','Import\u2026','Export\u2026','---'])
        t=appearance_task._active;self.assertIsNotNone(t);self.assertEqual(t.form.mode,'face')
        self.assertEqual(t.form.targets,[(panel.identity(self.box),'Face2')])
        Gui.Selection.clearSelection();Gui.Selection.addSelection(self.lid,'Face3');settle()
        self.assertIn((panel.identity(self.lid),'Face3'),t.form.targets)

    def test_native_save_and_reopen(self):
        appearance.apply(self.owner,[(self.box,2)],(.7,.2,.9),55);expected=colors(self.box)
        path=Path(os.environ['PLUS_TEST_DIR'])/'appearance.cadprt'
        document.save_document(self.doc,path);App.closeDocument(self.doc.Name);settle()
        self.doc=document.open_document(path)
        restored=colors(self.doc.getObject('Housing'))
        for (color,alpha),(wanted,wanted_alpha) in zip(restored,expected):
            for actual,value in zip(color,wanted):self.assertAlmostEqual(actual,value,delta=1/255)
            self.assertAlmostEqual(alpha,wanted_alpha,places=4)

    def test_external_source_owns_undo_and_persistence(self):
        path=Path(os.environ['PLUS_TEST_DIR'])/'source.cadprt';document.save_document(self.doc,path)
        source=self.doc;owner=self.owner;box=self.box
        host=document.new_document('Host');document.validate(host).Definitions[0].Label='Host component'
        document.save_document(host,Path(os.environ['PLUS_TEST_DIR'])/'host.cadprt')
        external.import_file(host,source);hierarchy.add_child(document.validate(host).Definitions[0],owner);settle()
        host_undo=host.UndoCount;source_undo=source.UndoCount
        t=appearance_task.open_task(owner,((panel.identity(box),''),));t.form.value.setValue(45);self.assertTrue(t.apply())
        self.assertEqual(host.UndoCount,host_undo+1);self.assertEqual(source.UndoCount,source_undo+1)
        self.assertTrue(all(a==.45 for c,a in colors(box)));t.reject()
        document.save_document(source);Gui.runCommand('Std_Undo');settle()
        self.assertFalse(all(a==.45 for c,a in colors(box)))
