# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Part geometry commands cannot infer editing ownership from selection."""
import importlib
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import ComponentModel as Model

COMMANDS = (
    'Part_Cut', 'Part_Common', 'Part_Fuse', 'Part_CompJoinFeatures',
    'Part_CompSplitFeatures', 'Part_CompCompoundTools', 'Part_Compound', 'Part_Section',
    'Part_MakeSolid', 'Part_ReverseShape', 'Part_Boolean', 'Part_Scale', 'Part_MakeFace',
    'Part_Fillet', 'Part_Chamfer', 'Part_Mirror', 'Part_CrossSections', 'Part_Builder',
    'Part_Offset', 'Part_Offset2D', 'Part_CompOffset', 'Part_Thickness',
    'Part_RuledSurface', 'Part_ProjectionOnSurface', 'Part_LinkArrayCircular',
    'Part_LinkArrayPath', 'Part_LinkArrayPoint', 'Part_LinkArrayLinear',
    'Part_LinkArrayPolar', 'Part_CoordinateSystem', 'Part_DatumPlane', 'Part_DatumLine',
    'Part_DatumPoint', 'Part_SimpleCylinder', 'Part_ShapeFromMesh', 'Part_PointsFromMesh',
    'Part_SimpleCopy', 'Part_TransformedCopy', 'Part_ElementCopy', 'Part_RefineShape',
    'Part_Defeaturing', 'Part_Cylinder', 'Part_Box', 'Part_Sphere', 'Part_Cone', 'Part_Torus')


class TestComponentNativeModelingGuards(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench('PartWorkbench')
        self.doc = Model.new_file_document()
        self.root = Model.metadata(self.doc).RootComponent
        self.part = Model.children(self.root)[0].LinkedObject
        self.box = self.doc.addObject('Part::Box', 'Box')
        self.second = self.doc.addObject('Part::Box', 'Second')
        Model.register_object(self.part, self.box)
        Model.register_object(self.part, self.second)
        self.doc.recompute()
        self.nav = importlib.import_module('freecad.gui.ComponentNavigator')
        self.panel = self.nav.show(self.doc)
        Gui.updateGui()
        self.panel.activate_item(self.panel.structure.topLevelItem(0))
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.box)
        Gui.Selection.addSelection(self.second)

    def tearDown(self):
        Gui.Selection.clearSelection()
        if Gui.Control.activeDialog(): Gui.Control.closeDialog()
        for name in list(App.listDocuments()): App.closeDocument(name)

    def testFileDisablesAndRefusesNativeModelingCommands(self):
        names = {obj.Name for obj in self.doc.Objects}
        undo = self.doc.UndoCount
        visibility = {obj.Name: obj.Visibility for obj in self.doc.Objects if hasattr(obj, "Visibility")}
        for name in COMMANDS:
            with self.subTest(command=name):
                command = Gui.Command.get(name)
                self.assertIsNotNone(command)
                self.assertFalse(command.isActive())
                Gui.runCommand(name, 0)
                self.assertEqual({obj.Name for obj in self.doc.Objects}, names)
                self.assertEqual(self.doc.UndoCount, undo)
                self.assertFalse(self.doc.HasPendingTransaction)
                self.assertEqual({obj.Name: obj.Visibility for obj in self.doc.Objects if hasattr(obj, "Visibility")}, visibility)
                self.assertFalse(Gui.Control.activeDialog())
        self.assertEqual(self.root.ModelHistory, [])
        self.assertEqual(self.root.ResultObjects, [])

    def testMissingActivePartDoesNotFallBackToFileModeling(self):
        Gui.activeDocument().activeView().setActiveObject('part', None)
        self.assertFalse(Gui.Command.get('Part_Box').isActive())
        before = {obj.Name for obj in self.doc.Objects}
        Gui.runCommand('Part_Box', 0)
        self.assertEqual({obj.Name for obj in self.doc.Objects}, before)

    def testExplicitComponentEnablesExistingNativeWorkflow(self):
        self.panel.edit_model(self.panel.models.topLevelItem(0))
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.box)
        Gui.Selection.addSelection(self.second)
        for name in ('Part_Box', 'Part_Cut', 'Part_SimpleCopy', 'Part_RefineShape'):
            self.assertTrue(Gui.Command.get(name).isActive(), name)
        before = {obj.Name for obj in self.doc.Objects}
        Gui.runCommand('Part_Box', 0)
        added = [obj for obj in self.doc.Objects if obj.Name not in before]
        self.assertEqual(len(added), 1)
        self.assertEqual(Model.owner(added[0]), self.part)
        self.assertEqual(self.root.ModelHistory, [])
        self.doc.undo()
        self.assertEqual({obj.Name for obj in self.doc.Objects}, before)

    def testLegacyAndInspectionCommandsRemainAvailable(self):
        self.assertTrue(Gui.Command.get('Part_CheckGeometry').isActive())
        App.closeDocument(self.doc.Name)
        legacy = App.newDocument('LegacyGuard')
        legacy.UndoMode = 1
        self.assertTrue(Gui.Command.get('Part_Box').isActive())
        Gui.runCommand('Part_Box', 0)
        self.assertTrue(any(obj.isDerivedFrom('Part::Box') for obj in legacy.Objects))
        legacy.undo()
        self.assertEqual(legacy.Objects, [])
