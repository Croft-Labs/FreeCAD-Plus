# SPDX-License-Identifier: LGPL-2.1-or-later
"""Collect saved native documents without rewriting their geometry or identities."""
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import tempfile
import xml.etree.ElementTree as ET
import zipfile

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets


def tr(text):
    return App.Qt.translate("ProjectPackage", text)


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def review(doc):
    """Follow only serialized native XLinks, including unloaded dependencies.

    Preserve the relative directory layout so native documents remain byte-identical.
    No save, load, recompute, relink, or source mutation takes place here.
    """
    result = {"root": doc.FileName, "files": [], "references": [], "errors": []}
    errors = result["errors"]
    if not doc.FileName:
        errors.append(tr("Save the root document before reviewing a package."))
        return result
    pending = [Path(os.path.abspath(doc.FileName))]
    seen = set()
    while pending:
        path = pending.pop(0)
        if path in seen:
            continue
        if len(seen) >= 128:
            errors.append(tr("This package supports at most 128 native documents."))
            break
        seen.add(path)
        row = {"source": str(path), "path": "", "sha256": "", "size": 0}
        result["files"].append(row)
        try:
            if path.suffix.lower() != ".fcstd":
                raise ValueError(tr("Only saved FCStd dependencies are supported."))
            if not path.is_file():
                raise ValueError(tr("Missing or inaccessible source file."))
            if path.resolve() != path:
                raise ValueError(tr("Symbolic-link source paths are not supported."))
            for loaded in App.listDocuments().values():
                if loaded.FileName and Path(os.path.abspath(loaded.FileName)) == path:
                    gui_doc = Gui.getDocument(loaded.Name)
                    if (gui_doc and gui_doc.Modified) or loaded.HasPendingTransaction:
                        raise ValueError(tr("Save and finish edits in this document before packaging."))
                    if any("Touched" in obj.State or "Invalid" in obj.State for obj in loaded.Objects):
                        raise ValueError(tr("Recompute and repair this document, then save it."))
            row["sha256"] = digest(path)
            row["size"] = path.stat().st_size
            with zipfile.ZipFile(path) as archive:
                info = archive.getinfo("Document.xml")
                if info.file_size > 32 * 1024 * 1024:
                    raise ValueError(tr("Document metadata exceeds the supported review size."))
                tree = ET.fromstring(archive.read(info))
            for obj in tree.findall("./Objects/Object"):
                if "Python" in obj.get("type", ""):
                    errors.append(str(path) + ": " + tr("Python feature code is not bundled: ") + obj.get("name", ""))
            for obj in tree.findall("./ObjectData/Object"):
                for prop in obj.findall("./Properties/Property"):
                    kind = prop.get("type", "")
                    if kind in ("App::PropertyFile", "App::PropertyPath"):
                        value = prop.find("String")
                        if value is not None and value.get("value"):
                            errors.append(str(path) + ": " + obj.get("name", "") + "." + prop.get("name", "")
                                          + " - " + tr("External file/path assets are not collected."))
                    for link in prop.iter("XLink"):
                        relative = link.get("file", "")
                        if not relative:
                            continue
                        if PureWindowsPath(relative).drive or relative.startswith(("/", "\\")):
                            errors.append(str(path) + ": " + tr("Absolute external links require relinking before packaging: ") + relative)
                            continue
                        target = Path(os.path.abspath(path.parent / relative.replace("\\", "/")))
                        result["references"].append({"source": str(path), "target": str(target),
                            "object": obj.get("name", ""), "property": prop.get("name", ""), "relative": relative})
                        pending.append(target)
        except (OSError, ValueError, KeyError, zipfile.BadZipFile, ET.ParseError) as error:
            errors.append(str(path) + ": " + str(error))
    if result["files"]:
        try:
            base = Path(os.path.commonpath([str(Path(row["source"]).parent) for row in result["files"]]))
            for row in result["files"]:
                row["path"] = "documents/" + Path(row["source"]).relative_to(base).as_posix()
        except ValueError:
            errors.append(tr("All package sources must share a filesystem volume."))
    return result


def create_package(doc, snapshot, destination):
    """Publish one new ZIP only after all reviewed bytes have been copied and checked."""
    current = review(doc)
    if current["errors"]:
        raise ValueError("\n".join(current["errors"]))
    if current != snapshot:
        raise ValueError(tr("Sources changed after review. Refresh and review the package again."))
    destination = Path(destination).absolute()
    if destination.suffix.lower() != ".zip":
        raise ValueError(tr("Choose a new .zip package filename."))
    if destination.exists():
        raise ValueError(tr("The destination already exists. Choose a new filename."))
    names = {row["source"]: row["path"] for row in current["files"]}
    manifest = {"format": "FreeCAD-Plus-native-package", "version": 1,
                "entrypoint": names[str(Path(os.path.abspath(doc.FileName)))],
                "identity": "Preserved native document/object identities; not Make Unique.",
                "files": [{key: row[key] for key in ("path", "sha256", "size")} for row in current["files"]],
                "references": [{"source": names[ref["source"]], "target": names[ref["target"]],
                                "object": ref["object"], "property": ref["property"], "relative": ref["relative"]}
                               for ref in current["references"]]}
    fd, temporary = tempfile.mkstemp(prefix=".freecad-package-", suffix=".zip", dir=destination.parent)
    os.close(fd)
    try:
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as archive:
            for row in current["files"]:
                archive.write(row["source"], row["path"])
            archive.writestr("manifest.json", json.dumps(manifest, indent=2) + "\n")
            archive.writestr("README.txt", "Extract the entire ZIP to a new folder. Close the original project and its source documents.\n"
                             "Open " + manifest["entrypoint"] + ". Keep the documents directory layout unchanged.\n"
                             "Native identities and relative links are preserved. This is a file copy, not Make Unique.\n"
                             "Embedded archive assets are retained; external file assets and Python feature code are unsupported.\n")
        with zipfile.ZipFile(temporary) as archive:
            for row in current["files"]:
                with archive.open(row["path"]) as stream:
                    copied = hashlib.sha256()
                    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                        copied.update(chunk)
                if copied.hexdigest() != row["sha256"]:
                    raise ValueError(tr("A source changed while copying. Refresh and try again."))
        if review(doc) != current:
            raise ValueError(tr("Sources changed while copying. Refresh and try again."))
        # Hard-link publication is atomic and cannot overwrite an existing destination.
        # Unsupported destination filesystems fail without publishing a partial package.
        os.link(temporary, destination)
    finally:
        os.unlink(temporary)
    return manifest


