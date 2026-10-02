# SPDX-License-Identifier: LGPL-2.1-or-later
"""Three feedback workflows for editing shared components across file boundaries."""
import hashlib
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
import ComponentModel as Model
from PySide import QtCore, QtWidgets
from freecad.gui import ComponentNavigator as Navigator
from freecad.gui import ComponentSelection as Selection
from freecad.gui.ComponentExtrudeTask import active_component


class TestComponentEditContext(unittest.TestCase):
    def setUp(self):
        source = Path(os.environ["FREECAD_PLUS_SOURCE"])
        self.assertEqual(hashlib.sha256(Path(Navigator.__file__).read_bytes()).digest(),
                         hashlib.sha256((source / "src/Gui/ComponentNavigator.py").read_bytes()).digest())
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / self._testMethodName
        self.output.mkdir()
        self.external = Model.new_document("Support")
        self.part = Model.metadata(self.external).RootComponent
        self.body = self.box(self.part, "SupportBody")
        self.child = Model.add_component(self.part, label="Pin")
        self.pin = self.child.LinkedObject
        self.pin_body = self.box(self.pin, "PinBody")
        self.external.saveAs(str(self.output / "Support.cadprt"))
        self.doc = Model.new_document("Assembly")
        self.root = Model.metadata(self.doc).RootComponent
        self.doc.saveAs(str(self.output / "Assembly.cadprt"))
        self.first = Model.add_component(self.root, self.part)
        self.second = Model.add_component(self.root, self.part,
            placement=App.Placement(App.Vector(30, 5, 0), App.Rotation()))
        self.doc.save()
        self.panel = Navigator.show(self.doc)
        self.window = self.panel.mdi.activeSubWindow()
        Gui.Selection.clearSelection()
        self.panel.refresh()
        group = self.panel.structure.topLevelItem(0)
        self.assertEqual(group.childCount(), 0, "A new document must start with grouped instances")
        self.panel.toggle_instances(group)
        self.panel.refresh()

    def box(self, component, name):
        with Model.transaction(component.Document, "Create body"):
            obj = component.Document.addObject("Part::Feature", name)
            Model.register_object(component, obj, "Object", True)
            obj.Shape = Part.makeBox(2, 3, 4)
        return obj

    def tearDown(self):
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        Gui.updateGui()

    def row(self, ids):
        iterator = QtWidgets.QTreeWidgetItemIterator(self.panel.structure)
        while iterator.value():
            item = iterator.value()
            value = item.data(0, QtCore.Qt.UserRole)
            if value and list(value[1]) == ids:
                return item
            iterator += 1
        self.fail("Missing occurrence path: " + repr(ids))

    def activate(self, ids):
        self.panel.activate_item(self.row(ids))
        self.panel.refresh()

    def assert_context(self, root, component, ids):
        self.assertEqual(self.panel.root_key, Navigator.object_key(root))
        self.assertEqual(self.panel.active_key, Navigator.object_key(component))
        self.assertEqual(self.panel.active_path, ids)
        native = Gui.getDocument(root.Document.Name).activeView().getActiveObject("part", False)
        self.assertEqual(native, (component, root, Selection.native_path(root, ids)))
        self.assertEqual(active_component(), component)

    def testExternalEditKeepsAssemblyAndExactInstance(self):
        ids = [self.second.ObjectId]
        self.activate(ids)
        self.assertEqual(App.ActiveDocument, self.doc)
        self.assertEqual(self.panel.mdi.activeSubWindow(), self.window)
        self.assert_context(self.root, self.part, ids)
        self.assertEqual(self.panel.history.topLevelItem(1).text(2), self.body.Label)
        item = self.panel.history.topLevelItem(1)
        item.setSelected(True)
        selection = Gui.Selection.getSelectionEx("*", 0)
        self.assertEqual(selection[0].Object, self.root)
        self.assertEqual(list(selection[0].SubElementNames),
                         [Selection.native_path(self.root, ids, self.body)])
        self.activate([self.first.ObjectId])
        self.assert_context(self.root, self.part, [self.first.ObjectId])
        self.assertEqual(self.external.FileName, str(self.output / "Support.cadprt"))
        self.capture("external-edit-context.png")

    def testCopyUndoRedoAndMissingActiveOccurrence(self):
        ids = [self.second.ObjectId]
        self.activate(ids)
        copied = Model.make_independent(self.second)
        self.panel.refresh()
        self.assert_context(self.root, copied, ids)
        self.doc.undo()
        self.panel.refresh()
        self.assert_context(self.root, self.part, ids)
        self.doc.redo()
        self.panel.refresh()
        self.assert_context(self.root, self.second.LinkedObject, ids)
        with Model.transaction(self.doc, "Unresolve active instance"):
            self.second.setLink(None)
        self.panel.refresh()
        self.assert_context(self.root, self.root, [])
        self.assertEqual(self.panel.context.text(), "Editing: Assembly")
        self.doc.undo()
        self.panel.refresh()
        self.activate(ids)
        self.assert_context(self.root, self.second.LinkedObject, ids)

    def testIsolatedTabsRestoreNestedContextAndOwningFileTitle(self):
        ids = [self.second.ObjectId, self.child.ObjectId]
        self.activate(ids)
        self.assert_context(self.root, self.pin, ids)
        view = self.panel.open_component_tab(Navigator.object_key(self.part))
        isolated = self.panel.mdi.activeSubWindow()
        self.panel.refresh()
        self.activate([self.child.ObjectId])
        self.assert_context(self.part, self.pin, [self.child.ObjectId])
        self.panel.mdi.setActiveSubWindow(self.window)
        Gui.updateGui()
        self.assert_context(self.root, self.pin, ids)
        self.assertEqual(App.ActiveDocument, self.doc)
        self.panel.mdi.setActiveSubWindow(isolated)
        Gui.updateGui()
        self.assert_context(self.part, self.pin, [self.child.ObjectId])
        self.assertEqual(App.ActiveDocument, self.external)
        with Model.transaction(self.external, "Rename component"):
            self.part.Label = "Renamed support"
        saved = self.output / "Renamed-Support.cadprt"
        self.external.saveAs(str(saved))
        self.panel.refresh()
        self.assertEqual(isolated.windowTitle(), "Renamed support \u2014 " + str(saved))
        self.assertEqual(self.panel.open_component_tab(Navigator.object_key(self.part)), view)
        self.assertEqual(self.doc.FileName, str(self.output / "Assembly.cadprt"))
        self.doc.save()
        self.capture("isolated-nested-context.png")

    def capture(self, filename):
        self.panel.setFloating(True)
        self.panel.resize(850, 650)
        Gui.updateGui()
        self.panel.grab().save(str(self.output / filename))
