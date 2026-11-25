"""UI-only Move Components proposal. No document/placement operations."""
from PySide6 import QtCore, QtWidgets
import FreeCADGui as Gui
from . import task_status

METHODS = {'Move': ('Distance and vector', 'Point to point', 'Dynamic drag'),
           'Rotate': ('Axis and angle', 'Dynamic drag'),
           'Align': ('Axes', 'Coordinate systems')}

class MoveTask:
    def __init__(self, panel, rows):
        self.panel = panel
        self.form = QtWidgets.QWidget(); self.form.setWindowTitle('Move Components')
        self.form.setMinimumWidth(300)
        box = QtWidgets.QVBoxLayout(self.form); box.setContentsMargins(8,8,8,8)
        context = QtWidgets.QLabel('Active assembly: Machine — fixed\nParent frame: Drive unit')
        context.setWordWrap(True); box.addWidget(context)
        form = QtWidgets.QFormLayout()
        self.kind = QtWidgets.QComboBox(); self.kind.addItems(METHODS)
        self.method = QtWidgets.QComboBox()
        form.addRow('Type', self.kind); form.addRow('Method', self.method); box.addLayout(form)
        group = QtWidgets.QGroupBox('Components'); collector = QtWidgets.QVBoxLayout(group)
        self.components = QtWidgets.QListWidget(); self.components.addItems(['Motor', 'Coupling'])
        self.components.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.components.setFixedHeight(70); collector.addWidget(self.components)
        hint = QtWidgets.QLabel('Click the list, then pick components in the tree or view.')
        hint.setWordWrap(True); collector.addWidget(hint)
        actions = QtWidgets.QHBoxLayout()
        remove = QtWidgets.QPushButton('Remove'); clear = QtWidgets.QPushButton('Clear')
        remove.clicked.connect(lambda: [self.components.takeItem(self.components.row(i)) for i in self.components.selectedItems()])
        clear.clicked.connect(self.components.clear)
        actions.addWidget(remove); actions.addWidget(clear); collector.addLayout(actions)
        self.keep = QtWidgets.QCheckBox('Keep selection after Apply'); self.keep.setChecked(True)
        collector.addWidget(self.keep); box.addWidget(group)
        self.method_host = QtWidgets.QWidget(); self.method_layout = QtWidgets.QVBoxLayout(self.method_host)
        self.method_layout.setContentsMargins(0,0,0,0); box.addWidget(self.method_host)
        self.auto = QtWidgets.QCheckBox('Automatic preview'); self.auto.setChecked(True)
        update = QtWidgets.QPushButton('Update preview')
        row = QtWidgets.QHBoxLayout(); row.addWidget(self.auto); row.addWidget(update); box.addLayout(row)
        self.status = task_status.TaskStatus(); box.addWidget(self.status)
        box.addStretch()
        self.kind.currentTextChanged.connect(self.change_type)
        self.method.currentTextChanged.connect(self.change_method)
        self.change_type('Move')

    def quantity(self, value, unit='mm'):
        widget = Gui.UiLoader().createWidget('Gui::InputField')
        widget.setProperty('unit', unit); widget.setProperty('rawValue', value)
        return widget

    def combo(self, labels):
        widget = QtWidgets.QComboBox(); widget.addItems(labels); return widget

    def reference(self, text):
        widget = QtWidgets.QListWidget(); widget.addItem(text); widget.setFixedHeight(34)
        widget.setToolTip('Click to pick a reference. Delete clears it.')
        return widget

    def change_type(self, kind):
        self.method.blockSignals(True); self.method.clear(); self.method.addItems(METHODS[kind])
        self.method.blockSignals(False); self.change_method(self.method.currentText())

    def change_method(self, method):
        while self.method_layout.count():
            item = self.method_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        page = QtWidgets.QGroupBox(method); form = QtWidgets.QFormLayout(page)
        self.method_layout.addWidget(page)
        if method == 'Distance and vector':
            self.direction = self.combo(['Parent X', 'Parent Y', 'Parent Z', 'Pick edge / axis', 'Two points', 'Enter vector'])
            form.addRow('Direction', self.direction)
            details = QtWidgets.QWidget(); details_form = QtWidgets.QFormLayout(details)
            details_form.setContentsMargins(0,0,0,0)
            form.addRow(details)
            def show_direction(label):
                while details_form.rowCount(): details_form.removeRow(0)
                if label == 'Enter vector':
                    for axis,value in [('X',1),('Y',0),('Z',0)]:
                        field = QtWidgets.QDoubleSpinBox(); field.setRange(-1e9,1e9); field.setValue(value)
                        details_form.addRow(axis,field)
                elif label == 'Pick edge / axis': details_form.addRow('Reference',self.reference('Pick an edge or axis'))
                elif label == 'Two points':
                    details_form.addRow('From',self.reference('Pick start point'))
                    details_form.addRow('To',self.reference('Pick end point'))
                details.setVisible(details_form.rowCount() > 0)
            self.direction.currentTextChanged.connect(show_direction); show_direction('Parent X')
            form.addRow('Distance', self.quantity(20))
            form.addRow(QtWidgets.QCheckBox('Reverse direction'))
            guidance = 'Preview moves 2 components together. Apply commits one move.'
        elif method == 'Point to point':
            form.addRow('From', self.reference('Motor · vertex'))
            form.addRow('To', self.reference('Drive unit · origin'))
            note = QtWidgets.QLabel('Move the source point onto the destination. Keep orientation.')
            note.setWordWrap(True); form.addRow(note)
            guidance = 'Both reference points are ready for preview.'
        elif method == 'Axis and angle':
            form.addRow('Axis', self.combo(['Parent Z', 'Parent X', 'Parent Y', 'Pick edge / axis', 'Two points']))
            form.addRow('Pivot', self.reference('Parent origin'))
            form.addRow('Angle', self.quantity(30, 'deg'))
            form.addRow(QtWidgets.QCheckBox('Reverse rotation'))
            guidance = 'Rotate the group about the displayed axis and pivot.'
        elif method == 'Dynamic drag':
            form.addRow('Control', self.combo(['Components', 'Pivot only']))
            form.addRow('Pivot', self.reference('Selection center · parent axes'))
            form.addRow(QtWidgets.QPushButton('Reset pivot'))
            rotating = self.kind.currentText() == 'Rotate'
            form.addRow('Active handle', self.combo(['Z rotation ring', 'X rotation ring', 'Y rotation ring'] if rotating else
                                                  ['X arrow', 'Y arrow', 'Z arrow', 'XY plane', 'YZ plane', 'ZX plane']))
            form.addRow('Angle' if rotating else 'Distance', self.quantity(30 if rotating else 20, 'deg' if rotating else 'mm'))
            row = QtWidgets.QHBoxLayout(); row.addWidget(QtWidgets.QCheckBox('Snap angle' if rotating else 'Snap distance'))
            row.addWidget(self.quantity(15 if rotating else 1, 'deg' if rotating else 'mm')); form.addRow(row)
            guidance = ('Drag a rotation ring in the view.' if rotating else 'Drag an arrow or plane in the view.') + '\nRelease keeps the preview. Escape cancels the current drag.'
        elif method == 'Axes':
            form.addRow('Source axis', self.reference('Motor · shaft axis'))
            form.addRow('Target axis', self.reference('Coupling · bore axis'))
            form.addRow('Alignment', self.combo(['Coincident', 'Parallel']))
            form.addRow(QtWidgets.QCheckBox('Reverse target direction'))
            guidance = 'Align direction; Coincident also aligns the axis locations.'
        else:
            form.addRow('Source frame', self.reference('Motor · coordinate system'))
            form.addRow('Target frame', self.reference('Drive unit · coordinate system'))
            advanced = QtWidgets.QToolButton(); advanced.setText('Define origin and axes…'); advanced.setCheckable(True)
            form.addRow(advanced)
            details = QtWidgets.QWidget(); definitions = QtWidgets.QFormLayout(details)
            for frame in ('Source','Target'):
                for reference in ('origin','Z axis','X axis'):
                    definitions.addRow(frame+' '+reference,self.reference('Pick '+reference))
            form.addRow(details); details.hide(); advanced.toggled.connect(details.setVisible)
            guidance = 'Align the origin and all three axes, including roll.'
        self.status.setText(guidance)

    def show_blocked(self):
        self.status.setError('This component is fixed by an assembly constraint. Edit its constraint before repositioning it.')
        for buttons in Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox):
            for role in (QtWidgets.QDialogButtonBox.Apply,QtWidgets.QDialogButtonBox.Ok):
                button = buttons.button(role)
                if button: button.setEnabled(False)

    def getStandardButtons(self):
        return QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
    def clicked(self, button): self.status.setText('UI preview only — no placement was changed.')
    def accept(self): Gui.Control.closeDialog(); return True
    def reject(self): Gui.Control.closeDialog(); return True
    def isAllowedAlterSelection(self): return True
    def isAllowedAlterView(self): return True
    def isAllowedAlterDocument(self): return False

def open_task(panel, rows):
    task = MoveTask(panel, rows); Gui.Control.showDialog(task); return task
