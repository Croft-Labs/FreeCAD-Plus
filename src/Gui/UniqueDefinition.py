# SPDX-License-Identifier: LGPL-2.1-or-later
"""Make one native sketch/extrusion Part occurrence independent."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.DependencyInspector import identity, resolve


def tr(text):
    return App.Qt.translate("UniqueDefinition", text)


def selected_occurrence():
    selection = Gui.Selection.getSelectionEx("*", 0)
    if len(selection) != 1:
        raise ValueError(tr("Select one whole Link in the tree, without faces or occurrence paths."))
    link = selection[0].Object
    subnames = selection[0].SubElementNames
    if subnames:
        if len(subnames) != 1 or not subnames[0].endswith("."):
            raise ValueError(tr("Select the whole Link, not a face or edge."))
        path = link.getSubObjectList(subnames[0])
        if not path or any(obj.TypeId != "App::Part" for obj in path[:-1]):
            raise ValueError(tr("Select the Link itself, not a path through another occurrence."))
        link = path[-1]
    return link


def review(link):
    from BasicShapes.ShapeReferences import require_current
    if (link.TypeId != "App::Link" or link.ElementCount or link.Scale != 1
            or tuple(link.ScaleVector) != (1, 1, 1)):
        raise ValueError(tr("Select a direct, unscaled native Link, not an array or definition."))
    source = link.LinkedObject
    if source is None or source.Document != link.Document or source.TypeId != "App::Part":
        raise ValueError(tr("This workflow requires a same-document Part definition."))
    members = list(source.Group)
    sketches = [obj for obj in members if obj.TypeId == "Sketcher::SketchObject"]
    extrusions = [obj for obj in members if obj.TypeId == "Part::Extrusion"]
    if (len(members) != 2 or len(sketches) != 1 or len(extrusions) != 1
            or extrusions[0].Base != sketches[0]):
        raise ValueError(tr("Supported definition: one independent sketch and its native Part extrusion."))
    if any(dep not in members for obj in members for dep in obj.OutList):
        raise ValueError(tr("External or attached inputs are outside this copy workflow. No links will be detached silently."))
    if any(obj.ExpressionEngine or hasattr(obj, "SemanticIdentity") for obj in [source] + members):
        raise ValueError(tr("Expression-driven or prototype-identity definitions are outside this workflow."))
    if any(obj.TypeId != "App::Part" for obj in link.InList):
        raise ValueError(tr("This occurrence has consumers or relationships. Their remapping is outside this workflow."))
    require_current(link)
    shape = extrusions[0].Shape
    if shape.isNull() or not shape.isValid() or not shape.Solids:
        raise ValueError(tr("The extrusion must have a current valid solid result."))
    return {"link": identity(link), "source": identity(source),
            "members": [identity(obj) for obj in members],
            "shape": shape.hashCode(), "placement": tuple(link.LinkPlacement.toMatrix().A),
            "source_placement": tuple(source.Placement.toMatrix().A)}


def make_unique(link, expected, label):
    if App.ActiveDocument != link.Document or Gui.Control.activeDialog() or link.Document.HasPendingTransaction:
        raise ValueError(tr("Activate this document and finish the current task or edit transaction."))
    if review(link) != expected:
        raise ValueError(tr("The occurrence or definition changed. Review again before copying."))
    if not label.strip() or "\x00" in label:
        raise ValueError(tr("Enter a nonempty name for the independent definition."))
    source = link.LinkedObject
    placement = App.Placement(link.LinkPlacement)
    visible = link.Visibility
    source_members = list(source.Group)
    doc = link.Document
    doc.openTransaction("Make occurrence unique")
    try:
        copied = doc.copyObject(source, True)
        copied.Label = label
        copied.Visibility = source.Visibility
        copied_members = list(copied.Group)
        sketch = next(obj for obj in copied_members if obj.TypeId == "Sketcher::SketchObject")
        extrusion = next(obj for obj in copied_members if obj.TypeId == "Part::Extrusion")
        if (len(copied_members) != 2 or extrusion.Base != sketch
                or any(obj in source_members for obj in copied_members)
                or any(dep not in copied_members for obj in copied_members for dep in obj.OutList)):
            raise ValueError(tr("The copy did not isolate all feature inputs."))
        link.setLink(copied)
        link.LinkPlacement = placement
        link.Visibility = visible
        doc.recompute()
        if extrusion.Shape.isNull() or not extrusion.Shape.isValid() or "Invalid" in link.State:
            raise ValueError(tr("The independent result failed recompute."))
        doc.commitTransaction()
        return copied
    except Exception:
        doc.abortTransaction()
        doc.recompute()
        raise


class UniqueDialog(QtWidgets.QDialog):
    def __init__(self, link, parent=None):
        super().__init__(parent)
        self.key = identity(link)
        self.doc = link.Document
        self.expected = None
        self.closed = False
        self.saving = False
        self.setWindowTitle(tr("Make occurrence unique"))
        self.resize(720, 430)
        layout = QtWidgets.QVBoxLayout(self)
        self.summary = QtWidgets.QLabel()
        self.summary.setTextFormat(QtCore.Qt.PlainText)
        self.summary.setWordWrap(True)
        layout.addWidget(self.summary)
        self.members = QtWidgets.QTreeWidget()
        self.members.setHeaderLabels([tr("Copied input"), tr("Native type")])
        self.members.setRootIsDecorated(False)
        layout.addWidget(self.members)
        form = QtWidgets.QFormLayout()
        self.name = QtWidgets.QLineEdit()
        form.addRow(tr("New definition label"), self.name)
        layout.addLayout(form)
        note = QtWidgets.QLabel(tr(
            "Copies the Part, its independent sketch and extrusion into this document, "
            "with new native object identities. Internal inputs are remapped; no external "
            "dependencies are retained. Only this occurrence is relinked; its placement "
            "and visibility remain. Existing instances keep the original definition. "
            "Make Unique commits one Undo step and closes; Cancel creates nothing."))
        note.setWordWrap(True)
        layout.addWidget(note)
        self.message = QtWidgets.QLabel()
        self.message.setTextFormat(QtCore.Qt.PlainText)
        self.message.setWordWrap(True)
        layout.addWidget(self.message)
        actions = QtWidgets.QHBoxLayout()
        self.reviewButton = QtWidgets.QPushButton(tr("Review again"))
        self.createButton = QtWidgets.QPushButton(tr("Make Unique"))
        cancel = QtWidgets.QPushButton(tr("Cancel"))
        for button in (self.reviewButton, self.createButton, cancel):
            button.setAutoDefault(False)
            actions.addWidget(button)
        layout.addLayout(actions)
        self.reviewButton.clicked.connect(self.refresh)
        self.createButton.clicked.connect(self.commit)
        cancel.clicked.connect(self.reject)
        self.refresh()
        App.addDocumentObserver(self)

    def refresh(self):
        self.expected = None
        self.createButton.setEnabled(False)
        self.members.clear()
        try:
            link = resolve(self.key)
            self.expected = review(link)
            source = link.LinkedObject
            self.summary.setText(tr("Selected occurrence: ") + link.Label + " [" + link.Name + "]\n" +
                                 tr("Shared definition: ") + source.Label + " [" + source.Name + "]\n" +
                                 tr("Destination: ") + self.doc.Label + " [" + self.doc.Name + "]")
            for obj in source.Group:
                self.members.addTopLevelItem(QtWidgets.QTreeWidgetItem([obj.Label + " [" + obj.Name + "]", obj.TypeId]))
            self.members.resizeColumnToContents(0)
            if not self.name.text():
                self.name.setText(source.Label + tr(" (unique)"))
            self.createButton.setEnabled(True)
            self.message.setText(tr("Ready to copy the reviewed inputs. The original definition will be preserved."))
        except Exception as error:
            self.message.setText(str(error))

    def commit(self):
        if self.expected is None:
            return
        self.saving = True
        try:
            make_unique(resolve(self.key), self.expected, self.name.text())
            self.accept()
        except Exception as error:
            self.message.setText(str(error))
        finally:
            self.saving = False

    def invalidate(self, obj):
        if obj.Document == self.doc and not self.saving and not self.closed:
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


class CommandUnique:
    def GetResources(self):
        return {"MenuText": tr("Make occurrence unique..."),
                "ToolTip": tr("Copy a supported sketch/extrusion Part definition for one occurrence")}

    def IsActive(self):
        return App.ActiveDocument is not None and not Gui.Control.activeDialog()

    def Activated(self):
        try:
            link = selected_occurrence()
        except ValueError as error:
            QtWidgets.QMessageBox.information(Gui.getMainWindow(), tr("Make occurrence unique"), str(error))
            return
        dialog = UniqueDialog(link, Gui.getMainWindow())
        _dialogs.append(dialog)
        dialog.finished.connect(lambda _result: _dialogs.remove(dialog) if dialog in _dialogs else None)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()


def registerCommand():
    Gui.addCommand("Std_MakeOccurrenceUnique", CommandUnique())
