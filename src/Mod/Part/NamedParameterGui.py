# SPDX-License-Identifier: LGPL-2.1-or-later
"""Named parameter editor and explicit Part/container command entry."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtWidgets
from NamedParameters import create_parameter, edit_parameter_expression, rename_parameter


def _tr(text):
    return App.Qt.translate("NamedParameters", text)


class ParameterEditor(QtWidgets.QDialog):
    def __init__(self, obj, parent=None):
        super().__init__(parent)
        self.obj = obj
        self.doc = obj.Document
        self._closed = False
        self.setWindowTitle(_tr("Named parameters") + " - " + obj.Label)
        layout = QtWidgets.QFormLayout(self)
        self.parameter = QtWidgets.QComboBox()
        self.name = QtWidgets.QLineEdit()
        self.value = QtWidgets.QLineEdit()
        self.value.setReadOnly(True)
        self.displayUnit = QtWidgets.QComboBox()
        self.description = QtWidgets.QLineEdit()
        self.description.setReadOnly(True)
        self.expression = QtWidgets.QLineEdit()
        self.reference = QtWidgets.QLineEdit()
        self.reference.setReadOnly(True)
        self.copyReference = QtWidgets.QPushButton(_tr("Copy reference"))
        self.copyReference.clicked.connect(self.copyParameterReference)
        self.error = QtWidgets.QLabel()
        self.error.setWordWrap(True)
        self.apply = QtWidgets.QPushButton(_tr("Apply expression"))
        self.rename = QtWidgets.QPushButton(_tr("Rename"))
        self.refreshButton = QtWidgets.QPushButton(_tr("Refresh"))
        self.newName = QtWidgets.QLineEdit()
        self.newType = QtWidgets.QComboBox()
        self.newType.addItems(["Length", "Angle"])
        self.newDescription = QtWidgets.QLineEdit()
        self.newExpression = QtWidgets.QLineEdit()
        self.create = QtWidgets.QPushButton(_tr("Create parameter"))
        self.closeButton = QtWidgets.QPushButton(_tr("Close"))
        layout.addRow(_tr("Parameter"), self.parameter)
        layout.addRow(_tr("Name"), self.name)
        layout.addRow(_tr("Current value"), self.value)
        layout.addRow(_tr("Display unit"), self.displayUnit)
        layout.addRow(_tr("Description"), self.description)
        layout.addRow(_tr("Expression"), self.expression)
        layout.addRow(_tr("Reference in this document"), self.reference)
        layout.addRow(self.copyReference)
        layout.addRow(self.error)
        layout.addRow(self.apply, self.rename)
        layout.addRow(_tr("New name"), self.newName)
        layout.addRow(_tr("New type"), self.newType)
        layout.addRow(_tr("New expression"), self.newExpression)
        layout.addRow(_tr("New description"), self.newDescription)
        layout.addRow(self.create)
        layout.addRow(self.refreshButton, self.closeButton)
        self.displayUnit.currentIndexChanged.connect(self.updateDisplayedValue)
        self.parameter.currentIndexChanged.connect(self.loadParameter)
        self.create.clicked.connect(self.createParameter)
        self.apply.clicked.connect(self.applyExpression)
        self.rename.clicked.connect(self.renameParameter)
        self.closeButton.clicked.connect(self.reject)
        self.refreshButton.clicked.connect(lambda: self.refresh(self.parameter.currentText()))
        self.refresh()
        App.addDocumentObserver(self)

    def refresh(self, selected=None):
        if self._closed:
            return
        self.parameter.blockSignals(True)
        self.parameter.clear()
        for name in self.obj.PropertiesList:
            if self.obj.getTypeIdOfProperty(name) in ("App::PropertyLength", "App::PropertyAngle"):
                self.parameter.addItem(name)
        index = self.parameter.findText(selected) if selected else 0
        self.parameter.setCurrentIndex(max(0, index))
        self.parameter.blockSignals(False)
        self.loadParameter()

    def loadParameter(self, *args):
        if self._closed:
            return
        available = [name for name in self.obj.PropertiesList
                     if self.obj.getTypeIdOfProperty(name) in
                     ("App::PropertyLength", "App::PropertyAngle")]
        displayed = [self.parameter.itemText(i) for i in range(self.parameter.count())]
        if displayed != available:
            for widget in (self.name, self.expression, self.apply, self.rename):
                widget.setEnabled(False)
            self.value.clear()
            self.reference.clear()
            self.copyReference.setEnabled(False)
            self.displayUnit.setEnabled(False)
            self.description.clear()
            self.error.setText("Parameter list changed outside this editor. Refresh to continue.")
            return
        name = self.parameter.currentText()
        enabled = bool(name)
        self.reference.setText(self.obj.Name + "." + name if enabled else "")
        self.copyReference.setEnabled(enabled)
        for widget in (self.name, self.expression, self.apply, self.rename):
            widget.setEnabled(enabled)
        self.name.setText(name)
        previous_unit = self.displayUnit.currentText()
        self.displayUnit.blockSignals(True)
        self.displayUnit.clear()
        if enabled:
            units = (["mm", "cm", "m", "in", "ft"]
                     if self.obj.getTypeIdOfProperty(name) == "App::PropertyLength"
                     else ["deg", "rad"])
            self.displayUnit.addItems(units)
            if previous_unit in units:
                self.displayUnit.setCurrentText(previous_unit)
        self.displayUnit.blockSignals(False)
        self.displayUnit.setEnabled(enabled)
        self.description.setText(self.obj.getDocumentationOfProperty(name) if enabled else "")
        self.updateDisplayedValue()
        expressions = dict(self.obj.ExpressionEngine)
        self.expression.setText(expressions.get(name, expressions.get("." + name, "")))
        self.error.clear()
        self._snapshot = self.snapshot()

    def copyParameterReference(self):
        if self._closed:
            return
        try:
            self.requireUnchanged()
        except Exception as error:
            self.error.setText(str(error))
            return
        if self.reference.text():
            QtWidgets.QApplication.clipboard().setText(self.reference.text())

    def applyExpression(self):
        if self._closed:
            return
        try:
            self.requireUnchanged()
            edit_parameter_expression(self.obj, self.parameter.currentText(), self.expression.text())
        except Exception as error:
            self.error.setText(str(error))
            return
        self.loadParameter()

    def renameParameter(self):
        if self._closed:
            return
        name = self.name.text()
        try:
            self.requireUnchanged()
            rename_parameter(self.obj, self.parameter.currentText(), name)
        except Exception as error:
            self.error.setText(str(error))
            return
        self.refresh(name)

    def snapshot(self):
        return tuple((name, str(getattr(self.obj, name)))
                     for name in self.obj.PropertiesList
                     if self.obj.getTypeIdOfProperty(name) in
                     ("App::PropertyLength", "App::PropertyAngle")), tuple(self.obj.ExpressionEngine)

    def requireUnchanged(self):
        if self.snapshot() != self._snapshot:
            raise ValueError("Parameters changed outside this editor. Refresh before applying changes.")

    def slotDeletedObject(self, obj):
        if obj == self.obj:
            self.reject()

    def slotDeletedDocument(self, doc):
        if doc == self.doc:
            self.reject()

    def done(self, result):
        if not self._closed:
            self._closed = True
            App.removeDocumentObserver(self)
        super().done(result)

    def createParameter(self):
        if self._closed:
            return
        name = self.newName.text()
        try:
            self.requireUnchanged()
            create_parameter(self.obj, name, self.newType.currentText(), self.newExpression.text(),
                             self.newDescription.text())
        except Exception as error:
            self.error.setText(str(error))
            return
        self.refresh(name)
        self.newName.clear()
        self.newExpression.clear()
        self.newDescription.clear()

    def updateDisplayedValue(self, *args):
        if self._closed:
            return
        name = self.parameter.currentText()
        unit = self.displayUnit.currentText()
        if not name or not unit:
            self.value.clear()
            return
        if name not in self.obj.PropertiesList:
            self.value.clear()
            self.error.setText("Parameter list changed outside this editor. Refresh to continue.")
            return
        self.value.setText(str(getattr(self.obj, name).getValueAs(unit)) + " " + unit)


def edit_parameter_set(parameters, parent=None):
    """Open an explicitly supplied Part-owned native container; caller retains dialog."""
    owner = parameters.getParentGeoFeatureGroup()
    if parameters.TypeId != "App::FeaturePython" or owner is None or owner.TypeId != "App::Part":
        raise ValueError("Choose a native parameter container in an explicit Part definition")
    dialog = ParameterEditor(parameters, parent)
    dialog.show()
    return dialog


_dialogs = {}


def selected_parameter_target():
    from NamedParameters import is_parameter_set

    selection = Gui.Selection.getSelection()
    if len(selection) != 1 or (selection[0].TypeId != "App::Part"
                               and not is_parameter_set(selection[0])):
        raise ValueError(_tr("Select one Part container or its named parameter set in the tree."))
    return selection[0]


def open_for_target(target):
    """Resolve only the explicitly selected definition; retain one dialog per set."""
    from NamedParameters import create_parameter_set, is_parameter_set

    if target.Document.HasPendingTransaction:
        raise ValueError(_tr("Finish the current edit before opening named parameters."))
    if target.TypeId == "App::Part":
        candidates = [obj for obj in target.Group if is_parameter_set(obj)]
        if len(candidates) > 1:
            raise ValueError(_tr("This Part has multiple parameter sets. Select the set to edit."))
        parameters = candidates[0] if candidates else create_parameter_set(target)
    elif is_parameter_set(target):
        parameters = target
    else:
        raise ValueError(_tr("Select a Part definition or its named parameter set, not a Body or occurrence."))
    key = (parameters.Document.Name, parameters.Name)
    dialog = _dialogs.get(key)
    if dialog is None:
        dialog = edit_parameter_set(parameters, Gui.getMainWindow())
        _dialogs[key] = dialog
        dialog.finished.connect(lambda _result: _dialogs.pop(key, None))
    dialog.show()
    dialog.raise_()
    dialog.activateWindow()
    return dialog


class CommandNamedParameters:
    def GetResources(self):
        return {"MenuText": _tr("Named parameters..."),
                "ToolTip": _tr("Select a Part container or its parameter set to create and edit named lengths and angles.")}

    def IsActive(self):
        try:
            target = selected_parameter_target()
            return not target.Document.HasPendingTransaction
        except ValueError:
            return False

    def Activated(self):
        try:
            open_for_target(selected_parameter_target())
        except Exception as error:
            QtWidgets.QMessageBox.warning(Gui.getMainWindow(), _tr("Named parameters"), str(error))


def registerCommand():
    Gui.addCommand("Part_NamedParameters", CommandNamedParameters())
