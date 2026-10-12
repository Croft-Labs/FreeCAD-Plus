# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Qt acceptance for the independent Plus ribbon presentation."""
import os
import unittest
from pathlib import Path
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtGui, QtOpenGLWidgets, QtTest, QtWidgets
from freecad_plus import toolbars, ui_modes, selection_toolbar, curve_selection, category_selection


def settle():
    QtTest.QTest.qWait(350)


class TestPlusToolbars(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:
            self.skipTest('Use an isolated native validation profile')
        self.before = set(App.listDocuments())
        self.prefs = App.ParamGet('User parameter:BaseApp/Preferences/General')
        self.saved = [self.prefs.GetInt(key, 0) for key in ui_modes.KEYS]
        self.saved_categories = {k: category_selection.preferences().GetBool(k, True)
                                 for k in category_selection.CATEGORIES}
        for key in category_selection.CATEGORIES:
            category_selection.preferences().SetBool(key, True)
        self.saved_intent = curve_selection.intent()
        selection_toolbar.preferences().SetString('CurveIntent', 'Single Curve')
        self.saved_persistent = selection_toolbar.preferences().GetBool('Persistent', True)
        selection_toolbar.preferences().SetBool('Persistent', True)
        self.saved_directional = selection_toolbar.preferences().GetBool('Directional', True)
        selection_toolbar.preferences().SetBool('Directional', True)
        self.prefs.SetInt('ToolbarUIMode', 0)
        Gui.activateWorkbench('PartDesignWorkbench')
        ui_modes.apply_modes()
        self.ribbon = toolbars._controller
        Gui.getMainWindow().showMaximized()
        self.tab('Modeling')
        settle()

    def tearDown(self):
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():
            Gui.activeDocument().resetEdit()
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)
        for key, value in self.saved_categories.items():
            category_selection.preferences().SetBool(key, value)
        selection_toolbar.preferences().SetString('CurveIntent', self.saved_intent)
        selection_toolbar.preferences().SetBool('Directional', self.saved_directional)
        selection_toolbar.preferences().SetBool('Persistent', self.saved_persistent)
        for key, value in zip(ui_modes.KEYS, self.saved):
            self.prefs.SetInt(key, value)
        ui_modes.apply_modes()
        settle()

    def tab(self, label):
        index = next(i for i in range(self.ribbon.tabbar.count())
                     if self.ribbon.tabbar.tabText(i) == label)
        self.ribbon.tabbar.setCurrentIndex(index)
        settle()

    def test_classic_restore_and_independent_preferences(self):
        r = self.ribbon
        self.assertTrue(r.bar.isVisible())
        self.assertTrue(all(b.isHidden() for b in r.native_bars()))
        self.prefs.SetInt('ToolbarUIMode', 1)
        ui_modes.apply_modes()
        settle()
        self.assertTrue(r.bar.isHidden())
        file_bar = next(b for b in r.native_bars() if b.objectName() == 'File')
        self.assertTrue(file_bar.isVisible())
        file_bar.hide()
        original = [(b, b.parentWidget(), b.actions()) for b in r.native_bars()]
        self.prefs.SetInt('ToolbarUIMode', 0)
        self.prefs.SetInt('ModelPanelUIMode', 1)
        self.prefs.SetInt('TaskPanelUIMode', 1)
        ui_modes.apply_modes()
        settle()
        self.assertTrue(r.bar.isVisible())
        self.assertEqual(ui_modes.modes(), ('Classic', 'Plus', 'Classic'))
        self.prefs.SetInt('ToolbarUIMode', 1)
        ui_modes.apply_modes()
        settle()
        self.assertTrue(file_bar.isHidden())
        for bar, parent, actions in original:
            self.assertEqual(bar.parentWidget(), parent)
            self.assertEqual(bar.actions(), actions)
        file_bar.show()

    def test_bim_status_controls_keep_native_ownership(self):
        App.ParamGet('User parameter:BaseApp/Preferences/Mod/BIM').SetBool('FirstTime', False)
        Gui.activateWorkbench('BIMWorkbench')
        ui_modes.apply_modes()
        settle()
        window = Gui.getMainWindow()
        self.addCleanup(window.statusBar().setVisible, not window.statusBar().isHidden())
        window.statusBar().show()
        settle()
        status = window.statusBar().findChild(QtWidgets.QToolBar, 'BIMStatusWidget')
        self.assertIsNotNone(status)
        self.assertTrue(status.isVisible())
        parent, actions = status.parentWidget(), status.actions()
        self.assertNotIn(status, self.ribbon.native_bars())
        self.assertIsNone(status.property('FreeCADPlusClassicVisible'))
        self.assertTrue(actions)
        for mode in (1, 0):
            self.prefs.SetInt('ToolbarUIMode', mode)
            ui_modes.apply_modes()
            settle()
            self.assertTrue(status.isVisible())
            self.assertEqual(status.parentWidget(), parent)
            self.assertEqual(status.actions(), actions)
        Gui.activateWorkbench('PartDesignWorkbench')
        ui_modes.apply_modes()
        settle()
        self.assertTrue(status.isHidden())
        self.assertNotIn(status, self.ribbon.native_bars())
        Gui.activateWorkbench('BIMWorkbench')
        ui_modes.apply_modes()
        settle()
        self.assertTrue(status.isVisible())
        self.assertEqual(status.parentWidget(), parent)
        self.assertEqual(status.actions(), actions)
        self.assertNotIn(status, self.ribbon.native_bars())

    def test_spreadsheet_native_color_widgets(self):
        Gui.activateWorkbench('SpreadsheetWorkbench')
        ui_modes.apply_modes()
        self.tab('All Tools')
        doc = App.newDocument('RibbonSheet')
        doc.UndoMode = 1
        sheet = doc.addObject('Spreadsheet::Sheet', 'Sheet')
        sheet.set('A1', 'Color test')
        doc.recompute()
        sheet.ViewObject.doubleClicked()
        settle()
        view = sheet.ViewObject.getView()
        view.select('A1', QtCore.QItemSelectionModel.SelectCurrent.value)
        view.setCurrentIndex('A1')
        settle()
        r = self.ribbon
        for suffix, color, read in (('ForegroundColor', QtGui.QColor('red'), sheet.getForeground),
                                    ('BackgroundColor', QtGui.QColor('yellow'), sheet.getBackground)):
            original = r.native['Spreadsheet'].findChild(QtWidgets.QPushButton, 'Spreadsheet_' + suffix)
            copy = r.scroll.widget().findChild(QtWidgets.QPushButton, 'PlusWidget_Spreadsheet_' + suffix)
            self.assertIsNotNone(copy)
            self.assertNotEqual(copy, original)
            self.assertEqual(copy.metaObject().className(), original.metaObject().className())
            parent = original.parentWidget()
            spy = QtTest.QSignalSpy(original.colorSet)
            undo = doc.UndoCount
            copy.setCurrentColor(color)
            settle()
            self.assertEqual(spy.count(), 1)
            self.assertEqual(doc.UndoCount, undo + 1)
            self.assertEqual(read('A1')[:3], (color.redF(), color.greenF(), color.blueF()))
            self.assertEqual(original.parentWidget(), parent)
            doc.undo()
            settle()
            self.assertEqual(doc.UndoCount, undo)
        r.host.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'ribbon-spreadsheet.png'))

    def test_tabs_modes_and_idle(self):
        r = self.ribbon
        self.assertEqual(r.tab, 'Modeling')
        self.assertEqual([g.objectName() for g in r.scroll.widget().findChildren(QtWidgets.QWidget)
                          if g.objectName().startswith('PlusGroup_')],
                         ['PlusGroup_' + n for n in ('Sketch','Modeling','Dress-Up','Transformation','Primitives','Other')])
        primitive = r.scroll.widget().findChild(QtWidgets.QToolButton, 'Plus_PartDesign_CompPrimitiveAdditive')
        self.assertEqual(primitive.menu().actions()[-1].text(), 'Tab')
        self.assertFalse(primitive.menu().actions()[-1].isEnabled())
        self.assertNotIn('Tab', [a.text() for a in r.sources['PartDesign_CompPrimitiveAdditive'][1].menu().actions()])
        self.tab('Sketch')
        self.assertEqual(Gui.activeWorkbench().name(), 'SketcherWorkbench')
        self.prefs.SetInt('ToolbarUIMode', 1)
        ui_modes.apply_modes()
        self.assertTrue(r.native['Sketcher'].isVisible())
        self.assertTrue(r.native['Geometries'].isHidden())
        self.prefs.SetInt('ToolbarUIMode', 0)
        ui_modes.apply_modes()
        self.assertTrue(r.scroll.widget().findChild(QtWidgets.QToolButton, 'Plus_Sketcher_CompCreateArc'))
        self.tab('View')
        self.assertEqual(Gui.activeWorkbench().name(), 'SketcherWorkbench')
        self.assertTrue(r.scroll.widget().findChild(QtWidgets.QToolButton, 'Plus_Std_ViewFitAll'))
        available = Gui.listWorkbenches()
        for i in range(r.selector.count()):
            _, wb = r.selector.itemData(i)
            flags = r.selector.model().flags(r.selector.model().index(i, 0))
            self.assertEqual(bool(flags & QtCore.Qt.ItemIsEnabled), wb in available)
        with patch.object(r, '_build_page', wraps=r._build_page) as build:
            QtTest.QTest.qWait(500)
            self.assertEqual(build.call_count, 0)
        output = Path(os.environ['PLUS_TEST_DIR'])
        r.host.grab().save(str(output/'ribbon-view.png'))
        self.tab('Home')
        self.assertEqual(Gui.activeWorkbench().name(), 'PartDesignWorkbench')
        self.assertEqual(r.tab, 'Home')
        self.tab('Modeling')
        r.host.grab().save(str(output/'ribbon-modeling.png'))

    def test_captions_and_icon_only_controls_on_narrow_window(self):
        window = Gui.getMainWindow()
        original_font = QtWidgets.QApplication.font()
        try:
            window.showNormal()
            window.resize(1000, 760)
            for scale in (1.0, 1.5):
                font = QtGui.QFont(original_font)
                if font.pointSizeF() > 0:
                    font.setPointSizeF(font.pointSizeF() * scale)
                else:
                    font.setPixelSize(round(font.pixelSize() * scale))
                QtWidgets.QApplication.setFont(font)
                self.ribbon.refresh()
                self.tab('Modeling')
                page = self.ribbon.scroll.widget()
                pending = [b for b in page.findChildren(QtWidgets.QToolButton)
                           if b.property('PlusUnavailable') is not None]
                self.assertTrue(pending)
                for button in pending:
                    self.assertFalse(button.isEnabled())
                    self.assertFalse(button.icon().isNull())
                    self.assertEqual(button.toolButtonStyle(), QtCore.Qt.ToolButtonIconOnly)
                    self.assertTrue(button.accessibleName())
                    self.assertIn('not available', button.toolTip())
                # Check actual full-inventory groups, including long native captions.
                Gui.activateWorkbench('FemWorkbench')
                ui_modes.apply_modes()
                self.assertEqual(self.ribbon.mode, 'FEM')
                self.tab('All Tools')
                captions = self.ribbon.scroll.widget().findChildren(QtWidgets.QLabel, 'PlusCaption')
                self.assertTrue(captions)
                self.assertTrue(any('\n' in c.text() for c in captions))
                for label in captions:
                    lines = label.text().split('\n')
                    self.assertLessEqual(len(lines), 2)
                    self.assertEqual(' '.join(lines), label.accessibleName())
                    metrics = label.fontMetrics()
                    self.assertGreaterEqual(label.contentsRect().width(),
                                            max(metrics.horizontalAdvance(line) for line in lines))
                    self.assertGreaterEqual(label.contentsRect().height(),
                                            metrics.height() + (len(lines) - 1) * metrics.lineSpacing())
                    top = label.mapTo(self.ribbon.scroll.widget(), QtCore.QPoint())
                    self.assertLessEqual(top.y() + label.height(), self.ribbon.scroll.viewport().height())
                scroll = self.ribbon.scroll.horizontalScrollBar()
                self.assertGreater(scroll.maximum(), 0)
                scroll.setValue(scroll.maximum())
                settle()
                self.ribbon.host.grab().save(str(Path(os.environ['PLUS_TEST_DIR']) /
                                                ('ribbon-narrow-' + str(scale) + '.png')))
                Gui.activateWorkbench('PartDesignWorkbench')
                ui_modes.apply_modes()
                self.tab('Modeling')
        finally:
            QtWidgets.QApplication.setFont(original_font)
            self.ribbon.refresh()
            window.showMaximized()
            settle()

    def directional(self, checked):
        button = self.ribbon.common.findChild(QtWidgets.QToolButton, 'PlusDirectionalSelection')
        self.assertIsNotNone(button)
        if button.isChecked() != checked:
            QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton)
        self.assertEqual(button.isChecked(), checked)
        self.assertEqual(selection_toolbar.preferences().GetBool('Directional'), checked)

    def drag_box(self, view, start, end, command=None, capture=None):
        widget = view.graphicsView().viewport()
        self.assertIsInstance(widget, QtOpenGLWidgets.QOpenGLWidget)
        ratio = widget.devicePixelRatioF()
        def point(xy):
            screen = view.getPointOnScreen(App.Vector(*xy, 0))
            pos = QtCore.QPoint(round(screen[0] / ratio), widget.height() - 1 - round(screen[1] / ratio))
            self.assertTrue(widget.rect().contains(pos), (pos, widget.rect()))
            return pos
        first, last = point(start), point(end)
        Gui.Selection.clearSelection()
        if command:
            Gui.runCommand(command)
            settle()
        QtTest.QTest.mouseMove(widget, first)
        # Deliver hover before press even when the OS cursor already occupies
        # this position after a preceding test drag or a toolbar-menu click.
        hover = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(first),
                                 QtCore.QPointF(widget.mapToGlobal(first)), QtCore.Qt.NoButton,
                                 QtCore.Qt.NoButton, QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(widget, hover)
        QtTest.QTest.qWait(50)
        QtTest.QTest.mousePress(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, first)
        for step in range(1, 9):
            pos = first + (last - first) * (step / 8)
            event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(pos),
                                     QtCore.QPointF(widget.mapToGlobal(pos)), QtCore.Qt.NoButton,
                                     QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
            QtWidgets.QApplication.sendEvent(widget, event)
            QtTest.QTest.qWait(20)
        if capture:
            view.redraw()
            settle()
            path = Path(os.environ['PLUS_TEST_DIR']) / capture
            if os.name == 'nt':
                from TestComponentFading import capture as framebuffer
                image, _ = framebuffer(view, path, prepare=False)
            else:
                image = widget.grabFramebuffer()
                image.save(str(path))
            self.assertTrue(any(image.pixelColor(image.width() * x // 4, image.height() * y // 4).value()
                                for x in (1, 2, 3) for y in (1, 2, 3)), 'Empty framebuffer capture')
        QtTest.QTest.mouseRelease(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, last)
        settle()
        if command:
            self.assertIsNone(view.graphicsView().property('FreeCADPlusBoxSelection'))
        return Gui.Selection.getSelectionEx()

    def category_toggle(self, name, enabled):
        button = self.ribbon.common.findChild(QtWidgets.QToolButton, 'PlusSelectionCategories')
        menu = button.menu()
        action = next(a for a in menu.actions() if a.text() == name)
        if action.isChecked() != enabled:
            def choose():
                QtTest.QTest.mouseClick(menu, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                                       menu.actionGeometry(action).center())
            QtCore.QTimer.singleShot(100, choose)
            QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton)
            settle()
        self.assertEqual(action.isChecked(), enabled)
        self.assertEqual(category_selection.preferences().GetBool(name, True), enabled)

    def test_category_menu_scope_and_gate_ownership(self):
        import Part
        button = self.ribbon.common.findChild(QtWidgets.QToolButton, 'PlusSelectionCategories')
        self.assertEqual([a.text() for a in button.menu().actions()],list(category_selection.CATEGORIES))
        self.assertTrue(all(a.isChecked() for a in button.menu().actions()))
        self.assertFalse(button.icon().isNull())
        doc=App.newDocument('CategoryScope');obj=doc.addObject('Part::Feature','Box')
        obj.Shape=Part.makeBox(10,10,10);doc.recompute()
        class Refuse:
            def allow(self, doc, obj, sub): return False
        Gui.Selection.addSelectionGate(Refuse())
        try:
            self.category_toggle('Faces',False)
            self.tab('Home')
            button=self.ribbon.common.findChild(QtWidgets.QToolButton,'PlusSelectionCategories')
            self.assertFalse(next(a for a in button.menu().actions() if a.text()=='Faces').isChecked())
            for mode in (1,0):
                self.prefs.SetInt('ToolbarUIMode',mode);ui_modes.apply_modes()
                Gui.Selection.addSelection(obj,'Face1')
                self.assertFalse(Gui.Selection.getSelection())
            Gui.activateWorkbench('FemWorkbench');ui_modes.apply_modes()
            self.assertFalse(category_selection._controller.active)
            self.assertIsNone(self.ribbon.common.findChild(QtWidgets.QToolButton,'PlusSelectionCategories'))
            Gui.activateWorkbench('PartDesignWorkbench');ui_modes.apply_modes()
            self.assertTrue(category_selection._controller.active)
        finally:
            Gui.Selection.removeSelectionGate()
        # A category preference must not interfere with command-driven selection.
        Gui.Selection.addSelection(obj,'Face1')
        self.assertTrue(Gui.Selection.getSelection())
        self.assertIsNone(Gui.getMainWindow().property('FreeCADPlusCategoryPicking'))

    def test_category_geometry_and_batch_admission(self):
        import Part
        doc=App.newDocument('CategoryKinds')
        box=doc.addObject('Part::Feature','Box');box.Shape=Part.makeBox(10,10,10)
        sheet=doc.addObject('Part::Feature','Sheet');sheet.Shape=Part.makePlane(10,10)
        curve=doc.addObject('Part::Feature','Curve');curve.Shape=Part.makeLine(App.Vector(0,0,0),App.Vector(10,0,0))
        point=doc.addObject('Part::Feature','Point');point.Shape=Part.Vertex(0,0,0)
        body=doc.addObject('PartDesign::Body','Body')
        plane=body.newObject('PartDesign::Plane','Plane')
        sketch=body.newObject('Sketcher::SketchObject','Sketch')
        sketch.addGeometry(Part.LineSegment(App.Vector(0,0,0),App.Vector(10,0,0)),False)
        root=doc.addObject('App::Part','Root')
        link=doc.addObject('App::Link','Occurrence');link.setLink(box);root.addObject(link)
        doc.recompute()
        cases=((box,'','Bodies'),(box,'Face1','Faces'),(box,'Edge1','Edges'),
               (box,'Vertex1','Vertices'),(sheet,'','Surfaces'),(sheet,'Edge1','Surfaces'),
               (curve,'Edge1','Curves'),(curve,'Vertex1','Points'),(point,'','Points'),
               (plane,'','Planes'),(body.Origin,'','Points'),(sketch,'Edge1','Curves'),
               (sketch,'Vertex1','Points'),(root,'Occurrence.Face1','Faces'))
        for obj,sub,expected in cases:
            self.assertEqual(category_selection.category(obj,sub),expected,(obj.Name,sub))
        # Exercise the same native hook used by box-selection batches. Its scope
        # is explicitly armed here; actual mouse routing is covered below.
        class OnlyFace:
            def allow(self, doc, obj, sub): return sub == 'Face1'
        Gui.Selection.addSelectionGate(OnlyFace())
        try:
            for allowed in (False,True):
                self.category_toggle('Faces',allowed)
                Gui.Selection.clearSelection()
                Gui.getMainWindow().setProperty('FreeCADPlusCategoryPicking',True)
                try:
                    Gui.Selection.addSelection(box,['Face1','Edge1'])
                    self.assertEqual([sub for e in Gui.Selection.getSelectionEx() for sub in e.SubElementNames],
                                     ['Face1'] if allowed else [])
                    Gui.Selection.clearPreselection()
                    Gui.Selection.setPreselection(box,'Face1',tp=0)
                    self.assertEqual(bool(Gui.Selection.getPreselection().ObjectName),allowed)
                finally:
                    category_selection._controller.end_pick()
        finally:
            Gui.Selection.removeSelectionGate()
        self.category_toggle('Faces',False)
        self.ribbon.host.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'ribbon-categories.png'))
        button = self.ribbon.common.findChild(QtWidgets.QToolButton, 'PlusSelectionCategories')
        def capture_menu():
            button.menu().grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'category-menu.png'))
            button.menu().close()
        QtCore.QTimer.singleShot(100, capture_menu)
        QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton)

    def test_category_native_model_boxes(self):
        import Part
        doc=App.newDocument('CategoryBoxes');box=doc.addObject('Part::Feature','Box')
        box.Shape=Part.makeBox(20,10,4,App.Vector(-10,-5,0));doc.recompute()
        view=Gui.activeDocument().activeView()
        view.setCameraType('Orthographic');view.viewTop();view.fitAll();view.getCameraNode().height=40;settle()
        self.category_toggle('Bodies',False)
        self.assertFalse(self.drag_box(view,(-12,7),(12,-7),'Std_BoxSelection'))
        self.category_toggle('Bodies',True)
        self.assertTrue(self.drag_box(view,(-12,7),(12,-7),'Std_BoxSelection'))
        box.Visibility=False
        curve=doc.addObject('Part::Feature','Curve');curve.Shape=Part.makeLine(App.Vector(-10,5,0),App.Vector(10,5,0))
        doc.recompute();settle()
        self.category_toggle('Curves',False)
        self.assertFalse(self.drag_box(view,(-12,7),(12,3),'Std_BoxElementSelection'))
        self.category_toggle('Curves',True)
        self.assertTrue(self.drag_box(view,(-12,7),(12,3),'Std_BoxElementSelection'))
        self.category_toggle('Curves',False)
        self.prefs.SetInt('ToolbarUIMode',1);ui_modes.apply_modes()
        self.assertTrue(self.drag_box(view,(-12,7),(12,3),'Std_BoxElementSelection'))

    def test_category_native_sketch_click_and_box(self):
        import Part
        self.tab('Sketch');doc=App.newDocument('CategorySketch')
        sketch=doc.addObject('Sketcher::SketchObject','Sketch')
        sketch.addGeometry(Part.LineSegment(App.Vector(-10,5,0),App.Vector(10,5,0)),False)
        doc.recompute();Gui.activeDocument().setEdit(sketch.Name);settle()
        view=Gui.activeDocument().activeView();view.viewTop();view.getCameraNode().height=40;settle()
        def click():
            Gui.Selection.clearSelection()
            widget=view.graphicsView().viewport();ratio=widget.devicePixelRatioF()
            screen=view.getPointOnScreen(App.Vector(-5,5,0))
            position=QtCore.QPoint(round(screen[0]/ratio),widget.height()-1-round(screen[1]/ratio))
            event=QtGui.QMouseEvent(QtCore.QEvent.MouseMove,QtCore.QPointF(position),
                                   QtCore.QPointF(widget.mapToGlobal(position)),QtCore.Qt.NoButton,
                                   QtCore.Qt.NoButton,QtCore.Qt.NoModifier)
            QtWidgets.QApplication.sendEvent(widget,event);settle()
            QtTest.QTest.mouseClick(widget,QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,position);settle()
            return [s for entry in Gui.Selection.getSelectionEx() for s in entry.SubElementNames]
        for allowed in (False,True):
            self.category_toggle('Curves',allowed)
            picked=self.drag_box(view,(-12,7),(12,3),capture='category-sketch-box.png' if allowed else None)
            self.assertEqual(any('Edge1' in e.SubElementNames for e in picked),allowed,
                             ([e.SubElementNames for e in picked],str(sketch.Geometry)))
            self.assertEqual('Edge1' in click(),allowed)
        # Removing a command's gate must not remove category admission, and an
        # active gate must still restrict Sketcher's batch-selection path.
        class Refuse:
            def allow(self,doc,obj,sub):return False
        Gui.Selection.addSelectionGate(Refuse())
        try:
            self.assertFalse(self.drag_box(view,(-12,7),(12,3)))
        finally:
            Gui.Selection.removeSelectionGate()
        self.category_toggle('Curves',False)
        picked = [s for e in self.drag_box(view,(-12,7),(12,3)) for s in e.SubElementNames]
        self.assertNotIn('Edge1', picked)
        self.assertIn('Vertex1', picked)  # Points remain independently enabled.
        self.category_toggle('Points',False)
        self.assertFalse(self.drag_box(view,(-12,7),(12,3)))
        self.prefs.SetInt('ToolbarUIMode',1);ui_modes.apply_modes()
        self.assertIn('Edge1',click())

    def sketch_click_fixture(self, connected=False, lines=None):
        import Part
        self.tab('Sketch')
        doc = App.newDocument('PlusSketchClicks')
        sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')
        if lines is None:
            lines = [((-10, 5), (10, 5)), ((-10, -5), (10, -5))]
        if connected:
            lines = [((-10, 5), (0, 5)), ((0, 5), (10, 5)), ((-10, -5), (10, -5))]
        for start, end in lines:
            sketch.addGeometry(Part.LineSegment(App.Vector(*start, 0), App.Vector(*end, 0)), False)
        doc.recompute()
        Gui.activeDocument().setEdit(sketch.Name)
        settle()
        view = Gui.activeDocument().activeView()
        view.setAnimationEnabled(False)
        view.viewTop()
        view.fitAll()
        view.getCameraNode().height = 40
        settle()
        return sketch, view

    def sketch_click(self, view, xy, modifiers=QtCore.Qt.NoModifier):
        widget = view.graphicsView().viewport()
        ratio = widget.devicePixelRatioF()
        screen = view.getPointOnScreen(App.Vector(*xy, 0))
        pos = QtCore.QPoint(round(screen[0]/ratio), widget.height()-1-round(screen[1]/ratio))
        self.assertTrue(widget.rect().contains(pos))
        hover = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(pos),
                                 QtCore.QPointF(widget.mapToGlobal(pos)), QtCore.Qt.NoButton,
                                 QtCore.Qt.NoButton, modifiers)
        QtWidgets.QApplication.sendEvent(widget, hover)
        settle()
        QtTest.QTest.mouseClick(widget, QtCore.Qt.LeftButton, modifiers, pos)
        settle()
        return {s for e in Gui.Selection.getSelectionEx() for s in e.SubElementNames}

    def persistent(self, checked):
        button = self.ribbon.common.findChild(QtWidgets.QToolButton, 'PlusPersistentSelection')
        self.assertIsNotNone(button)
        if button.isChecked() != checked:
            QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton)
            settle()
        self.assertEqual(selection_toolbar.preferences().GetBool('Persistent', True), checked)

    def sketch_command(self, name):
        button = self.ribbon.scroll.widget().findChild(QtWidgets.QToolButton, 'Plus_' + name)
        groups = {
            'Sketcher_CompHorVer': ('Sketcher_ConstrainHorVer', 'Sketcher_ConstrainHorizontal',
                                   'Sketcher_ConstrainVertical'),
            'Sketcher_CompDimensionTools': ('Sketcher_Dimension', None, 'Sketcher_ConstrainDistanceX',
                'Sketcher_ConstrainDistanceY', 'Sketcher_ConstrainDistance', 'Sketcher_ConstrainRadiam',
                'Sketcher_ConstrainRadius', 'Sketcher_ConstrainDiameter', 'Sketcher_ConstrainAngle',
                'Sketcher_ConstrainLock'),
        }
        grouped = None
        if button is None:
            grouped = next((choices for group, choices in groups.items() if name in choices), None)
            if grouped:
                group = next(group for group, choices in groups.items() if choices == grouped)
                button = self.ribbon.scroll.widget().findChild(QtWidgets.QToolButton, 'Plus_' + group)
        self.assertIsNotNone(button, name)
        self.ribbon.scroll.ensureWidgetVisible(button)
        settle()
        self.assertTrue(button.isEnabled(), name)
        if grouped:
            menu = button.menu()
            action = menu.actions()[grouped.index(name)]
            spy = QtTest.QSignalSpy(action.triggered)
            def choose():
                QtTest.QTest.mouseClick(menu, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                                       menu.actionGeometry(action).center())
            QtCore.QTimer.singleShot(100, choose)
            QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                                   QtCore.QPoint(button.width()-4, button.height()//2))
            self.assertEqual(spy.count(), 1)
        else:
            QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton)
        settle()

    def selected_subelements(self):
        return {s for e in Gui.Selection.getSelectionEx() for s in e.SubElementNames}

    def constraint_inputs(self, sketch, names):
        Gui.Selection.clearSelection()
        for name in names:
            Gui.Selection.addSelection(sketch, name)
        settle()
        self.assertEqual(self.selected_subelements(), set(names))

    def check_constraint_retention(self, sketch, command, names, kind, dispatch=None):
        doc = sketch.Document
        doc.UndoMode = 1
        geometry_count = sketch.GeometryCount
        for classic, persistent in ((False, True), (False, False), (True, True)):
            with self.subTest(command=command, classic=classic, persistent=persistent):
                self.prefs.SetInt('ToolbarUIMode', 0)
                ui_modes.apply_modes()
                self.persistent(persistent)
                if classic:
                    self.prefs.SetInt('ToolbarUIMode', 1)
                    ui_modes.apply_modes()
                self.constraint_inputs(sketch, names)
                undo = doc.UndoCount
                try:
                    if dispatch:
                        dispatch(command, classic)
                    elif classic:
                        Gui.runCommand(command)
                        settle()
                    else:
                        self.sketch_command(command)
                    self.assertEqual(sketch.ConstraintCount, 1)
                    self.assertEqual(sketch.Constraints[0].Type, kind)
                    self.assertEqual(sketch.solve(), 0)
                    self.assertTrue(all(g.toShape().isValid() for g in sketch.Geometry))
                    self.assertEqual(sketch.GeometryCount, geometry_count)
                    self.assertEqual(doc.UndoCount, undo + 1)
                    self.assertEqual(self.selected_subelements(),
                                     set(names) if persistent and not classic else set())
                    if command == 'Sketcher_ConstrainParallel' and persistent and not classic:
                        view = Gui.activeDocument().activeView()
                        output = Path(os.environ['PLUS_TEST_DIR'])/'persistent-parallel.png'
                        if os.name == 'nt':
                            from TestComponentFading import capture
                            capture(view, output, prepare=False)
                        else:
                            view.graphicsView().viewport().grabFramebuffer().save(str(output))
                    doc.undo()
                    settle()
                    self.assertEqual(sketch.ConstraintCount, 0)
                    self.assertEqual(sketch.GeometryCount, geometry_count)
                    doc.redo()
                    settle()
                    self.assertEqual(sketch.ConstraintCount, 1)
                    doc.undo()
                    settle()
                finally:
                    if doc.UndoCount > undo:
                        doc.undo()
                        settle()
        self.prefs.SetInt('ToolbarUIMode', 0)
        ui_modes.apply_modes()

    def test_constraint_retention_line_operations(self):
        sketch, view = self.sketch_click_fixture(lines=[((-10, 4), (8, 6)),
                                                       ((-8, -6), (10, -4))])
        for suffix, names, kind in (
                ('HorVer', ('Edge1',), 'Horizontal'),
                ('Horizontal', ('Edge1',), 'Horizontal'),
                ('Vertical', ('Edge1',), 'Vertical'),
                ('Parallel', ('Edge1', 'Edge2'), 'Parallel'),
                ('Block', ('Edge1',), 'Block')):
            self.check_constraint_retention(sketch, 'Sketcher_Constrain' + suffix, names, kind)

    def test_constraint_retention_points_and_symmetry(self):
        sketch, view = self.sketch_click_fixture()
        for command, names, kind in (
                ('Horizontal', ('Vertex1', 'Vertex3'), 'Horizontal'),
                ('Vertical', ('Vertex1', 'Vertex3'), 'Vertical'),
                ('CoincidentUnified', ('Vertex2', 'Vertex3'), 'Coincident'),
                ('CoincidentUnified', ('Vertex1', 'Edge2'), 'PointOnObject'),
                ('Symmetric', ('Edge1', 'Vertex3'), 'Symmetric'),
                ('Symmetric', ('Vertex1', 'Vertex2', 'Vertex3'), 'Symmetric'),
                ('Symmetric', ('Vertex1', 'Vertex2', 'V_Axis'), 'Symmetric')):
            self.check_constraint_retention(sketch, 'Sketcher_Constrain' + command, names, kind)

    def test_constraint_retention_concentric(self):
        import Part
        sketch, view = self.sketch_click_fixture()
        Gui.activeDocument().resetEdit()
        sketch.delGeometries([0, 1])
        for center, radius in ((App.Vector(-4, 3, 0), 3), (App.Vector(4, -3, 0), 5)):
            sketch.addGeometry(Part.Circle(center, App.Vector(0, 0, 1), radius), False)
        sketch.Document.recompute()
        Gui.activeDocument().setEdit(sketch.Name)
        settle()
        self.check_constraint_retention(sketch, 'Sketcher_ConstrainCoincidentUnified',
                                        ('Edge1', 'Edge2'), 'Coincident')

    def constraint_warning_timer(self):
        timer = QtCore.QTimer()
        def dismiss():
            modal = QtWidgets.QApplication.activeModalWidget()
            if isinstance(modal, QtWidgets.QDialog):
                modal.accept()
        timer.timeout.connect(dismiss)
        timer.start(25)
        self.addCleanup(timer.deleteLater)
        self.addCleanup(timer.stop)
        return timer

    def test_constraint_retention_rejections(self):
        import Sketcher
        sketch, view = self.sketch_click_fixture()
        sketch.Document.UndoMode = 1
        timer = self.constraint_warning_timer()
        for persistent in (True, False):
            self.persistent(persistent)
            self.constraint_inputs(sketch, ('Vertex1',))
            undo = sketch.Document.UndoCount
            self.sketch_command('Sketcher_ConstrainBlock')
            self.assertEqual(sketch.ConstraintCount, 0)
            self.assertEqual(sketch.Document.UndoCount, undo)
            self.assertEqual(self.selected_subelements(), {'Vertex1'})
        sketch.addConstraint(Sketcher.Constraint('Coincident', 0, 2, 1, 1))
        sketch.Document.recompute()
        self.constraint_inputs(sketch, ('Vertex2', 'Vertex3'))
        undo = sketch.Document.UndoCount
        self.sketch_command('Sketcher_ConstrainCoincidentUnified')
        self.assertEqual(sketch.ConstraintCount, 1)
        self.assertEqual(sketch.Document.UndoCount, undo)
        self.assertEqual(self.selected_subelements(), {'Vertex2', 'Vertex3'})
        timer.stop()

    def test_constraint_retention_tangency_substitution(self):
        import math
        import Part
        import Sketcher
        sketch, view = self.sketch_click_fixture()
        Gui.activeDocument().resetEdit()
        sketch.delGeometries([0, 1])
        sketch.addGeometry(Part.LineSegment(App.Vector(-10, 0, 0), App.Vector(0, 0, 0)), False)
        sketch.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(0, 5, 0), App.Vector(0, 0, 1), 5),
                                          -math.pi/2, 0), False)
        sketch.addConstraint(Sketcher.Constraint('Tangent', 0, 1))
        sketch.Document.recompute()
        Gui.activeDocument().setEdit(sketch.Name)
        settle()
        sketch.Document.UndoMode = 1
        timer = self.constraint_warning_timer()
        for names in (('Vertex2', 'Vertex3'), ('Vertex2', 'Edge2')):
            self.constraint_inputs(sketch, names)
            undo = sketch.Document.UndoCount
            self.sketch_command('Sketcher_ConstrainCoincidentUnified')
            self.assertEqual(sketch.ConstraintCount, 1)
            constraint = sketch.Constraints[0]
            self.assertEqual(constraint.Type, 'Tangent')
            self.assertEqual(constraint.FirstPos, 2)
            self.assertEqual(constraint.SecondPos, 1 if names[1] == 'Vertex3' else 0)
            self.assertEqual(self.selected_subelements(), set(names))
            self.assertEqual(sketch.GeometryCount, 2)
            self.assertEqual(sketch.Document.UndoCount, undo + 1)
            sketch.Document.undo()
            settle()
            self.assertEqual(sketch.Constraints[0].FirstPos, 0)
        timer.stop()

    def test_constraint_retention_interactive_picker_cleanup(self):
        sketch, view = self.sketch_click_fixture()
        Gui.Selection.clearSelection()
        self.sketch_command('Sketcher_ConstrainHorizontal')
        self.assertFalse(self.sketch_click(view, (-5, 5)))
        self.assertEqual(sketch.ConstraintCount, 1)
        self.assertFalse(self.sketch_click(view, (-5, -5)))
        self.assertEqual(sketch.ConstraintCount, 2)
        self.assertTrue(all(c.Type == 'Horizontal' for c in sketch.Constraints))
        QtTest.QTest.keyClick(view.graphicsView().viewport(), QtCore.Qt.Key_Escape)
        settle()
        self.assertIsNotNone(Gui.activeDocument().getInEdit())
        self.assertFalse(self.selected_subelements())

    def dimension_action(self, command, classic=False, text=None, accept=True,
                         reference=False, invoke=None):
        seen, errors = [], []
        timer = QtCore.QTimer()
        def respond():
            dialog = QtWidgets.QApplication.activeModalWidget()
            if not dialog or dialog.objectName() != 'SketcherGui__InsertDatum':
                return
            timer.stop()
            seen.append(dialog.windowTitle())
            try:
                if text is not None:
                    quantity = dialog.findChild(QtWidgets.QWidget, 'labelEdit')
                    editor = quantity.findChild(QtWidgets.QLineEdit)
                    self.assertIsNotNone(editor)
                    editor.setFocus()
                    QtTest.QTest.keyClick(editor, QtCore.Qt.Key_A, QtCore.Qt.ControlModifier)
                    QtTest.QTest.keyClicks(editor, text)
                    QtTest.QTest.keyClick(editor, QtCore.Qt.Key_Tab)
                if reference:
                    check = dialog.findChild(QtWidgets.QCheckBox, 'cbDriving')
                    QtTest.QTest.mouseClick(check, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                                           QtCore.QPoint(8, check.height()//2))
                    self.assertTrue(check.isChecked())
                box = dialog.findChild(QtWidgets.QDialogButtonBox, 'buttonBox')
                role = QtWidgets.QDialogButtonBox.Ok if accept else QtWidgets.QDialogButtonBox.Cancel
                self.assertTrue(box.button(role).isEnabled())
                QtTest.QTest.mouseClick(box.button(role), QtCore.Qt.LeftButton)
            except BaseException as error:
                errors.append(repr(error))
                dialog.reject()
        timer.timeout.connect(respond)
        timer.start(25)
        try:
            if invoke:
                invoke()
            elif classic:
                Gui.runCommand(command)
                settle()
            else:
                self.sketch_command(command)
        finally:
            timer.stop()
            timer.deleteLater()
        self.assertEqual(errors, [])
        self.assertEqual(len(seen), 1)
        settle()

    def dimension_preferences(self, show=True):
        prefs = App.ParamGet('User parameter:BaseApp/Preferences/Mod/Sketcher')
        self.addCleanup(prefs.SetBool, 'ShowDialogOnDistanceConstraint',
                        prefs.GetBool('ShowDialogOnDistanceConstraint', True))
        prefs.SetBool('ShowDialogOnDistanceConstraint', show)

    def dimension_circles(self):
        import Part
        sketch, view = self.sketch_click_fixture()
        Gui.activeDocument().resetEdit()
        sketch.delGeometries([0, 1])
        for x, radius in ((-6, 3), (6, 4)):
            sketch.addGeometry(Part.Circle(App.Vector(x, 0, 0), App.Vector(0, 0, 1), radius), False)
        sketch.Document.recompute()
        Gui.activeDocument().setEdit(sketch.Name)
        settle()
        return sketch, view

    def test_dimension_retention_lengths_and_angle(self):
        self.dimension_preferences()
        sketch, view = self.sketch_click_fixture(lines=[((-10, 4), (8, 6)), ((-8, -6), (10, -4))])
        for suffix, kind, value in (('DistanceX', 'DistanceX', '25 mm'),
                                    ('DistanceY', 'DistanceY', '8 mm'),
                                    ('Distance', 'Distance', '22 mm'),
                                    ('Angle', 'Angle', '30 deg')):
            def dispatch(command, classic):
                self.dimension_action(command, classic, text=value)
                expected = App.Units.Quantity(value).Value
                if kind == 'Angle':
                    import math
                    expected = math.radians(expected)
                self.assertAlmostEqual(sketch.Constraints[0].Value, expected, places=5)
                if suffix == 'DistanceX' and not classic and selection_toolbar.preferences().GetBool('Persistent'):
                    # Native datum autoscaling changes camera scale; Undo restores geometry only.
                    view.fitAll()
                    settle()
                    output = Path(os.environ['PLUS_TEST_DIR'])/'persistent-dimension.png'
                    if os.name == 'nt':
                        from TestComponentFading import capture
                        capture(view, output, prepare=False)
                    else:
                        view.graphicsView().viewport().grabFramebuffer().save(str(output))
            self.check_constraint_retention(sketch, 'Sketcher_Constrain' + suffix,
                                            ('Edge1',), kind, dispatch)

    def test_dimension_retention_circular(self):
        self.dimension_preferences()
        sketch, view = self.dimension_circles()
        for suffix, kind, value in (('Radius', 'Radius', '5 mm'),
                                    ('Diameter', 'Diameter', '10 mm'),
                                    ('Radiam', 'Diameter', '10 mm')):
            def dispatch(command, classic):
                self.dimension_action(command, classic, text=value)
                self.assertAlmostEqual(sketch.Constraints[0].Value, 5 if kind == 'Radius' else 10)
            self.check_constraint_retention(sketch, 'Sketcher_Constrain' + suffix,
                                            ('Edge1',), kind, dispatch)

    def test_dimension_retention_cancel(self):
        self.dimension_preferences()
        sketch, view = self.dimension_circles()
        sketch.Document.UndoMode = 1
        for classic, persistent in ((False, True), (False, False), (True, True)):
            self.prefs.SetInt('ToolbarUIMode', 0)
            ui_modes.apply_modes()
            self.persistent(persistent)
            if classic:
                self.prefs.SetInt('ToolbarUIMode', 1)
                ui_modes.apply_modes()
            names = ('Edge1', 'Edge2')
            self.constraint_inputs(sketch, names)
            undo = sketch.Document.UndoCount
            before = [g.Radius for g in sketch.Geometry]
            self.dimension_action('Sketcher_ConstrainRadius', classic, text='8 mm', accept=False)
            self.assertEqual(sketch.ConstraintCount, 0)
            self.assertEqual(sketch.Document.UndoCount, undo)
            self.assertEqual([g.Radius for g in sketch.Geometry], before)
            self.assertEqual(self.selected_subelements(), set() if classic else set(names))
            self.assertEqual(sketch.solve(), 0)

    def test_dimension_retention_reference_and_no_dialog(self):
        self.dimension_preferences()
        sketch, view = self.sketch_click_fixture()
        def dispatch(command, classic):
            self.dimension_action(command, classic, reference=True)
            self.assertFalse(sketch.getDriving(0))
        self.check_constraint_retention(sketch, 'Sketcher_ConstrainDistance', ('Edge1',), 'Distance', dispatch)
        self.dimension_preferences(show=False)
        self.check_constraint_retention(sketch, 'Sketcher_ConstrainDistance', ('Edge1',), 'Distance')

    def test_dimension_retention_batch_radius(self):
        self.dimension_preferences()
        sketch, view = self.dimension_circles()
        sketch.Document.UndoMode = 1
        self.constraint_inputs(sketch, ('Edge1', 'Edge2'))
        undo = sketch.Document.UndoCount
        self.dimension_action('Sketcher_ConstrainRadius', text='5 mm')
        self.assertEqual([c.Type for c in sketch.Constraints], ['Equal', 'Radius'])
        self.assertEqual(sketch.solve(), 0)
        self.assertTrue(all(g.toShape().isValid() for g in sketch.Geometry))
        self.assertTrue(all(abs(g.Radius-5) < 1e-7 for g in sketch.Geometry))
        self.assertEqual(self.selected_subelements(), {'Edge1', 'Edge2'})
        self.assertEqual(sketch.Document.UndoCount, undo+1)
        sketch.Document.undo()
        settle()
        self.assertEqual(sketch.ConstraintCount, 0)
        self.assertEqual([g.Radius for g in sketch.Geometry], [3, 4])
        sketch.Document.redo()
        settle()
        self.assertEqual(sketch.ConstraintCount, 2)
        self.assertTrue(all(abs(g.Radius-5) < 1e-7 for g in sketch.Geometry))

    def test_dimension_retention_continuous(self):
        self.dimension_preferences()
        sketch, view = self.sketch_click_fixture()
        Gui.Selection.clearSelection()
        self.sketch_command('Sketcher_ConstrainDistance')
        for point, count in (((-5, 5), 1), ((-5, -5), 2)):
            self.dimension_action(None, invoke=lambda: self.sketch_click(view, point))
            self.assertEqual(sketch.ConstraintCount, count)
            self.assertFalse(self.selected_subelements())
            self.assertEqual(sketch.solve(), 0)
        QtTest.QTest.keyClick(view.graphicsView().viewport(), QtCore.Qt.Key_Escape)
        settle()
        self.assertIsNotNone(Gui.activeDocument().getInEdit())
        self.assertFalse(self.selected_subelements())

    def test_persistent_control_scope_and_saved_choice(self):
        selection_toolbar.preferences().RemBool('Persistent')
        self.ribbon.refresh()
        button = self.ribbon.common.findChild(QtWidgets.QToolButton, 'PlusPersistentSelection')
        self.assertTrue(button.isChecked())
        self.assertFalse(button.icon().isNull())
        self.persistent(False)
        self.tab('Home')
        self.assertFalse(self.ribbon.common.findChild(QtWidgets.QToolButton, 'PlusPersistentSelection').isChecked())
        Gui.activateWorkbench('FemWorkbench')
        ui_modes.apply_modes()
        self.assertIsNone(self.ribbon.common.findChild(QtWidgets.QToolButton, 'PlusPersistentSelection'))
        self.assertIsNone(Gui.getMainWindow().property('FreeCADPlusPersistentSelection'))
        Gui.activateWorkbench('PartDesignWorkbench')
        ui_modes.apply_modes()
        self.persistent(True)
        self.prefs.SetInt('ToolbarUIMode', 1)
        ui_modes.apply_modes()
        self.assertIsNone(Gui.getMainWindow().property('FreeCADPlusPersistentSelection'))
        self.prefs.SetInt('ToolbarUIMode', 0)
        ui_modes.apply_modes()
        self.assertTrue(Gui.getMainWindow().property('FreeCADPlusPersistentSelection'))

    def test_persistent_equal_construction_and_cleanup(self):
        sketch, view = self.sketch_click_fixture()
        doc = sketch.Document
        doc.UndoMode = 1
        self.sketch_click(view, (-5, 5))
        self.sketch_click(view, (-5, -5), QtCore.Qt.ShiftModifier)
        inputs = {'Edge1', 'Edge2'}
        self.assertEqual(self.selected_subelements(), inputs)
        undo = doc.UndoCount
        self.sketch_command('Sketcher_ConstrainEqual')
        self.assertEqual(sketch.ConstraintCount, 1)
        self.assertEqual(sketch.Constraints[0].Type, 'Equal')
        self.assertEqual(doc.UndoCount, undo + 1)
        self.assertEqual(self.selected_subelements(), inputs)
        self.sketch_command('Sketcher_ToggleConstruction')
        self.assertTrue(all(sketch.getConstruction(i) for i in range(2)))
        self.assertEqual(doc.UndoCount, undo + 2)
        self.assertEqual(self.selected_subelements(), inputs)
        output = Path(os.environ['PLUS_TEST_DIR'])/'persistent-construction.png'
        if os.name == 'nt':
            from TestComponentFading import capture
            capture(view, output, prepare=False)
        else:
            view.graphicsView().viewport().grabFramebuffer().save(str(output))
        # A second command consumes the retained native construction indices.
        self.sketch_command('Sketcher_ToggleConstruction')
        self.assertFalse(any(sketch.getConstruction(i) for i in range(2)))
        self.assertEqual(self.selected_subelements(), inputs)
        doc.undo()
        settle()
        self.assertTrue(all(sketch.getConstruction(i) for i in range(2)))
        doc.undo()
        settle()
        self.assertFalse(any(sketch.getConstruction(i) for i in range(2)))
        doc.undo()
        settle()
        self.assertEqual(sketch.ConstraintCount, 0)
        doc.redo()
        settle()
        self.assertEqual(sketch.ConstraintCount, 1)
        self.assertEqual(self.sketch_click(view, (-5, 5)), {'Edge1'})
        QtTest.QTest.keyClick(view.graphicsView().viewport(), QtCore.Qt.Key_Escape)
        settle()
        self.assertFalse(self.selected_subelements())
        self.assertIsNotNone(Gui.activeDocument().getInEdit())
        self.sketch_click(view, (-5, 5))
        self.assertFalse(self.sketch_click(view, (15, 10)))
        self.sketch_click(view, (-5, 5))
        QtTest.QTest.keyClick(view.graphicsView().viewport(), QtCore.Qt.Key_Delete)
        settle()
        self.assertEqual(sketch.GeometryCount, 1)
        self.assertFalse(self.selected_subelements())
        Gui.activeDocument().resetEdit()
        settle()
        self.assertFalse(self.selected_subelements())

    def test_persistent_off_and_classic_commands(self):
        sketch, view = self.sketch_click_fixture()
        self.persistent(False)
        self.sketch_click(view, (-5, 5))
        self.sketch_click(view, (-5, -5), QtCore.Qt.ControlModifier)
        self.sketch_command('Sketcher_ConstrainEqual')
        self.assertEqual(sketch.ConstraintCount, 1)
        self.assertFalse(self.selected_subelements())
        self.sketch_click(view, (-5, 5))
        self.sketch_click(view, (-5, -5), QtCore.Qt.ControlModifier)
        self.sketch_command('Sketcher_ToggleConstruction')
        self.assertTrue(all(sketch.getConstruction(i) for i in range(2)))
        self.assertFalse(self.selected_subelements())
        # A saved ON preference must not change the original Classic command.
        self.persistent(True)
        self.prefs.SetInt('ToolbarUIMode', 1)
        ui_modes.apply_modes()
        settle()
        Gui.Selection.addSelection(sketch, 'Edge1')
        Gui.Selection.addSelection(sketch, 'Edge2')
        Gui.runCommand('Sketcher_ToggleConstruction')
        settle()
        self.assertFalse(any(sketch.getConstruction(i) for i in range(2)))
        self.assertFalse(self.selected_subelements())
        sketch.delConstraint(0)
        Gui.Selection.addSelection(sketch, 'Edge1')
        Gui.Selection.addSelection(sketch, 'Edge2')
        Gui.runCommand('Sketcher_ConstrainEqual')
        settle()
        self.assertEqual(sketch.ConstraintCount, 1)
        self.assertFalse(self.selected_subelements())

    def test_persistent_rejected_equal_preserves_inputs(self):
        sketch, view = self.sketch_click_fixture()
        sketch.Document.UndoMode = 1
        # This rejection happens before transaction creation and must keep inputs
        # even with persistence OFF. Native notifications remain visible.
        self.persistent(False)
        self.sketch_click(view, (-5, 5))
        undo = sketch.Document.UndoCount
        timer = QtCore.QTimer()
        def dismiss_warning():
            modal = QtWidgets.QApplication.activeModalWidget()
            if isinstance(modal, QtWidgets.QMessageBox):
                modal.accept()
        timer.timeout.connect(dismiss_warning)
        timer.start(25)
        try:
            self.sketch_command('Sketcher_ConstrainEqual')
        finally:
            timer.stop()
            timer.deleteLater()
        self.assertEqual(sketch.ConstraintCount, 0)
        self.assertEqual(sketch.Document.UndoCount, undo)
        self.assertEqual(self.selected_subelements(), {'Edge1'})

    def test_sketch_plain_click_replacement_and_modifiers(self):
        sketch, view = self.sketch_click_fixture()
        # Directional off still uses Plus click semantics.
        self.directional(False)
        click = lambda xy, modifiers=QtCore.Qt.NoModifier: self.sketch_click(view, xy, modifiers)
        self.assertEqual(click((-5, 5)), {'Edge1'})
        self.assertEqual(click((-5, -5)), {'Edge2'})
        self.assertEqual(click((-5, -5)), {'Edge2'})
        self.assertEqual(click((-10, 5)), {'Vertex1'})
        self.assertEqual(click((-10, -5)), {'Vertex3'})
        for modifier in (QtCore.Qt.ControlModifier, QtCore.Qt.ShiftModifier):
            self.assertEqual(click((-5, 5)), {'Edge1'})
            self.assertEqual(click((-5, -5), modifier), {'Edge1', 'Edge2'})
            self.assertEqual(click((15, 10), modifier), {'Edge1', 'Edge2'})
            self.assertEqual(click((-5, -5), modifier), {'Edge1'})
        self.assertFalse(click((15, 10)))
        self.assertEqual(click((-5, 5)), {'Edge1'})
        QtTest.QTest.keyClick(view.graphicsView().viewport(), QtCore.Qt.Key_Escape)
        settle()
        self.assertFalse(Gui.Selection.getSelection())
        self.assertIsNotNone(Gui.activeDocument().getInEdit())
        self.assertEqual(sketch.GeometryCount, 2)
        self.prefs.SetInt('ToolbarUIMode', 1)
        ui_modes.apply_modes()
        settle()
        self.assertEqual(click((-5, 5)), {'Edge1'})
        self.assertEqual(click((-5, -5)), {'Edge1', 'Edge2'})
        self.assertEqual(click((-5, -5)), {'Edge1'})
        self.assertFalse(click((15, 10)))

    def test_sketch_plain_constraint_click(self):
        import Sketcher
        sketch, view = self.sketch_click_fixture()
        sketch.addConstraint(Sketcher.Constraint('Horizontal', 0))
        sketch.Document.recompute()
        settle()
        widget = view.graphicsView().viewport()
        ratio = widget.devicePixelRatioF()
        center = view.getPointOnScreen(App.Vector(0, 5, 0))
        center = QtCore.QPoint(round(center[0]/ratio), widget.height()-1-round(center[1]/ratio))
        target = None
        # Locate the rendered native symbol using real hover, allowing its
        # theme/DPI-dependent placement instead of inventing a selection callback.
        for y in range(-96, 97, 6):
            for x in range(-96, 97, 6):
                pos = center + QtCore.QPoint(x, y)
                hover = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(pos),
                                         QtCore.QPointF(widget.mapToGlobal(pos)), QtCore.Qt.NoButton,
                                         QtCore.Qt.NoButton, QtCore.Qt.NoModifier)
                QtWidgets.QApplication.sendEvent(widget, hover)
                if 'Constraint1' in Gui.Selection.getPreselection().SubElementNames:
                    target = pos
                    break
            if target is not None:
                break
        self.assertIsNotNone(target, 'Native horizontal-constraint symbol was not found')
        self.assertEqual(self.sketch_click(view, (-5, -5)), {'Edge2'})
        for repeat in range(2):
            hover = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(target),
                                     QtCore.QPointF(widget.mapToGlobal(target)), QtCore.Qt.NoButton,
                                     QtCore.Qt.NoButton, QtCore.Qt.NoModifier)
            QtWidgets.QApplication.sendEvent(widget, hover)
            settle()
            QtTest.QTest.mouseClick(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, target)
            settle()
            self.assertEqual({s for e in Gui.Selection.getSelectionEx() for s in e.SubElementNames},
                             {'Constraint1'})
        self.assertEqual(self.sketch_click(view, (-5, -5)), {'Edge2'})
        self.assertEqual(sketch.ConstraintCount, 1)

    def test_sketch_plain_click_curve_intent_and_box(self):
        sketch, view = self.sketch_click_fixture(connected=True)
        self.curve_intent(1)
        picked = self.drag_box(view, (-12, 7), (12, -7))
        self.assertTrue({'Edge1', 'Edge2', 'Edge3'} <= {s for e in picked for s in e.SubElementNames})
        self.assertEqual(self.sketch_click(view, (-5, 5)), {'Edge1', 'Edge2'})
        self.assertEqual(self.sketch_click(view, (-5, -5)), {'Edge3'})
        self.assertEqual(self.sketch_click(view, (5, 5)), {'Edge1', 'Edge2'})
        self.assertEqual(self.sketch_click(view, (-5, -5)), {'Edge3'})
        self.assertEqual(sketch.GeometryCount, 3)
        path = Path(os.environ['PLUS_TEST_DIR'])/'sketch-plain-replacement.png'
        if os.name == 'nt':
            from TestComponentFading import capture
            capture(view, path, prepare=False)
        else:
            view.graphicsView().viewport().grabFramebuffer().save(str(path))

    def curve_intent(self, index):
        # Rebuilt controls still have their default geometry until Qt lays them out.
        settle()
        button = self.ribbon.common.findChild(QtWidgets.QToolButton, 'PlusCurveIntent')
        menu = button.menu()
        action = menu.actions()[index]
        observed = []
        def choose():
            observed.append(menu.isVisible())
            QtTest.QTest.mouseClick(menu, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                                   menu.actionGeometry(action).center())
        QtCore.QTimer.singleShot(100, choose)
        QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                               QtCore.QPoint(button.width()-4, button.height()//2))
        settle()
        self.assertEqual(observed, [True])
        self.assertEqual(button.defaultAction(), action)
        self.assertEqual(curve_selection.intent(), curve_selection.INTENTS[index])
        self.assertFalse(button.icon().isNull())
        self.assertEqual(len(menu.actions()), 3)
        self.assertEqual(sum(a.isChecked() for a in menu.actions()), 1)
        return button

    def test_curve_intent_control_and_scope(self):
        selection_toolbar.preferences().RemString('CurveIntent')
        self.ribbon.refresh()
        self.assertEqual(curve_selection.intent(), 'Single Curve')
        button = self.curve_intent(2)
        option = QtWidgets.QStyleOptionToolButton()
        button.initStyleOption(option)
        arrow = button.style().subControlRect(QtWidgets.QStyle.CC_ToolButton, option,
                                               QtWidgets.QStyle.SC_ToolButtonMenu, button)
        self.assertGreaterEqual(arrow.left(), button.iconSize().width())
        spy = QtTest.QSignalSpy(button.defaultAction().triggered)
        QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                               QtCore.QPoint(arrow.left()//2, button.height()//2))
        self.assertEqual(spy.count(), 1)
        self.assertFalse(button.menu().isVisible())
        button.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'curve-intent-split.png'))
        self.tab('Home')
        self.assertEqual(self.ribbon.common.findChild(QtWidgets.QToolButton, 'PlusCurveIntent').text(),
                         'Tangent Curves')
        Gui.activateWorkbench('FemWorkbench')
        ui_modes.apply_modes()
        self.assertFalse(curve_selection._controller.active)
        self.assertIsNone(self.ribbon.common.findChild(QtWidgets.QToolButton, 'PlusCurveIntent'))
        Gui.activateWorkbench('PartDesignWorkbench')
        ui_modes.apply_modes()
        self.assertTrue(curve_selection._controller.active)
        self.prefs.SetInt('ToolbarUIMode', 1)
        ui_modes.apply_modes()
        self.assertFalse(curve_selection._controller.active)
        self.assertEqual(curve_selection.intent(), 'Tangent Curves')

    def test_curve_intent_native_topology(self):
        import Part
        v = App.Vector
        line = lambda a,b: Part.makeLine(v(*a,0), v(*b,0))
        edges = {1:line((-10,0),(0,0)), 2:line((0,0),(10,0)), 3:line((10,0),(10,10))}
        self.assertEqual(curve_selection.connected(edges, 1), [1,2,3])
        self.assertEqual(curve_selection.connected(edges, 1, True), [1,2])
        edges[4] = line((0,0),(0,10))
        self.assertEqual(curve_selection.connected(edges, 1), [1,2,3,4])
        self.assertEqual(curve_selection.connected(edges, 1, True), [1])
        circle = Part.makeCircle(5, v(0,5,0))
        edges[5] = circle
        self.assertEqual(curve_selection.connected(edges, 5), [5])
        self.assertNotIn(5, curve_selection.connected(edges, 1))
        arc = Part.Arc(v(0,0,0),v(7.071067811865,2.928932188135,0),v(10,10,0)).toShape()
        smooth = {1:edges[1], 2:arc, 3:line((10,10),(10,20))}
        self.assertEqual(curve_selection.connected(smooth, 1, True), [1,2,3])
        box = Part.makeBox(10,10,10)
        combined = dict(enumerate(Part.makeCompound([box,box.copy()]).Edges,1))
        self.assertEqual(len(curve_selection.connected(combined, 1, topology=True)),12)
        doc = App.newDocument('CurveOwners')
        sketch = doc.addObject('Sketcher::SketchObject','Sketch')
        sketch.addGeometry(Part.Point(v(25,25,0)),True)
        sketch.addGeometry(Part.LineSegment(v(-10,0,0),v(0,0,0)),False)
        sketch.addGeometry(Part.LineSegment(v(0,0,0),v(10,0,0)),True)
        doc.recompute()
        self.assertEqual(curve_selection.candidates(sketch,'Edge1','Connected Curves'),['Edge1'])
        root = doc.addObject('App::Part','Root')
        link = doc.addObject('App::Link','Occurrence');link.setLink(sketch);root.addObject(link)
        doc.recompute()
        self.tab('Sketch')
        Gui.activeDocument().setEdit(sketch.Name);settle()
        self.assertEqual(curve_selection.candidates(sketch,'Edge2','Connected Curves'),['Edge2','Edge3'])
        self.assertEqual(curve_selection.candidates(root,'Occurrence.Edge2','Connected Curves'),
                         ['Occurrence.Edge2','Occurrence.Edge3'])

    def test_curve_intent_native_viewport_and_filters(self):
        import Part
        v = App.Vector
        doc = App.newDocument('CurvePicks')
        obj = doc.addObject('Part::Feature','Curves')
        obj.Shape = Part.makeCompound([Part.makeLine(v(-10,0,0),v(0,0,0)),
                                      Part.makeLine(v(0,0,0),v(10,0,0)),
                                      Part.makeLine(v(10,0,0),v(10,10,0))])
        separate = doc.addObject('Part::Feature','Separate')
        separate.Shape = Part.makeLine(v(10,10,0),v(15,10,0))
        doc.recompute()
        view = Gui.activeDocument().activeView()
        view.setCameraType('Orthographic');view.viewTop();view.fitAll()
        view.getCameraNode().height = 40
        settle()
        def picked():
            return {sub for entry in self.drag_box(view,(-11,2),(1,-2),'Std_BoxElementSelection')
                    for sub in entry.SubElementNames if entry.Object == obj}
        for index, expected in ((0,{'Edge1'}),(1,{'Edge1','Edge2','Edge3'}),(2,{'Edge1','Edge2'})):
            self.curve_intent(index)
            self.assertEqual(picked(),expected)
            self.assertNotIn(separate,Gui.Selection.getSelection())
        self.curve_intent(1)
        class OnlyFirst:
            def allow(self, doc, obj, sub): return sub == 'Edge1'
        Gui.Selection.addSelectionGate(OnlyFirst())
        try:
            self.assertEqual(picked(),{'Edge1'})
        finally:
            Gui.Selection.removeSelectionGate()
        # Programmatic command/collector selection and Classic are unchanged.
        Gui.Selection.clearSelection();Gui.Selection.addSelection(obj,'Edge1');settle()
        self.assertEqual(Gui.Selection.getSelectionEx()[0].SubElementNames,('Edge1',))
        self.prefs.SetInt('ToolbarUIMode',1);ui_modes.apply_modes()
        self.assertEqual(picked(),{'Edge1'})
        self.prefs.SetInt('ToolbarUIMode',0);ui_modes.apply_modes()
        obj.Visibility=False;separate.Visibility=False
        self.tab('Sketch')
        sketch=doc.addObject('Sketcher::SketchObject','Sketch')
        sketch.addGeometry(Part.LineSegment(v(-10,5,0),v(0,5,0)),False)
        sketch.addGeometry(Part.LineSegment(v(0,5,0),v(10,5,0)),True)
        doc.recompute();Gui.activeDocument().setEdit(sketch.Name);settle()
        view.viewTop();view.getCameraNode().height=40;settle()
        self.curve_intent(1)
        widget=view.graphicsView().viewport();ratio=widget.devicePixelRatioF()
        screen=view.getPointOnScreen(v(-5,5,0))
        position=QtCore.QPoint(round(screen[0]/ratio),widget.height()-1-round(screen[1]/ratio))
        Gui.Selection.clearSelection()
        event=QtGui.QMouseEvent(QtCore.QEvent.MouseMove,QtCore.QPointF(position),
                               QtCore.QPointF(widget.mapToGlobal(position)),QtCore.Qt.NoButton,
                               QtCore.Qt.NoButton,QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(widget,event);settle()
        QtTest.QTest.mouseClick(widget,QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,position);settle()
        self.assertEqual({s for entry in Gui.Selection.getSelectionEx() for s in entry.SubElementNames},
                         {'Edge1','Edge2'})
        self.ribbon.host.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'ribbon-curve-intent.png'))

    def test_directional_control_scope_and_saved_choice(self):
        selection_toolbar.preferences().RemBool('Directional')
        self.ribbon.refresh()
        self.assertTrue(self.ribbon.common.findChild(QtWidgets.QToolButton, 'PlusDirectionalSelection').isChecked())
        self.directional(False)
        self.tab('Home')
        self.assertFalse(self.ribbon.common.findChild(QtWidgets.QToolButton, 'PlusDirectionalSelection').isChecked())
        Gui.activateWorkbench('FemWorkbench')
        ui_modes.apply_modes()
        self.assertIsNone(self.ribbon.common.findChild(QtWidgets.QToolButton, 'PlusDirectionalSelection'))
        self.assertIsNone(Gui.getMainWindow().property('FreeCADPlusDirectionalSelection'))
        Gui.activateWorkbench('PartDesignWorkbench')
        ui_modes.apply_modes()
        self.assertFalse(self.ribbon.common.findChild(QtWidgets.QToolButton, 'PlusDirectionalSelection').isChecked())
        self.prefs.SetInt('ToolbarUIMode', 1)
        ui_modes.apply_modes()
        self.assertIsNone(Gui.getMainWindow().property('FreeCADPlusDirectionalSelection'))
        self.prefs.SetInt('ToolbarUIMode', 0)
        ui_modes.apply_modes()
        self.assertFalse(Gui.getMainWindow().property('FreeCADPlusDirectionalSelection'))

    def test_directional_native_object_and_element_boxes(self):
        import Part
        doc = App.newDocument('DirectionalBoxes')
        box = doc.addObject('Part::Feature', 'Box')
        box.Shape = Part.makeBox(20, 10, 4, App.Vector(-10, -5, 0))
        doc.recompute()
        view = Gui.activeDocument().activeView()
        view.setCameraType('Orthographic')
        view.viewTop()
        view.fitAll()
        view.getCameraNode().height = 40
        settle()
        # The marker is scoped to standard picking, including Escape cleanup.
        for command, picking in (('Std_BoxSelection', True), ('Std_ViewBoxZoom', False)):
            Gui.runCommand(command)
            settle()
            self.assertEqual(view.graphicsView().property('FreeCADPlusBoxSelection'), picking)
            QtTest.QTest.keyClick(view.graphicsView().viewport(), QtCore.Qt.Key_Escape)
            settle()
            self.assertIsNone(view.graphicsView().property('FreeCADPlusBoxSelection'))
        left, right = (-12, 7), (2, -7)
        for enabled in (True, False):
            self.directional(enabled)
            self.assertFalse(self.drag_box(view, left, right, 'Std_BoxSelection'))
            picked = self.drag_box(view, (2, 7), (-12, -7), 'Std_BoxSelection',
                                   'box-crossing.png' if enabled else 'box-enclosure.png')
            self.assertEqual(bool(picked), enabled)
            self.assertTrue(self.drag_box(view, (-12, 7), (12, -7), 'Std_BoxSelection'))
        # Native Classic left-to-right selection uses the box center, unchanged.
        self.prefs.SetInt('ToolbarUIMode', 1)
        ui_modes.apply_modes()
        self.assertTrue(self.drag_box(view, left, right, 'Std_BoxSelection'))
        self.prefs.SetInt('ToolbarUIMode', 0)
        ui_modes.apply_modes()
        self.directional(True)
        class Refuse:
            def allow(self, doc, obj, sub):
                return False
        Gui.Selection.addSelectionGate(Refuse())
        try:
            self.assertFalse(self.drag_box(view, (2, 7), (-12, -7), 'Std_BoxSelection'))
        finally:
            Gui.Selection.removeSelectionGate()
        box.Visibility = False
        curve = doc.addObject('Part::Feature', 'Curve')
        curve.Shape = Part.makeLine(App.Vector(-10, 0, 0), App.Vector(10, 0, 0))
        doc.recompute()
        for enabled in (True, False):
            self.directional(enabled)
            self.assertFalse(self.drag_box(view, (-12, 3), (2, -3), 'Std_BoxElementSelection'))
            self.assertEqual(bool(self.drag_box(view, (2, 3), (-12, -3), 'Std_BoxElementSelection')), enabled)
            self.assertTrue(self.drag_box(view, (-12, 3), (12, -3), 'Std_BoxElementSelection'))

    def test_directional_native_sketch_boxes(self):
        import Part
        self.tab('Sketch')
        doc = App.newDocument('DirectionalSketch')
        sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')
        sketch.addGeometry(Part.LineSegment(App.Vector(-10, 0, 0), App.Vector(10, 0, 0)), False)
        doc.recompute()
        Gui.activeDocument().setEdit(sketch.Name)
        settle()
        view = Gui.activeDocument().activeView()
        view.viewTop()
        view.fitAll()
        view.getCameraNode().height = 40
        settle()
        def has_edge(picked):
            return any('Edge1' in entry.SubElementNames for entry in picked)
        for enabled in (True, False):
            self.directional(enabled)
            self.assertFalse(has_edge(self.drag_box(view, (-12, 3), (2, -3))))
            self.assertEqual(has_edge(self.drag_box(view, (2, 3), (-12, -3),
                             capture='sketch-crossing.png' if enabled else 'sketch-enclosure.png')), enabled)
            self.assertTrue(has_edge(self.drag_box(view, (-12, 3), (12, -3))))
        self.prefs.SetInt('ToolbarUIMode', 1)
        ui_modes.apply_modes()
        self.assertTrue(has_edge(self.drag_box(view, (2, 3), (-12, -3))))

    def test_native_arc_split_and_last_used(self):
        r = self.ribbon
        self.tab('Sketch')
        doc = App.newDocument('RibbonArc')
        sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')
        Gui.activeDocument().setEdit(sketch.Name)
        settle()
        button = r.scroll.widget().findChild(QtWidgets.QToolButton, 'Plus_Sketcher_CompCreateArc')
        native_action, native_button = r.sources['Sketcher_CompCreateArc']
        self.assertIsNot(button, native_button)
        self.assertEqual(button.defaultAction(), native_action)
        self.assertEqual(button.menu(), native_button.menu())
        self.assertEqual(button.popupMode(), QtWidgets.QToolButton.MenuButtonPopup)
        menu = button.menu()
        choices = menu.actions()
        self.assertGreaterEqual(len(choices), 2)
        selected = choices[1]
        child_spy = QtTest.QSignalSpy(selected.triggered)
        root_spy = QtTest.QSignalSpy(native_action.triggered)
        observed = []
        def choose():
            observed.append(menu.isVisible())
            QtTest.QTest.mouseClick(menu, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                                   menu.actionGeometry(selected).center())
        QtCore.QTimer.singleShot(100, choose)
        QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                               QtCore.QPoint(button.width()-4, button.height()//2))
        settle()
        self.assertEqual(observed, [True])
        self.assertEqual(child_spy.count(), 1)
        self.assertEqual(root_spy.count(), 0)
        self.assertEqual(native_action.icon().cacheKey(), selected.icon().cacheKey())
        self.assertEqual(len(menu.actions()), len(choices))
        QtTest.QTest.keyClick(Gui.getMainWindow(), QtCore.Qt.Key_Escape)
        QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                               QtCore.QPoint(8, button.height()//2))
        settle()
        self.assertEqual(root_spy.count(), 1)
        self.assertFalse(menu.isVisible())
        # Same native action carries the last choice through Classic and tab rebuild.
        icon = native_action.icon().cacheKey()
        self.prefs.SetInt('ToolbarUIMode', 1)
        ui_modes.apply_modes()
        self.assertEqual(native_button.icon().cacheKey(), icon)
        self.assertTrue(r.native['Geometries'].isVisible())
        self.assertTrue(r.native['Sketcher'].isHidden())
        self.prefs.SetInt('ToolbarUIMode', 0)
        ui_modes.apply_modes()
        self.assertEqual(native_action.icon().cacheKey(), icon)
        # A live sketch blocks a switch to another native workbench.
        self.tab('Modeling')
        self.assertEqual(Gui.activeWorkbench().name(), 'SketcherWorkbench')
        self.assertTrue(Gui.activeDocument().getInEdit())
        r.host.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'ribbon-sketch.png'))
        Gui.activeDocument().resetEdit()
        settle()
        self.prefs.SetInt('ToolbarUIMode', 1)
        ui_modes.apply_modes()
        self.assertTrue(r.native['Sketcher'].isVisible())
        self.assertTrue(r.native['Geometries'].isHidden())

    def test_native_widget_factory_and_all_tools(self):
        r = self.ribbon
        native = Gui.Command.get('Std_Workbench')
        with self.assertRaises(TypeError):
            native.addToToolbar(QtWidgets.QWidget())
        with self.assertRaises(TypeError):
            native.addToToolbar(None)
        original_bar = r.native['Workbench']
        original_action = original_bar.actions()[0]
        original_widget = original_bar.widgetForAction(original_action)
        self.tab('All Tools')
        control = r.scroll.widget().findChild(QtWidgets.QToolBar, 'PlusControl_Std_Workbench')
        self.assertIsNotNone(control)
        widget = control.widgetForAction(control.actions()[0])
        self.assertEqual(widget.metaObject().className(), original_widget.metaObject().className())
        self.assertNotEqual(widget, original_widget)
        self.assertEqual(original_bar.widgetForAction(original_action), original_widget)
        self.assertEqual(widget.count(), original_widget.count())
        self.assertTrue(widget.isEnabled())
        groups = [w.objectName() for w in r.scroll.widget().findChildren(QtWidgets.QWidget)
                  if w.objectName().startswith('PlusGroup_')]
        self.assertEqual(len(groups), len(Gui.activeWorkbench().getToolbarItems()))
        self.assertIn('PlusGroup_Macro', groups)
        self.assertIn('PlusGroup_Clipboard', groups)
        self.assertIn('PlusGroup_Workbench', groups)
        self.assertIn('PlusGroup_Help', groups)
        self.assertIn('PlusGroup_Individual Views', groups)

    def test_added_workbench_expanded_group_and_custom_toolbar(self):
        class ExpandedGroup:
            def GetResources(self):
                return {'MenuText': 'Expanded views', 'DropDownMenu': False}

            def GetCommands(self):
                return ('Std_ViewFront', 'Std_ViewRear')

            def IsActive(self):
                return True

        class PlusCoverageWorkbench(Gui.Workbench):
            MenuText = 'Coverage workbench'
            ToolTip = 'Isolated toolbar acceptance fixture'

            def Initialize(self):
                self.appendToolbar('Coverage expanded', ['PlusCoverageExpanded', 'Separator', 'Std_ViewTop'])
                self.appendToolbar('Coverage custom', ['Std_Save', 'Std_Copy', 'Std_Paste'])

            def GetClassName(self):
                return 'Gui::PythonWorkbench'

        custom = App.ParamGet('User parameter:BaseApp/Workbench/Global/Toolbar/PlusCoverage')
        custom.SetString('Name', 'Coverage global')
        custom.SetString('Std_ViewFront', 'FreeCADGui')
        custom.SetString('Std_ViewRear', 'FreeCADGui')
        Gui.addCommand('PlusCoverageExpanded', ExpandedGroup())
        Gui.addWorkbench(PlusCoverageWorkbench())
        try:
            self.ribbon.selector.showPopup()
            self.ribbon.selector.hidePopup()
            index = next(i for i in range(self.ribbon.selector.count())
                         if self.ribbon.selector.itemData(i)[1] == 'PlusCoverageWorkbench')
            self.ribbon.selector.setCurrentIndex(index)
            settle()
            self.assertEqual(Gui.activeWorkbench().name(), 'PlusCoverageWorkbench')
            self.tab('All Tools')
            control = self.ribbon.scroll.widget().findChild(QtWidgets.QToolBar, 'PlusControl_PlusCoverageExpanded')
            self.assertIsNotNone(control)
            children = Gui.Command.get('PlusCoverageExpanded').getAction()
            self.assertEqual(len(children), 2)
            self.assertEqual(control.actions(), children)
            self.assertTrue(self.ribbon.scroll.widget().findChild(QtWidgets.QWidget, 'PlusGroup_Coverage custom'))
            self.assertTrue(self.ribbon.scroll.widget().findChild(QtWidgets.QWidget, 'PlusGroup_Coverage global'))
            native = self.ribbon.native['Coverage expanded']
            before = native.actions()
            self.prefs.SetInt('ToolbarUIMode', 1)
            ui_modes.apply_modes()
            self.assertTrue(native.isVisible())
            self.assertEqual(native.actions(), before)
        finally:
            App.ParamGet('User parameter:BaseApp/Workbench/Global/Toolbar').RemGroup('PlusCoverage')
            Gui.activateWorkbench('PartDesignWorkbench')
            Gui.removeWorkbench('PlusCoverageWorkbench')

    def test_live_customization_refresh(self):
        window = Gui.getMainWindow()
        Gui.Command.get('Std_DlgCustomize').getAction()[0].trigger()
        settle()
        dialog = next(w for w in window.findChildren(QtWidgets.QDialog)
                      if w.inherits('Gui::Dialog::DlgCustomizeImp'))
        self.assertTrue(dialog.property('FreeCADPlusObserved'))
        custom = App.ParamGet('User parameter:BaseApp/Workbench/PartDesignWorkbench/Toolbar/PlusLiveCoverage')
        custom.SetString('Name', 'Coverage live')
        custom.SetString('Std_ViewFront', 'FreeCADGui')
        native = window.addToolBar('Coverage live')
        native.setObjectName('Coverage live')
        Gui.Command.get('Std_ViewFront').addToToolbar(native)
        native.show()
        settle()
        try:
            self.tab('All Tools')
            # Exercise dialog-close refresh after a further native customization.
            custom.SetString('Std_ViewRear', 'FreeCADGui')
            Gui.Command.get('Std_ViewRear').addToToolbar(native)
            dialog.close()
            settle()
            group = self.ribbon.scroll.widget().findChild(QtWidgets.QWidget, 'PlusGroup_Coverage live')
            self.assertIsNotNone(group)
            self.assertTrue(group.findChild(QtWidgets.QToolButton, 'Plus_Std_ViewRear'))
            self.assertTrue(native.isHidden())
            self.prefs.SetInt('ToolbarUIMode', 1)
            ui_modes.apply_modes()
            self.assertTrue(native.isVisible())
            self.assertEqual(len(native.actions()), 2)
        finally:
            App.ParamGet('User parameter:BaseApp/Workbench/PartDesignWorkbench/Toolbar').RemGroup('PlusLiveCoverage')
            window.removeToolBar(native)
            native.deleteLater()
            settle()

    def test_plus_group_last_choice_and_native_state(self):
        r = self.ribbon
        button = r.scroll.widget().findChild(QtWidgets.QToolButton, 'Plus_PartDesign_Pad')
        actions = button.menu().actions()
        self.assertEqual(actions, [Gui.Command.get(c).getAction()[0]
                                  for c in ('PartDesign_Pad', 'PartDesign_Pocket')])
        # Emit only the menu selection notification: native commands require a profile.
        # Actual native command dispatch is covered by the Sketcher mouse test.
        button.menu().triggered.emit(actions[1])
        self.assertEqual(button.defaultAction(), actions[1])
        self.tab('Home')
        self.tab('Modeling')
        button = r.scroll.widget().findChild(QtWidgets.QToolButton, 'Plus_PartDesign_Pad')
        self.assertEqual(button.defaultAction(), actions[1])
        self.assertEqual(button.isEnabled(), actions[1].isEnabled())
        self.assertEqual(button.icon().cacheKey(), actions[1].icon().cacheKey())
        toolbars.preferences().SetString('PartDesign_Pad', 'PartDesign_Pad')


