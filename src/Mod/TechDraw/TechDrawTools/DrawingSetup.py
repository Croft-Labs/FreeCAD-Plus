# SPDX-License-Identifier: LGPL-2.1-or-later
"""Guided native page and orthographic projection setup for one root solid."""
from pathlib import Path
import math

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.DependencyInspector import identity, resolve


def tr(text):
    return App.Qt.translate("DrawingSetup", text)


TEMPLATES = {"A4 landscape": ("A4_Landscape_ISO5457_notitleblock.svg", 297, 210),
             "A3 landscape": ("A3_Landscape_ISO5457_notitleblock.svg", 420, 297)}
ORIENTATIONS = {"Front (looking along +Y)": ((0, -1, 0), (1, 0, 0)),
                "Top (looking along -Z)": ((0, 0, 1), (1, 0, 0)),
                "Right (looking along -X)": ((1, 0, 0), (0, 1, 0))}


def review(source):
    from BasicShapes.ShapeReferences import require_current
    if (not source.isDerivedFrom("Part::Feature") or source.getParentGeoFeatureGroup()
            or source.TypeId == "App::Link"):
        raise ValueError(tr("Select one whole solid or Body at the document root. Nested objects and occurrences are outside this setup."))
    require_current(source)
    if source.Shape.isNull() or not source.Shape.isValid() or not source.Shape.Solids:
        raise ValueError(tr("The source must contain current valid solid geometry."))
    return (identity(source), source.Shape.hashCode())


def options(source, template, scale, orientation, convention, projected):
    if template not in TEMPLATES or orientation not in ORIENTATIONS:
        raise ValueError(tr("Choose an available template and orientation."))
    if convention not in ("First angle", "Third angle"):
        raise ValueError(tr("Choose first-angle or third-angle projection."))
    if not math.isfinite(scale) or scale <= 0:
        raise ValueError(tr("Scale must be a finite positive drawing/model ratio."))
    filename, width, height = TEMPLATES[template]
    path = Path(App.getResourceDir()) / "Mod/TechDraw/Templates/ISO" / filename
    if not path.is_file():
        raise ValueError(tr("The selected built-in template is missing."))
    # A conservative rotation-independent envelope leaves room for borders/title block.
    span = source.Shape.BoundBox.DiagonalLength * scale
    envelope = 2 * span + 20 if projected else span
    if envelope > min(width - 30, height - 55):
        raise ValueError(tr("The view envelope is too large for this sheet. Reduce scale or choose a larger sheet."))
    return str(path), width, height


def create_drawing(source, expected, template, scale, orientation, convention, projected):
    doc = source.Document
    if App.ActiveDocument != doc or doc.HasPendingTransaction or Gui.Control.activeDialog():
        raise ValueError(tr("Activate this document and finish the current task or edit transaction."))
    if review(source) != expected:
        raise ValueError(tr("The source changed. Review again before creating the drawing."))
    path, width, height = options(source, template, scale, orientation, convention, projected)
    doc.openTransaction("Create drawing sheet")
    try:
        page = doc.addObject("TechDraw::DrawPage", "DrawingSheet")
        page.Label = source.Label + tr(" drawing")
        svg = doc.addObject("TechDraw::DrawSVGTemplate", "DrawingTemplate")
        svg.Template = path
        page.Template = svg
        page.Scale = scale
        page.ProjectionType = convention
        group = doc.addObject("TechDraw::DrawProjGroup", "DrawingViews")
        page.addView(group)
        group.Source = [source]
        group.ScaleType = "Custom"
        group.Scale = scale
        group.ProjectionType = convention
        group.AutoDistribute = True
        group.spacingX = 15
        group.spacingY = 15
        group.X = width / 2
        group.Y = height / 2 + 15
        group.addProjection("Front")
        direction, xdirection = ORIENTATIONS[orientation]
        group.Anchor.Direction = App.Vector(*direction)
        group.Anchor.XDirection = App.Vector(*xdirection)
        if projected:
            group.addProjection("Top")
            group.addProjection("Right")
        doc.recompute()
        if any("Invalid" in obj.State for obj in [page, group] + list(group.Views)):
            raise ValueError(tr("The drawing could not recompute. No partial sheet was kept."))
        doc.commitTransaction()
        return page
    except Exception:
        doc.abortTransaction()
        doc.recompute()
        raise


