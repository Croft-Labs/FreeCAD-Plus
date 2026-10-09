# SPDX-License-Identifier: LGPL-2.1-or-later
"""Whole-file legacy migration using installed modules and native consumers."""
import hashlib
import os
from pathlib import Path
import shutil
import time
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
import CadDocument
import ComponentModel as Model
from TestLegacyExtrusions import TestLegacyExtrusions


class TestLegacyIntegration(unittest.TestCase):
    setUp = TestLegacyExtrusions.setUp
    tearDown = TestLegacyExtrusions.tearDown
    same = TestLegacyExtrusions.same
    open_row = TestLegacyExtrusions.open_row

    def mixed(self):
        assembly = self.doc.addObject('App::Part', 'Assembly')
        assembly.Placement = App.Placement(App.Vector(10, 3, 1), App.Rotation(App.Vector(0, 0, 1), 30))
        part = self.doc.addObject('App::Part', 'Part'); assembly.addObject(part)
        part.Placement.Base.x = 15
        body = part.newObject('PartDesign::Body', 'Body')
        sketch = body.newObject('Sketcher::SketchObject', 'Sketch')
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2), False)
        sketch.addConstraint(Sketcher.Constraint('Radius', 0, 2))
        pad = body.newObject('PartDesign::Pad', 'Pad'); pad.Profile = sketch; pad.Length = 5
        body.Tip = pad
        native = part.newObject('PartDesign::Body', 'NativeBody'); native.Placement.Base.x = 20
        box = native.newObject('PartDesign::AdditiveBox', 'Box'); box.Length = box.Width = box.Height = 10
        fillet = native.newObject('PartDesign::Fillet', 'Fillet'); fillet.Base = (box, ['Edge1']); fillet.Radius = 1
        pattern = native.newObject('PartDesign::LinearPattern', 'Pattern'); pattern.Originals = [fillet]
        pattern.Direction = (native.Origin.OriginFeatures[0], ['']); pattern.Length = 5; pattern.Occurrences = 2
        native.Tip = pattern
        for i, transform in enumerate((False, True)):
            link = self.doc.addObject('App::Link', 'Use' + str(i)); assembly.addObject(link); link.setLink(part)
            link.LinkTransform = transform; link.LinkPlacement.Base.x = 50 + i * 20
        sibling = self.doc.addObject('Part::Box', 'Sibling'); assembly.addObject(sibling)
        sibling.Placement.Base.y = 40
        self.doc.recompute(); self.assertNotIn('Invalid', pattern.State)
        return assembly, part, body, sketch, pad, native, fillet, pattern, sibling

    def original(self, name):
        path = self.output / (name + '.FCStd'); self.doc.saveAs(str(path))
        return path, hashlib.sha256(path.read_bytes()).hexdigest()

    def close_all(self):
        for name in list(App.listDocuments()): App.closeDocument(name)

    def test_mixed_whole_file_shared_sibling_frames_undo_and_cold_restore(self):
        objects = self.mixed(); assembly, part, body, sketch, pad, native, fillet, pattern, sibling = objects
        shapes = {o.Name: Part.getShape(o).copy() for o in (assembly, self.doc.Use0, self.doc.Use1, sibling)}
        identities = [(o.Name, o.TypeId, o.ID, o.Label) for o in objects]
        group, tip, sibling_frame = list(native.Group), native.Tip, App.Placement(sibling.Placement)
        original, digest = self.original('MixedOriginal')
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(identities, [(o.Name, o.TypeId, o.ID, o.Label) for o in objects])
        self.assertEqual(native.Group, group); self.assertEqual(native.Tip, tip)
        self.assertTrue(sibling.Placement.isSame(sibling_frame, 1e-9))
        self.assertEqual(body.Producer, pad); self.assertEqual(Model.owner(fillet), native)
        for name, before in shapes.items(): self.same(before, Part.getShape(self.doc.getObject(name)))
        uuids = {o.Name: o.ObjectId for o in objects}
        self.doc.undo(); self.doc.recompute(); self.assertEqual(Model.owner(part), assembly)
        self.doc.redo(); self.doc.recompute(); Model.validate(self.doc)
        saved = self.output / 'Mixed.cadprt'; self.doc.saveAs(str(saved)); self.close_all()
        self.doc = CadDocument.open(saved)
        for name, oid in uuids.items(): self.assertEqual(self.doc.getObject(name).ObjectId, oid)
        for name, before in shapes.items(): self.same(before, Part.getShape(self.doc.getObject(name)))
        self.doc.Pad.Length = 8; self.doc.recompute()
        self.assertAlmostEqual(self.doc.Body.Shape.Volume, 32 * 3.141592653589793, places=7)
        self.assertEqual(self.doc.Use0.LinkedObject, self.doc.Use1.LinkedObject)
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), digest)

    def test_external_shared_mixed_definition_relocation_and_edit(self):
        self.mixed(); source = self.doc
        original, digest = self.original('ExternalOriginal')
        parent = App.newDocument('Parent'); parent.UndoMode = 1
        parent_original = self.output / 'ParentOriginal.FCStd'; parent.saveAs(str(parent_original))
        for i in range(2):
            link = parent.addObject('App::Link', 'External' + str(i)); link.setLink(source.Part)
            link.LinkTransform = False; link.LinkPlacement.Base.x = 80 + i * 30
        parent.recompute(); parent.save()
        parent_digest = hashlib.sha256(parent_original.read_bytes()).hexdigest()
        before = {o.Name: Part.getShape(o).copy() for o in (parent.External0, parent.External1)}
        CadDocument.convert_legacy(parent)
        with self.assertRaises(ValueError): parent.saveAs(str(self.output / 'Premature.cadprt'))
        source.saveAs(str(self.output / 'External.cadprt')); parent.saveAs(str(self.output / 'Parent.cadprt'))
        ids = source.Part.ObjectId, parent.External0.ObjectId, parent.External1.ObjectId
        self.close_all(); relocated = self.output / 'relocated'; relocated.mkdir(exist_ok=True)
        for name in ('External.cadprt', 'Parent.cadprt'): shutil.copy2(self.output / name, relocated / name)
        self.doc = CadDocument.open(relocated / 'Parent.cadprt')
        a, b = self.doc.External0, self.doc.External1; source = a.LinkedObject.Document
        self.assertEqual(a.LinkedObject, b.LinkedObject)
        self.assertEqual((a.LinkedObject.ObjectId, a.ObjectId, b.ObjectId), ids)
        self.assertEqual(Path(source.FileName).resolve(), (relocated / 'External.cadprt').resolve())
        for name, shape in before.items(): self.same(shape, Part.getShape(self.doc.getObject(name)))
        source.Pad.Length = 8; source.recompute(); self.doc.recompute()
        self.assertAlmostEqual(source.Body.Shape.Volume, 32 * 3.141592653589793, places=7)
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), digest)
        self.assertEqual(hashlib.sha256(parent_original.read_bytes()).hexdigest(), parent_digest)

    def test_actual_standard_open_mixed_models_tree_and_native_history(self):
        from PySide import QtCore, QtWidgets
        self.mixed(); original, digest = self.original('OpenMixed'); self.close_all()
        App.ParamGet('User parameter:BaseApp/Preferences/Dialog').SetBool('DontUseNativeDialog', True)
        handled = []; attempts = [0]
        def choose():
            attempts[0] += 1; dialog = QtWidgets.QApplication.activeModalWidget()
            with (self.output / 'open-dialog.log').open('a') as trace:
                trace.write(str((attempts[0], type(dialog).__name__, dialog.windowTitle() if dialog else None)) + '\n')
            if isinstance(dialog, QtWidgets.QFileDialog):
                dialog.setAttribute(QtCore.Qt.WA_DontShowOnScreen, True)
                dialog.setDirectory(str(original.parent)); dialog.selectFile(original.name)
                with (self.output / 'open-dialog.log').open('a') as trace:
                    trace.write(str((dialog.selectedFiles(), dialog.nameFilters())) + '\n')
                handled.append(True); dialog.accept()
                if dialog.isVisible() and attempts[0] < 100: QtCore.QTimer.singleShot(50, choose)
            elif attempts[0] < 100: QtCore.QTimer.singleShot(50, choose)
            elif dialog: dialog.reject()
        watchdog = QtCore.QTimer(); watchdog.setInterval(1000); ticks = [0]
        def inspect_modal():
            ticks[0] += 1; dialog = QtWidgets.QApplication.activeModalWidget()
            with (self.output / 'open-dialog.log').open('a') as trace:
                trace.write(str(('watch', ticks[0], type(dialog).__name__,
                                 dialog.text() if isinstance(dialog, QtWidgets.QMessageBox) else '')) + '\n')
            if isinstance(dialog, QtWidgets.QMessageBox) or ticks[0] >= 15:
                if dialog: dialog.reject()
        watchdog.timeout.connect(inspect_modal); watchdog.start()
        QtCore.QTimer.singleShot(50, choose)
        try: Gui.runCommand('Std_Open')
        finally: watchdog.stop()
        self.assertTrue(handled); self.doc = App.ActiveDocument
        import importlib
        ComponentNavigator = importlib.import_module("freecad.gui.ComponentNavigator")
        panel = ComponentNavigator.show(self.doc); panel.refresh()
        self.assertEqual(panel.models.topLevelItemCount(), 3)
        self.assertEqual(panel.structure.topLevelItem(0).text(0), self.doc.Label)
        alias = next(o for o in Model.history(self.doc.Part) if getattr(o, 'LegacyDressUpSource', None) == self.doc.Fillet)
        self.open_row(self.doc.Part, alias)
        self.assertEqual(Gui.getDocument(self.doc.Name).getInEdit().Object, self.doc.Fillet)
        Gui.Control.activeTaskDialog().reject(); Gui.updateGui(); self.doc.recompute()
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), digest)

    def test_legacy_draft_cam_consumers_after_conversion_edit_undo_and_reopen(self):
        from draftmake.make_clone import make_clone
        from Path.Main import Job
        _, _, body, sketch, pad, *_ = self.mixed()
        clone = make_clone(body, forcedraft=True); clone.Label = 'Legacy Draft consumer'
        job = Job.Create('LegacyJob', [body]); self.doc.recompute()
        names = clone.Name, job.Name; initial = body.Shape.Volume
        original, digest = self.original('ConsumersOriginal')
        CadDocument.convert_legacy(self.doc)
        self.assertAlmostEqual(clone.Shape.Volume, initial, places=7)
        self.assertAlmostEqual(job.Model.Group[0].Shape.Volume, initial, places=7)
        saved = self.output / 'Consumers.cadprt'; self.doc.saveAs(str(saved)); self.close_all()
        self.doc = CadDocument.open(saved); clone, job = [self.doc.getObject(n) for n in names]
        with Model.transaction(self.doc, 'Edit migrated consumer input'): self.doc.Pad.Length = 8
        self.assertAlmostEqual(clone.Shape.Volume, self.doc.Body.Shape.Volume, places=7)
        self.assertAlmostEqual(job.Model.Group[0].Shape.Volume, self.doc.Body.Shape.Volume, places=7)
        self.doc.undo(); self.doc.recompute(); self.assertAlmostEqual(clone.Shape.Volume, initial, places=7)
        self.doc.redo(); self.doc.recompute(); self.assertGreater(clone.Shape.Volume, initial)
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), digest)

    def test_legacy_drawing_consumer_after_conversion_and_cold_restore(self):
        from PySide import QtCore
        import TechDraw
        _, _, body, sketch, pad, *_ = self.mixed()
        page = self.doc.addObject('TechDraw::DrawPage', 'Page')
        template = self.doc.addObject('TechDraw::DrawSVGTemplate', 'Template')
        template.Template = App.getResourceDir() + 'Mod/TechDraw/Templates/ISO/A3_Landscape_blank.svg'; page.Template = template
        view = self.doc.addObject('TechDraw::DrawViewPart', 'View'); view.Source = [body]
        view.Direction = App.Vector(0, 0, 1); page.addView(view); self.doc.recompute()
        def wait(radius):
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                QtCore.QCoreApplication.processEvents()
                edges = view.getVisibleEdges()
                if len(edges) == 1 and abs(edges[0].Curve.Radius - radius) < 1e-6: return
                loop = QtCore.QEventLoop(); QtCore.QTimer.singleShot(25, loop.quit); loop.exec_()
            self.fail('Legacy drawing did not refresh its original Body')
        wait(2); CadDocument.convert_legacy(self.doc); self.doc.recompute(); wait(2)
        saved = self.output / 'Drawing.cadprt'; self.doc.saveAs(str(saved)); self.close_all()
        self.doc = CadDocument.open(saved); view = self.doc.View; wait(2)
        self.doc.Sketch.setDatum(0, App.Units.Quantity('3 mm')); self.doc.recompute(); wait(3)
        self.assertEqual(view.Source, [self.doc.Body]); self.assertNotIn('Invalid', view.State)

    def test_whole_file_recovery_preserves_native_history_and_reopens_geometry(self):
        assembly, part, body, sketch, pad, native, *_ = self.mixed()
        part.setExpression('Placement.Base.x', '15 mm'); self.doc.recompute()
        before = Part.getShape(assembly).copy(); groups = list(body.Group), list(native.Group)
        original, digest = self.original('RecoveryOriginal'); CadDocument.convert_legacy(self.doc)
        outputs = Model.finished_results(Model.children(Model.metadata(self.doc).RootComponent)[0].LinkedObject)
        self.assertTrue(any('dumb geometry' in x for x in Model.metadata(self.doc).ConversionReport))
        recovered = next(o for o in outputs if o.LegacyRecovery.startswith('Assembly:'))
        self.same(before, recovered.Shape); self.assertEqual((body.Group, native.Group), groups)
        saved = self.output / 'Recovery.cadprt'; self.doc.saveAs(str(saved)); self.close_all()
        self.doc = CadDocument.open(saved)
        self.assertEqual(self.doc.Body.Tip, self.doc.Pad); self.assertTrue(self.doc.Part.ExpressionEngine)
        recovered = next(o for o in Model.finished_results(Model.children(Model.metadata(self.doc).RootComponent)[0].LinkedObject)
                         if o.LegacyRecovery.startswith('Assembly:'))
        self.same(before, recovered.Shape); self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), digest)
