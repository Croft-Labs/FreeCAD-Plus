# SPDX-License-Identifier: LGPL-2.1-or-later
"""File-owned component inventory, graph guards and native persistence."""
import json
import hashlib
import importlib.util
import sys
import os
from pathlib import Path
import unittest
import zipfile

import FreeCAD as App
if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
    source = Path(__file__).resolve().parents[1]
    for name in ("ComponentModel", "CadDocument"):
        spec = importlib.util.spec_from_file_location(name, source / "src/Mod/Part" / (name + ".py"))
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
import ComponentModel as Model
import CadDocument
import Part
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from unittest.mock import patch
if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
    name = "freecad.gui.ComponentNavigator"
    installed = sys.modules.get(name)
    old_panel = getattr(installed, "_dock", None)
    if old_panel is not None:
        # Retire the installed observer before creating the source navigator.
        # Two live panes otherwise compete for selection and visibility state.
        App.removeDocumentObserver(old_panel)
        Gui.Selection.removeObserver(old_panel)
        old_panel.timer.stop()
        old_panel.selection_timer.stop()
        old_panel.deleteLater()
        installed._dock = None
        QtWidgets.QApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)
    spec = importlib.util.spec_from_file_location(name, source / "src/Gui/ComponentNavigator.py")
    # Registered native commands retain their original method globals. Reuse the
    # module namespace so they route to the same source pane as direct test calls.
    module = installed or importlib.util.module_from_spec(spec)
    module.__file__, module.__spec__, module.__loader__ = spec.origin, spec, spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    import freecad.gui
    freecad.gui.ComponentNavigator = module
Navigator = sys.modules["freecad.gui.ComponentNavigator"]


