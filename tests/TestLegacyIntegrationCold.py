# SPDX-License-Identifier: LGPL-2.1-or-later
"""Fresh-process restore of the grouped installed migration corpus."""
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import CadDocument
import ComponentModel as Model


class TestLegacyIntegrationCold(unittest.TestCase):
    def setUp(self):
        self.output = Path(os.environ['FREECAD_PLUS_INTEGRATION_FIXTURES'])

    def tearDown(self):
        for name in list(App.listDocuments()): App.closeDocument(name)

    def test_mixed_restore_and_shared_edit_undo(self):
        doc = CadDocument.open(self.output / 'Mixed.cadprt'); doc.UndoMode = 1
        self.assertEqual(doc.Body.Producer, doc.Pad)
        self.assertEqual(Model.owner(doc.Fillet), doc.NativeBody)
        self.assertEqual(doc.Use0.LinkedObject, doc.Use1.LinkedObject)
        before = doc.Body.Shape.Volume
        with Model.transaction(doc, 'Cold edit migrated Pad'): doc.Pad.Length = 9
        self.assertGreater(doc.Body.Shape.Volume, before)
        doc.undo(); doc.recompute(); self.assertAlmostEqual(doc.Body.Shape.Volume, before, places=7)
        doc.redo(); doc.recompute(); self.assertGreater(doc.Body.Shape.Volume, before)
        import importlib
        ComponentNavigator = importlib.import_module("freecad.gui.ComponentNavigator")
        panel = ComponentNavigator.show(doc); panel.refresh()
        self.assertEqual(panel.structure.topLevelItem(0).text(0), doc.Label)

    def test_relocated_external_full_restore_and_shared_update(self):
        doc = CadDocument.open(self.output / 'relocated' / 'Parent.cadprt')
        a, b = doc.External0, doc.External1; self.assertEqual(a.LinkedObject, b.LinkedObject)
        source = a.LinkedObject.Document
        self.assertEqual(Path(source.FileName).resolve(), (self.output / 'relocated' / 'External.cadprt').resolve())
        before = source.Body.Shape.Volume; source.Pad.Length = 9; source.recompute(); doc.recompute()
        self.assertGreater(source.Body.Shape.Volume, before)
        self.assertEqual(a.LinkedObject, b.LinkedObject); Model.validate(doc)

    def test_native_payload_and_explicit_recovery_restore(self):
        doc = CadDocument.open(self.output / 'Recovery.cadprt')
        self.assertEqual(doc.Body.Tip, doc.Pad)
        self.assertTrue(doc.Part.ExpressionEngine)
        outputs = Model.finished_results(Model.children(Model.metadata(doc).RootComponent)[0].LinkedObject)
        self.assertTrue(outputs); self.assertTrue(all(not o.Shape.isNull() for o in outputs))
        self.assertTrue(any('dumb geometry' in x for x in Model.metadata(doc).ConversionReport))