class PackageDialog(QtWidgets.QDialog):
    def __init__(self, doc, parent=None):
        super().__init__(parent)
        self.doc = doc
        self.closed = False
        self.snapshot = None
        self.setWindowTitle(tr("Package saved project"))
        self.resize(1050, 620)
        layout = QtWidgets.QVBoxLayout(self)
        heading = QtWidgets.QLabel(tr("Copy saved FCStd documents and relative native links into a portable ZIP. "
                                      "Originals and identities stay unchanged; this does not Make Unique. "
                                      "Embedded assets are retained. External file assets and Python feature code are unsupported."))
        heading.setWordWrap(True)
        layout.addWidget(heading)
        self.table = QtWidgets.QTreeWidget()
        self.table.setHeaderLabels([tr("Source file"), tr("Package path"), tr("Bytes")])
        layout.addWidget(self.table)
        self.message = QtWidgets.QLabel()
        self.message.setWordWrap(True)
        self.message.setTextFormat(QtCore.Qt.PlainText)
        self.message.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        layout.addWidget(self.message)
        row = QtWidgets.QHBoxLayout()
        self.destination = QtWidgets.QLineEdit()
        self.destination.setPlaceholderText(tr("New ZIP destination"))
        browse = QtWidgets.QPushButton(tr("Choose ZIP..."))
        browse.clicked.connect(self.browse)
        row.addWidget(self.destination)
        row.addWidget(browse)
        layout.addLayout(row)
        buttons = QtWidgets.QHBoxLayout()
        refresh = QtWidgets.QPushButton(tr("Refresh review"))
        refresh.clicked.connect(self.refresh)
        self.createButton = QtWidgets.QPushButton(tr("Create package"))
        self.createButton.clicked.connect(self.create)
        close = QtWidgets.QPushButton(tr("Close"))
        close.clicked.connect(self.reject)
        for button in (refresh, self.createButton, close):
            buttons.addWidget(button)
        layout.addLayout(buttons)
        App.addDocumentObserver(self)
        self.refresh()

    def browse(self):
        name, _filter = QtWidgets.QFileDialog.getSaveFileName(self, tr("New project package"), "", tr("ZIP package (*.zip)"))
        if name:
            self.destination.setText(name)

    def refresh(self):
        self.snapshot = None
        self.createButton.setEnabled(False)
        self.table.clear()
        try:
            self.snapshot = review(self.doc)
            for row in self.snapshot["files"]:
                self.table.addTopLevelItem(QtWidgets.QTreeWidgetItem([row["source"], row["path"], str(row["size"])]))
            for column in range(3):
                self.table.resizeColumnToContents(column)
            errors = self.snapshot["errors"]
            self.message.setText("\n".join(errors) if errors else tr("Ready: %1 native documents, %2 external references. "
                                 "Only the saved files shown above will be copied.").replace("%1", str(len(self.snapshot["files"])))
                                 .replace("%2", str(len(self.snapshot["references"]))))
            self.createButton.setEnabled(not errors)
        except Exception as error:
            self.message.setText(str(error))

    def create(self):
        try:
            manifest = create_package(self.doc, self.snapshot, self.destination.text())
            self.message.setText(tr("Package created. Extract to a new folder, close original documents, then open: ")
                                 + manifest["entrypoint"])
            self.createButton.setEnabled(False)
        except Exception as error:
            self.message.setText(str(error))

    def slotDeletedDocument(self, doc):
        if doc == self.doc:
            self.reject()

    def done(self, result):
        if not self.closed:
            self.closed = True
            App.removeDocumentObserver(self)
        super().done(result)


_dialogs = []


class PackageCommand:
    def GetResources(self):
        return {"MenuText": tr("Package saved project..."),
                "ToolTip": tr("Review and copy saved native documents and relative external links into a new ZIP")}

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        dialog = PackageDialog(App.ActiveDocument, Gui.getMainWindow())
        _dialogs.append(dialog)
        dialog.finished.connect(lambda _result: _dialogs.remove(dialog) if dialog in _dialogs else None)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()


def registerCommand():
    Gui.addCommand("Std_PackageProject", PackageCommand())
