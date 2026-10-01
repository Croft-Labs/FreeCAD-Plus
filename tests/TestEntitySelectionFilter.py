# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native selection policy, gate coexistence and UI recovery checks."""
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui import EntitySelectionFilter as Filters
from TestClarifySelection import TestClarifySelection as _ClarifyFixture, leaves, choose


class TestEntitySelectionFilter(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = App.newDocument("EntityFilterTest")
        self.box = self.doc.addObject("Part::Box", "Box")
        self.doc.recompute()
        Filters.set_mode(0)
        Gui.Selection.clearSelection()

    def tearDown(self):
        Filters.set_mode(0)
        Gui.Selection.removeSelectionGate()
        Gui.Selection.clearSelection()
        if Filters._panel is not None:
            Filters._panel.close()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        QtWidgets.QApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)

    def pick(self, sub, obj=None):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(obj or self.box, sub)
        return Gui.Selection.getSelectionEx("*", 0)

    def test_entity_modes_restrict_native_add_selection(self):
        for mode, allowed in ((1, "Vertex1"), (2, "Edge1"), (3, "Face1"), (4, "")):
            Filters.set_mode(mode)
            for sub in ("Vertex1", "Edge1", "Face1", ""):
                with self.subTest(mode=mode, sub=sub):
                    self.assertEqual(bool(self.pick(sub)), sub == allowed)
        Filters.set_mode(0)
        for sub in ("Vertex1", "Edge1", "Face1", ""):
            self.assertTrue(self.pick(sub))

    def test_command_gate_refines_filter_and_removal_retains_policy(self):
        class OnlyFirstFace:
            def allow(self, doc, obj, sub):
                return sub == "Face1"
        Filters.set_mode(3)
        Gui.Selection.addSelectionGate(OnlyFirstFace())
        self.assertTrue(self.pick("Face1"))
        self.assertFalse(self.pick("Face2"))
        self.assertFalse(self.pick("Edge1"))
        Filters.set_mode(0)
        self.assertFalse(self.pick("Face2"), "Reset must not remove a command gate")
        Filters.set_mode(3)
        Gui.Selection.removeSelectionGate()
        self.assertTrue(self.pick("Face2"))
        self.assertFalse(self.pick(""))

    def test_repeated_nested_occurrences_keep_exact_paths(self):
        assembly = self.doc.addObject("App::Part", "Assembly")
        for name in ("First", "Second"):
            link = self.doc.addObject("App::Link", name)
            link.setLink(self.box)
            assembly.addObject(link)
        self.doc.recompute()
        Filters.set_mode(3)
        for path in ("First.Face1", "Second.Face1"):
            selected = self.pick(path, assembly)
            self.assertEqual(len(selected), 1)
            self.assertEqual(selected[0].Object.Name, assembly.Name)
            self.assertEqual(selected[0].SubElementNames, (path,))
        self.assertFalse(self.pick("First.", assembly))
        Filters.set_mode(4)
        self.assertTrue(self.pick("First.", assembly))
        self.assertFalse(self.pick("First.Face1", assembly))

    def test_filter_preserves_existing_selection_geometry_and_undo(self):
        self.doc.UndoMode = 1
        Gui.Selection.addSelection(self.box, "Edge1")
        shape = self.box.Shape.exportBrepToString()
        undo = self.doc.UndoCount
        for mode in (3, 1, 4, 0):
            Filters.set_mode(mode)
            self.assertEqual(Gui.Selection.getSelectionEx()[0].SubElementNames, ("Edge1",))
        self.assertEqual(shape, self.box.Shape.exportBrepToString())
        self.assertEqual(undo, self.doc.UndoCount)

    def test_preselection_respects_filter_and_reset_clears_hover(self):
        Filters.set_mode(3)
        Gui.Selection.setPreselection(self.box, "Face1", tp=0)
        self.assertEqual(Gui.Selection.getPreselection().SubElementNames, ("Face1",))
        Gui.Selection.clearPreselection()
        Gui.Selection.setPreselection(self.box, "Edge1", tp=0)
        self.assertFalse(Gui.Selection.getPreselection().ObjectName)
        Gui.Selection.setPreselection(self.box, "Face1", tp=0)
        Filters.set_mode(0)
        self.assertFalse(Gui.Selection.getPreselection().ObjectName)

    def test_visible_reset_and_escape_restore_all(self):
        Gui.runCommand("Std_EntitySelectionFilter")
        panel = Filters._panel
        panel.combo.setCurrentIndex(3)
        self.assertEqual(Filters.mode(), 3)
        self.assertFalse(panel.indicator.isHidden())
        panel.indicator.click()
        self.assertEqual(Filters.mode(), 0)
        self.assertTrue(panel.indicator.isHidden())
        panel.combo.setCurrentIndex(2)
        from TestClarifySelection import QtTest
        QtTest.QTest.keyClick(panel, QtCore.Qt.Key_Escape)
        self.assertEqual(Filters.mode(), 0)
        self.assertFalse(panel.isVisible())
        self.assertTrue(self.pick("Face1"))

    def test_close_and_startup_reset_and_invalid_mode(self):
        Gui.runCommand("Std_EntitySelectionFilter")
        Filters._panel.combo.setCurrentIndex(1)
        Filters._panel.close()
        self.assertEqual(Filters.mode(), 0)
        Filters.set_mode(3)
        Filters.registerCommand()
        self.assertEqual(Filters.mode(), 0)
        for value in (-1, 5, True, "Face"):
            with self.assertRaises(ValueError):
                Filters.set_mode(value)

    def test_command_is_in_modeling_workbench_menu(self):
        # NoneWorkbench intentionally has no Visibility menu; use native Part.
        Gui.activateWorkbench("PartWorkbench")
        def commands(menu):
            for action in menu.actions():
                yield action.text().replace("&", "")
                if action.menu():
                    yield from commands(action.menu())
        self.assertIn("Selection filters…", list(commands(Gui.getMainWindow().menuBar())))


# Reuse the native ray-menu fixture without inheriting/re-running its test methods.
class TestFilteredRayMenu(unittest.TestCase):
    setUp = _ClarifyFixture.setUp
    menu = _ClarifyFixture.menu

    def tearDown(self):
        Filters.set_mode(0)
        from TestClarifySelection import TestClarifySelection
        TestClarifySelection.tearDown(self)

    def test_face_only_native_menu(self):
        Filters.set_mode(3)
        def drive(menu):
            entries = leaves(menu)
            self.assertTrue(entries)
            self.assertTrue(all("Face" in action.text() for _, action, _ in entries))
            choose(entries[0])
        self.menu(drive)
        selected = Gui.Selection.getSelectionEx()
        self.assertTrue(selected)
        self.assertTrue(selected[0].SubElementNames[0].startswith("Face"))

    def test_changed_filter_refuses_old_menu_candidate(self):
        Filters.set_mode(3)
        def drive(menu):
            entries = leaves(menu)
            self.assertTrue(entries)
            Filters.set_mode(2)
            choose(entries[0])
        self.menu(drive)
        self.assertFalse(Gui.Selection.getSelection())


# The imported fixture is not an additional suite in this module.
del _ClarifyFixture
