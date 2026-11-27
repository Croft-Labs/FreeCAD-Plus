# SPDX-License-Identifier: LGPL-2.1-or-later
import os
import json
import unittest
from unittest.mock import patch
from pathlib import Path
import FreeCAD as App
import FreeCADGui as Gui
import Part
from freecad_plus import document, hierarchy, external, file_actions, file_recovery
from PySide6 import QtCore, QtWidgets, QtTest


class TestPartsFiles(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:self.skipTest('Isolated directory required')
        self.output=Path(os.environ['PLUS_TEST_DIR'])/self._testMethodName;self.output.mkdir(exist_ok=True)
        self.before=set(App.listDocuments())
        self.host=document.new_document('Host');self.owner=document.validate(self.host).Definitions[0];self.owner.Label='Host part'
        document.save_document(self.host,self.output/'Host.cadprt')

    def tearDown(self):
        from freecad_plus import file_search_task
        if file_search_task._active:file_search_task._active.reject()
        Gui.Selection.clearSelection()
        for name in reversed(list(App.listDocuments())):
            if name not in self.before:App.closeDocument(name)

    def source(self,name):
        doc=document.new_document(name);part=document.validate(doc).Definitions[0];part.Label=name
        shape=part.newObject('Part::Feature','Solid');shape.Shape=Part.makeBox(3,4,5)
        doc.recompute();document.save_document(doc,self.output/(name+'.cadprt'))
        return doc,part

    def test_create_default_part_linked_without_assembly_placement(self):
        old=list(document.validate(self.host).Group)
        created=file_actions.create_linked_file(self.host,self.output/'NewPart.cadprt')
        root=document.validate(created)
        self.assertEqual(len(root.Definitions),1);self.assertEqual(len(root.Group),1)
        self.assertIn(root,document.validate(self.host).Imports)
        self.assertEqual(old,list(document.validate(self.host).Group))
        self.host.undo();self.assertNotIn(root,document.validate(self.host).Imports)
        with self.assertRaisesRegex(ValueError,'existing files'):
            file_actions.create_linked_file(self.host,self.output/'NewPart.cadprt')

    def test_copy_dependencies_shared_once_colors_placements_undo(self):
        leaf,bolt=self.source('Bolt');source,parent=self.source('Assembly')
        external.import_file(source,leaf)
        for x in (10,20):hierarchy.add_instance(parent,bolt,App.Placement(App.Vector(x,0,0),App.Rotation()))
        document.save_document(source)
        external.import_file(self.host,source)
        self.assertEqual(file_actions.dependencies([parent]),[leaf.FileName])
        before=tuple((o.Name,o.ID) for o in source.Objects)
        root=document.validate(self.host);count=len(root.Definitions)
        copies=file_actions.copy_parts(self.host,[parent])
        self.assertEqual(len(copies),2);self.assertNotEqual(copies[0].Label,parent.Label)
        children=[o for o in copies[0].Group if o.TypeId=='App::Link']
        self.assertEqual(len(children),2);self.assertEqual(children[0].LinkedObject,children[1].LinkedObject)
        self.assertEqual([o.LinkPlacement.Base.x for o in children],[10,20])
        self.assertTrue(all(o.Document==self.host for part in copies for o in part.OutListRecursive))
        self.assertEqual(before,tuple((o.Name,o.ID) for o in source.Objects))
        self.host.undo();self.assertEqual(len(root.Definitions),count)

    def test_bake_final_geometry_breaks_links_and_preserves_placements(self):
        source,parent=self.source('Assembly');leaf,bolt=self.source('Bolt')
        external.import_file(source,leaf)
        hierarchy.add_instance(parent,bolt,App.Placement(App.Vector(10,0,0),App.Rotation()))
        document.save_document(source)
        copies=file_actions.copy_parts(self.host,[parent],bake=True)
        self.assertEqual(len(copies),1)
        shapes=[o for o in copies[0].Group if hasattr(o,'Shape')]
        self.assertEqual(len(shapes),2);self.assertAlmostEqual(sum(o.Shape.Volume for o in shapes),120)
        self.assertAlmostEqual(max(o.Shape.BoundBox.XMax for o in shapes),13)
        self.assertFalse(any(o.TypeId=='App::Link' for o in copies[0].Group))
        self.assertTrue(all(o.Document==self.host for o in copies[0].OutListRecursive))

    def test_recovery_validates_identity_and_keeps_files_unchanged_until_save(self):
        source,part=self.source('Source');external.import_file(self.host,source)
        link=hierarchy.add_instance(self.owner,part)
        document.save_document(self.host)
        host_path=Path(self.host.FileName);source_path=Path(source.FileName)
        expected=(str(self.host.Uid),link.Name,link.ID,part.Name,part.ID)
        original=host_path.read_bytes();App.closeDocument(self.host.Name);App.closeDocument(source.Name)
        moved=self.output/'Moved.cadprt';source_path.rename(moved)
        with self.assertRaises(external.MissingReference) as caught:external.archive_graph(host_path)
        missing=caught.exception
        self.assertTrue(file_recovery.verify(moved,missing));self.assertFalse(file_recovery.verify(host_path,missing))
        self.assertIn((str(moved),True),list(file_recovery.search([str(self.output)],missing)))
        self.host=file_recovery.open_resolved(host_path,{source_path:moved})
        self.assertEqual(str(self.host.Uid),expected[0])
        restored=self.host.getObject(expected[1])
        self.assertEqual((restored.ID,restored.LinkedObject.Name,restored.LinkedObject.ID),expected[2:])
        self.assertEqual(Path(restored.LinkedObject.Document.FileName),moved)
        self.assertEqual(host_path.read_bytes(),original)
        document.save_document(self.host)
        self.assertIn(moved,external.archive_graph(host_path))

    def test_loaded_relocation_and_search_cancel(self):
        source,part=self.source('Source');external.import_file(self.host,source)
        old=Path(source.FileName);moved=self.output/'Renamed.cadprt';old.rename(moved)
        file_recovery.relocate_loaded(source,moved)
        self.assertEqual(Path(source.FileName),moved)
        document.save_document(self.host)
        self.assertIn(moved,external.archive_graph(self.host.FileName))
        missing=external.MissingReference(old,str(source.Uid),[part.Name])
        self.assertEqual(list(file_recovery.search([str(self.output)],missing,stopped=lambda:True)),[])

    def test_search_task_real_worker_verified_selection_and_remember(self):
        from freecad_plus import file_search_task
        source,part=self.source('Source')
        missing=external.MissingReference(self.output/'Old.cadprt',str(source.Uid),[part.Name])
        App.setActiveDocument(self.host.Name)
        calls=[];task=file_search_task.open_task(missing,calls.append,host=self.host)
        task.form.folders.addItem(str(self.output));task.search()
        for _ in range(100):
            QtTest.QTest.qWait(30)
            if task.worker is None:break
        self.assertIsNone(task.worker)
        self.assertEqual(task.form.results.topLevelItemCount(),1)
        task.form.results.setCurrentItem(task.form.results.topLevelItem(0));task.form.use.click()
        self.assertEqual(calls,[source.FileName])
        Gui.updateGui();QtTest.QTest.qWait(100)
        win=Gui.getMainWindow();full=win.grab();ratio=full.devicePixelRatio();pos=task.form.mapTo(win,QtCore.QPoint(0,0))
        full.copy(QtCore.QRect(round(pos.x()*ratio),round(pos.y()*ratio),round(task.form.width()*ratio),round(task.form.height()*ratio))).save(str(self.output/'search-task.png'))
        full.save(str(self.output/'search-window.png'))
        task.accept();self.assertEqual(file_recovery.remembered(self.host),[str(self.output)])
        task=file_search_task.open_task(missing,calls.append,host=self.host)
        task.form.folders.clear();task.search();self.assertTrue(task.form.status.error)
        task.reject();self.assertEqual(file_recovery.remembered(self.host),[str(self.output)])

    def test_missing_open_locate_and_cancel_workflow(self):
        from freecad_plus import file_workflows,file_actions_ui
        source,part=self.source('Source');external.import_file(self.host,source);document.save_document(self.host)
        path=self.host.FileName;old=Path(source.FileName)
        App.closeDocument(self.host.Name);App.closeDocument(source.Name)
        moved=self.output/'Moved.cadprt';old.rename(moved)
        def choose():
            dialog=QtWidgets.QApplication.activeModalWidget()
            if isinstance(dialog,file_actions_ui.MissingFileDialog):dialog.locate.click()
        QtCore.QTimer.singleShot(100,choose)
        with patch.object(file_actions_ui,'native_locate',return_value=str(moved)):
            self.host=file_workflows.open_file(path)
        self.assertIsNotNone(self.host)
        self.assertEqual(Path(document.validate(self.host).Imports[0].Document.FileName),moved)

    def test_parts_create_menu_and_copy_destinations(self):
        from freecad_plus import panel,file_actions_ui,editing
        source,part=self.source('Source');external.import_file(self.host,source)
        App.setActiveDocument(self.host.Name);dock=panel.show_panel();dock.refresh()
        model=next(item.data(0,panel._ROLE) for item in dock._maps[0].values()
                   if item.data(0,panel._ROLE).kind=='model' and item.data(0,panel._ROLE).ref==panel.identity(part))
        dock.edit_row(model)
        self.assertEqual(editing.context_path(self.host)[0],part)
        row=next(item.data(0,panel._ROLE) for item in dock._maps[0].values() if item.data(0,panel._ROLE).kind=='import')
        before=len(document.validate(self.host).Definitions)
        file_actions_ui.run_action(dock,'copy',row)
        self.assertEqual(len(document.validate(self.host).Definitions),before+1)
        self.assertEqual(len(document.validate(source).Definitions),1)
        with patch.object(file_actions_ui,'native_save',return_value=''):
            count=len(App.listDocuments());file_actions_ui.run_action(dock,'create');self.assertEqual(len(App.listDocuments()),count)

    def test_bake_nested_transforms_and_mesh_material(self):
        import Mesh
        source,parent=self.source('Assembly');leaf,bolt=self.source('Bolt')
        parent.Placement.Base=App.Vector(2,3,4);bolt.Placement.Base=App.Vector(5,6,7)
        external.import_file(source,leaf)
        link=hierarchy.add_instance(parent,bolt,App.Placement(App.Vector(10,0,0),App.Rotation(App.Vector(0,0,1),90)))
        link.LinkTransform=True
        mesh=parent.newObject('Mesh::Feature','Mesh');mesh.Mesh=Mesh.Mesh([((0,0,0),(1,0,0),(0,1,0))])
        mesh.Placement.Base=App.Vector(7,0,0);mesh.ViewObject.ShapeColor=(0.2,0.4,0.7)
        source.recompute()
        expected=Part.getShape(parent).BoundBox
        copy=file_actions.copy_parts(self.host,[parent],bake=True)[0]
        actual=Part.getShape(copy).BoundBox
        for name in ('XMin','XMax','YMin','YMax','ZMin','ZMax'):
            self.assertAlmostEqual(getattr(actual,name),getattr(expected,name),places=5)
        copied=next(obj for obj in copy.Group if obj.isDerivedFrom('Mesh::Feature'))
        self.assertEqual(copied.Mesh.CountFacets,1)
        self.assertEqual(tuple(copied.ViewObject.ShapeColor),tuple(mesh.ViewObject.ShapeColor))

    def test_subfile_menus_dependency_cancel_and_open_window(self):
        from freecad_plus import panel,file_actions_ui
        source,parent=self.source('Assembly');leaf,bolt=self.source('Bolt')
        external.import_file(source,leaf);hierarchy.add_instance(parent,bolt);document.save_document(source)
        external.import_file(self.host,source)
        App.setActiveDocument(self.host.Name);dock=panel.show_panel();dock.tabs.setCurrentIndex(0);dock.refresh()
        tree=dock.trees[0]
        item=next(item for item in dock._maps[0].values() if item.data(0,panel._ROLE).kind=='import' and item.data(0,panel._ROLE).ref==panel.identity(document.validate(source)))
        row=item.data(0,panel._ROLE);before=len(self.host.Objects);seen=[]
        def capture():
            menu=QtWidgets.QApplication.activePopupWidget()
            seen.extend((a.text(),a.isEnabled()) for a in menu.actions() if a.text())
            menu.grab().save(str(self.output/'subfile-menu.png'));menu.close()
        tree.scrollToItem(item);QtTest.QTest.qWait(100)
        QtCore.QTimer.singleShot(100,capture);dock._menu(tree,tree.visualItemRect(item).center())
        self.assertEqual([label for label,on in seen],['Open file in new window','Create new part file\u2026','Import models to file\u2026','Search folders\u2026'])
        def cancel():
            dialog=QtWidgets.QApplication.activeModalWidget()
            if isinstance(dialog,file_actions_ui.DependenciesDialog):
                dialog.grab().save(str(self.output/'dependencies.png'));dialog.reject()
        QtCore.QTimer.singleShot(100,cancel);file_actions_ui.run_action(dock,'copy',row)
        self.assertEqual(len(self.host.Objects),before)
        file_actions_ui.run_action(dock,'open',row)
        self.assertEqual(App.ActiveDocument,source)
        App.setActiveDocument(self.host.Name);dock.refresh()
        old=Path(source.FileName);old.rename(self.output/'Moved.cadprt');seen=[]
        item=next(item for item in dock._maps[0].values() if item.data(0,panel._ROLE).kind=='import' and item.data(0,panel._ROLE).ref==row.ref)
        tree.scrollToItem(item);QtTest.QTest.qWait(100)
        QtCore.QTimer.singleShot(100,capture);dock._menu(tree,tree.visualItemRect(item).center())
        self.assertIn(('Locate file\u2026',True),seen)
        self.assertIn(('Open file in new window',False),seen)
        self.assertIn(('Import models to file\u2026',False),seen)

    def test_copy_associative_external_geometry_and_expression(self):
        from freecad_plus import derived_geometry,editing
        source,parent=self.source('Assembly');leaf,bolt=self.source('Bolt')
        external.import_file(source,leaf);link=hierarchy.add_instance(parent,bolt)
        base=next(o for o in bolt.Group if hasattr(o,'Shape'))
        App.setActiveDocument(source.Name);editing.edit((document.validate(source).Group[0],))
        clone=derived_geometry.save(source,[(link,base.Name+'.')])[0]
        document.save_document(source)
        copies=file_actions.copy_parts(self.host,[parent])
        clone_copy=next(o for o in copies[0].OutListRecursive if derived_geometry.is_derived(o))
        self.assertEqual(clone_copy.SourceObject.Document,self.host)
        self.assertFalse(clone_copy.GeometryError)
        self.assertAlmostEqual(clone_copy.Shape.Volume,clone.Shape.Volume)
        document.save_document(self.host)
        manifest={'path':self.host.FileName,'uid':str(self.host.Uid),'ids':{o.Name:o.ID for o in self.host.Objects}}
        (self.output/'reopen.json').write_text(json.dumps(manifest),encoding='utf-8')


class TestPartsFilesFresh(unittest.TestCase):
    def test_fresh_saved_copy(self):
        folder=os.environ.get('PLUS_COMPONENTS_REOPEN')
        if not folder:self.skipTest('Requires a prior isolated copy fixture')
        info=json.loads((Path(folder)/'test_copy_associative_external_geometry_and_expression/reopen.json').read_text())
        doc=document.open_document(info['path'])
        try:
            self.assertEqual(str(doc.Uid),info['uid']);self.assertEqual({o.Name:o.ID for o in doc.Objects},info['ids'])
            self.assertEqual(len(external.archive_graph(info['path'])),1)
        finally:App.closeDocument(doc.Name)
