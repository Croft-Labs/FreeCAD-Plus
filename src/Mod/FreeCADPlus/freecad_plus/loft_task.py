# SPDX-License-Identifier: LGPL-2.1-or-later
"""Unified Loft task, sharing target presentation and the feature lifecycle."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets
from pivy import coin
from . import document, extrude_task, loft, modeling, planes
from .plane_task import buttons


class LoftTask(extrude_task.ExtrudeTask):
    engine = loft
    title = 'Loft'
    icon = 'PartDesign_AdditiveLoft'
    selection_noun = 'sections'

    def configure_form(self):
        self.profile.header.setText('Sections')
        self.start.hide();self.extent.hide();self.advanced.hide()
        self.fields = {'target': self.fields['target']};self.numbers = [];self.values = {}
        for button in self.profile.findChildren(QtWidgets.QPushButton):button.hide()
        buttons(self.profile.layout, [('Up', lambda:self.move_section(-1)), ('Down', lambda:self.move_section(1)),
                                      ('Remove', self.remove_profile), ('Clear', self.clear_profile)])
        self.profiles.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.profiles.model().rowsMoved.connect(self.sections_moved)
        layout = self.form.layout();self.options = self.section(layout, 'Loft options')
        layout.removeWidget(self.options);layout.insertWidget(layout.indexOf(self.preview), self.options)
        self.ruled = QtWidgets.QCheckBox('Ruled surface');self.closed_loft = QtWidgets.QCheckBox('Closed')
        self.closed_loft.setToolTip('Connect the last section back to the first. This does not cap a sheet.')
        for control in (self.ruled, self.closed_loft, self.refine):
            self.options.layout.addWidget(control);control.show()
        self.ruled.toggled.connect(self.changed);self.closed_loft.toggled.connect(self.changed)

    def usable_geometry(self, obj, sheet=False):
        if super().usable_geometry(obj, sheet):return True
        return (obj.isDerivedFrom('Part::Feature') and not obj.TypeId.startswith('Part::Datum')
                and obj.TypeId not in ('PartDesign::Plane', 'PartDesign::Line', 'PartDesign::Point')
                and bool(obj.Shape.Vertexes) and not obj.Shape.Edges)

    def initial_selection(self, which):
        self.entry_error = ''
        raw = [(entry.Object, sub) for entry in Gui.Selection.getSelectionEx('*', 0)
               for sub in entry.SubElementNames or ('',)]
        try:
            for ref in planes.canonical(self.owner, raw):
                obj, sub = ref
                if not sub and hasattr(obj, 'Shape') and obj.Shape.Solids and not obj.isDerivedFrom('Sketcher::SketchObject'):
                    target = obj.Tip if obj.TypeId == 'PartDesign::Body' else obj
                    modeling._target_body(self.owner, target)
                    if self.links.get('target', (target, ''))[0] != target:raise ValueError('Select one target solid.')
                    self.links['target'] = (target, '')
                else:
                    ref = loft.profile_reference(ref)
                    # Preserve open sections on entry so Sheet can be selected.
                    loft.validate_profiles(self.owner, [ref], 'Sheet')
                    if ref not in self.refs:self.refs.append(ref)
        except Exception as exc:self.entry_error = str(exc)
        self.modes['Subtract' if which == 'SubtractiveLoft' else 'Add' if which == 'AdditiveLoft' else 'New Solid'].setChecked(True)

    def settings(self):
        return dict(output=self.output(), operation=self.mode(), ruled=self.ruled.isChecked(),
                    closed=self.closed_loft.isChecked(), refine=self.refine.isChecked())

    def load_feature(self, feature):
        self.refs = planes.flatten(feature.ProfileReferences);self.links = loft.references(feature)
        values = loft.settings(feature)
        self.outputs[values['output']].setChecked(True);self.modes[values['operation']].setChecked(True)
        self.ruled.setChecked(values['ruled']);self.closed_loft.setChecked(values['closed']);self.refine.setChecked(values['refine'])

    def refresh_fields(self):
        super().refresh_fields()
        for i, ref in enumerate(self.refs):self.profiles.item(i).setData(QtCore.Qt.UserRole, i)

    def move_section(self, delta):
        row = self.profiles.currentRow();other = row + delta
        if row < 0 or not 0 <= other < len(self.refs):return
        self.refs[row], self.refs[other] = self.refs[other], self.refs[row]
        self.refresh_fields();self.profiles.setCurrentRow(other);self.changed()

    def sections_moved(self, *args):
        order = [self.profiles.item(i).data(QtCore.Qt.UserRole) for i in range(self.profiles.count())]
        self.refs = [self.refs[i] for i in order]
        self.refresh_fields();self.changed()

    def update_output(self):
        super().update_output()
        sheet = self.output() == 'Sheet'
        self.profile_hint.setText(('Select open or closed section curves in loft order.' if sheet else
                                  'Select closed section profiles in loft order.') + ' Drag rows or use Up / Down to reorder.')
        with QtCore.QSignalBlocker(self.display):self.display.setItemText(0, 'Loft preview' if sheet else 'Tool volume')

    def changed(self, *args):
        if not self.ready or self.closed:return
        self.update_output();self.presentation.update_usable();self.update_target();self.presentation.update_style()
        if self.automatic.isChecked():self.render()
        else:
            self.clear_overlay();self.status.setText('Preview needs update.');self.set_ok(self.target_ready())
        self.refresh_target()

    def pick_region(self, callback):
        pass  # Section picks append profiles instead of replacing a sketch region.

    def highlight_profile(self):
        super().highlight_profile()
        if self.profile_highlight is None:return
        # Native Loft accepts vertex endpoints. Show those selected points even
        # when editing hides their donor geometry; edge highlighting has no ink
        # for a vertex-only section. Respect explicit eye choices as for curves.
        points = []
        for ref in self.refs:
            if ref[0] in self.presentation.manual and not self.presentation.desired.get(ref[0]):continue
            if not self.feature and not all(obj.Visibility for obj in document.owned_path(self.owner, ref[0])):continue
            shape = planes.shape(self.owner, ref)
            if shape.ShapeType == 'Vertex':points.append(tuple(self.world.multVec(shape.Point)))
        if points:
            style = coin.SoDrawStyle();style.pointSize = 5;self.profile_highlight.addChild(style)
            coords = coin.SoCoordinate3();coords.point.setValues(0, len(points), points);self.profile_highlight.addChild(coords)
            node = coin.SoPointSet();node.numPoints = len(points);self.profile_highlight.addChild(node)

    def addSelection(self, doc, name, sub, *args):
        if self.closed:return
        if self.pick != 'profile':return super().addSelection(doc, name, sub, *args)
        try:
            self.check()
            if not self.require_target():
                Gui.Selection.removeSelection(doc, name, sub);return
            ref = loft.profile_reference(planes.canonical(self.owner, [(App.getDocument(doc).getObject(name), sub)])[0])
            document.require_predecessors(self.owner, self.feature, [ref])
            loft.validate_profiles(self.owner, [ref], self.output())
            if ref in self.refs:self.refs.remove(ref)
            else:self.refs.append(ref)
            self.refresh_fields();self.changed();Gui.Selection.removeSelection(doc, name, sub)
        except Exception as exc:self.status.setError(str(exc))


def show(feature=None, which='Loft'):
    if Gui.Control.activeDialog():raise ValueError('Finish the current task first.')
    if feature is not None and not loft.is_loft(feature):raise ValueError('This feature uses the native editor.')
    task = LoftTask(feature, which);extrude_task._active = task
    Gui.Control.showDialog(task);task.changed()
    if getattr(task, 'entry_error', ''):task.status.setError(task.entry_error)
    from . import panel
    panel.begin_feature_task(task)
    return task


def dispatch(which):
    modeling._context(Gui.activeDocument().Document)
    show(which=which)
    return True


class Command:
    def GetResources(self):
        return dict(MenuText='Loft', ToolTip='Loft ordered sections into a solid or sheet', Pixmap='PartDesign_AdditiveLoft')

    def IsActive(self):return Gui.activeDocument() is not None and not Gui.Control.activeDialog()

    def Activated(self):
        try:
            if not any('PlusFormat' in obj.PropertiesList for obj in Gui.activeDocument().Document.Objects):
                Gui.runCommand('PartDesign_AdditiveLoft');return
            show()
        except Exception as exc:
            from .thicken_task import show_error
            show_error('Loft', str(exc))


def install():Gui.addCommand('FreeCADPlus_Loft', Command())
