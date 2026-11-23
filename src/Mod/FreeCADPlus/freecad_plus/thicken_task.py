# SPDX-License-Identifier: LGPL-2.1-or-later
"""Thicken's sheet collector on the common feature task lifecycle."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtWidgets
from . import document, extrude_task, modeling, planes, thicken
from .plane_task import label
from .task_status import TaskStatus


class ThickenTask(extrude_task.ExtrudeTask):
    engine = thicken
    title = 'Thicken'
    icon = 'Part_Offset'
    selection_noun = 'sheets'

    def usable_geometry(self, obj, sheet=False):
        return (not obj.isDerivedFrom('Sketcher::SketchObject')
                and super().usable_geometry(obj, sheet))

    def configure_form(self):
        self.modes['New Solid'].setText('New')
        self.profile.header.setText('Sheets / faces')
        self.profile_hint.setText('Select a sheet or connected faces from one sheet.')
        for button in self.profile.findChildren(QtWidgets.QPushButton):
            if button.text() == 'Whole sketch':button.hide()
        self.start.hide();self.extent.hide();self.advanced.hide()
        self.fields = {'target': self.fields['target']}
        self.numbers = [];self.values = {}
        layout = self.form.layout()
        self.thickness_section = self.section(layout, 'Thickness')
        self.thickness_row, self.amount = self.numeric(self.thickness_section.layout, 'Total thickness', 1)
        self.amount.setRange(.01, 100000)
        self.normal = self.combo(self.thickness_section.layout, 'Direction',
                                 ['Along normal', 'Opposite normal', 'Symmetric'])
        self.direction_hint = label('');self.thickness_section.layout.addWidget(self.direction_hint)
        self.join_section = self.section(layout, 'Advanced', False)
        self.join = self.combo(self.join_section.layout, 'Corner join', ['Sharp', 'Rounded'])
        for section in (self.thickness_section, self.join_section):
            layout.removeWidget(section);layout.insertWidget(layout.indexOf(self.preview), section)

    def initial_selection(self, which):
        self.entry_error = ''
        raw = [(entry.Object, sub) for entry in Gui.Selection.getSelectionEx('*', 0)
               for sub in entry.SubElementNames or ('',)]
        try:
            for ref in planes.canonical(self.owner, raw):
                ref = thicken.profile_reference(ref)
                thicken.validate_profiles(self.owner, self.refs + [ref])
                self.refs.append(ref)
        except Exception as exc:
            self.entry_error = str(exc)

    def settings(self):
        return dict(operation=self.mode(), thickness=self.values[self.amount],
                    direction=self.normal.currentText(), join=self.join.currentText())

    def load_feature(self, feature):
        self.refs = planes.flatten(feature.ProfileReferences)
        self.links = thicken.references(feature)
        values = thicken.settings(feature)
        self.modes[values['operation']].setChecked(True)
        self.amount.setValue(values['thickness']);self.values[self.amount] = values['thickness']
        self.normal.setCurrentText(values['direction']);self.join.setCurrentText(values['join'])

    def refresh_fields(self):
        super().refresh_fields()
        for i, (obj, sub) in enumerate(self.refs):
            if not sub:self.profiles.item(i).setText(obj.Label + ' · Whole sheet')

    def changed(self, *args):
        if not self.ready or self.closed:return
        self.update_target();self.presentation.update_style()
        self.direction_hint.setText('Half of the total thickness on each side of the sheet.'
                                   if self.normal.currentText() == 'Symmetric' else
                                   'Thickness follows the sheet surface normals.')
        if self.automatic.isChecked():self.render()
        else:
            self.clear_overlay();self.status.setText('Preview needs update.');self.set_ok(self.target_ready())
        self.refresh_target()

    def pick_region(self, callback):
        # Native face and History picks are the sheet collector's only inputs.
        pass

    def addSelection(self, doc, name, sub, *args):
        if self.closed:return
        if self.pick != 'profile':return super().addSelection(doc, name, sub, *args)
        try:
            self.check()
            if not self.require_target():
                Gui.Selection.removeSelection(doc, name, sub);return
            ref = thicken.profile_reference(planes.canonical(self.owner, [(App.getDocument(doc).getObject(name), sub)])[0])
            document.require_predecessors(self.owner, self.feature, [ref])
            refs = [old for old in self.refs if old != ref] if ref in self.refs else self.refs + [ref]
            if refs:thicken.validate_profiles(self.owner, refs)
            if ref not in self.refs and not ref[1]:refs = [ref]
            elif ref not in self.refs:refs = [old for old in refs if old[1]]
            self.refs = refs;self.refresh_fields();self.changed()
            Gui.Selection.removeSelection(doc, name, sub)
        except Exception as exc:self.status.setError(str(exc))


def show(feature=None):
    if Gui.Control.activeDialog():raise ValueError('Finish the current task first.')
    if feature is not None and not thicken.is_thicken(feature):
        raise ValueError('This feature uses the native editor.')
    task = ThickenTask(feature);extrude_task._active = task
    Gui.Control.showDialog(task);task.changed()
    if getattr(task, 'entry_error', ''):task.status.setError(task.entry_error)
    from . import panel
    panel.begin_feature_task(task)
    return task


def show_error(title, message):
    dialog = QtWidgets.QDialog(Gui.getMainWindow());dialog.setWindowTitle(title)
    layout = QtWidgets.QVBoxLayout(dialog);status = TaskStatus();status.setError(message);layout.addWidget(status)
    buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
    buttons.rejected.connect(dialog.reject);layout.addWidget(buttons)
    dialog.resize(440, 155);dialog.exec()


class Command:
    def GetResources(self):
        return dict(Pixmap='Part_Offset', MenuText='Thicken', ToolTip='Give a sheet thickness to create a solid')

    def IsActive(self):
        if Gui.activeDocument() is None:return False
        try:modeling._context(Gui.activeDocument().Document);return True
        except (ValueError, RuntimeError):return False

    def Activated(self):
        try:show()
        except Exception as exc:show_error('Thicken', str(exc))


def install():
    Gui.addCommand('Plus_Thicken', Command())
