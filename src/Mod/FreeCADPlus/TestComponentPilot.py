# SPDX-License-Identifier: LGPL-2.1-or-later
"""Run inside the FreeCAD GUI with PLUS_TEST_DIR pointing to temporary output."""
import hashlib
import json
import os
from pathlib import Path
import unittest
import zipfile
import xml.etree.ElementTree as ET

import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
from freecad_plus import document as component, editing


class TestComponentPilot(unittest.TestCase):
    def setUp(self):
        if "PLUS_TEST_DIR" not in os.environ:
            self.skipTest("Set PLUS_TEST_DIR to an isolated validation directory")
        self.output = Path(os.environ["PLUS_TEST_DIR"])
        self.before = set(App.listDocuments())
        self.doc = component.new_document("ComponentPilot")

    def tearDown(self):
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)

    def rectangle(self):
        sketch = editing.new_sketch(self.doc)
        with component.transaction(self.doc, "Rectangle"):
            points = [(0, 0), (20, 0), (20, 10), (0, 10)]
            for i, point in enumerate(points):
                end = points[(i + 1) % 4]
                index = sketch.addGeometry(Part.LineSegment(App.Vector(*point, 0), App.Vector(*end, 0)), False)
                sketch.addConstraint(Sketcher.Constraint("Block", index))
        self.assertEqual(sketch.solve(), 0)
        return sketch

    def test_structure_context_and_empty_file(self):
        root = component.validate(self.doc)
        self.assertEqual([o.Name for o in root.Definitions], ["Part001"])
        self.assertEqual(len(root.Group), 1)
        definition, occurrence = editing.context(self.doc)
        self.assertEqual(occurrence.LinkedObject, definition)
        self.assertFalse(definition.Visibility)
        self.assertTrue(occurrence.Visibility)
        self.assertEqual(len(component.history(self.doc)), 4)
        editing.edit_file(self.doc)
        Gui.Selection.addSelection(definition)
        with self.assertRaises(ValueError):
            editing.new_sketch(self.doc)
        Gui.Selection.clearSelection()
        editing.edit(occurrence)
        self.doc.undo()
        self.assertEqual(len(self.doc.Objects), 0)
        with self.assertRaises(ValueError):
            editing.context(self.doc)
        self.doc.redo()
        root = component.validate(self.doc)
        self.assertEqual(len(root.Group), 1)
        # Removing the occurrence retains the catalog. Then remove the definition
        # and its native Origin children; empty component files remain supported.
        with component.transaction(self.doc, "Remove occurrence"):
            self.doc.removeObject(root.Group[0].Name)
        self.assertEqual(len(root.Definitions), 1)
        definition = root.Definitions[0]
        descendants = list(definition.Origin.OriginFeatures)
        with component.transaction(self.doc, "Empty file"):
            root.Definitions = []
            for obj in descendants:
                self.doc.removeObject(obj.Name)
            self.doc.removeObject(definition.Origin.Name)
            self.doc.removeObject(definition.Name)
        self.assertEqual(len(component.validate(self.doc).Definitions), 0)
        component.save_document(self.doc, self.output / "empty.cadprt")

    def test_edit_context_is_per_view(self):
        gui_doc = Gui.activeDocument()
        first = gui_doc.activeView()
        root = component.validate(self.doc)
        first_context = first.getActiveObject("PlusEdit", False)
        gui_doc.createView("Gui::View3DInventor")
        self.assertNotEqual(gui_doc.activeView(), first)
        with self.assertRaises(ValueError):
            editing.context(self.doc)
        editing.edit(root.Group[0])
        editing.edit_file(self.doc)
        self.assertEqual(first.getActiveObject("PlusEdit", False), first_context)

    def test_modeling_rollback_undo_and_ownership(self):
        sketch = self.rectangle()
        definition, occurrence = editing.context(self.doc)
        body = definition.Group[0]
        count = len(self.doc.Objects)
        empty_sketch = editing.new_sketch(self.doc)
        after_empty = len(self.doc.Objects)
        with self.assertRaises(ValueError):
            editing.pad(self.doc, empty_sketch, 5)
        self.assertEqual(len(self.doc.Objects), after_empty)
        self.doc.undo()  # Empty sketch creation is still the last committed step.
        self.assertEqual(len(self.doc.Objects), count)
        pad = editing.pad(self.doc, sketch, 5)
        self.assertEqual(pad.Profile[0], sketch)
        self.assertEqual(body.Tip, pad)
        self.assertAlmostEqual(pad.Shape.Volume, 1000)
        self.assertEqual(component.history(self.doc, definition), [sketch, pad])
        self.doc.undo()
        self.assertIsNone(self.doc.getObject("Pad"))
        self.doc.redo()
        pad = self.doc.getObject("Pad")
        self.assertAlmostEqual(pad.Shape.Volume, 1000)
        with component.transaction(self.doc, "Change Pad"):
            pad.Length = 8
        self.assertAlmostEqual(pad.Shape.Volume, 1600)
        self.doc.undo(); self.doc.recompute()
        self.assertAlmostEqual(pad.Shape.Volume, 1000)
        self.doc.redo(); self.doc.recompute()
        self.assertAlmostEqual(pad.Shape.Volume, 1600)
        with self.assertRaisesRegex(ValueError, "outside component ownership"):
            with component.transaction(self.doc, "Invalid file-owned geometry"):
                self.doc.addObject("Part::Box", "UnownedBox")
        self.assertIsNone(self.doc.getObject("UnownedBox"))
        self.assertEqual(body.Tip, pad)
        self.assertTrue(pad.Shape.isValid())

    def test_persistence_fixture(self):
        sketch = self.rectangle()
        pad = editing.pad(self.doc, sketch, 5)
        root = component.validate(self.doc)
        definition, occurrence = editing.context(self.doc)
        with component.transaction(self.doc, "Rename and place"):
            definition.Label = "Renamed plate"
            occurrence.LinkPlacement = App.Placement(App.Vector(30, 4, 2), App.Rotation(App.Vector(0, 0, 1), 20))
        prefs = App.ParamGet("User parameter:BaseApp/Preferences/Document")
        prefs.SetBool("CheckExtension", True)
        path = component.save_document(self.doc, self.output / "pilot.cadprt")
        self.assertTrue(path.is_file())
        self.assertFalse(Path(str(path) + ".FCStd").exists())
        self.assertTrue(prefs.GetBool("CheckExtension"))
        self.assertFalse(Gui.activeDocument().Modified)
        identities = {o.Name: o.ID for o in self.doc.Objects}
        snapshot = dict(uid=str(self.doc.Uid), identities=identities,
                        matrix=occurrence.LinkPlacement.toMatrix().A,
                        volume=pad.Shape.Volume, label=definition.Label)
        (self.output / "expected.json").write_text(json.dumps(snapshot, indent=2))
        self.assertEqual(component.open_document(path), self.doc)
        name = self.doc.Name
        App.closeDocument(name)
        self.doc = component.open_document(path)
        self.assertEqual(str(self.doc.Uid), snapshot["uid"])
        self.assertEqual({o.Name: o.ID for o in self.doc.Objects}, identities)
        self.assertEqual(len(component.validate(self.doc).Group), 1)
        with self.assertRaises(ValueError):
            editing.context(self.doc)  # Transient Edit is never restored by save.
        component.save_document(self.doc)
        self.assertEqual(len(component.validate(self.doc).Definitions), 1)

    def test_schema_and_failed_save_protection(self):
        path = component.save_document(self.doc, self.output / "protected.cadprt")
        original = path.read_bytes()
        future = self.output / "future.cadprt"
        with zipfile.ZipFile(path) as source, zipfile.ZipFile(future, "w") as dest:
            for name in source.namelist():
                content = source.read(name)
                if name == "Document.xml":
                    tree = ET.fromstring(content)
                    tree.find("./ObjectData/Object/Properties/Property[@name='PlusSchema']/Integer").set("value", "99")
                    content = ET.tostring(tree)
                dest.writestr(name, content)
        digest = hashlib.sha256(future.read_bytes()).hexdigest()
        documents = set(App.listDocuments())
        with self.assertRaises(ValueError): component.open_document(future)
        with self.assertRaises(ValueError): component.save_document(self.doc, future)
        self.assertEqual(set(App.listDocuments()), documents)
        self.assertEqual(hashlib.sha256(future.read_bytes()).hexdigest(), digest)
        with component.transaction(self.doc, "Unsaved rename"):
            component.validate(self.doc).Definitions[0].Label = "Pending edit"
        # A file occupying the parent directory forces a native save failure.
        parent = self.output / "not-a-directory"
        parent.write_text("block directory creation")
        filename = self.doc.FileName
        with self.assertRaises(Exception): component.save_document(self.doc, parent / "failure.cadprt")
        self.assertEqual(self.doc.FileName, filename)
        self.assertTrue(Gui.activeDocument().Modified)
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(component.validate(self.doc).Definitions[0].Label, "Pending edit")

    def test_native_workflow_outside_pilot(self):
        stock = App.newDocument("LegacyControl")
        stock.UndoMode = 1
        body = stock.addObject("PartDesign::Body", "Body")
        sketch = body.newObject("Sketcher::SketchObject", "Sketch")
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 3), False)
        pad = body.newObject("PartDesign::Pad", "Pad")
        pad.Profile = sketch; pad.Length = 4
        stock.recompute()
        self.assertAlmostEqual(pad.Shape.Volume, 36 * 3.141592653589793)
        stock.saveAs(str(self.output / "legacy.FCStd"))
        self.assertTrue((self.output / "legacy.FCStd").is_file())
        with self.assertRaises(ValueError): component.validate(stock)
        disguised = self.output / "disguised.cadprt"
        disguised.write_bytes((self.output / "legacy.FCStd").read_bytes())
        with self.assertRaises(ValueError): component.open_document(disguised)


