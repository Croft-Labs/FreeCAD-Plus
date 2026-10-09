# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native file relationship transactions and external definition isolation."""
import os
from pathlib import Path
import FreeCAD as App
import ComponentModel as Model
import CadDocument
import TestComponentAssemblySolver as Pilot


class TestComponentRelationshipTransactions(Pilot.TestComponentAssemblySolver):
    def frame(self, x):
        return App.Placement(App.Vector(x, 0, 0), App.Rotation())

    def snapshot(self):
        return ({obj.Name for obj in self.doc.Objects}, self.doc.UndoCount,
                self.first.LinkPlacement, self.second.LinkPlacement,
                self.first.getPropertyStatus("LinkPlacement"),
                self.second.getPropertyStatus("LinkPlacement"))

    def testGroundCreateEditRemoveUndoRedo(self):
        ground = Model.ground_occurrence(self.first)
        self.assertEqual(Model.ground_occurrence(self.first), ground)
        joint = Model.create_fixed_relationship(self.first, self.second, self.frame(15))
        name = joint.Name
        self.assertAlmostEqual(self.second.LinkPlacement.Base.x, 15)
        Model.edit_fixed_relationship(joint, self.frame(25), self.frame(0))
        self.assertAlmostEqual(self.second.LinkPlacement.Base.x, 25)
        self.doc.undo()
        self.assertAlmostEqual(self.second.LinkPlacement.Base.x, 15)
        self.doc.redo()
        self.assertAlmostEqual(self.second.LinkPlacement.Base.x, 25)
        Model.remove_relationships(self.doc, [joint])
        self.assertIsNone(self.doc.getObject(name))
        self.doc.undo()
        self.assertIsNotNone(self.doc.getObject(name))
        self.doc.redo()
        self.assertIsNone(self.doc.getObject(name))
        self.assertOwnership()

    def testGroundRemovalReleasesLocksAndUndoRestoresThem(self):
        ground = Model.ground_occurrence(self.first)
        ground_name = ground.Name
        self.assertIn("ReadOnly", self.first.getPropertyStatus("LinkPlacement"))
        Model.remove_relationships(self.doc, [ground])
        self.assertNotIn("ReadOnly", self.first.getPropertyStatus("LinkPlacement"))
        self.assertNotIn("ReadOnly", self.first.getPropertyStatus("Placement"))
        self.doc.undo()
        self.assertIsNotNone(self.doc.getObject(ground_name))
        self.assertIn("ReadOnly", self.first.getPropertyStatus("LinkPlacement"))
        self.doc.redo()
        self.assertNotIn("ReadOnly", self.first.getPropertyStatus("LinkPlacement"))
        self.assertIsNone(self.doc.getObject(ground_name))

    def testActualConflictingSolveRollsBack(self):
        Model.ground_occurrence(self.first)
        Model.ground_occurrence(self.second)
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "could not be solved"):
            Model.create_fixed_relationship(self.first, self.second, self.frame(15))
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(self.doc.HasPendingTransaction)
        self.assertOwnership()

    def testInvalidAndUngroundedRequestsDoNotLeaveObjects(self):
        before = self.snapshot()
        for target in (self.first, self.definition):
            with self.assertRaises(ValueError):
                Model.create_fixed_relationship(self.first, target)
            self.assertEqual(self.snapshot(), before)
        with self.assertRaisesRegex(ValueError, "grounded"):
            Model.create_fixed_relationship(self.first, self.second)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(self.doc.HasPendingTransaction)

    def testFirstGroundAndContextAreOneUndoStep(self):
        doc = Model.new_file_document("FirstGround")
        occurrence = Model.children(Model.metadata(doc).RootComponent)[0]
        before = {obj.Name for obj in doc.Objects}
        ground = Model.ground_occurrence(occurrence)
        name = ground.Name
        doc.undo()
        self.assertEqual({obj.Name for obj in doc.Objects}, before)
        self.assertIsNone(Model.assembly_context(doc))
        self.assertNotIn("ReadOnly", occurrence.getPropertyStatus("LinkPlacement"))
        doc.redo()
        self.assertEqual(doc.getObject(name).ObjectToGround, occurrence)
        self.assertIn("ReadOnly", occurrence.getPropertyStatus("LinkPlacement"))
        Model.validate(doc)

    def testConflictingEditRestoresConnectorsAndPlacement(self):
        Model.ground_occurrence(self.first)
        joint = Model.create_fixed_relationship(self.first, self.second, self.frame(15))
        Model.ground_occurrence(self.second)
        before = self.snapshot()
        old = App.Placement(joint.Placement1)
        with self.assertRaisesRegex(ValueError, "could not be solved"):
            Model.edit_fixed_relationship(joint, self.frame(25), self.frame(0))
        self.assertEqual(joint.Placement1, old)
        self.assertEqual(self.snapshot(), before)

    def testExternalDefinitionIsNotMovedOrWritten(self):
        output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        source = Model.new_file_document("SharedHardware")
        definition = Model.children(Model.metadata(source).RootComponent)[0].LinkedObject
        box = source.addObject("Part::Box", "HardwareBox")
        Model.register_object(definition, box, "Operation")
        source.recompute()
        sourcefile = output / "transaction-hardware.cadprt"
        source.saveAs(str(sourcefile))
        original = sourcefile.read_bytes()
        filename = output / "transaction-assembly.cadprt"
        self.doc.saveAs(str(filename))
        Model.remove_instances([self.second])
        self.second = Model.add_component(self.root, definition)
        self.second.LinkPlacement = self.frame(40)
        Model.ground_occurrence(self.first)
        joint = Model.create_fixed_relationship(self.first, self.second, self.frame(15))
        self.assertAlmostEqual(self.second.LinkPlacement.Base.x, 15)
        self.assertTrue(definition.Placement.isIdentity())
        self.assertNotIn("ReadOnly", definition.getPropertyStatus("Placement"))
        self.doc.save()
        self.assertEqual(sourcefile.read_bytes(), original)
        expected = Model.assembly_record(self.doc)
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        reopened = CadDocument.open(filename)
        self.assertEqual(Model.assembly_record(reopened), expected)
        self.assertEqual(Model.assembly_context(reopened).solve(), 0)
        root = Model.metadata(reopened).RootComponent
        external = Model.children(root)[1]
        self.assertNotEqual(external.LinkedObject.Document, reopened)
        self.assertTrue(external.LinkedObject.Placement.isIdentity())
        self.assertAlmostEqual(external.LinkPlacement.Base.x, 15)
        self.assertEqual(sourcefile.read_bytes(), original)
