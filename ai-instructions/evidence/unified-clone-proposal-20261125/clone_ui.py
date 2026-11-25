"""UI-only Clone/Extract geometry proposal; no geometry or document operations."""
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets
from freecad_plus.task_status import TaskStatus

OBJECTS = [('Bracket / Body','cloned body'),('Cover / Sheet','cloned surface'),
           ('Bracket / Layout','cloned sketch'),('Bracket / Datum plane','cloned plane')]


class GeometryTask:
    def __init__(self, extract=False, edit=False):
        self.extract,self.edit=extract,edit
        self.form=QtWidgets.QWidget();self.form.setWindowTitle('Extract geometry' if extract else 'Clone')
        layout=QtWidgets.QVBoxLayout(self.form);layout.setContentsMargins(6,6,6,6)
        def note(text):
            label=QtWidgets.QLabel(text);label.setWordWrap(True);layout.addWidget(label);return label
        note('<b>Editing component: assy_1</b>')
        if edit:note('Editing: '+('extracted surface' if extract else 'cloned body'))
        note('Select faces on an object owned by assy_1.' if extract else
             'Select whole objects from direct child components.')
        header=QtWidgets.QHBoxLayout();header.addWidget(QtWidgets.QLabel('Faces' if extract else 'Whole objects'))
        header.addStretch()
        if not extract:
            browse=QtWidgets.QPushButton('Browse direct children…');browse.clicked.connect(self.browse);header.addWidget(browse)
        layout.addLayout(header)
        self.objects=QtWidgets.QTreeWidget();self.objects.setColumnCount(2)
        self.objects.setHeaderLabels(['Source face' if extract else 'Source object','Result name'])
        self.objects.setRootIsDecorated(False);self.objects.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.objects.header().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        self.objects.header().setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeToContents)
        self.objects.setMinimumHeight(170);self.objects.setMaximumHeight(200)
        self.objects.setToolTip('Click the list to pick. Click adds; Shift-click removes. Delete removes selected inputs.')
        layout.addWidget(self.objects)
        actions=QtWidgets.QHBoxLayout()
        remove=QtWidgets.QPushButton('Remove');remove.clicked.connect(self.remove)
        clear=QtWidgets.QPushButton('Clear');clear.clicked.connect(lambda:self.populate([]))
        actions.addWidget(remove);actions.addWidget(clear);actions.addStretch();layout.addLayout(actions)
        if extract:
            note('To extract a child component’s face, first clone its whole object into assy_1.')
            note('Creates a separate extracted surface. The cloned body remains available.')
        else:
            note('Bodies, surfaces, sketches and planes are cloned as complete objects. Faces, edges and vertices are not Clone inputs.')
            note('Source construction history stays in the child. Parent features can modify the cloned result or combine it with a parent body.')
        self.preview=QtWidgets.QCheckBox('Show preview');self.preview.setChecked(True);layout.addWidget(self.preview)
        self.update=QtWidgets.QCheckBox('Recompute on update');self.update.setChecked(True);layout.addWidget(self.update)
        note('Updates from the source in the parent coordinate system.' if not extract else
             'Updates from the selected faces on the parent-owned object.')
        self.status=TaskStatus();layout.addWidget(self.status)
        self.summary=note('');layout.addStretch()
        rows=[('cloned body / Face3','extracted surface')] if extract else OBJECTS[:1] if edit else OBJECTS
        self.populate(rows)

    def populate(self,rows):
        self.objects.clear()
        for source,result in rows:QtWidgets.QTreeWidgetItem(self.objects,[source,result])
        self.status.setText('Click the list to add or remove '+('faces.' if self.extract else 'whole objects.'))
        self.summary.setText(('Update existing result' if self.edit else str(len(rows))+' new result'+('s' if len(rows)!=1 else ''))+' · One Undo step')

    def remove(self):
        for item in self.objects.selectedItems():self.objects.takeTopLevelItem(self.objects.indexOfTopLevelItem(item))
        self.summary.setText(str(self.objects.topLevelItemCount())+' new results · One Undo step')

    def browse(self):
        dialog=QtWidgets.QDialog(self.form);dialog.setWindowTitle('Whole objects from direct children');dialog.resize(530,350)
        layout=QtWidgets.QVBoxLayout(dialog);note=QtWidgets.QLabel('Choose objects owned by the direct child occurrences of assy_1.');note.setWordWrap(True);layout.addWidget(note)
        tree=QtWidgets.QTreeWidget();tree.setHeaderLabels(['Child / object','Geometry']);layout.addWidget(tree)
        groups={};types=['Body','Surface','Sketch','Plane']
        for (source,result),kind in zip(OBJECTS,types):
            child,name=source.split(' / ')
            if child not in groups:
                groups[child]=QtWidgets.QTreeWidgetItem(tree,[child+' — occurrence 1',''])
                groups[child].setFlags(QtCore.Qt.ItemIsEnabled);groups[child].setExpanded(True)
            item=QtWidgets.QTreeWidgetItem(groups[child],[name,kind]);item.setData(0,QtCore.Qt.UserRole,(source,result))
            item.setFlags(item.flags()|QtCore.Qt.ItemIsUserCheckable);item.setCheckState(0,QtCore.Qt.Checked)
        tree.header().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        info=QtWidgets.QLabel('Reference children are eligible. Excluded children and deeper component levels are unavailable.');info.setWordWrap(True);layout.addWidget(info)
        buttons=QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel);layout.addWidget(buttons)
        buttons.accepted.connect(dialog.accept);buttons.rejected.connect(dialog.reject)
        if dialog.exec()==QtWidgets.QDialog.Accepted:
            rows=[]
            for group in groups.values():
                for index in range(group.childCount()):
                    item=group.child(index)
                    if item.checkState(0)==QtCore.Qt.Checked:rows.append(item.data(0,QtCore.Qt.UserRole))
            if self.edit and len(rows)!=1:self.status.setError('Choose one whole source object when editing cloned body.')
            else:self.populate(rows)

    def invalid_face(self):
        self.status.setError('A face cannot be cloned. Select its whole body, then use Extract geometry on cloned body to create an extracted surface.')

    def getStandardButtons(self):return (QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel).value
    def accept(self):return False
    def reject(self):Gui.Control.closeDialog();return True
    def isAllowedAlterDocument(self):return False
    def isAllowedAlterSelection(self):return True
    def isAllowedAlterView(self):return True


class PreviewCommand:
    def __init__(self,extract=False):self.extract=extract
    def GetResources(self):
        return {'MenuText':'Extract geometry' if self.extract else 'Clone',
                'ToolTip':'Extract faces from parent-owned geometry' if self.extract else 'Clone whole objects from direct children',
                'Pixmap':'PartDesign_SubShapeBinder' if self.extract else 'PartDesign_ShapeBinder'}
    def IsActive(self):return not bool(Gui.Control.activeDialog())
    def Activated(self):Gui.Control.showDialog(GeometryTask(self.extract))
