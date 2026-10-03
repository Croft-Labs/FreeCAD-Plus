# SPDX-License-Identifier: LGPL-2.1-or-later
"""Task-owned curve emphasis, independent of native selection and document colors."""
import hashlib
import importlib
import json
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
import ComponentModel as Model
import ComponentSketch as Sketch
from pivy import coin
from PySide import QtCore, QtGui, QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest


class TestComponentCurveDisplay(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartDesignWorkbench")
        self.doc = Model.new_document("Curve display")
        self.component = Model.metadata(self.doc).RootComponent
        self.sketches = [self.rectangle(x) for x in (0, 25, 50)]
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        self.task = None
        self.colors = {s.Name: (s.ViewObject.LineColor, s.ViewObject.PointColor) for s in self.sketches}
        Gui.Selection.clearSelection()
        Gui.activeDocument().activeView().viewTop()
        Gui.activeDocument().activeView().fitAll()

    def tearDown(self):
        if self.task:
            self.task.reject()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def rectangle(self, x):
        sketch = Sketch.create(self.component)
        points = [App.Vector(x, 0, 0), App.Vector(x + 10, 0, 0),
                  App.Vector(x + 10, 10, 0), App.Vector(x, 10, 0)]
        for start, end in zip(points, points[1:] + points[:1]):
            sketch.addGeometry(Part.LineSegment(start, end))
        self.doc.recompute()
        return sketch

    def launch(self, name="Extrude", **kwargs):
        module = importlib.import_module("freecad.gui.Component" + name + "Task")
        for module_name in ("ComponentTaskWidgets", "ComponentExtrudeTask", "ComponentOperationTask", "ComponentSectionTask", "ComponentPipeTask"):
            installed = importlib.import_module("freecad.gui." + module_name)
            path = Path(os.environ["FREECAD_PLUS_SOURCE"]) / "src/Gui" / (module_name + ".py")
            self.assertEqual(hashlib.sha256(path.read_bytes()).digest(),
                             hashlib.sha256(Path(installed.__file__).read_bytes()).digest())
        self.task = module.launch(**kwargs)
        self.task.auto_preview.setChecked(False)
        return self.task

    def unchanged_colors(self):
        for source in self.sketches:
            self.assertEqual((source.ViewObject.LineColor, source.ViewObject.PointColor), self.colors[source.Name])

    def assert_emphasis(self, selected, active):
        Gui.Selection.clearSelection()
        Gui.updateGui()
        self.assertEqual(set(self.task.curve_highlights), set(selected))
        for highlight in self.task.curve_highlights.values():
            self.assertGreaterEqual(highlight.root.findChild(highlight.node), 0)
            self.assertTrue(highlight.node.isOfType(coin.SoAnnotation.getClassTypeId()))
        for source in self.sketches:
            self.assertEqual(source.Name in self.task.curve_materials, source.Name != active)
            self.assertEqual(source.ViewObject.ShowClosedRegions,
                             bool(source.Name == active and self.task.region_pick.isChecked()))
        self.unchanged_colors()

    def testIncrementalPicksFocusClearAndRegionToggle(self):
        task = self.launch()
        first, second, third = self.sketches
        self.assertTrue(all(s.ViewObject.ShowClosedRegions for s in self.sketches))
        Gui.Selection.addSelection(self.doc.Name, first.Name, "Edge1")
        self.assertEqual(task.curve_names(), ["Edge1"])
        task.length.setFocus()
        self.assert_emphasis([first.Name], first.Name)
        Gui.getMainWindow().grab().save(str(self.output / "one-edge-other-sketches-gray.png"))
        Gui.Selection.addSelection(self.doc.Name, first.Name, "Edge2")
        self.assertEqual(task.curve_names(), ["Edge1", "Edge2"])
        self.assert_emphasis([first.Name], first.Name)
        task.region_pick.setChecked(False)
        self.assert_emphasis([first.Name], first.Name)
        task.region_pick.setChecked(True)
        task.set_curves([], False)
        self.assertFalse(task.curve_highlights)
        self.assertFalse(task.curve_materials)
        self.assertTrue(all(s.ViewObject.ShowClosedRegions for s in self.sketches))
        task.profile.setCurrentIndex(task.profile.findData(second.Name))
        self.assert_emphasis([second.Name], second.Name)
        materials = list(task.curve_materials.values())
        task.reject()
        self.task = None
        self.assertTrue(all(root.findChild(material) < 0 for root, material in materials))
        self.assertFalse(any(s.ViewObject.ShowClosedRegions for s in self.sketches))
        self.unchanged_colors()

    def testAcceptEditPreviewAndCancel(self):
        first = self.sketches[0]
        task = self.launch()
        task.profile.setCurrentIndex(task.profile.findData(first.Name))
        self.assertTrue(task.preview(), task.status.text())
        self.assert_emphasis([first.Name], first.Name)
        Gui.activeDocument().activeView().viewAxonometric()
        Gui.activeDocument().activeView().fitAll()
        Gui.updateGui()
        Gui.getMainWindow().grab().save(str(self.output / "extrude-preview-highlight.png"))
        accepted = task.accept()
        self.assertTrue(accepted)
        operation = task.operation
        self.task = None
        self.assertFalse(task.curve_highlights)
        self.assertFalse(task.curve_materials)
        task = self.launch(operation=operation)
        self.assertEqual(len(task.curve_names()), 4)
        self.assert_emphasis([first.Name], first.Name)
        task.length.setProperty("rawValue", 20.)
        self.assertTrue(task.preview(), task.status.text())
        self.assert_emphasis([first.Name], first.Name)
        task.reject()
        self.task = None
        self.assertFalse(task.curve_highlights)
        self.assertFalse(task.curve_materials)
        self.unchanged_colors()

    def testAllSharedProfileCollectors(self):
        first = self.sketches[0]
        for name in ("Revolve", "Helix", "Loft", "Pipe"):
            with self.subTest(operation=name):
                task = self.launch(name)
                task.use_selection([(first, "Edge1")])
                self.assert_emphasis([first.Name], first.Name)
                task.reject()
                self.task = None
                self.assertFalse(task.curve_highlights)
                self.assertFalse(task.curve_materials)
                self.assertFalse(any(s.ViewObject.ShowClosedRegions for s in self.sketches))

    def testLatestCurveToggleAndDeleteAcrossOperations(self):
        source = self.sketches[0]
        for name in ("Extrude", "Revolve", "Helix", "Loft", "Pipe"):
            with self.subTest(operation=name):
                task = self.launch(name)
                labels = [b.text() for b in task.form.findChildren(QtWidgets.QPushButton)]
                self.assertFalse(set(labels) & {"Add selected curves", "Add selected", "Use selected"})
                for edge in ("Edge1", "Edge2"):
                    Gui.Selection.addSelection(self.doc.Name, source.Name, edge)
                    self.assertEqual([i.data(QtCore.Qt.UserRole) for i in task.curves.selectedItems()], [edge])
                self.assertEqual(task.curve_names(), ["Edge1", "Edge2"])
                Gui.Selection.addSelection(self.doc.Name, source.Name, "Edge2")
                self.assertEqual(task.curve_names(), ["Edge1"])
                self.assertEqual(task.curves.selectedItems(), [])
                self.assertEqual(task.curves.currentRow(), -1)
                QtTest.QTest.keyClick(task.curves, QtCore.Qt.Key_Delete)
                self.assertEqual(task.curve_names(), ["Edge1"])
                Gui.Selection.addSelection(self.doc.Name, source.Name, "Edge2")
                Gui.updateGui()
                QtTest.QTest.keyClick(task.curves, QtCore.Qt.Key_Delete)
                self.assertEqual(task.curve_names(), ["Edge1"])
                self.assertEqual(task.curves.selectedItems(), [])
                task.curves.item(0).setSelected(True)
                QtTest.QTest.keyClick(task.curves, QtCore.Qt.Key_Delete)
                self.assertEqual(task.curve_names(), [])
                self.assertFalse(task.curve_highlights)
                self.assertIsNotNone(self.doc.getObject(source.Name))
                task.reject()
                self.task = None

    def testPipePathLatestToggleAndDelete(self):
        task = self.launch("Pipe")
        source = self.sketches[0]
        task.orientation.setCurrentIndex(task.orientation.findData("Auxiliary"))
        for role in ("spine", "auxiliary"):
            with self.subTest(role=role):
                task.set_role(role)
                fields = task.paths[role]
                edges = fields["edges"]
                for edge in ("Edge1", "Edge2"):
                    Gui.Selection.addSelection(self.doc.Name, source.Name, edge)
                    self.assertEqual([i.text() for i in edges.selectedItems()], [edge])
                Gui.Selection.addSelection(self.doc.Name, source.Name, "Edge2")
                self.assertEqual([edges.item(i).text() for i in range(edges.count())], ["Edge1"])
                self.assertEqual(edges.currentRow(), -1)
                Gui.Selection.addSelection(self.doc.Name, source.Name, "Edge1")
                self.assertEqual(edges.count(), 0)
                self.assertFalse(fields["whole"], "Removing the last edge must not select the whole path")
                Gui.Selection.addSelection(self.doc.Name, source.Name, "Edge1")
                Gui.Selection.addSelection(self.doc.Name, source.Name, "Edge2")
                edges.item(0).setSelected(True)
                QtTest.QTest.keyClick(edges, QtCore.Qt.Key_Delete)
                self.assertEqual(edges.count(), 0)
                self.assertEqual(edges.currentRow(), -1)
                self.assertFalse(fields["whole"])
                self.assertIsNotNone(self.doc.getObject(source.Name))

    def testRepeatedViewportClickAndKeyboardDelete(self):
        task = self.launch()
        Gui.updateGui()
        viewport = max((w for w in Gui.getMainWindow().findChildren(QtWidgets.QWidget)
                        if "GL" in w.metaObject().className() and w.width() > 100 and w.height() > 100),
                       key=lambda w: w.width() * w.height())
        point = App.Vector(10, 5, 0)
        for expected in (["Edge2"], [], ["Edge2"]):
            sx, sy = task.view.getPointOnScreen(point)
            ratio = viewport.devicePixelRatioF()
            pos = QtCore.QPoint(round(sx / ratio), viewport.height() - round(sy / ratio) - 1)
            event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(pos),
                                     QtCore.QPointF(viewport.mapToGlobal(pos)), QtCore.Qt.NoButton,
                                     QtCore.Qt.NoButton, QtCore.Qt.NoModifier)
            QtWidgets.QApplication.sendEvent(viewport, event)
            QtTest.QTest.mouseClick(viewport, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, pos)
            Gui.updateGui()
            self.assertEqual(task.curve_names(), expected, task.status.text())
            self.assertEqual([i.data(QtCore.Qt.UserRole) for i in task.curves.selectedItems()], expected)
        self.assertEqual(QtWidgets.QApplication.focusWidget(), task.curves)
        QtTest.QTest.qWait(200)
        self.assert_emphasis([self.sketches[0].Name], self.sketches[0].Name)
        Gui.getMainWindow().grab().save(str(self.output / "latest-curve-list.png"))
        QtTest.QTest.keyClick(QtWidgets.QApplication.focusWidget(), QtCore.Qt.Key_Delete)
        self.assertEqual(task.curve_names(), [])
        self.assertIsNotNone(self.doc.getObject(self.sketches[0].Name))

    def testTiltedViewportEdgePicksDoNotCollectRegions(self):
        self.check_tilted_clicks("Extrude")

    def testTiltedRevolveEdgePicks(self):
        self.check_tilted_clicks("Revolve")

    def testTiltedHelixEdgePicks(self):
        self.check_tilted_clicks("Helix")

    def testTiltedLoftEdgePicks(self):
        self.check_tilted_clicks("Loft")

    def testTiltedPipeEdgePicks(self):
        self.check_tilted_clicks("Pipe")

    def check_tilted_clicks(self, operation):
        task = self.launch(operation)
        def viewport_click(point, dx=0, dy=0):
            Gui.updateGui()
            viewport = max((w for w in Gui.getMainWindow().findChildren(QtWidgets.QWidget)
                            if "GL" in w.metaObject().className() and w.width() > 100 and w.height() > 100),
                           key=lambda w: w.width() * w.height())
            sx, sy = task.view.getPointOnScreen(point)
            ratio = viewport.devicePixelRatioF()
            pos = QtCore.QPoint(round(sx / ratio) + dx, viewport.height() - round(sy / ratio) - 1 + dy)
            event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(pos),
                                     QtCore.QPointF(viewport.mapToGlobal(pos)), QtCore.Qt.NoButton,
                                     QtCore.Qt.NoButton, QtCore.Qt.NoModifier)
            QtWidgets.QApplication.sendEvent(viewport, event)
            hits = task.view.getObjectsInfo((round(pos.x() * ratio), round((viewport.height() - pos.y() - 1) * ratio)))
            QtTest.QTest.mouseClick(viewport, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, pos)
            Gui.updateGui()
            return hits
        evidence = []
        for angle in (0, 35, 65):
            task.view.setCameraOrientation(App.Rotation(App.Vector(1, 1, 0), angle).Q)
            task.view.fitAll()
            Gui.updateGui()
            for point in (App.Vector(5, 0, 0), App.Vector(10, 5, 0), App.Vector(5, 10, 0)):
                for dx, dy in ((0, 0), (1, 1), (-1, -1), (2, -2), (-2, 2)):
                    task.set_curves([], False)
                    picked = []
                    original = task.use_selection
                    def observe(picks=None, toggle=False):
                        picked.extend(element for obj, element in picks or [] if element.startswith("Edge"))
                        return original(picks, toggle)
                    task.use_selection = observe
                    try:
                        hits = viewport_click(point, dx, dy)
                    finally:
                        task.use_selection = original
                    if picked:
                        evidence.append(dict(angle=angle, offset=[dx, dy], expected=picked[-1], actual=task.curve_names(), hits=hits))
            task.set_curves([], False)
            # Bottom/left edges coincide with the visible origin axes; use the
            # unobstructed edges for deterministic native sequential picks.
            for point, expected in ((App.Vector(10, 5, 0), ["Edge2"]),
                                    (App.Vector(5, 10, 0), ["Edge2", "Edge3"]),
                                    (App.Vector(5, 10, 0), ["Edge2"])):
                viewport_click(point)
                self.assertEqual(task.curve_names(), expected, (operation, angle))
            self.assertEqual(task.curves.currentRow(), -1)
            task.set_curves([], False)
            viewport_click(App.Vector(5, 5, 0))
            self.assertEqual(set(task.curve_names()), {"Edge1", "Edge2", "Edge3", "Edge4"})
        (self.output / (operation + "-edge-region-clicks.json")).write_text(json.dumps(evidence, indent=2, default=str), encoding="utf8")
        self.assertGreater(len(evidence), 10)
        failures = [e for e in evidence if e["actual"] != [e["expected"]]]
        self.assertEqual(failures, [], str(failures[:3]))

    def testLoftRetainsEverySectionHighlight(self):
        first, second, third = self.sketches
        second.Placement.Base.z = 15
        self.doc.recompute()
        task = self.launch("Loft")
        task.add_row(first, None)
        task.add_row(second, None)
        self.assert_emphasis([first.Name, second.Name], None)
        self.assertTrue(task.preview(), task.status.text())
        self.assert_emphasis([first.Name, second.Name], None)
        task.ordered.setCurrentRow(1)
        self.assert_emphasis([first.Name, second.Name], second.Name)
        task.remove_section()
        # A draft remains selected until it too is cleared.
        task.profile.setCurrentIndex(0)
        self.assert_emphasis([first.Name], None)
        task.clear_sections()
        self.assertFalse(task.curve_highlights)
        self.assertFalse(task.curve_materials)

    def testPipeProfileSpineAndAuxiliaryCollectors(self):
        first = self.sketches[0]
        paths = []
        for x in (0, 15):
            path = self.doc.addObject("Part::Feature", "Path")
            path.Shape = Part.makeLine(App.Vector(x, 0, 0), App.Vector(x, 0, 20))
            Model.register_object(self.component, path)
            paths.append(path)
        self.doc.recompute()
        task = self.launch("Pipe")
        task.add_row(first, None)
        task.set_path("spine", paths[0], ["Edge1"])
        task.set_role("spine")
        self.assert_emphasis([first.Name, paths[0].Name], paths[0].Name)
        self.assertTrue(task.preview(), task.status.text())
        task.orientation.setCurrentIndex(task.orientation.findData("Auxiliary"))
        task.set_path("auxiliary", paths[1], ["Edge1"])
        task.set_role("auxiliary")
        self.assert_emphasis([first.Name] + [p.Name for p in paths], paths[1].Name)
        task.clear_path("auxiliary")
        self.assert_emphasis([first.Name, paths[0].Name], None)
        task.orientation.setCurrentIndex(task.orientation.findData("Standard"))
        task.set_role(None)
        task.profile.setCurrentIndex(task.profile.findData(first.Name))
        self.assert_emphasis([first.Name, paths[0].Name], first.Name)

    def testSavedColorsAreNotTemporaryDisplayOverrides(self):
        first = self.sketches[0]
        task = self.launch()
        task.use_selection([(first, "Edge1")])
        self.assert_emphasis([first.Name], first.Name)
        path = self.output / "CurveDisplay.cadprt"
        names = [s.Name for s in self.sketches]
        self.doc.saveAs(str(path))
        task.reject()
        self.task = None
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.sketches = [self.doc.getObject(name) for name in names]
        self.unchanged_colors()
        self.assertFalse(any(s.ViewObject.ShowClosedRegions for s in self.sketches))

    def testHighlightUsesSketchAndComponentPlacement(self):
        first = self.sketches[0]
        self.component.Placement = App.Placement(App.Vector(80, 20, 10), App.Rotation(App.Vector(0, 0, 1), 25))
        first.AttachmentOffset = App.Placement(App.Vector(10, 20, 30), App.Rotation(App.Vector(1, 0, 0), 90))
        self.doc.recompute()
        task = self.launch()
        task.use_selection([(first, "Edge1")])
        action = coin.SoGetBoundingBoxAction(coin.SbViewportRegion(640, 480))
        action.apply(task.curve_highlights[first.Name].node)
        bounds = action.getBoundingBox()
        parent = first.getGlobalPlacement().multiply(first.Placement.inverse())
        points = [parent.multVec(vertex.Point) for vertex in first.Shape.Edges[0].Vertexes]
        for axis in range(3):
            self.assertAlmostEqual(bounds.getMin()[axis], min(point[axis] for point in points), places=4)
            self.assertAlmostEqual(bounds.getMax()[axis], max(point[axis] for point in points), places=4)
