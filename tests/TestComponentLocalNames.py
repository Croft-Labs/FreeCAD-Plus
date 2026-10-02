# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component-local labels must not inherit document-wide object numbering."""
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
import ComponentModel as Model
import ComponentSketch as Sketch
import ComponentExtrude as Extrude
from freecad.gui import ComponentNavigator as Navigator


class TestComponentLocalNames(unittest.TestCase):
    def setUp(self):
        self.preferences = App.ParamGet("User parameter:BaseApp/Preferences/Document")
        self.duplicates = self.preferences.GetBool("DuplicateLabels")
        self.preferences.SetBool("DuplicateLabels", False)
        self.doc = Model.new_document("Assembly")
        self.first = Model.create_definition(self.doc, "Component001")
        self.second = Model.create_definition(self.doc, "Component002")

    def tearDown(self):
        self.preferences.SetBool("DuplicateLabels", self.duplicates)
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def sketch_and_body(self, component):
        sketch = Sketch.create(component)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
        self.doc.recompute()
        operation, body = Extrude.create(component, sketch, 4)
        return sketch, operation, body

    def testNativeNewDocumentDefaults(self):
        Gui.runCommand("Std_New")
        first = App.ActiveDocument
        self.assertEqual((first.Name, first.Label, first.FileName), ("untitled001", "untitled001", ""))
        self.assertEqual(Model.metadata(first).RootComponent.Label, "Part001")
        Gui.runCommand("Std_New")
        second = App.ActiveDocument
        self.assertEqual((second.Name, second.Label, second.FileName), ("untitled002", "untitled002", ""))
        self.assertEqual(Model.metadata(second).RootComponent.Label, "Part001")

    def testIndependentCountersAndOriginRows(self):
        first = self.sketch_and_body(self.first)
        second = self.sketch_and_body(self.second)
        for objects in (first, second):
            self.assertEqual([obj.Label for obj in objects], ["Sketch001", "Extrude001", "Body001"])
        self.assertTrue(all(a.Name != b.Name and a.ObjectId != b.ObjectId
                            for a, b in zip(first, second)))
        later = self.sketch_and_body(self.first)
        self.assertEqual([obj.Label for obj in later], ["Sketch002", "Extrude002", "Body002"])
        later_names = [obj.Name for obj in later]
        self.doc.undo()
        self.doc.redo()
        self.assertEqual([self.doc.getObject(name).Label for name in later_names],
                         ["Sketch002", "Extrude002", "Body002"])
        for component in (self.first, self.second):
            panel = Navigator.show(self.doc)
            panel.root_key = panel.active_key = Navigator.object_key(component)
            panel.active_path = []
            panel.refresh()
            self.assertEqual(panel.history.topLevelItem(0).text(2), "Origin")

    def testCustomLabelsAndLegacyUniqueness(self):
        sketch, operation, body = self.sketch_and_body(self.first)
        sketch.Label = "Mounting profile"
        body.Label = "Bracket"
        custom = self.doc.addObject("Part::Feature", "Reserved")
        custom.Label = "Sketch001"
        Model.register_object(self.first, custom)
        next_sketch = Sketch.create(self.first)
        self.assertEqual(next_sketch.Label, "Sketch002")
        self.assertEqual(sketch.Label, "Mounting profile")
        self.assertEqual(body.Label, "Bracket")
        legacy = self.doc.addObject("Part::Feature", "Legacy")
        legacy.Label = "Bracket"
        self.assertNotEqual(legacy.Label, "Bracket")

    def testSaveReopenKeepsLocalLabelsAndIdentities(self):
        objects = self.sketch_and_body(self.first) + self.sketch_and_body(self.second)
        before = [(obj.Name, obj.ObjectId, obj.Label) for obj in objects]
        output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "LocalLabels.cadprt"
        self.doc.saveAs(str(output))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(output))
        self.assertEqual([(self.doc.getObject(name).Name, self.doc.getObject(name).ObjectId,
                           self.doc.getObject(name).Label) for name, identity, label in before], before)
        Model.validate(self.doc)

    def testPartDefinitionsDoNotNumberTheirOccurrences(self):
        doc = Model.new_document()
        root = Model.metadata(doc).RootComponent
        self.assertEqual(doc.Label, "untitled001")
        self.assertEqual(root.Label, "Part001")
        first = Model.add_component(root)
        second = Model.add_component(root)
        nested = Model.add_component(first.LinkedObject)
        self.assertEqual([obj.Label for obj in (first.LinkedObject, second.LinkedObject, nested.LinkedObject)],
                         ["Part002", "Part003", "Part004"])
        self.assertEqual([obj.Label for obj in (first, second, nested)], ["Part002", "Part003", "Part004"])
        repeated = Model.add_component(root, first.LinkedObject)
        self.assertEqual(repeated.Label, "Part002")
        self.assertEqual(Model.next_part_label(doc), "Part005")
        reserved = Model.create_definition(doc, "Part006")
        self.assertEqual(Model.create_definition(doc).Label, "Part005")
        self.assertEqual(reserved.Label, "Part006")
        self.assertEqual(Model.next_part_label(doc), "Part007")
        self.assertEqual(Model.create_definition(doc, "Bracket").Label, "Bracket")
        legacy = doc.addObject("Part::Feature", "LegacyLabel")
        legacy.Label = "Part002"
        self.assertNotEqual(legacy.Label, "Part002")
        Model.validate(doc)
