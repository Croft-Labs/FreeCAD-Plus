# SPDX-License-Identifier: LGPL-2.1-or-later
"""Cold-process reopen of the packaged editing batch's native file fixtures."""
import hashlib
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import ComponentModel as Model
import CadDocument
from freecad.gui import ComponentNavigator as Navigator


class TestComponentEditingCold(unittest.TestCase):
    def setUp(self):
        self.assertFalse(App.listDocuments(), 'Cold acceptance requires no open documents')
        self.fixtures = Path(os.environ['FREECAD_PLUS_EDIT_FIXTURES'])

    def tearDown(self):
        for name in list(App.listDocuments()):
            App.closeDocument(name)

    def testFixedRelationshipAndOriginOnlyHistoryReopen(self):
        filename = self.fixtures / 'file-relationships.cadprt'
        expected = CadDocument.preflight(filename)['assembly']
        doc = CadDocument.open(filename)
        self.assertEqual(Model.assembly_record(doc), expected)
        self.assertEqual(Model.assembly_context(doc).solve(), 0)
        root = Model.metadata(doc).RootComponent
        self.assertTrue(Model.is_file_container(root))
        self.assertEqual(root.ModelHistory, [])
        self.assertEqual(root.ResultObjects, [])
        self.assertAlmostEqual(Model.children(root)[1].LinkPlacement.Base.x, 15, places=5)
        panel = Navigator.show(doc)
        panel.activate_item(panel.structure.topLevelItem(0))
        panel.refresh()
        self.assertEqual(panel.active_key, Navigator.object_key(root))
        self.assertEqual(panel.history.topLevelItemCount(), 1)
        Gui.updateGui()
        panel.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "file-history.png"))

    def testExternalDefinitionRemainsUnchangedAfterColdSolve(self):
        hardware = self.fixtures / 'transaction-hardware.cadprt'
        before = hashlib.sha256(hardware.read_bytes()).digest()
        doc = CadDocument.open(self.fixtures / 'transaction-assembly.cadprt')
        root = Model.metadata(doc).RootComponent
        second = Model.children(root)[1]
        self.assertNotEqual(second.LinkedObject.Document, doc)
        self.assertTrue(second.LinkedObject.Placement.isIdentity())
        self.assertEqual(Model.assembly_context(doc).solve(), 0)
        self.assertAlmostEqual(second.LinkPlacement.Base.x, 15, places=5)
        self.assertEqual(hashlib.sha256(hardware.read_bytes()).digest(), before)
        panel = Navigator.show(doc)
        panel.activate_item(panel.structure.topLevelItem(0))
        self.assertEqual(Gui.activeDocument().Document, doc)
        self.assertEqual(root.ModelHistory, [])
