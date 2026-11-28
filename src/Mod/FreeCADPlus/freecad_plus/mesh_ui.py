# SPDX-License-Identifier: LGPL-2.1-or-later
# Native mesher settings inside the approved persistent collector.
from PySide6 import QtCore,QtWidgets
from .task_status import TaskStatus

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
