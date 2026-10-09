# SPDX-License-Identifier: LGPL-2.1-or-later
"""Shared-reference datum plane creation and editing."""
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtWidgets
from freecad.gui.ComponentTaskWidgets import CompactFormLayout, ModelingTaskUI, ReferenceCollector
from freecad.gui.OccurrenceMove import Ghost

_task = None


def tr(text):
    return App.Qt.translate('ComponentPlane', text)


class PlaneTask(QtCore.QObject, ModelingTaskUI):
    def __init__(self, component, operation=None, context=None):
        super().__init__()
        import ComponentPlane as Plane
        self.component, self.operation, self.context = component, operation, context
        self.result = self.ghost = None
        self.observing = False
        self.highlights = []
        self.pick_role = 'plane'
        self.origin_reference = None
        self.original_visibility = operation.Visibility if operation else None
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle(tr('Datum Plane'))
        outer = QtWidgets.QVBoxLayout(self.form)
        self.sections = []
        for title in ('1. Plane orientation and location', '2. Orientation', '3. Origin selection', '4. Preview'):
            section = QtWidgets.QGroupBox(tr(title))
            CompactFormLayout(section)
            outer.addWidget(section)
            self.sections.append(section)
        definition, orientation, origin, preview = [s.layout() for s in self.sections]
        self.mode = self.combo(definition, 'Define plane', [(name, name) for name in ('Select geometry', 'Enter values')])
        origins = {obj.Role: obj for obj in component.Origin.OriginFeatures}
        self.plane_collector = ReferenceCollector(component, [(name.replace('_', ' '), (origins[name], ''))
                                                             for name in ('XY_Plane', 'YZ_Plane', 'XZ_Plane')])
        definition.addRow(self.plane_collector)
        self.numeric = QtWidgets.QWidget()
        numeric = CompactFormLayout(self.numeric)
        numeric.setContentsMargins(0, 0, 0, 0)
        self.position, self.normal = [], []
        for axis in 'XYZ':
            field = self.quantity()
            numeric.addRow(tr(axis + ' offset'), field)
            self.position.append(field)
        for axis, value in zip("XYZ", (0., 0., 1.)):
            field = QtWidgets.QDoubleSpinBox()
            field.setRange(-1e9, 1e9)
            field.setDecimals(8)
            field.setValue(value)
            numeric.addRow(axis.lower() + "'", field)
            self.normal.append(field)
        definition.addRow(self.numeric)
        self.reverse_normal = QtWidgets.QPushButton(tr('Reverse normal direction'))
        self.reverse_normal.setCheckable(True)
        definition.addRow(self.reverse_normal)
        offset_row = QtWidgets.QWidget()
        offset_layout = QtWidgets.QHBoxLayout(offset_row)
        offset_layout.setContentsMargins(0, 0, 0, 0)
        self.offset = self.quantity()
        self.reverse_offset = QtWidgets.QPushButton(tr('Reverse'))
        offset_layout.addWidget(self.offset)
        offset_layout.addWidget(self.reverse_offset)
        definition.addRow(tr('Offset distance'), offset_row)
        self.axis_collector = ReferenceCollector(component, [(axis + ' axis', (origins[axis + '_Axis'], '')) for axis in 'XYZ'])
        orientation.addRow(self.axis_collector)
        self.reverse_axis = QtWidgets.QPushButton(tr('Reverse direction'))
        self.reverse_axis.setCheckable(True)
        orientation.addRow(self.reverse_axis)
        self.origin_field = QtWidgets.QLineEdit()
        self.origin_field.setReadOnly(True)
        self.origin_field.setPlaceholderText(tr('Part origin projected to plane'))
        self.origin_field.setToolTip(tr('Click here, then pick an origin, point or curve endpoint. Delete restores the part origin.'))
        self.origin_field.installEventFilter(self)
        origin.addRow(self.origin_field)
        self.preview_enabled = self.checkbox(preview, 'Preview', True)
        self.automatic = self.checkbox(preview, 'Recompute on update', True)
        self.timer = QtCore.QTimer(self.form)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.preview)
        self.build_status(outer)
        values = Plane.read(operation) if operation else Plane.defaults()
        self.stored_origin = values.get('stored_origin')
        self.stored_axis = values.get('stored_axis')
        self.mode.setCurrentIndex(self.mode.findData(values['mode']))
        self.plane_collector.set_references(values['references'])
        self.axis_collector.set_references(values['axis'])
        self.origin_reference = values['origin']
        self.show_origin_reference()
        for field, value in zip(self.position, values['position']):
            field.setProperty('rawValue', value)
        for field, value in zip(self.normal, values['normal']):
            field.setValue(value)
        self.offset.setProperty('rawValue', values['offset'])
        self.reverse_normal.setChecked(values['reverse_normal'])
        self.reverse_axis.setChecked(values['reverse_axis'])
        for collector, role in ((self.plane_collector, 'plane'), (self.axis_collector, 'axis')):
            collector.activated.connect(lambda role=role: self.activate(role))
            collector.changed.connect(self.changed)
        self.axis_collector.changed.connect(self.clear_stored_axis)
        self.mode.currentIndexChanged.connect(self.changed)
        for field in self.position + self.normal + [self.offset]:
            field.valueChanged.connect(self.changed)
        for button in (self.reverse_normal, self.reverse_axis, self.automatic):
            button.toggled.connect(self.changed)
        self.reverse_offset.clicked.connect(lambda: self.offset.setProperty('rawValue', -float(self.offset.property('rawValue'))))
        self.preview_enabled.toggled.connect(self.preview)
        if not operation and context:
            for obj, element in context.profile_selection:
                try:
                    Plane.geometry(component, (obj, element))
                    self.plane_collector.collect((obj, element))
                except ValueError:
                    pass
        self.changed()

    def eventFilter(self, watched, event):
        if watched == self.origin_field:
            if event.type() in (QtCore.QEvent.FocusIn, QtCore.QEvent.MouseButtonPress):
                self.activate('origin')
            if event.type() in (QtCore.QEvent.ShortcutOverride, QtCore.QEvent.KeyPress) and event.key() == QtCore.Qt.Key_Delete:
                if event.type() == QtCore.QEvent.KeyPress:
                    self.origin_reference = None
                    self.stored_origin = None
                    self.show_origin_reference()
                    self.changed()
                event.accept()
                return True
        return super().eventFilter(watched, event)

    def activate(self, role):
        self.pick_role = role
        self.status.setText(tr('Picking plane geometry' if role == 'plane' else 'Picking X direction' if role == 'axis' else 'Picking projected origin'))

    def show_origin_reference(self):
        obj, name = self.origin_reference or (None, '')
        self.origin_field.setText(obj.Label + (' / ' + name if name else '') if obj else
                                  tr('Stored origin: ') + str(self.stored_origin) if self.stored_origin else '')

    def clear_stored_axis(self):
        self.stored_axis = None
        self.changed()

    def values(self):
        return dict(mode=self.mode.currentData(), references=self.plane_collector.references(),
                    position=tuple(float(f.property('rawValue')) for f in self.position),
                    normal=tuple(f.value() for f in self.normal), reverse_normal=self.reverse_normal.isChecked(),
                    offset=float(self.offset.property('rawValue')), axis=self.axis_collector.references(),
                    reverse_axis=self.reverse_axis.isChecked(), origin=self.origin_reference,
                    stored_origin=self.stored_origin, stored_axis=self.stored_axis)

    def changed(self, *args):
        import ComponentPlane as Plane
        numeric = self.mode.currentData() == 'Enter values'
        self.numeric.setVisible(numeric)
        self.plane_collector.setVisible(not numeric)
        self.remove_preview()
        self.timer.stop()
        values = self.values()
        try:
            if numeric:
                normal = Plane.unit(App.Vector(*values['normal']))
            else:
                surface = Plane.surface(self.component, values['references'], self.operation)
                normal = surface.Rotation.multVec(App.Vector(0, 0, 1))
            self.plane_collector.status.setText(tr('Defined'))
        except Exception as error:
            prefix = 'Under-defined: ' if isinstance(error, Plane.UnderDefined) else 'Invalid: '
            self.plane_collector.status.setText(tr(prefix) + str(error))
            normal = None
        try:
            Plane.axis(self.component, values['axis'], normal or App.Vector(0, 0, 1), self.operation)
            self.axis_collector.status.setText(tr('Defined' if values['axis'] else 'Defined: closest component axis projected to plane'))
            if self.stored_axis and not values['axis']:
                self.axis_collector.status.setText(tr('Defined: retained X direction from the existing plane'))
        except Exception as error:
            prefix = 'Under-defined: ' if isinstance(error, Plane.UnderDefined) else 'Invalid: '
            self.axis_collector.status.setText(tr(prefix) + str(error))
        try:
            Plane.evaluate(self.component, values, self.operation)
            self.status.setText(tr('Defined. OK saves the plane.'))
            if self.automatic.isChecked() and self.preview_enabled.isChecked():
                self.timer.start(120)
        except Exception as error:
            self.status.setText(('Under-defined: ' if isinstance(error, Plane.UnderDefined) else 'Invalid: ') + str(error))
        self.highlight_references()

    def preview(self, *args):
        import ComponentPlane as Plane
        self.timer.stop()
        self.remove_preview()
        if not self.preview_enabled.isChecked():
            return
        try:
            placement = Plane.evaluate(self.component, self.values(), self.operation)
            span = 25.
            shape = Part.makePlane(span, span, App.Vector(-span / 2, -span / 2, 0))
            shape.Placement = self.component.getGlobalPlacement().multiply(placement)
            self.ghost = Ghost(shape, color=(0.65, 0.25, 0.85), filled=True, transparency=.65)
        except Exception as error:
            self.status.setText(str(error))

    def remove_preview(self):
        if self.ghost:
            self.ghost.remove()
            self.ghost = None

    def highlight_references(self):
        import ComponentPlane as Plane
        for ghost in self.highlights:
            ghost.remove()
        self.highlights = []
        refs = self.plane_collector.references() + self.axis_collector.references()
        if self.origin_reference:
            refs.append(self.origin_reference)
        for ref in refs:
            try:
                kind, data = Plane.geometry(self.component, ref, self.operation)
                if kind == 'edge':
                    shape = data
                elif kind == 'line':
                    shape = Part.makeLine(data[0] - data[1] * 12.5, data[0] + data[1] * 12.5)
                elif kind == 'point':
                    shape = Part.Vertex(data)
                else:
                    shape = Part.makePlane(25, 25, App.Vector(-12.5, -12.5, 0))
                    shape.Placement = data
                shape = shape.copy()
                shape.transformShape(self.component.getGlobalPlacement().toMatrix())
                self.highlights.append(Ghost(shape, color=(1., .65, 0.)))
            except Exception:
                pass  # Missing references stay listed for repair.

    def addSelection(self, document, name, subname, *args):
        import ComponentPlane as Plane
        from freecad.gui import ComponentSelection as Selection
        try:
            doc = App.listDocuments().get(document)
            base = doc.getObject(name) if doc else None
            item = base.getSubObject(subname, 1) if base and subname else base
            element = subname.rsplit('.', 1)[-1] if subname else ''
            if item not in [self.component.Origin] + list(self.component.Origin.OriginFeatures):
                resolved = Selection.resolve(self.component, base, subname)
                if len(resolved) != 1 or resolved[0].item is None:
                    raise ValueError(tr('Pick geometry in the active component.'))
                item, element = resolved[0].item, resolved[0].element
            if not element.startswith(('Face', 'Edge', 'Vertex')):
                element = ''
            reference = (item, element)
            kind, geometry = Plane.geometry(self.component, reference, self.operation)
            if self.pick_role == 'origin':
                if kind != 'point':
                    raise ValueError(tr('Select an origin, point or curve endpoint.'))
                self.origin_reference = reference
                self.stored_origin = None
                self.show_origin_reference()
                self.changed()
            else:
                if self.pick_role == 'axis' and kind not in ('edge', 'line', 'point'):
                    raise ValueError(tr('Select an edge, line, axis or two points.'))
                collector = self.axis_collector if self.pick_role == 'axis' else self.plane_collector
                collector.collect(reference)
        except Exception as error:
            self.status.setText(str(error))
        finally:
            Gui.Selection.removeSelection(document, name, subname)

    def start(self):
        self.component.Origin.ViewObject.setTemporaryOriginPlanes(True)
        if self.operation:
            self.operation.Visibility = False
        Gui.Selection.clearSelection()
        Gui.Selection.addObserver(self, 0)
        self.observing = True

    def getStandardButtons(self):
        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        return getattr(buttons, 'value', buttons)

    def accept(self):
        import ComponentPlane as Plane
        try:
            self.result = Plane.apply(self.component, self.values(), self.operation)
            normalized = self.result.ProjectedFrame.Normal
            for field, value in zip(self.normal, normalized):
                field.blockSignals(True)
                field.setValue(value)
                field.blockSignals(False)
        except Exception as error:
            self.status.setText(str(error))
            return False
        self.finish()
        return True

    def reject(self):
        self.finish()
        return True

    def finish(self):
        global _task
        self.timer.stop()
        self.remove_preview()
        for ghost in self.highlights:
            ghost.remove()
        self.highlights = []
        if self.observing:
            Gui.Selection.removeObserver(self)
            self.observing = False
        self.component.Origin.ViewObject.setTemporaryOriginPlanes(False)
        if self.operation:
            self.operation.Visibility = self.original_visibility
        Gui.Control.closeDialog()
        _task = None
        if self.context:
            self.context.restore()


def launch(component=None, operation=None):
    global _task
    from freecad.gui.ComponentExtrudeTask import active_component, modeling_component
    from freecad.gui.ComponentNavigator import TaskContext
    import ComponentModel as Model
    if Gui.Control.activeDialog():
        raise ValueError(tr('Finish the current task before editing a plane.'))
    component = modeling_component(Model.owner(operation) if operation else component or active_component())
    context = TaskContext(component)
    try:
        context.enter(operation)
        _task = PlaneTask(component, operation, context)
        Gui.Control.showDialog(_task)
        _task.start()
    except Exception:
        if _task:
            _task.finish()
        else:
            context.restore()
        raise
    return _task
