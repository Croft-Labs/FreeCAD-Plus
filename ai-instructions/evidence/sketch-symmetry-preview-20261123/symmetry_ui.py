from PySide6 import QtCore,QtWidgets
from freecad_plus.selection_list import SelectionList
from freecad_plus.task_status import TaskStatus

def proposed():return True

class SymmetryPanel(QtWidgets.QWidget):
    def __init__(self,parent):
        super().__init__(parent);self.pick='geometry';self.invalid=False
        layout=QtWidgets.QVBoxLayout(self);layout.setContentsMargins(0,0,0,0)
        layout.addWidget(QtWidgets.QLabel('Geometry'))
        self.items=SelectionList();self.items.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.items.installEventFilter(self);self.items.viewport().installEventFilter(self)
        layout.addWidget(self.items)
        row=QtWidgets.QHBoxLayout();self.remove=QtWidgets.QPushButton('Remove');self.clear=QtWidgets.QPushButton('Clear')
        row.addWidget(self.remove);row.addWidget(self.clear);layout.addLayout(row)
        self.remove.clicked.connect(self.remove_rows);self.clear.clicked.connect(self.clear_geometry)
        layout.addWidget(QtWidgets.QLabel('Axis of symmetry'))
        self.axis=QtWidgets.QLineEdit();self.axis.setReadOnly(True);self.axis.setPlaceholderText('Select an axis or straight line')
        self.axis.installEventFilter(self);layout.addWidget(self.axis)
        hint=QtWidgets.QLabel('Select a sketch axis or straight line. A point can be used as a symmetry center.');hint.setWordWrap(True);layout.addWidget(hint)
        self.delete=QtWidgets.QCheckBox('Delete original geometries (U)');self.constraints=QtWidgets.QCheckBox('Create symmetry constraints (J)')
        layout.addWidget(self.delete);layout.addWidget(self.constraints)
        self.delete.toggled.connect(lambda on:self.constraints.setChecked(False) if on else None)
        self.constraints.toggled.connect(lambda on:self.delete.setChecked(False) if on else None)
        self.status=TaskStatus('Select geometry, then choose the axis.');layout.addWidget(self.status)
        self.apply=QtWidgets.QPushButton('Apply');self.apply.clicked.connect(self.apply_preview)
        self.done=QtWidgets.QPushButton('Done')
        row=QtWidgets.QHBoxLayout();row.addWidget(self.apply);row.addWidget(self.done);layout.addLayout(row)
        footer=QtWidgets.QLabel('UI preview: selection and Apply are simulated.');footer.setWordWrap(True);layout.addWidget(footer)
        self.sync()

    def eventFilter(self,obj,event):
        if event.type() in (QtCore.QEvent.FocusIn,QtCore.QEvent.MouseButtonPress):
            self.pick='axis' if obj is self.axis else 'geometry';self.sync()
        if event.type()==QtCore.QEvent.KeyPress and event.key()==QtCore.Qt.Key_Delete:
            if obj is self.axis:self.choose_axis('')
            else:self.remove_rows()
            return True
        return False

    def sync(self):
        self.items.setStyleSheet('QListWidget {border:2px solid #347bb7;}' if self.pick=='geometry' else '')
        self.axis.setStyleSheet('QLineEdit {border:2px solid #347bb7;}' if self.pick=='axis' else '')
        self.apply.setEnabled(self.items.count()>0 and bool(self.axis.text()) and not self.invalid)

    def add_geometry(self,name,shift=False):
        found=self.items.findItems(name,QtCore.Qt.MatchExactly)
        if shift:
            for item in found:self.items.takeItem(self.items.row(item))
        elif not found:self.items.addItem(name)
        self.invalid=False;self.status.setText('Click adds geometry; Shift-click removes it.');self.sync()

    def remove_rows(self):
        for item in self.items.selectedItems():self.items.takeItem(self.items.row(item))
        self.sync()

    def clear_geometry(self):
        self.items.clear();self.pick='geometry';self.sync()

    def choose_axis(self,name):
        self.axis.setText(name);self.pick='axis';self.invalid=False
        self.status.setText('Ready to create mirrored geometry.' if name and self.items.count() else 'Select geometry, then choose the axis.')
        self.sync()

    def invalid_axis(self):
        self.invalid=True;self.status.setError('A curved edge cannot define the axis. Select a straight line, sketch axis, or point.');self.sync()

    def apply_preview(self):
        self.clear_geometry();self.status.setText('Apply simulated. Select geometry for another mirror.');self.sync()

def install(dock):
    native=next(w for w in dock.findChildren(QtWidgets.QWidget) if w.metaObject().className().endswith('SketcherToolDefaultWidget'))
    parent=native.parentWidget();layout=parent.layout();native.hide()
    panel=SymmetryPanel(parent);layout.addWidget(panel);panel.show()

    task_names = ('TaskSketcherMessages', 'TaskSketcherConstraints',
                  'TaskSketcherElements', 'TaskSketcherSolverAdvanced')
    panel.hidden_sections = [(w, not w.isHidden()) for w in dock.findChildren(QtWidgets.QWidget)
                             if any(w.metaObject().className().endswith(n) for n in task_names)]
    for widget, was_visible in panel.hidden_sections:
        widget.hide()
    panel.restored = False
    def restore():
        if panel.restored:
            return
        panel.restored = True
        for widget, was_visible in panel.hidden_sections:
            widget.setVisible(was_visible)
        timer.stop()
    timer = QtCore.QTimer(dock)
    timer.setInterval(50)
    timer.timeout.connect(lambda: restore() if not panel.isVisible() else None)
    panel.done.clicked.connect(restore)
    cancel = dock.findChild(QtWidgets.QPushButton, 'SketchCancelAction')
    if cancel:
        cancel.clicked.connect(restore)
    timer.start()
    return panel
