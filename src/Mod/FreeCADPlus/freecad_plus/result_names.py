# SPDX-License-Identifier: LGPL-2.1-or-later
"""Draft result labels. Object identities and geometry references never change."""
from PySide6 import QtCore, QtWidgets


def checked(value):
    value = value.strip()
    if not value:
        raise ValueError('Enter a result name.')
    if any(ord(char) < 32 for char in value):
        raise ValueError('Use a single line for the result name.')
    return value


def assign(obj, value):
    if value is not None:
        value = checked(value)
        obj.Label = value
        if obj.Label != value:
            raise ValueError('The result name is already used. Choose another name.')


def defaults(owner, bases, *, style='native', exclude=()):
    used = {o.Label for o in owner.Document.Objects if o not in exclude}
    # Native object creation also reserves internal names, even after a rename.
    if style == 'native':used.update(o.Name for o in owner.Document.Objects if o not in exclude)
    result = []
    for base in bases:
        if style == 'mesh':
            base = owner.Label + '_Mesh';index = 1
            name = base + f'{index:03d}'
            while name in used:index += 1;name = base + f'{index:03d}'
        elif style == 'derived':
            name = base;index = 2
            while name in used:name = base + f' ({index})';index += 1
        else:
            name = base;index = 1
            while name in used:name = base + f'{index:03d}';index += 1
        used.add(name);result.append(name)
    return result


class Names(QtWidgets.QWidget):
    """Keep drafts by stable input key when collectors reorder or recompute."""
    changed = QtCore.Signal()

    def __init__(self, layout, owner, base=None, feature=None, *, style='native', section=False):
        super().__init__()
        self.setObjectName('PlusResultNames')
        self.owner=owner;self.base=base;self.style=style;self.feature=feature
        self.fields={};self.drafts={};self.keys=[]
        self.rows=QtWidgets.QFormLayout(self);self.rows.setContentsMargins(0,0,0,0)
        if section:
            group=QtWidgets.QGroupBox('Preview');box=QtWidgets.QVBoxLayout(group);box.addWidget(self);layout.addWidget(group)
            self.preview_layout=box
        else:layout.addWidget(self);self.preview_layout=layout
        if base is not None:self.reset(feature)

    @property
    def field(self):return self.fields[self.keys[0]]

    def reset(self, feature=None):
        self.feature=feature;self.drafts.clear()
        value=feature.Label if feature else defaults(self.owner,[self.base],style=self.style)[0]
        self.sync([('result','Result name',value)])

    def sync(self, entries):
        keys=[key for key,_,_ in entries]
        if keys == self.keys:
            for key,title,value in entries:
                if key not in self.drafts:
                    blocker=QtCore.QSignalBlocker(self.fields[key]);self.fields[key].setText(value);del blocker
                self.rows.labelForField(self.fields[key]).setText(title)
            return
        while self.rows.rowCount():self.rows.removeRow(0)
        self.fields={};self.keys=keys
        for key,title,value in entries:
            field=QtWidgets.QLineEdit(self.drafts.get(key,value));field.setObjectName('PlusResultName')
            field.setAccessibleName(title);self.rows.addRow(title,field);self.fields[key]=field
            field.textChanged.connect(lambda text,key=key:self.edited(key,text))

    def edited(self,key,text):
        self.drafts[key]=text;self.changed.emit()

    def values(self):
        result=[]
        for key in self.keys:
            try:result.append(checked(self.fields[key].text()))
            except ValueError:
                self.fields[key].setFocus();raise
        return result

    def value(self):return self.values()[0]


def add_before(form, owner, base, feature, before, *, style='native'):
    """Add a Preview group immediately before an existing status/preview widget."""
    layout=form.layout();index=layout.indexOf(before)
    names=Names(layout,owner,base,feature,style=style,section=True)
    group=names.parentWidget();layout.removeWidget(group);layout.insertWidget(index,group)
    return names


