# SPDX-License-Identifier: LGPL-2.1-or-later
"""Actual Qt interaction and native ownership checks for the component panel."""
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, hierarchy, editing, external, panel


def settle():
    QtTest.QTest.qWait(60)


class TestComponentPanel(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:
            self.skipTest('Set PLUS_TEST_DIR to an isolated validation directory')
        self.output = Path(os.environ['PLUS_TEST_DIR']) / self._testMethodName
        self.output.mkdir(exist_ok=True)
        self.before = set(App.listDocuments())
        # Drain native delayed SyncView selection before creating the next fixture.
        Gui.Selection.clearSelection()
        QtTest.QTest.qWait(350)
        self.doc = document.new_document('PanelFixture')
        self.root = document.validate(self.doc)
        self.parent = self.root.Definitions[0]
        self.child = hierarchy.create_definition(self.doc, 'Shared child')
        self.nested = hierarchy.add_instance(self.parent, self.child)
        self.first = self.root.Group[0]
        self.second = hierarchy.add_instance(self.root, self.parent,
                                            App.Placement(App.Vector(25, 0, 0), App.Rotation()))
        editing.edit((self.second, self.nested))
        self.sketch = editing.new_sketch(self.doc)
        self.sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2), False)
        self.doc.recompute()
        self.pad = editing.pad(self.doc, self.sketch, 5)
        self.unused = hierarchy.create_definition(self.doc, 'Unused component')
        self.widget = panel.show_panel()
        self.widget.resize(380, 650)
        settle()

    def tearDown(self):
        self.widget.close()
        settle()
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)
        settle()

    def rows(self, index):
        return [(item, item.data(0, panel._ROLE)) for item in self.widget._maps[index].values()]

    def occurrence(self, path):
        key = tuple(panel.identity(o) for o in path)
        return next(item for item, row in self.rows(1) if row.path == key)

    def model(self, definition):
        return next(item for item, row in self.rows(0) if row.ref == panel.identity(definition) and row.kind == 'model')

    def click(self, tree_index, item, double=False, modifier=QtCore.Qt.NoModifier):
        self.widget.tabs.setCurrentIndex(tree_index)
        tree = self.widget.trees[tree_index]
        tree.scrollToItem(item)
        settle()
        point = tree.visualItemRect(item).center()
        QtTest.QTest.mouseClick(tree.viewport(), QtCore.Qt.LeftButton, modifier, point)
        if double:
            QtTest.QTest.mouseDClick(tree.viewport(), QtCore.Qt.LeftButton, modifier, point)
        settle()

    def test_projection_ownership_and_history_without_body_rows(self):
        before = [(o.Name, o.ID) for o in self.doc.Objects]
        undo = self.doc.UndoCount
        self.assertEqual([self.widget.tabs.tabText(i) for i in range(3)], ['Models', 'Part Tree', 'History'])
        self.assertEqual(self.widget.trees[1].topLevelItemCount(), 1)
        self.assertFalse(self.widget.trees[1].topLevelItem(0).icon(0).isNull())
        self.assertEqual(len([r for _, r in self.rows(0) if r.kind == 'model']), 3)
        self.assertEqual(len([r for _, r in self.rows(1) if r.kind == 'occurrence']), 4)
        history = [panel.lookup(r.ref) for _, r in self.rows(2)]
        self.assertEqual(history, [self.sketch, self.pad])
        self.assertNotIn('PartDesign::Body', [o.TypeId for o in history])
        # A repeated refresh must not recreate rows, geometry or transactions.
        row = self.occurrence((self.second, self.nested))
        self.widget.refresh()
        self.assertIs(self.occurrence((self.second, self.nested)), row)
        self.assertEqual([(o.Name, o.ID) for o in self.doc.Objects], before)
        self.assertEqual(self.doc.UndoCount, undo)

    def test_mouse_selection_double_click_edit_and_model_occurrence_memory(self):
        initial = editing.context_path(self.doc)
        first_child = self.occurrence((self.first, self.nested))
        self.click(1, first_child)
        self.assertEqual(editing.context_path(self.doc), initial)
        selected = Gui.Selection.getSelectionEx(self.doc.Name, 0)
        self.assertTrue(selected, f'{self.widget.message.text()} selectedRows={len(self.widget.trees[1].selectedItems())} rect={self.widget.trees[1].visualItemRect(first_child)} visible={self.widget.trees[1].isVisible()} selection={Gui.Selection.getSelectionEx()}')
        self.assertEqual(tuple(selected[0].SubElementNames), (hierarchy.subname((self.first, self.nested)),))
        # An observer update between clicks retains the same row and intended target.
        self.parent.Label = 'Renamed parent'
        settle()
        self.assertIs(first_child, self.occurrence((self.first, self.nested)))
        self.click(1, first_child, double=True)
        self.assertEqual(editing.context_path(self.doc), (self.child, (self.first, self.nested)))
        for item, row in self.rows(1):
            if row.kind == 'occurrence' and row.ref == panel.identity(self.child):
                self.assertTrue(item.font(0).bold())
                self.assertTrue(item.data(0, panel._ACTIVE))
        self.assertTrue(self.model(self.child).font(0).bold())
        self.assertTrue(first_child.data(0, panel._EDITED))
        self.click(1, self.occurrence((self.second, self.nested)), double=True)
        self.click(1, self.occurrence((self.first,)), double=True)
        self.click(0, self.model(self.child), double=True)
        self.assertEqual(editing.context_path(self.doc)[1], (self.second, self.nested))
        file_item = self.widget.trees[1].topLevelItem(0)
        self.click(1, file_item)
        self.assertEqual(editing.context_path(self.doc)[0], self.child)
        self.click(1, file_item, double=True)
        with self.assertRaises(ValueError): editing.context_path(self.doc)
        self.assertEqual(len(self.rows(2)), 4)
        before = len(self.doc.Objects)
        self.widget.edit_row(self.model(self.unused).data(0, panel._ROLE))
        self.assertEqual(editing.context_path(self.doc), (self.unused, ()))
        self.assertEqual(len(self.doc.Objects), before)

    def test_tab_guard_stale_rows_and_per_view_context(self):
        old_row = self.occurrence((self.second, self.nested)).data(0, panel._ROLE)
        old_view = Gui.activeDocument().activeView()
        first_subwindow = Gui.getMainWindow().findChild(QtWidgets.QMdiArea).activeSubWindow()
        Gui.activeDocument().createView('Gui::View3DInventor')
        editing.edit((self.first, self.nested)); settle()
        self.widget.edit_row(self.model(self.parent).data(0, panel._ROLE))
        self.widget.edit_row(self.model(self.child).data(0, panel._ROLE))
        self.assertEqual(editing.context_path(self.doc)[1], (self.first, self.nested))
        Gui.getMainWindow().findChild(QtWidgets.QMdiArea).setActiveSubWindow(first_subwindow)
        settle()
        self.assertEqual(Gui.activeDocument().activeView(), old_view)
        self.assertEqual(editing.context_path(self.doc)[1], (self.second, self.nested))
        # Finish native delayed SyncView selection before the independent tab guard check.
        QtTest.QTest.qWait(350)
        other = document.new_document('OtherPanelFile')
        with self.assertRaises(ValueError): self.widget.edit_row(old_row)
        settle()
        self.assertEqual(self.widget._binding[0], other)
        App.setActiveDocument(self.doc.Name); settle()
        with document.transaction(self.doc, 'Remove occurrence'):
            self.doc.removeObject(self.second.Name)
        settle()
        with self.assertRaises(ValueError): self.widget.edit_row(old_row)
        self.doc.undo(); self.doc.recompute(); settle()
        restored = self.doc.getObject(old_row.path[0][2])
        self.assertIsNotNone(restored)
        self.assertEqual(len([r for _, r in self.rows(1) if r.kind == 'occurrence']), 4)

    def test_nested_import_labels_and_external_edit_remain_in_assembly(self):
        document.save_document(self.doc, self.output / 'Assembly.cadprt')
        source = document.new_document('Hardware')
        source_root = document.validate(source)
        source_root.Definitions[0].Label = self.child.Label
        document.save_document(source, self.output / 'Hardware.cadprt')
        leaf = document.new_document('Fasteners')
        document.save_document(leaf, self.output / 'Fasteners.cadprt')
        external.import_file(source, leaf)
        document.save_document(source)
        external.import_file(self.doc, source)
        link = hierarchy.add_instance(self.root, source_root.Definitions[0])
        App.setActiveDocument(self.doc.Name); settle()
        labels = [r.label for _, r in self.rows(0)]
        self.assertIn('Shared child (Hardware)', labels)
        self.assertIn('Part001 (Fasteners)', labels)
        self.assertIn('Hardware', labels)
        self.assertIn('Fasteners', labels)
        self.click(0, self.model(source_root.Definitions[0]), double=True)
        self.assertEqual(App.ActiveDocument, self.doc)
        self.assertEqual(editing.context_path(self.doc), (source_root.Definitions[0], (link,)))
        sketch = editing.new_sketch(self.doc); settle()
        self.assertEqual(sketch.Document, source)
        self.assertEqual([panel.lookup(r.ref) for _, r in self.rows(2)], [sketch])

    def test_file_origin_visibility_persistence_and_no_display_model_mutation(self):
        editing.edit_file(self.doc); settle()
        origin = self.root.Origin
        origin.Visibility = False; settle()
        plane_item = next(item for item, row in self.rows(2) if panel.lookup(row.ref).TypeId == 'App::Plane')
        plane = panel.lookup(plane_item.data(0, panel._ROLE).ref)
        plane.Visibility = False; settle()
        plane_item.setCheckState(0, QtCore.Qt.Checked); settle()
        self.assertTrue(plane.Visibility)
        self.assertTrue(origin.Visibility)
        self.doc.undo(); self.doc.recompute(); settle()
        self.assertFalse(origin.Visibility)
        self.doc.redo(); self.doc.recompute(); settle()
        self.assertTrue(origin.Visibility)
        path = document.save_document(self.doc, self.output / 'Panel.cadprt')
        ids = {o.Name: o.ID for o in self.doc.Objects}
        self.widget.close(); App.closeDocument(self.doc.Name)
        self.doc = document.open_document(path)
        self.widget = panel.show_panel(); settle()
        self.assertEqual({o.Name: o.ID for o in self.doc.Objects}, ids)
        self.assertEqual(self.widget.trees[1].topLevelItemCount(), 1)
        self.assertEqual(len(self.rows(2)), 4)

    def test_event_coalescing_idle_and_observer_cleanup(self):
        before = self.widget.refresh_count
        for i in range(20): self.child.Label = 'Child ' + str(i)
        settle()
        self.assertLessEqual(self.widget.refresh_count - before, 2)
        self.assertEqual(self.model(self.child).text(0), 'Child 19')
        before = self.widget.refresh_count
        QtTest.QTest.qWait(350)
        self.assertEqual(self.widget.refresh_count, before)
        callbacks = len(editing._context_observers)
        self.widget.close(); settle()
        self.assertEqual(len(editing._context_observers), callbacks - 1)
        before = self.widget.refresh_count
        self.child.Label = 'After close'; self.doc.recompute(); settle()
        self.assertEqual(self.widget.refresh_count, before)
        self.widget = panel.show_panel(); settle()
        self.assertEqual(len(editing._context_observers), callbacks)


