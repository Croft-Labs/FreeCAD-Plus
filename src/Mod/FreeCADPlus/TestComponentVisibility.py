# SPDX-License-Identifier: LGPL-2.1-or-later
"""Per-view explicit hiding; no fading or Bodies Only acceptance is claimed."""
import json
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, display, editing, hierarchy, panel, isolation
import TestComponentPanel as fixtures
from TestUnusedModels import visibility
settle=fixtures.settle

class TestComponentVisibility(unittest.TestCase):
    setUp=fixtures.TestComponentPanel.setUp
    tearDown=fixtures.TestComponentPanel.tearDown
    rows=fixtures.TestComponentPanel.rows
    occurrence=fixtures.TestComponentPanel.occurrence

    def view(self):return Gui.activeDocument().activeView()
    def hit(self,view,x):return view.getObjectInfoRay(App.Vector(x+.3,.2,20),App.Vector(0,0,-1))
    def row(self,path):return self.occurrence(path).data(0,panel._ROLE)

    def test_native_hiding_is_view_local_and_clears(self):
        editing.edit_file(self.doc);settle();view=self.view()
        self.assertTrue(hasattr(view,'setComponentHiddenPaths'))
        self.assertIsNotNone(self.hit(view,0));self.assertIsNotNone(self.hit(view,25))
        ids={o.Name:o.ID for o in self.doc.Objects};vis=visibility(self.doc);undo=self.doc.UndoCount
        display.set_state(self.root,self.first,part_type='Excluded');settle()
        self.assertIsNone(self.hit(view,0));self.assertIsNotNone(self.hit(view,25))
        other=self.widget.open_row(self.row((self.first,)));settle()
        self.assertIsNotNone(self.hit(other,0));self.assertIsNone(self.hit(view,0))
        self.assertIsNotNone(self.hit(other,25));self.assertIsNotNone(self.hit(view,25))
        self.assertEqual(visibility(self.doc),vis);self.assertEqual({o.Name:o.ID for o in self.doc.Objects},ids)
        self.assertEqual(self.doc.UndoCount,undo+1)
        self.widget.close();settle()
        self.assertIsNotNone(self.hit(view,0));self.assertIsNotNone(self.hit(other,0))
        for current in (view,other):
            names=[str(current.getSceneGraph().getChild(i).getName()) for i in range(current.getSceneGraph().getNumChildren())]
            self.assertNotIn('PlusVisibilityContext',names)

    def test_filtered_view_close_preserves_other_view_and_reopen(self):
        editing.edit_file(self.doc);settle();view=self.view()
        display.set_state(self.root,self.first,shown=False);settle()
        other=self.widget.open_row(self.row((self.first,)));settle()
        self.assertIsNone(self.hit(view,0));self.assertIsNotNone(self.hit(other,0))
        area=Gui.getMainWindow().findChild(QtWidgets.QMdiArea)
        window=next(w for w in area.subWindowList() if w.isAncestorOf(view.graphicsView()))
        window.close();settle()
        self.assertEqual(len(self.widget._states),1)
        self.assertIsNotNone(self.hit(other,0));self.assertIsNotNone(self.hit(other,25))
        # A fresh unfiltered native view must not inherit a destroyed view's key.
        self.widget.close();settle();Gui.activeDocument().createView('Gui::View3DInventor');settle()
        fresh=self.view();self.assertIsNotNone(self.hit(fresh,0));self.assertIsNotNone(self.hit(fresh,25))

    def test_hidden_excluded_reference_context_and_undo(self):
        editing.edit((self.second,));settle();view=self.view();vis=visibility(self.doc)
        display.set_state(self.parent,self.nested,shown=False);settle()
        self.assertIsNone(self.hit(view,0));self.assertIsNone(self.hit(view,25))
        self.doc.undo();self.doc.recompute();settle();self.assertIsNotNone(self.hit(view,25))
        display.set_state(self.parent,self.nested,part_type='Reference');settle()
        self.assertIsNone(self.hit(view,0));self.assertIsNotNone(self.hit(view,25))
        editing.edit_file(self.doc);settle()
        self.assertIsNone(self.hit(view,0));self.assertIsNone(self.hit(view,25))
        editing.edit((self.first,));settle();self.assertIsNotNone(self.hit(view,0));self.assertIsNone(self.hit(view,25))
        self.assertEqual(display.state(self.nested),('Reference',True));self.assertEqual(visibility(self.doc),vis)
        display.set_state(self.parent,self.nested,part_type='Excluded');settle();self.assertIsNone(self.hit(view,0))
        with self.assertRaisesRegex(ValueError,'Excluded'):display.set_state(self.parent,self.nested,shown=True)
        editing.edit((self.first,self.nested));settle();self.assertIsNotNone(self.hit(view,0))

    def test_native_validation_recompute_and_persistence(self):
        editing.edit_file(self.doc);settle();view=self.view();vis=visibility(self.doc)
        display.set_state(self.root,self.first,shown=False);settle();self.assertIsNone(self.hit(view,0))
        with self.assertRaises(ValueError):view.setComponentHiddenPaths(self.root,['Missing.'])
        self.assertIsNone(self.hit(view,0))
        self.pad.Length=7;self.doc.recompute();settle();self.assertIsNone(self.hit(view,0));self.assertIsNotNone(self.hit(view,25))
        document.save_document(self.doc,self.output/'Visibility.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':{o.Name:o.ID for o in self.doc.Objects},'visibility':vis,'first':self.first.Name,'pad':self.pad.Name}))
        display.set_state(self.root,self.first,shown=True);settle();self.assertIsNotNone(self.hit(view,0))
        self.widget.close();settle();view.setComponentHiddenPaths(self.root,[self.second.Name+'.'])
        self.assertIsNone(self.hit(view,25));view.setComponentHiddenPaths();self.assertIsNotNone(self.hit(view,25))
        self.assertEqual(visibility(self.doc),vis)

    def test_unused_isolation_restores_filtered_assembly_and_idle(self):
        editing.edit_file(self.doc);settle();view=self.view()
        display.set_state(self.root,self.first,shown=False);settle()
        other=self.widget.open_row(self.row((self.second,)));settle()
        editing.edit_unused(self.doc,self.unused);settle();self.assertIsNotNone(isolation.current(other))
        self.assertIsNone(self.hit(other,0));self.assertIsNone(self.hit(other,25))
        self.assertIsNone(self.hit(view,0));self.assertIsNotNone(self.hit(view,25))
        editing.edit_file(self.doc);settle();self.assertIsNone(self.hit(other,0));self.assertIsNotNone(self.hit(other,25))
        self.assertIsNone(self.hit(view,0));self.assertIsNotNone(self.hit(view,25))
        count=self.widget.refresh_count;QtTest.QTest.qWait(250);self.assertEqual(self.widget.refresh_count,count)

def verify_fresh_process(output):
    folder=Path(output)/'test_native_validation_recompute_and_persistence'
    expected=json.loads((folder/'expected.json').read_text());doc=document.open_document(folder/'Visibility.cadprt')
    widget=None
    try:
        assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
        assert visibility(doc)==expected['visibility'] and doc.getObject(expected['pad']).Length.Value==7
        widget=panel.show_panel();editing.edit_file(doc);settle();view=Gui.activeDocument().activeView()
        assert view.getObjectInfoRay(App.Vector(.3,.2,20),App.Vector(0,0,-1)) is None
        assert view.getObjectInfoRay(App.Vector(25.3,.2,20),App.Vector(0,0,-1)) is not None
        widget.close();settle()
        assert view.getObjectInfoRay(App.Vector(.3,.2,20),App.Vector(0,0,-1)) is not None
    finally:
        if widget:widget.close()
        App.closeDocument(doc.Name)
