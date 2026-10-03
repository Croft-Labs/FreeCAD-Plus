# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component sketch-plane choice followed by the native Sketcher editor."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.ComponentExtrudeTask import active_component, CompactFormLayout

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
        self.sections = []
        for title in ("Define Plane", "Define Origin", "Define Orientation"):
            section = QtWidgets.QGroupBox(tr(title))
            CompactFormLayout(section)
            layout.addWidget(section)
            self.sections.append(section)
        definition, origin, orientation = [section.layout() for section in self.sections]
        self.base = QtWidgets.QComboBox()
        for name in Sketch.PLANES[:-1]:
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
        origin.addRow(self.offset_label, self.offset)
        self.orientation_mode = QtWidgets.QComboBox()
        for name in ("Rotation angles", "Axis directions"):
            self.orientation_mode.addItem(tr(name), name)
        orientation.addRow(tr("Orientation"), self.orientation_mode)
        self.rotations = []
        self.rotation_labels = []
        for label in ("Rotation X", "Rotation Y", "Rotation Z"):
            control = Gui.UiLoader().createWidget("Gui::QuantitySpinBox")
            control.setProperty("unit", "deg")
            control.setProperty("minimum", -360.0)
            control.setProperty("maximum", 360.0)
            caption = QtWidgets.QLabel(tr(label))
            orientation.addRow(caption, control)
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
        self.capture = QtWidgets.QPushButton(tr("Use selected face or plane"))
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
        selected = context.selection if context else task_geometry(component)
        if len(selected) == 1:
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
            selected = task_geometry(self.component)
            if len(selected) == 1:
                self.capture_face(selected)

    def update_plane(self, *args):
        new = self.creating_plane()
        choice = self.base.currentData() if new else self.plane.currentData()
        self.base.setVisible(new)
        self.base_label.setVisible(new)
        self.user_plane.setVisible(choice == "User plane")
        self.user_plane_label.setVisible(choice == "User plane")
        self.source.setVisible(choice == "Selected planar face")
        for caption, control in zip(self.origin_labels, self.origins):
            caption.setVisible(new)
            control.setVisible(new)
        self.offset_label.setText(tr("Origin Z / Offset") if new else tr("Offset"))
        self.sections[2].setVisible(new)
        vectors = self.orientation_mode.currentData() == "Axis directions"
        for caption, control in zip(self.rotation_labels, self.rotations):
            caption.setVisible(not vectors)
            control.setVisible(not vectors)
        self.direction_axis_label.setVisible(vectors)
        self.direction_axis.setVisible(vectors)
        self.direction_hint.setVisible(vectors)
        for caption, row in self.direction_rows:
            caption.setVisible(vectors)
            row.setVisible(vectors)
        self.create_datum.setVisible(new and not self.datum_only)
        self.status.setText(tr("OK creates the datum plane. Cancel creates nothing.") if self.datum_only else
                            tr("Create Datum Plane makes it available below. OK creates the plane and sketch together; Cancel creates neither until the plane is explicitly created.")
                            if new else tr("Select an origin plane, a user plane, or a planar face. OK opens Sketcher."))

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
            selected = picks if isinstance(picks, list) else task_geometry(self.component)
            if len(selected) != 1:
                raise ValueError(tr("Select one planar face in the active component."))
            candidate = selected[0]
            if candidate[0] in Sketch.user_planes(self.component):
                Sketch.check_plane(self.component, candidate[0])
                self.user_plane.setCurrentIndex(self.user_plane.findData(candidate[0].Name))
                control.setCurrentIndex(control.findData("User plane"))
            else:
                self.support = Sketch.check_support(self.component, candidate)
                control.setCurrentIndex(control.findData("Selected planar face"))
                self.source.setText(self.support[0].Label + " / " + self.support[1])
            self.status.setText(tr("Ready. The attachment will follow this support."))
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
        return dict(base=choice, offset=float(self.offset.property("rawValue")), support=support,
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
                                            values["angles"], values["origin"], values["directions"])
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
    global _task
    if Gui.Control.activeDialog():
        raise ValueError(tr("Finish the current task before creating a sketch."))
    component = component or active_component()
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
        return bool(App.ActiveDocument and sum(getattr(obj, "ComponentRole", "") == "Document"
                                              for obj in App.ActiveDocument.Objects) == 1
                    and not Gui.Control.activeDialog())

    def Activated(self):
        launch(datum_only=True)


def install_datum_command():
    if not Gui.Command.get("Std_ComponentDatumPlane"):
        Gui.addCommand("Std_ComponentDatumPlane", DatumPlaneCommand())
