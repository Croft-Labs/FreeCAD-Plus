# SPDX-License-Identifier: LGPL-2.1-or-later
"""Review the existing Extend Face command before native feature creation."""
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtWidgets
from freecad.gui.OccurrenceMove import Ghost
import ExtendFaceReview as Review

tr = Review.tr
_dialogs = []


class ExtendDialog(QtWidgets.QDialog):
    def __init__(self, source, face, parent=None):
        super().__init__(parent)
        self.ref = Review.Input(source, face)
        self.doc = source.Document
        self.previewed = self.ghost = self.result = None
        self.closed = self.busy = False
        self.setWindowTitle(tr("Extend Face"))
        self.resize(590, 510)
        layout = QtWidgets.QVBoxLayout(self)

        def label(text):
            widget = QtWidgets.QLabel(text)
            widget.setWordWrap(True)
            widget.setTextFormat(QtCore.Qt.PlainText)
            layout.addWidget(widget)
            return widget

        label(self.ref.label)
        label(tr("Samples the underlying surface over an expanded rectangular U/V domain and fits a B-spline face. "
                 "Percentages refer to parameter spans, not millimetres. Positive grows; negative shrinks. "
                 "Original trimming loops and holes are not retained. This is an approximation, not recovery of original design intent."))
        form = QtWidgets.QFormLayout()
        self.fields = {}
        for prop, title in (("ExtendUNeg", "U negative side (%)"), ("ExtendUPos", "U positive side (%)"),
                            ("ExtendVNeg", "V negative side (%)"), ("ExtendVPos", "V positive side (%)"),
                            ("Tolerance", "Fitting tolerance (mm)"), ("SampleU", "U samples"), ("SampleV", "V samples")):
            if prop.startswith("Sample"):
                widget = QtWidgets.QSpinBox()
                widget.setRange(4, 64)
                widget.setValue(32)
            else:
                widget = QtWidgets.QDoubleSpinBox()
                widget.setDecimals(7 if prop == "Tolerance" else 3)
                widget.setRange(1e-7, 10) if prop == "Tolerance" else widget.setRange(-50, 1000)
                widget.setValue(0.1 if prop == "Tolerance" else 5)
            widget.setObjectName(prop)
            widget.valueChanged.connect(self.invalidate)
            self.fields[prop] = widget
            form.addRow(tr(title), widget)
        layout.addLayout(form)
        label(tr("Preview shows the fitted face boundary. Create saves a separate extended surface linked to the source. "
                 "Source geometry and visibility are preserved. The fitting tolerance is not a certified maximum deviation or self-intersection check."))
        self.message = label(tr("Review the settings, then preview."))
        self.message.setObjectName("extendReviewStatus")
        row = QtWidgets.QHBoxLayout()
        self.previewButton = QtWidgets.QPushButton(tr("Preview surface"))
        self.createButton = QtWidgets.QPushButton(tr("Create surface"))
        self.cancelButton = QtWidgets.QPushButton(tr("Cancel"))
        for button in (self.previewButton, self.createButton, self.cancelButton):
            button.setAutoDefault(False)
            row.addWidget(button)
        layout.addLayout(row)
        self.previewButton.clicked.connect(self.preview)
        self.createButton.clicked.connect(self.commit)
        self.cancelButton.clicked.connect(self.reject)
        self.createButton.setEnabled(False)
        App.addDocumentObserver(self)

    def invalidate(self, *args):
        if self.ghost is not None:
            self.ghost.remove()
            self.ghost = None
        self.previewed = None
        self.createButton.setEnabled(False)
        self.message.setText(tr("Preview required after changed inputs."))

    def values(self):
        return {prop: field.value() / (100. if prop.startswith("Extend") else 1)
                for prop, field in self.fields.items()}

    def preview(self):
        self.invalidate()
        self.busy = True
        try:
            checked = Review.probe(self.ref, self.values())
            self.ghost = Ghost(Part.makeCompound(checked["shape"].Edges))
            self.previewed = checked
            self.createButton.setEnabled(True)
            self.message.setText(tr("Preview: one fitted sheet face, area {area:.9g} mm². Source unchanged; no feature created yet.").format(area=checked["shape"].Area))
        except Exception as error:
            self.message.setText(str(error))
        finally:
            self.busy = False

    def commit(self):
        self.busy = True
        try:
            self.result = Review.create(self.previewed)
            self.accept()
        except Exception as error:
            self.invalidate()
            self.message.setText(str(error))
        finally:
            self.busy = False

    def slotChangedObject(self, obj, prop):
        if obj.Document == self.doc and not self.busy and not self.closed:
            self.invalidate()

    def slotDeletedObject(self, obj):
        if obj.Document == self.doc and not self.closed:
            self.invalidate()

    def slotDeletedDocument(self, doc):
        if doc == self.doc:
            self.reject()

    def slotActivateDocument(self, doc):
        if doc != self.doc and not self.busy and not self.closed:
            self.invalidate()

    def done(self, result):
        if not self.closed:
            self.closed = True
            self.invalidate()
            App.removeDocumentObserver(self)
        super().done(result)


def show():
    selection = Gui.Selection.getSelectionEx("*", 0)
    try:
        if len(selection) != 1 or len(selection[0].SubElementNames) != 1:
            raise ValueError(tr("Select a single face on a root Part shape or Body."))
        dialog = ExtendDialog(selection[0].Object, selection[0].SubElementNames[0], Gui.getMainWindow())
    except Exception as error:
        QtWidgets.QMessageBox.warning(Gui.getMainWindow(), tr("Extend Face"), str(error))
        return None
    _dialogs.append(dialog)
    dialog.finished.connect(lambda _r: _dialogs.remove(dialog) if dialog in _dialogs else None)
    dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    dialog.show()
    return dialog
