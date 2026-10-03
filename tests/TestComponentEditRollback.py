# SPDX-License-Identifier: LGPL-2.1-or-later
"""Temporary suppression of the history tail during native and Plus edits."""
import importlib
import hashlib
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
import ComponentModel as Model
import ComponentSketch as Sketch
import ComponentExtrude as Extrude
import ComponentExtent as Extent
from freecad.gui import ComponentNavigator as Navigator
from freecad.gui import ComponentExtrudeTask as ExtrudeTask
from PySide import QtCore
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest


class TestComponentEditRollback(unittest.TestCase):
    def setUp(self):
        source = Path(os.environ['FREECAD_PLUS_SOURCE'])
        for module, relative in ((Model, 'src/Mod/Part/ComponentModel.py'),
                                 (Navigator, 'src/Gui/ComponentNavigator.py')):
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((source / relative).read_bytes()).digest())
        self.doc = Model.new_document('Edit history rollback')
        self.part = Model.metadata(self.doc).RootComponent
        self.boxes = []
        for i in range(10):
            box = self.doc.addObject('Part::Box', 'Feature')
            Model.register_object(self.part, box, 'Object', True)
            box.Label = 'Feature ' + str(i + 1)
            self.boxes.append(box)
        self.doc.recompute()
        self.panel = Navigator.show(self.doc)
        self.panel.tabs.setCurrentWidget(self.panel.history)
        self.settle()

    def tearDown(self):
        for name in ('Extrude', 'Revolve', 'Loft', 'Pipe', 'Helix', 'Primitive'):
            module = importlib.import_module('freecad.gui.Component' + name + 'Task')
            if module._task:
                module._task.reject()
        for doc in list(App.listDocuments().values()):
            gui = Gui.getDocument(doc.Name)
            if gui.getInEdit():
                gui.resetEdit()
        self.settle()
        for context in list(Model._edit_rollbacks):
            context.restore()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        self.settle()
        self.assertFalse(Model._edit_rollbacks)

    def settle(self):
        Gui.updateGui()
        QtTest.QTest.qWait(200)

    def row(self, obj):
        self.panel.refresh()
        return next(self.panel.history.topLevelItem(i) for i in range(self.panel.history.topLevelItemCount())
                    if self.panel.history.topLevelItem(i).data(0, QtCore.Qt.UserRole) == Navigator.object_key(obj))

    def testFifthOfTenNativeEditRestoresAuthoredStates(self):
        Model.set_suppressed(self.boxes[7], True)
        self.boxes[8].Visibility = False
        before = [(getattr(b, 'UserSuppressed', False), b.Visibility) for b in self.boxes]
        undo = self.doc.UndoCount
        self.panel.edit_history(Navigator.object_key(self.boxes[4]))
        self.settle()
        for i, obj in enumerate(self.boxes):
            self.assertEqual(Model.edit_suppressed(obj), i >= 5)
            self.assertEqual(getattr(obj, 'UserSuppressed', False), before[i][0])
            if i >= 5:
                self.assertFalse(obj.Visibility)
                self.assertEqual(self.row(obj).checkState(0), QtCore.Qt.Unchecked)
                self.assertEqual(Model.history_state(obj), 'Suppressed during edit')
                with self.assertRaises(ValueError):
                    Model.current_shape(obj)
        self.assertFalse(Model.edit_suppressed(self.part.Origin))
        self.assertEqual(self.doc.UndoCount, undo)
        self.panel.setFloating(True)
        self.panel.resize(700, 600)
        self.panel.grab().save(str(Path(os.environ['FREECAD_PLUS_VALIDATION_DIR']) / 'fifth-feature-edit.png'))
        Gui.activeDocument().resetEdit()
        self.settle()
        self.assertEqual([(getattr(b, 'UserSuppressed', False), b.Visibility) for b in self.boxes], before)
        self.assertFalse(Model._edit_rollbacks)
        self.assertEqual(self.doc.UndoCount, undo)

    def testReorderedHistoryDefinesTailAndLastHasNone(self):
        Model.reorder_history(self.part, [self.boxes[9]], 0)
        self.panel.edit_history(Navigator.object_key(self.boxes[4]))
        self.settle()
        self.assertFalse(Model.edit_suppressed(self.boxes[9]))
        self.assertTrue(Model.edit_suppressed(self.boxes[8]))
        Gui.activeDocument().resetEdit()
        self.settle()
        self.panel.edit_history(Navigator.object_key(self.boxes[8]))
        self.settle()
        self.assertFalse(any(Model.edit_suppressed(b) for b in self.boxes))
        Gui.activeDocument().resetEdit()
        self.settle()

    def profile_and_extrude(self):
        profile = Sketch.create(self.part)
        profile.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
        self.doc.recompute()
        op, result = Extrude.create(self.part, profile, 5, options=Extent.defaults())
        later = self.doc.addObject('Part::Box', 'LaterIndependent')
        Model.register_object(self.part, later, 'Object', True)
        dependent = self.doc.addObject('Part::Mirroring', 'LaterDependent')
        Model.register_object(self.part, dependent, 'Object', True)
        dependent.Source = result
        self.doc.recompute()
        Model.publish_result(self.part, dependent)
        # Native expression provides a downstream recompute assertion without a test proxy.
        later.setExpression('Height', '<<' + op.Label + '>>.Length')
        self.doc.recompute()
        return profile, op, result, later, dependent

    def testExtrudeAcceptFailureCancelUndoAndReopen(self):
        profile, op, result, later, dependent = self.profile_and_extrude()
        initial = list(self.part.ModelHistory)
        for accept in (False, True):
            self.panel.edit_history(Navigator.object_key(op))
            task = ExtrudeTask._task
            self.assertTrue(Model.edit_suppressed(later))
            self.assertTrue(Model.edit_suppressed(dependent))
            self.assertFalse(Model.edit_suppressed(result))
            with patch.object(task.backend, 'edit', side_effect=ValueError('invalid dimensions')):
                self.assertFalse(task.accept())
            self.assertTrue(Model.edit_suppressed(later))
            if accept:
                task.length.setProperty('rawValue', 8)
                if not task.accept():
                    self.fail(task.status.text())
            else:
                task.reject()
            self.settle()
            self.assertFalse(Model._edit_rollbacks)
            self.assertTrue(later.Visibility)
            self.assertEqual(list(self.part.ModelHistory), initial)
        self.assertAlmostEqual(result.Shape.Volume, 32 * 3.141592653589793)
        self.assertAlmostEqual(later.Height.Value, 8)
        self.assertAlmostEqual(dependent.Shape.Volume, result.Shape.Volume)
        self.assertAlmostEqual(Model.result_for_operation(dependent).Shape.Volume, result.Shape.Volume)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(later.Height.Value, 5)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(later.Height.Value, 8)
        path = Path(os.environ['FREECAD_PLUS_VALIDATION_DIR']) / 'EditRollback.cadprt'
        self.doc.saveAs(str(path))
        name = later.Name
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.assertEqual(Model.history_state(self.doc.getObject(name)), 'Ready')
        self.assertAlmostEqual(self.doc.getObject(name).Height.Value, 8)

    def testSketchEditSuppressesOperationsAndPublishedResults(self):
        profile, op, result, later, dependent = self.profile_and_extrude()
        visibility = {obj.Name: obj.Visibility for obj in Model.history(self.part)}
        self.panel.edit_history(Navigator.object_key(profile))
        self.settle()
        for obj in (op, result, later, dependent):
            self.assertTrue(Model.edit_suppressed(obj))
            self.assertFalse(obj.Visibility)
        self.assertNotIn(result, Model.finished_results(self.part))
        Gui.activeDocument().resetEdit()
        self.settle()
        self.assertFalse(Model._edit_rollbacks)
        self.assertEqual({obj.Name: obj.Visibility for obj in Model.history(self.part)}, visibility)

    def testFailedEditorStartupRestoresTail(self):
        visibility = [obj.Visibility for obj in self.boxes]
        with patch.object(ExtrudeTask, 'ExtrudeTask', side_effect=ValueError('cannot open editor')):
            with self.assertRaises(ValueError):
                ExtrudeTask.launch(operation=self.boxes[4])
        self.assertFalse(Model._edit_rollbacks)
        self.assertEqual([obj.Visibility for obj in self.boxes], visibility)

    def testSaveDuringEditDoesNotPersistTemporarySuppression(self):
        before = [obj.Visibility for obj in self.boxes]
        self.panel.edit_history(Navigator.object_key(self.boxes[4]))
        self.settle()
        path = Path(os.environ['FREECAD_PLUS_VALIDATION_DIR']) / 'SavedDuringEdit.cadprt'
        self.doc.saveAs(str(path))
        self.assertTrue(Model.edit_suppressed(self.boxes[5]))
        Gui.activeDocument().resetEdit()
        self.settle()
        names = [obj.Name for obj in self.boxes]
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.assertEqual([self.doc.getObject(name).Visibility for name in names], before)
        self.assertFalse(any(Model.edit_suppressed(obj) for obj in self.doc.Objects))

    def testAllSixModelingEditorsSuppressIndependentTail(self):
        def rectangle(z=0, left=2, right=4, top=3):
            sketch = Sketch.create(self.part, offset=z)
            points = [App.Vector(left, 0, 0), App.Vector(right, 0, 0),
                      App.Vector(right, top, 0), App.Vector(left, top, 0)]
            for a, b in zip(points, points[1:] + points[:1]):
                sketch.addGeometry(Part.LineSegment(a, b))
            self.doc.recompute()
            return sketch
        profile, end, helix_profile = rectangle(), rectangle(z=10), rectangle(right=3, top=1)
        path = self.doc.addObject('Part::Feature', 'Path')
        path.Shape = Part.makePolygon([App.Vector(), App.Vector(0, 0, 10)])
        Model.register_object(self.part, path)
        pipe_profile = rectangle(left=0, right=4, top=4)
        pipe = importlib.import_module('ComponentPipe').defaults()
        pipe['spine'] = (path, [])
        helix = importlib.import_module('ComponentHelix').defaults()
        helix.update(pitch=3., height=6., turns=2.)
        cases = [('Extrude', [profile, 5.], {'options': Extent.defaults()}),
                 ('Revolve', [profile, 270.], {}),
                 ('Loft', [[(profile, None), (end, None)]], {}),
                 ('Pipe', [[(pipe_profile, None)]], {'options': pipe}),
                 ('Helix', [[(helix_profile, None)]], {'options': helix}),
                 ('Primitive', [[]], {})]
        for name, args, kwargs in cases:
            with self.subTest(operation=name):
                backend = importlib.import_module('Component' + name)
                op, result = backend.create(self.part, *args, **kwargs)
                tail = self.doc.addObject('Part::Box', 'IndependentTail')
                Model.register_object(self.part, tail, 'Object', True)
                self.doc.recompute()
                self.panel.edit_history(Navigator.object_key(op))
                self.settle()
                self.assertTrue(Model.edit_suppressed(tail))
                self.assertFalse(tail.Visibility)
                self.assertFalse(Model.edit_suppressed(result))
                module = importlib.import_module('freecad.gui.Component' + name + 'Task')
                module._task.reject()
                self.settle()
                self.assertFalse(Model._edit_rollbacks)
                self.assertTrue(tail.Visibility)

    def testClosingDocumentDuringNativeEditClearsRollback(self):
        self.panel.edit_history(Navigator.object_key(self.boxes[4]))
        self.settle()
        App.closeDocument(self.doc.Name)
        self.settle()
        self.assertFalse(Model._edit_rollbacks)

    def testSaveDuringChangedNativeEditPublishesFreshDownstreamGeometry(self):
        base = self.boxes[4]
        mirror = self.doc.addObject('Part::Mirroring', 'MirroredTail')
        Model.register_object(self.part, mirror, 'Operation')
        mirror.Source = base
        self.doc.recompute()
        result = Model.publish_result(self.part, mirror)
        self.doc.recompute()
        self.panel.edit_history(Navigator.object_key(base))
        base.Length = 27
        self.doc.recompute()
        self.assertTrue(Model.edit_suppressed(result))
        path = Path(os.environ['FREECAD_PLUS_VALIDATION_DIR']) / 'ChangedDuringEdit.cadprt'
        self.doc.saveAs(str(path))
        self.assertTrue(Model.edit_suppressed(result))
        self.assertFalse(mirror.Visibility)
        result_name, base_name = result.Name, base.Name
        Gui.activeDocument().resetEdit()
        self.settle()
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.assertAlmostEqual(self.doc.getObject(result_name).Shape.Volume, 2700)
        self.assertAlmostEqual(self.doc.getObject(base_name).Shape.Volume, 2700)

    def testSaveFailureRetainsTemporarySuppression(self):
        self.panel.edit_history(Navigator.object_key(self.boxes[4]))
        self.settle()
        obstruction = Path(os.environ['FREECAD_PLUS_VALIDATION_DIR']) / 'file-not-directory'
        obstruction.write_text('test save failure')
        with self.assertRaises(Exception):
            self.doc.saveAs(str(obstruction / 'blocked.cadprt'))
        self.settle()
        self.assertTrue(Model.edit_suppressed(self.boxes[5]))
        self.assertFalse(self.boxes[5].Visibility)
        Gui.activeDocument().resetEdit()
        self.settle()
        self.assertFalse(Model._edit_rollbacks)
        self.assertTrue(self.boxes[5].Visibility)
