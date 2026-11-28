# SPDX-License-Identifier: LGPL-2.1-or-later
"""Approved shared creation/placement task for native sketches."""
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtWidgets
from . import plane_task, planes, sketch_placement, modeling, sketch_visibility

_active = None


class SketchPlacementTask(plane_task.PlaneTask):
    # Plane refinements are approved independently of the Sketch placement UI.
    reference_guidance = False

    def __init__(self, feature=None):
        self.origin_visibility = None
        super().__init__(feature)
        self.form.setWindowTitle('New Sketch')
        self.form.setWindowIcon(Gui.getIcon('Sketcher_NewSketch'))
        self.plane.header.setText('Sketch plane')
        self.origin_visibility = sketch_visibility.Planes(self.definition)

    def title(self, ref):
        obj, sub = ref
        element = Part.splitSubname(sub)[2]
        return obj.Label + ('.' + element if element else '')

    def load_feature(self, feature):
        self.refs = planes.flatten(feature.PlaneReferences)
        self.origin_refs = planes.flatten(feature.OriginPoint)
        self.axis_refs = planes.flatten(feature.AxisReferences)
        self.committed_offset = sketch_placement.saved_offset(feature)
        self.offset.setValue(self.committed_offset)
        from .quantity_fields import restore
        restore(feature, {'SketchPlaneOffset':self.offset})
        self.y_choice.setChecked(feature.DefinedAxis == 'Y')
        self.flip.setChecked(feature.FlipNormal)

    def selected_plane_object(self):
        return sketch_placement.plane_object(self.refs)

    def placement(self):
        self.check()
        axis = 'X' if self.x_choice.isChecked() else 'Y'
        sketch_placement.validate(self.definition, self.refs, self.origin_refs, self.axis_refs,
                                  axis, self.flip.isChecked(), self.feature, self.committed_offset, self.normal_to_line)
        return sketch_placement.solve(self.definition, self.refs, self.origin_refs, self.axis_refs,
                                      axis, self.flip.isChecked(), self.committed_offset, self.normal_to_line)

    def update(self, *args):
        super().update(*args)
        support=self.selected_plane_object()
        if len(self.refs)==1:
            name=self.title(self.refs[0])
            axis='X' if self.x_choice.isChecked() else 'Y'
            if not self.origin_refs:
                self.origin_ref.setText(name+' origin' if support else 'Projected part origin')
                self.origin_hint.setText("Using the selected plane's origin." if support else
                                         'Part origin projected onto the selected face.')
                if self.committed_offset:
                    self.origin_hint.setText('Using the selected plane frame with offset.' if support else
                                             'Part origin projected onto the offset sketch plane.')
            if not self.axis_refs:
                self.axis_ref.setText(name+' '+axis+' axis' if support else
                                      ('Projected part X' if axis=='X' else 'Y derived from projected part X'))
        if self.valid and len(self.refs)==1:
            self.status.setText('Using the selected plane’s origin and orientation.' if support else
                                'Using the projected part origin and X axis.')

    def accept(self):
        transaction_id = None
        try:
            self.offset.interpretText()
            self.committed_offset = self.offset.value()
            self.placement()
            # Automatic visibility must not enter the sketch's native transaction.
            self.origin_visibility.restore()
            args = (self.refs, self.origin_refs, self.axis_refs,
                    'X' if self.x_choice.isChecked() else 'Y', self.flip.isChecked())
            if self.feature is not None:
                self.result = sketch_placement.save(self.doc, *args, feature=self.feature, offset=self.committed_offset,
                                                   normal_to_line=self.normal_to_line, quantity_units={'SketchPlaneOffset':self.offset._unit})
                self.reject()
            else:
                # Native drawing owns completion of the new-sketch transaction.
                transaction_id = App.setActiveTransaction('Create a new sketch')
                self.result = self.definition.newObject('Sketcher::SketchObject', 'Sketch')
                sketch_placement.configure(self.result, *args, offset=self.committed_offset,
                                           normal_to_line=self.normal_to_line, quantity_units={'SketchPlaneOffset':self.offset._unit})
                self.source_doc.recompute()
                if 'Invalid' in self.result.State:
                    raise ValueError('The sketch could not be recomputed')
                self._continue_history = True
                self.reject()
                # The native task OK callback must unwind before another task
                # can be opened. Otherwise Sketcher sees the retiring dialog.
                QtCore.QTimer.singleShot(0, lambda: self.enter_drawing(transaction_id))
            return True
        except Exception as exc:
            if transaction_id is not None:
                App.closeActiveTransaction(True, transaction_id)
            if not self.closed:
                self.origin_visibility.apply()
            self.status.setError(str(exc))
            return False

    def enter_drawing(self, transaction_id):
        try:
            modeling._enter_editor(self.doc, self.definition, self.path, self.result)
        except Exception as exc:
            App.closeActiveTransaction(True, transaction_id)
            App.Console.PrintError(str(exc) + '\n')
        finally:
            from . import panel
            self._continue_history = False
            panel.end_feature_task(self)

    def reject(self):
        global _active
        if self.origin_visibility is not None:
            self.origin_visibility.restore()
        result = super().reject()
        if _active is self:
            _active = None
        return result


def show(feature=None):
    global _active
    if Gui.Control.activeDialog():
        raise ValueError('Finish the current task first')
    if feature is not None and not sketch_placement.is_managed(feature):
        raise ValueError('This sketch uses native attachment settings')
    _active = SketchPlacementTask(feature)
    Gui.Control.showDialog(_active)
    _active.update()
    from . import panel
    panel.begin_feature_task(_active)
    return _active
