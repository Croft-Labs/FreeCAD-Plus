# SPDX-License-Identifier: LGPL-2.1-or-later
"""Integrated acceptance for approved component, collector and task changes."""
import os
from pathlib import Path
import unittest
import FreeCAD as App, FreeCADGui as Gui, Part
from PySide6 import QtCore, QtGui, QtWidgets, QtTest
from freecad_plus import document, hierarchy, panel, editing, isolation, assembly
from freecad_plus import appearance, appearance_task, selection_toolbar, selection_scope, surface_selection, curve_selection


def settle():QtTest.QTest.qWait(120)


class TestPendingWorkflows(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:self.skipTest('Requires isolated native GUI profile')
        from freecad_plus import category_selection
        self.saved_intents=(curve_selection.intent(),surface_selection.intent())
        self.saved_categories={key:category_selection.preferences().GetBool(key,True) for key in category_selection.CATEGORIES}
        self.doc=document.new_document('PendingWorkflows');self.root=document.validate(self.doc)
        self.owner=self.root.Definitions[0];self.top=self.root.Group[0]
        self.box=self.owner.newObject('Part::Box','Housing');self.doc.recompute()
        self.view=Gui.activeDocument().activeView()
        self.dock=panel.show_panel();self.dock.refresh();settle()

    def tearDown(self):
        if appearance_task._active:appearance_task._active.reject()
        from freecad_plus import category_selection
        selection_toolbar.preferences().SetString('CurveIntent',self.saved_intents[0])
        selection_toolbar.preferences().SetString('SurfaceIntent',self.saved_intents[1])
        for key,value in self.saved_categories.items():category_selection.preferences().SetBool(key,value)
        for name in list(App.listDocuments()):App.closeDocument(name)
        settle()

    def test_single_part_default_stale_cache_and_saved_manual_choice(self):
        state=self.dock._state(self.dock._binding);state['assembly']=None;state['assembly_path']=()
        undo=self.doc.UndoCount;context=editing.context_path(self.doc);tab=self.dock.tabs.currentIndex()
        self.assertEqual(self.dock._assembly_context(self.dock._binding)[0],self.owner)
        self.assertEqual((self.doc.UndoCount,editing.context_path(self.doc),self.dock.tabs.currentIndex()),(undo,context,tab))
        other=hierarchy.create_definition(self.doc,'Other')
        state['assembly']=None
        self.assertIsNone(self.dock._assembly_context(self.dock._binding)[0])
        self.dock.activate_assembly(other)
        self.assertEqual(self.dock._assembly_context(self.dock._binding)[0],other)
        document.save_document(self.doc,Path(os.environ['PLUS_TEST_DIR'])/'single-default.cadprt')
        self.assertEqual(assembly.recalled(self.doc),other)

    def test_exact_edit_modes_preserve_fixed_assembly_tab_expansion_and_undo(self):
        child=hierarchy.create_definition(self.doc,'Child');solid=child.newObject('Part::Box','Solid')
        one=hierarchy.add_instance(self.owner,child);two=hierarchy.add_instance(self.owner,child)
        self.doc.recompute();self.dock.activate_assembly(self.owner,(self.top,));self.dock.tabs.setCurrentIndex(1)
        self.dock.refresh();settle()
        row=next(i.data(0,panel._ROLE) for i in self.dock._maps[1].values() if i.data(0,panel._ROLE).path==tuple(panel.identity(o) for o in (self.top,two)))
        undo=self.doc.UndoCount;vis=[o.Visibility for o in self.doc.Objects]
        self.dock.edit_row(row);self.assertEqual(editing.context_path(self.doc),(child,(self.top,two)))
        self.assertIsNone(isolation.current(self.view))
        self.dock.edit_row(row,mode='isolation');self.assertEqual(editing.context_path(self.doc),(child,()))
        self.assertEqual(isolation.current(self.view).anchor_definition(),child)
        self.dock.edit_row(row,mode='assembly');self.assertEqual(editing.context_path(self.doc),(child,(self.top,two)))
        self.assertEqual(self.dock.tabs.currentIndex(),1)
        self.assertEqual(self.dock._assembly_context(self.dock._binding)[0],self.owner)
        self.assertEqual((self.doc.UndoCount,[o.Visibility for o in self.doc.Objects]),(undo,vis))

    def test_unused_assembly_child_edits_keep_assembly_preview(self):
        parent=hierarchy.create_definition(self.doc,'UnusedAssembly')
        child=hierarchy.create_definition(self.doc,'Nested');child.newObject('Part::Box','NestedSolid')
        link=hierarchy.add_instance(parent,child,App.Placement(App.Vector(20,5,3),App.Rotation()))
        self.doc.recompute()
        self.dock.activate_assembly(parent);self.dock.refresh();settle()
        row=next(i.data(0,panel._ROLE) for i in self.dock._maps[1].values() if i.data(0,panel._ROLE).path==(panel.identity(link),))
        self.dock.edit_row(row,mode='assembly');session=isolation.current(self.view)
        self.assertEqual(session.anchor_definition(),parent);self.assertEqual(session.definition(),child)
        self.assertEqual(self.view.getActiveObject('PlusEdit',False)[1:],(parent,link.Name+'.'))
        self.assertEqual(editing.context_path(self.doc),(child,()))
        self.assertTrue(editing.world_placement(self.doc).isSame(link.LinkPlacement,1e-8))
        from freecad_plus import geometry
        solid=child.Group[-1]
        self.assertEqual(geometry.require_access(self.doc,parent,link.Name+'.'+solid.Name+'.Face1',active=child),solid)
        self.dock.edit_row(row,mode='isolation');self.assertEqual(isolation.current(self.view).anchor_definition(),child)

    def test_surface_topology_sharp_smooth_and_independent_solids(self):
        cube=Part.makeBox(4,4,4)
        faces=dict(enumerate(cube.Faces,1))
        self.assertEqual(curve_selection._walk(surface_selection.graph(faces),1),list(range(1,7)))
        self.assertEqual(curve_selection._walk(surface_selection.graph(faces,True),1),[1])
        compound=Part.makeCompound([cube,Part.makeBox(4,4,4,App.Vector(4,0,0))])
        self.assertEqual(len(curve_selection._walk(surface_selection.graph(dict(enumerate(compound.Faces,1))),1)),6)
        rounded=cube.makeFillet(.5,cube.Edges)
        graph=surface_selection.graph(dict(enumerate(rounded.Faces,1)),True)
        self.assertGreater(len(curve_selection._walk(graph,1)),1)

    def test_surface_toolbar_pick_expansion_shift_reset_and_materials(self):
        from freecad_plus import ui_modes, toolbars, category_selection
        for category in category_selection.CATEGORIES:category_selection.preferences().SetBool(category,True)
        ui_modes.apply_modes();selection_toolbar.preferences().SetString('CurveIntent','Tangent Curves')
        selection_toolbar.preferences().SetString('SurfaceIntent','Connected Surfaces')
        task=appearance_task.open_task(self.owner,());task.form.face.setChecked(True)
        task.form.clear_targets();settle()
        self.assertEqual(selection_scope.current()[0],'surface')
        button=Gui.getMainWindow().findChild(QtWidgets.QToolButton,'PlusCurveIntent')
        self.assertEqual(button.text(),'Connected Surfaces')
        before=[m.DiffuseColor for m in appearance.materials(self.box)];undo=self.doc.UndoCount
        root=self.root;sub=hierarchy.subname((self.top,self.box))+'Face1'
        controller=curve_selection._controller;controller.active=True
        self.view.setAnimationEnabled(False);self.view.viewTop();self.view.fitAll();settle()
        viewport=self.view.graphicsView().viewport();ratio=viewport.devicePixelRatioF()
        box=self.box.Shape.BoundBox
        screen=self.view.getPointOnScreen(App.Vector((box.XMin+box.XMax)/2,(box.YMin+box.YMax)/2,box.ZMax))
        point=QtCore.QPoint(round(screen[0]/ratio),viewport.height()-1-round(screen[1]/ratio))
        event=QtGui.QMouseEvent(QtCore.QEvent.MouseMove,QtCore.QPointF(point),QtCore.QPointF(viewport.mapToGlobal(point)),
                               QtCore.Qt.NoButton,QtCore.Qt.NoButton,QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(viewport,event);settle()
        QtTest.QTest.mouseClick(viewport,QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,point);settle()
        self.assertEqual(len(task.form.targets),6)
        self.assertIsNotNone(task.highlights.node)
        self.assertEqual([m.DiffuseColor for m in appearance.materials(self.box)],before)
        self.assertEqual(self.doc.UndoCount,undo)
        from freecad_plus.selection_list import pick_intent
        QtTest.QTest.mouseClick(viewport,QtCore.Qt.LeftButton,QtCore.Qt.ShiftModifier,point)
        settle();self.assertFalse(task.form.targets)
        task.pick(root,sub);task.form.value.setValue(40);self.assertTrue(task.apply());settle()
        self.assertFalse(task.form.targets);self.assertEqual(task.form.mode,'body')
        self.assertEqual(task.form.value.value(),0);self.assertIsNone(task.highlights.node)
        self.assertEqual(button.text(),'Tangent Curves');self.assertTrue(task.form.done.isEnabled())
        task.form.done.click();settle();self.assertIsNone(appearance_task._active)
        self.assertEqual(self.doc.UndoCount,undo+1)

    def test_queued_surface_pick_cannot_cross_mode_change(self):
        task=appearance_task.open_task(self.owner,());task.form.face.setChecked(True);task.form.clear_targets()
        selection_toolbar.preferences().SetString('SurfaceIntent','Connected Surfaces')
        controller=curve_selection._controller;controller.active=True;controller.picking=True
        Gui.Selection.addSelection(self.root,hierarchy.subname((self.top,self.box))+'Face1')
        task.form.body.setChecked(True);task.form.face.setChecked(True)
        settle();controller.end_pick();self.assertFalse(task.form.targets)

    def test_native_face_highlights_follow_preferences_and_leave_materials_unchanged(self):
        prefs=App.ParamGet('User parameter:BaseApp/Preferences/View')
        saved=(prefs.GetBool('EnableSelection',True),prefs.GetUnsigned('SelectionColor'),
               prefs.GetBool('EnablePreselection',True),prefs.GetUnsigned('HighlightColor'))
        before=[m.DiffuseColor for m in appearance.materials(self.box)];undo=self.doc.UndoCount
        try:
            prefs.SetBool('EnableSelection',True);prefs.SetBool('EnablePreselection',True)
            prefs.SetUnsigned('SelectionColor',0x3b5bdbff);prefs.SetUnsigned('HighlightColor',0x007a00ff)
            sub=hierarchy.subname((self.top,self.box))+'Face6'
            task=appearance_task.open_task(self.owner,((panel.identity(self.root),sub),))
            self.view.setAnimationEnabled(False);self.view.viewAxonometric();self.view.fitAll();settle()
            out=Path(os.environ['PLUS_TEST_DIR'])
            def capture(name,color):
                path=out/name;self.view.saveImage(str(path),600,450,'Current')
                image=QtGui.QImage(str(path))
                count=sum(image.pixelColor(x,y).name()==color for x in range(0,image.width(),3) for y in range(0,image.height(),3))
                self.assertGreater(count,100,name)
            capture('appearance-selected.png','#3b5bdb')
            Gui.Selection.setPreselection(self.root,sub,tp=0);settle()
            self.assertIsNotNone(task.hover)
            capture('appearance-preselected.png','#007a00')
            Gui.getMainWindow().findChild(QtWidgets.QDockWidget,'Tasks').grab().save(str(out/'appearance-task.png'))
            Gui.getMainWindow().findChild(QtWidgets.QToolButton,'PlusCurveIntent').grab().save(str(out/'surface-control.png'))
            prefs.SetBool('EnableSelection',False);prefs.SetBool('EnablePreselection',False)
            QtTest.QTest.qWait(300);self.assertIsNone(task.highlights.node)
            self.assertEqual([m.DiffuseColor for m in appearance.materials(self.box)],before)
            self.assertEqual(self.doc.UndoCount,undo)
        finally:
            prefs.SetBool('EnableSelection',saved[0]);prefs.SetUnsigned('SelectionColor',saved[1])
            prefs.SetBool('EnablePreselection',saved[2]);prefs.SetUnsigned('HighlightColor',saved[3])

    def test_shell_face_scope_and_focus_restore(self):
        from freecad_plus import shell_task, extrude_task
        Gui.Selection.clearSelection();task=shell_task.show();settle()
        try:
            self.assertEqual(selection_scope.current()[0],'surface')
            task.thickness.setFocus();settle()
            self.assertEqual(selection_scope.current()[0],'curve')
            task.activate_list();settle()
            self.assertEqual(selection_scope.current()[0],'surface')
        finally:task.reject()

    def test_responsive_tabs_equal_shrink_and_scroll(self):
        tabs=panel.ComponentTabBar();tabs.setExpanding(False);tabs.setUsesScrollButtons(True)
        for label in ('Home','Modeling','Sketch','Assembly','Mesh','View','Part','All Tools'):tabs.addTab(label)
        tabs.resize(900,40);tabs.show();settle()
        wide=[tabs.tabRect(i).width() for i in range(tabs.count())]
        self.assertLessEqual(max(wide)-min(wide),1)
        tabs.resize(620,40);settle();narrow=[tabs.tabRect(i).width() for i in range(tabs.count())]
        self.assertLessEqual(max(narrow)-min(narrow),1);self.assertLess(max(narrow),max(wide))
        tabs.resize(240,40);settle()
        self.assertTrue(any(b.isVisible() for b in tabs.findChildren(QtWidgets.QToolButton)))
        tabs.close();tabs.deleteLater()