class TestUIModes(unittest.TestCase):
    """Normal startup, real preference dialogs, mixed modes and shared native tasks."""
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:
            self.skipTest('Use an isolated profile and PLUS_TEST_DIR for UI-mode acceptance')
        from freecad_plus import ui_modes
        self.modes=ui_modes
        self.prefs=App.ParamGet('User parameter:BaseApp/Preferences/General')
        self.window=Gui.getMainWindow()
        self.before=set(App.listDocuments())
        self.output=Path(os.environ['PLUS_TEST_DIR'])

    def tearDown(self):
        for name in set(App.listDocuments())-self.before:
            gui=Gui.getDocument(name)
            if gui.getInEdit():gui.resetEdit()
            if App.getActiveTransaction():App.closeActiveTransaction(True)
            App.closeDocument(name)
        settle()

    def choose_modes(self,values):
        for key,value in zip(self.modes.KEYS,values):self.prefs.SetInt(key,value)
        self.modes.apply_modes();settle()

    def check_model(self,plus):
        self.assertEqual(panel._panel.isVisible(),plus)
        dock=self.window.findChild(QtWidgets.QDockWidget,'Model')
        self.assertIsNotNone(dock)
        trees=[w for w in dock.findChildren(QtWidgets.QWidget) if w.metaObject().className()=='Gui::TreePanel']
        self.assertTrue(trees)
        self.assertEqual(trees[0].isHidden(),plus)
        self.assertEqual(dock.windowTitle(),'Properties' if plus else 'Model')
        self.assertTrue(dock.findChild(QtWidgets.QTreeView,'propertyEditorData'))

    def preferences(self,callback):
        errors=[];completed=[];attempts=[0]
        def interact():
            dialogs=[w for w in QtWidgets.QApplication.topLevelWidgets() if isinstance(w,QtWidgets.QDialog)]
            dlg=next((w for w in dialogs if 'DlgPreferencesImp' in w.metaObject().className() and w.isVisible()),None)
            attempts[0]+=1
            if dlg is None and attempts[0]<100:
                QtCore.QTimer.singleShot(50,interact)
                return
            try:
                self.assertIsNotNone(dlg)
                boxes=[dlg.findChild(QtWidgets.QComboBox,key) for key in self.modes.KEYS]
                self.assertTrue(all(boxes))
                callback(dlg,boxes);completed.append(True)
            except BaseException as error:errors.append(error)
            finally:
                if dlg is not None:dlg.reject()
                else:
                    for visible in dialogs:
                        if visible.isVisible():visible.reject()
        QtCore.QTimer.singleShot(250,interact)
        Gui.showPreferences('General',0);QtTest.QTest.qWait(400)
        if errors:raise errors[0]
        self.assertTrue(completed)

    def test_01_default_startup_and_preferences_cancel(self):
        self.assertEqual(self.modes.modes(),('Plus','Plus','Plus'))
        self.check_model(True)
        self.assertTrue(panel._panel.toggleViewAction().isVisible())
        def check(dlg,boxes):
            group=dlg.findChild(QtWidgets.QGroupBox,'GroupBox3')
            self.assertEqual(group.title(),'Application')
            for row,box in enumerate(boxes):
                self.assertEqual(box.currentText(),'Plus UI Mode')
                self.assertEqual([box.itemText(i) for i in range(box.count())],['Plus UI Mode','Classic UI Mode'])
                self.assertEqual(group.layout().getItemPosition(group.layout().indexOf(box))[:2],(row,1))
                box.setCurrentIndex(1)
            group.grab().save(str(self.output/'preferences.png'))
        self.preferences(check)
        self.assertEqual(self.modes.modes(),('Plus','Plus','Plus'))
        self.check_model(True)

    def test_02_mixed_modes_preserve_backend_and_menu(self):
        import itertools
        doc=document.new_document('MixedModes');root=document.validate(doc)
        sketch=editing.new_sketch(doc);sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),2),False)
        feature=editing.pad(doc,sketch,5);doc.recompute()
        ids={o.Name:o.ID for o in doc.Objects};undo=doc.UndoCount
        owner,path=editing.context_path(doc)
        Gui.activateWorkbench('PartDesignWorkbench');settle()
        def toolbar_actions():
            return {bar.objectName():tuple(a.objectName() for a in bar.actions())
                    for bar in self.window.findChildren(QtWidgets.QToolBar)}
        actions=toolbar_actions()
        for values in itertools.product((0,1),repeat=3):
            self.choose_modes(values);self.check_model(values[0]==0)
            self.assertEqual({o.Name:o.ID for o in doc.Objects},ids);self.assertEqual(doc.UndoCount,undo)
            self.assertEqual(editing.context_path(doc),(owner,path))
            self.assertEqual(toolbar_actions(),actions);self.assertTrue(feature.Shape.isValid())
            self.assertAlmostEqual(feature.Shape.Volume,20*3.141592653589793)
            document.validate(doc)
        self.choose_modes((0,1,0))
        panel._panel.close();settle();self.assertFalse(panel._panel._closed)
        self.assertFalse(panel._panel.isVisible())
        panel._panel.toggleViewAction().trigger();settle();self.check_model(True)
        Gui.activateWorkbench('PartWorkbench');settle();self.check_model(True)
        self.assertTrue(panel._panel.toggleViewAction().isVisible())

    def test_03_native_pad_pocket_survive_presentation_changes(self):
        import json,math
        from TestComponentModeling import accept_task,messages
        from freecad_plus import geometry,display
        doc=document.new_document('SharedExtrude');root=document.validate(doc);owner=root.Definitions[0]
        Gui.activateWorkbench('PartDesignWorkbench');self.choose_modes((1,1,1))
        sketch=editing.new_sketch(doc);sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),2),False)
        doc.recompute();Gui.Selection.clearSelection();Gui.Selection.addSelection(sketch)
        with messages() as errors:Gui.runCommand('PartDesign_Pad');settle()
        self.assertFalse(errors,errors)
        pad=Gui.getDocument(doc.Name).getInEdit().Object
        length=next(w for w in self.window.findChildren(QtWidgets.QWidget) if w.objectName()=='lengthEdit' and w.isVisible())
        self.assertTrue(length.setProperty('rawValue',5.0));settle()
        task=Gui.Control.activeDialog();transaction=App.getActiveTransaction()
        self.choose_modes((0,0,0))
        self.assertEqual(Gui.Control.activeDialog(),task);self.assertEqual(App.getActiveTransaction(),transaction)
        self.assertEqual(Gui.getDocument(doc.Name).getInEdit().Object,pad)
        accept_task();doc.recompute();self.assertAlmostEqual(pad.Shape.Volume,20*math.pi)
        profile=editing.new_sketch(doc);profile.Placement.Base=App.Vector(0,0,5)
        profile.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),0.5),False)
        doc.recompute();Gui.Selection.clearSelection();Gui.Selection.addSelection(profile)
        with messages() as errors:Gui.runCommand('PartDesign_Pocket');settle()
        self.assertFalse(errors,errors)
        pocket=Gui.getDocument(doc.Name).getInEdit().Object
        length=next(w for w in self.window.findChildren(QtWidgets.QWidget) if w.objectName()=='lengthEdit' and w.isVisible())
        self.assertTrue(length.setProperty('rawValue',2.0));settle()
        self.choose_modes((1,0,1));self.assertEqual(Gui.getDocument(doc.Name).getInEdit().Object,pocket)
        accept_task();doc.recompute();self.assertTrue(pocket.Shape.isValid())
        self.assertAlmostEqual(pocket.Shape.Volume,19.5*math.pi)
        name=pocket.Name;doc.undo();doc.recompute();self.assertIsNone(doc.getObject(name))
        doc.redo();doc.recompute();pocket=doc.getObject(name)
        self.assertAlmostEqual(pocket.Shape.Volume,19.5*math.pi)
        source=hierarchy.create_definition(doc,'Reference')
        foreign=source.newObject('Part::Box','Foreign');link=hierarchy.add_instance(owner,source)
        display.set_state(owner,link,part_type='Reference');doc.recompute()
        for mode in (0,1):
            self.choose_modes((mode,mode,mode))
            with self.assertRaises(ValueError):geometry.require_modeling_inputs(profile,[(foreign,'')])
        name=pocket.Name;document.validate(doc)
        document.save_document(doc,self.output/'UIModes.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':{o.Name:o.ID for o in doc.Objects},
            'pad':pad.Name,'pocket':name,'profile':profile.Name,'volume':pocket.Shape.Volume}))

    def test_04_preferences_apply_and_persist(self):
        self.choose_modes((0,0,0))
        def apply(dlg,boxes):
            for box,value in zip(boxes,(1,0,1)):box.setCurrentIndex(value)
            buttons=dlg.findChild(QtWidgets.QDialogButtonBox)
            buttons.button(QtWidgets.QDialogButtonBox.Apply).click();settle()
            self.assertEqual(self.modes.modes(),('Classic','Plus','Classic'));self.check_model(False)
        self.preferences(apply)
        self.preferences(lambda dlg,boxes:self.assertEqual([b.currentIndex() for b in boxes],[1,0,1]))
        App.saveParameter()


    def test_05_independent_native_tree_layout(self):
        groups={name:App.ParamGet('User parameter:BaseApp/Preferences/DockWindows/'+name)
                for name in ('ComboView','TreeView','PropertyView')}
        old={name:group.GetBool('Enabled',name=='ComboView') for name,group in groups.items()}
        try:
            for name,group in groups.items():group.SetBool('Enabled',name!='ComboView')
            QtTest.QTest.qWait(1200)
            self.choose_modes((0,0,0))
            tree=self.window.findChild(QtWidgets.QDockWidget,'Tree view')
            self.assertIsNotNone(tree);self.assertTrue(tree.isHidden())
            self.assertFalse(tree.toggleViewAction().isVisible())
            self.choose_modes((1,0,0));self.assertFalse(tree.isHidden())
            self.assertTrue(tree.toggleViewAction().isVisible())
            properties=self.window.findChild(QtWidgets.QDockWidget,'Property view')
            self.assertIsNotNone(properties);self.assertFalse(properties.isHidden())
            self.choose_modes((0,0,0));self.assertTrue(tree.isHidden())
        finally:
            for name,group in groups.items():group.SetBool('Enabled',old[name])
            QtTest.QTest.qWait(1200)
            self.choose_modes((1,0,1));App.saveParameter()


