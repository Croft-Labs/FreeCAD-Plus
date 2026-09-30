# SPDX-License-Identifier: LGPL-2.1-or-later
"""Test-only existing-parameter editor. Not installed or registered as a command."""
from PySide import QtWidgets
from prototypes.NamedParameters import edit_parameter_expression, rename_parameter


class ParameterEditor(QtWidgets.QDialog):
    def __init__(self, obj, parent=None):
        super().__init__(parent)
        self.obj = obj
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
        self.closeButton = QtWidgets.QPushButton("Close")
        layout.addRow("Parameter", self.parameter)
        layout.addRow("Name", self.name)
        layout.addRow("Current value", self.value)
        layout.addRow("Expression", self.expression)
        layout.addRow(self.error)
        layout.addRow(self.apply, self.rename)
        layout.addRow(self.closeButton)
        self.parameter.currentIndexChanged.connect(self.loadParameter)
        self.apply.clicked.connect(self.applyExpression)
        self.rename.clicked.connect(self.renameParameter)
        self.closeButton.clicked.connect(self.reject)
        self.refresh()

    def refresh(self, selected=None):
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
        name = self.parameter.currentText()
        enabled = bool(name)
        for widget in (self.name, self.expression, self.apply, self.rename):
            widget.setEnabled(enabled)
        self.name.setText(name)
        self.value.setText(str(getattr(self.obj, name)) if enabled else "")
        expressions = dict(self.obj.ExpressionEngine)
        self.expression.setText(expressions.get(name, expressions.get("." + name, "")))
        self.error.clear()

    def applyExpression(self):
        try:
            edit_parameter_expression(self.obj, self.parameter.currentText(), self.expression.text())
        except Exception as error:
            self.error.setText(str(error))
            return
        self.loadParameter()

    def renameParameter(self):
        name = self.name.text()
        try:
            rename_parameter(self.obj, self.parameter.currentText(), name)
        except Exception as error:
            self.error.setText(str(error))
            return
        self.refresh(name)