class DrawingDialog(QtWidgets.QDialog):
    def __init__(self, source, parent=None):
        super().__init__(parent)
        self.key = identity(source)
        self.doc = source.Document
        self.expected = None
        self.closed = False
        self.saving = False
        self.page = None
        self.setWindowTitle(tr("Create drawing sheet"))
        self.resize(630, 390)
        layout = QtWidgets.QVBoxLayout(self)
        self.sourceLabel = QtWidgets.QLabel(tr("Source: ") + source.Label + " [" + source.Name + "]")
        self.sourceLabel.setTextFormat(QtCore.Qt.PlainText)
        layout.addWidget(self.sourceLabel)
        form = QtWidgets.QFormLayout()
        self.template = QtWidgets.QComboBox()
        self.template.addItems(list(TEMPLATES))
        self.scale = QtWidgets.QDoubleSpinBox()
        self.scale.setRange(0.001, 100)
        self.scale.setDecimals(3)
        self.scale.setValue(1)
        self.orientation = QtWidgets.QComboBox()
        self.orientation.addItems(list(ORIENTATIONS))
        self.convention = QtWidgets.QComboBox()
        self.convention.addItems(["First angle", "Third angle"])
        self.projected = QtWidgets.QCheckBox(tr("Add top and right projections"))
        self.projected.setChecked(True)
        for label, widget in [(tr("Sheet template"), self.template),
                              (tr("Scale (drawing / model)"), self.scale),
                              (tr("Base orientation"), self.orientation),
                              (tr("Projection convention"), self.convention),
                              (tr("Views"), self.projected)]:
            form.addRow(label, widget)
        layout.addLayout(form)
        note = QtWidgets.QLabel(tr(
            "Sheet coordinates are millimetres. Views stay linked to this source in this "
            "document and update through native recompute. First/third angle controls "
            "projected view placement. Create commits one Undo step; Cancel creates nothing. "
            "Open the resulting sheet to inspect the geometry. Annotations, section/detail "
            "views and occurrence sources use separate workflows."))
        note.setWordWrap(True)
        layout.addWidget(note)
        self.message = QtWidgets.QLabel()
        self.message.setTextFormat(QtCore.Qt.PlainText)
        self.message.setWordWrap(True)
        layout.addWidget(self.message)
        buttons = QtWidgets.QHBoxLayout()
        self.reviewButton = QtWidgets.QPushButton(tr("Review again"))
        self.createButton = QtWidgets.QPushButton(tr("Create sheet"))
        cancel = QtWidgets.QPushButton(tr("Cancel"))
        for button in (self.reviewButton, self.createButton, cancel):
            button.setAutoDefault(False)
            buttons.addWidget(button)
        layout.addLayout(buttons)
        self.reviewButton.clicked.connect(self.refresh)
        self.createButton.clicked.connect(self.commit)
        cancel.clicked.connect(self.reject)
        self.refresh()
        App.addDocumentObserver(self)

    def refresh(self):
        self.expected = None
        self.createButton.setEnabled(False)
        try:
            self.expected = review(resolve(self.key))
            self.createButton.setEnabled(True)
            self.message.setText(tr("Ready. The sheet and all views will be created together."))
        except Exception as error:
            self.message.setText(str(error))

    def commit(self):
        if self.expected is None:
            return
        self.saving = True
        try:
            self.page = create_drawing(resolve(self.key), self.expected, self.template.currentText(),
                                       self.scale.value(), self.orientation.currentText(),
                                       self.convention.currentText(), self.projected.isChecked())
            self.accept()
            # Native page display can finish asynchronously after creation commits.
            self.page.ViewObject.show()
        except Exception as error:
            self.message.setText(str(error))
        finally:
            self.saving = False

    def invalidate(self, obj):
        if obj.Document == self.doc and not self.closed and not self.saving:
            self.expected = None
            self.createButton.setEnabled(False)
            self.message.setText(tr("The document changed. Recompute if needed, then Review again."))

    def slotChangedObject(self, obj, prop):
        self.invalidate(obj)

    def slotCreatedObject(self, obj):
        self.invalidate(obj)

    def slotDeletedObject(self, obj):
        if identity(obj) == self.key:
            self.reject()
        else:
            self.invalidate(obj)

    def slotDeletedDocument(self, doc):
        if doc == self.doc:
            self.reject()

    def done(self, result):
        if not self.closed:
            self.closed = True
            App.removeDocumentObserver(self)
        super().done(result)


_dialogs = []


class CommandDrawingSetup:
    def GetResources(self):
        return {"MenuText": tr("Create drawing sheet..."), "Pixmap": "TechDraw_PageDefault",
                "ToolTip": tr("Choose a template and linked orthographic views for one root solid")}

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        selected = Gui.Selection.getSelectionEx("*", 0)
        if len(selected) != 1 or selected[0].SubElementNames:
            QtWidgets.QMessageBox.information(Gui.getMainWindow(), tr("Create drawing sheet"),
                                             tr("Select one whole root solid or Body in the tree."))
            return
        dialog = DrawingDialog(selected[0].Object, Gui.getMainWindow())
        _dialogs.append(dialog)
        dialog.finished.connect(lambda _result: _dialogs.remove(dialog) if dialog in _dialogs else None)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()


Gui.addCommand("TechDraw_DrawingSetup", CommandDrawingSetup())
