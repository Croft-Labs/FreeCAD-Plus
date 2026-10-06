# SPDX-License-Identifier: LGPL-2.1-or-later
import tempfile
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
from PySide import QtCore, QtGui, QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest
from freecad.gui import ConstraintPalette as Policy
from freecad.gui import ConstraintPaletteGui as UI
from freecad.gui import DesignSelection as Selection


def settle(milliseconds=80):
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(milliseconds, loop.quit)
    loop.exec_()


class TestConstraintPalette(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("SketcherWorkbench")
        from freecad.gui import PlusRibbon
        PlusRibbon.apply_preferences()
        PlusRibbon._ribbon.configure("Design", "Sketch")
        PlusRibbon._ribbon.render()
        PlusRibbon._ribbon.place_plus_bars()
        self.params = Selection.parameters()
        self.saved = (self.params.GetBool("Active", False), self.params.GetBool("Persistent", True))
        self.params.SetBool("Active", True)
        self.params.SetBool("Persistent", True)
        self.doc = App.newDocument("PaletteTest")
        self.doc.UndoMode = 1
        self.sketch = self.doc.addObject("Sketcher::SketchObject", "Sketch")
        for y, length in ((0, 10), (5, 12), (10, 15)):
            self.sketch.addGeometry(Part.LineSegment(App.Vector(0, y, 0), App.Vector(length, y, 0)), False)
        self.doc.recompute()
        Gui.activeDocument().setEdit(self.sketch.Name)
        UI.install()
        # Native workbench/edit activation posts layout and selection updates.
        # Enter each test only after that real GUI transition has settled.
        Gui.updateGui()
        settle(250)

    def tearDown(self):
        UI._controller.close()
        Gui.Selection.clearSelection()
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():
            Gui.activeDocument().resetEdit()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        self.params.SetBool("Active", self.saved[0])
        self.params.SetBool("Persistent", self.saved[1])
        settle(10)

    def select(self, *names):
        Gui.Selection.clearSelection()
        for name in names:
            Gui.Selection.addSelection(self.sketch, name)
        return Policy.selected(self.sketch)

    def execute(self, key):
        return Policy.execute(self.sketch, Policy.selected(self.sketch), key)

    def test_equal_then_construction_and_undo(self):
        names = self.select("Edge1", "Edge2", "Edge3")
        self.execute("Equal")
        self.assertEqual(self.sketch.ConstraintCount, 2)
        self.assertEqual(Policy.selected(self.sketch), names)
        self.assertTrue(next(a for a in Policy.actions(self.sketch, names) if a.key == "Equal").reason)
        self.execute("construction")
        self.assertEqual([self.sketch.getConstruction(i) for i in range(3)], [True] * 3)
        self.assertEqual(Policy.selected(self.sketch), names)
        self.doc.undo()
        self.assertEqual([self.sketch.getConstruction(i) for i in range(3)], [False] * 3)

    def test_native_lowercase_selection_names(self):
        self.assertEqual(Selection.category(self.sketch, "vertex1"), "Points")
        self.assertEqual(Selection.resolve(self.sketch, "edge1")[2], "Edge1")

    def test_escape_without_palette_clears_native_selection(self):
        from freecad.gui.DesignSelectionToolbar import SelectionToolbar
        bar = SelectionToolbar(Gui.getMainWindow())
        try:
            bar.set_design_active(True)
            self.select("Edge1")
            settle()
            mdi = Gui.getMainWindow().findChild(QtWidgets.QMdiArea).activeSubWindow()
            widgets = [w for w in mdi.findChildren(QtWidgets.QWidget)
                       if "GL" in w.metaObject().className() and w.width() > 100]
            widget = max(widgets, key=lambda w: w.width() * w.height())
            QtTest.QTest.keyClick(widget, QtCore.Qt.Key_Escape)
            settle(150)
            self.assertFalse(Gui.Selection.getSelection())
        finally:
            QtWidgets.QApplication.instance().removeEventFilter(bar)
            bar.deleteLater()

    def test_mixed_construction_is_normal_first(self):
        self.sketch.setConstruction(1, True)
        self.select("Edge1", "Edge2", "Edge3")
        self.execute("construction")
        self.assertEqual([self.sketch.getConstruction(i) for i in range(3)], [False] * 3)
        self.execute("construction")
        self.assertEqual([self.sketch.getConstruction(i) for i in range(3)], [True] * 3)

    def test_persistence_off_clears_success_and_failure_keeps_selection(self):
        names = self.select("Edge1")
        self.sketch.addConstraint(Sketcher.Constraint("Horizontal", 0))
        with self.assertRaises(ValueError):
            self.execute("Vertical")
        self.assertEqual(Policy.selected(self.sketch), names)
        self.params.SetBool("Persistent", False)
        self.execute("construction")
        self.assertEqual(Policy.selected(self.sketch), [])

    def dimensions(self):
        indices = list(self.sketch.addConstraint([Sketcher.Constraint("Distance", 0, 10.),
                                                Sketcher.Constraint("Distance", 1, 12.)]))
        for i in indices:
            self.sketch.renameConstraint(i, "Length" + str(i))
        return indices

    def test_multi_dimension_conversion_and_save_reopen(self):
        indices = self.dimensions()
        self.select(*("Constraint%d" % (i + 1) for i in indices))
        names = [c.Name for c in self.sketch.Constraints]
        self.execute("reference")
        self.assertEqual([self.sketch.getDriving(i) for i in indices], [False, False])
        self.execute("driving")
        self.assertEqual([self.sketch.getDriving(i) for i in indices], [True, True])
        self.assertEqual([c.Name for c in self.sketch.Constraints], names)
        self.doc.undo()
        self.assertEqual([self.sketch.getDriving(i) for i in indices], [False, False])
        Gui.activeDocument().resetEdit()
        path = Path(tempfile.mkdtemp(prefix="palette_")) / "dimensions.FCStd"
        self.doc.recompute()
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.sketch = self.doc.getObject("Sketch")
        self.assertEqual([c.Name for c in self.sketch.Constraints], names)
        self.assertEqual([self.sketch.getDriving(i) for i in indices], [False, False])

    def test_invalid_make_driving_is_committed_and_undoable(self):
        self.dimensions()
        duplicate = self.sketch.addConstraint(Sketcher.Constraint("Distance", 0, 10.))
        self.sketch.setDriving(duplicate, False)
        self.sketch.solve()
        self.select("Constraint%d" % (duplicate + 1))
        action = next(a for a in Policy.actions(self.sketch, Policy.selected(self.sketch)) if a.key == "driving")
        self.assertFalse(action.reason)
        success, error = self.execute("driving")
        self.assertTrue(success)
        self.assertTrue(error)
        self.assertTrue(self.sketch.getDriving(duplicate))
        self.assertNotEqual(self.sketch.solve(), 0)
        self.doc.undo()
        self.assertFalse(self.sketch.getDriving(duplicate))
        self.assertEqual(self.sketch.solve(), 0)

    def test_driving_expression_preserved_and_action_disabled(self):
        self.dimensions()
        self.sketch.setExpression("Constraints.Length0", "10 mm")
        self.select("Constraint1", "Constraint2")
        expressions = list(self.sketch.ExpressionEngine)
        self.assertTrue(Policy._expression(self.sketch, 0), repr(expressions))
        with self.assertRaises(ValueError):
            self.execute("reference")
        self.assertEqual(list(self.sketch.ExpressionEngine), expressions)
        self.assertTrue(self.sketch.getDriving(0))

    def test_reference_conversion_can_remove_one_of_several_conflicts(self):
        self.dimensions()
        duplicates = self.sketch.addConstraint([Sketcher.Constraint("Distance", 0, 10.),
                                               Sketcher.Constraint("Distance", 1, 12.)])
        for i in duplicates:
            self.sketch.setDriving(i, False)
        self.select("Constraint3", "Constraint4")
        self.execute("driving")
        self.select("Constraint3")
        success, error = self.execute("reference")
        self.assertTrue(success)
        self.assertTrue(error)  # The other redundant dimension is still driving.
        self.assertFalse(self.sketch.getDriving(2))
        self.assertTrue(self.sketch.getDriving(3))
        self.select("Constraint4")
        self.execute("reference")
        self.assertEqual(self.sketch.solve(), 0)

    def test_structural_eligibility_disabled_tooltips_and_no_hover_mutation(self):
        self.sketch.addConstraint(Sketcher.Constraint("Horizontal", 0))
        names = self.select("Edge1")
        actions = Policy.actions(self.sketch, names)
        keys = {a.key: a for a in actions}
        self.assertNotIn("Equal", keys)
        self.assertNotIn("Radius", keys)
        self.assertTrue(keys["Horizontal"].reason)
        self.assertTrue(keys["Vertical"].reason)
        parent = QtWidgets.QWidget(Gui.getMainWindow())
        parent.resize(400, 300)
        palette = UI.Palette(parent, UI._controller)
        try:
            before = (self.sketch.ConstraintCount, self.sketch.Geometry[0].toShape().Length)
            palette.update_actions(actions, parent.size())
            button = palette.buttons["Horizontal"]
            self.assertFalse(button.isEnabled())
            native = Gui.Command.get("Sketcher_ConstrainHorizontal").getAction()[0]
            self.assertEqual(button.toolTip(), native.toolTip())
            self.assertEqual(button.statusTip(), keys["Horizontal"].reason)
            event = QtGui.QHelpEvent(QtCore.QEvent.ToolTip, QtCore.QPoint(1, 1), button.mapToGlobal(QtCore.QPoint(1, 1)))
            QtWidgets.QApplication.sendEvent(button, event)
            self.assertEqual(QtWidgets.QToolTip.text(), button.toolTip())
            self.assertEqual(Gui.getMainWindow().statusBar().currentMessage(), keys["Horizontal"].reason)
            self.assertEqual(before, (self.sketch.ConstraintCount, self.sketch.Geometry[0].toShape().Length))
        finally:
            QtWidgets.QToolTip.hideText()
            parent.deleteLater()

    def test_native_icons_tooltips_and_palette_click(self):
        import os
        import hashlib
        import json
        from freecad.gui import ConstraintPalette as Backend
        cases = [("construction", "Sketcher_ToggleConstruction"),
                 ("driving", "Sketcher_ToggleDrivingConstraint"),
                 ("reference", "Sketcher_ToggleDrivingConstraint"),
                 ("Concentric", "Sketcher_ConstrainCoincident")]
        cases += [(key, "Sketcher_Constrain" + key) for key in
                  ("Block", "Horizontal", "Vertical", "Parallel", "Perpendicular",
                   "Angle", "Distance", "DistanceX", "DistanceY", "Equal", "Tangent",
                   "Radius", "Diameter", "Coincident", "PointOnObject", "Symmetric")]
        parent = QtWidgets.QWidget(Gui.getMainWindow())
        parent.resize(400, 300)
        parent.show()
        palette = UI.Palette(parent, UI._controller)
        try:
            # Cover every presentation mapping, including dimension and toggle
            # actions, without executing fabricated structural selections.
            palette.update_actions([Backend.Action(key, key) for key, _ in cases], parent.size())
            palette.show()
            for key, command in cases:
                native = Gui.Command.get(command).getAction()[0]
                button = palette.buttons[key]
                self.assertEqual(button.text(), "")
                self.assertEqual(button.toolButtonStyle(), QtCore.Qt.ToolButtonIconOnly)
                self.assertFalse(button.icon().isNull(), command)
                self.assertEqual(button.icon().cacheKey(), native.icon().cacheKey(), command)
                self.assertEqual(button.toolTip(), native.toolTip(), command)
                self.assertTrue(button.accessibleName())
            button = palette.buttons["Horizontal"]
            native = Gui.Command.get("Sketcher_ConstrainHorizontal").getAction()[0]
            tip = native.toolTip()
            try:
                native.setToolTip(tip + " native presentation refresh")
                self.assertEqual(button.toolTip(), native.toolTip())
            finally:
                native.setToolTip(tip)
            names = self.select("Edge1", "Edge2")
            controller = UI._controller
            controller.clicked(parent, parent.mapToGlobal(QtCore.QPoint(200, 200)), controller.generation)
            controller.poll.stop()
            actual = controller.palette
            actual.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "constraint-palette-icons.png"))
            module = Path(UI.__file__).resolve()
            self.assertTrue(module.is_relative_to(Path(App.ConfigGet("AppHomePath")).resolve()))
            source = Path(os.environ["FREECAD_PLUS_SOURCE"]) / "src/Gui/ConstraintPaletteGui.py"
            digest = hashlib.sha256(module.read_bytes()).hexdigest()
            self.assertEqual(digest, hashlib.sha256(source.read_bytes()).hexdigest())
            evidence = {"module": str(module), "sha256": digest,
                        "device_pixel_ratio": actual.devicePixelRatioF(),
                        "logical_size": [actual.width(), actual.height()],
                        "icon_size": [actual.buttons["Equal"].iconSize().width(),
                                      actual.buttons["Equal"].iconSize().height()],
                        "native_presentation_mappings": len(cases)}
            (Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "palette-presentation.json").write_text(json.dumps(evidence, indent=2))
            equal = actual.buttons["Equal"]
            event = QtGui.QHelpEvent(QtCore.QEvent.ToolTip, QtCore.QPoint(1, 1), equal.mapToGlobal(QtCore.QPoint(1, 1)))
            QtWidgets.QApplication.sendEvent(equal, event)
            self.assertEqual(QtWidgets.QToolTip.text(), Gui.Command.get("Sketcher_ConstrainEqual").getAction()[0].toolTip())
            QtTest.QTest.mouseClick(equal, QtCore.Qt.LeftButton)
            settle()
            self.assertEqual(self.sketch.ConstraintCount, 1)
            self.assertEqual(Policy.selected(self.sketch), names)
            self.doc.undo()
            self.assertEqual(self.sketch.ConstraintCount, 0)
            # Small viewports wrap icons and retain the viewport clamp.
            actual.update_actions(Policy.actions(self.sketch, names), QtCore.QSize(100, 120))
            self.assertLessEqual(actual.width(), 100)
            self.assertLessEqual(actual.height(), 120)
            self.assertEqual(actual.scroll.horizontalScrollBar().maximum(), 0)
        finally:
            QtWidgets.QToolTip.hideText()
            UI._controller.close()
            palette.deleteLater()
            parent.deleteLater()

    def test_tooltip_disappears_before_constraint_execution(self):
        from unittest.mock import patch
        controller = UI._controller
        parent = Gui.getMainWindow()
        self.select("Edge1", "Edge2")
        controller.clicked(parent, parent.mapToGlobal(QtCore.QPoint(500, 400)), controller.generation)
        controller.poll.stop()
        button = controller.palette.buttons["Equal"]
        event = QtGui.QHelpEvent(QtCore.QEvent.ToolTip, QtCore.QPoint(1, 1),
                                button.mapToGlobal(QtCore.QPoint(1, 1)))
        QtWidgets.QApplication.sendEvent(button, event)
        tips = lambda: [w for w in QtWidgets.QApplication.topLevelWidgets()
                        if w.windowType() == QtCore.Qt.ToolTip and w.isVisible()]
        self.assertTrue(tips(), "A real native tooltip must be visible before the click")
        entered = []
        original = Policy.execute

        def execute(*args):
            entered.append(not tips())
            return original(*args)

        with patch.object(Policy, "execute", execute):
            QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton)
        # No settle/sleep: the tooltip must disappear before native solving starts.
        self.assertEqual(entered, [True])
        self.assertFalse(tips())
        self.assertFalse(button.isVisible(), "Retired buttons must hide before deferred deletion")
        self.assertEqual(self.sketch.ConstraintCount, 1)
        self.assertEqual(Policy.selected(self.sketch), ["Edge1", "Edge2"])
        self.assertIsNotNone(controller.palette)
        self.doc.undo()
        controller.update()
        button = controller.palette.buttons["Equal"]
        event = QtGui.QHelpEvent(QtCore.QEvent.ToolTip, QtCore.QPoint(1, 1),
                                button.mapToGlobal(QtCore.QPoint(1, 1)))
        QtWidgets.QApplication.sendEvent(button, event)
        self.assertTrue(tips())
        controller.close()
        self.assertFalse(tips(), "Close must remove tooltip immediately too")
        self.params.SetBool("Persistent", False)
        controller.clicked(parent, parent.mapToGlobal(QtCore.QPoint(500, 400)), controller.generation)
        controller.poll.stop()
        button = controller.palette.buttons["Equal"]
        event = QtGui.QHelpEvent(QtCore.QEvent.ToolTip, QtCore.QPoint(1, 1),
                                button.mapToGlobal(QtCore.QPoint(1, 1)))
        QtWidgets.QApplication.sendEvent(button, event)
        self.assertTrue(tips())
        QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton)
        self.assertFalse(tips())
        self.assertIsNone(controller.palette)
        self.assertEqual(Policy.selected(self.sketch), [])
        self.doc.undo()
        self.assertEqual(self.sketch.ConstraintCount, 0)

    def test_viewport_clamp_and_corridor_grace(self):
        bounds = QtCore.QRect(4, 4, 300, 250)
        for anchor in (QtCore.QPoint(300, 5), QtCore.QPoint(4, 4), QtCore.QPoint(150, 240)):
            rect = UI.placement(anchor, QtCore.QSize(240, 140), bounds)
            self.assertTrue(bounds.contains(rect))
            region = UI.corridor(anchor, rect)
            self.assertTrue(region.contains(QtCore.QPointF(anchor)))
            self.assertTrue(region.contains(QtCore.QPointF(rect.center())))
        # Actual Qt timer cancellation, using a real selected sketch and widget.
        self.select("Edge1")
        parent = QtWidgets.QWidget(Gui.getMainWindow())
        parent.resize(600, 400)
        parent.show()
        controller = UI._controller
        try:
            anchor = parent.mapToGlobal(QtCore.QPoint(300, 300))
            controller.clicked(parent, anchor, controller.generation)
            controller.poll.stop()  # Positions below drive the same timer deterministically.
            outside = parent.mapToGlobal(QtCore.QPoint(0, 399))
            controller.track(outside)
            self.assertTrue(controller.dismiss.isActive())
            settle(600)
            controller.track(anchor)
            self.assertFalse(controller.dismiss.isActive())
            settle(500)
            self.assertIsNotNone(controller.palette)
            controller.track(outside)
            settle(1100)
            self.assertIsNone(controller.palette)
            self.assertEqual(Policy.selected(self.sketch), ["Edge1"])
        finally:
            controller.close()
            parent.deleteLater()

    def test_native_pointer_click_escape_empty_and_drag(self):
        window = Gui.getMainWindow()
        available = window.screen().availableGeometry()
        window.resize(min(1400, available.width()), min(950, available.height()-45))
        window.move(available.topLeft())
        # Finish queued dock/window layout before fitting the edit camera. A
        # zero-sized viewport at fit time can project the click to (0, 0).
        Gui.updateGui()
        settle(150)
        view = Gui.activeDocument().activeView()
        view.viewTop()
        view.fitAll()
        settle(150)
        QtWidgets.QApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)
        mdi = window.findChild(QtWidgets.QMdiArea).activeSubWindow()
        widgets = [w for w in mdi.findChildren(QtWidgets.QWidget)
                   if "GL" in w.metaObject().className() and w.width() > 100 and w.height() > 100]
        widget = max(widgets, key=lambda w: w.width() * w.height())
        sx, sy = view.getPointOnScreen(App.Vector(5, 0, 0))
        ratio = widget.devicePixelRatioF()
        point = QtCore.QPoint(round(sx / ratio), widget.height() - round(sy / ratio) - 1)
        self.assertTrue(5 < point.x() < widget.width()-5 and 5 < point.y() < widget.height()-5,
                        repr((point, widget.size(), view.getCameraOrientation())))
        self.select("Edge1")
        settle()
        self.assertIsNone(UI._controller.palette)  # Programmatic/box selection never opens it.
        Gui.Selection.clearSelection()
        QtTest.QTest.mouseMove(widget, point)
        settle()
        QtTest.QTest.mouseClick(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, point)
        settle(150)
        self.assertIsNotNone(UI._controller.palette, repr((Selection.active(), Policy.selected(self.sketch),
                             widget.metaObject().className(), point, UI._controller.generation)))
        QtTest.QTest.keyClick(widget, QtCore.Qt.Key_Escape)
        settle()
        self.assertIsNone(UI._controller.palette)
        self.assertFalse(Gui.Selection.getSelection())
        self.assertEqual(Policy.editing_sketch(), self.sketch)
        QtTest.QTest.mouseMove(widget, point + QtCore.QPoint(15, 15))
        settle()
        QtTest.QTest.mouseMove(widget, point)
        settle()
        QtTest.QTest.mouseClick(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, point)
        settle(150)
        self.assertIsNotNone(UI._controller.palette, repr(Policy.selected(self.sketch)))
        empty = QtCore.QPoint(30, 30)
        QtTest.QTest.mouseMove(widget, empty)
        settle()
        QtTest.QTest.mouseClick(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, empty)
        settle()
        self.assertIsNone(UI._controller.palette)
        self.assertFalse(Gui.Selection.getSelection())
        QtTest.QTest.mousePress(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, empty)
        end = empty + QtCore.QPoint(70, 70)
        event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(end),
                                 QtCore.QPointF(widget.mapToGlobal(end)), QtCore.Qt.NoButton,
                                 QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(widget, event)
        QtTest.QTest.mouseRelease(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, end)
        settle()
        self.assertIsNone(UI._controller.palette)


