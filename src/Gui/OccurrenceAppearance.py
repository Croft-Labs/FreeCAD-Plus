# SPDX-License-Identifier: LGPL-2.1-or-later
"""Explicit whole-link appearance edits using native view properties and transactions."""
import math

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets


def _tr(text):
    return App.Qt.translate("OccurrenceAppearance", text)


def _identity(obj):
    return (obj.Document.Name, obj.Name, obj.ID)


def _material_values(material):
    return {name: getattr(material, name) for name in (
        "DiffuseColor", "AmbientColor", "SpecularColor", "EmissiveColor", "Shininess", "Transparency")}


def validate(link):
    if link.TypeId != "App::Link" or link.ElementCount:
        raise ValueError(_tr("Select one whole native Link, not an array or a source definition."))
    source = link.LinkedObject
    if (source is None or not hasattr(source, "Document") or source.Document != link.Document
            or not source.isDerivedFrom("Part::Feature")):
        raise ValueError(_tr("This pilot requires a direct link to a Part shape or Body in the same document."))
    view = link.ViewObject
    if (len(view.ShapeAppearance) != 1 or view.OverrideColorList or view.MaterialList
            or view.OverrideMaterialList):
        raise ValueError(_tr("Per-element or array appearance overrides are outside this editor's scope."))
    return source


def selected_link():
    selection = Gui.Selection.getSelectionEx("*", 0)
    if len(selection) != 1:
        raise ValueError(_tr("Select one whole Link object in the tree, without faces or nested occurrence paths."))
    link = selection[0].Object
    subnames = selection[0].SubElementNames
    if subnames:
        if len(subnames) != 1 or not subnames[0].endswith("."):
            raise ValueError(_tr("Select a whole Link, without faces or edges."))
        path = link.getSubObjectList(subnames[0])
        if not path or any(obj.TypeId != "App::Part" for obj in path[:-1]):
            raise ValueError(_tr("Select the Link itself, not a path through another occurrence."))
        link = path[-1]
    validate(link)
    return link


def state(link):
    source = validate(link)
    return {"link": _identity(link), "source": _identity(source),
            "visible": link.Visibility, "override": link.ViewObject.OverrideMaterial,
            "material": _material_values(link.ViewObject.ShapeAppearance[0]),
            "source_materials": [_material_values(m) for m in source.ViewObject.ShapeAppearance]}


def apply(link, expected, visible, override, rgb, transparency):
    if App.ActiveDocument != link.Document or Gui.Control.activeDialog() or link.Document.HasPendingTransaction:
        raise ValueError(_tr("Activate the occurrence's document and finish the current task or edit transaction."))
    current = state(link)
    if current != expected:
        raise ValueError(_tr("The link, source or appearance changed. Reload before applying."))
    if (len(rgb) != 3 or any(not math.isfinite(x) or not 0 <= x <= 1 for x in rgb)
            or not math.isfinite(transparency) or not 0 <= transparency <= 100):
        raise ValueError(_tr("Choose a valid RGB colour and transparency from 0 to 100 percent."))
    doc = link.Document
    doc.openTransaction("Change occurrence appearance")
    try:
        if override:
            values = current["material"] if current["override"] else current["source_materials"][0]
            material = App.Material(**values)
            material.DiffuseColor = tuple(rgb) + (1.0,)
            material.Transparency = transparency / 100.0
            link.ViewObject.ShapeAppearance = [material]
        link.ViewObject.OverrideMaterial = override
        link.Visibility = visible
        doc.commitTransaction()
    except Exception:
        doc.abortTransaction()
        raise


