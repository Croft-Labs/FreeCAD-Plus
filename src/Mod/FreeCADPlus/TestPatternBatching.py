# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native acceptance for batched pattern creation and retained relationships."""
import json
import cProfile
import pstats
import os
import time
import unittest
from pathlib import Path
import FreeCAD as App
import Part
import Sketcher
from PySide6 import QtOpenGLWidgets
import TestSketchPattern as fixtures
from freecad_plus import sketch_pattern as pattern


class TestPatternBatching(unittest.TestCase):
    setUp = fixtures.TestPatternGeometry.setUp
    tearDown = fixtures.TestPatternGeometry.tearDown

    def test_grid12_spacing_equal_edits_undo_and_save(self):
        s = self.s
        s.addGeometry(Part.Circle(App.Vector(5, 3, 0), App.Vector(0, 0, 1), 2))
        s.addConstraint(Sketcher.Constraint('Diameter', 0, 4.))
        before = s.DoF
        options = fixtures.linear(directions='Two directions',
                                  d1=fixtures.extent(count=12),
                                  d2=fixtures.extent(count=12, reference=(-2, 0)))
        start = time.perf_counter()
        copies = pattern.apply(s, [0], options, True)
        elapsed = time.perf_counter() - start
        self.assertEqual(len(copies), 143)
        self.assertEqual((s.GeometryCount, s.ConstraintCount), (287, 716))
        self.assertEqual(s.solve(), 0)
        self.assertEqual(s.DoF, before)
        self.doc.undo()
        self.assertEqual((s.GeometryCount, s.ConstraintCount), (1, 1))
        self.doc.redo()
        self.assertEqual((s.GeometryCount, s.ConstraintCount), (287, 716))
        helpers = {i for i in range(s.GeometryCount) if s.getConstruction(i)}
        self.assertEqual(len(helpers), 143)
        constraints = s.Constraints
        for i in copies:
            self.assertTrue(any(c.Type == 'Equal' and {c.First, c.Second} == {0, i}
                                for c in constraints))
        self.assertEqual(sum(c.Type == 'Equal' and c.First in helpers for c in constraints), 141)
        self.assertEqual(sum(c.Type == 'Parallel' and c.Second in helpers for c in constraints), 143)
        self.assertEqual(sum(c.Type == 'Coincident' and c.Second in helpers for c in constraints), 286)
        masters = [i for i, c in enumerate(constraints) if c.Type == 'Distance']
        self.assertEqual(len(masters), 2)
        self.doc.openTransaction('Edit original diameter and pitches')
        s.setDatum(0, App.Units.Quantity('6 mm'))
        s.setDatum(masters[0], App.Units.Quantity('11 mm'))
        s.setDatum(masters[1], App.Units.Quantity('13 mm'))
        self.doc.recompute()
        self.doc.commitTransaction()
        self.assertEqual(s.solve(), 0)
        self.assertEqual(s.DoF, before)
        origin = s.Geometry[0].Center
        for n, i in enumerate([0] + copies):
            g = s.Geometry[i]
            self.assertAlmostEqual(g.Radius, 3., places=6)
            self.assertLess((g.Center-origin-App.Vector((n//12)*11, (n%12)*13, 0)).Length, 1e-5)
        for c in s.Constraints:
            if c.Type == 'Coincident' and c.Second in helpers:
                self.assertLess((s.getPoint(c.First,c.FirstPos)-s.getPoint(c.Second,c.SecondPos)).Length,1e-5)
        for hidden in (True, False):
            pattern.set_chain_hidden(s, hidden)
            self.assertEqual(s.solve(), 0)
            self.assertEqual(s.DoF, before)
            self.assertEqual(pattern.chain_is_hidden(s), hidden)
        if os.environ.get('PLUS_TEST_DIR'):
            out = Path(os.environ['PLUS_TEST_DIR'])
            self.doc.saveAs(str(out/'grid12.FCStd'))
            (out/'grid12-timing.json').write_text(json.dumps(dict(seconds=elapsed,instances=144,
                helpers=143,constraints=716,equal_sizes=143,pitch_drivers=2),indent=2))

    def test_radial_and_two_point_direction_with_mixed_construction(self):
        self.s.addGeometry(Part.Circle(App.Vector(20,0,0),App.Vector(0,0,1),2))
        self.s.addGeometry(Part.LineSegment(App.Vector(0,0,0),App.Vector(10,0,0)),True)
        self.assertEqual(self.s.solve(),0)
        before = self.s.DoF
        copies=pattern.apply(self.s,[0,1],fixtures.linear(d1=fixtures.extent(
            method='Two points',start=(1,1),end=(1,2))),True)
        self.assertEqual([self.s.getConstruction(i) for i in copies],[False,True,False,True])
        self.assertEqual(self.s.solve(),0)
        self.assertEqual(self.s.DoF,before)
        self.doc.undo()
        copies=pattern.apply(self.s,[0],fixtures.circular(directions='Radial',
            radial=fixtures.extent(reference=(0,3),count=5,value=4)),True)
        self.assertEqual(self.s.solve(),0)
        self.assertEqual(self.s.DoF,before)
        datum=next(i for i,c in enumerate(self.s.Constraints) if c.Type=='Distance')
        self.s.setDatum(datum,App.Units.Quantity('6 mm'));self.doc.recompute()
        base=self.s.Geometry[0].Center
        for n,i in enumerate(copies,1):
            self.assertAlmostEqual((self.s.Geometry[i].Center-base).Length,n*6,places=5)
            self.assertAlmostEqual(self.s.Geometry[i].Radius,self.s.Geometry[0].Radius,places=6)

    def test_redundancy_fallback_preserves_source_and_rejects_conflict(self):
        self.s.addGeometry(Part.LineSegment(App.Vector(0,0,0),App.Vector(4,0,0)))
        self.s.addConstraint(Sketcher.Constraint('Horizontal',0))
        original=self.s.Constraints[0].dumpContent()
        batch=pattern._ConstraintBatch(self.s)
        batch.optional=[Sketcher.Constraint('Horizontal',0),Sketcher.Constraint('Distance',0,4.)]
        batch.flush()
        self.assertEqual(self.s.solve(),0)
        self.assertEqual(self.s.ConstraintCount,2)
        self.assertEqual(self.s.Constraints[0].dumpContent(),original)
        batch.optional=[Sketcher.Constraint('Distance',0,5.)]
        with self.assertRaisesRegex(ValueError,'conflict'):batch.flush()
        self.assertEqual(self.s.solve(),0)
        self.assertEqual(self.s.ConstraintCount,2)
        self.assertAlmostEqual(self.s.Geometry[0].length(),4.)


class TestPatternBatchingTask(unittest.TestCase):
    setUp = fixtures.TestPatternTask.setUp
    tearDown = fixtures.TestPatternTask.tearDown
    enter = fixtures.TestPatternTask.enter
    pick = fixtures.TestPatternTask.pick

    def test_grid12_apply_in_sketch_edit(self):
        from PySide6 import QtTest
        self.enter();self.pick(self.p.items,'Edge2')
        self.p.layout_mode.setCurrentText('Two directions')
        self.pick(self.p.d1.reference,'H_Axis');self.pick(self.p.d2.reference,'V_Axis')
        self.p.d1.count.setValue(12);self.p.d2.count.setValue(12)
        self.assertTrue(self.p.apply.isEnabled())
        profiler=cProfile.Profile();started=time.perf_counter();profiler.enable()
        self.p.apply.click()
        profiler.disable();elapsed=time.perf_counter()-started
        if os.environ.get('PLUS_TEST_DIR'):
            with (Path(os.environ['PLUS_TEST_DIR'])/'grid12-task-profile.txt').open('w') as stream:
                pstats.Stats(profiler,stream=stream).sort_stats('tottime').print_stats(30)
        self.assertEqual(self.p.items.count(),0,self.p.status.text())
        self.assertEqual(self.s.GeometryCount,288)
        self.assertEqual(self.s.solve(),0)
        self.assertEqual(len(self.s.PatternSpacingTags),143)
        self.assertEqual(self.p._preview,[])
        self.assertIsNone(self.p._helper_node)
        self.doc.undo();self.assertEqual(self.s.GeometryCount,2)
        self.doc.redo();self.assertEqual(self.s.GeometryCount,288)
        self.p.done.click();QtTest.QTest.qWait(100)
        self.assertIsNotNone(self.Gui.activeDocument().getInEdit())
        if os.environ.get('PLUS_TEST_DIR'):
            (Path(os.environ['PLUS_TEST_DIR'])/'grid12-task-timing.json').write_text(json.dumps(dict(seconds=elapsed),indent=2))
