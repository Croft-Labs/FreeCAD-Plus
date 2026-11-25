# SPDX-License-Identifier: LGPL-2.1-or-later
"""Shared creation/edit form for component instance quantities and patterns."""
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets
from .movement import Collector
from .task_status import TaskStatus


class InstanceForm(QtWidgets.QGroupBox):
    def __init__(self, owner, parts, edit=False):
        super().__init__()
        self.resize_timer = QtCore.QTimer(self)
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.resize_page)
        self.setWindowTitle('Edit instance pattern' if edit else 'Create instances')
        layout = QtWidgets.QVBoxLayout(self); layout.setContentsMargins(6, 6, 6, 6)
        def note(text):
            label = QtWidgets.QLabel(text); label.setWordWrap(True); return label
        heading = note('Add to: ' + owner.Label)
        font = heading.font(); font.setBold(True); heading.setFont(font); layout.addWidget(heading)
        source = QtWidgets.QHBoxLayout()
        source.addWidget(note('Components: ' + ', '.join(parts)))
        self.change = QtWidgets.QPushButton('Change parts…'); self.change.setEnabled(not edit)
        source.addWidget(self.change); layout.addLayout(source)
        layout.addWidget(note('Update this pattern. Instances outside it stay unchanged.' if edit else
            'Counts include the first new instance. Existing instances stay unchanged.'))
        self.top = QtWidgets.QFormLayout(); layout.addLayout(self.top)
        self.mode = QtWidgets.QComboBox(); self.mode.addItems(('Quantity', 'Linear', 'Grid', 'Circular'))
        if edit: self.mode.model().item(0).setEnabled(False)
        self.top.addRow('Arrangement', self.mode)
        self.count = QtWidgets.QSpinBox(); self.count.setRange(1, 10000)
        self.top.addRow('Instances per part', self.count)
        self.pages = QtWidgets.QStackedWidget(); layout.addWidget(self.pages)
        self.units = {}; self.positions = {}; self.directions = {}; self.references = {}; self.vectors = {}
        def unit(key, value, unit='mm'):
            field = Gui.UiLoader().createWidget('Gui::InputField')
            field.setProperty('unit', unit); field.setText(str(value) + ' ' + unit)
            field.valueChanged.connect(lambda *args, field=field: field.setProperty('patternParseError', ''))
            field.parseError.connect(lambda error, field=field: field.setProperty('patternParseError', str(error)))
            field.setMinimumWidth(50); self.units[key] = field; return field
        def page(title):
            box = QtWidgets.QGroupBox(title); form = QtWidgets.QFormLayout(box); self.pages.addWidget(box); return form
        def position(form, key, title):
            row = QtWidgets.QHBoxLayout(); fields = []
            for axis in 'XYZ':
                row.addWidget(QtWidgets.QLabel(axis)); field = unit(key + axis, 0)
                row.addWidget(field); fields.append(field)
            form.addRow(title, row); self.positions[key] = fields
        def direction(form, key, title, axes=('Parent X', 'Parent Y', 'Parent Z'), vector=False):
            box = QtWidgets.QComboBox(); box.addItems((*axes, 'Pick edge / axis', *(['Enter vector'] if vector else [])))
            form.addRow(title, box); self.directions[key] = box
            reference = Collector('Click here, then pick an edge or axis'); form.addRow('Reference', reference)
            self.references[key] = reference
            value = QtWidgets.QLineEdit('1, 0, 0'); form.addRow('Vector X, Y, Z', value); self.vectors[key] = value
            def changed(*args):
                form.setRowVisible(reference, box.currentText() == 'Pick edge / axis')
                form.setRowVisible(value, box.currentText() == 'Enter vector')
                self.resize_timer.start(0)
            box.currentIndexChanged.connect(changed); changed()
        quantity = page('Placement'); position(quantity, 'quantity', 'Position')
        quantity.addRow(note('Instances start together at this position. Move or constrain each one afterward.'))
        linear = page('Linear pattern'); position(linear, 'linear', 'Start')
        direction(linear, 'linear', 'Direction', vector=True)
        linear.addRow('Spacing', unit('linear_spacing', 25))
        self.reverse = QtWidgets.QCheckBox('Reverse direction'); linear.addRow(self.reverse)
        grid = page('Grid pattern'); position(grid, 'grid', 'Start')
        self.columns = QtWidgets.QSpinBox(); self.columns.setRange(1, 1000); self.columns.setValue(3)
        grid.addRow('Columns', self.columns); direction(grid, 'columns', 'Column direction')
        grid.addRow('Column spacing', unit('column_spacing', 25))
        self.rows = QtWidgets.QSpinBox(); self.rows.setRange(1, 1000); self.rows.setValue(2)
        grid.addRow('Rows', self.rows); direction(grid, 'rows', 'Row direction')
        self.directions['rows'].setCurrentText('Parent Y')
        grid.addRow('Row spacing', unit('row_spacing', 20))
        circular = page('Circular pattern'); position(circular, 'circular', 'Center')
        direction(circular, 'circular', 'Axis', ('Parent Z', 'Parent X', 'Parent Y'))
        circular.addRow('Radius', unit('radius', 50))
        circular.addRow('Start angle', unit('angle', 0, 'deg'))
        self.full = QtWidgets.QCheckBox('Full circle — evenly spaced'); self.full.setChecked(True); circular.addRow(self.full)
        circular.addRow('Angular spacing', unit('angular_spacing', 60, 'deg'))
        self.orientation = QtWidgets.QComboBox(); self.orientation.addItems(('Keep component orientation', 'Rotate with pattern'))
        circular.addRow('Orientation', self.orientation)
        circular.addRow(note('The first instance uses parent X projected onto the circle plane (parent Y for an X axis). No duplicate at 360°.'))
        layout.addWidget(note('Coordinates and directions are relative to ' + owner.Label + '.'))
        self.preview = QtWidgets.QCheckBox('Preview instances'); self.preview.setChecked(True); layout.addWidget(self.preview)
        self.summary = note(''); layout.addWidget(self.summary)
        self.persistence = note(''); layout.addWidget(self.persistence)
        self.status = TaskStatus(); layout.addWidget(self.status); layout.addStretch()
        self.mode.currentIndexChanged.connect(self.refresh)
        self.full.toggled.connect(self.refresh)
        for field in (self.count, self.columns, self.rows): field.valueChanged.connect(self.refresh)
        self.refresh()

    def resize_page(self):
        page = self.pages.currentWidget()
        height = max(page.sizeHint().height(), page.layout().totalHeightForWidth(self.pages.width())) + 8
        self.pages.setFixedHeight(height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'pages'): self.resize_page()

    def refresh(self, *args):
        index = self.mode.currentIndex(); self.pages.setCurrentIndex(index)
        self.top.setRowVisible(1, index != 2)
        self.units['angular_spacing'].setEnabled(not self.full.isChecked())
        if self.full.isChecked(): self.units['angular_spacing'].setProperty('rawValue', 360.0 / self.count.value())
        self.persistence.setText('Creates independent placements in one Undo step.' if index == 0 else
            'Saved as an editable pattern. Right-click a member → Edit instance pattern. One Undo step.')
        self.resize_page()

    @staticmethod
    def value(field):
        if field.property('patternParseError') or not field.hasAcceptableInput(): raise ValueError('Enter a valid numeric value')
        value = field.property('rawValue')
        return float(value.Value if hasattr(value, 'Value') else value)
