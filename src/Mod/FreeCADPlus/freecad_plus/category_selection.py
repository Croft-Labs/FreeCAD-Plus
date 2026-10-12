# SPDX-License-Identifier: LGPL-2.1-or-later
"""Independent Plus viewport category admission, intersected with native gates."""
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets

CATEGORIES = ('Planes', 'Bodies', 'Surfaces', 'Faces', 'Edges', 'Curves', 'Points', 'Vertices')
_controller = None


def preferences():
    from .selection_toolbar import preferences as selection_preferences
    return selection_preferences().GetGroup('Categories')


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
    def __init__(self):
        super().__init__(Gui.getMainWindow())
        self.active = False
        self.enabled = {}
        self.cache = {}
        QtWidgets.QApplication.instance().installEventFilter(self)

    def configure(self, active):
        self.enabled = {name: preferences().GetBool(name, True) for name in CATEGORIES}
        if active != self.active:
            Gui.Selection.setPlusSelectionGate(self if active else None)
        self.active = active
        self.end_pick()

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


def append_controls(row):
    button = QtWidgets.QToolButton()
    button.setObjectName('PlusSelectionCategories')
    button.setText('Selection categories')
    button.setAccessibleName('Selection categories')
    button.setToolTip('Selection categories\nChoose the geometry allowed for viewport selection.')
    button.setIcon(Gui.getIcon('view-select'))
    button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
    button.setAutoRaise(True)
    button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
    menu = QtWidgets.QMenu(button)
    for name in CATEGORIES:
        action = menu.addAction(name)
        action.setCheckable(True)
        action.setChecked(preferences().GetBool(name, True))
        def changed(checked, name=name):
            preferences().SetBool(name, checked)
            _controller.configure(True)
            Gui.Selection.clearPreselection()
        action.toggled.connect(changed)
    button.setMenu(menu)
    row.addWidget(button)
