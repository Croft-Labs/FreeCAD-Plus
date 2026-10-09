# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component sketch-plane choice followed by the native Sketcher editor."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets
from freecad.gui.ComponentExtrudeTask import active_component, modeling_component, CompactFormLayout

_task = None


def tr(text):
    return App.Qt.translate("ComponentSketch", text)


class SketchTask:
    def __init__(self, component, context=None, datum_only=False):
        import ComponentModel as Model
        import ComponentSketch as Sketch
        Model.activate(component, strict=False)
        self.component, self.support, self.result = component, None, None
        self.context = context
        self.datum_only = datum_only
        self.origin_reference = None
        self.axis_references = []
        self.pick_role = None
        self.origin = component.Origin
        self.origin_planes = {obj.Name: obj.Role.replace("_", " ").replace("Plane", "plane")
                              for obj in self.origin.OriginFeatures
                              if getattr(obj, "Role", "") in ("XY_Plane", "XZ_Plane", "YZ_Plane")}
        self.observing = False
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle(tr("Datum Plane") if datum_only else tr("New Sketch"))
        layout = QtWidgets.QVBoxLayout(self.form)
        self.plane = QtWidgets.QComboBox()
        for name in Sketch.PLANES:
            self.plane.addItem(tr(name), name)
        layout.addWidget(self.plane)
        self.plane.setAccessibleName(tr("Sketch attachment"))
        self.plane.setVisible(not datum_only)
        self.follow_support = QtWidgets.QCheckBox(tr("Follow support"))
        self.follow_support.setChecked(True)
        self.follow_support.setToolTip(tr("Follow a valid support. If it disappears or fails, keep the last valid sketch frame. Uncheck to copy its frame once."))
        self.follow_support.setVisible(not datum_only)
        layout.addWidget(self.follow_support)
        self.sections = []
        for title in ("Define Surface", "Z Direction", "Sketch Origin", "X Direction"):
            section = QtWidgets.QGroupBox(tr(title))
            CompactFormLayout(section)
            layout.addWidget(section)
            self.sections.append(section)
        definition, normal, origin, orientation = [section.layout() for section in self.sections]
        self.base = QtWidgets.QComboBox()
        for name in Sketch.BASE_PLANES:
            self.base.addItem(tr(name), name)
        self.base_label = QtWidgets.QLabel(tr("Base plane"))
        definition.addRow(self.base_label, self.base)
        self.user_plane = QtWidgets.QComboBox()
        for obj in Sketch.user_planes(component):
            self.user_plane.addItem(obj.Label, obj.Name)
        self.user_plane_label = QtWidgets.QLabel(tr("User plane"))
        definition.addRow(self.user_plane_label, self.user_plane)
        self.origins = []
        self.origin_labels = []
        for label in ("Origin X", "Origin Y"):
            control = Gui.UiLoader().createWidget("Gui::QuantitySpinBox")
            control.setProperty("unit", "mm")
            control.setProperty("minimum", -1e9)
            control.setProperty("maximum", 1e9)
            caption = QtWidgets.QLabel(tr(label))
            origin.addRow(caption, control)
            self.origins.append(control)
            self.origin_labels.append(caption)
        self.offset = Gui.UiLoader().createWidget("Gui::QuantitySpinBox")
        self.offset.setProperty("unit", "mm")
        self.offset.setProperty("minimum", -1e9)
        self.offset.setProperty("maximum", 1e9)
        self.offset_label = QtWidgets.QLabel(tr("Offset"))
        definition.addRow(self.offset_label, self.offset)
        self.orientation_mode = QtWidgets.QComboBox()
        for name in ("Projected references", "Rotation angles", "Axis directions"):
            self.orientation_mode.addItem(tr(name), name)
        definition.addRow(tr("Frame definition"), self.orientation_mode)
        self.rotations = []
        self.rotation_labels = []
        for label in ("Rotation X", "Rotation Y", "Rotation Z"):
            control = Gui.UiLoader().createWidget("Gui::QuantitySpinBox")
            control.setProperty("unit", "deg")
            control.setProperty("minimum", -360.0)
            control.setProperty("maximum", 360.0)
            caption = QtWidgets.QLabel(tr(label))
            definition.addRow(caption, control)
            self.rotations.append(control)
            self.rotation_labels.append(caption)
        self.direction_axis = QtWidgets.QComboBox()
        for name in ("X", "Y"):
            self.direction_axis.addItem(tr(name + "-axis direction"), name)
        self.direction_axis_label = QtWidgets.QLabel(tr("In-plane axis"))
        orientation.addRow(self.direction_axis_label, self.direction_axis)
        self.direction_rows = []
        self.directions = []
        for label, values in (("X-axis direction", (1, 0, 0)), ("Z-axis direction", (0, 0, 1))):
            row = QtWidgets.QWidget()
            boxes = CompactFormLayout(row)
            boxes.setContentsMargins(0, 0, 0, 0)
            controls = []
            for axis, value in zip(("X", "Y", "Z"), values):
                spin = QtWidgets.QDoubleSpinBox()
                spin.setRange(-1e6, 1e6)
                spin.setDecimals(6)
                spin.setValue(value)
                spin.setAccessibleName(tr(label) + " " + axis)
                boxes.addRow(axis, spin)
                controls.append(spin)
            caption = QtWidgets.QLabel(tr(label))
            orientation.addRow(caption, row)
            self.direction_rows.append((caption, row))
            self.directions.append(controls)
        self.direction_hint = QtWidgets.QLabel(tr("Directions and origin are measured in the base attachment frame. Z sets the normal; X or Y is projected onto its plane."))
        self.direction_hint.setWordWrap(True)
        orientation.addRow(self.direction_hint)
        self.reverse_z = QtWidgets.QPushButton(tr("Reverse Z"))
        self.reverse_z.setCheckable(True)
        normal.addRow(tr("Z follows the surface normal"), self.reverse_z)
        self.origin_source = QtWidgets.QComboBox()
        self.origin_source.addItems([tr("Part origin projected to plane"), tr("Selected point projected to plane")])
        origin.addRow(self.origin_source)
        self.origin_pick = QtWidgets.QPushButton(tr("Select origin point"))
        origin.addRow(self.origin_pick)
        self.origin_selection = QtWidgets.QLabel(tr("Part origin"))
        self.origin_selection.setWordWrap(True)
        origin.addRow(self.origin_selection)
        self.x_source = QtWidgets.QComboBox()
        self.x_source.addItems([tr("Closest component axis"), tr("Line or edge"), tr("Two points")])
        orientation.addRow(self.x_source)
        self.x_pick = QtWidgets.QPushButton(tr("Select X direction"))
        orientation.addRow(self.x_pick)
        self.x_selection = QtWidgets.QLabel(tr("Project the component axis closest to the plane. Ties use X, then Y, then Z."))
        self.x_selection.setWordWrap(True)
        orientation.addRow(self.x_selection)
        self.reverse_x = QtWidgets.QPushButton(tr("Reverse X"))
        self.reverse_x.setCheckable(True)
        orientation.addRow(self.reverse_x)
        self.origin_pick.clicked.connect(lambda: self.start_frame_pick("origin"))
        self.x_pick.clicked.connect(lambda: self.start_frame_pick("axis"))
        self.origin_source.currentIndexChanged.connect(self.origin_source_changed)
        self.x_source.currentIndexChanged.connect(self.x_source_changed)
        self.capture = QtWidgets.QPushButton(tr("Use selected geometry"))
        definition.addRow(self.capture)
        self.source = QtWidgets.QLabel(tr("No face selected"))
        self.source.setTextFormat(QtCore.Qt.PlainText)
        self.source.setWordWrap(True)
        definition.addRow(self.source)
        self.create_datum = QtWidgets.QPushButton(tr("Create Datum Plane"))
        layout.addWidget(self.create_datum)
        self.create_datum.clicked.connect(self.create_attachment_plane)
        self.status = QtWidgets.QLabel(tr("Select the XY, XZ or YZ origin plane in the view, or choose a plane below. OK opens Sketcher."))
        self.status.setWordWrap(True)
        self.status.setTextFormat(QtCore.Qt.PlainText)
        layout.addWidget(self.status)
        self.capture.clicked.connect(self.capture_face)
        self.plane.currentIndexChanged.connect(self.update_plane)
        self.base.currentIndexChanged.connect(self.update_plane)
        self.orientation_mode.currentIndexChanged.connect(self.update_plane)
        self.direction_axis.currentIndexChanged.connect(self.update_axis)
        self.update_plane()
        from freecad.gui.ComponentNavigator import task_geometry
        selected = context.profile_selection if context else task_geometry(component, multiple=True)
        if len(selected) in (1, 2):
            self.capture_face(selected)
        origin = self.selected_origin()
        if origin:
            control = self.base if self.creating_plane() else self.plane
            control.setCurrentIndex(control.findData(origin))

    def creating_plane(self):
        return self.datum_only or self.plane.currentData() == "Create new plane"

    def update_axis(self, *args):
        axis = self.direction_axis.currentData()
        self.direction_rows[0][0].setText(tr(axis + "-axis direction"))
        for name, control in zip(("X", "Y", "Z"), self.directions[0]):
            control.setAccessibleName(tr(axis + "-axis direction") + " " + name)
        # Keep entered values when choosing which in-plane axis they describe.

    def selected_origin(self):
        entries = Gui.Selection.getSelectionEx("*", 0)
        if len(entries) != 1 or len(entries[0].SubElementNames) > 1:
            return None
        entry = entries[0]
        subname = entry.SubElementNames[0] if entry.SubElementNames else ""
        obj = entry.Object.getSubObject(subname, 1) if subname else entry.Object
        if obj is not None and obj.Document == self.component.Document and obj.Name in self.origin_planes:
            return self.origin_planes[obj.Name]
        return None

    def show_origin_planes(self):
        self.origin.ViewObject.setTemporaryOriginPlanes(True)
        Gui.Selection.addObserver(self, 0)
        self.observing = True

    def addSelection(self, document, name, subname, *args):
        if self.pick_role and self.creating_plane():
            self.capture_frame_pick(document, name, subname)
            return
        if document != self.component.Document.Name:
            return
        base = self.component.Document.getObject(name)
        if base is None:
            return
        obj = base.getSubObject(subname, 1) if subname else base
        if obj is None:
            return
        if obj.Name in self.origin_planes:
            control = self.base if self.creating_plane() else self.plane
            control.setCurrentIndex(control.findData(self.origin_planes[obj.Name]))
            self.status.setText(tr("Origin plane selected."))
        else:
            from freecad.gui.ComponentNavigator import task_geometry
            selected = task_geometry(self.component, multiple=True)
            if len(selected) in (1, 2):
                self.capture_face(selected)

    def update_plane(self, *args):
        new = self.creating_plane()
        independent = self.plane.currentData() == "Independent plane" and not self.datum_only
        defined = new or independent
        self.orientation_mode.model().item(0).setEnabled(not independent)
        if independent and self.orientation_mode.currentData() == "Projected references":
            self.orientation_mode.setCurrentIndex(1)
        self.follow_support.setEnabled(not independent)
        self.follow_support.setVisible(not independent and not self.datum_only)
        self.capture.setVisible(not independent)
        projected = new and self.orientation_mode.currentData() == "Projected references"
        self.sections[1].setVisible(projected)
        self.sections[3].setVisible(projected or (defined and self.orientation_mode.currentData() == "Axis directions"))
        for widget in (self.origin_source, self.origin_pick, self.origin_selection,
                       self.x_source, self.x_pick, self.x_selection, self.reverse_x):
            widget.setVisible(projected)
        self.orientation_mode.setVisible(defined)
        self.sections[0].layout().labelForField(self.orientation_mode).setVisible(defined)
        choice = self.base.currentData() if new else self.plane.currentData()
        self.base.setVisible(new)
        self.base_label.setVisible(new)
        self.user_plane.setVisible(choice == "User plane")
        self.user_plane_label.setVisible(choice == "User plane")
        self.source.setVisible(choice in ("Selected planar face", "Selected two edges"))
        for caption, control in zip(self.origin_labels, self.origins):
            caption.setVisible(defined and not projected)
            control.setVisible(defined and not projected)
        self.offset_label.setText(tr("Origin Z") if independent else tr("Surface offset") if new else tr("Offset"))
        self.sections[2].setVisible(defined)
        vectors = defined and self.orientation_mode.currentData() == "Axis directions"
        for caption, control in zip(self.rotation_labels, self.rotations):
            caption.setVisible(defined and not vectors)
            control.setVisible(defined and not vectors)
        self.direction_axis_label.setVisible(vectors)
        self.direction_axis.setVisible(vectors)
        self.direction_hint.setVisible(vectors)
        for caption, row in self.direction_rows:
            caption.setVisible(vectors)
            row.setVisible(vectors)
        self.direction_hint.setText(tr("Origin and directions are measured in the active component. Z sets the normal; X or Y is projected onto its plane.") if independent else
                                    tr("Directions and origin are measured in the base attachment frame. Z sets the normal; X or Y is projected onto its plane."))
        self.create_datum.setVisible(new and not self.datum_only)
        self.status.setText(tr("OK creates the datum plane. Cancel creates nothing.") if self.datum_only else
                            tr("Create Datum Plane makes it available below. OK creates the plane and sketch together; Cancel creates neither until the plane is explicitly created.")
                            if new else tr("Define the origin and orientation in component coordinates. The sketch has no support.") if independent else
                            tr("Choose a plane, planar face or two coplanar edges. Follow support retains the last valid frame if the support is unavailable. OK opens Sketcher."))

    def origin_source_changed(self, index):
        if index == 0:
            self.origin_reference = None
            self.origin_selection.setText(tr("Part origin"))
            self.pick_role = None
        else:
            self.start_frame_pick("origin")

    def x_source_changed(self, index):
        self.axis_references = []
        if index == 0:
            self.pick_role = None
            self.x_selection.setText(tr("Project the component axis closest to the plane. Ties use X, then Y, then Z."))
        else:
            self.start_frame_pick("axis")

    def start_frame_pick(self, role):
        if role == "origin":
            self.origin_source.blockSignals(True)
            self.origin_source.setCurrentIndex(1)
            self.origin_source.blockSignals(False)
            self.origin_reference = None
            self.origin_selection.setText(tr("Select a vertex or datum point."))
        else:
            if self.x_source.currentIndex() == 0:
                self.x_source.blockSignals(True)
                self.x_source.setCurrentIndex(1)
                self.x_source.blockSignals(False)
            self.axis_references = []
            self.x_selection.setText(tr("Select two vertices or datum points in order.") if self.x_source.currentIndex() == 2 else
                                     tr("Select an edge or datum axis. Curved edges use their midpoint tangent."))
        self.pick_role = role
        Gui.Selection.clearSelection()

    def capture_frame_pick(self, document, name, subname):
        import ComponentSketch as Sketch
        try:
            doc = App.listDocuments().get(document)
            base = doc.getObject(name) if doc else None
            obj = base.getSubObject(subname, 1) if base and subname else base
            element = subname.rsplit(".", 1)[-1] if subname else ""
            if not element.startswith(("Vertex", "Edge")):
                element = ""
            reference = (obj, [element] if element else [])
            point = self.pick_role == "origin" or self.x_source.currentIndex() == 2
            Sketch.reference_geometry(self.component, reference, point)
            if self.pick_role == "origin":
                self.origin_reference = reference
                self.origin_selection.setText(obj.Label + (" / " + element if element else ""))
                self.pick_role = None
            else:
                if reference not in self.axis_references:
                    self.axis_references.append(reference)
                self.x_selection.setText(" -> ".join(o.Label + (" / " + n[0] if n else "") for o, n in self.axis_references))
                if len(self.axis_references) == (2 if point else 1):
                    self.pick_role = None
            self.status.setText(tr("Reference selected. It will be projected onto the surface."))
        except Exception as error:
            self.status.setText(str(error))

    def capture_face(self, picks=None):
        import ComponentSketch as Sketch
        from freecad.gui.ComponentNavigator import task_geometry
        try:
            control = self.base if self.creating_plane() else self.plane
            origin = self.selected_origin() if not isinstance(picks, list) else None
            if origin:
                control.setCurrentIndex(control.findData(origin))
                self.status.setText(tr("Origin plane selected."))
                return
            selected = picks if isinstance(picks, list) else task_geometry(self.component, multiple=True)
            if len(selected) == 2 and not self.creating_plane():
                Sketch.two_edge_frame(self.component, selected)
                self.support = selected
                control.setCurrentIndex(control.findData("Selected two edges"))
                self.source.setText(" / ".join(obj.Label + ": " + name for obj, name in selected))
                self.status.setText(tr("Two edges selected. They define the sketch plane."))
                return
            if len(selected) != 1:
                raise ValueError(tr("Select a plane, one planar face, or two coplanar edges in the active component."))
            candidate = selected[0]
            if candidate[0] in Sketch.user_planes(self.component):
                Sketch.check_plane(self.component, candidate[0])
                self.user_plane.setCurrentIndex(self.user_plane.findData(candidate[0].Name))
                control.setCurrentIndex(control.findData("User plane"))
            else:
                self.support = Sketch.check_support(self.component, candidate)
                control.setCurrentIndex(control.findData("Selected planar face"))
                self.source.setText(self.support[0].Label + " / " + self.support[1])
            self.status.setText(tr("Support selected. Follow support keeps the last valid frame if the support becomes unavailable."))
        except Exception as error:
            self.status.setText(str(error))

    def getStandardButtons(self):
        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        return getattr(buttons, "value", buttons)

    def plane_values(self):
        choice = self.base.currentData() if self.creating_plane() else self.plane.currentData()
        support = (self.component.Document.getObject(self.user_plane.currentData())
                   if choice == "User plane" and self.user_plane.currentData() else self.support)
        directions = None
        if self.orientation_mode.currentData() == "Axis directions":
            directions = (self.direction_axis.currentData(),
                          *(tuple(control.value() for control in row) for row in self.directions))
        frame = None
        if self.creating_plane() and self.orientation_mode.currentData() == "Projected references":
            if self.origin_source.currentIndex() and self.origin_reference is None:
                raise ValueError(tr("Select an origin point or choose the projected part origin."))
            expected = (0, 1, 2)[self.x_source.currentIndex()]
            if len(self.axis_references) != expected:
                raise ValueError(tr("Select one edge or two points for the X direction."))
            frame = dict(origin_reference=self.origin_reference, axis_references=self.axis_references,
                         reverse_z=self.reverse_z.isChecked(), reverse_x=self.reverse_x.isChecked())
        return dict(frame=frame, base=choice, offset=float(self.offset.property("rawValue")), support=support,
                    angles=tuple(float(c.property("rawValue")) for c in self.rotations),
                    origin=tuple(float(c.property("rawValue")) for c in self.origins), directions=directions)

    def create_attachment_plane(self):
        import ComponentSketch as Sketch
        try:
            plane = Sketch.create_plane(self.component, **self.plane_values())
            self.user_plane.clear()
            for obj in Sketch.user_planes(self.component):
                self.user_plane.addItem(obj.Label, obj.Name)
            self.user_plane.setCurrentIndex(self.user_plane.findData(plane.Name))
            self.offset.setProperty("rawValue", 0)
            self.plane.setCurrentIndex(self.plane.findData("User plane"))
            self.status.setText(tr("Plane created and selected. OK opens the attached sketch. Cancel keeps the plane; Undo removes it."))
        except Exception as error:
            self.status.setText(str(error))

    def accept(self):
        import ComponentSketch as Sketch
        try:
            values = self.plane_values()
            if self.datum_only:
                self.result = Sketch.create_plane(self.component, **values)
            else:
                self.result = Sketch.create(self.component, self.plane.currentData(),
                                            values["offset"], values["support"], self.base.currentData(),
                                            values["angles"], values["origin"], values["directions"], values["frame"],
                                            follow_support=self.follow_support.isChecked())
        except Exception as error:
            self.status.setText(str(error))
            return False
        self.finish(restore=self.datum_only)
        if self.datum_only:
            return True
        # TaskView defers closeDialog() while the OK callback is running.
        # Enter Sketcher only after it has removed this task from the panel.
        QtCore.QTimer.singleShot(0, self.open_editor)
        return True

    def open_editor(self):
        try:
            App.setActiveDocument(self.component.Document.Name)
            gui = Gui.getDocument(self.component.Document.Name)
            if Gui.Control.activeDialog(gui):
                raise ValueError(tr("Close the current task before editing the new sketch."))
            Gui.Selection.clearSelection()
            if self.context:
                self.context.edit(self.result)
            elif not gui.setEdit(self.result.Name):
                raise ValueError(tr("The new sketch could not enter edit mode."))
        except Exception as error:
            if self.context:
                self.context.restore()
            App.Console.PrintError(str(error) + "\n")

    def reject(self):
        self.finish()
        return True

    def finish(self, restore=True):
        global _task
        if self.observing:
            Gui.Selection.removeObserver(self)
            self.observing = False
        self.origin.ViewObject.setTemporaryOriginPlanes(False)
        Gui.Control.closeDialog()
        _task = None
        if restore and self.context:
            self.context.restore()


