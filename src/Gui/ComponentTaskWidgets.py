# SPDX-License-Identifier: LGPL-2.1-or-later
"""Shared modeling controls and curve-picking lifecycle.

Consumers retain operation-specific geometry and readiness rules. All profile,
section and Pipe path collectors use CurveCollector; CurveSelection owns the
profile observer, region arbitration and temporary viewport emphasis.
"""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets
from freecad.gui.OccurrenceMove import Ghost


def tr(text):
    return App.Qt.translate("ComponentOperation", text)


class CompactFormLayout(QtWidgets.QFormLayout):
    """Keep modeling forms usable in a narrow, vertically scrolling Tasks pane."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRowWrapPolicy(QtWidgets.QFormLayout.WrapLongRows)
        self.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)

    def addRow(self, *args):
        super().addRow(*args)
        # Object labels and attachment descriptions must not determine dock width.
        for arg in args:
            if isinstance(arg, QtWidgets.QComboBox):
                arg.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
                arg.setMinimumContentsLength(12)
                arg.currentTextChanged.connect(arg.setToolTip)
                arg.setToolTip(arg.currentText())
            elif isinstance(arg, QtWidgets.QListWidget):
                arg.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                arg.setTextElideMode(QtCore.Qt.ElideMiddle)
                arg.setMouseTracking(True)
                arg.itemEntered.connect(lambda item: item.setToolTip(item.text()))
        label = self.itemAt(self.rowCount() - 1, QtWidgets.QFormLayout.LabelRole)
        if label and isinstance(label.widget(), QtWidgets.QLabel):
            label.widget().setWordWrap(True)


class CurveListWidget(QtWidgets.QListWidget):
    """Delete edits the task's collector, never the document selection."""
    removeRequested = QtCore.Signal()
    focusReceived = QtCore.Signal()

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focusReceived.emit()

    def event(self, event):
        if event.type() == QtCore.QEvent.ShortcutOverride and event.key() == QtCore.Qt.Key_Delete:
            event.accept()
            return True
        return super().event(event)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            self.removeRequested.emit()
            event.accept()
        else:
            super().keyPressEvent(event)

    def highlight(self, row=-1):
        self.clearSelection()
        self.setCurrentRow(row)
        if row >= 0:
            self.scrollToItem(self.item(row))


def toggled_curves(names, elements, toggle=False):
    """Return one deduplicated collector update and its latest selected row."""
    names = list(names)
    current = None
    for name in dict.fromkeys(elements):
        if toggle and name in names:
            names.remove(name)
            current = None
        else:
            if name not in names:
                names.append(name)
            current = name
    return names, current


class CurveCollector(QtWidgets.QWidget):
    """One source/list/action component, configured for profiles or path edges."""

    def __init__(self, component, *, source_label="Profile", placeholder="Select a profile…",
                 curves_label="Selected curves", height=100, allow_solids=False,
                 allow_vertex=False, actions=(), remove=None, regions=None):
        super().__init__()
        import ComponentModel as Model
        form = CompactFormLayout(self)
        form.setContentsMargins(0, 0, 0, 0)
        self.source = None
        if source_label is not None:
            self.source = QtWidgets.QComboBox()
            self.source.addItem(tr(placeholder), None)
            for obj in Model.history(component):
                if (getattr(obj, "ComponentRole", "") in ("Object", "Reference", "Result")
                        and hasattr(obj, "Shape") and (allow_solids or not obj.Shape.Solids)
                        and (obj.Shape.Edges or (allow_vertex and len(obj.Shape.Vertexes) == 1))):
                    self.source.addItem(obj.Label + " (" + obj.Name + ")", obj.Name)
            form.addRow(tr(source_label), self.source)
        self.curves = CurveListWidget()
        self.curves.setMaximumHeight(height)
        self.curves.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        if remove is not None:
            self.curves.removeRequested.connect(remove)
        form.addRow(tr(curves_label), self.curves)
        self.actions = button_row(form, actions)
        self.region_pick = None
        if regions is not None:
            self.region_pick = QtWidgets.QCheckBox(tr("Pick closed regions in the view"))
            self.region_pick.setChecked(True)
            self.region_pick.setToolTip(tr("Click inside a region to collect its outer contour and hole contours. Clicking a curve selects only that curve."))
            self.region_pick.toggled.connect(regions)
            form.addRow(self.region_pick)


