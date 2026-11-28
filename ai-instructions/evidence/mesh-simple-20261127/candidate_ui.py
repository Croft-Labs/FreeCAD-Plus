# SPDX-License-Identifier: LGPL-2.1-or-later
# Native mesher settings inside the approved persistent collector.
from PySide6 import QtCore,QtWidgets
from freecad_plus.task_status import TaskStatus

class MeshForm(QtWidgets.QGroupBox):
    def __init__(self,tessellation):
        super().__init__()
        self.tess=tessellation;self.closed=None;self.applied=0
        self.setWindowTitle('Mesh From Shape');self.setAutoFillBackground(True)
        layout=QtWidgets.QVBoxLayout(self)
        title=QtWidgets.QLabel('Mesh From Shape');font=title.font();font.setBold(True);font.setPointSize(12);title.setFont(font)
        layout.addWidget(title)
        group=QtWidgets.QGroupBox('Objects to mesh');inputs=QtWidgets.QVBoxLayout(group)
        self.destination=QtWidgets.QLabel('Add to: Active component');inputs.addWidget(self.destination)
        modes=QtWidgets.QHBoxLayout();modes.addWidget(QtWidgets.QLabel('Pick:'))
        self.solid=QtWidgets.QRadioButton('Solid');self.surface=QtWidgets.QRadioButton('Surface');self.solid.setChecked(True)
        modes.addWidget(self.solid);modes.addWidget(self.surface);modes.addStretch();inputs.addLayout(modes)
        self.sources=QtWidgets.QListWidget();self.sources.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.sources.setMinimumHeight(125);self.sources.setMaximumHeight(160);
        inputs.addWidget(self.sources)
        row=QtWidgets.QHBoxLayout();row.addStretch();self.remove=QtWidgets.QPushButton('Remove');self.clear=QtWidgets.QPushButton('Clear')
        row.addWidget(self.remove);row.addWidget(self.clear);inputs.addLayout(row)
        self.hint=QtWidgets.QLabel();self.hint.setWordWrap(True);inputs.addWidget(self.hint)
        self.solid.toggled.connect(self.update_hint);self.update_hint()
        layout.addWidget(group)
        self.tess.findChild(QtWidgets.QCheckBox,'checkBoxDontQuit').hide()
        # Keep the native methods, units and complete parameter widgets.
        # Shrink only the native Standard page's blank spacer for this panel.
        page=self.tess.findChild(QtWidgets.QWidget,'pageStandard')
        for i in range(page.layout().count()):
            item=page.layout().itemAt(i)
            if item.spacerItem():item.spacerItem().changeSize(0,0,QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)
        layout.addWidget(self.tess)
        self.tess.show()
        output=QtWidgets.QLabel('Creates one combined mesh in the active component\'s History. Source geometry is kept.')
        output.setWordWrap(True);layout.addWidget(output)
        self.status=TaskStatus();layout.addWidget(self.status)
        buttons=QtWidgets.QHBoxLayout();buttons.addStretch()
        self.done=QtWidgets.QPushButton('Done');self.apply=QtWidgets.QPushButton('Apply');self.cancel=QtWidgets.QPushButton('Cancel')
        for b in (self.done,self.apply,self.cancel):buttons.addWidget(b)
        layout.addLayout(buttons)
        self.defaults=[]
        for w in self.tess.findChildren(QtWidgets.QWidget):
            if isinstance(w,QtWidgets.QCheckBox):self.defaults.append((w,'checked',w.isChecked()))
            elif isinstance(w,QtWidgets.QComboBox):self.defaults.append((w,'currentIndex',w.currentIndex()))
            elif isinstance(w,QtWidgets.QAbstractSpinBox):self.defaults.append((w,'value',w.property('value')))
        self.method=self.tess.findChild(QtWidgets.QTabWidget,'stackedWidget');self.method_default=self.method.currentIndex()
        self.resize(460,760);self.sync()

    def update_hint(self):
        self.hint.setText(('Click a solid in the view or select its finished body in History.' if self.solid.isChecked()
            else 'Click faces in the view or select a sheet in History.')+' Shift-click removes; Delete removes list rows.')

    def reset(self):
        self.sources.clear();self.solid.setChecked(True)
        for w,prop,value in self.defaults:w.setProperty(prop,value)
        self.method.setCurrentIndex(self.method_default)

    def sync(self):pass


