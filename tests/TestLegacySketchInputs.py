# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native legacy sketch ownership, associative inputs and shared consumers."""
import hashlib
import math
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
import CadDocument
import ComponentModel as Model
import LegacyConversion
from PySide import QtCore, QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest


class TestLegacySketchInputs(unittest.TestCase):
    def setUp(self):
        self.names = set(App.listDocuments())
        self.doc = App.newDocument('LegacySketchInputs')
        self.doc.UndoMode = 1
        self.output = Path(os.environ['FREECAD_PLUS_VALIDATION_DIR'])

    def tearDown(self):
        for name in set(App.listDocuments()) - self.names:
            gui = Gui.getDocument(name)
            if gui.getInEdit():
                gui.resetEdit()
            if Gui.Control.activeDialog():
                Gui.Control.closeDialog()
            App.closeDocument(name)
        Gui.updateGui()

    def build(self, attached=True):
        part = self.doc.addObject('App::Part', 'Part')
        part.Placement = App.Placement(App.Vector(20, 2, 1), App.Rotation(App.Vector(0,1,0),35))
        body = self.doc.addObject('PartDesign::Body', 'Body')
        part.addObject(body)
        if attached:
            body.Placement = App.Placement(App.Vector(7,3,2), App.Rotation(App.Vector(0,1,0),25))
        sketch = (body.newObject('Sketcher::SketchObject', 'Sketch') if attached
                  else self.doc.addObject('Sketcher::SketchObject', 'Sketch'))
        if not attached:
            part.addObject(sketch)
        if attached:
            plane = body.newObject('PartDesign::Plane', 'DatumPlane')
            plane.Placement.Base.z = 4
            sketch.AttachmentSupport = [(plane, '')]
            sketch.MapMode = 'ObjectXY'
            sketch.AttachmentOffset.Base.z = 2
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0,0,1),2),False)
        sketch.addConstraint(Sketcher.Constraint('Radius',0,2))
        params = self.doc.addObject('App::FeaturePython','Parameters')
        params.addProperty('App::PropertyLength','Radius'); params.Radius = 2
        sketch.setExpression('Constraints[0]', 'Parameters.Radius')
        reference = (body.newObject('PartDesign::Feature','ReferenceCurve') if attached
                     else self.doc.addObject('Part::Feature','ReferenceCurve'))
        if not attached:
            part.addObject(reference)
        reference.Shape = Part.makeLine(App.Vector(10,0,0),App.Vector(12,0,0))
        sketch.addExternal(reference.Name,'Edge1')
        pad = body.newObject('PartDesign::Pad','Pad')
        pad.Profile = sketch; pad.Length = 5; body.Tip = pad
        for i, transform in enumerate((False,True)):
            link = self.doc.addObject('App::Link','Use'+str(i))
            link.setLink(part); link.LinkTransform = transform
            link.LinkPlacement.Base.x = 50+i*20
        self.doc.recompute()
        self.assertNotIn('Invalid',body.State)
        return part,body,sketch,pad

    def alias(self, source):
        return next(o for o in self.doc.Objects if getattr(o,'LegacySketchSource',None)==source)

    def same(self, a, b):
        self.assertAlmostEqual(a.Volume,b.Volume,places=8)
        self.assertAlmostEqual(a.cut(b).Volume,0,places=8)
        self.assertAlmostEqual(b.cut(a).Volume,0,places=8)

    def test_native_attachment_constraints_external_geometry_and_instances(self):
        part,body,sketch,pad = self.build()
        identity = sketch.Name,sketch.TypeId,sketch.ID
        inputs = list(sketch.AttachmentSupport),str(sketch.MapMode),list(sketch.ExternalGeometry),list(sketch.ExpressionEngine)
        group,tip = list(body.Group),body.Tip
        frames = sketch.getGlobalPlacement()
        shapes = {o.Name:Part.getShape(o).copy() for o in (body,self.doc.Use0,self.doc.Use1)}
        CadDocument.convert_legacy(self.doc)
        alias = self.alias(sketch)
        self.assertEqual(identity,(sketch.Name,sketch.TypeId,sketch.ID))
        self.assertEqual(inputs,(list(sketch.AttachmentSupport),str(sketch.MapMode),list(sketch.ExternalGeometry),list(sketch.ExpressionEngine)))
        self.assertEqual((body.Group,body.Tip),(group,tip))
        self.assertEqual(Model.owner(sketch),body)
        self.assertTrue(sketch.getGlobalPlacement().isSame(frames,1e-8))
        self.assertEqual(alias.LinkedObject,sketch)
        self.assertNotEqual(alias.ObjectId,sketch.ObjectId)
        self.assertTrue(alias.LinkPlacement.isSame(body.Placement.multiply(sketch.Placement),1e-8))
        self.assertLess(part.ModelHistory.index(alias.Name),part.ModelHistory.index(body.Name))
        self.assertNotIn(alias.Name,part.ResultObjects); self.assertFalse(alias.Visibility)
        for name,shape in shapes.items(): self.same(shape,Part.getShape(self.doc.getObject(name)))
        Model.validate(self.doc)

    def test_dimension_external_inputs_promoted_by_safe_pilot(self):
        part,body,sketch,pad = self.build(False)
        expressions,external = list(sketch.ExpressionEngine),list(sketch.ExternalGeometry)
        shape = body.Shape.copy()
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(body.LegacyHistoryState,'Mapped Sketch-Pad pilot',str(Model.metadata(self.doc).ConversionReport))
        self.assertEqual(Model.owner(sketch),part)
        self.assertEqual(expressions,list(sketch.ExpressionEngine))
        self.assertEqual(external,list(sketch.ExternalGeometry))
        self.same(shape,body.Shape)
        with Model.transaction(self.doc,'Edit expression source'):
            self.doc.Parameters.Radius = 3
        self.assertAlmostEqual(body.Shape.Volume,math.pi*9*5,places=7)
        self.assertEqual(pad.Profile[0],sketch)

    def test_retained_frame_dimension_edits_undo_and_reopen_preserve_original(self):
        part,body,sketch,pad = self.build()
        original = self.output/'SketchOriginal.FCStd'; self.doc.saveAs(str(original))
        digest = hashlib.sha256(original.read_bytes()).hexdigest()
        CadDocument.convert_legacy(self.doc)
        alias = self.alias(sketch)
        identities = {o.Name:o.ObjectId for o in (part,body,sketch,alias)}
        before = sketch.getGlobalPlacement()
        with Model.transaction(self.doc,'Change original inputs'):
            self.doc.Parameters.Radius = 3
            self.doc.DatumPlane.Placement.Base.z = 9
        self.assertAlmostEqual(body.Shape.Volume,math.pi*9*5,places=7)
        self.assertFalse(sketch.getGlobalPlacement().isSame(before,1e-8))
        self.assertTrue(alias.LinkPlacement.isSame(body.Placement.multiply(sketch.Placement),1e-8))
        self.doc.undo(); self.doc.recompute()
        self.assertAlmostEqual(body.Shape.Volume,math.pi*4*5,places=7)
        self.doc.redo(); self.doc.recompute()
        saved = self.output/'SketchConverted.cadprt'; self.doc.saveAs(str(saved))
        self.assertEqual(digest,hashlib.sha256(original.read_bytes()).hexdigest())
        App.closeDocument(self.doc.Name); self.doc = CadDocument.open(saved)
        for name,value in identities.items(): self.assertEqual(self.doc.getObject(name).ObjectId,value)
        with Model.transaction(self.doc,'Edit reopened sketch inputs'):
            self.doc.Parameters.Radius = 4
        self.assertAlmostEqual(self.doc.Body.Shape.Volume,math.pi*16*5,places=7)
        self.assertEqual(self.doc.Sketch.ExternalGeometry[0][0],self.doc.ReferenceCurve)

    def test_shared_independent_sketch_stays_one_input(self):
        part,body,sketch,pad = self.build(False)
        other = self.doc.addObject('Part::Extrusion','OtherExtrusion'); part.addObject(other)
        other.Base = sketch; other.Dir = App.Vector(0,0,8); other.Solid = True
        self.doc.recompute()
        self.assertAlmostEqual(other.Shape.Volume,math.pi*4*8,places=7)
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(pad.Profile[0],sketch); self.assertEqual(other.Base,sketch)
        self.assertEqual(Model.owner(sketch),part)
        self.assertEqual(part.ModelHistory.count(sketch.Name),1)
        with Model.transaction(self.doc,'Edit shared dimension'):
            self.doc.Parameters.Radius = 3
        self.assertAlmostEqual(body.Shape.Volume,math.pi*9*5,places=7)
        self.assertAlmostEqual(other.Shape.Volume,math.pi*9*8,places=7)

    def test_old_file_upgrade_is_idempotent_and_undoable(self):
        part,body,sketch,pad = self.build()
        with patch.object(LegacyConversion,'migrate_sketch_inputs'):
            CadDocument.convert_legacy(self.doc)
        saved = self.output/'BeforeSketchAdapter.cadprt'; self.doc.saveAs(str(saved))
        App.closeDocument(self.doc.Name); self.doc = CadDocument.open(saved)
        alias = self.alias(self.doc.Sketch)
        count = len(self.doc.Objects)
        CadDocument.convert_legacy(self.doc); self.assertEqual(count,len(self.doc.Objects))
        self.doc.undo(); self.doc.recompute()
        self.assertFalse(hasattr(Model.metadata(self.doc),'LegacySketchVersion'))
        self.doc.redo(); self.doc.recompute()
        self.assertEqual(self.doc.getObject(alias.Name).LinkedObject,self.doc.Sketch)

    def test_missing_source_reports_repair(self):
        part,body,sketch,pad = self.build()
        CadDocument.convert_legacy(self.doc); alias = self.alias(sketch)
        with Model.transaction(self.doc,'Remove retained sketch'):
            self.doc.removeObject(sketch.Name)
        self.assertIsNone(alias.LegacySketchSource)
        self.assertEqual(Model.history_state(alias),'Needs repair')
        self.assertIn('missing',Model.history_detail(alias))

    def test_sketch_dependencies_order_sources_before_consumers(self):
        part,body,sketch,pad = self.build()
        later = body.newObject('Sketcher::SketchObject','LaterInput')
        later.addGeometry(Part.LineSegment(App.Vector(10,0,0),App.Vector(12,0,0)),False)
        self.doc.recompute()
        sketch.addExternal(later.Name,'Edge1')
        body.Tip = pad; self.doc.recompute()
        CadDocument.convert_legacy(self.doc)
        self.assertLess(part.ModelHistory.index(self.alias(later).Name),
                        part.ModelHistory.index(self.alias(sketch).Name))
        self.assertEqual(sketch.ExternalGeometry[-1][0],later)

    def test_native_history_double_click_opens_original_sketch(self):
        from freecad.gui import ComponentNavigator as Navigator
        part,body,sketch,pad = self.build()
        CadDocument.convert_legacy(self.doc); alias = self.alias(sketch)
        inputs = list(sketch.AttachmentSupport),list(sketch.ExpressionEngine),list(sketch.ExternalGeometry)
        panel = Navigator.show(self.doc)
        panel.open_component_tab(Navigator.object_key(part)); panel.tabs.setCurrentWidget(panel.history)
        panel.setFloating(True); panel.resize(850,650); panel.show()
        Gui.getMainWindow().show(); Gui.updateGui(); QtTest.QTest.qWait(200); panel.refresh()
        row = next(panel.history.topLevelItem(i) for i in range(panel.history.topLevelItemCount())
                   if panel.history.topLevelItem(i).data(0,QtCore.Qt.UserRole)==Navigator.object_key(alias))
        rect = panel.history.visualItemRect(row)
        point = QtCore.QPoint(panel.history.header().sectionViewportPosition(2)+18,rect.center().y())
        QtTest.QTest.mouseDClick(panel.history.viewport(),QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,point)
        Gui.updateGui(); QtTest.QTest.qWait(200)
        edit = Gui.getDocument(self.doc.Name).getInEdit()
        self.assertIsNotNone(edit); self.assertEqual(edit.Object,sketch)
        Gui.getDocument(self.doc.Name).resetEdit()
        if Gui.Control.activeDialog(): Gui.Control.closeDialog()
        self.doc.recompute()
        self.assertEqual(inputs,(list(sketch.AttachmentSupport),list(sketch.ExpressionEngine),list(sketch.ExternalGeometry)))
