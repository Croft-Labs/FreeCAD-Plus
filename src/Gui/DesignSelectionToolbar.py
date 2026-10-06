# SPDX-License-Identifier: LGPL-2.1-or-later
"""Design-only toolbar and click-scoped curve intent. Native gates own filtering."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui import DesignSelection as Policy


def tr(text):
    return QtCore.QCoreApplication.translate("DesignSelection", text)


def _selection_keys():
    return {(s.DocumentName, s.ObjectName, sub)
            for s in Gui.Selection.getSelectionEx("*", 0)
            for sub in s.SubElementNames}


class SelectionToolbar(QtWidgets.QToolBar):
    def __init__(self, window):
        super().__init__(tr("Selection"), window)
        self.setObjectName("FreeCADPlusSelection")
        self.setMovable(False)
        self.setFloatable(False)
        self.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        self.toggleViewAction().setVisible(False)
        self.intent = QtWidgets.QComboBox(self)
        self.intent.setObjectName("designCurveIntent")
        self.intent.setAccessibleName(tr("Curve selection"))
        self.intent.addItems([tr(value) for value in Policy.MODES])
        self.intent.setToolTip(tr("Select one curve, endpoint-connected curves, or a tangent chain"))
        self.addWidget(self.intent)
        # Intent is session-local; the owner specified persistent toggle choices.
        self.intent.setCurrentIndex(0)
        self.filters = QtWidgets.QToolButton(self)
        self.filters.setObjectName("designEntityFilters")
        self.filters.setText(tr("Selection Filter"))
        self.filters.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.menu = QtWidgets.QMenu(self.filters)
        self.filters.setMenu(self.menu)
        self.categories = []
        mask = Policy.parameters().GetInt("Categories", Policy.ALL) & Policy.ALL
        for index, label in enumerate(Policy.CATEGORIES):
            action = self.menu.addAction(tr(label))
            action.setCheckable(True)
            action.setChecked(bool(mask & (1 << index)))
            action.toggled.connect(self.set_categories)
            self.categories.append(action)
        self.addWidget(self.filters)
        self.directional = self.addAction(tr("Directional Selection"))
        self.directional.setObjectName("designDirectionalSelection")
        self.directional.setCheckable(True)
        self.directional.setChecked(Policy.parameters().GetBool("Directional", True))
        self.directional.setToolTip(tr("Left to right: enclosed; right to left: crossing. Off: enclosed in either direction."))
        self.directional.toggled.connect(lambda value: Policy.parameters().SetBool("Directional", value))
        self.persistent = self.addAction(tr("Persistent Selection"))
        self.persistent.setObjectName("designPersistentSelection")
        self.persistent.setCheckable(True)
        self.persistent.setChecked(Policy.parameters().GetBool("Persistent", True))
        self.persistent.setToolTip(tr("Keep selected items after operations. Escape or an empty-space click still deselects."))
        self.persistent.toggled.connect(lambda value: Policy.parameters().SetBool("Persistent", value))
        self._press = None
        self._generation = 0
        self._enabled = False
        Policy.parameters().SetBool("Active", False)
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.hide()

    def set_categories(self, *args):
        mask = sum(1 << i for i, action in enumerate(self.categories) if action.isChecked())
        Policy.parameters().SetInt("Categories", mask)
        Gui.Selection.clearPreselection()

    def set_design_active(self, enabled):
        if self._enabled != enabled:
            self._generation += 1
            self._press = None
            Gui.Selection.clearPreselection()
        self._enabled = enabled
        Policy.parameters().SetBool("Active", enabled)
        self.setVisible(enabled)

    @staticmethod
    def _viewport(widget):
        while widget is not None:
            if "View3DInventor" in widget.metaObject().className():
                return True
            widget = widget.parentWidget() if isinstance(widget, QtWidgets.QWidget) else None
        return False

    def eventFilter(self, watched, event):
        if not self._enabled or not self._viewport(watched):
            return False
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Escape:
            from freecad.gui.MoveComponentsTask import _task
            if _task and _task.manipulator and _task.manipulator.dragging:
                # Its viewport-scoped handler cancels the gesture before broader deselection.
                return False
            # Do not consume it: native tools still handle cancellation normally.
            self._generation += 1
            Policy.clear_after_escape()
        elif event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
            self._generation += 1
            document = App.ActiveDocument.Name if App.ActiveDocument else None
            self._press = (event.globalPos(), _selection_keys(), self._generation, document)
        elif event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
            press, self._press = self._press, None
            if press and (event.globalPos() - press[0]).manhattanLength() <= QtWidgets.QApplication.startDragDistance():
                QtCore.QTimer.singleShot(0, lambda: self.expand_click(press[1], press[2], press[3]))
        return False

    def expand_click(self, previous, generation, document):
        if not self._enabled or generation != self._generation or self.intent.currentIndex() == 0:
            return
        if not App.ActiveDocument or App.ActiveDocument.Name != document:
            return
        # An active feature collector owns its input semantics. Do not expand
        # collected references behind its back. Sketch edit is the exception.
        edit = Gui.activeDocument().getInEdit() if Gui.activeDocument() else None
        if Gui.Control.activeDialog() and not (edit and edit.Object.isDerivedFrom("Sketcher::SketchObject")):
            return
        for document, name, sub in sorted(_selection_keys() - previous):
            doc = App.listDocuments().get(document)
            root = doc.getObject(name) if doc else None
            if root is None:
                continue
            try:
                paths = Policy.chain_paths(root, sub, self.intent.currentIndex())
            except (RuntimeError, ValueError, AttributeError):
                continue
            for path in paths:
                # Native addSelection intersects both entity policy and command gate.
                Gui.Selection.addSelection(document, name, path)
