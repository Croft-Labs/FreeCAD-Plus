# SPDX-License-Identifier: LGPL-2.1-or-later
"""Cold-process checks using installed modules and the standard GUI commands."""
import hashlib
import json
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import ComponentModel as Model
import CadDocument
from freecad.gui import ComponentNavigator


class TestInstalledComponentDocument(unittest.TestCase):
    def setUp(self):
        # Correlate native Qt diagnostics with the cold workflow that emitted them.
        os.write(2, ("Cold GUI check: " + self._testMethodName + "\n").encode())

    def tearDown(self):
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def testInstalledModulesMatchCheckout(self):
        source = Path(os.environ["FREECAD_PLUS_SOURCE"])
        pairs = [(Model, "src/Mod/Part/ComponentModel.py"),
                 (CadDocument, "src/Mod/Part/CadDocument.py"),
                 (ComponentNavigator, "src/Gui/ComponentNavigator.py")]
        identities = []
        for module, relative in pairs:
            installed = Path(module.__file__)
            self.assertNotEqual(installed.resolve(), (source / relative).resolve())
            digest = hashlib.sha256(installed.read_bytes()).hexdigest()
            self.assertEqual(digest, hashlib.sha256((source / relative).read_bytes()).hexdigest())
            identities.append({"source": relative, "installed": str(installed), "sha256": digest})
        (Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "installed-identities.json").write_text(
            json.dumps(identities, indent=2), encoding="utf-8")

    def testStandardNewCreatesRootComponent(self):
        Gui.runCommand("Std_New")
        doc = App.ActiveDocument
        root = Model.metadata(doc).RootComponent
        self.assertTrue(Model.is_component(root))
        panel = ComponentNavigator.show(doc)
        self.assertEqual(panel.structure.topLevelItemCount(), 1)
        self.assertEqual(panel.structure.topLevelItem(0).text(0), root.Label)
        self.assertEqual(Gui.activeDocument().activeView().getActiveObject("part"), root)

    def testCameraCommandsAcrossClosingAndNewViews(self):
        doc = Model.new_document("Camera lifecycle")
        Gui.updateGui()
        commands = [Gui.Command.get(name) for name in
                    ("Std_OrthographicCamera", "Std_PerspectiveCamera")]
        for command in commands:
            command.getAction()
            self.assertTrue(command.isActive())
        App.closeDocument(doc.Name)
        # Query before the closed Qt window has finished deferred destruction.
        Gui.Command.update()
        self.assertTrue(all(not command.isActive() for command in commands))
        for name in ("Std_Save", "Std_Undo", "Std_Redo"):
            command = Gui.Command.get(name)
            command.getAction()
            self.assertFalse(command.isActive(), name + " must not query a detached view")
        doc = Model.new_document("Restored camera")
        Gui.updateGui()
        self.assertTrue(all(command.isActive() for command in commands))
        Gui.runCommand("Std_PerspectiveCamera", 1)
        self.assertIn("PerspectiveCamera", Gui.activeDocument().activeView().getCamera())
        Gui.runCommand("Std_OrthographicCamera", 1)
        self.assertIn("OrthographicCamera", Gui.activeDocument().activeView().getCamera())

    def testStandardOpenConvertsLegacyWithoutChangingOriginal(self):
        doc = App.newDocument("LegacyGui")
        box = doc.addObject("Part::Box", "Box")
        doc.recompute()
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "Original.FCStd"
        doc.saveAs(str(path))
        before = path.read_bytes()
        App.closeDocument(doc.Name)
        from PySide import QtCore, QtWidgets
        App.ParamGet("User parameter:BaseApp/Preferences/Dialog").SetBool("DontUseNativeDialog", True)
        handled = []
        attempts = [0]
        def choose_file():
            attempts[0] += 1
            dialog = QtWidgets.QApplication.activeModalWidget()
            if isinstance(dialog, QtWidgets.QFileDialog):
                dialog.setAttribute(QtCore.Qt.WA_DontShowOnScreen, True)
                dialog.selectFile(str(path))
                handled.append(True)
                dialog.accept()
            elif attempts[0] < 100:
                QtCore.QTimer.singleShot(50, choose_file)
            elif dialog:
                dialog.reject()
        QtCore.QTimer.singleShot(50, choose_file)
        Gui.runCommand("Std_Open")
        self.assertTrue(handled, "The standard Open dialog must be exercised")
        converted = App.ActiveDocument
        self.assertTrue(Model.is_component(Model.metadata(converted).RootComponent))
        self.assertEqual(converted.FileName, "")
        self.assertEqual(path.read_bytes(), before)

    def testStandardSaveAsAndCopyUseComponentFormat(self):
        from PySide import QtCore, QtWidgets
        doc = App.newDocument("LegacyNameCollision")
        doc.addObject("Part::Box", "ComponentDocument")
        doc.recompute()
        self.assertFalse(ComponentNavigator.Command().IsActive())
        CadDocument.convert_legacy(doc)
        self.assertNotEqual(Model.metadata(doc).Name, "ComponentDocument")
        self.assertTrue(ComponentNavigator.Command().IsActive())
        identity = Model.metadata(doc).ObjectId
        output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        App.ParamGet("User parameter:BaseApp/Preferences/Dialog").SetBool("DontUseNativeDialog", True)
        for command, path in [("Std_SaveAs", output / "StandardSave.cadprt"),
                              ("Std_SaveCopy", output / "StandardCopy.cadprt")]:
            filters = []
            attempts = [0]
            def choose_file():
                attempts[0] += 1
                dialog = QtWidgets.QApplication.activeModalWidget()
                if isinstance(dialog, QtWidgets.QFileDialog):
                    filters.extend(dialog.nameFilters())
                    dialog.setAttribute(QtCore.Qt.WA_DontShowOnScreen, True)
                    dialog.selectFile(str(path))
                    dialog.accept()
                elif attempts[0] < 100:
                    QtCore.QTimer.singleShot(50, choose_file)
                elif dialog:
                    dialog.reject()
            QtCore.QTimer.singleShot(50, choose_file)
            Gui.runCommand(command)
            self.assertTrue(any("*.cadprt" in value for value in filters))
            self.assertTrue(path.exists())
            self.assertEqual(CadDocument.preflight(path)["document"], identity)
        self.assertEqual(Path(doc.FileName), output / "StandardSave.cadprt")

    def testColdExternalRoundTrip(self):
        fixture = Path(os.environ["FREECAD_PLUS_COMPONENT_FIXTURES"]) / "ExternalParent.cadprt"
        doc = CadDocument.open(fixture)
        root = Model.metadata(doc).RootComponent
        reference = next(o for o in doc.Objects if getattr(o, "ComponentRole", "") == "Reference")
        self.assertAlmostEqual(Model.current_shape(reference).Volume, 60)
        self.assertNotEqual(reference.SourceObject.Document, doc)
        panel = ComponentNavigator.show(doc)
        self.assertEqual(panel.structure.topLevelItem(0).text(0), root.Label)
        from PySide import QtCore
        self.assertEqual([panel.tabs.tabText(i) for i in range(panel.tabs.count())],
                         ["Models", "Part Tree", "History"])
        counts = Model.instance_counts(root)
        expected = set(Model.definitions(doc)) | set(counts)
        actual = {}
        for index in range(panel.models.topLevelItemCount()):
            row = panel.models.topLevelItem(index)
            self.assertEqual(row.childCount(), 0)
            component = ComponentNavigator.resolve(row.data(0, QtCore.Qt.UserRole))
            actual[component] = int(row.text(1))
        self.assertEqual(actual, {component: counts.get(component, 0) for component in expected})
        root_row = panel.structure.topLevelItem(0)
        self.assertEqual(root_row.childCount(), len(Model.children(root)))
        for index in range(root_row.childCount()):
            self.assertTrue(all(ComponentNavigator.resolve(key).ComponentRole == "Occurrence"
                                for key, ids in panel.members(root_row.child(index))))
        self.assertEqual(panel.history.topLevelItem(0).text(2), "Origin")
        self.assertEqual(panel.history.topLevelItem(0).child(0).text(2), "Origin Planes")
        self.assertTrue(root.Origin.Visibility)
        self.assertFalse(any(plane.Visibility for plane in ComponentNavigator.origin_planes(root.Origin)))
        reference_row = next(panel.history.topLevelItem(index)
                             for index in range(panel.history.topLevelItemCount())
                             if panel.history.topLevelItem(index).data(0, QtCore.Qt.UserRole)
                             == ComponentNavigator.object_key(reference))
        self.assertEqual(reference_row.text(3), "Ready")
