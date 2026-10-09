# SPDX-License-Identifier: LGPL-2.1-or-later
"""Occurrence-exact fade planning uses the existing visible representation traversal."""
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import ComponentModel as Model
import Part
from freecad.gui import ComponentNavigator as Navigator


class TestComponentContextDisplayPlan(unittest.TestCase):
    def setUp(self):
        self.doc = Model.new_document("Context display plan")
        self.root = Model.metadata(self.doc).RootComponent
        self.first = Model.add_component(self.root, label="Shared")
        self.shared = self.first.LinkedObject
        self.second = Model.add_component(self.root, self.shared)
        self.child = Model.add_component(self.shared, label="Child")
        self.body = self.geometry(self.shared, "SharedBody")
        self.child_body = self.geometry(self.child.LinkedObject, "ChildBody")
        self.root_body = self.geometry(self.root, "RootBody")
        self.doc.recompute()
        Gui.updateGui()

    def geometry(self, component, name):
        obj = self.doc.addObject("Part::Feature", name)
        Model.register_object(component, obj, "Object", True)
        obj.Shape = Part.makeBox(2, 3, 4)
        obj.Visibility = True
        return obj

    def tearDown(self):
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def plan(self, ids):
        return {path: floor for path, obj, floor in Navigator.context_display_plan(self.root, ids)}

    def testOnlyChosenOccurrenceAndDescendantsRemainUnfaded(self):
        plan = self.plan([self.first.ObjectId])
        self.assertEqual(plan[self.first.Name + "." + self.body.Name + "."], 0)
        self.assertEqual(plan[self.first.Name + "." + self.child.Name + "." + self.child_body.Name + "."], 0)
        self.assertEqual(plan[self.second.Name + "." + self.body.Name + "."], .75)
        self.assertEqual(plan[self.second.Name + "." + self.child.Name + "." + self.child_body.Name + "."], .75)
        self.assertEqual(plan[self.root_body.Name + "."], .75)

    def testNestedEditFadesParentAndOtherUseOfSameChild(self):
        plan = self.plan([self.first.ObjectId, self.child.ObjectId])
        self.assertEqual(plan[self.first.Name + "." + self.body.Name + "."], .75)
        self.assertEqual(plan[self.first.Name + "." + self.child.Name + "." + self.child_body.Name + "."], 0)
        self.assertEqual(plan[self.second.Name + "." + self.child.Name + "." + self.child_body.Name + "."], .75)

    def testRootContextAndHiddenBranches(self):
        self.second.Visibility = False
        plan = self.plan([])
        self.assertTrue(plan)
        self.assertEqual(set(plan.values()), {0})
        self.assertFalse(any(path.startswith(self.second.Name + ".") for path in plan))
        self.assertEqual(set(plan), set(Navigator.visible_paths(self.root, self.root, [])))
        Model.set_representation(self.root, [self.first.ObjectId, self.child.ObjectId], "Hidden")
        plan = self.plan([self.first.ObjectId])
        self.assertFalse(any(self.child.Name + "." in path for path in plan))

    def testPlanningDoesNotModifyAuthoredAppearanceOrGeometry(self):
        self.body.ViewObject.Transparency = 90
        self.child_body.ViewObject.Transparency = 25
        before = [(obj.ViewObject.Transparency, obj.ViewObject.ShapeColor, obj.Shape.Volume)
                  for obj in (self.body, self.child_body)]
        for ids in ([self.first.ObjectId], [self.second.ObjectId], []):
            self.plan(ids)
        self.assertEqual(before, [(obj.ViewObject.Transparency, obj.ViewObject.ShapeColor, obj.Shape.Volume)
                                 for obj in (self.body, self.child_body)])

    def testStalePathIsRejectedRatherThanFadingWrongBranch(self):
        with self.assertRaises(ValueError):
            self.plan([self.first.ObjectId, "deleted-occurrence"])
