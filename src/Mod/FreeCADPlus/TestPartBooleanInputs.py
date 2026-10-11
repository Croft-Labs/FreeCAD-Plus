# SPDX-License-Identifier: LGPL-2.1-or-later
"""Part Boolean component eligibility, ownership, native tasks and persistence."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, display, editing, geometry, hierarchy
from TestComponentPanel import TestComponentPanel, settle
from TestComponentModeling import TestComponentModeling, messages
from TestComponentReferences import TestComponentReferences
from TestComponentInputEditors import TestComponentInputEditors


class TestPartBooleanInputs(unittest.TestCase):
    setUp = TestComponentPanel.setUp
    tearDown = TestComponentModeling.tearDown
    select = TestComponentModeling.select
    control = TestComponentReferences.control
    task_button = TestComponentInputEditors.task_button

    def boxes(self, owner=None):
        Gui.activateWorkbench('PartWorkbench')
        owner = owner or self.child
        create = owner.addObject if hasattr(owner, 'Objects') else owner.newObject
        a=create('Part::Box','BooleanBase'); b=create('Part::Box','BooleanTool')
        for obj in (a,b): obj.Length=4; obj.Width=4; obj.Height=4
        b.Placement.Base=App.Vector(2,0,0)
        doc = owner if hasattr(owner, 'Objects') else owner.Document
        doc.recompute(); settle()
        return a,b

    def snapshot(self):
        return ({o.Name:o.ID for o in self.doc.Objects},self.doc.UndoCount,App.getActiveTransaction(),
                [(o.Name,tuple(c.Name for c in document.owned_children(o))) for o in self.doc.Objects],
                [(o.Name,o.Visibility) for o in self.doc.Objects if hasattr(o,'Visibility')])

    def test_commands_reject_reference_excluded_and_missing_edit_atomically(self):
        a,b=self.boxes()
        source=hierarchy.create_definition(self.doc,'Reference tool')
        foreign,_=self.boxes(source); link=hierarchy.add_instance(self.child,source)
        path=hierarchy.subname((self.second,self.nested,link))+foreign.Name+'.'
        for kind in ('Reference','Excluded'):
            display.set_state(self.child,link,part_type=kind);settle()
            for command in ('Part_Cut','Part_Common','Part_Fuse'):
                self.select(a);Gui.Selection.addSelection(self.doc.Name,self.root.Name,path)
                before=self.snapshot()
                with messages() as errors:Gui.runCommand(command);settle()
                self.assertTrue(any(kind in e for e in errors),(command,errors))
                self.assertEqual(self.snapshot(),before);document.validate(self.doc)
        editing.edit_file(self.doc);self.select(a);Gui.Selection.addSelection(self.doc.Name,b.Name)
        before=self.snapshot()
        with messages() as errors:Gui.runCommand('Part_Cut');settle()
        self.assertTrue(any('Edit a component' in e for e in errors),errors)
        self.assertEqual(self.snapshot(),before)

    def test_commands_preserve_input_ownership_undo_history_and_save(self):
        expected=[]
        for command,kind,volume in [('Part_Cut','Part::Cut',32),('Part_Common','Part::MultiCommon',32),('Part_Fuse','Part::MultiFuse',96)]:
            a,b=self.boxes();before_ids={o.Name:o.ID for o in self.doc.Objects}
            self.select(a);Gui.Selection.addSelection(self.doc.Name,b.Name)
            with messages() as errors:Gui.runCommand(command);settle()
            self.assertFalse(errors,errors)
            result=next(o for o in self.doc.Objects if o.Name not in before_ids)
            self.assertEqual(result.TypeId,kind);self.assertTrue(result.Shape.isValid())
            self.assertAlmostEqual(result.Shape.Volume,volume)
            self.assertTrue(all(o in self.child.Group for o in (a,b,result)))
            self.assertFalse(a.Visibility);self.assertFalse(b.Visibility)
            history=document.history(self.doc,self.child)
            self.assertLess(history.index(a),history.index(result));self.assertLess(history.index(b),history.index(result))
            name=result.Name;self.doc.undo();self.doc.recompute();settle()
            self.assertEqual({o.Name:o.ID for o in self.doc.Objects},before_ids)
            self.assertTrue(a.Visibility);self.assertTrue(b.Visibility)
            self.doc.redo();self.doc.recompute();settle();result=self.doc.getObject(name)
            document.validate(self.doc)
            expected.append({'result':name,'base':a.Name,'tool':b.Name,'volume':volume})
        document.save_document(self.doc,self.output/'PartBooleans.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':{o.Name:o.ID for o in self.doc.Objects},
            'definition':self.child.Name,'results':expected}))

    def choose(self,name,obj):
        tree=self.control(QtWidgets.QTreeWidget,name)
        for i in range(tree.topLevelItemCount()):
            parent=tree.topLevelItem(i)
            for j in range(parent.childCount()):
                item=parent.child(j);item.setCheckState(0,QtCore.Qt.Checked if item.data(0,QtCore.Qt.UserRole)==obj.Name else QtCore.Qt.Unchecked)

    def test_dialog_apply_rejects_foreign_input_then_accepts_owned_geometry(self):
        a,b=self.boxes();source=hierarchy.create_definition(self.doc,'Reference catalog')
        foreign,_=self.boxes(source);link=hierarchy.add_instance(self.child,source)
        display.set_state(self.child,link,part_type='Reference');settle()
        Gui.Selection.clearSelection();Gui.runCommand('Part_Boolean');settle()
        self.choose('firstShape',a);self.choose('secondShape',foreign)
        before=self.snapshot()
        with messages() as errors:self.task_button(QtWidgets.QDialogButtonBox.Apply)
        self.assertTrue(errors,errors);self.assertEqual(self.snapshot(),before)
        self.assertTrue(Gui.Control.activeDialog())
        self.choose('secondShape',b);self.control(QtWidgets.QRadioButton,'unionButton').setChecked(True)
        with messages() as errors:self.task_button(QtWidgets.QDialogButtonBox.Apply)
        self.assertFalse(errors,errors)
        result=next(o for o in self.doc.Objects if o.Name not in before[0])
        self.assertAlmostEqual(result.Shape.Volume,96);self.assertTrue(result.Shape.isValid())
        self.assertTrue(all(o in self.child.Group for o in (a,b,result)));document.validate(self.doc)
        Gui.Control.closeDialog();settle()

    def test_legacy_commands_and_dialog_bypass_component_policy(self):
        legacy=App.newDocument('LegacyPartBoolean')
        with patch.object(geometry,'require_part_boolean_inputs',side_effect=AssertionError('Legacy entered Plus')):
            for command,volume in [('Part_Cut',32),('Part_Common',32),('Part_Fuse',96)]:
                a,b=self.boxes(legacy);before=set(legacy.Objects)
                self.select(a);Gui.Selection.addSelection(legacy.Name,b.Name)
                with messages() as errors:Gui.runCommand(command);settle()
                self.assertFalse(errors,errors)
                result=next(o for o in legacy.Objects if o not in before)
                self.assertAlmostEqual(result.Shape.Volume,volume)
            a,b=self.boxes(legacy);Gui.Selection.clearSelection();Gui.runCommand('Part_Boolean');settle()
            self.choose('firstShape',a);self.choose('secondShape',b)
            self.control(QtWidgets.QRadioButton,'interButton').setChecked(True);before=set(legacy.Objects)
            with messages() as errors:self.task_button(QtWidgets.QDialogButtonBox.Apply)
            self.assertFalse(errors,errors)
            result=next(o for o in legacy.Objects if o not in before);self.assertAlmostEqual(result.Shape.Volume,32)
            Gui.Control.closeDialog();settle()

    def section_shapes(self, owner=None):
        Gui.activateWorkbench('PartWorkbench')
        owner = owner or self.child
        a=owner.newObject('Part::Box','SectionBase')
        a.Length=4;a.Width=4;a.Height=4
        material=a.ViewObject.ShapeAppearance[0];material.DiffuseColor=(0.2,0.4,0.6)
        a.ViewObject.ShapeAppearance=[material]
        b=owner.newObject('Part::Plane','SectionPlane')
        b.Length=4;b.Width=4;b.Placement.Base=App.Vector(0,0,2)
        owner.Document.recompute();settle()
        return a,b

    def test_section_command_rejection_preserves_state(self):
        a,b=self.section_shapes()
        source=hierarchy.create_definition(self.doc,'Reference section source')
        foreign,_=self.section_shapes(source);link=hierarchy.add_instance(self.child,source)
        path=hierarchy.subname((self.second,self.nested,link))+foreign.Name+'.'
        for kind in ('Reference','Excluded'):
            display.set_state(self.child,link,part_type=kind);settle()
            self.select(b);Gui.Selection.addSelection(self.doc.Name,self.root.Name,path)
            before=self.snapshot()
            with messages() as errors:Gui.runCommand('Part_Section');settle()
            self.assertTrue(any(kind in error for error in errors),errors)
            self.assertEqual(self.snapshot(),before)
        editing.edit_file(self.doc);self.select(a);Gui.Selection.addSelection(self.doc.Name,b.Name)
        before=self.snapshot()
        with messages() as errors:Gui.runCommand('Part_Section');settle()
        self.assertTrue(any('Edit a component' in error for error in errors),errors)
        self.assertEqual(self.snapshot(),before)

    def test_section_command_ownership_undo_and_save(self):
        a,b=self.section_shapes();ids={o.Name:o.ID for o in self.doc.Objects}
        self.select(a);Gui.Selection.addSelection(self.doc.Name,b.Name)
        with messages() as errors:Gui.runCommand('Part_Section');settle()
        self.assertFalse(errors,errors)
        result=next(o for o in self.doc.Objects if o.Name not in ids)
        self.assertEqual(result.TypeId,'Part::Section');self.assertTrue(result.Shape.isValid())
        self.assertAlmostEqual(result.Shape.Length,16)
        self.assertTrue(all(o in self.child.Group for o in (a,b,result)))
        self.assertEqual((result.Base,result.Tool),(a,b))
        history=document.history(self.doc,self.child)
        self.assertLess(history.index(a),history.index(result));self.assertLess(history.index(b),history.index(result))
        self.assertFalse(a.Visibility);self.assertFalse(b.Visibility)
        self.assertEqual(result.ViewObject.LineMaterial.DiffuseColor,a.ViewObject.ShapeAppearance[0].DiffuseColor)
        name=result.Name;self.doc.undo();self.doc.recompute();settle()
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},ids)
        self.assertTrue(a.Visibility);self.assertTrue(b.Visibility)
        self.doc.redo();self.doc.recompute();settle();result=self.doc.getObject(name)
        document.validate(self.doc);document.save_document(self.doc,self.output/'Section.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':{o.Name:o.ID for o in self.doc.Objects},
            'definition':self.child.Name,'result':name,'base':a.Name,'tool':b.Name}))

    def test_section_dialog_apply_and_undo(self):
        a,b=self.section_shapes();Gui.Selection.clearSelection();Gui.runCommand('Part_Boolean');settle()
        self.choose('firstShape',a);self.choose('secondShape',b)
        self.control(QtWidgets.QRadioButton,'sectionButton').setChecked(True)
        ids={o.Name:o.ID for o in self.doc.Objects}
        with messages() as errors:self.task_button(QtWidgets.QDialogButtonBox.Apply)
        self.assertFalse(errors,errors)
        result=next(o for o in self.doc.Objects if o.Name not in ids)
        self.assertEqual(result.TypeId,'Part::Section');self.assertAlmostEqual(result.Shape.Length,16)
        self.assertTrue(all(o in self.child.Group for o in (a,b,result)))
        document.validate(self.doc);Gui.Control.closeDialog();settle()
        self.doc.undo();self.doc.recompute();settle()
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},ids)

    def test_section_legacy_parenting_and_policy_bypass(self):
        legacy=App.newDocument('LegacySection');owner=legacy.addObject('App::Part','LegacyPart')
        a,b=self.section_shapes(owner);before=set(legacy.Objects)
        self.select(a);Gui.Selection.addSelection(legacy.Name,b.Name)
        with patch.object(geometry,'require_part_boolean_inputs',side_effect=AssertionError('Legacy entered Plus')):
            with messages() as errors:Gui.runCommand('Part_Section');settle()
        self.assertFalse(errors,errors)
        result=next(o for o in legacy.Objects if o not in before)
        self.assertTrue(a in owner.Group and b in owner.Group)
        self.assertNotIn(result,owner.Group)
        self.assertAlmostEqual(result.Shape.Length,16)
        self.assertEqual(result.ViewObject.LineMaterial.DiffuseColor,a.ViewObject.ShapeAppearance[0].DiffuseColor)


    def test_compound_rejection_preserves_state(self):
        a,b=self.boxes()
        source=hierarchy.create_definition(self.doc,'Compound source')
        foreign,_=self.boxes(source);link=hierarchy.add_instance(self.child,source)
        path=hierarchy.subname((self.second,self.nested,link))+foreign.Name+'.'
        for kind in ('Reference','Excluded','Full Component'):
            display.set_state(self.child,link,part_type=kind);settle()
            self.select(a);Gui.Selection.addSelection(self.doc.Name,self.root.Name,path)
            before=self.snapshot()
            with messages() as errors:Gui.runCommand('Part_Compound');settle()
            expected=kind if kind!='Full Component' else 'owned by the edited component'
            self.assertTrue(any(expected in error for error in errors),errors)
            self.assertEqual(self.snapshot(),before);document.validate(self.doc)
        editing.edit_file(self.doc);self.select(a)
        before=self.snapshot()
        with messages() as errors:Gui.runCommand('Part_Compound');settle()
        self.assertTrue(any('Edit a component' in error for error in errors),errors)
        self.assertEqual(self.snapshot(),before)

    def test_compound_ownership_order_undo_and_save(self):
        a,b=self.boxes();ids={o.Name:o.ID for o in self.doc.Objects}
        path=hierarchy.subname((self.second,self.nested))
        self.select(self.root,path+b.Name+'.Face1')
        Gui.Selection.addSelection(self.doc.Name,self.root.Name,path+b.Name+'.Face2')
        Gui.Selection.addSelection(self.doc.Name,self.root.Name,path+a.Name+'.')
        with messages() as errors:Gui.runCommand('Part_Compound');settle()
        self.assertFalse(errors,errors)
        result=next(o for o in self.doc.Objects if o.Name not in ids)
        self.assertEqual(result.TypeId,'Part::Compound');self.assertEqual(result.Links,[b,a])
        self.assertTrue(result.Shape.isValid());self.assertEqual(len(result.Shape.Solids),2)
        self.assertAlmostEqual(result.Shape.Volume,128)
        self.assertTrue(all(o in self.child.Group for o in (a,b,result)))
        self.assertEqual(document.owned_children(result),[])
        history=document.history(self.doc,self.child)
        self.assertLess(history.index(a),history.index(result));self.assertLess(history.index(b),history.index(result))
        self.assertFalse(a.Visibility);self.assertFalse(b.Visibility)
        name=result.Name;self.doc.undo();self.doc.recompute();settle()
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},ids)
        self.assertTrue(a.Visibility);self.assertTrue(b.Visibility)
        self.doc.redo();self.doc.recompute();settle();result=self.doc.getObject(name)
        self.assertEqual(result.Links,[b,a]);document.validate(self.doc)
        document.save_document(self.doc,self.output/'Compound.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':{o.Name:o.ID for o in self.doc.Objects},
            'definition':self.child.Name,'result':name,'base':a.Name,'tool':b.Name}))

    def test_compound_unused_single_input(self):
        editing.edit_unused(self.doc,self.unused)
        a,_=self.boxes(self.unused);ids={o.Name:o.ID for o in self.doc.Objects}
        self.select(a)
        with messages() as errors:Gui.runCommand('Part_Compound');settle()
        self.assertFalse(errors,errors)
        result=next(o for o in self.doc.Objects if o.Name not in ids)
        self.assertEqual(result.Links,[a]);self.assertTrue(result.Shape.isValid())
        self.assertAlmostEqual(result.Shape.Volume,64)
        self.assertTrue(a in self.unused.Group and result in self.unused.Group)
        self.assertIn(result,document.history(self.doc,self.unused));document.validate(self.doc)
        self.doc.undo();self.doc.recompute();settle()
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},ids)

    def test_compound_legacy_parenting_and_policy_bypass(self):
        legacy=App.newDocument('LegacyCompound');a,b=self.boxes(legacy)
        before=set(legacy.Objects);self.select(b);Gui.Selection.addSelection(legacy.Name,a.Name)
        with patch.object(geometry,'require_part_boolean_inputs',side_effect=AssertionError('Legacy entered Plus')):
            with messages() as errors:Gui.runCommand('Part_Compound');settle()
        self.assertFalse(errors,errors)
        result=next(o for o in legacy.Objects if o not in before)
        self.assertEqual(result.TypeId,'Part::Compound');self.assertEqual(result.Links,[b,a])
        self.assertIsNone(result.getParentGeoFeatureGroup())
        self.assertAlmostEqual(result.Shape.Volume,128);self.assertEqual(len(result.Shape.Solids),2)
        self.assertFalse(a.Visibility);self.assertFalse(b.Visibility)


    def editable_compound(self):
        a,b=self.boxes()
        result=self.child.newObject('Part::Compound','EditableCompound');result.Links=[a]
        self.doc.recompute();settle()
        return result,a,b

    def test_compound_links_drop_rejection_and_cleanup(self):
        result,a,b=self.editable_compound()
        source=hierarchy.create_definition(self.doc,'Link source')
        foreign,_=self.boxes(source);link=hierarchy.add_instance(self.child,source)
        path=hierarchy.subname((self.second,self.nested,link))+foreign.Name+'.'
        for kind in ('Reference','Excluded','Full Component'):
            display.set_state(self.child,link,part_type=kind);settle()
            before=self.snapshot();links=list(result.Links)
            self.assertFalse(result.ViewObject.canDropObject(foreign,self.root,path,[]))
            with self.assertRaises(Exception):result.ViewObject.dropObject(foreign,self.root,path,[])
            self.assertEqual(result.Links,links);self.assertEqual(self.snapshot(),before)
        # Same source identity through a Reference occurrence must still be rejected.
        display.set_state(self.root,self.first,part_type='Reference');settle()
        path=hierarchy.subname((self.first,self.nested))+b.Name+'.'
        self.assertFalse(result.ViewObject.canDropObject(b,self.root,path,[]))
        before=self.snapshot()
        with self.assertRaisesRegex(Exception,'Reference|Excluded'):result.ViewObject.dropObject(b,self.root,path,[])
        self.assertEqual(self.snapshot(),before)
        editing.edit_file(self.doc);before=self.snapshot()
        self.assertFalse(result.ViewObject.canDropObject(b))
        with self.assertRaisesRegex(Exception,'Edit a component'):result.ViewObject.dropObject(b)
        self.assertEqual(self.snapshot(),before)
        result.ViewObject.dragObject(a);self.doc.recompute();settle()
        self.assertEqual(result.Links,[]);self.assertIn(a,self.child.Group)

    def test_compound_links_drop_undo_save(self):
        result,a,b=self.editable_compound();ids={o.Name:o.ID for o in self.doc.Objects}
        path=hierarchy.subname((self.second,self.nested))+b.Name+'.'
        self.assertTrue(result.ViewObject.canDropObject(b,self.root,path,[]))
        self.assertFalse(result.ViewObject.canDragAndDropObject(b))
        self.doc.openTransaction('Add Compound input')
        result.ViewObject.dropObject(b,self.root,path,[]);self.doc.recompute();self.doc.commitTransaction();settle()
        self.assertEqual(result.Links,[a,b]);self.assertAlmostEqual(result.Shape.Volume,128)
        self.assertTrue(all(o in self.child.Group for o in (a,b,result)))
        self.assertFalse(b.Visibility);document.validate(self.doc)
        self.doc.undo();self.doc.recompute();settle()
        self.assertEqual(result.Links,[a]);self.assertTrue(b.Visibility)
        self.doc.redo();self.doc.recompute();settle()
        self.assertEqual(result.Links,[a,b]);self.assertEqual({o.Name:o.ID for o in self.doc.Objects},ids)
        document.save_document(self.doc,self.output/'CompoundLinks.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':ids,'definition':self.child.Name,
            'result':result.Name,'base':a.Name,'tool':b.Name}))

    def test_compound_links_replace_admission_and_undo(self):
        result,a,b=self.editable_compound()
        source=hierarchy.create_definition(self.doc,'Replacement source');foreign,_=self.boxes(source)
        before=self.snapshot()
        with self.assertRaises(Exception):result.ViewObject.replaceObject(a,foreign)
        self.assertEqual(result.Links,[a]);self.assertEqual(self.snapshot(),before)
        editing.edit((self.first,));before=self.snapshot()
        with self.assertRaisesRegex(Exception,'belong to the edited component'):result.ViewObject.replaceObject(a,b)
        self.assertEqual(self.snapshot(),before)
        editing.edit((self.second,self.nested));self.doc.openTransaction('Replace Compound input')
        self.assertEqual(result.ViewObject.replaceObject(a,b),1)
        self.doc.recompute();self.doc.commitTransaction();settle()
        self.assertEqual(result.Links,[b]);self.assertTrue(all(o in self.child.Group for o in (a,b,result)))
        document.validate(self.doc);self.doc.undo();self.doc.recompute();settle()
        self.assertEqual(result.Links,[a])

    def open_compound_links(self,result):
        objects=result if isinstance(result,list) else [result]
        self.select(objects[0])
        for obj in objects[1:]:Gui.Selection.addSelection(obj.Document.Name,obj.Name)
        QtTest.QTest.qWait(400)
        tabs=Gui.getMainWindow().findChild(QtWidgets.QTabWidget,'propertyTab')
        tabs.setCurrentIndex(1);settle()
        tree=Gui.getMainWindow().findChild(QtWidgets.QTreeView,'propertyEditorData')
        tree.show();tree.expandAll();settle()
        def find(parent=QtCore.QModelIndex()):
            model=tree.model()
            for row in range(model.rowCount(parent)):
                index=model.index(row,0,parent)
                if index.data()=='Links':return index.siblingAtColumn(1)
                child=find(index)
                if child.isValid():return child
            return QtCore.QModelIndex()
        index=find();self.assertTrue(index.isValid(),'Compound Links property missing')
        tree.scrollTo(index);tree.setCurrentIndex(index);tree.edit(index);settle()
        buttons=[w for w in tree.findChildren(QtWidgets.QPushButton) if w.isVisible()]
        self.assertTrue(buttons,'Links edit button missing');buttons[-1].click();settle()
        return next(w for w in Gui.getMainWindow().findChildren(QtWidgets.QDialog)
                    if 'DlgPropertyLink' in w.metaObject().className() and w.isVisible())

    def choose_compound_links(self,dlg,objects):
        tree=dlg.findChild(QtWidgets.QTreeWidget,'treeWidget')
        check=dlg.findChild(QtWidgets.QCheckBox,'checkObjectType')
        check.setChecked(False);settle()
        tree.clearSelection()
        found=set()
        def visit(item):
            name=bytes(item.data(0,QtCore.Qt.UserRole) or b'').decode()
            if name in {o.Name for o in objects}:
                item.setSelected(True);found.add(name)
            for n in range(item.childCount()):visit(item.child(n))
        for n in range(tree.topLevelItemCount()):
            root=tree.topLevelItem(n);root.setExpanded(True);visit(root)
        self.assertEqual(found,{o.Name for o in objects});settle()

    def test_compound_links_property_dialog_reject_continue_remove(self):
        result,a,b=self.editable_compound()
        source=hierarchy.create_definition(self.doc,'Property source');foreign,_=self.boxes(source)
        dlg=self.open_compound_links(result);self.choose_compound_links(dlg,[a,foreign]);before=self.snapshot()
        with messages() as errors:dlg.accept();settle()
        self.assertTrue(errors,errors);self.assertTrue(dlg.isVisible())
        self.assertEqual(result.Links,[a]);self.assertEqual(self.snapshot(),before)
        self.choose_compound_links(dlg,[a,b])
        with messages() as errors:dlg.accept();settle()
        self.assertFalse(errors,errors);self.assertFalse(dlg.isVisible())
        self.assertEqual(set(result.Links),{a,b});self.assertTrue(all(o in self.child.Group for o in (a,b,result)))
        self.doc.recompute();self.assertAlmostEqual(result.Shape.Volume,128);document.validate(self.doc)
        editing.edit_file(self.doc)
        dlg=self.open_compound_links(result);self.choose_compound_links(dlg,[a])
        with messages() as errors:dlg.accept();settle()
        self.assertFalse(errors,errors);self.assertEqual(result.Links,[a])

    def test_compound_links_multi_property_edit_is_atomic(self):
        result,a,b=self.editable_compound()
        foreign,_=self.boxes(self.unused)
        other=self.unused.newObject('Part::Compound','OtherCompound');other.Links=[foreign]
        self.doc.recompute();settle()
        dlg=self.open_compound_links([result,other]);self.choose_compound_links(dlg,[a,b])
        before=self.snapshot()
        with messages() as errors:dlg.accept();settle()
        self.assertTrue(errors,errors)
        self.assertEqual(result.Links,[a]);self.assertEqual(other.Links,[foreign])
        self.assertEqual(self.snapshot(),before);document.validate(self.doc)
        if dlg.isVisible():dlg.reject();settle()

    def test_compound_links_legacy_bypass(self):
        legacy=App.newDocument('LegacyCompoundLinks');a,b=self.boxes(legacy)
        result=legacy.addObject('Part::Compound','Compound');result.Links=[a];legacy.recompute();settle()
        with patch.object(geometry,'require_modeling_inputs',side_effect=AssertionError('Legacy entered Plus')):
            self.assertTrue(result.ViewObject.canDragAndDropObject(b))
            self.assertTrue(result.ViewObject.canDropObject(b));result.ViewObject.dropObject(b)
            self.assertEqual(result.Links,[a,b]);result.ViewObject.dragObject(b)
            self.assertEqual(result.ViewObject.replaceObject(a,b),1);self.assertEqual(result.Links,[b])
            dlg=self.open_compound_links(result);self.choose_compound_links(dlg,[a,b])
            with messages() as errors:dlg.accept();settle()
            self.assertFalse(errors,errors);self.assertEqual(set(result.Links),{a,b})
        legacy.recompute();self.assertAlmostEqual(result.Shape.Volume,128)



def verify_fresh_process(output):
    folder=Path(output)/'test_commands_preserve_input_ownership_undo_history_and_save'
    expected=json.loads((folder/'expected.json').read_text())
    doc=document.open_document(folder/'PartBooleans.cadprt')
    try:
        assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
        definition=doc.getObject(expected['definition'])
        for case in expected['results']:
            result=doc.getObject(case['result']);a=doc.getObject(case['base']);b=doc.getObject(case['tool'])
            assert all(o in definition.Group for o in (a,b,result))
            assert abs(result.Shape.Volume-case['volume'])<1e-7
            a.Height=6;b.Height=6;doc.recompute()
            assert result.Shape.isValid() and abs(result.Shape.Volume-case['volume']*1.5)<1e-7
        document.validate(doc)
    finally:App.closeDocument(doc.Name)


def verify_section_fresh_process(output):
    folder=Path(output)/'test_section_command_ownership_undo_and_save'
    expected=json.loads((folder/'expected.json').read_text())
    doc=document.open_document(folder/'Section.cadprt')
    try:
        assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
        owner=doc.getObject(expected['definition']);result=doc.getObject(expected['result'])
        a=doc.getObject(expected['base']);b=doc.getObject(expected['tool'])
        assert all(o in owner.Group for o in (a,b,result))
        assert result.Base==a and result.Tool==b and abs(result.Shape.Length-16)<1e-7
        a.Length=3;doc.recompute();document.validate(doc)
        assert result.Shape.isValid() and abs(result.Shape.Length-14)<1e-7
    finally:App.closeDocument(doc.Name)


def verify_compound_fresh_process(output):
    folder=Path(output)/'test_compound_ownership_order_undo_and_save'
    expected=json.loads((folder/'expected.json').read_text())
    doc=document.open_document(folder/'Compound.cadprt')
    try:
        assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
        owner=doc.getObject(expected['definition']);result=doc.getObject(expected['result'])
        a=doc.getObject(expected['base']);b=doc.getObject(expected['tool'])
        assert all(o in owner.Group for o in (a,b,result))
        assert result.Links==[b,a] and abs(result.Shape.Volume-128)<1e-7
        a.Height=6;doc.recompute();document.validate(doc)
        assert result.Shape.isValid() and len(result.Shape.Solids)==2
        assert abs(result.Shape.Volume-160)<1e-7
        assert result.Links==[b,a] and all(o in owner.Group for o in (a,b,result))
    finally:App.closeDocument(doc.Name)


def verify_compound_links_fresh_process(output):
    folder=Path(output)/'test_compound_links_drop_undo_save'
    expected=json.loads((folder/'expected.json').read_text())
    doc=document.open_document(folder/'CompoundLinks.cadprt')
    try:
        assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
        owner=doc.getObject(expected['definition']);result=doc.getObject(expected['result'])
        a=doc.getObject(expected['base']);b=doc.getObject(expected['tool'])
        assert result.Links==[a,b] and all(o in owner.Group for o in (a,b,result))
        assert abs(result.Shape.Volume-128)<1e-7
        b.Height=6;doc.recompute();document.validate(doc)
        assert result.Shape.isValid() and abs(result.Shape.Volume-160)<1e-7
        assert result.Links==[a,b]
    finally:App.closeDocument(doc.Name)
