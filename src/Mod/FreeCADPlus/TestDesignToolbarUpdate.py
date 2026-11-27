# SPDX-License-Identifier: LGPL-2.1-or-later
"""Design ribbon entries preserve native Part controls and component routing."""
import os
import unittest
from pathlib import Path
import FreeCAD as App,FreeCADGui as Gui
from PySide6 import QtCore,QtGui,QtWidgets,QtTest
from freecad_plus import document,editing,hierarchy,panel,toolbars,ui_modes,appearance_command,appearance_task,appearance,external

def settle():Gui.updateGui();QtTest.QTest.qWait(150)

class TestDesignToolbarUpdate(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench('PartDesignWorkbench');ui_modes.apply_modes()
        self.doc=document.new_document('ToolbarUpdate');self.owner=document.validate(self.doc).Definitions[0]
        self.box=self.owner.newObject('Part::Box','Housing');self.doc.recompute();settle()
        self.r=toolbars._controller
        self.tab('Modeling')

    def tearDown(self):
        if appearance_task._active:appearance_task._active.reject()
        for name in list(App.listDocuments()):App.closeDocument(name)
        App.ParamGet('User parameter:BaseApp/Preferences/General').SetInt('ToolbarUIMode',0)
        ui_modes.apply_modes();settle()

    def tab(self,name):
        self.r.select_tab(next(i for i,(label,_) in enumerate(self.r.tabs) if label==name));settle()

    def commands(self,parent):
        return [c for b in parent.findChildren(QtWidgets.QToolButton) for c in b.property('PlusCommands') or []]

    def boolean_signature(self):
        group=self.r.scroll.widget().findChild(QtWidgets.QWidget,'PlusGroup_Boolean Tools')
        self.assertIsNotNone(group)
        grid=group.layout().itemAt(0).layout();result=[]
        for i in range(grid.count()):
            button=grid.itemAt(i).widget();self.assertIsInstance(button,QtWidgets.QToolButton)
            action=button.defaultAction();self.assertIsNotNone(action)
            result.append((grid.getItemPosition(i),button.objectName(),button.iconSize(),
                           action.text(),button.popupMode(),button.width(),
                           [a.text() for a in button.menu().actions()] if button.menu() else []))
        return result

    def test_00_boolean_group_exactly_matches_part_and_survives_reload(self):
        self.assertEqual(Gui.activeWorkbench().name(),'PartDesignWorkbench')
        cold=self.boolean_signature();self.assertEqual(len(cold),9)
        undo=self.doc.UndoCount;objects=[o.ID for o in self.doc.Objects]
        self.tab('Part');part=self.boolean_signature();self.assertEqual(cold,part)
        self.tab('Modeling');self.assertEqual(self.boolean_signature(),part)
        self.r.refresh();settle();self.assertEqual(self.boolean_signature(),part)
        self.assertEqual(self.doc.UndoCount,undo);self.assertEqual([o.ID for o in self.doc.Objects],objects)
        out=Path(os.environ['PLUS_TEST_DIR'])
        self.r.scroll.widget().findChild(QtWidgets.QWidget,'PlusGroup_Boolean Tools').grab().save(str(out/'modeling-boolean.png'))
        self.r.bar.grab().save(str(out/'modeling.png'))
        self.tab('Part');self.r.scroll.widget().findChild(QtWidgets.QWidget,'PlusGroup_Boolean Tools').grab().save(str(out/'part-boolean.png'))

    def test_home_tabs_common_and_sheep(self):
        self.assertNotIn('All Tools',[t for t,_ in self.r.tabs]);self.tab('Home')
        self.assertEqual(set(self.commands(self.r.scroll.widget())),{'Part_CheckGeometry','Std_Part','Std_Group','Std_VarSet','Std_DlgMacroRecord','Std_DlgMacroExecute','Std_DlgMacroExecuteDirect','Std_WhatsThis'})
        common=self.commands(self.r.common)
        i=common.index('Std_Save');self.assertEqual(common[i:i+4],['Std_Save','Std_SaveAll','Std_SaveAs','Std_Part'])
        self.r.bar.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'home.png'))
        self.tab('Modeling');clone=self.r.scroll.widget().findChild(QtWidgets.QToolButton,'Plus_Plus_Clone')
        self.assertEqual(clone.icon().pixmap(32,32).toImage(),Gui.getIcon('PartDesign_Clone').pixmap(32,32).toImage())

    def test_new_component_buttons_dispatch_native_command_once(self):
        for place in ('common','Assembly'):
            self.tab('Assembly' if place=='Assembly' else 'Home')
            parent=self.r.scroll.widget() if place=='Assembly' else self.r.common
            button=parent.findChild(QtWidgets.QToolButton,'Plus_Std_Part')
            self.assertIs(button.defaultAction(),Gui.Command.get('Std_Part').getAction()[0])
            before=len(document.validate(self.doc).Definitions);button.click();settle()
            self.assertEqual(len(document.validate(self.doc).Definitions),before+1)
        self.tab('Assembly');self.r.bar.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'assembly.png'))

    def test_appearance_faces_apply_and_empty_selection(self):
        Gui.Selection.clearSelection();Gui.Selection.addSelection(self.box,'Face2');settle()
        button=self.r.scroll.widget().findChild(QtWidgets.QToolButton,'Plus_Plus_Appearance')
        self.assertTrue(appearance_command.Command().IsActive());button.click();settle()
        task=appearance_task._active;self.assertIsNotNone(task)
        self.assertEqual(task.form.targets,[(panel.identity(self.box),'Face2')])
        before=appearance.materials(self.box);undo=self.doc.UndoCount
        task.form.value.setValue(35);self.assertTrue(task.apply());task.reject()
        self.assertEqual(self.doc.UndoCount,undo+1)
        self.assertAlmostEqual(appearance.materials(self.box)[1].Transparency,.35,places=5)
        self.assertAlmostEqual(appearance.materials(self.box)[0].Transparency,before[0].Transparency,places=5)
        Gui.Selection.clearSelection();Gui.runCommand('Plus_Appearance');settle()
        self.assertFalse(appearance_task._active.form.targets)
        self.assertFalse(appearance_command.Command().IsActive())

    def test_appearance_active_child_import_and_unavailable_context(self):
        child=hierarchy.create_definition(self.doc,'Child');shape=child.newObject('Part::Box','ChildBox')
        link=hierarchy.add_child(self.owner,child);self.doc.recompute()
        editing.edit((document.validate(self.doc).Group[0],link));self.assertEqual(appearance_command.target(),child)
        editing.edit_file(self.doc);self.assertFalse(appearance_command.Command().IsActive())
        source=self.doc;document.save_document(source,Path(os.environ['PLUS_TEST_DIR'])/'toolbar-source.cadprt')
        host=document.new_document('ToolbarHost');host_owner=document.validate(host).Definitions[0]
        host_owner.Label='Host component';document.save_document(host,Path(os.environ['PLUS_TEST_DIR'])/'toolbar-host.cadprt')
        external.import_file(host,source);imported=hierarchy.add_child(host_owner,child)
        editing.edit((document.validate(host).Group[0],imported));self.assertEqual(appearance_command.target(),child)
        Gui.Selection.clearSelection();Gui.Selection.addSelection(shape,'Face1');Gui.runCommand('Plus_Appearance');settle()
        task=appearance_task._active;self.assertEqual(task.owner_ref,panel.identity(child))
        self.assertEqual(task.form.targets,[(panel.identity(shape),'Face1')]);task.reject()
        App.newDocument('Legacy');self.assertFalse(appearance_command.Command().IsActive())

    def test_other_modes_and_classic_remain_unchanged(self):
        original=[(b,b.parentWidget(),list(b.actions())) for b in self.r.native_bars()]
        prefs=App.ParamGet('User parameter:BaseApp/Preferences/General');prefs.SetInt('ToolbarUIMode',1)
        ui_modes.apply_modes();settle();self.assertTrue(self.r.bar.isHidden())
        for bar,parent,actions in original:
            self.assertEqual(bar.parentWidget(),parent);self.assertEqual(bar.actions(),actions)
        prefs.SetInt('ToolbarUIMode',0);ui_modes.apply_modes()
        Gui.activateWorkbench('DraftWorkbench');self.r.refresh();settle()
        self.assertIn('All Tools',[t for t,_ in self.r.tabs])
        self.assertNotIn('Std_Part',self.commands(self.r.common))