def prepare_fresh_process():
    """Save an isolated profile through the normal shutdown path."""
    prefs = App.ParamGet('User parameter:BaseApp/Preferences/General')
    prefs.SetString('AutoloadModule', 'PartDesignWorkbench')
    prefs.SetInt('ToolbarUIMode', 1)
    Gui.activateWorkbench('PartDesignWorkbench')
    ui_modes.apply_modes()
    bars = {b.objectName(): b for b in toolbars._controller.native_bars()}
    bars['File'].hide()
    bars['Edit'].show()
    prefs.SetInt('ToolbarUIMode', 0)
    ui_modes.apply_modes()
    toolbars.preferences().SetString('PartDesign_Pad', 'PartDesign_Pocket')
    selection_toolbar.preferences().SetBool('Directional', False)
    selection_toolbar.preferences().SetBool('Persistent', False)
    selection_toolbar.preferences().SetString('CurveIntent', 'Tangent Curves')
    category_selection.preferences().SetBool('Faces', False)
    App.saveParameter()


def verify_fresh_process():
    """Verify independent restart, saved Plus choice and Classic visibility."""
    Gui.activateWorkbench('PartDesignWorkbench')
    ui_modes.apply_modes()
    settle()
    r = toolbars._controller
    assert r.bar.isVisible()
    assert r.common.findChild(QtWidgets.QToolButton, 'PlusCurveIntent').text() == 'Tangent Curves'
    assert curve_selection.intent() == 'Tangent Curves'
    categories = r.common.findChild(QtWidgets.QToolButton, 'PlusSelectionCategories')
    assert categories is not None
    assert not next(a for a in categories.menu().actions() if a.text() == 'Faces').isChecked()
    assert category_selection._controller.active
    directional = r.common.findChild(QtWidgets.QToolButton, 'PlusDirectionalSelection')
    assert directional is not None and not directional.isChecked()
    assert Gui.getMainWindow().property('FreeCADPlusDirectionalSelection') is False
    persistent = r.common.findChild(QtWidgets.QToolButton, 'PlusPersistentSelection')
    assert persistent is not None and not persistent.isChecked()
    assert Gui.getMainWindow().property('FreeCADPlusPersistentSelection') is False
    assert all(b.isHidden() for b in r.native_bars())
    button = r.scroll.widget().findChild(QtWidgets.QToolButton, 'Plus_PartDesign_Pad')
    assert button.defaultAction() == Gui.Command.get('PartDesign_Pocket').getAction()[0]
    App.ParamGet('User parameter:BaseApp/Preferences/General').SetInt('ToolbarUIMode', 1)
    ui_modes.apply_modes()
    settle()
    assert r.native['File'].isHidden()
    assert r.native['Edit'].isVisible()
    assert r.bar.isHidden()

