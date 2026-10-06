# SPDX-License-Identifier: LGPL-2.1-or-later
"""Click-only sketch palette, viewport-clamped placement and one-second travel grace."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets
from freecad.gui import DesignSelection as Selection

_controller = None

# Presentation only: the palette keeps its existing batch/solver execution.
NATIVE_COMMANDS = {
    "construction": "Sketcher_ToggleConstruction",
    "driving": "Sketcher_ToggleDrivingConstraint",
    "reference": "Sketcher_ToggleDrivingConstraint",
    "Concentric": "Sketcher_ConstrainCoincident",
}


def native_action(action):
    name = NATIVE_COMMANDS.get(action.key, action.command or "Sketcher_Constrain" + action.key)
    command = Gui.Command.get(name)
    actions = command.getAction() if command else []
    return actions[0] if actions else None


class NativeButton(QtWidgets.QToolButton):
    """Share native presentation without binding native activation or eligibility."""
    def __init__(self, action, parent):
        super().__init__(parent)
        self.native = native_action(action)
        self.reason = action.reason
        if self.native:
            self.refresh_presentation()
            self.native.changed.connect(self.refresh_presentation)
        else:
            self.setIcon(Gui.getIcon("preferences-general.svg"))
            self.setToolTip(App.Qt.translate("ConstraintPalette", action.label))

    @QtCore.Slot()
    def refresh_presentation(self):
        self.setIcon(self.native.icon())
        self.setToolTip(self.native.toolTip())
        self.setStatusTip(self.reason or self.native.statusTip())


def backend():
    # Avoid loading Sketcher during application startup.
    from freecad.gui import ConstraintPalette
    return ConstraintPalette


def viewport(widget):
    candidate = widget
    while isinstance(widget, QtWidgets.QWidget):
        if "View3DInventor" in widget.metaObject().className():
            return candidate if isinstance(candidate, QtWidgets.QWidget) else widget
        widget = widget.parentWidget()
    return None


def placement(anchor, size, bounds):
    """Qt logical pixels throughout: above first, then below, finally clamp."""
    width, height = min(size.width(), bounds.width()), min(size.height(), bounds.height())
    x = anchor.x() - width // 2
    y = anchor.y() - height - 12
    if y < bounds.top():
        y = anchor.y() + 12
    return QtCore.QRect(max(bounds.left(), min(x, bounds.right() - width + 1)),
                        max(bounds.top(), min(y, bounds.bottom() - height + 1)), width, height)


def corridor(anchor, rect):
    path = QtGui.QPainterPath()
    target = QtCore.QPointF(max(rect.left(), min(anchor.x(), rect.right())),
                           max(rect.top(), min(anchor.y(), rect.bottom())))
    path.moveTo(QtCore.QPointF(anchor))
    path.lineTo(target)
    stroker = QtGui.QPainterPathStroker()
    stroker.setWidth(24)
    region = stroker.createStroke(path)
    region.addEllipse(QtCore.QPointF(anchor), 12, 12)
    region.addRect(QtCore.QRectF(rect.adjusted(-4, -4, 4, 4)))
    return region


class Palette(QtWidgets.QFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("FreeCADPlusConstraintPalette")
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setAutoFillBackground(True)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll.setWidgetResizable(True)
        self.content = QtWidgets.QWidget()
        self.grid = QtWidgets.QGridLayout(self.content)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.scroll.setWidget(self.content)
        layout.addWidget(self.scroll)
        self.buttons = {}

    def update_actions(self, actions, maximum):
        while self.grid.count():
            item = self.grid.takeAt(0)
            item.widget().deleteLater()
        self.buttons.clear()
        icon_size = Gui.getMainWindow().iconSize()
        cell = max(icon_size.width(), icon_size.height()) + 12
        spacing = 4
        columns = max(1, min(6, len(actions), (maximum.width() - 12 + spacing) // (cell + spacing)))
        width = min(maximum.width(), columns * cell + (columns - 1) * spacing + 12)
        self.grid.setSpacing(spacing)
        for index, action in enumerate(actions):
            button = NativeButton(action, self.content)
            button.setAccessibleName(App.Qt.translate("ConstraintPalette", action.label))
            button.setAccessibleDescription(action.reason)
            button.setText("")
            button.setFocusPolicy(QtCore.Qt.NoFocus)
            button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
            button.setIconSize(icon_size)
            button.setFixedSize(min(cell, max(1, width - 12)), cell)
            button.setEnabled(not action.reason and button.native is not None)
            button.setProperty("disabledReason", action.reason)
            button.setProperty("paletteAction", action.key)
            button.installEventFilter(self)
            button.clicked.connect(lambda checked=False, key=action.key: self.controller.execute(key))
            self.grid.addWidget(button, index // columns, index % columns)
            self.buttons[action.key] = button
        self.grid.activate()
        desired = self.content.sizeHint()
        self.resize(width, min(maximum.height(), desired.height() + 12))

    def eventFilter(self, watched, event):
        if event.type() == QtCore.QEvent.ToolTip:
            reason = watched.property("disabledReason")
            if reason:
                Gui.getMainWindow().statusBar().showMessage(reason, 10000)
            QtWidgets.QToolTip.showText(event.globalPos(), watched.toolTip(), watched)
            return True  # Native tooltip also works for disabled controls.
        return False


class Controller(QtCore.QObject):
    def __init__(self):
        super().__init__(Gui.getMainWindow())
        self.palette = None
        self.sketch = None
        self.anchor = None
        self.region = None
        self.press = None
        self.executing = False
        self.generation = 0
        self.dismiss = QtCore.QTimer(self)
        self.dismiss.setSingleShot(True)
        self.dismiss.setInterval(1000)
        self.dismiss.timeout.connect(self.close)
        self.poll = QtCore.QTimer(self)
        self.poll.setInterval(50)
        self.poll.timeout.connect(self.track)
        self.update_timer = QtCore.QTimer(self)
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self.update)
        QtWidgets.QApplication.instance().installEventFilter(self)
        Gui.Selection.addObserver(self)
        App.addDocumentObserver(self)
        Gui.addDocumentObserver(self)

    def valid(self):
        return Selection.active() and self.sketch is not None and backend().editing_sketch() == self.sketch

    def close(self):
        self.generation += 1
        self.dismiss.stop()
        self.poll.stop()
        self.update_timer.stop()
        self.press = None
        if self.palette:
            self.palette.hide()
            self.palette.deleteLater()
        self.palette = self.sketch = self.region = None

    def clicked(self, widget, position, generation):
        if generation != self.generation or not Selection.active():
            return
        sketch = backend().editing_sketch()
        if not sketch or not backend().selected(sketch):
            self.close()
            return
        if self.palette and self.palette.parentWidget() != widget:
            self.close()
        self.sketch = sketch
        self.anchor = widget.mapFromGlobal(position)
        if not self.palette:
            self.palette = Palette(widget, self)
        self.dismiss.stop()
        self.update(reposition=True)
        self.poll.start()

    def update(self, reposition=False):
        if self.executing:
            return
        if not self.valid():
            self.close()
            return
        names = backend().selected(self.sketch)
        actions = backend().actions(self.sketch, names)
        if not actions:
            self.close()
            return
        old = self.palette.geometry()
        bounds = self.palette.parentWidget().rect().adjusted(4, 4, -4, -4)
        self.palette.update_actions(actions, bounds.size())
        if reposition or old.isEmpty():
            rect = placement(self.anchor, self.palette.size(), bounds)
        else:
            # Keep the existing top-left corner while actions update under pointer.
            rect = QtCore.QRect(old.topLeft(), self.palette.size())
            rect.moveLeft(max(bounds.left(), min(rect.left(), bounds.right() - rect.width() + 1)))
            rect.moveTop(max(bounds.top(), min(rect.top(), bounds.bottom() - rect.height() + 1)))
        self.palette.setGeometry(rect)
        self.region = corridor(self.anchor, rect)
        self.palette.show()
        self.palette.raise_()

    def track(self, position=None):
        if self.executing:
            return
        if not self.valid():
            self.close()
            return
        point = self.palette.parentWidget().mapFromGlobal(position or QtGui.QCursor.pos())
        if self.region.contains(QtCore.QPointF(point)):
            self.dismiss.stop()
        elif not self.dismiss.isActive():
            self.dismiss.start()

    def execute(self, key):
        if not self.valid():
            self.close()
            return
        self.executing = True
        self.dismiss.stop()
        try:
            backend().execute(self.sketch, backend().selected(self.sketch), key)
        except (RuntimeError, ValueError, IndexError) as error:
            App.Console.PrintError(str(error) + "\n")
            Gui.getMainWindow().statusBar().showMessage(str(error), 10000)
        finally:
            self.executing = False
        if self.valid():
            self.update()

    def eventFilter(self, watched, event):
        if not Selection.active():
            if self.palette:
                self.close()
            return False
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Escape:
            if self.palette:
                Gui.Selection.clearSelection()
                self.close()
                # A visible contextual palette owns this dismissal. A second
                # native Escape would exit Sketcher and select its parent object.
                return True
            return False
        if (self.palette and isinstance(watched, QtWidgets.QWidget)
                and (watched == self.palette or self.palette.isAncestorOf(watched))):
            return False
        view = viewport(watched)
        if view is None:
            return False
        if event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
            if backend().editing_sketch():
                self.generation += 1
                self.press = (event.globalPos(), self.generation)
        elif event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
            press, self.press = self.press, None
            if press and (press[0] - event.globalPos()).manhattanLength() <= QtWidgets.QApplication.startDragDistance():
                # Native pick and connected-curve expansion finish before sampling selection.
                QtCore.QTimer.singleShot(0, lambda: QtCore.QTimer.singleShot(0, lambda: self.clicked(view, press[0], press[1])))
        elif event.type() == QtCore.QEvent.Resize and self.palette and watched == self.palette.parentWidget():
            self.update_timer.start(0)
        return False

    def addSelection(self, *args):
        if self.palette:
            self.update_timer.start(0)

    removeSelection = addSelection
    clearSelection = addSelection

    def slotChangedObject(self, obj, prop):
        if self.palette and not self.executing and prop in ("Geometry", "Constraints", "ExpressionEngine"):
            self.update_timer.start(0)

    def slotDeletedObject(self, obj):
        if self.palette:
            self.close()

    def slotDeletedDocument(self, doc):
        self.close()

    def slotResetEdit(self, *args):
        self.close()

    def slotUndoDocument(self, doc):
        if self.palette:
            self.update_timer.start(0)

    slotRedoDocument = slotUndoDocument


def install():
    global _controller
    if _controller is None:
        _controller = Controller()
