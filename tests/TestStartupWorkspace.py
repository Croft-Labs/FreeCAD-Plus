# SPDX-License-Identifier: LGPL-2.1-or-later
"""Real cold-start acceptance; run successive phases with one isolated profile."""
import os
import json
import hashlib
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui import ComponentNavigator as Navigator, PlusRibbon


class TestStartupWorkspace(unittest.TestCase):
    def testColdStartupAndSavedWorkspace(self):
        window = Gui.getMainWindow()
        phase = os.environ['FREECAD_PLUS_STARTUP_PHASE']
        # Command-line macros enter native MRU during delayedStartup; allow its
        # queued model-reset visibility update to complete before inspecting it.
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(300, loop.quit)
        loop.exec()
        self.assertTrue(window.isVisible())
        self.assertIsNone(App.ActiveDocument)
        self.assertTrue(PlusRibbon._ribbon.enabled)
        self.assertTrue(Navigator._startup_layout.applied)
        home = Path(App.ConfigGet('AppHomePath')).resolve()
        source = Path(os.environ['FREECAD_PLUS_SOURCE'])
        for name in ('PlusDefaults.py', 'PlusRibbon.py', 'ComponentNavigator.py',
                     'DesignLayersGui.py', 'DesignSelectionToolbar.py'):
            installed = home/'Ext/freecad/gui'/name
            self.assertEqual(hashlib.sha256(installed.read_bytes()).digest(),
                             hashlib.sha256((source/'src/Gui'/name).read_bytes()).digest(), name)
        tasks = window.findChild(QtWidgets.QDockWidget, 'Tasks')
        panel = window.findChild(QtWidgets.QDockWidget, 'ComponentNavigator')
        attributes = window.findChild(QtWidgets.QDockWidget, 'Model')
        ribbon = PlusRibbon._ribbon
        Path(os.environ['FREECAD_PLUS_VALIDATION_DIR'],'docks.json').write_text(json.dumps({'docks': [{'name':d.objectName(),'parent':d.parentWidget().objectName() if d.parentWidget() else None,'area':window.dockWidgetArea(d).value,'floating':d.isFloating(),'visible':d.isVisibleTo(window)} for d in window.findChildren(QtWidgets.QDockWidget)], 'overlay':App.ParamGet('User parameter:BaseApp/Preferences/DockWindows').GetBool('ActivateOverlay'), 'saved':Navigator._startup_layout.saved_state},indent=2))
        if phase == 'Restore':
            self.assertEqual(window.dockWidgetArea(tasks), QtCore.Qt.LeftDockWidgetArea)
            self.assertEqual(window.dockWidgetArea(panel), QtCore.Qt.RightDockWidgetArea)
            self.assertTrue(attributes.isFloating())
            self.assertEqual(window.toolBarArea(ribbon.common), QtCore.Qt.BottomToolBarArea)
            self.assertEqual(window.toolBarArea(ribbon.selection_toolbar), QtCore.Qt.LeftToolBarArea)
            self.assertEqual(window.toolBarArea(ribbon.layers_toolbar), QtCore.Qt.BottomToolBarArea)
            self.assertFalse(App.ParamGet('User parameter:BaseApp/Preferences/DockWindows').GetBool('ActivateOverlay'))
            ribbon.apply()
            window.hide()
            window.show()
            self.assertEqual(window.dockWidgetArea(panel), QtCore.Qt.RightDockWidgetArea)
            self.assertEqual(window.toolBarArea(ribbon.common), QtCore.Qt.BottomToolBarArea)
        else:
            self.assertEqual(window.dockWidgetArea(tasks), QtCore.Qt.RightDockWidgetArea)
            self.assertFalse(tasks.isFloating())
            self.assertTrue(tasks.isVisibleTo(window))
        panes = [p for p in window.findChildren(QtWidgets.QWidget, 'ComponentStartActions')
                 if p.isVisibleTo(window)]
        self.assertTrue(panes, 'Startup file actions must be visible without an overlay command')
        for name in ('Std_New', 'Std_Open'):
            button = panes[0].findChild(QtWidgets.QToolButton, name)
            self.assertIsNotNone(button)
            self.assertTrue(button.isVisibleTo(window))
        view = window.findChild(QtWidgets.QWidget, 'StartView')
        self.assertIsNotNone(view, 'Cold startup must create the native recent-files view')
        self.assertTrue(view.isVisibleTo(window))
        self.assertTrue(view.property('PlusRecentFilesOnly'))
        cards = next(c for c in view.findChildren(QtWidgets.QListView)
                     if c.model() and c.model().metaObject().className() == 'Start::RecentFilesModel')
        self.assertEqual(view.findChild(QtWidgets.QLabel, 'RecentFilesEmpty').isVisibleTo(view),
                         cards.model().rowCount() == 0)
        self.assertEqual(cards.isVisibleTo(view), cards.model().rowCount() > 0)
        if phase == 'Customize':
            window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, tasks)
            window.addDockWidget(QtCore.Qt.RightDockWidgetArea, panel)
            attributes.setFloating(True)
            window.addToolBar(QtCore.Qt.BottomToolBarArea, ribbon.common)
            window.addToolBar(QtCore.Qt.LeftToolBarArea, ribbon.selection_toolbar)
            window.addToolBar(QtCore.Qt.BottomToolBarArea, ribbon.layers_toolbar)
            ribbon.apply()
            self.assertEqual(window.dockWidgetArea(panel), QtCore.Qt.RightDockWidgetArea)
            self.assertEqual(window.toolBarArea(ribbon.common), QtCore.Qt.BottomToolBarArea)
        window.grab().save(str(Path(os.environ['FREECAD_PLUS_VALIDATION_DIR'])/'startup.png'))
        App.saveParameter()
