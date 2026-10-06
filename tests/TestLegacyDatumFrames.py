# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native datum identities, frame access and retained attachment editability."""
import math
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
import CadDocument
import ComponentModel as Model
import ComponentSketch as Sketch
import ComponentPlane as Plane
from PySide import QtCore, QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest


class TestLegacyDatumFrames(unittest.TestCase):
    def setUp(self):
        self.names = set(App.listDocuments())
        self.doc = App.newDocument("LegacyDatums")
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

    def frame(self, x=7, angle=25):
        return App.Placement(App.Vector(x, 3, 2), App.Rotation(App.Vector(0, 1, 0), angle))

    def build(self):
        part = self.doc.addObject("App::Part", "Part")
        part.Placement = self.frame(20, 35)
        body = self.doc.addObject("PartDesign::Body", "Body")
        part.addObject(body)
        body.Placement = self.frame()
        plane = body.newObject("PartDesign::Plane", "DatumPlane")
        origin = next(o for o in body.Origin.OriginFeatures if o.Role == "XY_Plane")
        plane.AttachmentSupport = [(origin, '')]
        plane.MapMode = 'ObjectXY'
        plane.AttachmentOffset = App.Placement(App.Vector(0, 0, 4), App.Rotation(App.Vector(0, 0, 1), 15))
        axis = body.newObject("PartDesign::Line", "DatumAxis")
        axis.Placement = self.frame(2, 40)
        point = body.newObject("PartDesign::Point", "DatumPoint")
        point.Placement.Base = App.Vector(2, 4, 6)
        sketch = body.newObject('Sketcher::SketchObject', 'Sketch')
        sketch.AttachmentSupport = [(plane, '')]
        sketch.MapMode = 'ObjectXY'
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2), False)
        pad = body.newObject('PartDesign::Pad', 'Pad')
        pad.Profile = sketch
        pad.Length = 5
        body.Tip = pad
        for i, transform in enumerate((False, True)):
            link = self.doc.addObject('App::Link', 'Use' + str(i))
            link.setLink(part)
            link.LinkTransform = transform
            link.LinkPlacement = self.frame(50 + i * 20, 10)
        self.doc.recompute()
        return part, body, plane, axis, point, sketch, pad

    def alias(self, source):
        return next(o for o in self.doc.Objects if getattr(o, 'LegacyDatumSource', None) == source)

    def same(self, a, b):
        self.assertAlmostEqual(a.Volume, b.Volume, places=8)
        self.assertAlmostEqual(a.cut(b).Volume, 0, places=8)
        self.assertAlmostEqual(b.cut(a).Volume, 0, places=8)

    def test_origins_datums_supports_frames_and_shared_geometry(self):
        part, body, plane, axis, point, sketch, pad = self.build()
        origins = [part.Origin, body.Origin] + list(part.Origin.OriginFeatures) + list(body.Origin.OriginFeatures)
        native = [(o.Name, o.TypeId, o.ID) for o in origins + [plane, axis, point]]
        frames = {o.Name: o.getGlobalPlacement() for o in (plane, axis, point, sketch)}
        shapes = {o.Name: Part.getShape(o).copy() for o in (part, self.doc.Use0, self.doc.Use1)}
        supports = list(plane.AttachmentSupport), list(sketch.AttachmentSupport)
        group, tip = list(body.Group), body.Tip
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(native, [(o.Name, o.TypeId, o.ID) for o in origins + [plane, axis, point]])
        self.assertTrue(all(o.ObjectId for o in origins))
        self.assertEqual(body.Group, group)
        self.assertEqual(body.Tip, tip)
        self.assertEqual((list(plane.AttachmentSupport), list(sketch.AttachmentSupport)), supports)
        for source in (plane, axis, point):
            self.assertTrue(source.getGlobalPlacement().isSame(frames[source.Name], 1e-8))
            alias = self.alias(source)
            self.assertEqual(alias.LinkedObject, source)
            self.assertEqual(Model.owner(alias), part)
            self.assertNotEqual(alias.ObjectId, source.ObjectId)
            self.assertNotIn(alias.Name, part.ResultObjects)
        for name, shape in shapes.items():
            self.same(shape, Part.getShape(self.doc.getObject(name)))
        self.assertIn(self.alias(plane), Sketch.user_planes(part))
        self.assertEqual(Plane.geometry(part, (self.alias(plane), ''))[0], 'plane')
        self.assertTrue(Plane.geometry(part, (self.alias(plane), ''))[1].isSame(body.Placement.multiply(plane.Placement), 1e-8))
        self.assertEqual(Plane.geometry(part, (self.alias(axis), ''))[0], 'line')
        self.assertEqual(Plane.geometry(part, (self.alias(point), ''))[0], 'point')
        Model.validate(self.doc)

    def test_native_frame_offset_changes_undo_and_cold_reopen(self):
        part, body, plane, axis, point, sketch, pad = self.build()
        CadDocument.convert_legacy(self.doc)
        alias = self.alias(plane)
        ids = {o.Name: o.ObjectId for o in (body, plane, alias, body.Origin)}
        initial = sketch.getGlobalPlacement()
        with Model.transaction(self.doc, 'Edit retained plane offset'):
            plane.AttachmentOffset.Base.z = 9
        self.assertFalse(sketch.getGlobalPlacement().isSame(initial, 1e-8))
        self.assertAlmostEqual(plane.AttachmentOffset.Base.z, 9)
        self.assertTrue(alias.LinkPlacement.isSame(body.Placement.multiply(plane.Placement), 1e-8))
        self.doc.undo(); self.doc.recompute()
        self.assertTrue(sketch.getGlobalPlacement().isSame(initial, 1e-8))
        self.doc.redo(); self.doc.recompute()
        with Model.transaction(self.doc, 'Move retained native frame'):
            body.Placement = self.frame(12, 50)
        self.assertTrue(alias.LinkPlacement.isSame(body.Placement.multiply(plane.Placement), 1e-8))
        path = self.output / 'DatumFrames.cadprt'
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(path)
        for name, identity in ids.items():
            self.assertEqual(self.doc.getObject(name).ObjectId, identity)
        self.assertEqual(self.doc.Sketch.AttachmentSupport[0][0], self.doc.DatumPlane)
        self.assertEqual(self.doc.DatumPlane.AttachmentSupport[0][0].Role, 'XY_Plane')
        with Model.transaction(self.doc, 'Edit reopened native datum'):
            self.doc.DatumPlane.AttachmentOffset.Base.z = 11
        self.assertAlmostEqual(self.doc.DatumPlane.Placement.Base.z, 11)
        self.assertTrue(self.alias(self.doc.DatumPlane).LinkPlacement.isSame(
            self.doc.Body.Placement.multiply(self.doc.DatumPlane.Placement), 1e-8))

    def test_new_component_sketch_uses_linked_native_plane(self):
        part, body, plane, *_ = self.build()
        CadDocument.convert_legacy(self.doc)
        alias = self.alias(plane)
        sketch = Sketch.create(part, 'User plane', support=alias)
        expected = body.Placement.multiply(plane.Placement)
        self.assertTrue(sketch.Placement.isSame(expected, 1e-8), str((sketch.Placement, expected)))
        self.assertEqual(Model.owner(sketch), part)
        self.assertEqual(sketch.FrameSupport[0][0], alias)
        with Model.transaction(self.doc, 'Edit linked native plane used by new sketch'):
            plane.AttachmentOffset.Base.z = 8
        expected = body.Placement.multiply(plane.Placement)
        self.assertTrue(sketch.Placement.isSame(expected, 1e-8))

    def test_component_owned_datum_is_not_a_result_and_keeps_native_formulas(self):
        part = self.doc.addObject('App::Part', 'Part')
        plane = self.doc.addObject('PartDesign::Plane', 'Plane')
        part.addObject(plane)
        plane.MapMode = 'Deactivated'
        plane.setExpression('AttachmentOffset.Base.z', '6 mm')
        self.doc.recompute()
        original = list(plane.ExpressionEngine)
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(Model.owner(plane), part)
        self.assertEqual(plane.ComponentRole, 'Object')
        self.assertNotIn(plane.Name, part.ResultObjects)
        self.assertEqual(list(plane.ExpressionEngine), original)
        self.assertEqual(plane.LegacyDatumState, 'Retained native attachment')
        with self.assertRaisesRegex(ValueError, 'native attachment editor'):
            Plane.apply(part, Plane.defaults(), plane)
        self.assertEqual(list(plane.ExpressionEngine), original)

    def test_coordinate_system_frame_and_attachment_are_retained(self):
        part, body, plane, *_ = self.build()
        system = body.newObject('PartDesign::CoordinateSystem', 'DatumCS')
        system.Placement = self.frame(4, 60)
        self.doc.recompute()
        frame = system.getGlobalPlacement()
        native_id = system.ID
        CadDocument.convert_legacy(self.doc)
        alias = self.alias(system)
        self.assertEqual(system.ID, native_id)
        self.assertEqual(Model.owner(system), body)
        self.assertEqual(Model.owner(alias), part)
        self.assertTrue(system.getGlobalPlacement().isSame(frame,1e-8))
        self.assertTrue(alias.LinkPlacement.isSame(
            part.getGlobalPlacement().inverse().multiply(frame),1e-8))
        self.assertNotIn(alias.Name, part.ResultObjects)
        self.assertFalse(alias.Visibility)

    def test_missing_datum_is_reported_without_inventing_geometry(self):
        part, body, plane, *_ = self.build()
        CadDocument.convert_legacy(self.doc)
        alias = self.alias(plane)
        with Model.transaction(self.doc, 'Delete retained datum'):
            self.doc.removeObject(plane.Name)
        self.assertIsNone(alias.LegacyDatumSource)
        self.assertEqual(Model.history_state(alias), 'Needs repair')
        self.assertIn('missing', Model.history_detail(alias))
        with self.assertRaisesRegex(ValueError, 'missing'):
            Plane.geometry(part,(alias,''))
        self.assertNotIn(alias, Sketch.user_planes(part))

    def test_upgrade_previously_converted_content_is_idempotent_and_undoable(self):
        import LegacyConversion
        from unittest.mock import patch
        part, body, plane, *_ = self.build()
        with patch.object(LegacyConversion, 'migrate_datum_frames'):
            CadDocument.convert_legacy(self.doc)
        path = self.output / 'PreviousTask.cadprt'
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(path)
        self.assertEqual(Model.metadata(self.doc).LegacyFrameVersion, 1)
        count = len(self.doc.Objects)
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(len(self.doc.Objects), count)
        self.doc.undo(); self.doc.recompute()
        self.assertFalse(hasattr(Model.metadata(self.doc), 'LegacyFrameVersion'))
        self.doc.redo(); self.doc.recompute()
        self.assertEqual(self.alias(self.doc.DatumPlane).LinkedObject, self.doc.DatumPlane)

    def test_native_datum_history_edit_event_preserves_support_on_cancel(self):
        from freecad.gui import ComponentNavigator as Navigator
        part, body, plane, *_ = self.build()
        CadDocument.convert_legacy(self.doc)
        alias = self.alias(plane)
        support, mode, offset = list(plane.AttachmentSupport), plane.MapMode, App.Placement(plane.AttachmentOffset)
        panel = Navigator.show(self.doc)
        panel.open_component_tab(Navigator.object_key(part))
        panel.tabs.setCurrentWidget(panel.history)
        panel.setFloating(True); panel.resize(850,650); panel.show()
        Gui.getMainWindow().show(); Gui.updateGui(); QtTest.QTest.qWait(200)
        panel.refresh()
        row = next(panel.history.topLevelItem(i) for i in range(panel.history.topLevelItemCount())
                   if panel.history.topLevelItem(i).data(0,QtCore.Qt.UserRole)==Navigator.object_key(alias))
        rect = panel.history.visualItemRect(row)
        point = QtCore.QPoint(panel.history.header().sectionViewportPosition(2)+18, rect.center().y())
        QtTest.QTest.mouseDClick(panel.history.viewport(),QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,point)
        Gui.updateGui(); QtTest.QTest.qWait(150)
        edit = Gui.getDocument(self.doc.Name).getInEdit()
        self.assertIsNotNone(edit)
        self.assertEqual(edit.Object, plane)
        Gui.getDocument(self.doc.Name).resetEdit()
        if Gui.Control.activeDialog(): Gui.Control.closeDialog()
        self.doc.recompute()
        self.assertEqual(list(plane.AttachmentSupport), support)
        self.assertEqual(plane.MapMode, mode)
        self.assertTrue(plane.AttachmentOffset.isSame(offset,1e-8))
