# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native component naming scopes, mutation guards and persistence."""
import json
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtTest
from freecad_plus import (assembly, component_add, document, editing, external,
                         hierarchy, naming, panel, part_transfer_ops)


class TestComponentNames(unittest.TestCase):
    def setUp(self):
        self.before = set(App.listDocuments())
        self.out = Path(os.environ['PLUS_TEST_DIR']) / self._testMethodName
        self.out.mkdir(exist_ok=True)
        naming.install()

    def tearDown(self):
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)
        QtTest.QTest.qWait(50)

    def file(self, name, label=None):
        doc = document.new_document(name)
        root = document.validate(doc)
        root.Definitions[0].Label = label or name
        document.save_document(doc, self.out/(name+'.cadprt'))
        return doc, root, root.Definitions[0]

    def state(self, doc):
        return (doc.UndoCount, [(o.Name,o.ID,o.Label,str(o.Placement) if hasattr(o,'Placement') else '',
                [(x.Document.Name,x.Name) for x in o.OutList]) for o in doc.Objects])

    def force_label(self, obj, label):
        naming._observer.reverting = True
        try: obj.Label = label
        finally: naming._observer.reverting = False

    def test_local_create_rename_case_and_unicode(self):
        doc,root,part=self.file('CaseScope','Machine')
        bolt=hierarchy.create_definition(doc,'Café')
        before=self.state(doc)
        for label in ('MACHINE',' machine ','Cafe\u0301',' '):
            with self.assertRaisesRegex(ValueError,'unique within this file'):
                hierarchy.create_definition(doc,label)
        self.assertEqual(self.state(doc),before)
        with self.assertRaises(ValueError):hierarchy.rename_definition(bolt,'machine')
        self.assertEqual(self.state(doc),before)
        hierarchy.rename_definition(bolt,'Fastener')
        doc.undo();self.assertEqual(bolt.Label,'Café')
        doc.redo();self.assertEqual(bolt.Label,'Fastener')

    def test_import_collision_reports_both_files_before_mutation(self):
        host,hr,h=self.file('Host','Bolt')
        source,sr,s=self.file('Hardware','bolt')
        before=self.state(host);src=self.state(source)
        with self.assertRaisesRegex(ValueError,'Hardware.cadprt') as failure:
            external.import_file(host,source)
        self.assertIn('Host.cadprt',str(failure.exception))
        self.assertEqual(self.state(host),before);self.assertEqual(self.state(source),src)

    def test_two_imports_collide_even_when_unused_or_nested(self):
        host,hr,h=self.file('Host')
        a,ar,ap=self.file('A','Bolt');b,br,bp=self.file('B','bolt')
        external.import_file(host,a);before=self.state(host)
        with self.assertRaises(ValueError):external.import_file(host,b)
        self.assertEqual(self.state(host),before)
        wrapper,wr,wp=self.file('Wrapper');external.import_file(wrapper,b);document.save_document(wrapper)
        with self.assertRaises(ValueError):external.import_file(host,wrapper)
        self.assertEqual(self.state(host),before)

    def test_batch_collisions_are_preflighted_together(self):
        host,hr,h=self.file('Host');a,ar,ap=self.file('A','Bolt');b,br,bp=self.file('B','bolt')
        before=self.state(host)
        with self.assertRaises(ValueError):hierarchy.add_children(h,[ap,bp])
        self.assertEqual(self.state(host),before);self.assertEqual(hr.Imports,[])

    def test_same_definition_instances_and_diamond_imports_are_valid(self):
        source,sr,s=self.file('Source','Bolt');left,lr,l=self.file('Left');right,rr,r=self.file('Right')
        external.import_file(left,source);external.import_file(right,source)
        document.save_document(left);document.save_document(right)
        host,hr,h=self.file('Host');external.import_file(host,left);external.import_file(host,right)
        links=hierarchy.add_children(h,[s,s]);self.assertEqual(len(links),1)
        more=hierarchy.add_instance(h,s);self.assertEqual(more.LinkedObject,links[0].LinkedObject)
        naming.validate_for_save(host);document.save_document(host)

    def test_reverse_importers_block_source_rename_and_creation(self):
        source,sr,s=self.file('Source','Bolt');host,hr,h=self.file('Host','Motor')
        external.import_file(host,source);before=self.state(source)
        with self.assertRaises(ValueError):hierarchy.rename_definition(s,'MOTOR')
        with self.assertRaises(ValueError):hierarchy.create_definition(source,'motor')
        self.assertEqual(self.state(source),before)
        other,orr,o=self.file('Unrelated','Screw')
        hierarchy.rename_definition(s,'Screw') # Unrelated open files are not one scope.
        self.assertEqual(s.Label,o.Label)

    def test_native_label_edit_is_rejected_and_valid_rename_shared(self):
        source,sr,s=self.file('Source','Bolt');host,hr,h=self.file('Host','Motor')
        external.import_file(host,source);link=hierarchy.add_instance(h,s)
        s.Label='motor';self.assertEqual(s.Label,'Bolt')
        s.Label='Screw';self.assertEqual(link.LinkedObject.Label,'Screw')
        naming.validate_for_save(host)

    def test_generated_new_name_reserves_imports(self):
        host,hr,h=self.file('Host');source,sr,s=self.file('Hardware','Part001')
        external.import_file(host,source)
        App.setActiveDocument(host.Name);editing.edit((hr.Group[0],))
        picker=component_add.Picker(Gui.getMainWindow(),True)
        self.assertEqual(picker.name.text(),'Part002');picker.reject()
        created=hierarchy.new_part();self.assertEqual(created.Label,'Part002')

    def test_independent_copy_checks_imported_names(self):
        host,hr,h=self.file('Host');source,sr,s=self.file('Source','Bolt')
        external.import_file(host,source);before=self.state(host)
        with self.assertRaises(ValueError):external.copy_definition(s,host,'BOLT',placements_to_replace=())
        self.assertEqual(self.state(host),before)
        copied=external.copy_definition(s,host,'Spare bolt',placements_to_replace=())
        self.assertNotEqual(copied,s);naming.validate_for_save(host)

    def test_legacy_conflict_is_repairable_but_native_saves_refuse_it(self):
        doc,root,part=self.file('Legacy','Motor')
        second=hierarchy.create_definition(doc,'Bolt');third=hierarchy.create_definition(doc,'Nut')
        self.force_label(second,'motor');self.force_label(third,'MOTOR')
        original=Path(doc.FileName).read_bytes()
        original_path,original_label=doc.FileName,doc.Label
        with self.assertRaises(Exception):doc.save()
        with self.assertRaises(Exception):doc.saveCopy(str(self.out/'InvalidCopy.cadprt'))
        with self.assertRaises(Exception):doc.saveAs(str(self.out/'InvalidAs.cadprt'))
        self.assertEqual((doc.FileName,doc.Label),(original_path,original_label))
        self.assertEqual(Path(doc.FileName).read_bytes(),original)
        self.assertFalse((self.out/'InvalidCopy.cadprt').exists())
        document.validate(doc) # Structural navigation must still work for repair.
        hierarchy.rename_definition(second,'Bolt')
        with self.assertRaises(ValueError):naming.validate_for_save(doc)
        hierarchy.rename_definition(third,'Nut');document.save_document(doc)

    def test_exact_tree_qualification_across_nested_sources(self):
        a,ar,part4=self.file('file_name_A','part_4')
        c,cr,part8=self.file('file_name_C','part_8')
        b,br,sub5=self.file('file_name_B','sub_assy_5');part7=hierarchy.create_definition(b,'part_7')
        external.import_file(b,c);hierarchy.add_children(sub5,[part7,part8]);document.save_document(b)
        host,hr,assy=self.file('open_file','assy_1');sub2=hierarchy.create_definition(host,'sub_assy_2');part3=hierarchy.create_definition(host,'part_3')
        external.import_file(host,a);external.import_file(host,b)
        hierarchy.add_children(assy,[sub2,sub5]);hierarchy.add_children(sub2,[part3,part4])
        App.setActiveDocument(host.Name);editing.edit((hr.Group[0],))
        dock=panel.show_panel();dock.activate_assembly(assy);dock.refresh()
        labels=[item.data(0,panel._ROLE).label for item in dock._maps[1].values()]
        for expected in ('assy_1','sub_assy_2','part_3','part_4 (file_name_A)','sub_assy_5 (file_name_B)','part_7 (file_name_B)','part_8 (file_name_C)'):
            self.assertIn(expected,labels)
        document.save_document(host)
        (self.out/'reopen.json').write_text(json.dumps({'host':host.FileName,'source':a.FileName,'part':part4.Name}))

    def test_export_unique_names_without_renaming_sources(self):
        a,ar,ap=self.file('A','Bolt');b,br,bp=self.file('B','bolt')
        destination=self.out/'Export.cadprt'
        part_transfer_ops.export_parts([ap,bp],destination)
        opened=document.open_document(destination)
        labels=[part.Label for part in document.validate(opened).Definitions]
        self.assertEqual(len({naming.key(label) for label in labels}),2)
        self.assertEqual((ap.Label,bp.Label),('Bolt','bolt'))