def verify_ui_modes_reopen(output):
    import json,math
    from freecad_plus import ui_modes
    assert ui_modes.modes()==('Classic','Plus','Classic')
    assert panel._panel is not None and not panel._panel.isVisible()
    expected=json.loads((Path(output)/'expected.json').read_text())
    doc=document.open_document(Path(output)/'UIModes.cadprt')
    try:
        assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
        pocket=doc.getObject(expected['pocket']);assert abs(pocket.Shape.Volume-expected['volume'])<1e-7
        pocket.Length=3;doc.recompute();document.validate(doc)
        assert pocket.Shape.isValid() and abs(pocket.Shape.Volume-19.25*math.pi)<1e-7
    finally:App.closeDocument(doc.Name)


class TestNativeComponentCreation(unittest.TestCase):
    """Drive the ordinary command entry points, not only backend fixtures."""
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:
            self.skipTest('Set PLUS_TEST_DIR to an isolated validation directory')
        from freecad_plus import ui_modes
        self.modes = ui_modes
        self.before = set(App.listDocuments())
        self.prefs = App.ParamGet('User parameter:BaseApp/Preferences/General')
        self.old = self.prefs.GetInt('ModelPanelUIMode', 0)
        self.output = Path(os.environ['PLUS_TEST_DIR'])

    def tearDown(self):
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)
        self.prefs.SetInt('ModelPanelUIMode', self.old)
        self.modes.apply_modes()
        settle()

    def model_names(self):
        return {item.data(0, panel._ROLE).ref for item in panel._panel._maps[0].values()
                if item.data(0, panel._ROLE).kind == 'model'}

    def test_new_file_and_part_both_presentations(self):
        import json
        for mode in (0, 1):
            self.prefs.SetInt('ModelPanelUIMode', mode)
            self.modes.apply_modes()
            Gui.runCommand('Std_New'); settle()
            doc = App.ActiveDocument
            root = document.validate(doc)
            self.assertEqual([d.Label for d in root.Definitions], ['Part001'])
            self.assertEqual(len(root.Group), 1)
            self.assertEqual(root.Group[0].LinkedObject, root.Definitions[0])
            self.assertEqual(editing.context(doc)[0], root.Definitions[0])
            context = Gui.activeDocument().activeView().getActiveObject('PlusEdit', False)
            existing = {o.Name: o.ID for o in doc.Objects}
            placed = tuple(o.Name for o in root.Group)
            undo = doc.UndoCount
            Gui.runCommand('Std_Part'); settle()
            document.validate(doc)
            self.assertEqual([d.Label for d in root.Definitions], ['Part001', 'Part002'])
            created = root.Definitions[-1]
            name = created.Name
            self.assertIn(panel.identity(created), self.model_names())
            self.assertEqual(tuple(o.Name for o in root.Group), placed)
            self.assertEqual(sum(o.TypeId == 'App::Link' for o in doc.Objects), 1)
            self.assertFalse(any(item.data(0, panel._ROLE).kind == 'unused'
                                 for item in panel._panel._maps[1].values()))
            self.assertEqual(Gui.activeDocument().activeView().getActiveObject('PlusEdit', False), context)
            self.assertEqual({n: doc.getObject(n).ID for n in existing}, existing)
            self.assertEqual(doc.UndoCount, undo + 1)
            doc.undo(); settle()
            self.assertIsNone(doc.getObject(name)); self.assertEqual(len(self.model_names()), 1)
            doc.redo(); settle()
            self.assertIn(panel.identity(doc.getObject(name)), self.model_names())
            self.assertEqual(tuple(o.Name for o in root.Group), placed)
            Gui.runCommand('Std_Part'); settle()
            self.assertEqual([d.Label for d in root.Definitions], ['Part001', 'Part002', 'Part003'])
            if mode == 0:
                document.save_document(doc, self.output/'CreatedModels.cadprt')
                (self.output/'creation_expected.json').write_text(json.dumps({
                    'ids': {o.Name:o.ID for o in doc.Objects}, 'definitions':[d.Name for d in root.Definitions],
                    'instances':list(placed)}), encoding='utf-8')
            App.closeDocument(doc.Name); settle()

    def test_external_definition_owns_new_part(self):
        source = document.new_document('CreationSource')
        document.save_document(source, self.output/'CreationSource.cadprt')
        doc = document.new_document('CreationAssembly')
        document.save_document(doc, self.output/'CreationAssembly.cadprt')
        external.import_file(doc, source)
        imported = document.validate(source).Definitions[0]
        editing.edit_unused(doc, imported); settle()
        root = document.validate(doc)
        domestic = tuple(d.Name for d in root.Definitions)
        source_root = document.validate(source)
        links = tuple(o.Name for o in source_root.Group)
        undo = source.UndoCount
        Gui.runCommand('Std_Part'); settle()
        self.assertEqual(tuple(d.Name for d in root.Definitions), domestic)
        self.assertEqual(len(source_root.Definitions), 2)
        self.assertEqual(source.UndoCount, undo + 1)
        created = source_root.Definitions[-1]
        self.assertIn(panel.identity(created), self.model_names())
        self.assertEqual(tuple(o.Name for o in source_root.Group), links)
        self.assertEqual(editing.context(doc)[0], imported)
        source.undo(); settle()
        self.assertEqual(len(source_root.Definitions), 1)
        document.validate(doc)

    def test_empty_document_and_existing_legacy(self):
        doc = App.newDocument('EmptyNative'); doc.UndoMode = 1
        Gui.runCommand('Std_Part'); settle()
        root = document.validate(doc)
        self.assertEqual([d.Label for d in root.Definitions], ['Part001'])
        self.assertEqual(list(root.Group), [])
        self.assertEqual(len(self.model_names()), 1)
        self.assertEqual(panel._panel.trees[1].topLevelItem(0).childCount(), 0)
        doc.undo(); settle(); self.assertEqual(list(doc.Objects), [])
        doc.redo(); settle(); self.assertEqual(len(document.validate(doc).Definitions), 1)
        legacy = App.newDocument('ExistingLegacy')
        box = legacy.addObject('Part::Box', 'Box'); legacy.recompute()
        old_id = box.ID
        Gui.runCommand('Std_Part'); settle()
        self.assertFalse(any('PlusFormat' in o.PropertiesList for o in legacy.Objects))
        self.assertEqual(legacy.getObject('Box').ID, old_id)
        self.assertTrue(any(o.TypeId == 'App::Part' for o in legacy.Objects))


def verify_native_creation_reopen(output):
    import json
    output = Path(output)
    expected = json.loads((output/'creation_expected.json').read_text(encoding='utf-8'))
    doc = document.open_document(output/'CreatedModels.cadprt')
    try:
        root = document.validate(doc)
        assert {o.Name:o.ID for o in doc.Objects} == expected['ids']
        assert [d.Name for d in root.Definitions] == expected['definitions']
        assert [o.Name for o in root.Group] == expected['instances']
        editing.edit_file(doc); settle()
        assert len([item for item in panel._panel._maps[0].values()
                    if item.data(0,panel._ROLE).kind == 'model']) == 3
        assert panel._panel.trees[1].topLevelItem(0).childCount() == 1
    finally:
        App.closeDocument(doc.Name)