class TestComponentFileHierarchy(unittest.TestCase):
    def setUp(self):
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        source = Path(__file__).resolve().parents[1]
        for module in (Model, CadDocument):
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest(),
                             hashlib.sha256((source / "src/Mod/Part" / Path(module.__file__).name).read_bytes()).hexdigest())
        self.assembly = self.document("Assembly")
        self.hardware = self.document("Hardware")
        self.screw = Model.create_definition(self.hardware, "M3 screw")
        Model.create_definition(self.hardware, "M4 screw")
        self.hardware.save()

    def tearDown(self):
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def document(self, label):
        doc = Model.new_document(label)
        doc.saveAs(str(self.output / (label + ".cadprt")))
        return doc

    def root(self, doc):
        return Model.metadata(doc).RootComponent

    def testImportExposesUnusedDefinitionsWithoutPlacingThem(self):
        record = Model.import_file(self.assembly, self.hardware)
        self.assertEqual(Model.children(self.root(self.assembly)), [])
        self.assertEqual(Model.external_documents(self.assembly), [self.hardware])
        self.assertEqual(Model.available_definitions(self.assembly),
                         Model.definitions(self.assembly) + Model.definitions(self.hardware))
        self.assertEqual(Model.import_file(self.assembly, self.hardware), record)
        self.assertEqual(len(Model.file_imports(self.assembly)), 1)
        self.assembly.undo()
        self.assertEqual(Model.file_imports(self.assembly), [])
        self.assembly.redo()
        self.assertEqual(len(Model.file_imports(self.assembly)), 1)

    def testPlacedImportRemainsAfterLastInstanceIsDeleted(self):
        link = Model.add_component(self.root(self.assembly), self.screw)
        Model.remove_instances([link])
        self.assertIn(self.screw, Model.available_definitions(self.assembly))
        self.assertEqual(len(Model.file_imports(self.assembly)), 1)
        self.assertEqual(Model.instance_counts(self.root(self.assembly)), {})

    def testNestedImportsAndNoPlacementSurviveReopen(self):
        coatings = self.document("Coatings")
        Model.create_definition(coatings, "Zinc")
        coatings.save()
        Model.import_file(self.hardware, coatings)
        self.hardware.save()
        Model.import_file(self.assembly, self.hardware)
        self.assembly.save()
        filename = self.assembly.FileName
        ids = [Model.metadata(doc).ObjectId for doc in (self.assembly, self.hardware, coatings)]
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        assembly = CadDocument.open(filename)
        hardware = Model.external_documents(assembly)[0]
        coating = Model.external_documents(hardware)[0]
        self.assertEqual([Model.metadata(doc).ObjectId for doc in (assembly, hardware, coating)], ids)
        self.assertEqual([obj.Label for obj in Model.definitions(hardware)],
                         ["Hardware", "M3 screw", "M4 screw"])
        self.assertEqual(Model.children(self.root(assembly)), [])
        Model.validate(assembly)

    def testFileCycleAcrossUnrelatedDefinitionsIsRejectedBeforeMutation(self):
        Model.add_component(self.root(self.assembly), self.screw)
        independent = Model.create_definition(self.assembly, "Unrelated")
        before = [obj.Name for obj in self.hardware.Objects]
        with self.assertRaisesRegex(ValueError, "circular"):
            Model.add_component(self.root(self.hardware), independent)
        self.assertEqual([obj.Name for obj in self.hardware.Objects], before)
        self.assertFalse(self.hardware.HasPendingTransaction)

    def testTransitiveFileCyclesAndSelfImportAreRejected(self):
        coatings = self.document("Coatings")
        Model.import_file(self.assembly, self.hardware)
        Model.import_file(self.hardware, coatings)
        before = len(coatings.Objects)
        with self.assertRaisesRegex(ValueError, "circular"):
            Model.import_file(coatings, self.assembly)
        with self.assertRaisesRegex(ValueError, "itself"):
            Model.import_file(coatings, coatings)
        self.assertEqual(len(coatings.Objects), before)

    def testDiamondImportsShareTheSameFile(self):
        coatings = self.document("Coatings")
        Model.import_file(self.hardware, coatings)
        Model.import_file(self.assembly, self.hardware)
        Model.import_file(self.assembly, coatings)
        Model.validate(self.assembly)
        self.assertEqual(Model.external_documents(self.assembly), [self.hardware, coatings])
        self.assertEqual(Model.external_documents(self.hardware), [coatings])

    def testConflictingFileIdentitiesAcrossImportBranchesRefuseBeforeMutation(self):
        # Save Copy preserves document identity; it is not an independent component copy.
        alias_path = self.output / "HardwareAlias.cadprt"
        self.hardware.saveCopy(str(alias_path))
        alias = CadDocument.open(alias_path)
        self.assertNotEqual(alias, self.hardware)
        self.assertEqual(Model.metadata(alias).ObjectId, Model.metadata(self.hardware).ObjectId)
        first = self.document("FirstBranch")
        second = self.document("SecondBranch")
        Model.import_file(first, self.hardware)
        Model.import_file(second, alias)
        # Both direct and nested incoming aliases must fail before a transaction.
        for index, source in enumerate((alias, second)):
            with self.subTest(source=source.Label):
                target = self.document("IdentityTarget" + str(index))
                Model.import_file(target, first)
                before = [(obj.Name, getattr(obj, "ObjectId", "")) for obj in target.Objects]
                with self.assertRaisesRegex(ValueError, "same component document identity"):
                    Model.import_file(target, source)
                self.assertEqual([(obj.Name, getattr(obj, "ObjectId", ""))
                                  for obj in target.Objects], before)
                self.assertFalse(target.HasPendingTransaction)
                self.assertEqual(Model.external_documents(target), [first])
                Model.validate(target)

    def testLegacyOccurrenceOnlyFilesKeepTheirInventory(self):
        Model.add_component(self.root(self.assembly), self.screw)
        for record in Model.file_imports(self.assembly):
            self.assembly.removeObject(record.Name)
        self.assertEqual(Model.external_documents(self.assembly), [self.hardware])
        self.assembly.save()
        data = CadDocument.preflight(self.assembly.FileName)
        self.assertNotIn("component-file-imports-v1", data["required"])
        self.assertNotIn("imports", data)

    def testImportCapabilityCannotBeStripped(self):
        Model.import_file(self.assembly, self.hardware)
        self.assembly.save()
        filename = Path(self.assembly.FileName)
        with zipfile.ZipFile(filename) as archive:
            entries = {name: archive.read(name) for name in archive.namelist()}
        data = json.loads(entries[CadDocument.MANIFEST])
        data["required"].remove("component-file-imports-v1")
        entries[CadDocument.MANIFEST] = json.dumps(data).encode("utf8")
        altered = self.output / "stripped-import-capability.cadprt"
        with zipfile.ZipFile(altered, "w") as archive:
            for name, value in entries.items():
                archive.writestr(name, value)
        with self.assertRaisesRegex(ValueError, "capability"):
            CadDocument.preflight(altered)

    def testIndependentCopyAndSelectedReplacementPreservePlacement(self):
        box = self.hardware.addObject("Part::Box", "ScrewGeometry")
        Model.register_object(self.screw, box, "Object", True)
        self.hardware.recompute()
        first = Model.add_component(self.root(self.assembly), self.screw,
            placement=App.Placement(App.Vector(12, 3, 4), App.Rotation()))
        second = Model.add_component(self.root(self.assembly), self.screw)
        ident = first.ObjectId
        copy = Model.copy_definition(self.screw, self.assembly, "Domestic screw")
        self.assertNotEqual(copy.ObjectId, self.screw.ObjectId)
        self.assertEqual(first.LinkedObject, self.screw)
        Model.replace_instances(self.screw, copy, [first])
        self.assertEqual(first.LinkedObject, copy)
        self.assertEqual(first.ObjectId, ident)
        self.assertEqual(first.LinkPlacement.Base, App.Vector(12, 3, 4))
        self.assertEqual(second.LinkedObject, self.screw)
        copied_box = Model.history(copy)[0]
        copied_box.Length = 17
        self.assembly.recompute()
        self.assertNotEqual(box.Length, copied_box.Length)
        self.assembly.undo()  # Undo replacement while retaining the independent copy.
        self.assertEqual(first.LinkedObject, self.screw)
        self.assertIn(copy, Model.definitions(self.assembly))
        self.assembly.redo()
        self.assertEqual(first.LinkedObject, copy)
        self.assembly.save()
        CadDocument.preflight(self.assembly.FileName)

    def testDomesticNamesAreUniqueButExternalNamesMayMatch(self):
        domestic = Model.create_definition(self.assembly, "M3 screw")
        Model.import_file(self.assembly, self.hardware)
        self.assertEqual(Model.component_label(domestic, self.assembly), "M3 screw")
        self.assertEqual(Model.component_label(self.screw, self.assembly), "M3 screw (Hardware)")
        before = len(self.assembly.Objects)
        with self.assertRaises(ValueError):
            Model.create_definition(self.assembly, "m3 SCREW")
        self.assertEqual(len(self.assembly.Objects), before)

    def testModelsGroupsIncludeUnusedAndNestedDefinitions(self):
        coatings = self.document("Coatings")
        Model.create_definition(coatings, "Zinc")
        Model.import_file(self.hardware, coatings)
        Model.import_file(self.assembly, self.hardware)
        panel = Navigator.show(self.assembly)
        self.assertEqual(panel.models.topLevelItem(0).text(0), "Assembly")
        group = panel.models.topLevelItem(1)
        self.assertEqual(group.text(0), "Hardware")
        self.assertEqual([group.child(i).text(0) for i in range(group.childCount())],
                         ["Hardware (Hardware)", "M3 screw (Hardware)", "M4 screw (Hardware)", "Coatings"])
        self.assertEqual(group.child(3).child(1).text(0), "Zinc (Coatings)")
        group.setExpanded(True)
        panel.refresh()
        self.assertTrue(panel.models.topLevelItem(1).isExpanded())
        panel.edit_model(panel.models.topLevelItem(1))  # Headers are not definitions.
        self.assertEqual(panel.active_key, Navigator.object_key(self.root(self.assembly)))
        panel.models.topLevelItem(1).setSelected(True)
        panel.select_models()
        self.assertEqual(Gui.Selection.getSelection(), [])
        panel.tabs.setCurrentWidget(panel.models)
        panel.resize(650, 550)
        Gui.updateGui()
        panel.grab().save(str(self.output / "file-hierarchy-models.png"))

    def testHostDomesticCannotBeInsertedIntoExternalActiveComponent(self):
        host_part = Model.create_definition(self.assembly, "Host only")
        link = Model.add_component(self.root(self.assembly), self.screw)
        panel = Navigator.show(self.assembly)
        panel.activate_item(panel.structure.topLevelItem(0).child(0))
        self.assertEqual(panel.active_key, Navigator.object_key(self.screw))
        with self.assertRaisesRegex(ValueError, "defining file"):
            panel.insert_model(Navigator.object_key(host_part))
        self.assertEqual(Model.children(self.screw), [])
        coatings = self.document("Coatings")
        Model.import_file(self.hardware, coatings)
        panel.set_document(self.assembly)
        panel.activate_item(panel.structure.topLevelItem(0).child(0))
        placed = panel.insert_model(Navigator.object_key(self.root(coatings)))
        self.assertEqual(placed.Document, self.hardware)
        self.assertEqual(Model.owner(placed), self.screw)

    def testCreateInExistingFileAndCancelStorageChoice(self):
        panel = Navigator.show(self.assembly)
        with patch.object(QtWidgets.QInputDialog, "getItem", return_value=("External — existing file", True)), \
             patch.object(QtWidgets.QFileDialog, "getOpenFileName", return_value=(self.hardware.FileName, "")), \
             patch.object(QtWidgets.QInputDialog, "getText", return_value=("M5 screw", True)):
            added = panel.new_component(open_editor=False)
        self.assertEqual(added.Document, self.hardware)
        self.assertIn(added, Model.available_definitions(self.assembly))
        saved = CadDocument.preflight(self.hardware.FileName)
        self.assertIn(added.ObjectId, [item["id"] for item in saved["definitions"]])
        before = len(self.assembly.Objects)
        with patch.object(QtWidgets.QInputDialog, "getItem", return_value=("", False)):
            self.assertIsNone(panel.new_component())
        self.assertEqual(len(self.assembly.Objects), before)


    def testCopyNestedDomesticHierarchyAndExternalFileKeepsOriginal(self):
        washer = Model.create_definition(self.hardware, "Washer")
        nested = Model.add_component(self.screw, washer)
        box = self.hardware.addObject("Part::Box", "WasherShape")
        Model.register_object(washer, box, "Object", True)
        self.hardware.recompute()
        copy = Model.copy_definition(self.screw, self.assembly, "Domestic assembly")
        child = Model.children(copy)[0].LinkedObject
        self.assertNotEqual(child.ObjectId, washer.ObjectId)
        self.assertEqual(child.Document, self.assembly)
        self.assertNotEqual(Model.history(child)[0].ObjectId, box.ObjectId)
        self.assertEqual(Model.children(copy)[0].DefinitionId, child.ObjectId)
        filename = self.output / "IndependentHardware.cadprt"
        external = Model.copy_to_external_file(self.screw, filename)
        self.assertNotEqual(external.ObjectId, self.screw.ObjectId)
        self.assertIn(self.screw, Model.definitions(self.hardware))
        self.assertEqual(nested.LinkedObject, washer)
        self.assertEqual(Model.children(external)[0].LinkedObject.Document, external.Document)
        CadDocument.preflight(filename)

    def testIndependentExternalCopyRetainsExplicitExternalChildren(self):
        coatings = self.document("Coatings")
        original = Model.add_component(self.screw, self.root(coatings))
        filename = self.output / "CoatedScrew.cadprt"
        copy = Model.copy_to_external_file(self.screw, filename)
        self.assertEqual(Model.children(copy)[0].LinkedObject, original.LinkedObject)
        self.assertEqual(Model.external_documents(copy.Document), [coatings])
        self.assertNotIn(self.hardware, Model.external_documents(copy.Document))
        CadDocument.preflight(filename)

    def testMissingUnusedImportRecoversByFileIdentity(self):
        record = Model.import_file(self.assembly, self.hardware)
        self.assembly.save()
        filename = self.assembly.FileName
        sourcefile = Path(self.hardware.FileName)
        moved = sourcefile.with_name("RelocatedHardware.cadprt")
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        sourcefile.rename(moved)
        assembly = CadDocument.open(filename)
        record = Model.file_imports(assembly)[0]
        self.assertIsNone(record.Source)
        with self.assertRaises(ValueError):
            CadDocument.manifest(assembly)
        source = Model.repair_file_import(record, moved)
        self.assertEqual(Model.external_documents(assembly), [source])
        assembly.save()
        CadDocument.preflight(filename)

    def testCreateDomesticAndNewExternalFile(self):
        panel = Navigator.show(self.assembly)
        with patch.object(QtWidgets.QInputDialog, "getItem", return_value=("Domestic — current defining file", True)), \
             patch.object(QtWidgets.QInputDialog, "getText", return_value=("Domestic part", True)):
            domestic = panel.new_component(open_editor=False)
        self.assertEqual(domestic.Document, self.assembly)
        filename = str(self.output / "NewExternal.cadprt")
        with patch.object(QtWidgets.QInputDialog, "getItem", return_value=("External — new file", True)), \
             patch.object(QtWidgets.QFileDialog, "getSaveFileName", return_value=(filename, "")), \
             patch.object(QtWidgets.QInputDialog, "getText", return_value=("Domestic part", True)):
            external = panel.new_component(open_editor=False)
        self.assertNotEqual(external.Document, self.assembly)
        self.assertIn(external.Document, Model.external_documents(self.assembly))
        self.assertEqual(Model.children(self.root(self.assembly)), [])
        CadDocument.preflight(filename)

    def testExternalEditIsSeenByAnotherAssemblyAfterReopen(self):
        other = self.document("OtherAssembly")
        box = self.hardware.addObject("Part::Box", "ScrewShape")
        Model.register_object(self.screw, box, "Object", True)
        self.hardware.recompute()
        self.hardware.save()
        Model.add_component(self.root(self.assembly), self.screw)
        Model.add_component(self.root(other), self.screw)
        other.save()
        filename = other.FileName
        box.Length = 27
        self.hardware.recompute()
        self.hardware.save()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        reopened = CadDocument.open(filename)
        screw = Model.children(self.root(reopened))[0].LinkedObject
        self.assertEqual(Model.history(screw)[0].Length.Value, 27)

    def testCopyPromptDefaultsToNoReplacementAndAcceptsSelection(self):
        first = Model.add_component(self.root(self.assembly), self.screw)
        second = Model.add_component(self.root(self.assembly), self.screw)
        panel = Navigator.show(self.assembly)
        seen = []
        def accept(dialog):
            listing = dialog.findChild(QtWidgets.QListWidget)
            seen.append(listing.count())
            self.assertTrue(all(listing.item(i).checkState() == QtCore.Qt.Unchecked
                                for i in range(listing.count())))
            listing.item(0).setCheckState(QtCore.Qt.Checked)
            return QtWidgets.QDialog.Accepted
        with patch.object(QtWidgets.QInputDialog, "getText", return_value=("Domestic screw", True)), \
             patch.object(QtWidgets.QDialog, "exec", accept):
            copy = panel.copy_domestic(Navigator.object_key(self.screw))
        self.assertEqual(seen, [2])
        self.assertEqual(first.LinkedObject, copy)
        self.assertEqual(second.LinkedObject, self.screw)
        with patch.object(QtWidgets.QInputDialog, "getText", return_value=("Another copy", True)), \
             patch.object(QtWidgets.QDialog, "exec", return_value=QtWidgets.QDialog.Rejected):
            retained = panel.copy_domestic(Navigator.object_key(self.screw))
        self.assertIn(retained, Model.definitions(self.assembly))
        self.assertEqual(second.LinkedObject, self.screw)

    def testDrivenReplacementAndExpressionCopyRefuseBeforeMutation(self):
        link = Model.add_component(self.root(self.assembly), self.screw)
        copy = Model.copy_definition(self.screw, self.assembly, "Independent")
        link.Scale = 2
        with self.assertRaisesRegex(ValueError, "driven geometry"):
            Model.replace_instances(self.screw, copy, [link])
        self.assertEqual(link.LinkedObject, self.screw)
        box = self.hardware.addObject("Part::Box", "DrivenGeometry")
        Model.register_object(self.screw, box, "Object", True)
        box.setExpression("Length", "2 * 3 mm")
        before = len(self.assembly.Objects)
        with self.assertRaisesRegex(ValueError, "Expression"):
            Model.copy_definition(self.screw, self.assembly, "Refused")
        self.assertEqual(len(self.assembly.Objects), before)
        self.assertFalse(self.assembly.HasPendingTransaction)

    def testWriteColdHierarchyFixture(self):
        assembly = self.document("ColdAssembly")
        hardware = self.document("ColdHardware")
        coatings = self.document("ColdCoatings")
        other = self.document("ColdOtherAssembly")
        screw = Model.create_definition(hardware, "M3 screw")
        zinc = Model.create_definition(coatings, "Zinc")
        coatings.save()
        shape = hardware.addObject("Part::Box", "ScrewGeometry")
        shape.Length = 3
        Model.register_object(screw, shape, "Object", True)
        hardware.recompute()
        Model.import_file(hardware, coatings)
        hardware.save()
        first = Model.add_component(self.root(assembly), screw,
            placement=App.Placement(App.Vector(12, 3, 4), App.Rotation()))
        shared = Model.add_component(self.root(assembly), screw)
        Model.add_component(self.root(other), screw)
        domestic = Model.copy_definition(screw, assembly, "M3 screw")
        Model.replace_instances(screw, domestic, [first])
        shape.Length = 7
        hardware.recompute()
        hardware.save()
        assembly.recompute()
        assembly.save()
        other.save()
        expected = {"assembly": Model.metadata(assembly).ObjectId,
                    "hardware": Model.metadata(hardware).ObjectId,
                    "coatings": Model.metadata(coatings).ObjectId,
                    "screw": screw.ObjectId, "domestic": domestic.ObjectId,
                    "replaced": first.ObjectId, "shared": shared.ObjectId,
                    "zinc": zinc.ObjectId}
        (self.output / "cold-hierarchy.json").write_text(
            json.dumps(expected, indent=2), encoding="utf-8")

    def testFailedNestedOpenRestoresPreviouslyOpenDocuments(self):
        coatings = self.document("RollbackCoatings")
        Model.import_file(self.hardware, coatings)
        self.hardware.save()
        Model.import_file(self.assembly, self.hardware)
        self.assembly.save()
        assembly_path, coatings_path = self.assembly.FileName, coatings.FileName
        # A valid file was replaced by another definition at the expected path.
        import uuid
        Model.metadata(self.hardware).ObjectId = str(uuid.uuid4())
        self.hardware.save()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        for retain_dependency in (False, True):
            with self.subTest(retain_dependency=retain_dependency):
                if retain_dependency:
                    CadDocument.open(coatings_path)
                existing = Model.new_document("UnsavedWork")
                self.root(existing).Label = "Keep my unsaved edits"
                before = dict(App.listDocuments())
                App.setActiveDocument(existing.Name)
                with self.assertRaisesRegex(ValueError, "identity differs"):
                    CadDocument.open(assembly_path)
                self.assertEqual(App.listDocuments(), before)
                self.assertEqual(App.ActiveDocument, existing)
                self.assertEqual(self.root(existing).Label, "Keep my unsaved edits")
                self.assertEqual(existing.FileName, "")
            for doc in list(App.listDocuments().values()):
                App.closeDocument(doc.Name)

    def testFailedRootRestoreClosesNewDependencyGraph(self):
        Model.import_file(self.assembly, self.hardware)
        self.assembly.save()
        filename = self.assembly.FileName
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        activate = Model.activate
        def fail_root(component, strict=True):
            path = component.Document.FileName
            if path and Path(path).resolve() == Path(filename).resolve():
                raise ValueError("Injected root activation failure")
            return activate(component, strict)
        with patch.object(Model, "activate", side_effect=fail_root):
            with self.assertRaisesRegex(ValueError, "root activation failure"):
                CadDocument.open(filename)
        self.assertEqual(App.listDocuments(), {})

    def testManifestRejectsOmittedDuplicateAndReparentedPlacements(self):
        Model.add_component(self.root(self.assembly), self.screw)
        Model.create_definition(self.assembly, "Other parent")
        self.assembly.save()
        with zipfile.ZipFile(self.assembly.FileName) as archive:
            entries = {name: archive.read(name) for name in archive.namelist()}
        for mode in ("omitted", "duplicate", "reparented", "external-kind", "definition-name"):
            with self.subTest(mode=mode):
                data = json.loads(entries[CadDocument.MANIFEST])
                parent = next(d for d in data["definitions"] if d["occurrences"])
                other = next(d for d in data["definitions"] if d != parent)
                if mode == "omitted":
                    parent["occurrences"] = []
                elif mode == "duplicate":
                    parent["occurrences"].append(dict(parent["occurrences"][0]))
                elif mode == "reparented":
                    other["occurrences"] = parent["occurrences"]
                    parent["occurrences"] = []
                elif mode == "external-kind":
                    parent["occurrences"][0]["external"] = False
                else:
                    parent["object"] = "UnknownDefinition"
                path = self.output / (mode + "-placements.cadprt")
                with zipfile.ZipFile(path, "w") as archive:
                    for name, payload in entries.items():
                        archive.writestr(name, json.dumps(data).encode("utf-8")
                                         if name == CadDocument.MANIFEST else payload)
                with self.assertRaises(ValueError):
                    CadDocument.preflight(path)

    def testManifestRejectsMalformedHierarchyRecords(self):
        Model.add_component(self.root(self.assembly), self.screw)
        self.assembly.save()
        with zipfile.ZipFile(self.assembly.FileName) as archive:
            entries = {name: archive.read(name) for name in archive.namelist()}
        for mode in ("definition", "occurrences", "occurrence", "external", "history"):
            with self.subTest(mode=mode):
                data = json.loads(entries[CadDocument.MANIFEST])
                parent = next(d for d in data["definitions"] if d["occurrences"])
                if mode == "definition":
                    data["definitions"] = [None]
                elif mode == "occurrences":
                    parent["occurrences"] = None
                elif mode == "occurrence":
                    parent["occurrences"] = [None]
                elif mode == "external":
                    parent["occurrences"][0]["external"] = "true"
                else:
                    parent["history"] = "Not a history list"
                path = self.output / (mode + "-malformed.cadprt")
                with zipfile.ZipFile(path, "w") as archive:
                    for name, payload in entries.items():
                        archive.writestr(name, json.dumps(data).encode("utf-8")
                                         if name == CadDocument.MANIFEST else payload)
                with self.assertRaises(ValueError):
                    CadDocument.preflight(path)
