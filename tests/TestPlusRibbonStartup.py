# SPDX-License-Identifier: LGPL-2.1-or-later
"""Three successive isolated native processes prove preference persistence."""
import json
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui import PlusRibbon as UI


def settle():
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(500, loop.quit)
    loop.exec()


class TestPlusRibbonStartup(unittest.TestCase):
    def testColdStartupStyleAndClassicVisibility(self):
        self.assertNotEqual(os.environ.get("FREECAD_PLUS_PROFILE_SOURCE"), "1")
        output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        expected_file = output.parent / "classic-bars.json"
        params = App.ParamGet(UI.PARAM)
        window = Gui.getMainWindow()
        settle()
        self.assertIsNotNone(UI._ribbon, "Startup must install the ribbon service")
        ribbon = UI._ribbon
        phase = os.environ["FREECAD_PLUS_RIBBON_PHASE"]
        if phase == "Bootstrap":
            self.assertFalse(ribbon.enabled)
            Gui.activateWorkbench("PartDesignWorkbench")
            settle()
            bars = [bar for bar in window.findChildren(QtWidgets.QToolBar)
                    if bar != ribbon.toolbar and bar.toggleViewAction().isVisible()]
            hidden = next(bar for bar in bars if bar.objectName() == "Structure")
            hidden.hide()
            App.ParamGet("User parameter:BaseApp/MainWindow/Toolbars").SetBool(hidden.objectName(), False)
            expected_file.write_text(json.dumps({bar.objectName(): not bar.isHidden() for bar in bars}), encoding="utf-8")
            params.SetString("ToolbarUIStyle", "Plus")
            UI.apply_preferences()
            self.assertTrue(ribbon.enabled)
        elif phase == "Plus":
            self.assertEqual(params.GetString("ToolbarUIStyle"), "Plus")
            self.assertTrue(ribbon.enabled, "Plus must load without explicitly applying the preference")
            self.assertFalse(ribbon.toolbar.isHidden())
            params.SetString("ToolbarUIStyle", "Classic")
            UI.apply_preferences()
            self.assertFalse(ribbon.enabled)
        else:
            self.assertEqual(params.GetString("ToolbarUIStyle"), "Classic")
            self.assertFalse(ribbon.enabled)
        if phase != "Bootstrap":
            Gui.activateWorkbench("PartDesignWorkbench")
            settle()
            bars = {bar.objectName(): not bar.isHidden() for bar in window.findChildren(QtWidgets.QToolBar)
                    if bar != ribbon.toolbar and bar.toggleViewAction().isVisible()}
            for name, visible in json.loads(expected_file.read_text(encoding="utf-8")).items():
                self.assertEqual(bars.get(name), visible, name)
        App.saveParameter()
