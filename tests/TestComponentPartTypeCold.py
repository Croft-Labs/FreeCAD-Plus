# SPDX-License-Identifier: LGPL-2.1-or-later
"""Fresh-process acceptance of saved Part Type contexts and native exports."""
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import ComponentModel as Model
import CadDocument
from PySide import QtCore, QtWidgets
from freecad.gui import ComponentNavigator as Navigator


class TestComponentPartTypeCold(unittest.TestCase):
    def setUp(self):
        self.assertFalse(App.listDocuments(), "Cold checks require no open documents")
        self.fixtures = Path(os.environ["FREECAD_PLUS_EDIT_FIXTURES"])
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])

    def tearDown(self):
        for name in list(App.listDocuments()):
            App.closeDocument(name)

    def edit(self, panel, definition):
        iterator = QtWidgets.QTreeWidgetItemIterator(panel.models)
        while iterator.value():
            row = iterator.value()
            if row.data(0, QtCore.Qt.UserRole) == Navigator.object_key(definition):
                panel.edit_model(row)
                panel.refresh()
                return
            iterator += 1
        self.fail("Missing definition in Models")

    def testSavedOwnerContextRestoresAndSwitches(self):
        filename = self.fixtures / "part-type-context.cadprt"
        data = CadDocument.preflight(filename)
        self.assertIn("component-part-types-v1", data["required"])
        self.assertIn("component-active-part-type-v1", data["required"])
        doc = CadDocument.open(filename)
        top = next(d for d in Model.definitions(doc) if d.Label == "Top plate")
        assembly = next(d for d in Model.definitions(doc) if d.Label == "Fan assembly")
        bottom = next(c for c in Model.children(top) if c.LinkedObject.Label == "Bottom plate")
        fan = next(c for c in Model.children(bottom.LinkedObject) if c.LinkedObject.Label == "Fan")
        panel = Navigator.show(doc)
        self.edit(panel, top)
        root = Navigator.resolve(panel.root_key)
        ids = list(panel.active_path)
        self.assertEqual(Model.effective_part_type(root, ids, ids), "Bodies Only")
        self.assertEqual(panel.structure.headerItem().text(3), "Part Type")
        self.assertEqual(Model.effective_part_type(root, ids + [bottom.ObjectId], ids), "Reference")
        self.assertEqual(Model.effective_part_type(root, ids + [bottom.ObjectId, fan.ObjectId], ids), "Excluded")
        expected = bottom.Name + "." + bottom.LinkedObject.Name + "Guide."
        plan = Navigator.context_display_plan(root, ids)
        self.assertTrue(any(path.endswith(expected) for path, obj, floor in plan))
        self.edit(panel, assembly)
        self.assertEqual(Model.effective_part_type(root, ids + [bottom.ObjectId], panel.active_path), "Excluded")
        self.edit(panel, top)
        self.assertEqual(Model.active_part_type(top), "Bodies Only")
        self.assertEqual(Model.part_type(top, bottom), "Reference")
        self.assertEqual(Model.part_type(bottom.LinkedObject, fan), "Excluded")
        Gui.updateGui()
        panel.grab().save(str(self.output / "cold-part-types.png"))

    def testPromotedResultExportsOnceAfterColdReopen(self):
        doc = CadDocument.open(self.fixtures / "native-save.cadprt")
        root = Model.owner(doc.getObject("LocalBody"))
        source = next(c for c in Model.children(root) if c.LinkedObject.Label == "Source")
        self.assertEqual(Model.part_type(root, source), "Reference")
        references = [o for o in Model.history(root) if o.ComponentRole == "Reference"]
        self.assertEqual(len(references), 1)
        Model.activate(root)
        with self.assertRaises(ValueError):
            Model.require_geometry_access(source)
        path = self.output / "cold-promoted.step"
        Part.export([root], str(path))
        shape = Part.read(str(path))
        self.assertEqual(len(shape.Solids), 2)
        self.assertAlmostEqual(shape.Volume, 36)
        doc.getObject("SourceBody").Shape = Part.makeBox(4, 3, 4)
        doc.recompute()
        Model.activate(root)
        self.assertAlmostEqual(sum(s.Volume for s in Model.output_shapes(root)), 60)