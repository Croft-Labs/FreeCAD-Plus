# SPDX-License-Identifier: LGPL-2.1-or-later
"""Approved Move/Rotate/Align method controls; operations live in movement.py."""
from PySide6 import QtWidgets


def build_method(task, method):
    page = QtWidgets.QGroupBox(method); form = QtWidgets.QFormLayout(page)
    task.method_layout.addWidget(page)
    if method == 'Distance and vector':
        task.direction = task.combo(('Parent X', 'Parent Y', 'Parent Z', 'Pick edge / axis', 'Two points', 'Enter vector'))
        form.addRow('Direction', task.direction)
        host = QtWidgets.QWidget(); details = QtWidgets.QFormLayout(host); details.setContentsMargins(0, 0, 0, 0)
        details.addRow('Reference', task.reference('direction', 'Pick an edge or axis'))
        details.addRow('From', task.reference('from', 'Pick start point'))
        details.addRow('To', task.reference('to', 'Pick end point'))
        task.vector_fields = []
        for axis, value in zip('XYZ', (1, 0, 0)):
            field = QtWidgets.QDoubleSpinBox(); field.setDecimals(6); field.setRange(-1e9, 1e9); field.setValue(value)
            field.editingFinished.connect(task.input_changed); details.addRow(axis, field); task.vector_fields.append(field)
        form.addRow(host)
        def show_direction(*args):
            index = task.direction.currentIndex()
            for row in range(details.rowCount()):
                details.setRowVisible(row, (row == 0 and index == 3) or (row in (1, 2) and index == 4) or (row >= 3 and index == 5))
            host.setVisible(index >= 3)
        task.direction.currentIndexChanged.connect(show_direction); show_direction()
        task.distance = task.quantity(nonnegative=True); form.addRow('Distance', task.distance)
        task.reverse = QtWidgets.QCheckBox('Reverse direction'); form.addRow(task.reverse); task.reverse.toggled.connect(task.input_changed)
    elif method == 'Point to point':
        form.addRow('From', task.reference('from', 'Pick source point'))
        form.addRow('To', task.reference('to', 'Pick destination point'))
        note = QtWidgets.QLabel('Move the source point onto the destination. Keep orientation.'); note.setWordWrap(True); form.addRow(note)
    elif method == 'Axis and angle':
        task.axis = task.combo(('Parent X', 'Parent Y', 'Parent Z', 'Pick edge / axis', 'Two points'))
        task.axis.setCurrentIndex(2); form.addRow('Axis', task.axis)
        host = QtWidgets.QWidget(); details = QtWidgets.QFormLayout(host); details.setContentsMargins(0, 0, 0, 0)
        details.addRow('Reference', task.reference('axis', 'Pick an edge or axis'))
        details.addRow('From', task.reference('from', 'Pick first axis point'))
        details.addRow('To', task.reference('to', 'Pick second axis point')); form.addRow(host)
        def show_axis(*args):
            index = task.axis.currentIndex()
            for row in range(3): details.setRowVisible(row, (row == 0 and index == 3) or (row > 0 and index == 4))
            host.setVisible(index >= 3)
        task.axis.currentIndexChanged.connect(show_axis); show_axis()
        pivot = QtWidgets.QHBoxLayout(); pivot.addWidget(task.reference('pivot', 'Axis origin (Delete to reset)'))
        reset = QtWidgets.QPushButton('Reset'); reset.clicked.connect(lambda: task.clear_reference('pivot')); pivot.addWidget(reset)
        form.addRow('Pivot', pivot)
        task.angle = task.quantity('deg', nonnegative=True); form.addRow('Angle', task.angle)
        task.reverse = QtWidgets.QCheckBox('Reverse rotation'); form.addRow(task.reverse); task.reverse.toggled.connect(task.input_changed)
    elif method == 'Dynamic drag':
        task.control = task.combo(('Components', 'Pivot only')); form.addRow('Control', task.control)
        if task.kind.currentText() == 'Rotate': task.control.model().item(1).setEnabled(False)
        form.addRow('Pivot', task.reference('pivot', 'Selection center · parent axes'))
        reset = QtWidgets.QPushButton('Reset pivot'); reset.clicked.connect(task.reset_pivot); form.addRow(reset)
        rotating = task.kind.currentText() == 'Rotate'
        task.handle = task.combo(('X rotation ring', 'Y rotation ring', 'Z rotation ring') if rotating else
                                 ('X arrow', 'Y arrow', 'Z arrow', 'XY plane', 'YZ plane', 'ZX plane'))
        form.addRow('Active handle', task.handle)
        task.drag_value = task.quantity('deg' if rotating else 'mm'); form.addRow('Angle' if rotating else 'Distance', task.drag_value)
        task.drag_value.textEdited.connect(lambda *unused: setattr(task, 'drag_dirty', True))
        task.snap = QtWidgets.QCheckBox('Snap angle' if rotating else 'Snap distance'); task.snap.toggled.connect(task.input_changed)
        snap = QtWidgets.QHBoxLayout(); snap.addWidget(task.snap)
        task.increment = task.quantity('deg' if rotating else 'mm', 15 if rotating else 1, True); snap.addWidget(task.increment); form.addRow(snap)
        task.drag_value.valueChanged.disconnect(task.input_changed); task.drag_value.valueChanged.connect(task.numeric_drag)
        task.handle.currentIndexChanged.connect(task.reset_numeric_drag); task.control.currentIndexChanged.connect(task.reset_numeric_drag)
    elif method == 'Axes':
        form.addRow('Source axis', task.reference('source_axis', 'Pick source axis'))
        form.addRow('Target axis', task.reference('target_axis', 'Pick target axis'))
        task.alignment = task.combo(('Coincident', 'Parallel')); form.addRow('Alignment', task.alignment)
        task.reverse = QtWidgets.QCheckBox('Reverse target direction'); form.addRow(task.reverse); task.reverse.toggled.connect(task.input_changed)
    else:
        form.addRow('Source frame', task.reference('source_frame', 'Pick source coordinate system'))
        form.addRow('Target frame', task.reference('target_frame', 'Pick target coordinate system'))
        task.advanced = QtWidgets.QToolButton(); task.advanced.setText('Define origin and axes…'); task.advanced.setCheckable(True); form.addRow(task.advanced)
        host = QtWidgets.QWidget(); definitions = QtWidgets.QFormLayout(host)
        for frame in ('Source', 'Target'):
            for reference in ('origin', 'Z axis', 'X axis'):
                definitions.addRow(frame + ' ' + reference, task.reference(frame.lower() + '_' + reference[0].lower(), 'Pick ' + reference))
        form.addRow(host); host.hide(); task.advanced.toggled.connect(host.setVisible); task.advanced.toggled.connect(task.input_changed)
