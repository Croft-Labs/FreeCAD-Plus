# SPDX-License-Identifier: LGPL-2.1-or-later
"""Independent Plus viewport category admission, intersected with native gates."""
import FreeCADGui as Gui
from PySide6 import QtCore, QtGui, QtWidgets

CATEGORIES = ('Planes', 'Bodies', 'Surfaces', 'Faces', 'Edges', 'Curves', 'Points', 'Vertices')
_controller = None


def preferences():
    from .selection_toolbar import preferences as selection_preferences
    return selection_preferences().GetGroup('Categories')


def enabled_categories():
    """Repair legacy empty filters before they can block all viewport picking."""
    prefs = preferences()
    enabled = {name for name in CATEGORIES if prefs.GetBool(name, True)}
    if not enabled:
        enabled = set(CATEGORIES)
        for name in CATEGORIES:
            prefs.SetBool(name, True)
    return enabled


def set_categories(enabled):
    """Commit a complete nonempty filter before refreshing the native gate."""
    enabled = set(enabled)
    if not enabled or not enabled.issubset(CATEGORIES):
        raise ValueError('Choose at least one known selection category')
    prefs = preferences()
    for name in CATEGORIES:
        prefs.SetBool(name, name in enabled)
    if _controller is not None:
        _controller.configure(_controller.active)
    Gui.Selection.clearPreselection()


def category(root, subname):
    """Classify the native geometry owner without following dependency graphs."""
    import Part
    prefix, _, _ = Part.splitSubname(subname or '')
    owner = root.getSubObject(prefix, 1) if prefix else root
    if owner is None:
        return None
    owner = owner.getLinkedObject(True)
    element = Part.splitSubname(root.resolveSubElement(subname or '')[2])[2]
    kind = owner.TypeId
    if kind in ('App::Plane', 'PartDesign::Plane', 'Part::DatumPlane'):
        return 'Planes'
    if kind in ('App::Origin', 'PartDesign::Point', 'Part::DatumPoint'):
        return 'Points'
    if owner.isDerivedFrom('Sketcher::SketchObject'):
        if element.startswith('Constraint'):
            return None  # Constraint editing remains a native Sketcher operation.
        if element.startswith('Vertex') or element == 'RootPoint':
            return 'Points'
        if element in ('H_Axis', 'V_Axis'):
            return None
        return 'Curves'
    if not hasattr(owner, 'Shape'):
        return None  # Preserve workbench-specific objects outside this taxonomy.
    shape = owner.Shape
    if shape.isNull():
        return None
    if shape.Solids:
        for prefix, result in (('Face', 'Faces'), ('Edge', 'Edges'), ('Vertex', 'Vertices')):
            if element.startswith(prefix):
                return result
        return 'Bodies'
    if shape.Faces:
        return 'Surfaces'
    if element.startswith('Vertex') or not shape.Edges:
        return 'Points'
    return 'Curves'


class Controller(QtCore.QObject):
    changed = QtCore.Signal()

    def __init__(self):
        super().__init__(Gui.getMainWindow())
        self.active = False
        self.enabled = {}
        self.cache = {}
        QtWidgets.QApplication.instance().installEventFilter(self)

    def configure(self, active):
        enabled = enabled_categories()
        previous = self.enabled
        self.enabled = {name: name in enabled for name in CATEGORIES}
        if active != self.active:
            Gui.Selection.setPlusSelectionGate(self if active else None)
        self.active = active
        self.end_pick()
        if previous != self.enabled:
            self.changed.emit()

    def eventFilter(self, watched, event):
        if self.active and event.type() in (QtCore.QEvent.MouseMove,
                                            QtCore.QEvent.MouseButtonPress,
                                            QtCore.QEvent.MouseButtonRelease):
            widget = watched if isinstance(watched, QtWidgets.QWidget) else None
            while widget is not None:
                if widget.inherits('Gui::View3DInventorViewer'):
                    Gui.getMainWindow().setProperty('FreeCADPlusCategoryPicking', True)
                    QtCore.QTimer.singleShot(0, self.end_pick)
                    break
                widget = widget.parentWidget()
        return False

    def end_pick(self):
        Gui.getMainWindow().setProperty('FreeCADPlusCategoryPicking', None)
        self.cache.clear()

    def allow(self, doc, root, sub):
        if all(self.enabled.values()):
            return True
        key = (doc.Name, root.Name, sub or '')
        if key not in self.cache:
            self.cache[key] = category(root, sub)
        return self.enabled.get(self.cache[key], True)


