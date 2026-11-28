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


# Isolated UI prototype: defaults are in memory, Apply only resets controls.
InstalledMeshForm=MeshForm
class MeshForm(InstalledMeshForm):
    revised=True
    def __init__(self,tessellation):
        super().__init__(tessellation)
        inputs=self.sources.parentWidget().layout();pick=inputs.takeAt(1).layout()
        while pick.count():
            item=pick.takeAt(0)
            if item.widget():item.widget().hide()
        self.method.setCurrentIndex(0);self.method_default=0
        self.layout().removeWidget(self.tess)
        self.advanced_dialog=QtWidgets.QDialog(self);self.advanced_dialog.setWindowTitle('Advanced mesh settings')
        self.advanced_dialog.setModal(True)
        self.advanced_dialog.setStyleSheet('QDialog { background: #efefef; color: #000000; }')
        popup=QtWidgets.QVBoxLayout(self.advanced_dialog)
        models=QtWidgets.QGroupBox('Meshing model');choices=QtWidgets.QHBoxLayout(models);self.radios=[]
        for index,name in enumerate(('Standard','Mefisto','Netgen','Gmsh')):
            radio=QtWidgets.QRadioButton(name);radio.setEnabled(self.method.isTabEnabled(index))
            radio.toggled.connect(lambda checked,i=index:self.method.setCurrentIndex(i) if checked else None)
            choices.addWidget(radio);self.radios.append(radio)
        self.radios[0].setChecked(True);popup.addWidget(models)
        self.method.tabBar().hide()
        self.tess.findChild(QtWidgets.QGroupBox,'groupBoxMeshingOptions').setTitle('Default settings')
        popup.addWidget(self.tess)
        note=QtWidgets.QLabel('Use these settings for this mesh and as defaults for new meshes.');note.setWordWrap(True);popup.addWidget(note)
        actions=QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel);popup.addWidget(actions)
        actions.accepted.connect(self.advanced_dialog.accept);actions.rejected.connect(self.advanced_dialog.reject)
        self.advanced_dialog.accepted.connect(self.accept_advanced);self.advanced_dialog.rejected.connect(self.cancel_advanced)
        self.basics=QtWidgets.QGroupBox('Mesh settings');self.fields=QtWidgets.QFormLayout(self.basics)
        self.layout().insertWidget(2,self.basics)
        self.advanced=QtWidgets.QPushButton('Advanced settings…');self.advanced.clicked.connect(self.open_advanced)
        self.saved_defaults=self.state();self.render_fields()

    def update_hint(self):
        self.hint.setText('Select solids or surfaces in the view or History. Shift-click removes; Delete removes list rows.')

    def native(self,name):return self.tess.findChild(QtWidgets.QWidget,name)

    def state(self):
        values=[]
        for w in self.tess.findChildren(QtWidgets.QWidget):
            if isinstance(w,QtWidgets.QCheckBox):values.append((w,'checked',w.isChecked()))
            elif isinstance(w,QtWidgets.QComboBox):values.append((w,'currentIndex',w.currentIndex()))
            elif isinstance(w,QtWidgets.QAbstractSpinBox):
                prop='rawValue' if w.metaObject().indexOfProperty('rawValue')>=0 else 'value'
                values.append((w,prop,w.property(prop)))
            elif w.objectName()=='fileChooser':values.append((w,'fileName',w.property('fileName')))
        return values,self.method.currentIndex()

    def restore(self,state):
        values,index=state
        for widget,prop,value in values:widget.setProperty(prop,value)
        self.method.setCurrentIndex(index);self.radios[index].setChecked(True)

    def open_advanced(self):
        self.draft_before=self.state();self.radios[self.method.currentIndex()].setChecked(True)
        self.advanced_dialog.resize(510,490);self.advanced_dialog.open()

    def accept_advanced(self):
        self.saved_defaults=self.state();self.render_fields()

    def cancel_advanced(self):
        self.restore(self.draft_before);self.render_fields()

    def number(self,name,label,suffix=''):
        native=self.native(name);spin=QtWidgets.QDoubleSpinBox()
        prop='rawValue' if native.metaObject().indexOfProperty('rawValue')>=0 else 'value'
        spin.setDecimals(3);spin.setRange(float(native.property('minimum')),float(native.property('maximum')))
        spin.setSuffix(suffix);spin.setValue(float(native.property(prop)));spin.setEnabled(native.isEnabled())
        spin.valueChanged.connect(lambda value:native.setProperty(prop,value));self.controls[name]=spin;self.fields.addRow(label,spin)

    def combo(self,name,label):
        native=self.native(name);combo=QtWidgets.QComboBox()
        combo.addItems([native.itemText(i) for i in range(native.count())]);combo.setCurrentIndex(native.currentIndex())
        combo.currentIndexChanged.connect(native.setCurrentIndex)
        combo.currentIndexChanged.connect(self.refresh_enabled);self.controls[name]=combo;self.fields.addRow(label,combo)

    def checkbox(self,name,label):
        native=self.native(name);check=QtWidgets.QCheckBox(label);check.setChecked(native.isChecked())
        check.toggled.connect(native.setChecked);check.toggled.connect(self.refresh_enabled)
        self.controls[name]=check;self.fields.addRow(check)

    def refresh_enabled(self,*args):
        for name,widget in self.controls.items():widget.setEnabled(self.native(name).isEnabled())

    def render_fields(self):
        self.advanced.setParent(self)
        while self.fields.count():
            item=self.fields.takeAt(0)
            if item.widget():item.widget().deleteLater()
        self.controls={};index=self.method.currentIndex()
        if index==0:
            self.number('spinSurfaceDeviation','Linear deviation',' mm')
            self.number('spinAngularDeviation','Angular deviation','°')
        elif index==1:
            self.checkbox('checkMaximumEdgeLength','Limit edge length')
            self.number('spinMaximumEdgeLength','Maximum edge length',' mm')
        elif index==2:
            self.combo('comboFineness','Fineness')
            self.number('doubleGrading','Mesh size grading')
            self.number('spinEdgeElements','Elements per edge')
            self.number('spinCurvatureElements','Elements per curvature radius')
            self.checkbox('checkOptimizeSurface','Optimize surface')
            self.checkbox('checkSecondOrder','Second order elements')
            self.checkbox('checkQuadDominated','Quad dominated')
        else:
            self.combo('method','Meshing method')
            self.number('minSize','Minimum element size',' mm');self.number('maxSize','Maximum element size',' mm')
        self.fields.addRow(self.advanced);self.advanced.show()

    def reset(self):
        self.sources.clear();self.restore(self.saved_defaults);self.render_fields()