class TestConstraintPaletteNative(TestConstraintPalette):
    """Additional grouped-build acceptance: no source-overlay substitute."""
    def test_plain_point_click_replaces_and_modifiers_extend(self):
        window = Gui.getMainWindow()
        window.resize(1400, 950)
        Gui.updateGui()
        settle(150)
        view = Gui.activeDocument().activeView()
        view.viewTop()
        view.fitAll()
        settle(150)
        mdi = window.findChild(QtWidgets.QMdiArea).activeSubWindow()
        widget = max((w for w in mdi.findChildren(QtWidgets.QWidget)
                      if "GL" in w.metaObject().className() and w.width() > 100),
                     key=lambda w: w.width() * w.height())
        before = (self.doc.UndoCount, self.sketch.ConstraintCount,
                  tuple(g.toShape().Length for g in self.sketch.Geometry))
        def click(world=None, modifiers=QtCore.Qt.NoModifier):
            if world is None:
                pixel = QtCore.QPoint(25, 25)
            else:
                sx, sy = view.getPointOnScreen(App.Vector(*world))
                ratio = widget.devicePixelRatioF()
                pixel = QtCore.QPoint(round(sx / ratio), widget.height() - round(sy / ratio) - 1)
            QtTest.QTest.mouseMove(widget, pixel)
            settle(80)
            QtTest.QTest.mouseClick(widget, QtCore.Qt.LeftButton, modifiers, pixel)
            settle(QtWidgets.QApplication.doubleClickInterval() + 50)
        Gui.Selection.clearSelection()
        click((0, 5, 0))
        self.assertEqual(Policy.selected(self.sketch), ["Vertex3"])
        click((12, 5, 0))
        self.assertEqual(Policy.selected(self.sketch), ["Vertex4"])
        click((12, 5, 0))  # Plain repeat-click retains the one selected point.
        self.assertEqual(Policy.selected(self.sketch), ["Vertex4"])
        click((0, 5, 0), QtCore.Qt.ControlModifier)
        self.assertEqual(set(Policy.selected(self.sketch)), {"Vertex3", "Vertex4"})
        click((0, 10, 0), QtCore.Qt.ShiftModifier)
        self.assertEqual(set(Policy.selected(self.sketch)), {"Vertex3", "Vertex4", "Vertex5"})
        click(None, QtCore.Qt.ShiftModifier)
        self.assertEqual(set(Policy.selected(self.sketch)), {"Vertex3", "Vertex4", "Vertex5"})
        click()
        self.assertFalse(Policy.selected(self.sketch))
        self.assertEqual(before, (self.doc.UndoCount, self.sketch.ConstraintCount,
                         tuple(g.toShape().Length for g in self.sketch.Geometry)))

    def test_candidate_point_constraints_do_not_log_errors(self):
        outputs = [w for w in Gui.getMainWindow().findChildren(QtWidgets.QTextEdit)
                   if w.metaObject().className().endswith("ReportOutput")]
        self.assertTrue(outputs, "Native report output must be available")
        settle()
        before_text = outputs[0].toPlainText()
        before = (self.doc.UndoCount, self.sketch.ConstraintCount,
                  tuple(g.toShape().Length for g in self.sketch.Geometry), list(self.sketch.State))
        # Collapsing the endpoints of one line is an invalid hypothetical solve,
        # not a user operation: feasibility probing must remain read-only/quiet.
        self.select("Vertex3", "Vertex4")
        for _ in range(3):
            self.assertTrue(Policy.actions(self.sketch, Policy.selected(self.sketch)))
        settle(200)
        added = outputs[0].toPlainText()[len(before_text):]
        self.assertNotIn("Invalid solution", added)
        self.assertNotIn("Updating geometry: Error", added)
        self.assertEqual(before, (self.doc.UndoCount, self.sketch.ConstraintCount,
                         tuple(g.toShape().Length for g in self.sketch.Geometry), list(self.sketch.State)))

        # The quiet flag belongs to the cloned probe, never the live solver.
        offset = len(outputs[0].toPlainText())
        self.doc.openTransaction("Actual invalid coincidence")
        try:
            self.sketch.addConstraint(Sketcher.Constraint("Coincident", 1, 1, 1, 2))
            self.sketch.solve()
            settle(200)
            self.assertIn("Updating geometry: Error", outputs[0].toPlainText()[offset:])
        finally:
            self.doc.abortTransaction()

    def test_point_drag_undo_and_save_reopen(self):
        window = Gui.getMainWindow()
        window.resize(1400, 950)
        Gui.updateGui()
        settle(150)
        view = Gui.activeDocument().activeView()
        view.viewTop()
        view.fitAll()
        settle(150)
        mdi = window.findChild(QtWidgets.QMdiArea).activeSubWindow()
        widget = max((w for w in mdi.findChildren(QtWidgets.QWidget)
                      if "GL" in w.metaObject().className() and w.width() > 100),
                     key=lambda w: w.width() * w.height())
        sx, sy = view.getPointOnScreen(App.Vector(12, 5, 0))
        ratio = widget.devicePixelRatioF()
        point = QtCore.QPoint(round(sx / ratio), widget.height() - round(sy / ratio) - 1)
        original = self.sketch.Geometry[1].EndPoint
        self.select("Vertex4")
        QtTest.QTest.mouseMove(widget, point)
        settle(100)
        QtTest.QTest.mousePress(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, point)
        end = point + QtCore.QPoint(35, -25)
        event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(end),
                                 QtCore.QPointF(widget.mapToGlobal(end)), QtCore.Qt.NoButton,
                                 QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(widget, event)
        settle(100)
        QtTest.QTest.mouseRelease(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, end)
        settle(200)
        moved = self.sketch.Geometry[1].EndPoint
        self.assertGreater((moved - original).Length, 0.01)
        self.assertEqual(self.sketch.ConstraintCount, 0)
        self.doc.undo()
        self.assertLess((self.sketch.Geometry[1].EndPoint - original).Length, 1e-7)
        self.doc.redo()
        self.assertLess((self.sketch.Geometry[1].EndPoint - moved).Length, 1e-7)
        Gui.activeDocument().resetEdit()
        path = Path(tempfile.mkdtemp(prefix="palette_")) / "point-drag.FCStd"
        self.doc.recompute()
        self.doc.saveAs(str(path))
        name = self.sketch.Name
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.sketch = self.doc.getObject(name)
        self.assertLess((self.sketch.Geometry[1].EndPoint - moved).Length, 1e-7)

    def test_native_probe_is_read_only_and_finds_indirect_redundancy(self):
        # Native solver recognizes this indirect dependency. Equality cycles can
        # be accepted by the kernel, so they are not a redundancy oracle.
        self.sketch.addConstraint([Sketcher.Constraint("Horizontal", 0),
                                   Sketcher.Constraint("Parallel", 0, 1)])
        before = (self.doc.UndoCount, self.sketch.ConstraintCount,
                  tuple(g.toShape().Length for g in self.sketch.Geometry), list(self.sketch.State))
        status = self.sketch.diagnoseConstraintAdditions([Sketcher.Constraint("Horizontal", 1)])
        self.assertEqual(status, -2)
        self.assertEqual(before, (self.doc.UndoCount, self.sketch.ConstraintCount,
                         tuple(g.toShape().Length for g in self.sketch.Geometry), list(self.sketch.State)))

    def test_native_batch_rejects_unsupported_without_partial_conversion(self):
        ids = self.dimensions()
        with self.assertRaises(Exception):
            self.sketch.setDrivingBatch([ids[0], 999], False)
        self.assertTrue(self.sketch.getDriving(ids[0]))
