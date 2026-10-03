# SPDX-License-Identifier: LGPL-2.1-or-later
"""Shared section layout and transient previews for component operation tasks."""
import FreeCAD as App
from PySide import QtCore, QtGui, QtWidgets
from freecad.gui.ComponentExtrudeTask import ExtrudeTask, CompactFormLayout, CurveListWidget


def tr(text):
    return App.Qt.translate("ComponentOperation", text)


class OperationTask(ExtrudeTask):
    def build_sections(self):
        self.form = QtWidgets.QWidget()
        self.form.setAutoFillBackground(True)
        self.form.setBackgroundRole(QtGui.QPalette.Base)
        self.form.setForegroundRole(QtGui.QPalette.Text)
        self.form.setStyleSheet("QWidget { background-color: palette(base); color: palette(text); }")
        self.form.setWindowTitle(tr(self.operation_name))
        outer = QtWidgets.QVBoxLayout(self.form)
        self.sections = []
        for title, expanded in (("Main parameters", True), ("Dimensions", True), ("Advanced", False), ("Preview", True)):
            button = QtWidgets.QToolButton()
            button.setText(tr(title))
            button.setCheckable(True)
            button.setChecked(expanded)
            button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
            button.setArrowType(QtCore.Qt.DownArrow if expanded else QtCore.Qt.RightArrow)
            body = QtWidgets.QWidget()
            body.setVisible(expanded)
            layout = CompactFormLayout(body)
            button.toggled.connect(body.setVisible)
            button.toggled.connect(lambda checked, b=button: b.setArrowType(QtCore.Qt.DownArrow if checked else QtCore.Qt.RightArrow))
            outer.addWidget(button)
            outer.addWidget(body)
            self.sections.append((button, body, layout))
        return outer

    def combo(self, layout, label, items):
        widget = QtWidgets.QComboBox()
        for text, value in items:
            widget.addItem(tr(text), value)
        layout.addRow(tr(label), widget)
        return widget

    def build_profile_collector(self, main):
        import ComponentModel as Model
        component = self.component
        self.profile = self.combo(main, "Profile", [("Select a profile…", None)])
        for obj in Model.history(component):
            if (getattr(obj, "ComponentRole", "") in ("Object", "Reference", "Result") and hasattr(obj, "Shape")
                    and not obj.Shape.Solids and obj.Shape.Edges):
                self.profile.addItem(obj.Label + " (" + obj.Name + ")", obj.Name)
        self.curves = CurveListWidget()
        self.curves.removeRequested.connect(self.remove_selected_curves)
        self.curves.setMaximumHeight(100)
        self.curves.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        main.addRow(tr("Curves"), self.curves)
        row = QtWidgets.QWidget()
        buttons = QtWidgets.QGridLayout(row)
        buttons.setContentsMargins(0, 0, 0, 0)
        for index, (label, callback) in enumerate((("Remove", self.remove_selected_curves),
                                                 ("Clear", lambda: self.set_curves([], False)), ("Use all", self.profile_changed))):
            button = QtWidgets.QPushButton(tr(label))
            button.clicked.connect(callback)
            buttons.addWidget(button, index // 2, index % 2)
        main.addRow(row)
        self.region_pick = QtWidgets.QCheckBox(tr("Pick closed regions in the view"))
        self.region_pick.setChecked(True)
        self.region_pick.toggled.connect(self.update_regions)
        main.addRow(self.region_pick)

    def begin_reference_pick(self, field):
        self.reference_pick = field
        self.status.setText(tr("Pick a local axis, edge, plane or limiting face."))

    def addSelection(self, document, name, subname, *args):
        if self.reference_pick is not None:
            import ComponentModel as Model
            doc = App.listDocuments().get(document)
            base = doc.getObject(name) if doc else None
            item = base.getSubObject(subname, 1) if base and subname else base
            if item and (Model.owner(item) == self.component or item in self.component.Origin.OriginFeatures):
                element = subname.rsplit(".", 1)[-1]
                self.reference_pick.setText(item.Name + ("." + element if element.startswith(("Face", "Edge")) else ""))
                self.reference_pick = None
                return
        super().addSelection(document, name, subname, *args)
