# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native joint task meaning, limit recovery and persistence (F076)."""
from pathlib import Path
import tempfile
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import JointObject
import TestAssemblyFreedom as fixture


class TestJointReview(unittest.TestCase):
    def setUp(self):
        self.fixture = fixture.TestAssemblyFreedom()
        self.fixture.setUp()
        self.doc = self.fixture.doc
        self.assembly = self.fixture.assembly
        self.panel = None

    def tearDown(self):
        if JointObject.activeTask:
            JointObject.activeTask.reject()
        self.fixture.tearDown()

    def edit(self, kind="Slider"):
        joint = self.fixture.joint(kind)
        self.fixture.edit()
        self.beforeTask = self.fixture.snapshot()
        self.panel = JointObject.TaskAssemblyCreateJoint(JointObject.JointTypes.index(kind), joint)
        Gui.Control.showDialog(self.panel)
        fixture.settle()
        return joint

    def limits(self, minimum, maximum, angular=False):
        form = self.panel.jForm
        if angular:
            low, high = form.limitRotMinSpinbox, form.limitRotMaxSpinbox
            checks = form.limitCheckbox3, form.limitCheckbox4
        else:
            low, high = form.limitLenMinSpinbox, form.limitLenMaxSpinbox
            checks = form.limitCheckbox1, form.limitCheckbox2
        for check in checks:
            check.setChecked(True)
        low.setProperty("rawValue", minimum)
        high.setProperty("rawValue", maximum)
        fixture.settle()

    def testMeaningAndExactReferences(self):
        self.edit()
        before = self.fixture.snapshot()
        self.assertIn("translation along", self.panel.motionReview.text())
        self.assertIn("rotation is locked", self.panel.motionReview.text())
        self.assertIn("Other joints and grounding", self.panel.motionReview.text())
        self.assertEqual(self.panel.jForm.featureList.item(0).toolTip(), self.doc.Name + "#Base.Face6")
        self.assertEqual(before, self.fixture.snapshot())
        for kind, phrase in (("Revolute", "translation is locked"),
                             ("Cylindrical", "translation along and rotation"),
                             ("Ball", "joint origin"), ("Fixed", "locks relative")):
            self.panel.jForm.jointType.setCurrentIndex(JointObject.JointTypes.index(kind))
            self.assertIn(phrase, self.panel.motionReview.text())
        self.panel.reject()

    def testInvalidLengthCanBeCorrectedThenUndoRedoAndReopen(self):
        joint = self.edit()
        self.limits(10, -10)
        self.assertFalse(self.panel.accept())
        self.assertIs(JointObject.activeTask, self.panel)
        self.assertIn("Length minimum", self.panel.limitReview.text())
        self.limits(-10, 10)
        self.assertFalse(self.panel.limitReview.isVisible())
        self.assertTrue(self.panel.accept())
        self.assertEqual((joint.LengthMin.Value, joint.LengthMax.Value), (-10, 10))
        self.doc.undo()
        self.assertFalse(joint.EnableLengthMin)
        self.doc.redo()
        self.assertTrue(joint.EnableLengthMin)
        self.assertEqual(joint.LengthMax.Value, 10)
        Gui.activeDocument().resetEdit()
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "Joint.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            restored = App.openDocument(path)
            self.assertEqual(restored.Joint.JointType, "Slider")
            self.assertEqual(restored.Joint.LengthMin.Value, -10)
            self.assertTrue(restored.Joint.EnableLengthMax)
            self.assertEqual(restored.Joint.Reference1[0].Name, "Base")

    def testInvalidAngleCancelRestoresJointAndPlacements(self):
        joint = self.edit("Revolute")
        before = self.beforeTask
        self.limits(90, -90, angular=True)
        self.assertFalse(self.panel.accept())
        self.assertIn("Angle minimum", self.panel.limitReview.text())
        self.panel.reject()
        self.assertFalse(joint.EnableAngleMin)
        self.assertFalse(joint.EnableAngleMax)
        self.assertEqual(before, self.fixture.snapshot())

    def testCylindricalChecksBothPairsAndAllowsEqualBounds(self):
        self.edit("Cylindrical")
        self.limits(-10, 10)
        self.limits(30, -30, angular=True)
        self.assertFalse(self.panel.accept())
        self.limits(30, 30, angular=True)
        self.assertTrue(self.panel.accept())

    def testDisabledAndUnsupportedLimitsDoNotBlock(self):
        self.edit()
        self.limits(10, -10)
        self.panel.jForm.limitCheckbox2.setChecked(False)
        self.assertEqual(self.panel.updateLimitReview(), "")
        self.panel.jForm.limitCheckbox2.setChecked(True)
        self.panel.jForm.jointType.setCurrentIndex(JointObject.JointTypes.index("Fixed"))
        self.assertEqual(self.panel.updateLimitReview(), "")
        self.assertTrue(self.panel.accept())

    def testPreviewNormalizationCannotChangeAcceptedDisplayedBounds(self):
        joint = self.edit()
        self.limits(10, -10)
        self.doc.recompute()  # The native solver swaps model bounds, not task inputs.
        self.assertEqual(joint.LengthMin.Value, -10)
        self.panel.jForm.limitLenMaxSpinbox.setProperty("rawValue", 20)
        self.assertTrue(self.panel.accept())
        self.assertEqual((joint.LengthMin.Value, joint.LengthMax.Value), (10, 20))

    def testExpressionLimitsAreCheckedAndPreserved(self):
        joint = self.edit()
        self.limits(-5, 5)
        joint.setExpression("LengthMin", "LengthMax + 1 mm")
        self.doc.recompute()
        self.assertFalse(self.panel.accept())
        joint.setExpression("LengthMin", "-LengthMax")
        self.panel.jForm.limitLenMaxSpinbox.setProperty("rawValue", 10)
        self.doc.recompute()
        self.assertTrue(self.panel.accept())
        self.assertEqual(joint.LengthMin.Value, -10)
        self.assertIn(("LengthMin", "-LengthMax"), joint.ExpressionEngine)

    def testNewJointCancelLeavesNoPartialRelationship(self):
        self.fixture.edit()
        before = self.fixture.snapshot()
        names = {obj.Name for obj in self.doc.Objects}
        Gui.Selection.addSelection(self.assembly, "Base.Face6")
        Gui.Selection.addSelection(self.assembly, "Slider.Face6")
        self.panel = JointObject.TaskAssemblyCreateJoint(JointObject.JointTypes.index("Slider"))
        Gui.Control.showDialog(self.panel)
        fixture.settle()
        self.assertEqual(len(self.panel.refs), 2)
        self.limits(10, -10)
        self.assertFalse(self.panel.accept())
        self.panel.reject()
        self.assertEqual(names, {obj.Name for obj in self.doc.Objects})
        self.assertEqual(before, self.fixture.snapshot())
