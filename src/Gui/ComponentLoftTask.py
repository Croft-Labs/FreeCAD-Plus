# SPDX-License-Identifier: LGPL-2.1-or-later
"""One ordered-section Loft task for component creation and history editing."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.ComponentSectionTask import SectionTask
from freecad.gui.ComponentExtrudeTask import active_component

_task = None


def tr(text):
    return App.Qt.translate("ComponentLoft", text)


class LoftTask(SectionTask):
    operation_name = "Loft"

    def __init__(self, component, operation=None, preset=None, context=None):
        import ComponentModel as Model
        import ComponentLoft as Loft
        self.backend = Loft
        self.component, self.operation, self.context = component, operation, context
        self.ghost = self.result = self.mouse_callback = self.reference_pick = None
        self.observing, self.whole_profile = False, True
        self.profile_visibility, self.preview_transparency, self.preview_visibility = {}, {}, {}
        self.view = Gui.getDocument(component.Document.Name).activeView()
        outer = self.build_sections()
        main, dimensions, advanced, preview = [section[2] for section in self.sections]
        self.build_operation_controls(main, Loft.MODES)
        self.build_collectors(main, "Sections in loft order")
        self.interpolation = self.combo(main, "Type", [("Smooth", False), ("Ruled", True)])
        self.buttons(dimensions, (("Move up", lambda: self.move_section(-1)), ("Move down", lambda: self.move_section(1)),
                                  ("Reverse order", self.reverse_sections)))
        explanation = QtWidgets.QLabel(tr("Section placements define the span. Select a row to inspect or replace its curves."))
        explanation.setWordWrap(True)
        dimensions.addRow(explanation)
        self.closed = QtWidgets.QCheckBox(tr("Closed — connect last section to first"))
        advanced.addRow(self.closed)
        self.refine = self.checkbox(advanced, "Refine result", True)
        self.fuzzy = self.fuzzy_tolerance(advanced)
        self.build_preview_controls(preview)
        self.build_status(outer)
        self.profile.currentIndexChanged.connect(self.profile_changed)
        self.ordered.currentRowChanged.connect(self.inspect_section)
        self.mode.setCurrentIndex(Loft.MODES.index(preset) if preset in Loft.MODES else 0)
        if operation:
            sections, mode, target, options = Loft.read(operation)
            self.mode.setCurrentIndex(Loft.MODES.index(mode))
            if target:
                if self.target.findData(target.Name) < 0:
                    self.target.addItem(Model.display_object(target).Label, target.Name)
                self.target.setCurrentIndex(self.target.findData(target.Name))
            self.interpolation.setCurrentIndex(self.interpolation.findData(options["ruled"]))
            self.closed.setChecked(options["closed"])
            self.refine.setChecked(options["refine"])
            self.fuzzy.setProperty("rawValue", options["fuzzy"])
            for obj, elements in sections:
                self.add_row(obj, elements)
        else:
            from freecad.gui import ComponentSelection as Selection
            picks = context.profile_selection if context else [(p.item, p.element) for p in Selection.selected(component, Gui.Selection.getSelectionEx("*", 0)) if p.item is not None]
            grouped = {}
            for obj, element in picks:
                grouped.setdefault(obj, []).append(element)
            for obj, elements in grouped.items():
                if self.profile.findData(obj.Name) >= 0:
                    self.add_row(obj, elements if all(elements) else None)
        for field in (self.mode, self.target, self.interpolation, self.preview_mode):
            field.currentIndexChanged.connect(self.changed)
        for field in (self.closed, self.refine, self.auto_preview):
            field.toggled.connect(self.changed)
        self.preview_button.clicked.connect(self.preview)
        self.fuzzy.valueChanged.connect(self.changed)
        self.changed()

    def changed(self, *args):
        if not hasattr(self, "preview_timer"):
            return
        self.clear_preview()
        visible = self.mode.currentData() != "New Body"
        self.target.setVisible(visible)
        self.sections[0][2].labelForField(self.target).setVisible(visible)
        self.preview_timer.stop()
        enabled = self.preview_mode.currentData() != "None"
        self.preview_button.setEnabled(enabled)
        if enabled and self.auto_preview.isChecked() and self.ordered.count() >= 2:
            self.preview_timer.start(300)
        self.status.setText(tr("Append at least two sections in order. Add and Subtract require a target body."))

    def values(self):
        doc = self.component.Document
        sections = []
        for row in range(self.ordered.count()):
            name, elements = self.ordered.item(row).data(QtCore.Qt.UserRole)
            sections.append((doc.getObject(name), elements))
        mode = self.mode.currentData()
        target = doc.getObject(self.target.currentData()) if mode != "New Body" and self.target.currentData() else None
        return sections, mode, target, dict(ruled=self.interpolation.currentData(), closed=self.closed.isChecked(),
                                           refine=self.refine.isChecked(), fuzzy=float(self.fuzzy.property("rawValue")))

    def accept(self):
        self.preview_timer.stop()
        try:
            values = self.values()
            self.clear_preview()
            self.restore_profile_visibility()
            if self.operation:
                self.operation = self.backend.edit(self.operation, *values)
            else:
                self.operation, self.result = self.backend.create(self.component, *values)
        except Exception as error:
            self.status.setText(str(error))
            return False
        self.finish(committed=True)
        return True

    def finish(self, committed=False):
        global _task
        self.stop_selection()
        self.clear_preview()
        if not committed:
            self.restore_profile_visibility()
        Gui.Control.closeDialog()
        _task = None
        if self.context:
            self.context.restore()


def launch(preset=None, operation=None):
    global _task
    if Gui.Control.activeDialog():
        raise ValueError(tr("Finish the current task before starting Loft."))
    import ComponentModel as Model
    from freecad.gui.ComponentNavigator import TaskContext
    component = Model.owner(operation) if operation else active_component()
    context = TaskContext(component)
    try:
        context.enter(operation)
        _task = LoftTask(component, operation, preset, context)
        Gui.Control.showDialog(_task)
        _task.start_selection()
    except Exception:
        if _task:
            _task.finish()
        else:
            context.restore()
        raise
    return _task
