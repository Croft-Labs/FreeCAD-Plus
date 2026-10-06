# SPDX-License-Identifier: LGPL-2.1-or-later
"""Selection policy fixtures; native gates/command tests require the grouped build."""
import math
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtGui, QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest
from freecad.gui import DesignSelection as Policy


class TestDesignSelectionPolicy(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("DesignSelectionPolicy")
        self.params = Policy.parameters()
        self.old = (self.params.GetBool("Active", False),
                    self.params.GetInt("Categories", Policy.ALL),
                    self.params.GetBool("Persistent", True))
        self.params.SetBool("Active", True)
        self.params.SetInt("Categories", Policy.ALL)

    def tearDown(self):
        Gui.Selection.clearSelection()
        App.closeDocument(self.doc.Name)
        self.params.SetBool("Active", self.old[0])
        self.params.SetInt("Categories", self.old[1])
        self.params.SetBool("Persistent", self.old[2])

    def sketch(self, owner=None):
        sketch = self.doc.addObject("Sketcher::SketchObject", "Sketch")
        if owner:
            owner.addObject(sketch)
        sketch.addGeometry(Part.LineSegment(App.Vector(0, 0, 0), App.Vector(10, 0, 0)))
        sketch.addGeometry(Part.LineSegment(App.Vector(10, 0, 0), App.Vector(20, 0, 0)), True)
        sketch.addGeometry(Part.LineSegment(App.Vector(20, 0, 0), App.Vector(20, 10, 0)))
        self.doc.recompute()
        return sketch

    def test_sketch_inside_body_is_still_drawing_geometry(self):
        body = self.doc.addObject("PartDesign::Body", "Body")
        sketch = self.sketch(body)
        self.assertEqual(Policy.category(sketch, "Edge1"), "Curves")
        self.assertEqual(Policy.category(sketch, "Vertex1"), "Points")
        self.assertEqual(Policy.category(sketch, "RootPoint"), "Points")
        self.assertIsNone(Policy.category(sketch, "Constraint1"))

    def test_solid_sheet_wire_and_point_taxonomy(self):
        solid = self.doc.addObject("Part::Feature", "Solid")
        solid.Shape = Part.makeBox(5, 5, 5)
        for sub, expected in (("", "Bodies"), ("Face1", "Faces"),
                              ("Edge1", "Edges"), ("Vertex1", "Vertices")):
            self.assertEqual(Policy.category(solid, sub), expected)
        sheet = self.doc.addObject("Part::Feature", "Sheet")
        sheet.Shape = Part.makePlane(5, 5)
        self.assertEqual(Policy.category(sheet, "Face1"), "Surfaces")
        wire = self.doc.addObject("Part::Feature", "SpatialCurve")
        wire.Shape = Part.makeLine(App.Vector(), App.Vector(1, 2, 3))
        self.assertEqual(Policy.category(wire, "Edge1"), "Curves")
        self.assertEqual(Policy.category(wire, "Vertex1"), "Points")

    def test_plane_and_origin_classification(self):
        part = self.doc.addObject("App::Part", "Part")
        self.assertEqual(Policy.category(part.Origin, ""), "Points")
        plane = next(o for o in part.Origin.OriginFeatures if o.isDerivedFrom("App::Plane"))
        self.assertEqual(Policy.category(plane, ""), "Planes")

    def test_independent_category_checkboxes_and_inactive_bypass(self):
        sketch = self.sketch()
        self.params.SetInt("Categories", 1 << Policy.CATEGORIES.index("Points"))
        self.assertFalse(Policy.allows(sketch, "Edge1"))
        self.assertTrue(Policy.allows(sketch, "Vertex1"))
        self.params.SetInt("Categories", 0)
        self.assertFalse(Policy.allows(sketch, "Vertex1"))
        self.params.SetBool("Active", False)
        self.assertTrue(Policy.allows(sketch, "Edge1"))

    def test_chain_preserves_construction_geometry_indices(self):
        sketch = self.sketch()
        self.assertEqual(Policy.chain_paths(sketch, "Edge1", 1), ["Edge1", "Edge2", "Edge3"])
        self.assertEqual(Policy.chain_paths(sketch, "Edge1", 2), ["Edge1", "Edge2"])
        self.assertEqual(Policy.chain_paths(sketch, "Edge1", 0), ["Edge1"])

    def test_repeated_occurrences_keep_the_picked_path(self):
        sketch = self.sketch()
        assembly = self.doc.addObject("App::Part", "Assembly")
        for name in ("First", "Second"):
            link = self.doc.addObject("App::Link", name)
            link.setLink(sketch)
            assembly.addObject(link)
        self.doc.recompute()
        self.assertEqual(Policy.chain_paths(assembly, "Second.Edge1", 1),
                         ["Second.Edge1", "Second.Edge2", "Second.Edge3"])
        self.assertEqual(Policy.category(assembly, "Second.Vertex1"), "Points")

    def test_chain_does_not_cross_sketch_objects(self):
        first, second = self.sketch(), self.sketch()
        second.addGeometry(Part.LineSegment(App.Vector(20, 10, 0), App.Vector(30, 10, 0)))
        self.doc.recompute()
        self.assertEqual(Policy.chain_paths(first, "Edge1", 1), ["Edge1", "Edge2", "Edge3"])

    def test_closed_periodic_curve_seam_is_not_a_junction(self):
        sketch = self.doc.addObject("Sketcher::SketchObject", "Closed")
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 10))
        sketch.addGeometry(Part.LineSegment(App.Vector(10, 0, 0), App.Vector(20, 0, 0)))
        self.doc.recompute()
        self.assertEqual(Policy.chain_paths(sketch, "Edge1", 1), ["Edge1"])

    def test_branch_tolerance_and_loop_graph(self):
        def line(a, b):
            d = tuple(y-x for x, y in zip(a, b))
            length = math.sqrt(sum(x*x for x in d))
            d = tuple(x/length for x in d)
            return ((a, d), (b, d))
        graph = {1: line((0, 0, 0), (1, 0, 0)),
                 2: line((1, 0, 0), (2, 0, 0)),
                 3: line((1, 0, 0), (1, 1, 0))}
        self.assertEqual(Policy.connected_indices(graph, 1), [1, 2, 3])
        self.assertEqual(Policy.connected_indices(graph, 1, True), [1])
        graph[4] = line((2 + 2e-7, 0, 0), (3, 0, 0))
        self.assertNotIn(4, Policy.connected_indices(graph, 1))
        graph[5] = line((2, 0, 0), (0, 0, 0))
        self.assertEqual(Policy.connected_indices(graph, 1), [1, 2, 3, 5])

    def test_body_edges_form_connected_and_tangent_chains(self):
        box = self.doc.addObject("Part::Feature", "Box")
        box.Shape = Part.makeBox(3, 4, 5)
        self.doc.recompute()
        self.assertEqual(len(Policy.chain_paths(box, "Edge1", 1)), 12)
        self.assertEqual(Policy.chain_paths(box, "Edge1", 2), ["Edge1"])

    def test_shared_operation_policy_does_not_restore_deleted_entities(self):
        sketch = self.sketch()
        Gui.Selection.addSelection(sketch, "Edge1")
        self.params.SetBool("Persistent", True)
        Policy.finish_operation()
        self.assertTrue(Gui.Selection.getSelection())
        Gui.Selection.clearSelection()  # explicit deselection always wins
        Policy.finish_operation()
        self.assertFalse(Gui.Selection.getSelection())
        Gui.Selection.addSelection(sketch, "Edge1")
        self.doc.removeObject(sketch.Name)
        Policy.finish_operation()
        self.assertFalse(Gui.Selection.getSelection())
        other = self.sketch()
        Gui.Selection.addSelection(other, "Edge1")
        self.params.SetBool("Persistent", False)
        Policy.finish_operation()
        self.assertFalse(Gui.Selection.getSelection())


