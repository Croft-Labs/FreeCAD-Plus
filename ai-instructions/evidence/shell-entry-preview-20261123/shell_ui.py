from PySide6 import QtCore,QtWidgets
import FreeCADGui as Gui
from freecad_plus.plane_task import label,buttons
from freecad_plus.task_status import TaskStatus

def proposed():return True

class ShellTask:
    def __init__(self, ui_path):
        self.main=Gui.PySideUic.loadUi(ui_path);self.main.setWindowTitle('Shell');self.main.setWindowIcon(Gui.getIcon('PartDesign_Thickness'))
        self.main.findChild(QtWidgets.QWidget,'Value').setProperty('rawValue',1.0)
        layout=self.main.layout();layout.insertWidget(0,label('Component: Part001'))
        target=QtWidgets.QWidget();row=QtWidgets.QVBoxLayout(target);row.setContentsMargins(0,0,0,0)
        row.addWidget(label('Target solid'));fields=QtWidgets.QHBoxLayout()
        self.target=QtWidgets.QLineEdit();self.target.setReadOnly(True);self.target.setPlaceholderText('Select a solid or pick one of its faces')
        fields.addWidget(self.target,1);clear=QtWidgets.QPushButton('Clear');clear.clicked.connect(self.reset);fields.addWidget(clear);row.addLayout(fields)
        layout.insertWidget(1,target)
        self.status=TaskStatus();layout.insertWidget(2,self.status)
        self.select=self.main.findChild(QtWidgets.QToolButton,'buttonRefSel');self.select.setText('Select faces');self.select.setChecked(True)
        self.faces=self.main.findChild(QtWidgets.QListWidget,'listWidgetReferences')
        self.faces.setFixedHeight(5*(self.faces.fontMetrics().height()+4)+2*self.faces.frameWidth())
        self.faces.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        action_row=QtWidgets.QWidget();actions=QtWidgets.QVBoxLayout(action_row);actions.setContentsMargins(0,0,0,0)
        buttons(actions,[('Remove',self.remove),('Clear faces',self.clear_faces)])
        layout.insertWidget(layout.indexOf(self.faces)+1,action_row)
        self.preview=QtWidgets.QWidget();self.preview.setWindowTitle('Preview')
        options=QtWidgets.QVBoxLayout(self.preview)
        self.final=QtWidgets.QCheckBox('Show final result');options.addWidget(self.final)
        self.overlay=QtWidgets.QCheckBox('Show preview overlay');self.overlay.setChecked(True);options.addWidget(self.overlay)
        self.form=[self.main,self.preview];self.reset()
    def reset(self):
        self.target.clear();self.faces.clear();self.guidance()
    def guidance(self):
        missing=not self.target.text()
        self.target.setStyleSheet('QLineEdit {border: 2px solid #bd780b; border-radius: 3px; background: #fff3d6;}' if missing else '')
        self.status.setText('Select a solid or a face to begin.' if missing else
                            'Select the faces to remove from '+self.target.text()+'.' if not self.faces.count() else
                            'Faces selected. Set the wall thickness and review the preview.')
    def choose_solid(self,name):
        if name!=self.target.text():self.faces.clear()
        self.target.setText(name);self.guidance()
    def choose_face(self,name,face):
        if self.target.text() and name!=self.target.text():
            self.status.setError('This face belongs to another solid. Change Target solid first.');return
        self.target.setText(name);self.faces.addItem(face);self.guidance()
    def ignored_curve(self):
        self.status.setError('Curves cannot define a shell. Select a solid or one of its faces.')
    def ignored_sheet(self):
        self.status.setError('Shell requires a solid. Use Thicken to give a sheet thickness.')
    def clear_faces(self):self.faces.clear();self.guidance()
    def remove(self):
        for item in self.faces.selectedItems():self.faces.takeItem(self.faces.row(item))
        self.guidance()
    def getStandardButtons(self):return int(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
    def accept(self):return False
    def reject(self):Gui.Control.closeDialog();return True
    def isAllowedAlterSelection(self):return True
