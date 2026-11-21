# SPDX-License-Identifier: LGPL-2.1-or-later
"""Approved New Plane task; model changes occur only on acceptance."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets
from pivy import coin
from . import planes, modeling, editing, hierarchy

_active = None


class Section(QtWidgets.QWidget):
    def __init__(self, title, expanded=True):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 3, 0, 3)
        self.header = QtWidgets.QToolButton()
        self.header.setText(title)
        font = self.header.font(); font.setBold(True); self.header.setFont(font)
        self.header.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.header.setAutoRaise(True)
        self.header.setCheckable(True)
        self.header.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.content = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(self.content)
        self.layout.setContentsMargins(8, 2, 0, 4)
        self.layout.setSpacing(6)
        self.summary = QtWidgets.QLabel()
        self.summary.setWordWrap(True)
        self.summary.hide()
        layout.addWidget(self.header); layout.addWidget(self.summary); layout.addWidget(self.content)
        self.header.toggled.connect(self.expand)
        self.header.setChecked(expanded)
        self.expand(expanded)

    def expand(self, opened):
        self.content.setVisible(opened)
        self.header.setArrowType(QtCore.Qt.DownArrow if opened else QtCore.Qt.RightArrow)


def label(text):
    widget = QtWidgets.QLabel(text); widget.setWordWrap(True)
    return widget


def buttons(layout, entries):
    row = QtWidgets.QHBoxLayout()
    for text, callback in entries:
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(callback); row.addWidget(button)
    layout.addLayout(row)


class DeferredNumber(QtWidgets.QDoubleSpinBox):
    committed = QtCore.Signal()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.committed.emit()


def number(layout, title, value=0, suffix=' mm'):
    row = QtWidgets.QHBoxLayout()
    row.addWidget(QtWidgets.QLabel(title))
    field = DeferredNumber()
    field.setKeyboardTracking(False)
    field.setRange(-100000, 100000); field.setDecimals(2)
    field.setValue(value); field.setSuffix(suffix)
    row.addWidget(field, 1); layout.addLayout(row)
    return field


class PlaneTask(QtCore.QObject):
    def __init__(self, feature=None):
        super().__init__()
        self.doc = Gui.activeDocument().Document
        self.definition, self.path = modeling._context(self.doc)
        self.source_doc = self.definition.Document
        self.context = modeling._routing_context(self.doc, self.definition, self.path)
        self.view = Gui.activeDocument().activeView()
        self.feature = feature
        self.closed = False
        self.pick_target = 'plane'
        self.refs = []
        self.origin_refs = []
        self.axis_refs = []
        self.valid = False
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle('New Plane')
        self.form.setWindowIcon(Gui.getIcon('PartDesign_Plane'))
        layout = QtWidgets.QVBoxLayout(self.form)
        layout.setContentsMargins(6, 4, 6, 4); layout.setSpacing(4)
        layout.addWidget(label('Component: ' + self.definition.Label))
        self.plane = Section('Plane orientation and location')
        layout.addWidget(self.plane)
        self.plane.layout.addWidget(label('Select defining geometry in the model or History.'))
        self.reference_ui = QtWidgets.QWidget()
        refs = QtWidgets.QVBoxLayout(self.reference_ui); refs.setContentsMargins(0,0,0,0)
        self.references = QtWidgets.QListWidget(); self.references.setFixedHeight(60)
        refs.addWidget(self.references)
        buttons(refs, [('Remove', self.remove_reference), ('Clear', self.clear)])
        quick = QtWidgets.QHBoxLayout(); quick.addWidget(QtWidgets.QLabel('Origin plane:'))
        for text in ('XY', 'XZ', 'YZ'):
            button = QtWidgets.QToolButton(); button.setText(text)
            button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            button.clicked.connect(lambda checked=False, text=text: self.choose(text + ' Plane'))
            quick.addWidget(button)
        refs.addLayout(quick)
        self.plane.layout.addWidget(self.reference_ui)
        self.status = label('Under-defined — select geometry to define a plane.')
        self.plane.layout.addWidget(self.status)
        self.offset = number(self.plane.layout, 'Offset')
        reverse = QtWidgets.QPushButton('Reverse offset')
        reverse.clicked.connect(self.reverse_offset)
        self.plane.layout.addWidget(reverse)
        self.frame = Section('Origin and Orientation', False); layout.addWidget(self.frame)
        self.frame.layout.addWidget(label('Origin point'))
        origin_row = QtWidgets.QHBoxLayout()
        self.origin_ref = QtWidgets.QLineEdit(); self.origin_ref.setReadOnly(True)
        self.origin_ref.setPlaceholderText('Select a point')
        self.origin_ref.setToolTip('Select a point in the model or History')
        origin_row.addWidget(self.origin_ref, 1)
        clear_origin = QtWidgets.QPushButton('Clear'); clear_origin.clicked.connect(self.clear_origin)
        origin_row.addWidget(clear_origin); self.frame.layout.addLayout(origin_row)
        self.origin_hint = label('No point selected: universal origin projected onto the plane.')
        self.frame.layout.addWidget(self.origin_hint)
        axis_row = QtWidgets.QHBoxLayout(); axis_row.addWidget(QtWidgets.QLabel('Define axis:'))
        self.x_choice = QtWidgets.QRadioButton('X'); self.x_choice.setChecked(True)
        self.y_choice = QtWidgets.QRadioButton('Y')
        axis_row.addWidget(self.x_choice); axis_row.addWidget(self.y_choice); axis_row.addStretch()
        self.frame.layout.addLayout(axis_row)
        self.axis_ref = QtWidgets.QLineEdit(); self.axis_ref.setReadOnly(True)
        self.axis_ref.setPlaceholderText('Select a line, edge, or two points')
        self.frame.layout.addWidget(self.axis_ref)
        self.frame.layout.addWidget(label('Two points define the direction from first to second.'))
        buttons(self.frame.layout, [('Clear axis', self.clear_axis)])
        self.flip = QtWidgets.QPushButton('Flip normal'); self.flip.setCheckable(True)
        self.flip.setToolTip('Reverse the preview Z axis without moving the plane')
        self.frame.layout.addWidget(self.flip)
        self.frame.layout.addWidget(label('Z is normal to the plane; the remaining axis is derived.'))
        self.preview = Section('Preview'); layout.addWidget(self.preview)
        self.visible = QtWidgets.QCheckBox('Show preview'); self.visible.setChecked(True)
        self.automatic = QtWidgets.QCheckBox('Recompute on update'); self.automatic.setChecked(True)
        self.preview.layout.addWidget(self.visible); self.preview.layout.addWidget(self.automatic)
        layout.addStretch()
        self.overlay = None
        self.scene = self.view.getSceneGraph()
        self.committed_offset = 0.0
        self.preview_offset = None
        self.revisions = 0
        self.offset.committed.connect(self.numeric_left)
        self.automatic.toggled.connect(lambda checked: self.update() if checked else None)
        self.x_choice.toggled.connect(self.update)
        self.visible.toggled.connect(self.update)
        self.flip.toggled.connect(self.update)
        for field in (self.references, self.origin_ref, self.axis_ref):
            field.installEventFilter(self)
        if feature is not None:
            self.refs = planes.flatten(feature.PlaneReferences)
            self.origin_refs = planes.flatten(feature.OriginPoint)
            self.axis_refs = planes.flatten(feature.AxisReferences)
            self.offset.setValue(feature.Offset.Value)
            self.committed_offset = feature.Offset.Value
            self.y_choice.setChecked(feature.DefinedAxis == 'Y')
            self.flip.setChecked(feature.FlipNormal)
        else:
            raw = [(entry.Object, sub) for entry in Gui.Selection.getSelectionEx('*',0)
                   for sub in entry.SubElementNames or ('',)]
            try: self.refs = planes.canonical(self.definition, raw)
            except ValueError: pass
        Gui.Selection.addObserver(self)
        App.addDocumentObserver(self)
        editing.add_context_observer(self.context_changed)
        self.refresh_fields()

    def check(self):
        if self.closed or Gui.activeDocument() is None or Gui.activeDocument().activeView() != self.view:
            raise ValueError('Return to the view where this plane task was opened')
        definition, path = modeling._context(self.doc)
        if modeling._routing_context(self.doc, definition, path) != self.context:
            raise ValueError('The edited component changed; start New Plane again')

    def eventFilter(self, obj, event):
        if event.type() in (QtCore.QEvent.FocusIn, QtCore.QEvent.MouseButtonPress):
            self.pick_target = 'origin' if obj is self.origin_ref else ('axis' if obj is self.axis_ref else 'plane')
        return False

    def context_changed(self):
        if self.closed: return
        try: self.check()
        except Exception: self.reject()

    def slotDeletedDocument(self, doc):
        if doc in (self.doc, self.source_doc): self.reject()

    def title(self, ref):
        obj, sub = ref
        return obj.Label + ('.' + sub if sub else '')

    def refresh_fields(self):
        self.references.clear(); self.references.addItems([self.title(ref) for ref in self.refs])
        self.origin_ref.setText(', '.join(self.title(ref) for ref in self.origin_refs))
        self.axis_ref.setText(' → '.join(self.title(ref) for ref in self.axis_refs))
        self.origin_hint.setText('Selected point projected onto the plane.' if self.origin_refs else
                                'No point selected: universal origin projected onto the plane.')

    def clear_origin(self):
        self.origin_refs = []; self.refresh_fields(); self.update()

    def clear_axis(self):
        self.axis_refs = []; self.refresh_fields(); self.update()

    def reverse_offset(self):
        self.offset.setValue(-self.offset.value()); self.numeric_left()

    def numeric_left(self):
        value = self.offset.value()
        if value == self.committed_offset: return
        self.committed_offset = value
        if self.automatic.isChecked(): self.update()

    def addSelection(self, doc_name, obj_name, sub, *args):
        try:
            self.check()
            obj = App.getDocument(doc_name).getObject(obj_name)
            ref = planes.canonical(self.definition, [(obj, sub)])[0]
            kind = planes.describe(self.definition, ref)[0]
            if self.pick_target == 'origin':
                if kind != 'point': raise ValueError('Origin accepts a point only')
                self.origin_refs = [ref]
            elif self.pick_target == 'axis':
                if kind not in ('line','point'): raise ValueError('Select a line, edge or two points')
                if kind == 'line': self.axis_refs = [ref]
                elif ref not in self.axis_refs:
                    if len(self.axis_refs) >= 2 or (self.axis_refs and planes.describe(self.definition,self.axis_refs[0])[0] != 'point'):
                        self.axis_refs = []
                    self.axis_refs.append(ref)
            elif ref not in self.refs:
                self.refs.append(ref)
            self.refresh_fields(); self.update()
        except Exception as exc: self.status.setText(str(exc))

    def removeSelection(self, doc_name, obj_name, sub, *args):
        # Stored defining references persist until Remove/Clear. An origin point
        # explicitly deselected while picking origins restores the default.
        if self.pick_target != 'origin': return
        try:
            obj = App.getDocument(doc_name).getObject(obj_name)
            ref = planes.canonical(self.definition, [(obj, sub)])[0]
            if ref in self.origin_refs: self.clear_origin()
        except Exception: pass

    def clearSelection(self, *args):
        if self.pick_target == 'origin': self.clear_origin()

    def choose(self, name):
        self.pick_target = 'plane'
        role = name.replace(' ', '_')
        self.refs = [(next(obj for obj in self.definition.Origin.OriginFeatures if obj.Role == role), '')]
        self.refresh_fields(); self.update()

    def remove_reference(self):
        row = self.references.currentRow()
        if row >= 0: self.refs.pop(row)
        self.refresh_fields(); self.update()

    def clear(self):
        self.refs = []; self.refresh_fields(); self.update()

    def placement(self):
        self.check()
        for refs in (self.refs, self.origin_refs, self.axis_refs): planes.canonical(self.definition, refs)
        if self.feature is not None and any(obj == self.feature or obj in self.feature.InListRecursive
                                           for obj,sub in self.refs+self.origin_refs+self.axis_refs):
            raise ValueError('A plane cannot depend on itself or a downstream feature')
        return planes.solve(self.definition, self.refs, self.committed_offset, self.origin_refs,
                            self.axis_refs, 'X' if self.x_choice.isChecked() else 'Y', self.flip.isChecked())

    def remove_overlay(self):
        if self.overlay is not None:
            try: self.scene.removeChild(self.overlay)
            except RuntimeError: pass
            self.overlay = None

    def update(self, *args):
        if self.closed: return
        self.remove_overlay()
        try:
            placement = self.placement()
            self.valid = True
            self.status.setText('Defined — plane position and normal are valid.')
        except Exception as exc:
            self.valid = False; self.status.setText(str(exc))
        for box in Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox):
            button = box.button(QtWidgets.QDialogButtonBox.Ok)
            if button and button.isVisible(): button.setEnabled(self.valid)
        if not self.valid or not self.visible.isChecked(): return
        world = hierarchy.world_placement(self.doc, self.path) if self.path else App.Placement()
        placement = world.multiply(placement)
        origin = placement.Base
        x_axis, y_axis, normal = [placement.Rotation.multVec(v) for v in
                                 (App.Vector(1,0,0),App.Vector(0,1,0),App.Vector(0,0,1))]
        self.preview_offset = self.committed_offset
        self.revisions += 1
        self.overlay = coin.SoSeparator()
        material = coin.SoMaterial(); material.diffuseColor = (0.65,0.40,0.85); material.transparency = 0.65
        self.overlay.addChild(material)
        pick = coin.SoPickStyle(); pick.style = coin.SoPickStyle.UNPICKABLE; self.overlay.addChild(pick)
        coordinates = coin.SoCoordinate3()
        left, bottom = planes.bounds('X' if self.x_choice.isChecked() else 'Y', self.flip.isChecked())
        coordinates.point.setValues(0,4,[tuple(origin + x_axis*u + y_axis*v) for u,v in
                                         [(left,bottom),(left+60,bottom),(left+60,bottom+45),(left,bottom+45)]])
        self.overlay.addChild(coordinates)
        face = coin.SoFaceSet(); face.numVertices.setValue(4); self.overlay.addChild(face)
        for title, axis, color in [('X',x_axis,(0.85,0.12,0.12)),('Y',y_axis,(0.1,0.65,0.15)),('Z',normal,(0.15,0.3,0.95))]:
            branch = coin.SoSeparator()
            style = coin.SoDrawStyle(); style.lineWidth = 3; branch.addChild(style)
            ink = coin.SoMaterial(); ink.diffuseColor = color; ink.transparency = 0; branch.addChild(ink)
            vertices = coin.SoCoordinate3(); vertices.point.setValues(0,2,[tuple(origin),tuple(origin+axis*9)])
            branch.addChild(vertices)
            line = coin.SoLineSet(); line.numVertices.setValue(2); branch.addChild(line)
            shift = coin.SoTranslation(); shift.translation = tuple(origin+axis*10); branch.addChild(shift)
            font = coin.SoFont(); font.size = 16; branch.addChild(font)
            caption = coin.SoText2(); caption.string = title; branch.addChild(caption)
            self.overlay.addChild(branch)
        dot = coin.SoSeparator()
        ink = coin.SoMaterial(); ink.diffuseColor = (0.15,0.15,0.15); ink.transparency = 0; dot.addChild(ink)
        shift = coin.SoTranslation(); shift.translation = tuple(origin); dot.addChild(shift)
        sphere = coin.SoSphere(); sphere.radius = 0.45; dot.addChild(sphere)
        self.overlay.addChild(dot)
        self.scene.addChild(self.overlay)

    def getStandardButtons(self):
        return QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

    def accept(self):
        try:
            self.offset.interpretText()
            self.committed_offset = self.offset.value()
            self.placement()
            self.result = planes.save(self.doc, self.refs, self.committed_offset, self.origin_refs,
                                     self.axis_refs, 'X' if self.x_choice.isChecked() else 'Y',
                                     self.flip.isChecked(), self.feature)
            self.reject()
            return True
        except Exception as exc:
            self.status.setText(str(exc)); return False

    def reject(self):
        global _active
        if self.closed: return True
        self.closed = True
        Gui.Selection.removeObserver(self)
        App.removeDocumentObserver(self)
        editing.remove_context_observer(self.context_changed)
        self.remove_overlay()
        Gui.Control.closeDialog()
        _active = None
        return True


def show(feature=None):
    global _active
    if Gui.Control.activeDialog():
        raise ValueError('Finish the current task first')
    _active = PlaneTask(feature)
    Gui.Control.showDialog(_active)
    _active.update()
    return _active
