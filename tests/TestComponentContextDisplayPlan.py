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


    def testContextScenePreservesSourceAndPerFaceTransparency(self):
        red, green = App.Material(), App.Material()
        red.DiffuseColor, red.Transparency = (1., 0., 0.), .1
        green.DiffuseColor, green.Transparency = (0., 1., 0.), .9
        self.body.ViewObject.ShapeAppearance = [red, green]
        before = [(m.DiffuseColor, m.Transparency) for m in self.body.ViewObject.ShapeAppearance]
        scene, links, materials = Navigator.context_scene(self.root, [self.first.ObjectId])
        path = self.second.Name + "." + self.body.Name + "."
        values = list(materials[path].transparency.getValues())
        self.assertAlmostEqual(values[0], .75)
        self.assertAlmostEqual(values[1], .9)
        self.assertTrue(materials[path].diffuseColor.isIgnored())
        self.assertEqual([(m.DiffuseColor, m.Transparency) for m in self.body.ViewObject.ShapeAppearance], before)
        self.assertEqual(len(links), len(Navigator.context_display_plan(self.root, [self.first.ObjectId])))

    def testCoinTransparencyOverrideRetainsColor(self):
        from pivy import coin
        root = coin.SoSeparator()
        override = coin.SoMaterial()
        for field in (override.ambientColor, override.diffuseColor, override.specularColor,
                      override.emissiveColor, override.shininess):
            field.setIgnored(True)
        override.transparency = .75
        override.setOverride(True)
        authored = coin.SoMaterial()
        authored.diffuseColor = (1., 0., 0.)
        authored.transparency = .1
        for node in (override, authored, coin.SoCube()):
            root.addChild(node)
        observed = []
        action = coin.SoCallbackAction()
        def capture(data, action, node):
            observed.append((tuple(coin.SoLazyElement.getDiffuse(action.getState(), 0).getValue()),
                             coin.SoLazyElement.getTransparency(action.getState(), 0)))
            return coin.SoCallbackAction.CONTINUE
        action.addPreCallback(coin.SoCube.getClassTypeId(), capture, None)
        action.apply(root)
        self.assertEqual(observed[0][0], (1., 0., 0.))
        self.assertAlmostEqual(observed[0][1], .75)


    def testViewContextRestoresWithoutChangingSourceAppearance(self):
        import os
        from pathlib import Path
        from pivy import coin
        from PySide import QtCore
        self.second.LinkPlacement = App.Placement(App.Vector(12, 0, 0), App.Rotation())
        self.body.ViewObject.ShapeColor = (1., .1, .1)
        self.child_body.ViewObject.ShapeColor = (.1, .8, .1)
        self.root_body.Visibility = False
        self.doc.recompute()
        panel = Navigator.show(self.doc)
        panel.refresh()
        window = panel.mdi.activeSubWindow()
        original = Gui.activeDocument().activeView().getViewer().getSceneGraph()
        original.ref()
        try:
            row = next(panel.models.topLevelItem(i) for i in range(panel.models.topLevelItemCount())
                       if panel.models.topLevelItem(i).data(0, QtCore.Qt.UserRole) == Navigator.object_key(self.shared))
            panel.edit_model(row)
            panel.refresh()
            entry = next(e for e in panel.context_views if e['window'] == window)
            action = coin.SoGetBoundingBoxAction(coin.SbViewportRegion(800, 600))
            action.apply(entry['scene'])
            self.assertGreater(action.getBoundingBox().getMax()[0], 13.)
            self.assertFalse(self.root_body.Visibility)
            self.assertEqual(self.body.ViewObject.Transparency, 0)
            view = Gui.activeDocument().activeView()
            view.viewAxonometric();view.fitAll();Gui.updateGui()
            camera = view.getCamera()
            panel.refresh_context_view()
            import re
            numbers = lambda text: [float(v) for v in re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", text)]
            before, after = numbers(camera), numbers(view.getCamera())
            self.assertEqual(len(before), len(after))
            for expected, actual in zip(before, after):
                self.assertAlmostEqual(actual, expected, delta=1e-5)
            Gui.updateGui()
            self.assertEqual(panel.active_path, [self.first.ObjectId])
            view.getViewer().grabFramebuffer().save(str(Path(os.environ['FREECAD_PLUS_VALIDATION_DIR']) / 'context-render.png'))
            picked = view.getObjectInfoRay(App.Vector(13, 1, 10), App.Vector(0, 0, -1))
            self.assertIsNotNone(picked)
            self.assertIn(self.second.Name, str(picked), str(picked))
            panel.activate_item(panel.structure.topLevelItem(0))
            panel.refresh()
            self.assertFalse(panel.context_views)
            self.assertEqual(view.getViewer().getSceneGraph().getNodeId(), original.getNodeId())
        finally:
            original.unref()
