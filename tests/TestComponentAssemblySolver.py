# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native solver pilot: borrow file occurrences without transferring ownership.

The file service creates the solver context; native joint fixtures establish
solver membership independently of the upcoming relationship UI.
"""
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import ComponentModel as Model
import JointObject
from PySide import QtCore


class TestComponentAssemblySolver(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("AssemblyWorkbench")
        self.doc = Model.new_file_document("FileSolver")
        self.root = Model.metadata(self.doc).RootComponent
        self.first = Model.children(self.root)[0]
        self.definition = self.first.LinkedObject
        box = self.doc.addObject("Part::Box", "Box")
        Model.register_object(self.definition, box, "Operation")
        self.second = Model.add_component(self.root, self.definition)
        self.second.LinkPlacement = App.Placement(App.Vector(40, 0, 0), App.Rotation())
        self.context = Model.ensure_assembly_context(self.doc)
        self.joints = next(o for o in self.context.Group if o.isDerivedFrom("Assembly::JointGroup"))
        self.doc.recompute()

    def tearDown(self):
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        QtCore.QCoreApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)

    def fixed(self):
        joint = self.joints.newObject("App::FeaturePython", "Fixed")
        JointObject.Joint(joint, JointObject.JointTypes.index("Fixed"))
        JointObject.ViewProviderJoint(joint.ViewObject)
        # Detached local connectors isolate solver/occurrence ownership from
        # geometry picking, which belongs to the subsequent UI adapter.
        joint.Detach1 = True
        joint.Detach2 = True
        joint.Reference1 = (self.first, ["", ""])
        joint.Reference2 = (self.second, ["", ""])
        joint.Placement1 = App.Placement(App.Vector(15, 0, 0), App.Rotation())
        joint.Placement2 = App.Placement()
        return joint

    def assertOwnership(self):
        self.assertEqual(Model.children(self.root), [self.first, self.second])
        self.assertEqual(Model.owner(self.first), self.root)
        self.assertEqual(Model.owner(self.second), self.root)
        self.assertNotIn(self.first, self.context.Group)
        self.assertNotIn(self.second, self.context.Group)
        self.assertEqual(self.root.ModelHistory, [])
        self.assertEqual(self.root.ResultObjects, [])
        self.assertTrue(self.root.Placement.isIdentity())
        self.assertTrue(self.definition.Placement.isIdentity())
        Model.validate(self.doc)

    def testBorrowedGroundingAndJointSolveUndoRedo(self):
        # Native syncGroundedJoints must discover the occurrence in the file,
        # despite it not belonging to the AssemblyObject's own Group.
        self.first.setEditorMode("LinkPlacement", 1)
        self.fixed()
        self.doc.recompute()
        self.doc.clearUndos()
        before = App.Placement(self.second.LinkPlacement)
        with Model.transaction(self.doc, "Solve file relationships"):
            self.assertEqual(self.context.solve(), 0)
        self.assertTrue(self.context.isPartGrounded(self.first))
        self.assertAlmostEqual(self.second.LinkPlacement.Base.x, 15, places=5)
        self.assertOwnership()
        self.doc.undo()
        self.assertEqual(self.second.LinkPlacement, before)
        self.assertOwnership()
        self.doc.redo()
        self.assertAlmostEqual(self.second.LinkPlacement.Base.x, 15, places=5)
        self.assertOwnership()

    def testGroundingIsPerOccurrenceNotSharedDefinition(self):
        self.first.setEditorMode("LinkPlacement", 1)
        self.context.solve()
        self.assertTrue(self.context.isPartGrounded(self.first))
        self.assertFalse(self.context.isPartGrounded(self.second))
        self.assertEqual(self.second.LinkPlacement.Base.x, 40)
        self.assertOwnership()

    def testInvalidRootRefusesBeforeMovingOccurrences(self):
        self.first.setEditorMode("LinkPlacement", 1)
        self.fixed()
        before = App.Placement(self.second.LinkPlacement)
        self.context.ComponentRoot = self.definition
        try:
            with self.assertRaisesRegex((ValueError, RuntimeError), "component root"):
                self.context.solve()
            self.assertEqual(self.second.LinkPlacement, before)
        finally:
            self.context.ComponentRoot = self.root
        self.assertOwnership()

    def testLegacyAssemblyMembershipUnchanged(self):
        legacy = self.doc.addObject("Assembly::AssemblyObject", "Legacy")
        legacy.newObject("Assembly::JointGroup", "LegacyJoints")
        box = legacy.newObject("Part::Box", "LegacyBox")
        box.setEditorMode("Placement", 1)
        legacy.solve()
        self.assertTrue(legacy.isPartGrounded(box))
        self.assertFalse(legacy.isPartGrounded(self.first))
        self.assertOwnership()