def verify_fresh_process(output):
    """Second process: identity, transforms, references, editability and no duplicate root."""
    output = Path(output)
    expected = json.loads((output / "expected.json").read_text())
    doc = component.open_document(output / "pilot.cadprt")
    root = component.validate(doc)
    assert str(doc.Uid) == expected["uid"]
    assert {o.Name: o.ID for o in doc.Objects} == expected["identities"]
    assert len(root.Group) == len(root.Definitions) == 1
    occurrence = root.Group[0]
    assert all(abs(a - b) < 1e-10 for a, b in zip(occurrence.LinkPlacement.toMatrix().A, expected["matrix"]))
    assert occurrence.LinkedObject == root.Definitions[0]
    assert root.Definitions[0].Label == expected["label"]
    pad = doc.getObject("Pad")
    assert pad.Profile[0] == doc.getObject("Sketch")
    assert abs(pad.Shape.Volume - expected["volume"]) < 1e-7
    editing.edit(occurrence)
    with component.transaction(doc, "Fresh-process feature edit"):
        pad.Length = 7
    assert pad.Shape.isValid() and abs(pad.Shape.Volume - 1400) < 1e-7
    component.save_document(doc, output / "fresh-edited.cadprt")
    assert len(component.validate(doc).Group) == 1
    App.closeDocument(doc.Name)
