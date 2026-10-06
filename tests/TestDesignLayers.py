# SPDX-License-Identifier: LGPL-2.1-or-later
"""Run with the Plus payload; source overlays exercise native transactions/geometry."""
import os
from pathlib import Path
import tempfile
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtWidgets
from pivy import coin
from freecad.gui import DesignLayers as Layers
from freecad.gui import DesignLayersGui as UI


class TestDesignLayers(unittest.TestCase):
    def setUp(self):
        UI.install()
        self.doc = App.newDocument("LayerTest")
        self.doc.UndoMode = 1
        Layers.initialize(self.doc)

    def tearDown(self):
        if UI._panel:
            UI._panel.reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()

    def box(self, name="Box"):
        obj = self.doc.addObject("Part::Feature", name)
        obj.Shape = Part.makeBox(10, 10, 10)
        return obj

    def body(self):
        body = self.doc.addObject("PartDesign::Body", "Body")
        first = body.newObject("PartDesign::Feature", "First")
        first.Shape = Part.makeBox(10, 10, 10)
        sketch = body.newObject("Sketcher::SketchObject", "Sketch")
        sketch.addGeometry(Part.LineSegment(App.Vector(20, 0, 0), App.Vector(30, 0, 0)), False)
        last = body.newObject("PartDesign::Feature", "Last")
        last.Shape = Part.makeBox(15, 10, 10)
        body.Tip = last
        self.doc.recompute()
        first.Visibility = False
        last.Visibility = True
        sketch.Visibility = True
        return body, first, last, sketch

    def test_active_creation_and_origin_protection(self):
        layer = Layers.create(self.doc, "Machining")
        Layers.activate(self.doc, layer)
        box = self.box()
        self.assertEqual(box.DesignLayer, layer)
        body, first, last, sketch = self.body()
        self.assertEqual(Layers.layer_of(body), layer)
        self.assertEqual(Layers.layer_of(sketch), layer)
        for obj in [body.Origin] + list(body.Origin.OriginFeatures):
            self.assertEqual(Layers.layer_of(obj), Layers.BASE)
            self.assertFalse(Layers.move(self.doc, [obj], layer))
        with self.assertRaises(ValueError):
            Layers.rename(self.doc, Layers.BASE, "Other")
        with self.assertRaises(ValueError):
            Layers.delete(self.doc, Layers.BASE)
        with self.assertRaises(ValueError):
            Layers.create(self.doc, "BASE")

    def test_body_operations_and_sketch_are_distinct(self):
        body, first, last, sketch = self.body()
        a = Layers.create(self.doc, "Bodies")
        b = Layers.create(self.doc, "Sketches")
        Layers.move(self.doc, [sketch], b)
        Layers.move(self.doc, [first, last, body], a)
        self.assertEqual(Layers.targets(self.doc, [first, last]), [body])
        self.assertEqual([obj.DesignLayer for obj in (body, first, last)], [a] * 3)
        self.assertEqual(sketch.DesignLayer, b)
        Layers.activate(self.doc, b)
        extra = body.newObject("PartDesign::Feature", "Extra")
        self.assertEqual(Layers.layer_of(extra), a)
        self.assertEqual(sketch.DesignLayer, b)

    def test_undo_redo_and_delete_without_geometry_changes(self):
        body, first, last, sketch = self.body()
        before = [(o.Name, o.ID, o.Shape.Volume) for o in (body, first, last, sketch)]
        group = list(body.Group)
        layer = Layers.create(self.doc, "Layout")
        Layers.rename(self.doc, layer, "Detail")
        Layers.activate(self.doc, layer)
        self.doc.undo()
        self.assertEqual(Layers.state(self.doc)["active"], Layers.BASE)
        self.doc.redo()
        self.assertEqual(Layers.state(self.doc)["active"], layer)
        Layers.move(self.doc, [body, sketch], layer)
        self.doc.undo()
        self.assertEqual(Layers.layer_of(body), Layers.BASE)
        self.doc.redo()
        self.assertEqual(Layers.layer_of(body), layer)
        Layers.delete(self.doc, layer)
        self.assertEqual(Layers.state(self.doc)["active"], Layers.BASE)
        self.assertEqual(sketch.DesignLayer, Layers.BASE)
        self.assertEqual(before, [(o.Name, o.ID, o.Shape.Volume) for o in (body, first, last, sketch)])
        self.assertEqual(group, list(body.Group))
        self.doc.undo()
        self.assertEqual(Layers.state(self.doc)["active"], layer)
        self.assertEqual(sketch.DesignLayer, layer)
        self.doc.redo()
        self.assertEqual(len(Layers.state(self.doc)["layers"]), 1)

    def test_old_document_initialization_and_foreign_layer(self):
        box = self.box()
        box.removeProperty("DesignLayer")
        layer = Layers.create(self.doc, "Active")
        Layers.activate(self.doc, layer)
        box.removeProperty("DesignLayer")
        Layers.initialize(self.doc)
        self.assertEqual(box.DesignLayer, Layers.BASE)
        box.DesignLayer = "layer-from-another-document"
        Layers.initialize(self.doc)
        self.assertEqual(box.DesignLayer, Layers.BASE)

    @staticmethod
    def bounds(obj):
        action = coin.SoGetBoundingBoxAction(coin.SbViewportRegion(640, 480))
        action.apply(obj.ViewObject.RootNode)
        return action.getBoundingBox()

    def test_visibility_gates_preserve_individual_state_and_geometry(self):
        body, first, last, sketch = self.body()
        layer = Layers.create(self.doc, "Body layer")
        Layers.move(self.doc, [body], layer)
        UI.refresh()
        before = {o.Name: (o.Visibility, o.Shape.Volume, list(o.State)) for o in (body, first, last, sketch)}
        Layers.set_visible(self.doc, layer, False)
        UI.refresh()
        self.assertTrue(self.bounds(last).isEmpty())
        self.assertFalse(self.bounds(sketch).isEmpty())
        self.assertFalse(self.bounds(body).isEmpty())  # Body Group must still traverse the sketch.
        self.assertEqual(before, {o.Name: (o.Visibility, o.Shape.Volume, list(o.State)) for o in (body, first, last, sketch)})
        # Explicit individual changes while hidden are authored normally.
        last.Visibility = False
        Layers.set_visible(self.doc, layer, True)
        UI.refresh()
        self.assertFalse(last.Visibility)
        self.assertFalse(first.Visibility)
        self.assertTrue(sketch.Visibility)
        last.Visibility = True
        UI.refresh()
        self.assertFalse(self.bounds(last).isEmpty())
        body.ViewObject.DisplayModeBody = "Tip"
        Layers.set_visible(self.doc, layer, False)
        UI.refresh()
        self.assertTrue(self.bounds(body).isEmpty())

    def test_layer_visibility_undo_and_selection_policy(self):
        from freecad.gui import DesignSelection as Policy
        obj = self.box()
        layer = Layers.create(self.doc, "Hidden")
        Layers.move(self.doc, [obj], layer)
        Layers.set_visible(self.doc, layer, False)
        UI.refresh()
        self.assertFalse(Policy.allows(obj, "Edge1"))
        self.doc.undo()
        UI.refresh()
        self.assertTrue(Layers.visible(obj))
        self.doc.redo()
        UI.refresh()
        self.assertFalse(Layers.visible(obj))

    def test_save_reopen_native_formats(self):
        import ComponentModel as Model
        Model.initialize(self.doc, "Assembly")
        root = Model.metadata(self.doc).RootComponent
        box = self.box()
        Model.register_object(root, box, "Object", True)
        layer = Layers.create(self.doc, "Saved")
        Layers.move(self.doc, [box], layer)
        Layers.activate(self.doc, layer)
        Layers.set_visible(self.doc, layer, False)
        self.doc.recompute()
        name = box.Name
        for extension in ("FCStd", "cadprt"):
            path = Path(tempfile.mkdtemp(prefix="layers_")) / ("saved." + extension)
            self.doc.saveAs(str(path))
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(str(path))
            UI.refresh()
            box = self.doc.getObject(name)
            self.assertEqual(box.DesignLayer, layer)
            self.assertEqual(Layers.state(self.doc)["active"], layer)
            self.assertFalse(Layers.visible(box))
            self.assertAlmostEqual(box.Shape.Volume, 1000)
            self.assertEqual(len([o for o in self.doc.Objects if hasattr(o, "DesignLayerData")]), 1)

    def test_component_result_chain_keeps_input_sketch_independent(self):
        import ComponentModel as Model
        import ComponentExtrude as Extrude
        Model.initialize(self.doc, "Assembly")
        root = Model.metadata(self.doc).RootComponent
        sketch = self.doc.addObject("Sketcher::SketchObject", "Profile")
        points = [App.Vector(0, 0, 0), App.Vector(10, 0, 0), App.Vector(10, 10, 0), App.Vector(0, 10, 0)]
        for a, b in zip(points, points[1:] + points[:1]):
            sketch.addGeometry(Part.LineSegment(a, b), False)
        Model.register_object(root, sketch, "Object")
        self.doc.recompute()
        op, result = Extrude.create(root, sketch, 10)
        a = Layers.create(self.doc, "Body")
        b = Layers.create(self.doc, "Inputs")
        Layers.move(self.doc, [result], a)
        Layers.move(self.doc, [sketch], b)
        Layers.activate(self.doc, b)
        next_op, next_result = Extrude.create(root, sketch, 15, "Add", result)
        self.assertEqual(Layers.layer_of(next_op), a)
        self.assertEqual(Layers.layer_of(next_result), a)
        self.assertEqual(sketch.DesignLayer, b)
        self.assertEqual(len(Layers.targets(self.doc, [op, result, next_op, next_result])), 1)
        Layers.move(self.doc, [next_op], b)
        self.assertEqual([o.DesignLayer for o in (op, result, next_op, next_result)], [b] * 4)
        before = [o.Visibility for o in (op, result, next_op, next_result)]
        Layers.set_visible(self.doc, b, False)
        UI.refresh()
        Layers.set_visible(self.doc, b, True)
        UI.refresh()
        self.assertEqual([o.Visibility for o in (op, result, next_op, next_result)], before)

    def test_repeated_occurrences_resolve_definition_without_reparenting(self):
        part = self.doc.addObject("App::Part", "Part")
        obj = self.box()
        part.addObject(obj)
        a = self.doc.addObject("App::Link", "Instance")
        b = self.doc.addObject("App::Link", "Instance")
        a.setLink(part)
        b.setLink(part)
        layer = Layers.create(self.doc, "Shared")
        Gui.Selection.addSelection(a, obj.Name + ".Edge1")
        Gui.Selection.addSelection(b, obj.Name + ".Edge2")
        self.assertEqual(UI.selection(self.doc), [obj])
        Layers.move(self.doc, UI.selection(self.doc), layer)
        self.assertEqual(obj.DesignLayer, layer)
        self.assertEqual(part.Group, [obj])
        self.assertEqual(a.LinkedObject, part)
        self.assertEqual(b.LinkedObject, part)

    def test_task_controls_and_toolbar_menus(self):
        obj = self.box()
        layer = Layers.create(self.doc, "Design")
        bar = UI.LayersToolbar(Gui.getMainWindow())
        try:
            bar.set_design_active(True)
            self.assertFalse(bar.move.isEnabled())
            self.assertEqual(bar.move.popupMode(), QtWidgets.QToolButton.InstantPopup)
            Gui.Selection.addSelection(obj)
            UI.refresh()
            self.assertTrue(bar.move.isEnabled())
            bar.fill(bar.move, False)
            bar.move.menu().actions()[1].trigger()
            self.assertEqual(obj.DesignLayer, layer)
            self.assertEqual(bar.move.text(), "Move to Layer")
            UI.show()
            panel = UI._panel
            self.assertIsNotNone(panel)
            item = panel.list.topLevelItem(1)
            panel.list.itemDoubleClicked.emit(item, 1)
            self.assertEqual(Layers.state(self.doc)["active"], layer)
            item = panel.list.topLevelItem(1)
            self.assertTrue(item.font(1).bold())
            self.assertTrue(item.text(1).startswith("✓"))
            panel.clicked(item, 0)
            self.assertFalse(Layers.visible(obj))
            bar.set_design_active(False)
            self.assertIsNone(UI._panel)
            self.assertTrue(bar.isHidden())
        finally:
            UI._bars.discard(bar)
            bar.deleteLater()