class TestDesignSelectionNative(TestDesignSelectionPolicy):
    """Run with rebuilt FreeCADGui AND SketcherGui, not a Python-only overlay."""
    def test_actual_sketch_click_single_connected_tangent_escape_and_empty_space(self):
        Gui.activateWorkbench("SketcherWorkbench")
        sketch = self.sketch()
        window = Gui.getMainWindow()
        from freecad.gui import PlusRibbon
        PlusRibbon.apply_preferences()
        PlusRibbon._ribbon.configure("Design","Sketch")
        PlusRibbon._ribbon.place_plus_bars()
        bar = PlusRibbon._ribbon.selection_toolbar
        self.assertIsNotNone(bar)
        original, enabled, cursor = bar.intent.currentIndex(), bar._enabled, QtGui.QCursor.pos()
        Gui.activeDocument().setEdit(sketch.Name)
        try:
            bar.set_design_active(True)
            view = Gui.activeDocument().activeView()
            view.viewTop()
            view.fitAll()
            QtTest.QTest.qWait(200)
            widgets = [w for w in window.findChildren(QtWidgets.QWidget)
                       if "GL" in w.metaObject().className() and w.width()>100 and w.height()>100]
            widget = max(widgets,key=lambda w:w.width()*w.height())
            ratio = widget.devicePixelRatioF()
            for mode,expected in ((0,{"Edge1"}),(1,{"Edge1","Edge2","Edge3"}),
                                  (2,{"Edge1","Edge2"})):
                bar.intent.setCurrentIndex(mode)
                Gui.Selection.clearSelection()
                x,y = view.getPointOnScreen(App.Vector(5,0,0))
                pixel = QtCore.QPoint(round(x/ratio),widget.height()-round(y/ratio)-1)
                QtTest.QTest.mouseMove(widget,pixel)
                QtTest.QTest.qWait(150)
                QtTest.QTest.mouseClick(widget,QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,pixel)
                QtTest.QTest.qWait(200)
                selected = {sub.rsplit(".",1)[-1].capitalize()
                            for entry in Gui.Selection.getSelectionEx("*",0)
                            for sub in entry.SubElementNames}
                self.assertEqual(selected,expected)
            QtTest.QTest.keyClick(widget,QtCore.Qt.Key_Escape)
            QtTest.QTest.qWait(150)
            self.assertFalse(Gui.Selection.getSelection())
            Gui.Selection.addSelection(sketch,"Edge1")
            QtTest.QTest.mouseClick(widget,QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,QtCore.QPoint(8,8))
            QtTest.QTest.qWait(150)
            self.assertFalse(Gui.Selection.getSelection())
        finally:
            bar.intent.setCurrentIndex(original)
            bar.set_design_active(enabled)
            QtGui.QCursor.setPos(cursor)
            Gui.activeDocument().resetEdit()

    def test_native_gate_intersection(self):
        sketch = self.sketch()
        class FirstOnly:
            def allow(self, doc, obj, sub):
                return sub == "Edge1"
        try:
            Gui.Selection.addSelectionGate(FirstOnly())
            self.params.SetInt("Categories", 1 << Policy.CATEGORIES.index("Points"))
            Gui.Selection.addSelection(sketch, "Edge1")
            self.assertFalse(Gui.Selection.getSelection())
            self.params.SetInt("Categories", 1 << Policy.CATEGORIES.index("Curves"))
            Gui.Selection.addSelection(sketch, "Edge1")
            Gui.Selection.addSelection(sketch, "Edge2")
            self.assertEqual(Gui.Selection.getSelectionEx()[0].SubElementNames, ("Edge1",))
            Gui.Selection.clearPreselection()
            Gui.Selection.setPreselection(sketch, "Vertex1", tp=0)
            self.assertFalse(Gui.Selection.getPreselection().ObjectName)
        finally:
            Gui.Selection.removeSelectionGate()

    def test_equal_then_construction_retains_selected_curves(self):
        sketch = self.sketch()
        self.params.SetBool("Persistent", True)
        Gui.activeDocument().setEdit(sketch.Name)
        try:
            for i in range(1, 4):
                Gui.Selection.addSelection(sketch, "Edge%d" % i)
            Gui.runCommand("Sketcher_ConstrainEqual")
            self.assertEqual(set(Gui.Selection.getSelectionEx()[0].SubElementNames),
                             {"Edge1", "Edge2", "Edge3"})
            before = [sketch.getConstruction(i) for i in range(3)]
            Gui.runCommand("Sketcher_ToggleConstruction")
            self.assertEqual([sketch.getConstruction(i) for i in range(3)], [not x for x in before])
            self.assertEqual(len(Gui.Selection.getSelectionEx()[0].SubElementNames), 3)
        finally:
            Gui.activeDocument().resetEdit()


