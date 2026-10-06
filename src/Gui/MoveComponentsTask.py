# SPDX-License-Identifier: LGPL-2.1-or-later
"""Single task panel for parent-owned component placement workflows."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui import MoveComponents as Move
from freecad.gui import ComponentNavigator as Navigator
from freecad.gui import ComponentSelection as Selection
from freecad.gui import DesignSelection
from freecad.gui.ComponentTaskWidgets import CompactFormLayout, CurveCollector, ModelingTaskUI
from freecad.gui.OccurrenceMove import Ghost

_task = None


def tr(text):
    return App.Qt.translate("MoveComponents", text)


class MoveTask(ModelingTaskUI):
    def __init__(self, root, paths=()):
        self.session = Move.Session(root)
        mdi = Gui.getMainWindow().findChild(QtWidgets.QMdiArea)
        self.mdi, self.window = mdi, mdi.activeSubWindow() if mdi else None
        self.closed = self.selecting = self.applying = False
        self.ghosts = []
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle(tr("Move Components"))
        layout = CompactFormLayout(self.form)
        self.workflow = QtWidgets.QComboBox()
        self.workflow.addItems([tr(name) for name in Move.WORKFLOWS])
        layout.addRow(tr("Workflow"), self.workflow)
        self.collector = CurveCollector(root, source_label=None, curves_label="Components", height=110,
                                        actions=(("Add selection", self.collect), ("Remove", self.remove),
                                                 ("Clear", self.clear)), remove=self.remove)
        self.collector.curves.focusReceived.connect(self.collect_components)
        layout.addRow(self.collector)
        self.context = QtWidgets.QLabel(tr("Select whole component instances in Part Tree."))
        self.context.setWordWrap(True)
        layout.addRow(self.context)
        self.translate_fields = QtWidgets.QWidget()
        fields = CompactFormLayout(self.translate_fields)
        self.direction = QtWidgets.QComboBox()
        self.direction.addItems([tr(name) for name in ("Choose direction", "Parent X", "Parent Y", "Parent Z", "Pick straight reference")])
        fields.addRow(tr("Direction"), self.direction)
        self.reference = QtWidgets.QLabel()
        self.reference.setWordWrap(True)
        fields.addRow(self.reference)
        self.reverse = QtWidgets.QPushButton(tr("Reverse"))
        self.reverse.setCheckable(True)
        self.distance = self.quantity()
        self.distance.setProperty("minimum", 0.)
        fields.addRow(tr("Distance"), self.distance)
        layout.addRow(self.translate_fields)
        self.rotate_fields = QtWidgets.QWidget()
        rotation = CompactFormLayout(self.rotate_fields)
        self.axis_choice = QtWidgets.QComboBox()
        self.axis_choice.addItems([tr(name) for name in ("Choose axis", "Parent X", "Parent Y", "Parent Z",
                                                       "Pick straight reference", "Two points")])
        rotation.addRow(tr("Axis"), self.axis_choice)
        self.axis_pick = QtWidgets.QPushButton(tr("Pick axis again"))
        self.axis_pick.clicked.connect(self.change_axis)
        rotation.addRow(self.axis_pick)
        self.pivot_pick = QtWidgets.QPushButton(tr("Pick pivot point"))
        self.pivot_pick.clicked.connect(lambda: self.begin_pick("pivot"))
        self.pivot_clear = QtWidgets.QPushButton(tr("Use axis location"))
        self.pivot_clear.clicked.connect(self.clear_pivot)
        rotation.addRow(self.pivot_pick, self.pivot_clear)
        self.angle = self.quantity(unit="deg")
        self.angle.setProperty("minimum", 0.)
        self.angle.setProperty("maximum", 360.)
        rotation.addRow(tr("Angle (0–360°)"), self.angle)
        self.resolved = QtWidgets.QLabel()
        self.resolved.setWordWrap(True)
        self.resolved.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.resolved.setTextFormat(QtCore.Qt.PlainText)
        rotation.addRow(self.resolved)
        rule = QtWidgets.QLabel(tr("Positive rotation follows the right-hand rule about the axis arrow. Reverse negates the angle."))
        rule.setWordWrap(True)
        rotation.addRow(rule)
        layout.addRow(self.rotate_fields)
        self.rotate_fields.hide()
        self.point_fields = QtWidgets.QWidget()
        points = CompactFormLayout(self.point_fields)
        self.source_pick = QtWidgets.QPushButton(tr("Pick Source point"))
        self.destination_pick = QtWidgets.QPushButton(tr("Pick Destination point"))
        self.source_pick.clicked.connect(lambda: self.begin_pick("source_point"))
        self.destination_pick.clicked.connect(lambda: self.begin_pick("destination_point"))
        points.addRow(self.source_pick)
        points.addRow(self.destination_pick)
        self.point_resolved = QtWidgets.QLabel()
        self.point_resolved.setWordWrap(True)
        points.addRow(self.point_resolved)
        layout.addRow(self.point_fields)
        self.point_fields.hide()
        self.axes_fields = QtWidgets.QWidget()
        axes = CompactFormLayout(self.axes_fields)
        self.source_axis_pick = QtWidgets.QPushButton(tr("Pick Source axis"))
        self.target_axis_pick = QtWidgets.QPushButton(tr("Pick Target axis"))
        self.source_axis_pick.clicked.connect(lambda: self.begin_pick("source_axis"))
        self.target_axis_pick.clicked.connect(lambda: self.begin_pick("target_axis"))
        axes.addRow(self.source_axis_pick)
        axes.addRow(self.target_axis_pick)
        self.alignment_policy = QtWidgets.QComboBox()
        self.alignment_policy.addItems([tr("Make Coincident"), tr("Make Parallel")])
        axes.addRow(tr("Alignment"), self.alignment_policy)
        self.target_reverse = QtWidgets.QPushButton(tr("Reverse Target Direction"))
        self.target_reverse.setCheckable(True)
        axes.addRow(self.target_reverse)
        self.axes_resolved = QtWidgets.QLabel()
        self.axes_resolved.setWordWrap(True)
        axes.addRow(self.axes_resolved)
        self.alignment_policy.currentIndexChanged.connect(self.update_preview)
        self.target_reverse.toggled.connect(self.update_preview)
        layout.addRow(self.axes_fields)
        self.axes_fields.hide()
        self.frame_fields = QtWidgets.QWidget()
        frames = CompactFormLayout(self.frame_fields)
        self.frame_parts = {"source": {}, "target": {}}
        self.frame_labels = {}
        for side, caption in (("source", "Source"), ("target", "Target")):
            box = QtWidgets.QWidget()
            form = CompactFormLayout(box)
            pick = QtWidgets.QPushButton(tr("Pick " + caption + " coordinate system"))
            pick.clicked.connect(lambda checked=False, role=side+"_frame": self.begin_pick(role))
            parent = QtWidgets.QPushButton(tr("Use Parent coordinate system"))
            parent.clicked.connect(lambda checked=False, role=side: self.parent_frame(role))
            frames.addRow(pick)
            frames.addRow(parent)
            toggle = QtWidgets.QToolButton()
            toggle.setText(tr("Define " + caption + " Origin, Z and X"))
            toggle.setCheckable(True)
            toggle.toggled.connect(box.setVisible)
            frames.addRow(toggle)
            for part, label in (("origin", "Origin"), ("z", "Z direction"), ("x", "X direction")):
                button = QtWidgets.QPushButton(tr("Pick " + label))
                button.clicked.connect(lambda checked=False, role=side+"_"+part: self.begin_pick(role))
                form.addRow(button)
            frames.addRow(box)
            box.hide()
            label = QtWidgets.QLabel()
            label.setWordWrap(True)
            self.frame_labels[side] = label
            frames.addRow(label)
        layout.addRow(self.frame_fields)
        self.frame_fields.hide()
        self.manipulator = None
        self.saved_pivot = None
        self.interactive_fields = QtWidgets.QWidget()
        interactive = CompactFormLayout(self.interactive_fields)
        self.pivot_mode = QtWidgets.QComboBox()
        self.pivot_mode.addItems([tr("Move Components"), tr("Edit Pivot")])
        interactive.addRow(tr("Mode"), self.pivot_mode)
        self.pivot_mode.currentIndexChanged.connect(self.change_pivot_mode)
        self.interactive_pivot_pick = QtWidgets.QPushButton(tr("Pick pivot point or edge midpoint"))
        self.interactive_pivot_pick.clicked.connect(lambda: self.begin_pick("interactive_point"))
        interactive.addRow(self.interactive_pivot_pick)
        orientation = QtWidgets.QPushButton(tr("Pick pivot orientation axis"))
        orientation.clicked.connect(lambda: self.begin_pick("interactive_axis"))
        interactive.addRow(orientation)
        frame = QtWidgets.QPushButton(tr("Pick pivot orientation frame"))
        frame.clicked.connect(lambda: self.begin_pick("interactive_frame"))
        interactive.addRow(frame)
        self.pivot_reset = QtWidgets.QPushButton(tr("Reset Pivot"))
        self.pivot_reset.clicked.connect(self.reset_pivot)
        interactive.addRow(self.pivot_reset)
        from freecad.gui.MoveComponentsManipulator import HANDLES
        self.active_handle = QtWidgets.QComboBox()
        self.active_handle.addItems([tr(name) for name in HANDLES])
        interactive.addRow(tr("Active handle"), self.active_handle)
        self.handle_distance, self.handle_secondary = self.quantity(), self.quantity()
        self.handle_angle = self.quantity(unit="deg")
        interactive.addRow(tr("Distance"), self.handle_distance)
        interactive.addRow(tr("Plane second distance"), self.handle_secondary)
        interactive.addRow(tr("Angle"), self.handle_angle)
        numeric = QtWidgets.QPushButton(tr("Preview numeric gesture"))
        numeric.clicked.connect(self.numeric_gesture)
        interactive.addRow(numeric)
        self.translation_snap = QtWidgets.QCheckBox(tr("Snap distance"))
        self.rotation_snap = QtWidgets.QCheckBox(tr("Snap angle"))
        self.snap_distance, self.snap_angle = self.quantity(1.), self.quantity(15., unit="deg")
        self.snap_distance.setProperty("minimum", 1e-7)
        self.snap_angle.setProperty("minimum", 1e-7)
        interactive.addRow(self.translation_snap, self.snap_distance)
        interactive.addRow(self.rotation_snap, self.snap_angle)
        for widget in (self.translation_snap, self.rotation_snap):
            widget.toggled.connect(self.configure_snap)
        for widget in (self.snap_distance, self.snap_angle):
            widget.valueChanged.connect(self.configure_snap)
        self.pivot_resolved = QtWidgets.QLabel()
        self.pivot_resolved.setWordWrap(True)
        interactive.addRow(self.pivot_resolved)
        layout.addRow(self.interactive_fields)
        self.interactive_fields.hide()
        self.reference_objects = {}
        layout.addRow(self.reverse)
        self.reset_button = QtWidgets.QPushButton(tr("Reset movement inputs"))
        self.reset_button.clicked.connect(self.reset)
        layout.addRow(self.reset_button)
        self.status = QtWidgets.QLabel()
        self.status.setWordWrap(True)
        self.status.setTextFormat(QtCore.Qt.PlainText)
        layout.addRow(self.status)
        self.workflow.currentIndexChanged.connect(self.change_workflow)
        self.direction.currentIndexChanged.connect(self.change_direction)
        self.axis_choice.currentIndexChanged.connect(self.change_axis)
        self.angle.valueChanged.connect(self.update_preview)
        self.reverse.toggled.connect(self.update_preview)
        self.distance.valueChanged.connect(self.update_preview)
        self.selection_timer = QtCore.QTimer(self.form)
        self.selection_timer.setSingleShot(True)
        self.selection_timer.timeout.connect(self.collect)
        self.monitor = QtCore.QTimer(self.form)
        self.monitor.setInterval(150)
        self.monitor.timeout.connect(self.check_context)
        self.monitor.start()
        self.picking_reference = False
        self.first_point = None
        Gui.Selection.addObserver(self)
        App.addDocumentObserver(self)
        if paths:
            self.add_paths(paths)

    def getStandardButtons(self):
        flags = QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        return flags.value if hasattr(flags, "value") else int(flags)

    def isAllowedAlterDocument(self):
        return False

    def isAllowedAlterView(self):
        return True

    def isAllowedAlterSelection(self):
        return True

    def bind_parent(self):
        session = self.session
        dock = Navigator._dock
        if dock:
            dock.root_key = Navigator.object_key(session.root)
            dock.active_key = Navigator.object_key(session.parent)
            dock.active_path = list(session.parent_path)
            dock.bind_edit_context()
            dock.refresh()
        else:
            Gui.activeDocument().activeView().setActiveObject(
                "part", session.root, Selection.native_path(session.root, session.parent_path))
        self.context.setText(tr("Editing parent: ") + session.parent.Label + tr(
            ". Moves change its child placements in every instance of this parent."))

    def add_paths(self, paths):
        try:
            self.session.add(paths)  # Validate the complete batch before changing context/list.
            self.bind_parent()
            self.reset()
            self.refresh_list()
            self.highlight()
        except Exception as error:
            self.clear_preview()
            self.status.setText(str(error))
            return False
        return True

    def refresh_list(self):
        self.collector.curves.clear()
        for path, link in zip(self.session.paths, self.session.links()):
            row = QtWidgets.QListWidgetItem(link.Label + " #" + str(link.InstanceNumber))
            row.setData(QtCore.Qt.UserRole, path)
            row.setToolTip(Selection.native_path(self.session.root, path))
            self.collector.curves.addItem(row)

    def highlight(self):
        self.selecting = True
        try:
            Gui.Selection.clearSelection()
            for path in self.session.paths:
                Gui.Selection.addSelection(self.session.root, Selection.native_path(self.session.root, path))
        finally:
            self.selecting = False

    def collect_components(self):
        self.picking_reference = False

    def begin_pick(self, role):
        if self.session.parent is None:
            self.status.setText(tr("Select components first."))
            return
        self.picking_reference = role
        if self.manipulator:
            self.saved_pivot = App.Placement(self.manipulator.pivot)
            self.stop_manipulator()
        self.selecting = True
        try:
            Gui.Selection.clearSelection()
        finally:
            self.selecting = False
        self.clear_preview()
        instructions = {"axis": "Pick a straight line, edge or reference axis.",
                        "first": "Pick the first axis point (axis location).",
                        "second": "Pick a distinct second point (positive axis direction).",
                        "pivot": "Pick a vertex, point, origin or circular edge center for the pivot.",
                        "source_point": "Pick the Source vertex, point, origin or circle center.",
                        "destination_point": "Pick the Destination vertex, point, origin or circle center."}
        instructions.update({"source_axis": "Pick a Source straight line, reference axis, circle or cylindrical face.",
                             "target_axis": "Pick a Target straight line, reference axis, circle or cylindrical face."})
        for side in ("source", "target"):
            instructions.update({side+"_frame": "Pick a native origin or datum coordinate system.",
                                 side+"_origin": "Pick the frame Origin point.",
                                 side+"_z": "Pick the positive Z direction line or axis.",
                                 side+"_x": "Pick an X direction not parallel to Z."})
        instructions.update({"interactive_point": "Pick a pivot point, origin, circle center or edge midpoint.",
                             "interactive_axis": "Pick a positive pivot Z axis; the perpendicular X is deterministic.",
                             "interactive_frame": "Pick a native origin or datum frame for pivot orientation."})
        self.status.setText(tr(instructions[role]))

    def clear_pivot(self):
        self.session.pivot = None
        self.reference_objects.pop("pivot", None)
        self.picking_reference = False
        self.highlight()
        self.update_preview()

    def change_axis(self):
        self.session.axis = self.session.pivot = self.first_point = None
        for role in ("axis", "first", "second", "pivot"):
            self.reference_objects.pop(role, None)
        self.picking_reference = False
        index = self.axis_choice.currentIndex()
        self.axis_pick.setEnabled(index in (4, 5))
        if 1 <= index <= 3:
            self.session.axis = (App.Vector(), App.Vector(*((1, 0, 0), (0, 1, 0), (0, 0, 1))[index - 1]))
        self.update_preview()
        if index in (4, 5):
            self.begin_pick("axis" if index == 4 else "first")

    def collect(self):
        if self.closed or self.selecting:
            return
        try:
            entries = Gui.Selection.getSelectionEx("*", 0)
            if self.picking_reference:
                if len(entries) != 1 or len(entries[0].SubElementNames) > 1:
                    raise ValueError(tr("Pick one reference at a time."))
                entry = entries[0]
                subname = entry.SubElementNames[0] if entry.SubElementNames else ""
                role = self.picking_reference
                if role.startswith("interactive_"):
                    self.ensure_manipulator(self.saved_pivot)
                    if role == "interactive_point":
                        self.manipulator.pivot.Base = Move.reference_point(self.session, entry.Object, subname, midpoint=True)
                    elif role == "interactive_frame":
                        self.manipulator.pivot.Rotation = Move.reference_frame(self.session, entry.Object, subname).Rotation
                    else:
                        direction = Move.reference_alignment_axis(self.session, entry.Object, subname)[1]
                        basis = min((App.Vector(1,0,0), App.Vector(0,1,0), App.Vector(0,0,1)),
                                    key=lambda axis: abs(direction.dot(axis)))
                        self.manipulator.pivot.Rotation = Move.frame_from_references(self.manipulator.pivot.Base, direction, basis).Rotation
                    self.manipulator.write()
                    self.saved_pivot = None
                elif role == "direction":
                    self.session.direction = Move.reference_direction(self.session, entry.Object, subname)
                    self.reference.setText(entry.Object.Label + (" / " + subname if subname else ""))
                elif role == "axis":
                    self.session.axis = Move.reference_axis(self.session, entry.Object, subname)
                elif role in ("source_axis", "target_axis"):
                    setattr(self.session, role, Move.reference_alignment_axis(self.session, entry.Object, subname))
                elif role in ("source_frame", "target_frame"):
                    setattr(self.session, role, Move.reference_frame(self.session, entry.Object, subname))
                    self.frame_parts[role.split("_")[0]].clear()
                elif role in ("source_z", "source_x", "target_z", "target_x"):
                    side, part = role.split("_")
                    self.frame_parts[side][part] = Move.reference_alignment_axis(self.session, entry.Object, subname)[1]
                    setattr(self.session, side+"_frame", None)
                else:
                    point = Move.reference_point(self.session, entry.Object, subname)
                    if role == "first":
                        self.first_point = point
                        self.reference_objects[role] = (entry.Object.Document, entry.Object.Name, entry.Object)
                        self.begin_pick("second")
                        return
                    if role == "second":
                        self.session.axis = Move.axis_from_points(self.first_point, point)
                    elif role == "pivot":
                        self.session.pivot = point
                    elif role in ("source_point", "destination_point"):
                        setattr(self.session, role, point)
                    elif role in ("source_origin", "target_origin"):
                        side, part = role.split("_")
                        self.frame_parts[side][part] = point
                        setattr(self.session, side+"_frame", None)
                self.reference_objects[role] = (entry.Object.Document, entry.Object.Name, entry.Object)
                if role in ("source_frame", "target_frame"):
                    side = role.split("_")[0]
                    for part in ("origin", "z", "x"):
                        self.reference_objects.pop(side+"_"+part, None)
                elif role in ("source_origin", "source_z", "source_x", "target_origin", "target_z", "target_x"):
                    self.reference_objects.pop(role.split("_")[0]+"_frame", None)
                self.picking_reference = False
                self.highlight()
                self.update_preview()
            else:
                paths = Move.selection_paths(self.session.root, entries)
                if paths and any(path not in self.session.paths for path in paths):
                    self.add_paths(paths)
        except Exception as error:
            self.clear_preview()
            self.status.setText(str(error))

    def addSelection(self, *args):
        if not self.selecting:
            self.selection_timer.start(0)

    def remove(self):
        removed = [tuple(row.data(QtCore.Qt.UserRole)) for row in self.collector.curves.selectedItems()]
        self.session.paths = [path for path in self.session.paths if path not in removed]
        self.reset()
        self.refresh_list()
        self.highlight()

    def clear(self):
        self.session.paths = []
        self.reset()
        self.refresh_list()
        self.highlight()

    def clear_preview(self):
        for ghost in self.ghosts:
            ghost.remove()
        self.ghosts = []

    def reset(self):
        self.stop_manipulator()
        self.clear_preview()
        self.session.reset()
        self.picking_reference = False
        self.first_point = None
        self.reference_objects.clear()
        self.saved_pivot = None
        self.point_resolved.clear()
        self.axes_resolved.clear()
        for side in ("source", "target"):
            self.frame_parts[side].clear()
            self.frame_labels[side].clear()
        for widget, setter, value in ((self.alignment_policy, self.alignment_policy.setCurrentIndex, 0),
                                     (self.target_reverse, self.target_reverse.setChecked, False)):
            widget.blockSignals(True)
            setter(value)
            widget.blockSignals(False)
        for widget, setter, value in ((self.direction, self.direction.setCurrentIndex, 0),
                                      (self.axis_choice, self.axis_choice.setCurrentIndex, 0),
                                      (self.reverse, self.reverse.setChecked, False)):
            widget.blockSignals(True)
            setter(value)
            widget.blockSignals(False)
        self.distance.blockSignals(True)
        self.distance.setProperty("rawValue", 0.)
        self.distance.blockSignals(False)
        self.angle.blockSignals(True)
        self.angle.setProperty("rawValue", 0.)
        self.angle.blockSignals(False)
        self.resolved.clear()
        self.axis_pick.setEnabled(False)
        self.reference.clear()
        for widget in (self.handle_distance, self.handle_secondary, self.handle_angle):
            widget.setProperty("rawValue", 0.)
        self.pivot_mode.blockSignals(True)
        self.pivot_mode.setCurrentIndex(0)
        self.pivot_mode.blockSignals(False)
        self.pivot_resolved.clear()
        if self.workflow.currentIndex() == 5 and self.session.paths:
            self.ensure_manipulator()
        instructions = ("Choose a direction and distance. Teal geometry previews the move.",
                        "Choose an axis and angle. Teal geometry previews the move.",
                        "Pick Source and Destination. Orientations and group spacing are preserved.",
                        "Pick Source and Target axes. Coincident uses the closest target point.",
                        "Define complete Source and Target coordinate systems.",
                        "Drag native handles. Release retains preview; Apply commits.")
        self.status.setText(tr(instructions[self.workflow.currentIndex()]))

    def change_workflow(self):
        self.reset()
        mode = self.workflow.currentIndex()
        self.translate_fields.setVisible(mode == 0)
        self.rotate_fields.setVisible(mode == 1)
        self.point_fields.setVisible(mode == 2)
        self.axes_fields.setVisible(mode == 3)
        self.frame_fields.setVisible(mode == 4)
        self.interactive_fields.setVisible(mode == 5)
        self.reverse.setVisible(mode in (0, 1))
        if mode == 2:
            self.status.setText(tr("Pick Source and Destination. Orientations and group spacing are preserved."))
        if mode == 3:
            self.status.setText(tr("Pick Source and Target axes. Coincident maps the source anchor to the closest target point."))
        if mode == 4:
            self.status.setText(tr("Pick complete coordinate systems or define Origin, Z and X for each frame."))
        if mode == 5:
            self.status.setText(tr("Drag arrows, plane handles or rings. Release retains preview; Apply commits. Edit Pivot changes handles only."))

    def change_direction(self):
        index = self.direction.currentIndex()
        self.session.direction = App.Vector(*((1, 0, 0), (0, 1, 0), (0, 0, 1))[index - 1]) if 1 <= index <= 3 else None
        self.reference.clear()
        self.picking_reference = "direction" if index == 4 else False
        if self.picking_reference:
            self.selecting = True
            try:
                Gui.Selection.clearSelection()
            finally:
                self.selecting = False
        self.update_preview()
        if self.picking_reference:
            self.status.setText(tr("Pick a visible straight edge, line or reference axis in the viewport."))

    def delta(self, preview=False):
        mode = self.workflow.currentIndex()
        if mode not in range(6):
            raise ValueError(tr("Choose a movement workflow."))
        for document, name, obj in self.reference_objects.values():
            if document.getObject(name) != obj or "Invalid" in obj.State:
                raise ValueError(tr("A picked reference is unavailable or invalid. Reset and pick again."))
        if mode == 5:
            if self.picking_reference or (not preview and self.manipulator and self.manipulator.dragging):
                raise ValueError(tr("Finish the current pivot pick or release the drag before applying."))
            return self.session.interactive_delta
        if mode == 4:
            if self.picking_reference:
                raise ValueError(tr("Finish the pending coordinate-system pick before applying."))
            if not any(self.frame_parts.values()) and self.session.source_frame is None and self.session.target_frame is None:
                return App.Placement()
            for side in ("source", "target"):
                parts = self.frame_parts[side]
                if parts:
                    if set(parts) != {"origin", "z", "x"}:
                        missing = ", ".join(key for key in ("origin", "z", "x") if key not in parts)
                        raise ValueError(tr(side.title()+" frame still needs: ") + missing)
                    setattr(self.session, side+"_frame", Move.frame_from_references(parts["origin"], parts["z"], parts["x"]))
            return self.session.align_frames()
        if mode == 3:
            if self.picking_reference:
                raise ValueError(tr("Finish the pending axis pick before applying."))
            if self.session.source_axis is None and self.session.target_axis is None:
                return App.Placement()
            self.session.coincident = self.alignment_policy.currentIndex() == 0
            self.session.reverse_target = self.target_reverse.isChecked()
            return self.session.align_axes()
        if mode == 2:
            if self.picking_reference:
                raise ValueError(tr("Finish the pending point pick before applying."))
            if self.session.source_point is None and self.session.destination_point is None:
                return App.Placement()
            return self.session.point_to_point()
        self.session.reverse = self.reverse.isChecked()
        if mode == 1:
            if not self.angle.hasAcceptableInput():
                raise ValueError(tr("Enter a valid angle between 0 and 360 degrees."))
            self.session.angle = float(self.angle.property("rawValue"))
            if self.session.angle and self.picking_reference:
                raise ValueError(tr("Complete the pending axis or pivot pick before applying rotation."))
            return self.session.rotation()
        if not self.distance.hasAcceptableInput():
            raise ValueError(tr("Enter a valid nonnegative distance."))
        self.session.distance = float(self.distance.property("rawValue"))
        return self.session.translation()

    def update_preview(self, *args):
        self.clear_preview()
        self.resolved.clear()
        try:
            delta = self.delta(preview=True)
            if not self.session.paths:
                return
            shapes = self.session.preview_shapes(delta)
            if not delta.isIdentity():
                for shape in shapes:
                    self.ghosts.append(Ghost(shape))
            if self.workflow.currentIndex() == 5 and self.manipulator:
                self.pivot_resolved.setText(tr("Parent-frame pivot: ") + ", ".join(
                    App.Units.Quantity(str(v)+" mm").UserString for v in self.manipulator.pivot.Base))
            if self.workflow.currentIndex() == 2:
                source, target = self.session.source_point, self.session.destination_point
                if source is not None and target is not None:
                    def position(point):
                        return ", ".join(App.Units.Quantity(str(v) + " mm").UserString for v in point)
                    self.point_resolved.setText(tr("Source: ") + position(source) + "\n" +
                                                tr("Destination: ") + position(target) + "\n" +
                                                tr("Distance: ") + App.Units.Quantity(str((target-source).Length) + " mm").UserString)
                    size = max([shape.BoundBox.DiagonalLength * .04 for shape in shapes] or [.5])
                    self.ghosts.append(Ghost(Move.point_marker(self.session, (source, target), size), color=(1., .55, .05)))
            if self.workflow.currentIndex() == 3 and self.session.source_axis and self.session.target_axis:
                source, direction = self.session.source_axis
                target, target_direction = self.session.target_axis
                if self.session.reverse_target:
                    target_direction = -target_direction
                size = max([shape.BoundBox.DiagonalLength for shape in shapes] or [10.])
                mapped = (delta.multVec(source), delta.Rotation.multVec(direction))
                self.ghosts.append(Ghost(Move.axis_geometry(self.session, (mapped,), size), color=(.1, .8, .8)))
                self.ghosts.append(Ghost(Move.axis_geometry(self.session, ((target, target_direction),), size), color=(1., .55, .05)))
                self.axes_resolved.setText(tr("Source anchor stays fixed in Parallel; Coincident uses the nearest point on Target. Minimal-angle rotation preserves roll."))
            if self.workflow.currentIndex() == 4:
                source, target = self.session.source_frame, self.session.target_frame
                if source is not None and target is not None:
                    size = max([shape.BoundBox.DiagonalLength * .25 for shape in shapes] or [10.])
                    self.ghosts.append(Ghost(Move.frame_geometry(self.session, (source,), size), color=(.1, .8, .8)))
                    self.ghosts.append(Ghost(Move.frame_geometry(self.session, (target,), size), color=(1., .55, .05)))
                    for side, frame in (("source", source), ("target", target)):
                        origin = ", ".join(App.Units.Quantity(str(v)+" mm").UserString for v in frame.Base)
                        self.frame_labels[side].setText(tr(side.title()+" origin in parent: ") + origin)
            if self.workflow.currentIndex() == 1 and self.session.axis is not None:
                point, direction = self.session.resolved_axis()
                position = ", ".join(App.Units.Quantity(str(v) + " mm").UserString for v in point)
                self.resolved.setText(tr("Parent-frame pivot: ") + position + "\n" + tr("Positive axis: ")
                                      + ", ".join("{:.6g}".format(v) for v in direction) + "\n"
                                      + tr("Signed angle: ") + App.Units.Quantity(
                                          str(-self.session.angle if self.session.reverse else self.session.angle) + " deg").UserString)
                self.resolved.updateGeometry()
                size = max([shape.BoundBox.DiagonalLength for shape in shapes] or [10.])
                self.ghosts.append(Ghost(Move.axis_marker(self.session, size), color=(1., .55, .05)))
            self.status.setText(tr("Preview only. Apply commits one undoable move for all listed siblings."))
        except Exception as error:
            self.clear_preview()
            self.status.setText(str(error))

    def apply(self):
        self.applying = True
        try:
            delta = self.delta()
            if delta.isIdentity():
                self.reset()
                return True
            changed = self.session.commit(delta)
            if changed:
                self.reset()
                if not DesignSelection.persistent():
                    self.stop_manipulator()
                    self.session.paths = []
                    self.session.reset()
                self.refresh_list()
                self.highlight()
            return True
        except Exception as error:
            self.clear_preview()
            self.status.setText(str(error))
            return False
        finally:
            self.applying = False

    def clicked(self, button):
        apply = QtWidgets.QDialogButtonBox.Apply
        value = button.value if hasattr(button, "value") else int(button)
        if value == (apply.value if hasattr(apply, "value") else int(apply)):
            self.apply()

    def accept(self):
        # After Apply or an unavailable workflow with no movement, OK only closes.
        if not self.apply():
            return False
        self.close()
        return True

    def parent_frame(self, side):
        if self.session.parent is None:
            self.status.setText(tr("Select components first."))
            return
        self.frame_parts[side].clear()
        setattr(self.session, side+"_frame", App.Placement())
        for role in tuple(self.reference_objects):
            if role.startswith(side+"_"):
                del self.reference_objects[role]
        self.picking_reference = False
        self.highlight()
        self.update_preview()

    def reject(self):
        self.close()
        return True

    def close(self):
        global _task
        if self.closed:
            return
        self.closed = True
        self.selection_timer.stop()
        self.monitor.stop()
        self.stop_manipulator()
        self.clear_preview()
        Gui.Selection.removeObserver(self)
        App.removeDocumentObserver(self)
        if _task is self:
            _task = None
            if App.ActiveDocument is not None:
                Gui.Control.closeDialog()

    def check_context(self):
        if self.closed or self.applying:
            return
        if (App.ActiveDocument != self.session.root.Document
                or self.mdi and self.mdi.activeSubWindow() != self.window
                or not DesignSelection.active()):
            self.close()
            return
        try:
            if self.session.parent is not None and self.session.signature() != self.session.expected:
                self.stop_manipulator()
                self.clear_preview()
                self.status.setText(tr("The placement context changed. Reset movement inputs before continuing."))
        except Exception:
            self.close()

    def stop_manipulator(self):
        manipulator, self.manipulator = self.manipulator, None
        if manipulator:
            manipulator.close()
            manipulator.deleteLater()

    def ensure_manipulator(self, pivot=None):
        if self.manipulator is None and self.session.paths:
            from freecad.gui.MoveComponentsManipulator import Manipulator
            self.manipulator = Manipulator(self)
            if pivot is not None:
                self.manipulator.pivot = App.Placement(pivot)
                self.manipulator.write()

    def configure_snap(self, *args):
        try:
            if self.manipulator:
                self.manipulator.configure_snap()
        except Exception as error:
            self.status.setText(str(error))

    def change_pivot_mode(self, *args):
        if self.manipulator:
            self.manipulator.cancel_drag()

    def reset_pivot(self):
        if self.manipulator:
            self.manipulator.cancel_drag()
            self.manipulator.pivot = App.Placement(self.session.group_pivot(), App.Rotation())
            self.manipulator.write()
            self.update_preview()

    def numeric_gesture(self):
        try:
            self.ensure_manipulator()
            if self.manipulator is None:
                raise ValueError(tr("Select components first."))
            self.manipulator.numeric()
        except Exception as error:
            self.status.setText(str(error))

    def slotDeletedDocument(self, doc):
        if doc == self.session.root.Document:
            self.close()

    def slotDeletedObject(self, obj):
        if (obj == self.session.root or obj == self.session.parent
                or getattr(obj, "ObjectId", None) in (self.session.parent_path or ())):
            self.close()
        elif getattr(obj, "ObjectId", None) in {key for path in self.session.paths for key in path}:
            self.clear_preview()
            self.session.paths = [path for path in self.session.paths if obj.ObjectId not in path]
            self.reset()
            self.refresh_list()


def open_task(root=None, paths=None):
    global _task
    if Gui.Control.activeDialog():
        raise ValueError(tr("Finish the current task first."))
    root = root or (Navigator.resolve(Navigator._dock.root_key) if Navigator._dock and Navigator._dock.root_key else
                    Move.Model.metadata(App.ActiveDocument).RootComponent)
    if root.Document.HasPendingTransaction or Gui.activeDocument().getInEdit():
        raise ValueError(tr("Finish the current edit before moving components."))
    entries = Gui.Selection.getSelectionEx("*", 0) if paths is None else []
    _task = MoveTask(root)
    Gui.Control.showDialog(_task)
    if paths is not None:
        _task.add_paths(paths)
    elif entries:
        _task.collect()
    return _task


class Command:
    def GetResources(self):
        return {"MenuText": tr("Move Components"), "Pixmap": "Std_TransformManip.svg",
                "ToolTip": tr("Move sibling component instances relative to their owning parent")}

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        try:
            open_task()
        except Exception as error:
            App.Console.PrintError(str(error) + "\n")


def registerCommand():
    Gui.addCommand("Std_MoveComponents", Command())
