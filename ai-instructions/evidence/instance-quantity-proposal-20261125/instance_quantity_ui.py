"""Native presentation-only proposal; no document or placement operations."""
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets


class InstanceTask:
    def __init__(self, edit=False):
        self.edit = edit
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle('Edit instance pattern' if edit else 'Create instances')
        layout = QtWidgets.QVBoxLayout(self.form)
        layout.setContentsMargins(6, 6, 6, 6)
        def note(text):
            label = QtWidgets.QLabel(text); label.setWordWrap(True); return label
        layout.addWidget(note('<b>Add to: Machine</b>'))
        source = QtWidgets.QHBoxLayout()
        source.addWidget(QtWidgets.QLabel('Components: Bolt'))
        source.addStretch(); source.addWidget(QtWidgets.QPushButton('Change parts…'))
        layout.addLayout(source)
        layout.addWidget(note('Update this pattern. Instances outside it stay unchanged.' if edit else
            'Counts include the first new instance. Existing instances stay unchanged.'))
        form = QtWidgets.QFormLayout(); layout.addLayout(form)
        self.mode = QtWidgets.QComboBox(); self.mode.addItems(('Quantity', 'Linear', 'Grid', 'Circular'))
        form.addRow('Arrangement', self.mode)
        self.count = QtWidgets.QSpinBox(); self.count.setRange(1, 10000); self.count.setValue(1)
        form.addRow('Instances per part', self.count)
        self.form_layout = form
        self.pages = QtWidgets.QStackedWidget(); layout.addWidget(self.pages)
        self.fields = {}
        def unit(name, value, unit='mm'):
            field = Gui.UiLoader().createWidget('Gui::InputField')
            field.setProperty('unit', unit); field.setText(str(value)+' '+unit)
            field.setMinimumWidth(80); self.fields[name] = field; return field
        def combo(values):
            box = QtWidgets.QComboBox(); box.addItems(values); return box
        def direction(form, label, values, selected=0):
            box = combo(values); box.setCurrentIndex(selected); form.addRow(label,box)
            reference = QtWidgets.QListWidget(); reference.addItem('Click here, then pick an edge or axis')
            reference.setMaximumHeight(48); form.addRow('Reference',reference)
            vector = QtWidgets.QLineEdit('1, 0, 0'); form.addRow('Vector X, Y, Z',vector)
            def changed(*args):
                form.setRowVisible(reference,box.currentText()=='Pick edge / axis')
                form.setRowVisible(vector,box.currentText()=='Enter vector')
                QtCore.QTimer.singleShot(0,self.resize_page)
            box.currentIndexChanged.connect(changed); changed()
            return box
        def position(form, title, defaults=(0,0,0)):
            row = QtWidgets.QHBoxLayout()
            for axis, value in zip('XYZ', defaults):
                row.addWidget(QtWidgets.QLabel(axis)); row.addWidget(unit(title+axis, value))
            form.addRow(title, row)
        def page(title):
            box = QtWidgets.QGroupBox(title); form = QtWidgets.QFormLayout(box)
            self.pages.addWidget(box); return form
        quantity = page('Placement')
        position(quantity, 'Position')
        quantity.addRow(note('Instances start together at this position. Move or constrain each one afterward.'))
        linear = page('Linear pattern')
        position(linear, 'Start')
        direction(linear,'Direction',('Parent X', 'Parent Y', 'Parent Z', 'Pick edge / axis', 'Enter vector'))
        linear.addRow('Spacing', unit('linear_spacing', 25))
        linear.addRow(QtWidgets.QCheckBox('Reverse direction'))
        grid = page('Grid pattern')
        position(grid, 'Start')
        self.columns = QtWidgets.QSpinBox(); self.columns.setRange(1,1000); self.columns.setValue(3)
        self.rows = QtWidgets.QSpinBox(); self.rows.setRange(1,1000); self.rows.setValue(2)
        grid.addRow('Columns', self.columns)
        direction(grid,'Column direction',('Parent X','Parent Y','Parent Z','Pick edge / axis'))
        grid.addRow('Column spacing', unit('column_spacing',25))
        grid.addRow('Rows', self.rows)
        direction(grid,'Row direction',('Parent X','Parent Y','Parent Z','Pick edge / axis'),1)
        grid.addRow('Row spacing', unit('row_spacing',20))
        circle = page('Circular pattern')
        position(circle, 'Center')
        direction(circle,'Axis',('Parent Z','Parent X','Parent Y','Pick edge / axis'))
        circle.addRow('Radius', unit('radius',50))
        circle.addRow('Start angle', unit('start_angle',0,'deg'))
        self.full = QtWidgets.QCheckBox('Full circle — evenly spaced'); self.full.setChecked(True)
        circle.addRow(self.full)
        self.angle = unit('angular_spacing',60,'deg'); circle.addRow('Angular spacing',self.angle)
        self.angle.setEnabled(False); self.full.toggled.connect(lambda enabled:self.angle.setEnabled(not enabled))
        self.full.toggled.connect(self.refresh)
        circle.addRow('Orientation',combo(('Keep component orientation','Rotate with pattern')))
        circle.addRow(note('The first instance lies on the parent X direction for the shown Z axis. No duplicate at 360°.'))
        layout.addWidget(note('Coordinates and directions are relative to Machine.'))
        self.preview = QtWidgets.QCheckBox('Preview instances'); self.preview.setChecked(True); layout.addWidget(self.preview)
        self.summary = note(''); layout.addWidget(self.summary)
        self.persistence = note(''); layout.addWidget(self.persistence)
        layout.addStretch()
        self.mode.currentIndexChanged.connect(self.refresh)
        self.count.valueChanged.connect(self.refresh); self.columns.valueChanged.connect(self.refresh); self.rows.valueChanged.connect(self.refresh)
        self.refresh()

    def resize_page(self):
        self.pages.setFixedHeight(self.pages.currentWidget().sizeHint().height()+8)

    def refresh(self, *args):
        index = self.mode.currentIndex(); self.pages.setCurrentIndex(index)
        self.form_layout.setRowVisible(1,index != 2)
        count = self.rows.value()*self.columns.value() if index == 2 else self.count.value()
        if self.full.isChecked(): self.angle.setText(str(360.0/self.count.value())+' deg')
        self.summary.setText('<b>'+str(count)+(' instances in pattern' if self.edit else ' new instances')+' · 1 shared component</b>')
        self.persistence.setText('Creates independent placements in one Undo step.' if index == 0 else
            'Saved as an editable pattern. Right-click a member → Edit instance pattern. One Undo step.')
        self.resize_page()

    def getStandardButtons(self):
        return (QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel).value
    def accept(self):
        return False  # Preview-only; never create geometry or links.
    def reject(self):
        Gui.Control.closeDialog(); return True
    def isAllowedAlterDocument(self): return False
    def isAllowedAlterSelection(self): return True
    def isAllowedAlterView(self): return True
