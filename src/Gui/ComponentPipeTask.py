# SPDX-License-Identifier: LGPL-2.1-or-later
"""Unified component Pipe task with explicit profile, spine and auxiliary roles."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.ComponentSectionTask import SectionTask
from freecad.gui.ComponentExtrudeTask import active_component, CompactFormLayout, CurveListWidget

_task = None


def tr(text):
    return App.Qt.translate("ComponentPipe", text)


class PipeTask(SectionTask):
    operation_name = "Pipe"

    def __init__(self, component, operation=None, preset=None, context=None):
        import ComponentModel as Model
        import ComponentPipe as Pipe
        self.backend = Pipe
        self.component, self.operation, self.context = component, operation, context
        self.ghost = self.result = self.mouse_callback = self.reference_pick = None
        self.observing, self.whole_profile = False, True
        self.profile_visibility, self.preview_transparency, self.preview_visibility = {}, {}, {}
        self.path_role, self.paths = None, {}
        self.retained = Pipe.defaults()
        self.view = Gui.getDocument(component.Document.Name).activeView()
        outer = self.build_sections()
        main, dimensions, advanced, preview = [section[2] for section in self.sections]
        self.mode = self.combo(main, "Operation", [(name, name) for name in Pipe.MODES])
        self.target = self.combo(main, "Target body", [("Select a target body…", None)])
        for obj in Model.finished_results(component):
            if obj.Shape.Solids and (operation is None or operation not in obj.OutListRecursive):
                self.target.addItem(Model.display_object(obj).Label, obj.Name)
        self.build_collectors(main, "Profile then sections")
        self.buttons(main, (("Pick profile curves", lambda: self.set_role(None)),))
        self.transformation = self.combo(main, "Mode", [(name, name) for name in Pipe.TRANSFORMATIONS])
        self.transformation.setToolTip(tr("Constant uses the first profile; additional sections are retained for Multisection."))
        self.transition = self.combo(main, "Type / corner transition", [(name, name) for name in Pipe.TRANSITIONS])
        self.path_picker(dimensions, "Sweep path", "spine")
        self.buttons(dimensions, (("Move section up", lambda: self.move_section(-1)),
                                  ("Move section down", lambda: self.move_section(1))))
        hint = QtWidgets.QLabel(tr("The selected path defines length and direction; section placements define the sweep. Additional sections are used by Multisection."))
        hint.setWordWrap(True)
        dimensions.addRow(hint)
        self.orientation = self.combo(advanced, "Orientation", [(name, name) for name in Pipe.ORIENTATIONS])
        self.path_picker(advanced, "Auxiliary path", "auxiliary")
        self.curvilinear = QtWidgets.QCheckBox(tr("Curvilinear equivalence"))
        self.curvilinear.setChecked(True)
        advanced.addRow(self.curvilinear)
        self.binormal = []
        for axis, value in zip("XYZ", (0., 0., 1.)):
            field = QtWidgets.QDoubleSpinBox()
            field.setDecimals(6)
            field.setRange(-1e6, 1e6)
            field.setValue(value)
            advanced.addRow(tr("Binormal ") + axis, field)
            self.binormal.append(field)
        self.boolean = self.combo(advanced, "Subtractive result", [("Subtraction", "Subtraction"), ("Common (keep intersection)", "Common")])
        self.refine = QtWidgets.QCheckBox(tr("Refine result"))
        self.refine.setChecked(True)
        advanced.addRow(self.refine)
        self.fuzzy = self.quantity(0.)
        self.fuzzy.setProperty("minimum", -1.)
        self.fuzzy.setProperty("maximum", 1.)
        self.fuzzy.setToolTip(tr("Zero: native default. Negative: automatic tolerance. Positive: explicit tolerance up to 1 mm."))
        advanced.addRow(tr("Fuzzy tolerance"), self.fuzzy)
        self.auto_preview = QtWidgets.QCheckBox(tr("Recompute on change"))
        self.auto_preview.setChecked(True)
        preview.addRow(self.auto_preview)
        self.preview_mode = self.combo(preview, "Preview type", [(name, name) for name in ("None", "Overlay", "Result")])
        self.preview_mode.setCurrentIndex(1)
        self.preview_button = QtWidgets.QPushButton(tr("Update preview"))
        preview.addRow(self.preview_button)
        self.status = QtWidgets.QLabel()
        self.status.setTextFormat(QtCore.Qt.PlainText)
        self.status.setWordWrap(True)
        outer.addWidget(self.status)
        outer.addStretch()
        self.preview_timer = QtCore.QTimer(self.form)
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self.preview)
        self.profile.currentIndexChanged.connect(self.profile_changed)
        self.ordered.currentRowChanged.connect(self.inspect_section)
        self.mode.setCurrentIndex(Pipe.MODES.index(preset) if preset in Pipe.MODES else 0)
        if operation:
            sections, mode, target, options = Pipe.read(operation)
            self.retained = options
            self.mode.setCurrentIndex(Pipe.MODES.index(mode))
            if target:
                if self.target.findData(target.Name) < 0:
                    self.target.addItem(Model.display_object(target).Label, target.Name)
                self.target.setCurrentIndex(self.target.findData(target.Name))
            for field, key in ((self.transformation, "transformation"), (self.transition, "transition"),
                               (self.orientation, "orientation"), (self.boolean, "boolean")):
                field.setCurrentIndex(field.findData(options[key]))
            self.curvilinear.setChecked(options["curvilinear"])
            self.refine.setChecked(options["refine"])
            self.fuzzy.setProperty("rawValue", options["fuzzy"])
            for field, value in zip(self.binormal, options["binormal"]):
                field.setValue(value)
            for obj, elements in sections:
                self.add_row(obj, elements)
            for key in self.paths:
                if options[key]:
                    self.set_path(key, *options[key])
        else:
            self.preselection(context.profile_selection if context else None)
        for field in (self.mode, self.target, self.transformation, self.transition, self.orientation, self.boolean, self.preview_mode):
            field.currentIndexChanged.connect(self.changed)
        for field in (self.curvilinear, self.refine, self.auto_preview):
            field.toggled.connect(self.changed)
        for field in self.binormal + [self.fuzzy]:
            field.valueChanged.connect(self.changed)
        self.preview_button.clicked.connect(self.preview)
        self.changed()

    def path_picker(self, layout, label, key):
        import ComponentModel as Model
        host = QtWidgets.QWidget()
        form = CompactFormLayout(host)
        form.setContentsMargins(0, 0, 0, 0)
        source = self.combo(form, "Source", [("Select a path…", None)])
        for obj in Model.history(self.component):
            if hasattr(obj, "Shape") and obj.Shape.Edges and getattr(obj, "ComponentRole", "") in ("Object", "Reference", "Result"):
                source.addItem(obj.Label + " (" + obj.Name + ")", obj.Name)
        edges = CurveListWidget()
        edges.removeRequested.connect(lambda: self.remove_path_edges(key))
        edges.setMaximumHeight(60)
        edges.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        form.addRow(tr("Edges"), edges)
        self.paths[key] = dict(source=source, edges=edges, host=host, whole=True)
        self.buttons(form, (("Pick edges", lambda: self.set_role(key)),
                            ("Use whole", lambda: self.whole_path(key))))
        self.buttons(form, (("Remove edges", lambda: self.remove_path_edges(key)), ("Clear path", lambda: self.clear_path(key))))
        source.currentIndexChanged.connect(lambda: self.whole_path(key))
        layout.addRow(tr(label), host)

    def set_role(self, key):
        self.path_role = key
        self.reference_pick = None
        for name, fields in self.paths.items():
            fields["host"].setToolTip(tr("Active path collector") if name == key else "")
        self.status.setText(tr("Picking sweep path edges") if key == "spine" else tr("Picking auxiliary path edges") if key else tr("Picking profile curves; append or replace the section when ready."))
        self.update_curve_display()

    def active_curve_source(self):
        if self.path_role:
            return self.paths[self.path_role]["source"].currentData()
        return super().active_curve_source()

    def curve_display_inputs(self):
        selected = super().curve_display_inputs()
        for key, fields in self.paths.items():
            if key == "auxiliary" and self.orientation.currentData() != "Auxiliary":
                continue
            name = fields["source"].currentData()
            if name:
                elements = None if fields["whole"] else [fields["edges"].item(i).text() for i in range(fields["edges"].count())]
                selected.append((name, elements))
        return selected

    def set_path(self, key, obj, elements, whole=None, current=None):
        fields = self.paths[key]
        fields["source"].setCurrentIndex(fields["source"].findData(obj.Name))
        fields["edges"].clear()
        names = [name for name in elements if name]
        fields["whole"] = not names if whole is None else whole
        if names:
            fields["edges"].addItems(names)
        elif fields["whole"]:
            fields["edges"].addItem(tr("Whole path"))
        fields["edges"].highlight(names.index(current) if current in names else -1)
        self.changed()

    def whole_path(self, key):
        fields = self.paths[key]
        fields["edges"].clear()
        fields["whole"] = True
        if fields["source"].currentData():
            fields["edges"].addItem(tr("Whole path"))
        self.changed()

    def clear_path(self, key):
        self.paths[key]["source"].setCurrentIndex(0)
        self.whole_path(key)

    def path_value(self, key):
        fields = self.paths[key]
        name = fields["source"].currentData()
        if not name:
            return None
        if not fields["whole"] and fields["edges"].count() == 0:
            raise ValueError(tr("Select path edges or choose Use whole."))
        return self.component.Document.getObject(name), [] if fields["whole"] else [fields["edges"].item(i).text() for i in range(fields["edges"].count())]

    def remove_path_edges(self, key):
        fields = self.paths[key]
        if not fields["edges"].selectedItems():
            return
        for row in sorted((fields["edges"].row(item) for item in fields["edges"].selectedItems()), reverse=True):
            fields["edges"].takeItem(row)
        fields["edges"].highlight()
        fields["whole"] = False
        self.changed()

    def collect_path(self, key, picks=None, toggle=False):
        from freecad.gui import ComponentSelection as Selection
        picks = picks if picks is not None else [(p.item, p.element) for p in Selection.selected(self.component, Gui.Selection.getSelectionEx("*", 0)) if p.item is not None]
        try:
            if not picks or len({obj for obj, element in picks}) != 1:
                raise ValueError(tr("Choose path edges from one local object."))
            obj, elements = picks[0][0], [element for source, element in picks if element]
            fields = self.paths[key]
            if fields["source"].findData(obj.Name) < 0:
                raise ValueError(tr("Choose a path owned by the active component."))
            # Incremental disconnected picks remain visible for correction; final
            # path validation occurs at Preview/OK, never silently drops an edge.
            if elements and any(not e.startswith("Edge") or not e[4:].isdigit() for e in elements):
                raise ValueError(tr("Choose edges for the path."))
            if elements:
                names = ([fields["edges"].item(i).text() for i in range(fields["edges"].count())]
                         if fields["source"].currentData() == obj.Name and not fields["whole"] else [])
                current = None
                for element in dict.fromkeys(elements):
                    if toggle and element in names:
                        names.remove(element)
                        current = None
                    else:
                        if element not in names:
                            names.append(element)
                        current = element
                self.set_path(key, obj, names, whole=False, current=current)
                if self.observing:
                    fields["edges"].setFocus(QtCore.Qt.OtherFocusReason)
            else:
                self.set_path(key, obj, elements)
        except Exception as error:
            self.status.setText(str(error))

    def preselection(self, picks):
        from freecad.gui import ComponentSelection as Selection
        picks = picks if picks is not None else [(p.item, p.element) for p in Selection.selected(self.component, Gui.Selection.getSelectionEx("*", 0)) if p.item is not None]
        grouped = {}
        for obj, element in picks:
            grouped.setdefault(obj, []).append(element)
        for index, (obj, elements) in enumerate(grouped.items()):
            if index == 1 and self.paths["spine"]["source"].findData(obj.Name) >= 0:
                self.set_path("spine", obj, elements)
            elif self.profile.findData(obj.Name) >= 0:
                self.add_row(obj, elements if all(elements) else None)
        if self.ordered.count() > 1:
            self.transformation.setCurrentIndex(self.transformation.findData("Multisection"))

    def addSelection(self, document, name, subname, *args):
        if self.path_role:
            from freecad.gui import ComponentSelection as Selection
            doc = App.listDocuments().get(document)
            obj = doc.getObject(name) if doc else None
            picks = [(p.item, p.element) for p in Selection.resolve(self.component, obj, subname) if p.item is not None]
            self.collect_path(self.path_role, picks, toggle=True)
            if len(picks) == 1 and picks[0][1].startswith("Edge"):
                Gui.Selection.removeSelection(document, name, subname)
        else:
            super().addSelection(document, name, subname, *args)

    def pick_region(self, event):
        if self.path_role is None:
            super().pick_region(event)

    def changed(self, *args):
        if not hasattr(self, "preview_timer"):
            return
        self.clear_preview()
        for layout, widget, visible in ((self.sections[0][2], self.target, self.mode.currentData() != "New Body"),
                (self.sections[2][2], self.paths["auxiliary"]["host"], self.orientation.currentData() == "Auxiliary"),
                (self.sections[2][2], self.boolean, self.mode.currentData() == "Subtract")):
            widget.setVisible(visible)
            layout.labelForField(widget).setVisible(visible)
        self.curvilinear.setVisible(self.orientation.currentData() == "Auxiliary")
        if self.path_role == "auxiliary" and self.orientation.currentData() != "Auxiliary":
            self.path_role = None
        for field in self.binormal:
            field.setVisible(self.orientation.currentData() == "Binormal")
            self.sections[2][2].labelForField(field).setVisible(self.orientation.currentData() == "Binormal")
        self.preview_timer.stop()
        enabled = self.preview_mode.currentData() != "None"
        self.preview_button.setEnabled(enabled)
        if enabled and self.auto_preview.isChecked() and self.ordered.count() and self.paths["spine"]["source"].currentData():
            self.preview_timer.start(300)
        if self.path_role:
            self.set_role(self.path_role)
        else:
            self.status.setText(tr("Append a profile and select its sweep path. Add/Subtract require an explicit target."))
        self.update_curve_display()

    def values(self):
        doc = self.component.Document
        sections = []
        for row in range(self.ordered.count()):
            name, elements = self.ordered.item(row).data(QtCore.Qt.UserRole)
            sections.append((doc.getObject(name), elements))
        mode = self.mode.currentData()
        target = doc.getObject(self.target.currentData()) if mode != "New Body" and self.target.currentData() else None
        options = dict(self.retained)
        options.update(spine=self.path_value("spine"), auxiliary=self.path_value("auxiliary"),
                       transformation=self.transformation.currentData(), transition=self.transition.currentData(),
                       orientation=self.orientation.currentData(), binormal=tuple(field.value() for field in self.binormal),
                       curvilinear=self.curvilinear.isChecked(), boolean=self.boolean.currentData(),
                       refine=self.refine.isChecked(), fuzzy=float(self.fuzzy.property("rawValue")))
        return sections, mode, target, options

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
        raise ValueError(tr("Finish the current task before starting Pipe."))
    import ComponentModel as Model
    from freecad.gui.ComponentNavigator import TaskContext
    component = Model.owner(operation) if operation else active_component()
    context = TaskContext(component)
    try:
        context.enter()
        _task = PipeTask(component, operation, preset, context)
        Gui.Control.showDialog(_task)
        _task.start_selection()
    except Exception:
        if _task:
            _task.finish()
        else:
            context.restore()
        raise
    return _task