class TestDesignSelectionToolbar(unittest.TestCase):
    def test_ribbon_mode_and_classic_transitions(self):
        from freecad.gui import PlusRibbon
        prefs = App.ParamGet(PlusRibbon.PARAM)
        previous = prefs.GetString("ToolbarUIStyle", "Plus")
        ribbon = None
        try:
            PlusRibbon.apply_preferences()
            ribbon = PlusRibbon._ribbon
            prefs.SetString("ToolbarUIStyle", "Plus")
            ribbon.apply()
            ribbon.configure("Design")
            ribbon.place_plus_bars()
            self.assertFalse(ribbon.selection_toolbar.isHidden())
            self.assertTrue(Policy.active())
            self.assertIn(ribbon.selection_toolbar, ribbon.plus_bars())
            ribbon.configure("CAM")
            self.assertTrue(ribbon.selection_toolbar.isHidden())
            self.assertFalse(Policy.active())
            ribbon.configure("Design")
            self.assertTrue(Policy.active())
            prefs.SetString("ToolbarUIStyle", "Classic")
            ribbon.apply()
            self.assertTrue(ribbon.selection_toolbar.isHidden())
            self.assertFalse(Policy.active())
        finally:
            prefs.SetString("ToolbarUIStyle", previous)
            if ribbon:
                ribbon.apply()
                ribbon.configure("Design")
                ribbon.place_plus_bars()
            QtWidgets.QApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)

    def test_controls_settings_and_design_lifetime(self):
        from freecad.gui.DesignSelectionToolbar import SelectionToolbar
        params = Policy.parameters()
        saved = (params.GetBool("Directional", True), params.GetBool("Persistent", True),
                 params.GetInt("Categories", Policy.ALL), params.GetBool("Active", False))
        bar = None
        try:
            params.RemBool("Directional")
            params.RemBool("Persistent")
            bar = SelectionToolbar(Gui.getMainWindow())
            self.assertTrue(bar.directional.isChecked())
            self.assertTrue(bar.persistent.isChecked())
            self.assertEqual(bar.intent.count(), 3)
            self.assertEqual([a.text() for a in bar.categories], list(Policy.CATEGORIES))
            bar.set_design_active(True)
            self.assertTrue(Policy.active())
            bar.directional.setChecked(False)
            bar.persistent.setChecked(False)
            self.assertFalse(params.GetBool("Directional", True))
            self.assertFalse(Policy.persistent())
            bar.set_design_active(False)
            self.assertTrue(bar.isHidden())
            self.assertFalse(Policy.active())
        finally:
            if bar:
                bar.set_design_active(False)
                bar.deleteLater()
            params.SetBool("Directional", saved[0])
            params.SetBool("Persistent", saved[1])
            params.SetInt("Categories", saved[2])
            params.SetBool("Active", saved[3])
            QtWidgets.QApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)