class ReferenceCollector(CurveCollector):
    """The same collector with mixed geometry references and basic-choice menu."""
    changed = QtCore.Signal()
    activated = QtCore.Signal()

    def __init__(self, component, choices=()):
        super().__init__(component, source_label=None, curves_label="Geometry", height=90,
                         actions=(("Remove", self.remove_selected), ("Clear", lambda: self.set_references([]))),
                         remove=self.remove_selected)
        self.curves.focusReceived.connect(self.activated)
        self.basic = QtWidgets.QToolButton()
        self.basic.setText("...")
        self.basic.setToolTip(tr("Choose basic reference geometry"))
        self.basic.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        menu = QtWidgets.QMenu(self.basic)
        for label, reference in choices:
            menu.addAction(tr(label), lambda ref=reference: self.choose_basic(ref))
        self.basic.setMenu(menu)
        original_row = self.layout().takeRow(0)
        row = QtWidgets.QWidget()
        box = QtWidgets.QHBoxLayout(row)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(self.curves)
        box.addWidget(self.basic, 0, QtCore.Qt.AlignTop)
        self.layout().insertRow(0, original_row.labelItem.widget(), row)
        self.status = QtWidgets.QLabel()
        self.status.setWordWrap(True)
        self.layout().addRow(self.status)

    def references(self):
        return [self.curves.item(i).data(QtCore.Qt.UserRole) for i in range(self.curves.count())]

    def choose_basic(self, reference):
        self.curves.setFocus(QtCore.Qt.OtherFocusReason)
        self.activated.emit()
        self.set_references([reference], reference)

    def set_references(self, references, current=None):
        self.curves.clear()
        for reference in references:
            obj, name = reference
            item = QtWidgets.QListWidgetItem(obj.Label + (" / " + name if name else ""))
            item.setData(QtCore.Qt.UserRole, reference)
            self.curves.addItem(item)
        self.curves.highlight(references.index(current) if current in references else -1)
        self.changed.emit()

    def collect(self, reference):
        names, current = toggled_curves(self.references(), [reference], True)
        self.curves.setFocus(QtCore.Qt.OtherFocusReason)
        self.set_references(names, current)

    def remove_selected(self):
        removed = [item.data(QtCore.Qt.UserRole) for item in self.curves.selectedItems()]
        self.set_references([ref for ref in self.references() if ref not in removed])


