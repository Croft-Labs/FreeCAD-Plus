# SPDX-License-Identifier: LGPL-2.1-or-later
import unittest
import FreeCAD as App, FreeCADGui as Gui, Part
from PySide6 import QtCore, QtGui, QtWidgets, QtTest
from freecad_plus import document, hierarchy, editing, panel, display, derived_geometry as derived, clone_task
from TestDerivedGeometry import TestDerivedGeometry


class TestClonePicking(unittest.TestCase):
    setUp = TestDerivedGeometry.setUp
    tearDown = TestDerivedGeometry.tearDown
    ref = TestDerivedGeometry.ref
    snapshot = TestDerivedGeometry.snapshot

    def pick(self, obj, element, link=None, remove=False):
        from freecad_plus.selection_list import pick_intent
        link = link or self.link
        sub = hierarchy.subname((self.top, link)) + self.ref(obj, link)[1] + element
        with pick_intent(remove):Gui.Selection.addSelection(self.doc.Name, self.root.Name, sub)
        QtTest.QTest.qWait(120)

    def test_face_edge_picks_promote_whole_sources_and_deduplicate(self):
        before = self.snapshot();task = clone_task.show()
        self.pick(self.body, 'Face1');self.pick(self.base, 'Face2');self.pick(self.body, 'Edge1')
        self.pick(self.sheet, 'Face1');self.pick(self.sketch, 'Edge1')
        self.assertEqual(task.refs, [self.ref(self.body), self.ref(self.sheet), self.ref(self.sketch)])
        self.assertEqual(task.form.objects.topLevelItemCount(), 3)
        self.pick(self.base, 'Face1', remove=True)
        self.assertEqual(task.refs, [self.ref(self.sheet), self.ref(self.sketch)])
        task.reject();self.assertEqual(self.snapshot(), before)

    def test_actual_viewport_face_click_adds_body_without_browser(self):
        self.sheet.Visibility=False;self.sketch.Visibility=False
        view=Gui.activeDocument().activeView();view.setCameraType('Orthographic')
        view.setAnimationEnabled(False);view.viewTop()
        task=clone_task.show();view.fitAll();QtTest.QTest.qWait(200)
        point=Part.getShape(*self.ref(self.body),needSubElement=True).BoundBox.Center
        point.z+=3
        screen=view.getPointOnScreen(point);widget=view.graphicsView().viewport();ratio=widget.devicePixelRatioF()
        position=QtCore.QPoint(round(screen[0]/ratio),widget.height()-1-round(screen[1]/ratio))
        move=QtGui.QMouseEvent(QtCore.QEvent.MouseMove,QtCore.QPointF(position),QtCore.QPointF(widget.mapToGlobal(position)),
                              QtCore.Qt.NoButton,QtCore.Qt.NoButton,QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(widget,move);QtTest.QTest.qWait(80)
        QtTest.QTest.mouseClick(widget,QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,position);QtTest.QTest.qWait(180)
        self.assertEqual(task.refs,[self.ref(self.body)],task.form.status.text())
        task.form.grab().save(str(self.out/'viewport-clone.png'))
        task.reject()

    def test_repeated_occurrence_keeps_placement_and_one_undo(self):
        second = hierarchy.add_instance(self.owner, self.child, App.Placement(App.Vector(100, 0, 0), App.Rotation()))
        task = clone_task.show();self.pick(self.body, 'Face1');self.pick(self.body, 'Face1', second)
        self.assertEqual(task.refs, [self.ref(self.body), self.ref(self.body, second)])
        undo = self.doc.UndoCount
        self.assertTrue(task.accept());results = task.results
        self.assertEqual(self.doc.UndoCount, undo + 1)
        self.assertNotEqual(results[0].Shape.BoundBox.Center, results[1].Shape.BoundBox.Center)
        self.assertTrue(all(r.SourceObject == self.body for r in results))
        names = [r.Name for r in results]
        self.doc.undo();self.assertTrue(all(self.doc.getObject(name) is None for name in names))

    def test_direct_child_boundary_and_excluded_guard_remain(self):
        nested = hierarchy.create_definition(self.doc, 'Nested source')
        link = hierarchy.add_instance(self.child, nested)
        with document.transaction(self.doc, 'Nested geometry'):
            box = nested.newObject('Part::Box', 'NestedBox')
        prefix = self.link.Name + '.' + link.Name + '.' + box.Name + '.Face1'
        with self.assertRaises(ValueError):derived.canonical(self.doc, self.owner, (self.top,), self.owner, prefix)
        with self.assertRaises(ValueError):derived.canonical(self.doc, self.owner, (self.top,), self.base, 'Face1')
        display.set_state(self.owner, self.link, part_type='Reference')
        self.assertEqual(derived.canonical(self.doc, self.owner, (self.top,), self.link, self.ref(self.body)[1]+'Face1'), self.ref(self.body))
        display.set_state(self.owner, self.link, part_type='Excluded')
        with self.assertRaisesRegex(ValueError, 'Excluded'):
            derived.canonical(self.doc, self.owner, (self.top,), self.link, self.ref(self.body)[1]+'Face1')

    def test_unplaced_assembly_text_and_relative_nested_edit(self):
        with document.transaction(self.doc, 'Unplace assembly'):
            self.doc.removeObject(self.top.Name)
        editing.edit_in_assembly(self.doc, self.owner)
        self.dock.activate_assembly(self.owner);self.dock.refresh()
        rows = [i for i in self.dock._maps[1].values() if i.data(0, panel._ROLE).kind == 'occurrence']
        self.assertTrue(rows)
        self.assertTrue(all(i.foreground(0).style() == QtCore.Qt.NoBrush for i in rows))
        task = clone_task.show();task.pick(self.owner, self.link.Name+'.'+self.ref(self.sheet)[1]+'Face1')
        self.assertEqual(task.refs, [self.ref(self.sheet)]);task.reject()
        leaf = hierarchy.create_definition(self.doc, 'Leaf source')
        nested = hierarchy.add_instance(self.child, leaf)
        with document.transaction(self.doc, 'Leaf geometry'):
            box = leaf.newObject('Part::Box', 'LeafBox')
        editing.edit_in_assembly(self.doc, self.owner, (self.link,))
        task = clone_task.show()
        task.pick(self.owner, hierarchy.subname((self.link, nested, box))+'Face1')
        self.assertEqual(task.refs, [(nested, box.Name+'.')]);task.reject()

    def test_extract_still_requires_parent_owned_faces(self):
        with self.assertRaisesRegex(ValueError, 'parent-owned'):
            derived.canonical(self.doc, self.owner, (self.top,), self.link, self.ref(self.sheet)[1]+'Face1', True)
        result = derived.save(self.doc, [self.ref(self.body)])[0]
        self.assertEqual(derived.canonical(self.doc, self.owner, (self.top,), result, 'Face1', True), (result, 'Face1'))