# The nineteen workbenches registered by the retained official 1.1.4 baseline.
# NoneWorkbench is its additional empty workbench; optional unregistered examples
# such as MeshPart/Import are not silently enabled or removed by Plus.
CLASSIC_WORKBENCHES = (
    'AssemblyWorkbench', 'BIMWorkbench', 'CAMWorkbench', 'DraftWorkbench',
    'FemWorkbench', 'InspectionWorkbench', 'MaterialWorkbench', 'MeshWorkbench',
    'OpenSCADWorkbench', 'PartDesignWorkbench', 'PartWorkbench', 'PointsWorkbench',
    'ReverseEngineeringWorkbench', 'RobotWorkbench', 'SketcherWorkbench',
    'SpreadsheetWorkbench', 'SurfaceWorkbench', 'TechDrawWorkbench', 'TestWorkbench',
    'NoneWorkbench',
)


def audit_workbench(workbench):
    """Compare Plus's realized controls to the current native toolbar inventory."""
    Gui.activateWorkbench(workbench)
    assert Gui.activeWorkbench().name() == workbench, (workbench, 'Native activation failed')
    ui_modes.apply_modes()
    settle()
    r = toolbars._controller
    index = next(i for i in range(r.tabbar.count()) if r.tabbar.tabText(i) == 'All Tools')
    r.tabbar.setCurrentIndex(index)
    settle()
    items = Gui.activeWorkbench().getToolbarItems()
    commands = set(Gui.listCommands())
    represented = set()
    placeholders = set()
    actual_actions = set()
    groups = r.scroll.widget().findChildren(QtWidgets.QWidget)
    for widget in groups:
        represented.update(widget.property('PlusCommands') or ())
        placeholders.update(widget.property('PlusUnavailable') or ())
        actual_actions.update(widget.actions())
        if isinstance(widget, QtWidgets.QToolButton) and widget.menu():
            actual_actions.update(widget.menu().actions())
    expected = {c for cmds in items.values() for c in cmds if c != 'Separator' and c in commands}
    missing = expected - represented
    assert not missing, (workbench, 'Missing native command controls', sorted(missing))
    assert not expected.intersection(placeholders), (workbench, 'Native commands replaced with placeholders')
    group_names = [w.objectName() for w in groups if w.objectName().startswith('PlusGroup_')]
    assert len(group_names) == len(items), (workbench, 'Toolbar group count differs')
    native_action_count = 0
    for name in items:
        bar = r.native.get(name)
        assert bar is not None, (workbench, 'Missing Classic toolbar', name)
        for action in bar.actions():
            if action.isSeparator():
                continue
            if isinstance(action, QtWidgets.QWidgetAction):
                original = bar.widgetForAction(action)
                command = action.data()
                identity = command or 'Widget_' + original.objectName()
                control = r.scroll.widget().findChild(QtWidgets.QToolBar, 'PlusControl_' + identity)
                assert control is not None, (workbench, name, 'Missing widget factory', identity)
                copies = [control.widgetForAction(a) for a in control.actions()]
                assert any(w is not None and w != original and
                           w.metaObject().className() == original.metaObject().className()
                           for w in copies), (workbench, name, 'Widget class differs')
            else:
                assert action in actual_actions, (workbench, name, action.objectName(), action.text())
                native_action_count += 1
    routed = {wb for _, wb in r.tabs if wb}
    routed.update(r.selector.itemData(i)[1] for i in range(r.selector.count()))
    routed.update(wb for _, wb in toolbars.layout.DESIGN_TABS if wb)
    assert set(Gui.listWorkbenches()) <= routed, (workbench, 'Omitted workbench route')
    # Every group remains reachable using the horizontal scrollbar on narrow screens.
    scroll = r.scroll.horizontalScrollBar()
    scroll.setValue(scroll.maximum())
    QtTest.QTest.qWait(50)
    if workbench in ('CAMWorkbench', 'FemWorkbench', 'DraftWorkbench', 'AssemblyWorkbench', 'TechDrawWorkbench'):
        r.host.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/(workbench+'-all-tools-end.png')))
        scroll.setValue(0)
        QtTest.QTest.qWait(50)
        r.host.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/(workbench+'-all-tools.png')))
    preserved = [(b, b.parentWidget(), b.actions(), b.property('FreeCADPlusClassicVisible'))
                 for b in r.native_bars()]
    prefs = App.ParamGet('User parameter:BaseApp/Preferences/General')
    prefs.SetInt('ToolbarUIMode', 1)
    ui_modes.apply_modes()
    settle()
    for bar, parent, actions, visible in preserved:
        assert bar.parentWidget() == parent and bar.actions() == actions, (workbench, 'Classic ownership changed')
        assert bar.isVisible() == visible, (workbench, bar.objectName(), 'Classic visibility differs')
    prefs.SetInt('ToolbarUIMode', 0)
    ui_modes.apply_modes()
    settle()
    assert all(b.isHidden() for b in r.native_bars()), (workbench, 'Classic/Plus overlap')
    return dict(workbench=workbench, toolbars=len(items), commands=len(expected),
                native_actions=native_action_count, unavailable_in_classic=sorted(placeholders),
                toolbar_names=list(items))
