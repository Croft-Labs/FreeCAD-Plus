# SPDX-License-Identifier: LGPL-2.1-or-later
"""Mixed source collection, mesher-specific controls and explicit user defaults."""
import json
import math
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets
from .task_status import TaskStatus
PREFERENCES = 'User parameter:BaseApp/Preferences/FreeCADPlus/Meshing'

class MeshForm(QtWidgets.QGroupBox):

    def __init__(self, tessellation):
        super().__init__()
        self.tess = tessellation
        self.setWindowTitle('Mesh From Shape')
        self.setAutoFillBackground(True)
        layout = QtWidgets.QVBoxLayout(self)
        title = QtWidgets.QLabel('Mesh From Shape')
        font = title.font()
        font.setBold(True)
        font.setPointSize(12)
        title.setFont(font)
        layout.addWidget(title)
        group = QtWidgets.QGroupBox('Objects to mesh')
        inputs = QtWidgets.QVBoxLayout(group)
        self.destination = QtWidgets.QLabel('Add to: Active component')
        inputs.addWidget(self.destination)
        self.sources = QtWidgets.QListWidget()
        self.sources.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.sources.setMinimumHeight(125)
        self.sources.setMaximumHeight(160)
        inputs.addWidget(self.sources)
        row = QtWidgets.QHBoxLayout()
        row.addStretch()
        self.remove = QtWidgets.QPushButton('Remove')
        self.clear = QtWidgets.QPushButton('Clear')
        row.addWidget(self.remove)
        row.addWidget(self.clear)
        inputs.addLayout(row)
        self.hint = QtWidgets.QLabel()
        self.hint.setWordWrap(True)
        inputs.addWidget(self.hint)
        self.update_hint()
        layout.addWidget(group)
        self.tess.findChild(QtWidgets.QCheckBox, 'checkBoxDontQuit').hide()
        page = self.tess.findChild(QtWidgets.QWidget, 'pageStandard')
        for i in range(page.layout().count()):
            item = page.layout().itemAt(i)
            if item.spacerItem():
                item.spacerItem().changeSize(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        layout.addWidget(self.tess)
        self.tess.show()
        output = QtWidgets.QLabel("Creates one combined mesh in the active component's History. Source geometry is kept.")
        output.setWordWrap(True)
        layout.addWidget(output)
        self.status = TaskStatus()
        layout.addWidget(self.status)
        buttons = QtWidgets.QHBoxLayout()
        buttons.addStretch()
        self.done = QtWidgets.QPushButton('Done')
        self.apply = QtWidgets.QPushButton('Apply')
        self.cancel = QtWidgets.QPushButton('Cancel')
        for b in (self.done, self.apply, self.cancel):
            buttons.addWidget(b)
        layout.addLayout(buttons)
        self.method = self.tess.findChild(QtWidgets.QTabWidget, 'stackedWidget')
        self.method.setCurrentIndex(0)
        self.layout().removeWidget(self.tess)
        self.advanced_dialog = QtWidgets.QDialog(self)
        self.advanced_dialog.setWindowTitle('Advanced mesh settings')
        self.advanced_dialog.setModal(True)
        self.advanced_dialog.setPalette(self.palette())
        popup = QtWidgets.QVBoxLayout(self.advanced_dialog)
        models = QtWidgets.QGroupBox('Meshing model')
        choices = QtWidgets.QHBoxLayout(models)
        self.radios = []
        for index, name in enumerate(('Standard', 'Mefisto', 'Netgen', 'Gmsh')):
            radio = QtWidgets.QRadioButton(name)
            radio.setEnabled(self.method.isTabEnabled(index))
            radio.toggled.connect(lambda checked, i=index: self.method.setCurrentIndex(i) if checked else None)
            choices.addWidget(radio)
            self.radios.append(radio)
        self.radios[0].setChecked(True)
        popup.addWidget(models)
        self.method.tabBar().hide()
        self.tess.findChild(QtWidgets.QGroupBox, 'groupBoxMeshingOptions').setTitle('Default settings')
        popup.addWidget(self.tess)
        note = QtWidgets.QLabel('Use these settings for this mesh and as defaults for new meshes.')
        note.setWordWrap(True)
        popup.addWidget(note)
        actions = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.advanced_status = TaskStatus()
        popup.addWidget(self.advanced_status)
        popup.addWidget(actions)
        actions.accepted.connect(self.accept_advanced)
        actions.rejected.connect(self.advanced_dialog.reject)
        self.advanced_dialog.rejected.connect(self.cancel_advanced)
        self.basics = QtWidgets.QGroupBox('Mesh settings')
        self.fields = QtWidgets.QFormLayout(self.basics)
        self.layout().insertWidget(2, self.basics)
        self.advanced = QtWidgets.QPushButton('Advanced settings…')
        self.advanced.clicked.connect(self.open_advanced)
        self.native('relativeDeviation').setChecked(False)
        factory = self.state()
        try:
            saved = App.ParamGet(PREFERENCES).GetString('Defaults')
            if saved:
                self.restore(json.loads(saved))
        except (ValueError, TypeError, KeyError, OverflowError, AttributeError):
            self.restore(factory)
        self.saved_defaults = self.state()
        self.render_fields()

    def update_hint(self):
        self.hint.setText('Select solids or surfaces in the view or History. Shift-click removes; Delete removes list rows.')

    def reset(self):
        self.sources.clear()
        self.restore(self.saved_defaults)
        self.render_fields()

    def native(self, name):
        return self.tess.findChild(QtWidgets.QWidget, name)

    def state(self):
        controls = {}
        for w in self.tess.findChildren(QtWidgets.QWidget):
            if isinstance(w, QtWidgets.QCheckBox):
                prop, value = ('checked', w.isChecked())
            elif isinstance(w, QtWidgets.QComboBox):
                prop, value = ('currentIndex', w.currentIndex())
            elif isinstance(w, QtWidgets.QAbstractSpinBox):
                prop = self.numeric_property(w)
                value = float(w.property(prop))
            else:
                continue
            controls[w.objectName()] = [prop, value]
        return dict(version=1, method=self.method.currentIndex(), controls=controls)

    def restore(self, state):
        index = state['method']
        if type(index) is not int or not 0 <= index < self.method.count() or (not self.method.isTabEnabled(index)):
            raise ValueError('The saved meshing model is unavailable in this application')
        allowed = self.state()['controls']
        pending = []
        for name, pair in state.get('controls', {}).items():
            if name not in allowed:
                continue
            prop, value = pair
            widget = self.native(name)
            expected = allowed[name][0]
            if prop == 'value' and expected == 'rawValue':
                prop = expected
            if prop != expected:
                raise ValueError('Invalid saved mesh control: ' + name)
            if prop == 'checked':
                if type(value) is not bool:
                    raise ValueError('Invalid saved mesh option')
            elif prop == 'currentIndex':
                if type(value) is not int or not 0 <= value < widget.count():
                    raise ValueError('Invalid saved mesh choice')
            elif not isinstance(value, (int, float)) or not math.isfinite(value) or (not widget.property('minimum') <= value <= widget.property('maximum')):
                raise ValueError('Invalid saved mesh number: ' + name)
            pending.append((widget, prop, value))
        for widget, prop, value in sorted(pending, key=lambda item: item[1] not in ('currentIndex', 'checked')):
            widget.setProperty(prop, value)
        self.method.setCurrentIndex(index)
        self.radios[index].setChecked(True)

    def open_advanced(self):
        self.draft_before = self.state()
        self.path_before = self.native('fileChooser').property('fileName')
        self.radios[self.method.currentIndex()].setChecked(True)
        self.advanced_status.setText('')
        self.advanced_dialog.resize(510, 490)
        self.advanced_dialog.open()

    def accept_advanced(self):
        try:
            self.validate_inputs(advanced=True)
            state = self.state()
            App.ParamGet(PREFERENCES).SetString('Defaults', json.dumps(state))
            path = self.native('fileChooser').property('fileName')
            App.ParamGet('User parameter:BaseApp/Preferences/Mod/Mesh/Meshing').SetString('gmshExe', str(path or ''))
            self.saved_defaults = state
            self.render_fields()
            self.advanced_dialog.accept()
        except (ValueError, TypeError) as error:
            self.advanced_status.setError(str(error))

    def cancel_advanced(self):
        self.restore(self.draft_before)
        self.native('fileChooser').setProperty('fileName', self.path_before)
        self.render_fields()

    def number(self, name, label, suffix=''):
        native = self.native(name)
        prop = self.numeric_property(native)
        if prop == 'rawValue':
            spin = Gui.UiLoader().createWidget('Gui::QuantitySpinBox')
            spin.setProperty('unit', native.property('unit'))
        else:
            spin = QtWidgets.QDoubleSpinBox()
            spin.setDecimals(native.decimals())
        for key in ('minimum', 'maximum', 'singleStep'):
            spin.setProperty(key, native.property(key))
        spin.setProperty(prop, native.property(prop))
        spin.setEnabled(native.isEnabled())
        spin.setToolTip(native.toolTip())
        spin.valueChanged.connect(lambda *unused: native.setProperty(prop, spin.property(prop)))
        self.controls[name] = spin
        self.fields.addRow(label, spin)

    def combo(self, name, label):
        native = self.native(name)
        combo = QtWidgets.QComboBox()
        combo.addItems([native.itemText(i) for i in range(native.count())])
        combo.setCurrentIndex(native.currentIndex())
        combo.currentIndexChanged.connect(native.setCurrentIndex)
        combo.currentIndexChanged.connect(self.refresh_enabled)
        self.controls[name] = combo
        self.fields.addRow(label, combo)

    def checkbox(self, name, label):
        native = self.native(name)
        check = QtWidgets.QCheckBox(label)
        check.setChecked(native.isChecked())
        check.toggled.connect(native.setChecked)
        check.toggled.connect(self.refresh_enabled)
        self.controls[name] = check
        self.fields.addRow(check)

    def refresh_enabled(self, *args):
        for name, widget in self.controls.items():
            native = self.native(name)
            widget.setEnabled(native.isEnabled())
            if isinstance(widget, QtWidgets.QAbstractSpinBox):
                with QtCore.QSignalBlocker(widget):
                    widget.setProperty(self.numeric_property(widget), native.property(self.numeric_property(native)))

    def render_fields(self):
        self.advanced.setParent(self)
        while self.fields.count():
            item = self.fields.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.controls = {}
        index = self.method.currentIndex()
        if index == 0:
            self.number('spinSurfaceDeviation', 'Linear deviation', ' mm')
            self.number('spinAngularDeviation', 'Angular deviation', '°')
        elif index == 1:
            self.checkbox('checkMaximumEdgeLength', 'Limit edge length')
            self.number('spinMaximumEdgeLength', 'Maximum edge length', ' mm')
        elif index == 2:
            self.combo('comboFineness', 'Fineness')
            self.number('doubleGrading', 'Mesh size grading')
            self.number('spinEdgeElements', 'Elements per edge')
            self.number('spinCurvatureElements', 'Elements per curvature radius')
            self.checkbox('checkOptimizeSurface', 'Optimize surface')
            self.checkbox('checkSecondOrder', 'Second order elements')
            self.checkbox('checkQuadDominated', 'Quad dominated')
        else:
            self.combo('method', 'Meshing method')
            self.number('minSize', 'Minimum element size', ' mm')
            self.number('maxSize', 'Maximum element size', ' mm')
        self.fields.addRow(self.advanced)
        self.advanced.show()

    @staticmethod
    def numeric_property(widget):
        return 'rawValue' if widget.metaObject().indexOfProperty('rawValue') >= 0 else 'value'

    def validate_inputs(self, advanced=False):
        widgets = self.tess.findChildren(QtWidgets.QAbstractSpinBox) if advanced else self.controls.values()
        for widget in widgets:
            if isinstance(widget, QtWidgets.QAbstractSpinBox) and widget.isEnabled() and (not widget.hasAcceptableInput()):
                raise ValueError('Enter a valid meshing value with the required units')

    def set_busy(self, busy):
        for widget in (self.sources, self.remove, self.clear, self.basics, self.done, self.apply):
            widget.setEnabled(not busy)
