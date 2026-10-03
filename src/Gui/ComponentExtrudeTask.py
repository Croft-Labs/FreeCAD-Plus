# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component Extrude creation/edit task with explicit profile and target choices."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.OccurrenceMove import Ghost

_task = None


def tr(text):
    return App.Qt.translate("ComponentExtrude", text)


def active_component():
    import ComponentModel as Model
    doc = App.ActiveDocument
    if doc is None:
        raise ValueError(tr("Create or open a component document first."))
    view = Gui.activeDocument().activeView()
    component = view.getActiveObject("part") if hasattr(view, "getActiveObject") else None
    return component if Model.is_component(component) else Model.metadata(doc).RootComponent


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


class ExtrudeTask:
    def __init__(self, component, operation=None, preset=None, context=None):
        import ComponentModel as Model
        import ComponentExtrude as Extrude
        self.component, self.operation = component, operation
        self.context = context
        self.ghost = None
        self.result = None
        self.whole_profile = True
        self.observing = False
        self.mouse_callback = None
        self.profile_visibility = {}
        self.region_visibility = {}
        self.reference_pick = None
        self.preview_transparency = {}
        self.view = Gui.getDocument(component.Document.Name).activeView()
        Model.activate(component, strict=False)
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle(tr("Extrude"))
        layout = CompactFormLayout(self.form)
        self.mode = QtWidgets.QComboBox()
        for name in Extrude.MODES:
            self.mode.addItem(tr(name), name)
        layout.addRow(tr("Operation"), self.mode)
        self.profile = QtWidgets.QComboBox()
        self.profile.addItem(tr("Select a profile…"), None)
        for obj in Model.history(component):
            if (getattr(obj, "ComponentRole", "") in ("Object", "Reference", "Result")
                    and hasattr(obj, "Shape") and not obj.Shape.Solids and obj.Shape.Edges):
                self.profile.addItem(obj.Label + " (" + obj.Name + ")", obj.Name)
        layout.addRow(tr("Profile"), self.profile)
        self.capture = QtWidgets.QPushButton(tr("Add selected curves"))
        layout.addRow(self.capture)
        self.curves = QtWidgets.QListWidget()
        self.curves.setMaximumHeight(100)
        self.curves.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        layout.addRow(tr("Selected curves"), self.curves)
        controls = QtWidgets.QWidget()
        buttons = QtWidgets.QHBoxLayout(controls)
        buttons.setContentsMargins(0, 0, 0, 0)
        self.remove_curves = QtWidgets.QPushButton(tr("Remove"))
        self.clear_curves = QtWidgets.QPushButton(tr("Clear"))
        self.all_curves = QtWidgets.QPushButton(tr("Use all"))
        for button in (self.remove_curves, self.clear_curves, self.all_curves):
            buttons.addWidget(button)
        layout.addRow(controls)
        self.region_pick = QtWidgets.QCheckBox(tr("Pick closed regions in the view"))
        self.region_pick.setChecked(True)
        self.region_pick.setToolTip(tr("Choose a sketch, then click inside a region. Its outer contour and hole contours are collected together."))
        layout.addRow(self.region_pick)
        self.target = QtWidgets.QComboBox()
        self.target.addItem(tr("Select a target body…"), None)
        for obj in Model.finished_results(component):
            if obj.Shape.Solids and (operation is None or operation not in obj.OutListRecursive):
                self.target.addItem(Model.display_object(obj).Label, obj.Name)
        layout.addRow(tr("Target body"), self.target)
        self.length = Gui.UiLoader().createWidget("Gui::QuantitySpinBox")
        self.length.setProperty("unit", "mm")
        self.length.setProperty("minimum", 0.001)
        self.length.setProperty("maximum", 1e9)
        self.length.setProperty("rawValue", 10.0)
        layout.addRow(tr("Length"), self.length)
        self.reverse = QtWidgets.QCheckBox(tr("Reverse direction"))
        layout.addRow(self.reverse)
        self.build_extents(layout)
        self.auto_preview = QtWidgets.QCheckBox(tr("Update preview automatically"))
        self.auto_preview.setChecked(True)
        layout.addRow(self.auto_preview)
        self.preview_timer = QtCore.QTimer(self.form)
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self.preview)
        self.preview_button = QtWidgets.QPushButton(tr("Preview"))
        layout.addRow(self.preview_button)
        self.status = QtWidgets.QLabel(tr("Choose a profile. No Body container is required."))
        self.status.setTextFormat(QtCore.Qt.PlainText)
        self.status.setWordWrap(True)
        layout.addRow(self.status)
        self.profile.currentIndexChanged.connect(self.profile_changed)
        if preset in Extrude.MODES:
            self.mode.setCurrentIndex(Extrude.MODES.index(preset))
        if operation:
            tool, mode, target = Extrude.parameters(operation)
            import ComponentProfile as Profile
            source, elements = Profile.selection(tool)
            self.profile.setCurrentIndex(self.profile.findData(source.Name))
            if elements is not None:
                self.set_curves(elements, False)
            self.length.setProperty("rawValue", tool.Length.Value if tool.TypeId == "PartDesign::Pad" else tool.LengthFwd.Value)
            self.load_extents(tool)
            self.reverse.setChecked(tool.Reversed)
            self.mode.setCurrentIndex(Extrude.MODES.index(mode))
            if target:
                if self.target.findData(target.Name) < 0:
                    self.target.addItem(Model.display_object(target).Label, target.Name)
                self.target.setCurrentIndex(self.target.findData(target.Name))
        else:
            self.use_selection(context.profile_selection if context else None)
        self.capture.clicked.connect(self.use_selection)
        self.preview_button.clicked.connect(self.preview)
        self.mode.currentIndexChanged.connect(self.changed)
        self.remove_curves.clicked.connect(self.remove_selected_curves)
        self.clear_curves.clicked.connect(lambda: self.set_curves([], False))
        self.all_curves.clicked.connect(self.profile_changed)
        self.region_pick.toggled.connect(self.update_regions)
        self.target.currentIndexChanged.connect(self.changed)
        self.length.valueChanged.connect(self.changed)
        self.reverse.toggled.connect(self.changed)
        self.auto_preview.toggled.connect(self.changed)
        self.changed()

    def getStandardButtons(self):
        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        return getattr(buttons, "value", buttons)

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

    def begin_reference_pick(self, field):
        self.reference_pick = field
        self.status.setText(tr("Pick a local limiting face, plane or shape. Profile collection is paused for this pick."))

    def build_extents(self, layout):
        import ComponentExtent as Extent
        self.sides = QtWidgets.QComboBox()
        for label, value in (("One dimension", "One side"), ("Two dimensions", "Two sides"), ("Symmetric", "Symmetric")):
            self.sides.addItem(tr(label), value)
        layout.addRow(tr("Sides"), self.sides)
        self.extent, self.extent2 = QtWidgets.QComboBox(), QtWidgets.QComboBox()
        for label, value in Extent.TYPES:
            self.extent.addItem(tr(label), value)
            self.extent2.addItem(tr(label), value)
        layout.addRow(tr("Type"), self.extent)
        self.limit, self.limit_row = self.reference_row(layout, "Limiting surface / shape")
        self.offset = self.quantity()
        self.offset.setToolTip(tr("Offset from the limiting surface; positive extends farther along side 1."))
        layout.addRow(tr("Offset"), self.offset)
        self.taper = self.quantity(unit="deg")
        layout.addRow(tr("Taper angle"), self.taper)
        layout.addRow(tr("Side 2 type"), self.extent2)
        self.length2 = self.quantity(10.)
        layout.addRow(tr("Side 2 length"), self.length2)
        self.limit2, self.limit_row2 = self.reference_row(layout, "Side 2 limiting surface / shape")
        self.offset2 = self.quantity()
        self.offset2.setToolTip(tr("Offset from the limiting surface; positive extends farther along side 2."))
        layout.addRow(tr("Side 2 offset"), self.offset2)
        self.taper2 = self.quantity(unit="deg")
        layout.addRow(tr("Side 2 taper angle"), self.taper2)
        self.start = QtWidgets.QComboBox()
        for label in ("Profile plane", "Offset", "Reference"):
            self.start.addItem(tr(label), label)
        layout.addRow(tr("Start"), self.start)
        self.start_offset = self.quantity()
        self.start_offset.setToolTip(tr("Signed offset from the profile plane or start reference along the extrusion direction."))
        layout.addRow(tr("Start offset"), self.start_offset)
        self.start_reference, self.start_row = self.reference_row(layout, "Start reference")
        self.custom = QtWidgets.QCheckBox(tr("Custom direction"))
        layout.addRow(self.custom)
        row = QtWidgets.QWidget()
        box = CompactFormLayout(row)
        box.setContentsMargins(0, 0, 0, 0)
        self.direction = []
        for label, value in (("X", 0.), ("Y", 0.), ("Z", 1.)):
            widget = QtWidgets.QDoubleSpinBox()
            widget.setRange(-1e6, 1e6)
            widget.setDecimals(6)
            widget.setValue(value)
            box.addRow(label, widget)
            self.direction.append(widget)
        self.direction_row = row
        layout.addRow(tr("Direction vector"), row)
        self.along_normal = QtWidgets.QCheckBox(tr("Length along sketch normal"))
        self.along_normal.setChecked(True)
        layout.addRow(self.along_normal)
        self.refine = QtWidgets.QCheckBox(tr("Refine result"))
        self.refine.setChecked(True)
        layout.addRow(self.refine)
        for widget in (self.sides, self.extent, self.extent2, self.start):
            widget.currentIndexChanged.connect(self.changed)
        for widget in (self.offset, self.offset2, self.taper, self.taper2, self.length2, self.start_offset, *self.direction):
            widget.valueChanged.connect(self.changed)
        for widget in (self.custom, self.along_normal, self.refine):
            widget.toggled.connect(self.changed)

    def load_extents(self, tool):
        import ComponentExtent as Extent
        values = Extent.read(tool)
        for widget, key in ((self.sides, "sides"), (self.extent, "extent"), (self.extent2, "extent2"), (self.start, "start")):
            widget.setCurrentIndex(widget.findData(values[key]))
        for widget, key in ((self.length2, "length2"), (self.offset, "offset"), (self.offset2, "offset2"),
                            (self.taper, "taper"), (self.taper2, "taper2"), (self.start_offset, "start_offset")):
            widget.setProperty("rawValue", values[key])
        for widget, key in ((self.limit, "limit"), (self.limit2, "limit2"), (self.start_reference, "start_reference")):
            widget.setText(Extent.reference_text(values[key]))
        self.custom.setChecked(values["custom"])
        self.along_normal.setChecked(values["along_normal"])
        self.refine.setChecked(values["refine"])
        for widget, value in zip(self.direction, values["direction"]):
            widget.setValue(value)

    def extent_options(self):
        import ComponentExtent as Extent
        values = Extent.defaults()
        values.update(sides=self.sides.currentData(), extent=self.extent.currentData(), extent2=self.extent2.currentData(),
                      start=self.start.currentData(), custom=self.custom.isChecked(),
                      direction=tuple(widget.value() for widget in self.direction),
                      along_normal=self.along_normal.isChecked(), refine=self.refine.isChecked())
        for widget, key in ((self.length2, "length2"), (self.offset, "offset"), (self.offset2, "offset2"),
                            (self.taper, "taper"), (self.taper2, "taper2"), (self.start_offset, "start_offset")):
            values[key] = float(widget.property("rawValue"))
        if values["extent"] in ("UpToFace", "UpToShape"):
            values["limit"] = Extent.reference(self.component, self.limit.text())
        if values["sides"] == "Two sides" and values["extent2"] in ("UpToFace", "UpToShape"):
            values["limit2"] = Extent.reference(self.component, self.limit2.text())
        if values["start"] == "Reference":
            values["start_reference"] = Extent.reference(self.component, self.start_reference.text())
        return values

    def changed(self, *args):
        if not hasattr(self, "status"):
            return
        self.clear_preview()
        two = self.sides.currentData() == "Two sides"
        layout = self.form.layout()
        layout.labelForField(self.length).setText(tr("Total length") if self.sides.currentData() == "Symmetric" else tr("Side 1 length") if two else tr("Length"))
        for widget in (self.extent2, self.length2, self.limit_row2, self.offset2, self.taper2):
            widget.setVisible(two)
            label = layout.labelForField(widget)
            if label:
                label.setVisible(two)
        self.length.setEnabled(self.extent.currentData() == "Length")
        self.length.setToolTip(tr("Total span, half on each side") if self.sides.currentData() == "Symmetric" else tr("Side 1 length"))
        self.limit_row.setEnabled(self.extent.currentData() in ("UpToFace", "UpToShape"))
        self.offset.setEnabled(self.extent.currentData() in ("UpToFace", "UpToShape", "UpToFirst", "UpToLast"))
        self.extent2.setEnabled(two)
        self.length2.setEnabled(two and self.extent2.currentData() == "Length")
        self.limit_row2.setEnabled(two and self.extent2.currentData() in ("UpToFace", "UpToShape"))
        self.offset2.setEnabled(two and self.extent2.currentData() in ("UpToFace", "UpToShape", "UpToFirst", "UpToLast"))
        self.taper2.setEnabled(two)
        self.start_offset.setEnabled(self.start.currentData() != "Profile plane")
        self.start_row.setEnabled(self.start.currentData() == "Reference")
        self.direction_row.setEnabled(self.custom.isChecked())
        self.along_normal.setEnabled(self.custom.isChecked())
        if self.auto_preview.isChecked() and self.profile.currentData():
            self.preview_timer.start(300)
        else:
            self.preview_timer.stop()
        self.target.setEnabled(self.mode.currentData() != "New Body")
        if not self.profile.currentData():
            self.status.setText(tr("Choose a profile. No Body container is required."))
        elif self.mode.currentData() != "New Body" and not self.target.currentData():
            self.status.setText(tr("Choose the body to add to or subtract from."))
        else:
            self.status.setText(tr("Select curves from one sketch, or click a closed region. Preview and OK require one connected region with optional holes."))

    def curve_names(self):
        return [self.curves.item(i).data(QtCore.Qt.UserRole) for i in range(self.curves.count())]

    def set_curves(self, names, whole=False):
        self.curves.clear()
        source = self.component.Document.getObject(self.profile.currentData()) if self.profile.currentData() else None
        for name in dict.fromkeys(names):
            item = QtWidgets.QListWidgetItem((source.Label + " / " if source else "") + name)
            item.setData(QtCore.Qt.UserRole, name)
            self.curves.addItem(item)
        self.whole_profile = whole
        self.changed()

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
        self.set_curves([name for name in self.curve_names() if name not in removed], False)

    def start_selection(self):
        self.update_regions()
        Gui.Selection.addObserver(self, 0)
        self.observing = True
        self.mouse_callback = self.view.addEventCallback("SoMouseButtonEvent", self.pick_region)

    def stop_selection(self):
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
        if not hasattr(self, "region_visibility"):
            self.region_visibility = {}
        for index in range(1, self.profile.count()):
            source = self.component.Document.getObject(self.profile.itemData(index))
            if source and hasattr(source.ViewObject, "ShowClosedRegions"):
                self.region_visibility.setdefault(source.Name, source.ViewObject.ShowClosedRegions)
                source.ViewObject.ShowClosedRegions = self.region_pick.isChecked()

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
            self.use_selection([(picks[0].item, picks[0].element)])

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
                    and hit_object in [ref[0] for ref in source.AttachmentSupport]
                    and (hit_object.isDerivedFrom("PartDesign::Plane")
                         or hit_object.isDerivedFrom("Part::Plane")))
                sketch_region_hit = (pick is not None and pick.item == source
                                     and pick.element.startswith("InternalFace"))
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
            self.set_curves(([] if self.whole_profile else self.curve_names()) + names, False)
        except Exception as error:
            self.status.setText(str(error))

    def clear_preview(self):
        if self.ghost:
            self.ghost.remove()
            self.ghost = None
        for name, transparency in self.preview_transparency.items():
            target = self.component.Document.getObject(name)
            if target:
                target.ViewObject.Transparency = transparency
        self.preview_transparency.clear()

    def use_selection(self, picks=None):
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
                self.set_curves(([] if self.whole_profile else self.curve_names()) + elements, False)
            else:
                self.profile_changed()
        except Exception as error:
            self.status.setText(str(error))

    def values(self):
        doc = self.component.Document
        profile = doc.getObject(self.profile.currentData()) if self.profile.currentData() else None
        if profile is None:
            raise ValueError(tr("Select a profile in the active component."))
        mode = self.mode.currentData()
        target = doc.getObject(self.target.currentData()) if self.target.currentData() and mode != "New Body" else None
        length = float(self.length.property("rawValue"))
        elements = self.curve_names() if profile.isDerivedFrom("Sketcher::SketchObject") else None
        return profile, length, mode, target, self.reverse.isChecked(), elements, self.extent_options()

    def preview(self):
        import ComponentExtrude as Extrude
        self.clear_preview()
        try:
            shape = Extrude.preview(self.component, *self.values(), volume_only=True)
            shape.Placement = self.component.getGlobalPlacement().multiply(shape.Placement)
            self.ghost = Ghost(shape, color=(1., 0., 0.) if self.mode.currentData() == "Subtract" else (0., 1., 0.),
                               filled=True, transparency=0.5)
            if self.mode.currentData() != "New Body" and self.target.currentData():
                target = self.component.Document.getObject(self.target.currentData())
                import ComponentModel as Model
                target = Model.display_object(target)
                self.preview_transparency[target.Name] = target.ViewObject.Transparency
                target.ViewObject.Transparency = max(75, target.ViewObject.Transparency)
            self.status.setText(tr("Preview ready. OK creates or updates the operation."))
            return True
        except Exception as error:
            self.status.setText(str(error))
            return False

    def accept(self):
        import ComponentExtrude as Extrude
        try:
            profile, length, mode, target, reverse, elements, options = self.values()
            self.clear_preview()
            self.restore_profile_visibility()
            if self.operation:
                self.operation = Extrude.edit(self.operation, profile, length, reverse, mode, target, elements, options)
            else:
                self.operation, self.result = Extrude.create(self.component, profile, length, mode, target, reverse, elements, options)
        except Exception as error:
            if self.profile.currentData():
                source = self.component.Document.getObject(self.profile.currentData())
                if source:
                    source.Visibility = True
            self.status.setText(str(error))
            return False
        self.finish(committed=True)
        return True

    def reject(self):
        self.finish()
        return True

    def finish(self, committed=False):
        global _task
        self.stop_selection()
        self.preview_timer = None
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
        raise ValueError(tr("Finish the current task before starting Extrude."))
    import ComponentModel as Model
    from freecad.gui.ComponentNavigator import TaskContext
    component = Model.owner(operation) if operation else active_component()
    context = TaskContext(component)
    try:
        context.enter()
        _task = ExtrudeTask(component, operation, preset, context)
        Gui.Control.showDialog(_task)
        _task.start_selection()
    except Exception:
        if _task:
            _task.stop_selection()
            _task.restore_profile_visibility()
            Gui.Control.closeDialog()
        _task = None
        context.restore()
        raise
    return _task