from TestWindowSelection import TestWindowSelection as _WindowFixture


class TestDesignSelectionBoxes(unittest.TestCase):
    _fixture_setup = _WindowFixture.setUp
    _fixture_teardown = _WindowFixture.tearDown
    point = _WindowFixture.point
    drag = _WindowFixture.drag
    names = _WindowFixture.names

    def setUp(self):
        self._fixture_setup()
        self.params = Policy.parameters()
        self.saved_policy = (self.params.GetBool("Active", False),
                             self.params.GetBool("Directional", True),
                             self.params.GetInt("Categories", Policy.ALL))
        self.params.SetBool("Active", True)
        self.params.SetInt("Categories", Policy.ALL)

    def tearDown(self):
        self.params.SetBool("Active", self.saved_policy[0])
        self.params.SetBool("Directional", self.saved_policy[1])
        self.params.SetInt("Categories", self.saved_policy[2])
        self._fixture_teardown()

    def test_directional_toggle_changes_native_crossing(self):
        self.params.SetBool("Directional", False)
        self.drag((8, 8), (2, 2))
        self.assertFalse(self.names())
        self.params.SetBool("Directional", True)
        self.drag((8, 8), (2, 2))
        self.assertEqual(self.names(), {"Box"})

    def test_box_element_checkbox_union_and_body_exclusion(self):
        self.params.SetInt("Categories", (1 << Policy.CATEGORIES.index("Edges"))
                           | (1 << Policy.CATEGORIES.index("Vertices")))
        self.drag((-1, -1), (11, 11), element=True)
        names = {n for s in Gui.Selection.getSelectionEx() for n in s.SubElementNames}
        self.assertTrue(any(n.startswith("Edge") for n in names))
        self.assertTrue(any(n.startswith("Vertex") for n in names))
        self.assertFalse(any(n.startswith("Face") for n in names))
        self.params.SetInt("Categories", 1 << Policy.CATEGORIES.index("Curves"))
        self.drag((-1, -1), (11, 11))
        self.assertFalse(self.names())


del _WindowFixture
