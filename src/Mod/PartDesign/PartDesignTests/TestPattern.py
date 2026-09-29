# SPDX-License-Identifier: LGPL-2.1-or-later

"""Stable result identity and retained settings for the combined Pattern feature."""

import tempfile
import unittest
from pathlib import Path

import FreeCAD as App


class TestPattern(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("PatternTest")
        self.doc.UndoMode = 1
        self.body = self.doc.addObject("PartDesign::Body", "Body")
        self.base = self.body.newObject("PartDesign::AdditiveBox", "Base")
        self.base.Length = self.base.Width = 40
        self.base.Height = 5
        self.base.Placement.Base = App.Vector(-20, -20, 0)
        self.bump = self.body.newObject("PartDesign::AdditiveBox", "Bump")
        self.bump.Length = self.bump.Width = self.bump.Height = 2
        self.bump.Placement.Base = App.Vector(5, 0, 5)
        self.doc.recompute()

    def tearDown(self):
        App.closeDocument(self.doc.Name)

    def makePattern(self):
        pattern = self.body.newObject("PartDesign::Pattern", "Pattern")
        pattern.Originals = [self.bump]
        linear, circular = pattern.PatternSettings
        axes = self.body.Origin.OriginFeatures
        linear.Direction = (axes[0], [""])
        linear.Direction2 = (axes[1], [""])
        circular.Axis = (axes[2], [""])
        linear.Length = 10
        linear.Occurrences = 3
        circular.Occurrences = 4
        self.doc.recompute()
        return pattern, linear, circular

    def assertVolume(self, pattern, volume):
        self.doc.recompute()
        self.assertTrue(pattern.isValid(), pattern.getStatusString())
        self.assertTrue(pattern.Shape.isValid())
        self.assertAlmostEqual(pattern.Shape.Volume, volume, places=5)

    def testSwitchPreservesIdentityLinksExpressionsAndBothSettings(self):
        pattern, linear, circular = self.makePattern()
        linear.setExpression("Length", "Bump.Length * 5")
        link = self.doc.addObject("App::FeaturePython", "Reference")
        link.addProperty("App::PropertyLink", "Target")
        link.Target = pattern
        self.assertVolume(pattern, 8024)
        for mode, active, volume in [("Circular", circular, 8032), ("Linear", linear, 8024)]:
            pattern.PatternType = mode
            self.assertVolume(pattern, volume)
            self.assertEqual(pattern.Transformations, [active])
            self.assertEqual(link.Target, pattern)
            self.assertEqual(pattern.TypeId, "PartDesign::Pattern")
            self.assertEqual(pattern.Originals, [self.bump])
        self.assertEqual(linear.ExpressionEngine, [("Length", "Bump.Length * 5")])
        self.assertEqual(circular.Occurrences, 4)

    def testSpacingSecondDirectionAndSuppressionRemainAvailable(self):
        pattern, linear, circular = self.makePattern()
        linear.Mode = "Spacing"
        linear.Offset = 5
        linear.Occurrences2 = 2
        linear.Length2 = 5
        self.assertVolume(pattern, 8048)
        linear.SuppressedPositions = [(1, 1)]
        self.assertVolume(pattern, 8040)
        pattern.PatternType = "Circular"
        circular.Mode = "Spacing"
        circular.Offset = 90
        self.assertVolume(pattern, 8032)
        circular.SuppressedIndices = [1]
        self.assertVolume(pattern, 8024)
        pattern.PatternType = "Linear"
        self.assertVolume(pattern, 8040)

    def testUndoRedoSwitch(self):
        pattern, linear, circular = self.makePattern()
        self.doc.openTransaction("Switch pattern")
        pattern.PatternType = "Circular"
        self.doc.recompute()
        self.doc.commitTransaction()
        self.doc.undo()
        self.assertEqual(pattern.PatternType, "Linear")
        self.assertEqual(pattern.Transformations, [linear])
        self.assertVolume(pattern, 8024)
        self.doc.redo()
        self.assertEqual(pattern.PatternType, "Circular")
        self.assertEqual(pattern.Transformations, [circular])
        self.assertVolume(pattern, 8032)

    def testSaveReopenRetainsInactiveSettings(self):
        pattern, linear, circular = self.makePattern()
        pattern.PatternType = "Circular"
        self.assertVolume(pattern, 8032)
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "pattern.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            pattern = self.doc.Pattern
            self.assertEqual(pattern.PatternType, "Circular")
            self.assertVolume(pattern, 8032)
            self.assertEqual(len(pattern.PatternSettings), 2)
            pattern.PatternType = "Linear"
            self.assertVolume(pattern, 8024)

    def testEmptyFeatureListIsInvalidAndRecovers(self):
        pattern, _, _ = self.makePattern()
        pattern.Originals = []
        self.doc.recompute()
        self.assertFalse(pattern.isValid())
        self.assertTrue(pattern.Shape.isNull())
        pattern.Originals = [self.bump]
        self.assertVolume(pattern, 8024)