# UI-only candidate. Geometry creation remains the installed implementation.
InstalledMeshForm=MeshForm
class MeshForm(InstalledMeshForm):
    def __init__(self,tessellation):
        super().__init__(tessellation)
        self.method.setCurrentIndex(0);self.method_default=0
        self.layout().removeWidget(self.tess)
        self.advanced_dialog=QtWidgets.QDialog(self)
        self.advanced_dialog.setWindowTitle('Advanced mesh settings')
        self.advanced_dialog.setModal(True)
        self.advanced_dialog.setStyleSheet('QDialog { background: #efefef; color: #000000; }')
        popup=QtWidgets.QVBoxLayout(self.advanced_dialog);popup.addWidget(self.tess)
        actions=QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
        popup.addWidget(actions);actions.accepted.connect(self.advanced_dialog.accept);actions.rejected.connect(self.advanced_dialog.reject)
        self.advanced_dialog.accepted.connect(self.accept_advanced)
        self.advanced_dialog.rejected.connect(self.cancel_advanced)
        self.advanced_dialog.resize(520,540)
        self.native_linear=self.tess.findChild(QtWidgets.QWidget,'spinSurfaceDeviation')
        self.native_angular=self.tess.findChild(QtWidgets.QWidget,'spinAngularDeviation')
        basics=QtWidgets.QGroupBox('Mesh settings');fields=QtWidgets.QFormLayout(basics)
        self.linear=QtWidgets.QDoubleSpinBox();self.linear.setDecimals(3);self.linear.setRange(.001,1e6);self.linear.setSuffix(' mm')
        self.angular=QtWidgets.QDoubleSpinBox();self.angular.setDecimals(2);self.angular.setRange(1,180);self.angular.setSuffix('°')
        fields.addRow('Linear deviation',self.linear);fields.addRow('Angular deviation',self.angular)
        self.advanced=QtWidgets.QPushButton('Advanced settings…')
        row=QtWidgets.QHBoxLayout();row.addStretch();row.addWidget(self.advanced);fields.addRow(row)
        self.layout().insertWidget(2,basics)
        self.linear.valueChanged.connect(lambda value:self.native_linear.setProperty('rawValue',value))
        self.angular.valueChanged.connect(lambda value:self.native_angular.setProperty('rawValue',value))
        self.advanced.clicked.connect(self.open_advanced)
        self.sync_basics()

    def state(self):
        values=[]
        for w in self.tess.findChildren(QtWidgets.QWidget):
            if isinstance(w,QtWidgets.QCheckBox):values.append((w,'checked',w.isChecked()))
            elif isinstance(w,QtWidgets.QComboBox):values.append((w,'currentIndex',w.currentIndex()))
            elif isinstance(w,QtWidgets.QAbstractSpinBox):values.append((w,'value',w.property('value')))
            elif w.objectName()=='fileChooser':values.append((w,'fileName',w.property('fileName')))
        return values,self.method.currentIndex()

    def open_advanced(self):
        self.draft_before=self.state();self.advanced_dialog.open()

    def accept_advanced(self):self.sync_basics()

    def cancel_advanced(self):
        values,index=self.draft_before
        for widget,prop,value in values:widget.setProperty(prop,value)
        self.method.setCurrentIndex(index);self.sync_basics()

    def sync_basics(self):
        for visible,native in ((self.linear,self.native_linear),(self.angular,self.native_angular)):
            value=native.property('value');value=float(value.Value if hasattr(value,'Value') else value)
            with QtCore.QSignalBlocker(visible):visible.setValue(value)
            visible.setEnabled(self.method.currentIndex()==0)
            visible.setToolTip('' if visible.isEnabled() else 'Controlled by Advanced settings.')

    def reset(self):
        super().reset();self.sync_basics()
