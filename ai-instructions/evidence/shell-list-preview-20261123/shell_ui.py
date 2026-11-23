from PySide6 import QtCore,QtWidgets
import FreeCADGui as Gui
from freecad_plus.plane_task import label
from freecad_plus.task_status import TaskStatus

def proposed():return True

class ShellTask(QtCore.QObject):
    def __init__(self,ui_path):
        super().__init__()
        self.main=Gui.PySideUic.loadUi(ui_path);self.main.setWindowTitle('Shell');self.main.setWindowIcon(Gui.getIcon('PartDesign_Thickness'))
        self.main.findChild(QtWidgets.QWidget,'Value').setProperty('rawValue',1.0)
        layout=self.main.layout();layout.insertWidget(0,label('Component: Part001'))
        native_toggle=self.main.findChild(QtWidgets.QToolButton,'buttonRefSel')
        layout.removeWidget(native_toggle);native_toggle.hide();native_toggle.setParent(None);native_toggle.deleteLater()
        self.faces=self.main.findChild(QtWidgets.QListWidget,'listWidgetReferences')
        self.faces.setFixedHeight(5*(self.faces.fontMetrics().height()+6)+2*self.faces.frameWidth())
        self.faces.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.faces.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.faces.setToolTip('Click this list to select faces in the view. Delete removes highlighted rows.')
        layout.insertWidget(layout.indexOf(self.faces),label('Faces to remove'))
        self.hint=label('');layout.insertWidget(layout.indexOf(self.faces),self.hint)
        self.status=TaskStatus();layout.insertWidget(layout.indexOf(self.faces)+1,self.status)
        actions=QtWidgets.QWidget();row=QtWidgets.QHBoxLayout(actions);row.setContentsMargins(0,0,0,0)
        self.remove_button=QtWidgets.QPushButton('Remove');self.remove_button.clicked.connect(self.remove)
        self.clear_button=QtWidgets.QPushButton('Clear faces');self.clear_button.clicked.connect(self.clear_faces)
        row.addWidget(self.remove_button);row.addWidget(self.clear_button)
        layout.insertWidget(layout.indexOf(self.status)+1,actions)
        self.preview=QtWidgets.QWidget();self.preview.setWindowTitle('Preview');options=QtWidgets.QVBoxLayout(self.preview)
        self.final=QtWidgets.QCheckBox('Show final result');options.addWidget(self.final)
        self.overlay=QtWidgets.QCheckBox('Show preview overlay');self.overlay.setChecked(True);options.addWidget(self.overlay)
        self.form=[self.main,self.preview];self.owner='';self.collecting=False
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.clear_faces();self.activate_list()
    def eventFilter(self,watched,event):
        if watched in (self.faces,self.faces.viewport()):
            if event.type() in (QtCore.QEvent.MouseButtonPress,QtCore.QEvent.FocusIn):self.activate_list()
            if event.type()==QtCore.QEvent.KeyPress and event.key()==QtCore.Qt.Key_Delete:
                self.remove();event.accept();return True
        elif event.type()==QtCore.QEvent.FocusIn and isinstance(watched,QtWidgets.QWidget):
            if watched not in (self.remove_button,self.clear_button) and (self.main.isAncestorOf(watched) or self.preview.isAncestorOf(watched)):
                self.collecting=False;self.update_hint()
        return False
    def activate_list(self):self.collecting=True;self.update_hint()
    def update_hint(self):
        self.faces.setStyleSheet('QListWidget { border: 2px solid #347bb7; }' if self.collecting else '')
        self.hint.setText('Click faces in the view to add them.' if self.collecting else 'Click the face list to add more faces.')
    def guidance(self):
        self.status.setText('Select faces to remove from one solid.' if not self.faces.count() else 'Delete or Remove removes highlighted rows. Clear faces removes all.')
    def choose_face(self,name,face):
        if not self.collecting:return False
        if self.owner and name!=self.owner:
            self.status.setError('Select faces from one solid. Clear faces before choosing a different solid.');return False
        text=name+' - '+face
        if not self.faces.findItems(text,QtCore.Qt.MatchExactly):
            self.owner=name;self.faces.addItem(text);self.faces.setCurrentRow(self.faces.count()-1)
            self.faces.scrollToItem(self.faces.currentItem())
        self.guidance();return True
    def ignored_curve(self):self.status.setError('Select faces of a solid. Curves cannot define a shell.')
    def ignored_sheet(self):self.status.setError('Shell requires solid faces. Use Thicken to give a sheet thickness.')
    def clear_faces(self):self.faces.clear();self.owner='';self.guidance()
    def remove(self):
        for item in self.faces.selectedItems():self.faces.takeItem(self.faces.row(item))
        if not self.faces.count():self.owner=''
        self.guidance()
    def getStandardButtons(self):return int(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
    def accept(self):return False
    def reject(self):
        QtWidgets.QApplication.instance().removeEventFilter(self);Gui.Control.closeDialog();return True
    def isAllowedAlterSelection(self):return True