def button_row(layout, entries):
    row = QtWidgets.QWidget()
    box = QtWidgets.QGridLayout(row)
    box.setContentsMargins(0, 0, 0, 0)
    buttons = []
    for index, (label, callback) in enumerate(entries):
        button = QtWidgets.QPushButton(tr(label))
        button.clicked.connect(callback)
        box.addWidget(button, index // 2, index % 2)
        buttons.append(button)
    layout.addRow(row)
    return buttons


class PreviewControls(QtWidgets.QWidget):
    """Common preview policy, update control and owned debounce timer."""

    def __init__(self, callback):
        super().__init__()
        layout = CompactFormLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.automatic = QtWidgets.QCheckBox(tr("Recompute on change"))
        self.automatic.setChecked(True)
        layout.addRow(self.automatic)
        self.mode = QtWidgets.QComboBox()
        for name in ("None", "Overlay", "Result"):
            self.mode.addItem(tr(name), name)
        self.mode.setCurrentIndex(1)
        layout.addRow(tr("Preview type"), self.mode)
        self.button = QtWidgets.QPushButton(tr("Update preview"))
        layout.addRow(self.button)
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(callback)


class ModelingTaskUI:
    """Reusable controls; operation-specific visibility and values stay local."""

    def combo(self, layout, label, items):
        widget = QtWidgets.QComboBox()
        for text, value in items:
            widget.addItem(tr(text), value)
        layout.addRow(tr(label), widget)
        return widget

    def buttons(self, layout, entries):
        return button_row(layout, entries)

    def build_profile_collector(self, layout, *, sections=False):
        self.collector = CurveCollector(self.component,
            source_label="Section source" if sections else "Profile",
            height=65 if sections else 100, allow_vertex=sections,
            actions=(("Remove", self.remove_selected_curves),
                     ("Clear", lambda: self.set_curves([], False)),
                     ("Use all", self.profile_changed)),
            remove=self.remove_selected_curves, regions=self.update_regions)
        self.profile, self.curves = self.collector.source, self.collector.curves
        self.region_pick = self.collector.region_pick
        layout.addRow(self.collector)

    def build_operation_controls(self, layout, modes):
        self.mode = self.combo(layout, "Operation", [(name, name) for name in modes])
        self.build_target_control(layout)

    def build_target_control(self, layout):
        import ComponentModel as Model
        self.target = self.combo(layout, "Target body", [("Select a target body…", None)])
        for obj in Model.finished_results(self.component):
            if obj.Shape.Solids and (self.operation is None or self.operation not in obj.OutListRecursive):
                self.target.addItem(Model.display_object(obj).Label, obj.Name)

    def build_preview_controls(self, layout):
        self.preview_controls = PreviewControls(self.preview)
        self.auto_preview = self.preview_controls.automatic
        self.preview_mode = self.preview_controls.mode
        self.preview_button = self.preview_controls.button
        self.preview_timer = self.preview_controls.timer
        layout.addRow(self.preview_controls)

    def checkbox(self, layout, label, checked=False):
        widget = QtWidgets.QCheckBox(tr(label))
        widget.setChecked(checked)
        layout.addRow(widget)
        return widget

    def fuzzy_tolerance(self, layout, value=0.):
        field = self.quantity(value)
        field.setProperty("minimum", -1.)
        field.setProperty("maximum", 1.)
        field.setToolTip(tr("Zero: native default. Negative: automatic tolerance. Positive: explicit tolerance, up to 1 mm."))
        layout.addRow(tr("Fuzzy tolerance"), field)
        return field

    def build_status(self, layout):
        self.status = QtWidgets.QLabel()
        self.status.setTextFormat(QtCore.Qt.PlainText)
        self.status.setWordWrap(True)
        if isinstance(layout, QtWidgets.QFormLayout):
            layout.addRow(self.status)
        else:
            layout.addWidget(self.status)
            layout.addStretch()

    def quantity(self, value=0., unit="mm"):
        widget = Gui.UiLoader().createWidget("Gui::QuantitySpinBox")
        widget.setProperty("unit", unit)
        widget.setProperty("minimum", -1e9)
        widget.setProperty("maximum", 1e9)
        widget.setProperty("rawValue", value)
        return widget


    def reference_row(self, layout, label):
        row = QtWidgets.QWidget()
        box = QtWidgets.QVBoxLayout(row)
        box.setContentsMargins(0, 0, 0, 0)
        field = QtWidgets.QLineEdit()
        field.setMinimumWidth(120)
        field.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        field.setPlaceholderText(tr("ObjectName.Face1 or plane/shape name"))
        pick, clear = QtWidgets.QPushButton(tr("Pick")), QtWidgets.QPushButton(tr("Clear"))
        pick.setMaximumWidth(55)
        clear.setMaximumWidth(55)
        box.addWidget(field)
        buttons = QtWidgets.QHBoxLayout()
        buttons.addWidget(pick)
        buttons.addWidget(clear)
        buttons.addStretch()
        box.addLayout(buttons)
        pick.clicked.connect(lambda: self.begin_reference_pick(field))
        clear.clicked.connect(field.clear)
        field.textChanged.connect(self.changed)
        layout.addRow(tr(label), row)
        return field, row


    def build_sections(self):
        self.form = QtWidgets.QWidget()
        self.form.setPalette(Gui.getMainWindow().palette())
        self.form.setWindowTitle(tr(self.operation_name))
        outer = QtWidgets.QVBoxLayout(self.form)
        self.sections = []
        for title, expanded in (("Main parameters", True), ("Dimensions", True), ("Advanced", False), ("Preview", True)):
            button = QtWidgets.QToolButton()
            button.setText(tr(title))
            button.setCheckable(True)
            button.setChecked(expanded)
            button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
            button.setArrowType(QtCore.Qt.DownArrow if expanded else QtCore.Qt.RightArrow)
            body = QtWidgets.QWidget()
            body.setVisible(expanded)
            layout = CompactFormLayout(body)
            button.toggled.connect(body.setVisible)
            button.toggled.connect(lambda checked, b=button: b.setArrowType(QtCore.Qt.DownArrow if checked else QtCore.Qt.RightArrow))
            outer.addWidget(button)
            outer.addWidget(body)
            self.sections.append((button, body, layout))
        return outer


class CurveSelection:
    """Shared profile input controller and task-owned display lifecycle."""

    def curve_names(self):
        return [self.curves.item(i).data(QtCore.Qt.UserRole) for i in range(self.curves.count())]


    def set_curves(self, names, whole=False, current=None):
        self.curves.clear()
        source = self.component.Document.getObject(self.profile.currentData()) if self.profile.currentData() else None
        for name in dict.fromkeys(names):
            item = QtWidgets.QListWidgetItem((source.Label + " / " if source else "") + name)
            item.setData(QtCore.Qt.UserRole, name)
            self.curves.addItem(item)
        names = self.curve_names()
        self.curves.highlight(names.index(current) if current in names else -1)
        self.whole_profile = whole
        self.changed()
        self.update_curve_display()


    def profile_changed(self, *args):
        source = self.component.Document.getObject(self.profile.currentData()) if self.profile.currentData() else None
        self.restore_profile_visibility()
        if source:
            self.profile_visibility.setdefault(source.Name, bool(source.Visibility))
            source.Visibility = True
        names = ["Edge" + str(i + 1) for i in range(len(source.Shape.Edges))] if source else []
        self.set_curves(names, True)


    def restore_profile_visibility(self):
        for name, visible in self.profile_visibility.items():
            source = self.component.Document.getObject(name)
            if source:
                source.Visibility = visible


    def remove_selected_curves(self):
        removed = {item.data(QtCore.Qt.UserRole) for item in self.curves.selectedItems()}
        if removed:
            self.set_curves([name for name in self.curve_names() if name not in removed], False)


    def collect_curves(self, elements, toggle=False):
        names = [] if self.whole_profile else self.curve_names()
        names, current = toggled_curves(names, elements, toggle)
        if self.observing:
            self.curves.setFocus(QtCore.Qt.OtherFocusReason)
        # Focus can give an empty-current list its first row. Apply the explicit
        # highlight after focus so deselection leaves no row selected.
        self.set_curves(names, False, current)


    def start_selection(self):
        self.curve_display_active = True
        self.update_regions()
        # The task owns persistent curve emphasis. Release native preselection so
        # clicking the same edge produces another pick, including without Ctrl.
        Gui.Selection.clearSelection()
        Gui.Selection.addObserver(self, 0)
        self.observing = True
        self.mouse_callback = self.view.addEventCallback("SoMouseButtonEvent", self.pick_region)


    def stop_selection(self):
        self.curve_display_active = False
        self.clear_curve_display()
        for name, visible in getattr(self, "region_visibility", {}).items():
            source = self.component.Document.getObject(name)
            if source:
                source.ViewObject.ShowClosedRegions = visible
        self.region_visibility = {}
        if getattr(self, "preview_timer", None) is not None:
            self.preview_timer.stop()
        if self.observing:
            Gui.Selection.removeObserver(self)
            self.observing = False
        if self.mouse_callback is not None:
            self.view.removeEventCallback("SoMouseButtonEvent", self.mouse_callback)
            self.mouse_callback = None


    def update_regions(self, *args):
        self.update_curve_display()


    def curve_display_inputs(self):
        """Collected geometry, independent of the transient native selection."""
        name = self.profile.currentData()
        return [(name, self.curve_names())] if name and self.curves.count() else []


    def active_curve_source(self):
        return self.profile.currentData()


    def clear_curve_display(self):
        for highlight in getattr(self, "curve_highlights", {}).values():
            highlight.remove()
        self.curve_highlights = {}
        for root, material in getattr(self, "curve_materials", {}).values():
            if root.findChild(material) >= 0:
                root.removeChild(material)
        self.curve_materials = {}


    def update_curve_display(self, *args):
        if not getattr(self, "curve_display_active", False):
            return
        import Part
        from pivy import coin
        self.clear_curve_display()
        doc = self.component.Document
        collected = {}
        for name, elements in self.curve_display_inputs():
            source = doc.getObject(name) if name else None
            if source is None or not hasattr(source, "Shape"):
                continue
            names = elements if elements is not None else ["Edge" + str(i + 1) for i in range(len(source.Shape.Edges))]
            if names:
                collected.setdefault(name, set()).update(names)
        active = self.active_curve_source()
        candidates = {self.profile.itemData(i) for i in range(1, self.profile.count())}
        if not hasattr(self, "region_visibility"):
            self.region_visibility = {}
        for source in doc.Objects:
            if not source.isDerivedFrom("Sketcher::SketchObject"):
                continue
            view = source.ViewObject
            if collected and source.Name != active:
                # Scene-only overrides never alter saved LineColor/PointColor,
                # appearance arrays, undo history or document persistence.
                material = coin.SoMaterial()
                material.diffuseColor = (0.65, 0.65, 0.65)
                material.setOverride(True)
                root = view.RootNode
                root.insertChild(material, 0)
                self.curve_materials[source.Name] = (root, material)
            if hasattr(view, "ShowClosedRegions"):
                self.region_visibility.setdefault(source.Name, view.ShowClosedRegions)
                if collected:
                    view.ShowClosedRegions = bool(self.region_pick.isChecked() and source.Name == active
                                                  and source.Name in candidates)
                elif source.Name in candidates:
                    view.ShowClosedRegions = self.region_pick.isChecked()
                else:
                    view.ShowClosedRegions = self.region_visibility[source.Name]
        color = App.ParamGet("User parameter:BaseApp/Preferences/View").GetUnsigned("SelectionColor", 0xffbf00ff)
        color = tuple(((color >> shift) & 255) / 255. for shift in (24, 16, 8))
        for name, elements in collected.items():
            source = doc.getObject(name)
            shapes = []
            for element in sorted(elements):
                try:
                    shapes.append(source.Shape.getElement(element))
                except Exception:
                    continue  # Stale inputs remain in the collector for repair.
            if not shapes:
                continue
            shape = Part.makeCompound(shapes)
            parent = source.getGlobalPlacement().multiply(source.Placement.inverse())
            shape.Placement = parent.multiply(shape.Placement)
            highlight = Ghost(shape, color=color)
            highlight.node.getChild(1).lineWidth = 3
            highlight.node.getChild(1).pointSize = 6
            # Annotation keeps the collected outline visible over solid previews.
            # Its separator contains all render state; the geometry stays unpickable.
            annotation = coin.SoAnnotation()
            annotation.addChild(highlight.node)
            highlight.root.removeChild(highlight.node)
            highlight.node = annotation
            highlight.root.addChild(annotation)
            self.curve_highlights[name] = highlight


    def addSelection(self, document, name, subname, *args):
        from freecad.gui import ComponentSelection as Selection
        doc = App.listDocuments().get(document)
        base = doc.getObject(name) if doc else None
        if self.reference_pick is not None and base is not None:
            import ComponentModel as Model
            item = base.getSubObject(subname, 1) if subname else base
            if item is not None and (Model.owner(item) == self.component or item in self.component.Origin.OriginFeatures):
                element = subname.rsplit(".", 1)[-1]
                self.reference_pick.setText(item.Name + ("." + element if element.startswith("Face") else ""))
                self.reference_pick = None
                return
        picks = Selection.resolve(self.component, base, subname)
        if len(picks) == 1 and picks[0].item is not None:
            if self.reference_pick is not None:
                pick = picks[0]
                self.reference_pick.setText(pick.item.Name + ("." + pick.element if pick.element else ""))
                self.reference_pick = None
                return
            if picks[0].element.startswith("InternalFace"):
                return  # Region hits are collected using the cursor's sketch-plane point.
            self.use_selection([(picks[0].item, picks[0].element)], toggle=True)
            if picks[0].element.startswith(("Edge", "Vertex")):
                Gui.Selection.removeSelection(document, name, subname)


    def pick_region(self, event):
        if self.reference_pick is not None or not self.region_pick.isChecked() or event.get("State") != "DOWN" or event.get("Button") != "BUTTON1":
            return
        position = event.get("Position")
        if not position:
            return
        try:
            import ComponentProfile as Profile
            from freecad.gui import ComponentSelection as Selection
            hits = self.view.getObjectsInfo(position) or []
            source = self.component.Document.getObject(self.profile.currentData()) if self.profile.currentData() else None
            # An interior click can choose the profile itself. Native hits may
            # name a component path rather than the sketch directly.
            resolved_hits = []
            for hit in hits:
                hit_doc = App.listDocuments().get(hit.get("Document"))
                base = hit_doc.getObject(hit.get("Object", "")) if hit_doc else None
                picks = Selection.resolve(self.component, base, hit.get("Component", ""))
                pick = picks[0] if len(picks) == 1 else None
                resolved_hits.append((hit, base, pick))
                if (source is None and pick and pick.item is not None
                        and pick.element.startswith("InternalFace")
                        and self.profile.findData(pick.item.Name) > 0):
                    source = pick.item
            if source is None or not source.isDerivedFrom("Sketcher::SketchObject") or not source.Visibility:
                return
            start, end = self.view.projectPointToLine(position)
            frame = self.component.getGlobalPlacement().multiply(source.Placement)
            normal = frame.Rotation.multVec(App.Vector(0, 0, 1))
            direction = end - start
            denominator = direction.dot(normal)
            if abs(denominator) < 1e-12:
                raise ValueError(tr("Turn the view so the sketch plane can be picked."))
            point = start + direction * ((frame.Base - start).dot(normal) / denominator)
            # Origin helpers can be picked on top of solids regardless of depth.
            # Inspect the full ray so ignoring a helper never exposes a region
            # occluded by real geometry. Geometry behind the sketch is harmless.
            for hit, hit_object, pick in resolved_hits:
                origin = self.component.Origin
                origin_hit = hit_object == origin or hit_object in origin.OriginFeatures
                support_plane_hit = (hit_object is not None
                    and hit_object in [ref[0] for ref in getattr(source, "FrameSupport", source.AttachmentSupport)]
                    and (hit_object.isDerivedFrom("PartDesign::Plane")
                         or hit_object.isDerivedFrom("Part::Plane")))
                sketch_region_hit = (pick is not None and pick.item == source
                                     and pick.element.startswith("InternalFace"))
                if (pick is not None and pick.item == source
                        and pick.element.startswith(("Edge", "Vertex"))):
                    return  # The native observer owns this click; never also collect its region.
                if origin_hit or support_plane_hit or sketch_region_hit:
                    continue
                if all(axis in hit for axis in ("x", "y", "z")):
                    hit_point = App.Vector(hit["x"], hit["y"], hit["z"])
                    if (hit_point - point).dot(direction) / direction.Length > 1e-6:
                        continue
                return  # Native edge picks are collected by the selection observer.
            point = self.component.getGlobalPlacement().inverse().multVec(point)
            names = Profile.region(source, point)
            self.profile.setCurrentIndex(self.profile.findData(source.Name))
            self.collect_curves(names)
        except Exception as error:
            self.status.setText(str(error))


    def use_selection(self, picks=None, toggle=False):
        from freecad.gui import ComponentSelection as Selection
        import ComponentModel as Model
        selected = picks if isinstance(picks, list) else [(p.item, p.element) for p in
            Selection.selected(self.component, Gui.Selection.getSelectionEx("*", 0)) if p.item is not None]
        if not selected:
            return
        try:
            sources = {obj for obj, element in selected}
            if len(sources) != 1:
                raise ValueError(tr("All selected curves must belong to the same sketch."))
            source = next(iter(sources))
            index = self.profile.findData(source.Name)
            if Model.owner(source) != self.component or index <= 0:
                raise ValueError(tr("Choose a sketch owned by the active component."))
            if self.profile.currentData() not in (None, source.Name) and self.curves.count():
                raise ValueError(tr("Choose the other sketch in the Profile field before collecting its curves."))
            elements = [element for obj, element in selected if element]
            if elements and (not source.isDerivedFrom("Sketcher::SketchObject")
                             or any(not name.startswith("Edge") or not name[4:].isdigit() for name in elements)):
                raise ValueError(tr("Select curves from one sketch."))
            self.profile.setCurrentIndex(index)
            if elements:
                names = ["Edge" + str(i + 1) for i in range(len(source.Shape.Edges))]
                if any(name not in names for name in elements):
                    raise ValueError(tr("A selected curve is unavailable. Select it again."))
                self.collect_curves(elements, toggle)
            else:
                self.profile_changed()
        except Exception as error:
            self.status.setText(str(error))