def launch(component=None, datum_only=False):
    if datum_only:
        from freecad.gui.ComponentPlaneTask import launch as launch_plane
        return launch_plane(component)
    global _task
    if Gui.Control.activeDialog():
        raise ValueError(tr("Finish the current task before creating a sketch."))
    component = modeling_component(component or active_component())
    from freecad.gui.ComponentNavigator import TaskContext
    context = TaskContext(component)
    try:
        context.enter()
        _task = SketchTask(component, context, datum_only)
        Gui.Control.showDialog(_task)
        _task.show_origin_planes()
    except Exception:
        if _task:
            if _task.observing:
                Gui.Selection.removeObserver(_task)
            _task.origin.ViewObject.setTemporaryOriginPlanes(False)
            Gui.Control.closeDialog()
        _task = None
        context.restore()
        raise
    return _task


class DatumPlaneCommand:
    def GetResources(self):
        return {"MenuText": tr("Datum Plane"), "ToolTip": tr("Create an attached datum plane in the active component"),
                "Pixmap": "Std_Plane"}

    def IsActive(self):
        if Gui.Control.activeDialog():
            return False
        try:
            active_component()
            return True
        except (ValueError, RuntimeError):
            return False

    def Activated(self):
        launch(datum_only=True)


def install_datum_command():
    if not Gui.Command.get("Std_ComponentDatumPlane"):
        Gui.addCommand("Std_ComponentDatumPlane", DatumPlaneCommand())
