# SPDX-License-Identifier: LGPL-2.1-or-later
"""Three feedback workflows for native Save routing through component ownership."""
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
import CadDocument
import ComponentModel as Model
from PySide import QtCore, QtWidgets
from freecad.gui import ComponentNavigator as Navigator
from freecad.gui import ComponentSelection as Selection


class TestComponentSaveRouting(unittest.TestCase):
    def setUp(self):
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / self._testMethodName
        self.output.mkdir()
        App.ParamGet("User parameter:BaseApp/Preferences/Dialog").SetBool("DontUseNativeDialog", True)
        self.external = Model.new_document("Support")
        self.part = Model.metadata(self.external).RootComponent
        self.body = self.external.addObject("Part::Feature", "SupportBody")
        Model.register_object(self.part, self.body, "Object", True)
        self.body.Shape = Part.makeBox(2, 3, 4)
        self.external.recompute()
        self.source_path = self.output / "Support.cadprt"
        self.external.saveAs(str(self.source_path))
        self.doc = Model.new_document("Assembly")
        self.root = Model.metadata(self.doc).RootComponent
        self.parent_path = self.output / "Assembly.cadprt"
        self.doc.saveAs(str(self.parent_path))
        self.first = Model.add_component(self.root, self.part)
        self.second = Model.add_component(self.root, self.part,
            placement=App.Placement(App.Vector(30, 5, 0), App.Rotation()))
        self.doc.save()
        self.parent_bytes = self.parent_path.read_bytes()
        self.panel = Navigator.show(self.doc)
        self.window = self.panel.mdi.activeSubWindow()
        group = self.panel.structure.topLevelItem(0).child(0)
        self.panel.toggle_instances(group)
        self.panel.refresh()
        self.panel.activate_item(self.panel.structure.topLevelItem(0).child(0).child(1))
        self.panel.refresh()
        self.path = [self.second.ObjectId]

    def tearDown(self):
        for doc in reversed(list(App.listDocuments().values())):
            App.closeDocument(doc.Name)
        Gui.updateGui()

    def assert_context(self):
        self.assertEqual(App.ActiveDocument, self.doc)
        self.assertEqual(self.panel.mdi.activeSubWindow(), self.window)
        self.assertEqual(self.panel.active_path, self.path)
        self.assertEqual(Gui.activeDocument().activeView().getActiveObject("part", False),
                         (self.part, self.root, Selection.native_path(self.root, self.path)))

    def file_command(self, command, path=None, caption="Save owning file:"):
        observed, errors = [], []
        attempts = [0]
        timer = QtCore.QTimer()
        timer.setInterval(30)
        def choose():
            attempts[0] += 1
            dialog = QtWidgets.QApplication.activeModalWidget()
            if isinstance(dialog, QtWidgets.QFileDialog):
                timer.stop()
                observed.append((dialog.windowTitle(), dialog.nameFilters()))
                dialog.setAttribute(QtCore.Qt.WA_DontShowOnScreen, True)
                if path:
                    dialog.selectFile(str(path))
                    dialog.accept()
                else:
                    dialog.reject()
            elif dialog:
                timer.stop()
                errors.append(dialog.windowTitle())
                dialog.reject()
            elif attempts[0] > 100:
                timer.stop()
        timer.timeout.connect(choose)
        timer.start()
        try:
            Gui.runCommand(command)
        finally:
            timer.stop()
        self.assertFalse(errors, errors)
        self.assertEqual(len(observed), 1)
        self.assertTrue(observed[0][0].startswith(caption), observed)
        self.assertTrue(any("*.cadprt" in value for value in observed[0][1]))

    def testSaveExternalOwnerLeavesDirtyParentUntouched(self):
        before = self.source_path.read_bytes()
        with Model.transaction(self.external, "Edit support"):
            self.body.Shape = Part.makeBox(5, 3, 4)
        with Model.transaction(self.doc, "Edit parent"):
            self.root.Label = "Unsaved parent change"
        Gui.runCommand("Std_Save")
        self.assertNotEqual(self.source_path.read_bytes(), before)
        self.assertEqual(self.parent_path.read_bytes(), self.parent_bytes)
        self.assertEqual(CadDocument.preflight(self.source_path)["document"], Model.metadata(self.external).ObjectId)
        self.assert_context()
        # Cold reopen confirms which file actually received the geometry change.
        for doc in reversed(list(App.listDocuments().values())):
            App.closeDocument(doc.Name)
        reopened = CadDocument.open(self.parent_path)
        root = Model.metadata(reopened).RootComponent
        self.assertEqual(root.Label, "Assembly")
        linked = Model.children(root)[0].LinkedObject
        self.assertAlmostEqual(Model.history(linked)[0].Shape.Volume, 60)

    def testExternalSaveCopyCancelAndSaveAsPreserveContext(self):
        original = self.source_path.read_bytes()
        identity = Model.metadata(self.external).ObjectId
        self.file_command("Std_SaveAs")
        self.assert_context()
        self.assertEqual(self.source_path.read_bytes(), original)
        with Model.transaction(self.external, "Edit support"):
            self.body.Shape = Part.makeBox(6, 3, 4)
        copied = self.output / "Support-Copy.cadprt"
        self.file_command("Std_SaveCopy", copied, "Save a copy of owning file:")
        self.assertEqual(CadDocument.preflight(copied)["document"], identity)
        self.assertEqual(Path(self.external.FileName), self.source_path)
        self.assertEqual(self.source_path.read_bytes(), original)
        self.assert_context()
        renamed = self.output / "Support-Renamed.cadprt"
        self.file_command("Std_SaveAs", renamed)
        self.assertEqual(CadDocument.preflight(renamed)["document"], identity)
        self.assertEqual(Path(self.external.FileName), renamed)
        self.assertEqual(self.first.LinkedObject, self.second.LinkedObject)
        self.assertEqual(self.parent_path.read_bytes(), self.parent_bytes)
        self.assert_context()
        self.panel.edit_model(self.panel.models.topLevelItem(0))
        Gui.runCommand("Std_Save")
        self.assertIn("Support-Renamed.cadprt", CadDocument.preflight(self.parent_path)["dependencies"].values())

    def testEmbeddedIsolatedFirstSaveOwnsWholeDocument(self):
        doc = Model.new_document("Embedded owner")
        root = Model.metadata(doc).RootComponent
        link = Model.add_component(root, label="Embedded pin")
        panel = Navigator.show(doc)
        view = panel.open_component_tab(Navigator.object_key(link))
        window = panel.mdi.activeSubWindow()
        identity = Model.metadata(doc).ObjectId
        destination = self.output / "Embedded-Owner.cadprt"
        self.file_command("Std_Save", destination)
        data = CadDocument.preflight(destination)
        self.assertEqual(data["document"], identity)
        self.assertEqual({item["id"] for item in data["definitions"]}, {root.ObjectId, link.LinkedObject.ObjectId})
        self.assertEqual(panel.mdi.activeSubWindow(), window)
        self.assertEqual(Gui.activeDocument().activeView(), view)
        self.assertEqual(panel.active_key, Navigator.object_key(link.LinkedObject))
        panel.refresh()
        self.assertEqual(Path(doc.FileName), destination)
        self.assertIn(doc.FileName, window.windowTitle())
        panel.setFloating(True)
        panel.resize(850, 650)
        Gui.updateGui()
        panel.grab().save(str(self.output / "saved-embedded-component.png"))
