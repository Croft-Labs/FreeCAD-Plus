from PySide6 import QtCore, QtGui, QtWidgets
import FreeCADGui as Gui
from freecad_plus.plane_task import Section, label, buttons
from freecad_plus.selection_list import SelectionList
from freecad_plus.task_status import TaskStatus

def configure(tasks):
    # Only this isolated process's action-label widgets change; native commands stay intact.
    for button in tasks.findChildren(QtWidgets.QToolButton):
        name=button.text().replace('&','')
        if name=='Additive Loft':
            action=QtGui.QAction(Gui.getIcon('PartDesign_AdditiveLoft'),'Loft',button)
            button.setDefaultAction(action)
        elif name=='Subtractive Loft':button.hide()
    return True

class LoftTask:
    def __init__(self):
        self.form=QtWidgets.QWidget();self.form.setWindowTitle('Loft');self.form.setWindowIcon(Gui.getIcon('PartDesign_AdditiveLoft'))
        layout=QtWidgets.QVBoxLayout(self.form);layout.setContentsMargins(6,4,6,4);layout.setSpacing(2)
        layout.addWidget(label('Component: Part001'))
        operation=Section('Operation');layout.addWidget(operation)
        self.modes={};self.group=QtWidgets.QButtonGroup(self.form)
        for name in ('New','Add','Subtract'):
            button=QtWidgets.QRadioButton(name);self.group.addButton(button);self.modes[name]=button
            operation.layout.addWidget(button);button.clicked.connect(self.changed)
        self.modes['New'].setChecked(True)
        self.target_row=QtWidgets.QWidget();row=QtWidgets.QVBoxLayout(self.target_row);row.setContentsMargins(0,0,0,0)
        row.addWidget(label('Target solid'));self.target=QtWidgets.QLineEdit();self.target.setReadOnly(True)
        self.target.setPlaceholderText('Select the solid to modify');row.addWidget(self.target)
        self.target_hint=TaskStatus();row.addWidget(self.target_hint);operation.layout.addWidget(self.target_row)
        section=Section('Sections');layout.addWidget(section)
        section.layout.addWidget(label('Select profiles in loft order. Drag rows or use Up / Down to reorder.'))
        self.sections=SelectionList();self.sections.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.sections.addItems(['Sketch · Base profile','Sketch001 · Middle profile','Sketch002 · End profile'])
        section.layout.addWidget(self.sections)
        buttons(section.layout,[('Up',lambda:self.move(-1)),('Down',lambda:self.move(1)),('Remove',self.remove),('Clear',self.sections.clear)])
        self.options=Section('Loft options');layout.addWidget(self.options)
        self.ruled=QtWidgets.QCheckBox('Ruled surface');self.closed=QtWidgets.QCheckBox('Closed')
        self.refine=QtWidgets.QCheckBox('Refine result');self.refine.setChecked(True)
        for control in (self.ruled,self.closed,self.refine):self.options.layout.addWidget(control)
        preview=Section('Preview');layout.addWidget(preview)
        row=QtWidgets.QHBoxLayout();row.addWidget(label('Show'));self.display=QtWidgets.QComboBox();self.display.addItems(['Tool volume','Result'])
        row.addWidget(self.display,1);preview.layout.addLayout(row)
        row=QtWidgets.QHBoxLayout()
        for name in ('Show preview','Recompute on update'):
            control=QtWidgets.QCheckBox(name);control.setChecked(True);row.addWidget(control)
        preview.layout.addLayout(row);preview.layout.addWidget(QtWidgets.QPushButton('Update preview'))
        self.status=TaskStatus();layout.addWidget(self.status);layout.addStretch();self.changed()
    def move(self,delta):
        i=self.sections.currentRow();j=i+delta
        if i>=0 and 0<=j<self.sections.count():
            item=self.sections.takeItem(i);self.sections.insertItem(j,item);self.sections.setCurrentRow(j)
    def remove(self):self.sections.takeItem(self.sections.currentRow())
    def changed(self,*args):
        mode=next(name for name,button in self.modes.items() if button.isChecked())
        self.target_row.setVisible(mode!='New')
        missing=mode!='New' and not self.target.text()
        self.target.setStyleSheet('QLineEdit {border: 2px solid #bd780b; background: #fff3d6; color: #875300;}' if missing else '')
        self.target_hint.setText('Select the target solid before selecting sections.' if missing else '')
        self.status.setText('Tool volume · creates a new solid.' if mode=='New' else 'Select a target solid to preview '+mode.lower()+'.' if missing else 'Tool volume · '+mode.lower()+'.')
    def getStandardButtons(self):return int(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
    def accept(self):return False
    def reject(self):Gui.Control.closeDialog();return True
    def isAllowedAlterSelection(self):return True
