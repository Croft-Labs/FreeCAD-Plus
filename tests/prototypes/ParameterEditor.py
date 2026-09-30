# SPDX-License-Identifier: LGPL-2.1-or-later
"""Test-only existing-parameter editor. Not installed or registered as a command."""
import FreeCAD as App
from PySide import QtWidgets
from prototypes.NamedParameters import create_parameter, edit_parameter_expression, rename_parameter


class ParameterEditor(QtWidgets.QDialog):
    def __init__(self, obj, parent=None):
        super().__init__(parent)
        self.obj = obj
        self.doc = obj.Document
        self._closed = False
        self.setWindowTitle("Parameter editor prototype")
        layout = QtWidgets.QFormLayout(self)
        self.parameter = QtWidgets.QComboBox()
        self.name = QtWidgets.QLineEdit()
        self.value = QtWidgets.QLineEdit()
        self.value.setReadOnly(True)
        self.expression = QtWidgets.QLineEdit()
        self.error = QtWidgets.QLabel()
        self.error.setWordWrap(True)
        self.apply = QtWidgets.QPushButton("Apply expression")
        self.rename = QtWidgets.QPushButton("Rename")
        self.refreshButton = QtWidgets.QPushButton("Refresh")
        self.newName = QtWidgets.QLineEdit()
        self.newType = QtWidgets.QComboBox()
        self.newType.addItems(["Length", "Angle"])
        self.newExpression = QtWidgets.QLineEdit()
        self.create = QtWidgets.QPushButton("Create parameter")
        self.closeButton = QtWidgets.QPushButton("Close")
        layout.addRow("Parameter", self.parameter)
        layout.addRow("Name", self.name)
        layout.addRow("Current value", self.value)
        layout.addRow("Expression", self.expression)
        layout.addRow(self.error)
        layout.addRow(self.apply, self.rename)
        layout.addRow("New name", self.newName)
        layout.addRow("New type", self.newType)
        layout.addRow("New expression", self.newExpression)
        layout.addRow(self.create)
        layout.addRow(self.refreshButton, self.closeButton)
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
            self.error.setText("Parameter list changed outside this editor. Refresh to continue.")
            return
        name = self.parameter.currentText()
        enabled = bool(name)
        for widget in (self.name, self.expression, self.apply, self.rename):
            widget.setEnabled(enabled)
        self.name.setText(name)
        self.value.setText(str(getattr(self.obj, name)) if enabled else "")
        expressions = dict(self.obj.ExpressionEngine)
        self.expression.setText(expressions.get(name, expressions.get("." + name, "")))
        self.error.clear()
        self._snapshot = self.snapshot()

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
            create_parameter(self.obj, name, self.newType.currentText(), self.newExpression.text())
        except Exception as error:
            self.error.setText(str(error))
            return
        self.refresh(name)
        self.newName.clear()
        self.newExpression.clear()