def native_open(contents, feature=None):
    """Native task bridge, called only in a component document by TaskView."""
    import FreeCADGui as Gui
    from . import derived_geometry, document
    if not contents or any(w.findChild(QtWidgets.QWidget,'PlusResultNames') for w in contents):return
    if feature is None:
        edit=Gui.activeDocument().getInEdit() if Gui.activeDocument() else None
        feature=edit.Object if edit else None
    if feature is None:
        native_create(contents)
        return
    try:owner=derived_geometry.owner(feature)
    except ValueError:return
    if owner is None or feature not in document.history(owner.Document,owner):return
    # Reuse the native Part Design Preview box, including dress-ups and holes.
    preview=next((w.findChild(QtWidgets.QCheckBox,'showFinalCheckBox') for w in contents
                  if w.findChild(QtWidgets.QCheckBox,'showFinalCheckBox')),None)
    container=preview.parentWidget() if preview else contents[-1]
    layout=container.layout()
    if layout is None:return
    names=Names(layout,owner,feature.Label,feature,section=preview is None)
    names.native_host=container
    names.native_contents=contents
    names.setProperty('PlusNativeNames',True)
    if preview and isinstance(layout,QtWidgets.QBoxLayout):
        layout.removeWidget(names);layout.insertWidget(0,names)
    from .task_status import TaskStatus
    names.status=TaskStatus();names.rows.addRow(names.status)


def native_accept(contents):
    """Validate before native acceptance; label writes share its pending Undo."""
    for root in contents:
        for names in root.findChildren(Names):
            if not names.property('PlusNativeNames'):continue
            try:
                feature=names.feature
                if feature is None:
                    names.value();continue
                if feature.Document.getObject(feature.Name)!=feature:raise ValueError('The result is no longer available.')
                if not feature.Document.HasPendingTransaction:raise ValueError('Reopen this feature before changing its name.')
                assign(feature,names.value());names.status.setText('')
            except (ValueError,RuntimeError,ReferenceError) as error:
                names.status.setError(str(error));return False
    return True


def native_create(contents):
    from . import editing
    import FreeCAD as App
    primitives=next((w.findChild(QtWidgets.QComboBox,'PrimitiveTypeCB') for w in contents
                     if w.findChild(QtWidgets.QComboBox,'PrimitiveTypeCB')),None)
    boolean=next((w for root in contents for w in root.findChildren(QtWidgets.QWidget)
                  if w.findChild(QtWidgets.QRadioButton,'unionButton') and w.findChild(QtWidgets.QTreeWidget,'firstShape')),None)
    if not primitives and not boolean:return
    owner,_=editing.context_path(App.ActiveDocument)
    names=Names(contents[-1].layout(),owner,section=True)
    names.setProperty('PlusNativeNames',True)
    names.feature=None
    if primitives:
        bases=('Plane','Box','Cylinder','Cone','Sphere','Ellipsoid','Torus','Prism','Wedge','Helix','Spiral','Circle','Ellipse','Vertex','Line','Polygon')
        names.seed=lambda:bases[primitives.currentIndex()]
        primitives.currentIndexChanged.connect(lambda:native_refresh(names))
    else:
        names.seed=lambda:next(base for control,base in (('unionButton','Fusion'),('interButton','Common'),('diffButton','Cut'),('sectionButton','Section'))
                               if boolean.findChild(QtWidgets.QRadioButton,control).isChecked())
        for radio in boolean.findChildren(QtWidgets.QRadioButton):radio.toggled.connect(lambda:native_refresh(names))
    native_refresh(names)
    from .task_status import TaskStatus
    names.status=TaskStatus();names.rows.addRow(names.status)


def native_refresh(names):
    names.base=names.seed()
    names.sync([('result','Result name',defaults(names.owner,[names.base])[0])])


def native_created(obj):
    """Called by native create dialogs before their existing commit."""
    import FreeCADGui as Gui
    dock=Gui.getMainWindow().findChild(QtWidgets.QDockWidget,'Tasks')
    if dock:
        for names in dock.findChildren(Names):
            if names.property('PlusNativeNames') and names.feature is None and names.owner.Document==obj.Document:
                assign(obj,names.value());names.drafts.clear();native_refresh(names);return