def apply(active):
    global _controller
    if _controller is None:
        _controller = Controller()
    _controller.configure(active)


class CategoryButton(QtWidgets.QToolButton):
    def __init__(self):
        super().__init__()
        self.armed = False
        self.setObjectName('PlusSelectionCategories')
        self.setAccessibleName('Selection categories')
        self.setIcon(Gui.getIcon('view-select'))
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.setAutoRaise(True)
        self.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        menu = QtWidgets.QMenu(self)
        panel = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setContentsMargins(12, 10, 12, 12)
        actions = QtWidgets.QHBoxLayout()
        reset = QtWidgets.QPushButton('Select all / reset')
        reset.setObjectName('SelectAllReset')
        self.select_one = QtWidgets.QPushButton('Select 1')
        self.select_one.setObjectName('SelectOneCategory')
        self.select_one.setCheckable(True)
        actions.addWidget(reset)
        actions.addWidget(self.select_one)
        layout.addLayout(actions)
        self.hint = QtWidgets.QLabel()
        self.hint.setWordWrap(True)
        self.hint.setFixedWidth(270)
        self.hint.setMinimumHeight(52)
        layout.addWidget(self.hint)
        self.boxes = {}
        for name in CATEGORIES:
            box = QtWidgets.QCheckBox(name)
            box.setObjectName('Category' + name)
            self.boxes[name] = box
            layout.addWidget(box)
            box.clicked.connect(lambda checked, name=name: self.choose(name, checked))
        action = QtWidgets.QWidgetAction(menu)
        action.setDefaultWidget(panel)
        menu.addAction(action)
        reset.clicked.connect(self.reset_all)
        self.select_one.clicked.connect(self.arm)
        menu.aboutToShow.connect(self.refresh)
        menu.aboutToHide.connect(self.dismiss)
        self.setMenu(menu)
        if _controller is not None:
            _controller.changed.connect(self.refresh)
        self.refresh()

    @QtCore.Slot()
    def refresh(self):
        enabled = enabled_categories()
        omitted = [name for name in CATEGORIES if name not in enabled]
        if not omitted:
            summary = 'All'
        elif len(enabled) == 1:
            summary = next(iter(enabled)) + ' only'
        elif len(omitted) == 1:
            summary = omitted[0] + ' omitted'
        else:
            summary = str(len(omitted)) + ' omitted'
        self.setText(summary)
        self.setToolTip('Selection categories: ' + summary + '\nAllowed: ' +
                       ', '.join(name for name in CATEGORIES if name in enabled))
        for name, box in self.boxes.items():
            box.setChecked(name in enabled)
            box.setEnabled(self.armed or len(enabled) > 1 or name not in enabled)
        self.select_one.setChecked(self.armed)
        if self.armed:
            self.hint.setText('Choose one category below. Click outside to keep the current filter.')
            self.hint.setStyleSheet('QLabel { background: #fff0bf; color: #604300; '
                                   'border: 1px solid #c78a20; padding: 6px; }')
        else:
            self.hint.setText('At least one category must stay selected.' if len(enabled) == 1
                              else 'Choose which geometry can be selected.')
            self.hint.setStyleSheet('')

    def choose(self, name, checked):
        enabled = enabled_categories()
        armed = self.armed
        self.armed = False
        if armed:
            enabled = {name}
        elif checked:
            enabled.add(name)
        elif len(enabled) > 1:
            enabled.discard(name)
        set_categories(enabled)
        self.refresh()
        if armed:
            self.menu().close()

    def reset_all(self):
        self.armed = False
        set_categories(CATEGORIES)
        self.refresh()

    def arm(self, checked):
        # No settings or gate changes until the replacement category is chosen.
        self.armed = checked
        self.refresh()

    def dismiss(self):
        self.armed = False
        self.refresh()


def append_controls(row):
    row.addWidget(CategoryButton())
