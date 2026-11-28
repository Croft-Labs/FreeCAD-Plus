# SPDX-License-Identifier: LGPL-2.1-or-later
"""History presentation on real native/Plus features, without model mutation."""
import os
import unittest
from pathlib import Path
import FreeCAD as App, FreeCADGui as Gui, Part
from PySide6 import QtCore, QtGui, QtTest
from freecad_plus import document, modeling, extrusion, panel, history_operations as operations
from TestDesignInteractions import TestDesignInteractions, settle


class TestHistoryOperations(unittest.TestCase):
    setUp = TestDesignInteractions.setUp
    tearDown = TestDesignInteractions.tearDown
    dialog = TestDesignInteractions.dialog

    def circle(self, radius, z=0):
        sketch = modeling.new_sketch(self.doc)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), radius), False)
        sketch.Placement.Base.z = z; self.doc.recompute()
        return sketch

    def fixture(self, subtract=True):
        profile = self.circle(10)
        first = extrusion.save(self.doc, [(profile, '')], {}, {'length': 8.})
        profile2 = self.circle(6, 8)
        second = extrusion.save(self.doc, [(profile2, '')], {'target': (first, '')},
                                {'length': 4., 'operation': 'Add'})
        first.Label = 'extrude001'; second.Label = 'extrude002'
        features = [first, second]
        if subtract:
            profile3 = self.circle(3)
            third = extrusion.save(self.doc, [(profile3, '')], {'target': (second, '')},
                                   {'length': 12., 'operation': 'Subtract'})
            third.Label = 'extrude003'; features.append(third)
        self.panel.refresh(); settle()
        return features, profile2

    def item(self, obj):
        return next(i for i in self.panel._maps[2].values()
                    if i.data(0, panel._ROLE).ref == panel.identity(obj))

    def test_real_extrusions_labels_icons_selection_and_visibility(self):
        features, _ = self.fixture()
        before = [(o.Name, o.Label, o.ID, o.Shape.Volume, o.Visibility) for o in features]
        undo = self.doc.UndoCount
        native = [o.ViewObject.Icon.pixmap(32, 32).toImage() for o in features]
        for _ in range(3):self.panel.refresh()
        self.assertEqual([self.item(o).text(0) for o in features],
                         ['extrude001 (new body)', 'extrude002 (add)', 'extrude003 (subtract)'])
        icons = [self.item(o).icon(0).pixmap(32, 32).toImage() for o in features]
        self.assertEqual(icons[0], icons[1]); self.assertNotEqual(icons[0], icons[2])
        self.assertEqual(native, [o.ViewObject.Icon.pixmap(32, 32).toImage() for o in features])
        self.assertEqual(before, [(o.Name, o.Label, o.ID, o.Shape.Volume, o.Visibility) for o in features])
        self.assertEqual(self.doc.UndoCount, undo)
        item = self.item(features[-1]); tree = self.panel.trees[2]; tree.setCurrentItem(item); settle()
        selected = Gui.Selection.getSelectionEx('', 0)
        self.assertEqual(len(selected), 1)
        self.assertEqual((selected[0].DocumentName, selected[0].ObjectName, selected[0].SubElementNames[0]),
                         item.data(0, panel._ROLE).selection)
        row = item.data(0, panel._ROLE); shown = panel.history_visible(self.owner, features[-1])
        self.panel.toggle_history_visibility(row); settle()
        self.assertNotEqual(panel.history_visible(self.owner, features[-1]), shown)
        self.doc.undo(); settle(); self.assertEqual(panel.history_visible(self.owner, features[-1]), shown)
        Gui.Selection.clearSelection(); self.panel.refresh(); settle()
        self.panel.grab().save(str(Path(os.environ['PLUS_TEST_DIR']) / 'installed-history-operations.png'))

    def test_edit_mode_rename_and_undo_refresh_without_accumulating_suffix(self):
        features, profile = self.fixture(False); first, feature = features
        identity = feature.ID; undo = self.doc.UndoCount
        extrusion.save(self.doc, [(profile, '')], {'target': (first, '')},
                       {'length': 4., 'operation': 'Subtract', 'reverse': True}, feature)
        settle(); self.assertEqual(feature.ID, identity)
        self.assertEqual(self.item(feature).text(0), 'extrude002 (subtract)')
        self.assertEqual(self.doc.UndoCount, undo + 1)
        self.doc.undo(); settle(); self.assertEqual(self.item(feature).text(0), 'extrude002 (add)')
        with document.transaction(self.doc, 'Rename feature'):feature.Label = 'Bore (revision A)'
        settle(); self.assertEqual(self.item(feature).text(0), 'Bore (revision A) (add)')
        self.panel.refresh(); self.assertEqual(feature.Label, 'Bore (revision A)')
        self.assertEqual(self.item(feature).text(0), 'Bore (revision A) (add)')

    def test_save_reopen_keeps_raw_labels_and_derived_presentation(self):
        features, _ = self.fixture(); names = [o.Name for o in features]
        expected = [(o.Label, o.ID, o.Shape.Volume) for o in features]
        path = Path(os.environ['PLUS_TEST_DIR']) / 'HistoryOperations.cadprt'
        document.save_document(self.doc, path); App.closeDocument(self.doc.Name)
        self.doc = document.open_document(path); self.owner = document.validate(self.doc).Definitions[0]
        self.panel = panel.show_panel(); self.panel.tabs.setCurrentIndex(2); self.panel.refresh(); settle()
        reopened = [self.doc.getObject(name) for name in names]
        self.assertEqual(expected, [(o.Label, o.ID, o.Shape.Volume) for o in reopened])
        self.assertEqual([self.item(o).text(0) for o in reopened],
                         ['extrude001 (new body)', 'extrude002 (add)', 'extrude003 (subtract)'])
        self.assertEqual(self.doc.UndoCount, 0)

    def test_supported_engine_schema_sheet_and_unknown_settings(self):
        obj = self.owner.newObject('Part::Feature', 'SchemaFixture')
        obj.Shape = Part.makePlane(10, 10)
        for engine in ('Extrude', 'Revolve', 'Loft', 'Thicken'):
            version = 'Plus' + engine + 'Version'; mode = engine + '_operation'; output = engine + '_output'
            obj.addProperty('App::PropertyInteger', version); setattr(obj, version, 1)
            obj.addProperty('App::PropertyString', mode); obj.addProperty('App::PropertyString', output)
            setattr(obj, output, 'Solid')
            for value, suffix in (('New Solid', 'new body'), ('Add', 'add'), ('Subtract', 'subtract')):
                setattr(obj, mode, value); self.assertEqual(operations.describe(obj), (value, suffix))
            setattr(obj, mode, 'New Solid'); setattr(obj, output, 'Sheet')
            self.assertEqual(operations.describe(obj), ('New Solid', 'new surface'))
            setattr(obj, mode, 'Subtract'); self.assertIsNone(operations.describe(obj))
            setattr(obj, version, 99); self.assertIsNone(operations.describe(obj))
            for prop in (version, mode, output):obj.removeProperty(prop)
        obj.Label = 'Extrude Add Subtract (new body)'
        self.assertIsNone(operations.describe(obj))
        icon = obj.ViewObject.Icon; text, unchanged = operations.presentation(obj, obj.Label, icon)
        self.assertEqual(text, obj.Label); self.assertEqual(unchanged.cacheKey(), icon.cacheKey())

    def test_native_additive_predecessor_subtractive_and_surface(self):
        body = self.owner.newObject('PartDesign::Body', 'NativeBody')
        first = body.newObject('PartDesign::AdditiveBox', 'FirstBox')
        first.Length = 10; first.Width = 10; first.Height = 10; self.doc.recompute()
        self.assertEqual(operations.describe(first), ('New Solid', 'new body'))
        second = body.newObject('PartDesign::AdditiveBox', 'SecondBox')
        second.Length = 12; second.Width = 10; second.Height = 10; self.doc.recompute()
        self.assertEqual(second.BaseFeature, first)
        self.assertEqual(operations.describe(second), ('Add', 'add'))
        cut = body.newObject('PartDesign::SubtractiveBox', 'CutBox')
        self.assertEqual(operations.describe(cut), ('Subtract', 'subtract'))
        sheet = self.owner.newObject('Part::Extrusion', 'NativeExtrusion'); sheet.Solid = False
        self.assertEqual(operations.describe(sheet), ('New Solid', 'new surface'))
        sheet.Solid = True; self.assertEqual(operations.describe(sheet), ('New Solid', 'new body'))
        unknown = self.owner.newObject('Part::Feature', 'Unknown')
        second.BaseFeature = unknown
        self.assertIsNone(operations.describe(second))

    def test_icon_cache_and_untouched_coordinate_and_sketch_rows(self):
        profile = self.circle(5); self.panel.refresh(); settle()
        self.assertEqual(self.item(profile).text(0), profile.Label)
        self.assertIsNone(operations.describe(profile))
        for obj in self.owner.Origin.OriginFeatures:self.assertIsNone(operations.describe(obj))
        icon = Gui.getIcon('PartDesign_Pad'); original = icon.pixmap(32, 32).toImage()
        new = operations.colored(icon, 'New Solid'); add = operations.colored(icon, 'Add')
        self.assertEqual(new.cacheKey(), add.cacheKey())
        self.assertNotEqual(new.pixmap(32, 32).toImage(), operations.colored(icon, 'Subtract').pixmap(32, 32).toImage())
        self.assertEqual(original, icon.pixmap(32, 32).toImage())
        self.assertLessEqual(len(operations._icons), 256)
        # Bright yellow highlights can exceed an 8-bit channel after shading.
        # Check the renderer's diagnostics, not just final pixel similarity.
        image = QtGui.QImage(16, 16, QtGui.QImage.Format_ARGB32)
        image.fill(QtGui.QColor(254, 250, 224))
        messages = []; previous = QtCore.qInstallMessageHandler(lambda kind, context, text: messages.append(text))
        try:
            bright = operations.colored(QtGui.QIcon(QtGui.QPixmap.fromImage(image)), 'New Solid')
            pixel = bright.pixmap(16, 16).toImage().pixelColor(0, 0)
        finally:
            QtCore.qInstallMessageHandler(previous)
        self.assertEqual(messages, []); self.assertEqual(pixel.red(), 255)
        self.assertEqual(pixel.alpha(), 255)
