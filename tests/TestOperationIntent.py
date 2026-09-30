# SPDX-License-Identifier: LGPL-2.1-or-later
"""Bounded native geometry and persistence checks for roadmap 10.3a/b."""
import os
from pathlib import Path
import sys
import unittest
import FreeCAD as App
import Part
sys.path.insert(0, str(Path(__file__).parent / "prototypes"))
import OperationIntent as intent


class TestOperationIntent(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("OperationIntentProof")
        self.part = self.doc.addObject("App::Part", "Model")
        self.tool = self.box("Tool", 1)
        self.target = self.box("Target", 0)
        self.doc.recompute()

    def tearDown(self):
        App.closeDocument(self.doc.Name)

    def box(self, name, x, parent=None):
        obj = self.doc.addObject("Part::Feature", name)
        (parent or self.part).addObject(obj)
        obj.Shape = Part.makeBox(2, 2, 2, App.Vector(x, 0, 0))
        return obj

    def testZeroOneMultipleCandidatesAndVisibility(self):
        self.assertEqual(intent.propose(self.part, self.tool.Shape, [])[0], "NewBody")
        self.target.Visibility = False
        mode, targets, reason = intent.propose(self.part, self.tool.Shape, [self.target]*2)
        self.assertEqual(mode, "Unite")
        self.assertEqual(targets, [self.target])
        other = self.box("Other", 2)
        mode, targets, reason = intent.propose(self.part, self.tool.Shape, [other, self.target])
        self.assertEqual(mode, "ChooseTargets")
        self.assertEqual(set(targets), {other, self.target})

    def testCrossPartAndOccurrenceCannotBecomeImplicitTargets(self):
        other = self.doc.addObject("App::Part", "OtherPart")
        external = self.box("External", 0, other)
        link = self.doc.addObject("App::Link", "Occurrence")
        self.part.addObject(link)
        link.setLink(external)
        self.doc.recompute()
        self.assertEqual(intent.propose(self.part, self.tool.Shape, [external, link])[0], "NewBody")

    def testContactAndUnavailableGeometryRequireReview(self):
        for x in (3, 3 + 5e-8):
            contact = Part.makeBox(2, 2, 2, App.Vector(x, 0, 0))
            self.assertEqual(intent.propose(self.part, contact, [self.tool])[0], "Review")
        self.target.Shape = Part.Shape()
        self.assertEqual(intent.propose(self.part, self.tool.Shape, [self.target])[0], "Review")
        self.assertEqual(intent.propose(self.part, Part.Shape(), [])[0], "Review")

    def testExplicitNewBodySurvivesOverlapAndPreviewSuggestions(self):
        result = intent.commit(self.part, self.tool, "NewBody", [])
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume, 8)
        self.assertEqual(intent.propose(self.part, self.tool.Shape, [self.target])[0], "Unite")
        self.assertEqual(result.Operation, "NewBody")
        self.assertEqual(result.Targets, [])
        self.assertAlmostEqual(result.Shape.Volume, 8)

    def testSavedTargetDoesNotSwitchWhenGeometryMoves(self):
        result = intent.commit(self.part, self.tool, "Unite", [self.target])
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume, 12)
        other = self.box("Other", 10)
        self.doc.openTransaction("Move tool to another target")
        self.tool.Placement.Base = App.Vector(10, 0, 0)
        self.doc.recompute()
        self.doc.commitTransaction()
        self.assertAlmostEqual(self.tool.Shape.BoundBox.XMin, 11)
        self.assertEqual(result.ResultStatus, "Failed")
        self.assertTrue(result.Shape.isNull())
        self.assertEqual(result.Operation, "Unite")
        self.assertEqual(result.Targets, [self.target])
        self.assertEqual(intent.propose(self.part, self.tool.Shape, [other])[0], "Unite")
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(result.ResultStatus, "Ready")
        self.assertAlmostEqual(result.Shape.Volume, 12)
        self.doc.redo()
        self.doc.recompute()
        self.assertTrue(result.Shape.isNull())
        self.assertEqual(result.Targets, [self.target])

    def testSubtractIntersectAndMissingTarget(self):
        for operation in ("Subtract", "Intersect"):
            result = intent.commit(self.part, self.tool, operation, [self.target])
            self.doc.recompute()
            self.assertAlmostEqual(result.Shape.Volume, 4)
            self.doc.openTransaction("Cancel target removal")
            result.Targets = []
            self.doc.recompute()
            self.assertTrue(result.Shape.isNull())
            self.doc.abortTransaction()
            self.doc.recompute()
            self.assertAlmostEqual(result.Shape.Volume, 4)

    def testSaveReopenRetainsModeAndTarget(self):
        result = intent.commit(self.part, self.tool, "Subtract", [self.target])
        self.doc.recompute()
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "OperationIntent.FCStd"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        result = self.doc.CommittedOperation
        result.touch()
        self.doc.recompute()
        self.assertEqual(result.Operation, "Subtract")
        self.assertEqual(result.Targets, [self.doc.Target])
        self.assertAlmostEqual(result.Shape.Volume, 4)