class AppearanceDialog(QtWidgets.QDialog):
    def __init__(self, link, parent=None):
        super().__init__(parent)
        self.link = link
        self._closed = False
        self.expected = None
        self.setWindowTitle(_tr("Occurrence appearance"))
        self.resize(660, 360)
        layout = QtWidgets.QFormLayout(self)
        self.identity = QtWidgets.QLabel()
        self.identity.setWordWrap(True)
        self.identity.setTextFormat(QtCore.Qt.PlainText)
        self.visible = QtWidgets.QCheckBox(_tr("Visible"))
        self.override = QtWidgets.QCheckBox(_tr("Override source appearance for this occurrence"))
        self.colorButton = QtWidgets.QPushButton()
        self.transparency = QtWidgets.QDoubleSpinBox()
        self.transparency.setRange(0, 100)
        self.transparency.setDecimals(2)
        self.transparency.setSuffix(" %")
        self.inherit = QtWidgets.QPushButton(_tr("Use source appearance"))
        self.reloadButton = QtWidgets.QPushButton(_tr("Reload current values"))
        self.applyButton = QtWidgets.QPushButton(_tr("Apply"))
        close = QtWidgets.QPushButton(_tr("Close"))
        self.message = QtWidgets.QLabel()
        self.message.setWordWrap(True)
        self.message.setTextFormat(QtCore.Qt.PlainText)
        note = QtWidgets.QLabel(_tr(
            "Changes apply to this whole occurrence. Colour and transparency affect display only, "
            "not engineering material, mass or FEM. Visibility does not suppress geometry or change "
            "BOM inclusion. Placement and shared source geometry are preserved. Apply is undoable; "
            "Close discards unapplied choices."))
        note.setWordWrap(True)
        layout.addRow(self.identity)
        layout.addRow(self.visible)
        layout.addRow(self.override)
        layout.addRow(_tr("Colour (all faces)"), self.colorButton)
        layout.addRow(_tr("Transparency"), self.transparency)
        layout.addRow(self.inherit)
        layout.addRow(note)
        layout.addRow(self.message)
        layout.addRow(self.reloadButton, self.applyButton)
        layout.addRow(close)
        for button in self.findChildren(QtWidgets.QPushButton):
            button.setAutoDefault(False)
        self.override.toggled.connect(self.updateControls)
        self.inherit.clicked.connect(lambda: self.override.setChecked(False))
        self.colorButton.clicked.connect(self.chooseColor)
        self.reloadButton.clicked.connect(self.reload)
        self.applyButton.clicked.connect(self.commit)
        close.clicked.connect(self.reject)
        self.reload()
        App.addDocumentObserver(self)

    def setColor(self, color):
        self.color = QtGui.QColor(color)
        self.colorButton.setText(self.color.name().upper())
        pixmap = QtGui.QPixmap(22, 16)
        pixmap.fill(self.color)
        self.colorButton.setIcon(QtGui.QIcon(pixmap))

    def chooseColor(self):
        color = QtWidgets.QColorDialog.getColor(self.color, self, _tr("Occurrence colour"))
        if color.isValid():
            self.setColor(color)

    def updateControls(self, *args):
        self.colorButton.setEnabled(self.override.isChecked())
        self.transparency.setEnabled(self.override.isChecked())

    def reload(self):
        try:
            self.expected = state(self.link)
            source = self.link.LinkedObject
            self.identity.setText(_tr("Occurrence: ") + self.link.Label + " [" + self.link.Name + "]\n" +
                                  _tr("Shared source: ") + source.Label + " [" + source.Name + "]")
            values = self.expected["material"] if self.expected["override"] else self.expected["source_materials"][0]
            self.visible.setChecked(self.expected["visible"])
            self.override.setChecked(self.expected["override"])
            self.setColor(QtGui.QColor.fromRgbF(*values["DiffuseColor"][:3]))
            self.transparency.setValue(values["Transparency"] * 100)
            self.updateControls()
            self.applyButton.setEnabled(True)
            self.message.setText(_tr("Review the occurrence values, then Apply. No live preview changes are made."))
        except Exception as error:
            self.expected = None
            self.applyButton.setEnabled(False)
            self.message.setText(str(error))

    def commit(self):
        try:
            apply(self.link, self.expected, self.visible.isChecked(), self.override.isChecked(),
                  self.color.getRgbF()[:3], self.transparency.value())
            self.reload()
            self.message.setText(_tr("Occurrence appearance applied. Undo restores the previous values."))
        except Exception as error:
            self.message.setText(str(error))

    def slotDeletedObject(self, obj):
        if obj == self.link:
            self.reject()
        elif self.expected and _identity(obj) == self.expected["source"]:
            self.expected = None
            self.applyButton.setEnabled(False)
            self.message.setText(_tr("The shared source was deleted. Repair the link and reload."))

    def slotDeletedDocument(self, doc):
        if doc == self.link.Document:
            self.reject()

    def done(self, result):
        if not self._closed:
            self._closed = True
            App.removeDocumentObserver(self)
        super().done(result)


_dialogs = []


class CommandAppearance:
    def GetResources(self):
        return {"MenuText": _tr("Occurrence appearance..."),
                "ToolTip": _tr("Edit one linked occurrence's visibility, colour and transparency")}

    def IsActive(self):
        try:
            link = selected_link()
            return (App.ActiveDocument == link.Document and not Gui.Control.activeDialog()
                    and not link.Document.HasPendingTransaction)
        except (ValueError, RuntimeError):
            return False

    def Activated(self):
        dialog = AppearanceDialog(selected_link(), Gui.getMainWindow())
        _dialogs.append(dialog)
        dialog.finished.connect(lambda _result: _dialogs.remove(dialog) if dialog in _dialogs else None)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()


def registerCommand():
    Gui.addCommand("Std_OccurrenceAppearance", CommandAppearance())
