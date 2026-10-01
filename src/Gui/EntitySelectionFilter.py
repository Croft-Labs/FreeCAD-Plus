# SPDX-License-Identifier: LGPL-2.1-or-later
"""Session entity policy, intersected with native command selection gates."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets


_panel = None
_parameter_path = "User parameter:BaseApp/Preferences/SelectionFilter"
_labels = ("All entities", "Vertices only", "Edges only", "Faces only", "Whole objects only")


def _tr(text):
    return QtCore.QCoreApplication.translate("SelectionFilter", text)


def mode():
    value = App.ParamGet(_parameter_path).GetInt("EntityMode", 0)
    return value if 0 <= value < len(_labels) else 0


def set_mode(value):
    if type(value) is not int or not 0 <= value < len(_labels):
        raise ValueError("Unknown entity selection filter")
    App.ParamGet(_parameter_path).SetInt("EntityMode", value)
    Gui.Selection.clearPreselection()
    # Keep deliberate existing selections. Only subsequent picks are filtered.
    if _panel is not None:
        _panel.refresh()


class FilterPanel(QtWidgets.QDialog):
    def __init__(self):
        super().__init__(Gui.getMainWindow())
        self.setObjectName("EntitySelectionFilterPanel")
        self.setWindowTitle(_tr("Selection filters"))
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.setModal(False)
        layout = QtWidgets.QVBoxLayout(self)
        self.combo = QtWidgets.QComboBox(self)
        self.combo.setObjectName("entityFilterMode")
        self.combo.addItems([_tr(label) for label in _labels])
        label = QtWidgets.QLabel(_tr("Selectable &entities:"), self)
        label.setBuddy(self.combo)
        layout.addWidget(label)
        layout.addWidget(self.combo)
        explanation = QtWidgets.QLabel(_tr(
            "Filters new picks in the viewport and Select Other. Command selection rules "
            "still apply. Existing selections are kept. Whole objects includes components, "
            "bodies, sketches and features together.\n\n"
            "The filter stays active while this window is open, including during commands. "
            "Reset, Close or Escape restores All entities."), self)
        explanation.setWordWrap(True)
        layout.addWidget(explanation)
        buttons = QtWidgets.QDialogButtonBox(self)
        reset = buttons.addButton(_tr("&Reset to all"), QtWidgets.QDialogButtonBox.ResetRole)
        reset.setObjectName("resetEntityFilter")
        reset.clicked.connect(lambda: set_mode(0))
        buttons.addButton(QtWidgets.QDialogButtonBox.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.indicator = QtWidgets.QPushButton(Gui.getMainWindow())
        self.indicator.setObjectName("entityFilterIndicator")
        self.indicator.setToolTip(_tr("Click to reset the entity filter to All entities"))
        self.indicator.clicked.connect(lambda: set_mode(0))
        Gui.getMainWindow().statusBar().addPermanentWidget(self.indicator)
        self.combo.currentIndexChanged.connect(set_mode)
        self.resize(440, 230)
        self.refresh()

    def refresh(self):
        current = mode()
        self.combo.blockSignals(True)
        self.combo.setCurrentIndex(current)
        self.combo.blockSignals(False)
        self.indicator.setText(_tr("Pick filter: ") + _tr(_labels[current]) + _tr(" — Reset"))
        self.indicator.setVisible(current != 0)

    def done(self, result):
        set_mode(0)
        super().done(result)

    def closeEvent(self, event):
        set_mode(0)
        super().closeEvent(event)


class _Command:
    def GetResources(self):
        return {"MenuText": _tr("Selection filters…"),
                "ToolTip": _tr("Restrict new picks to vertices, edges, faces or whole objects")}

    def IsActive(self):
        return True

    def Activated(self):
        global _panel
        if _panel is None:
            _panel = FilterPanel()
        _panel.refresh()
        _panel.show()
        _panel.raise_()
        _panel.activateWindow()


def registerCommand():
    # Never resume a restrictive policy from a previous application session.
    App.ParamGet(_parameter_path).SetInt("EntityMode", 0)
    Gui.addCommand("Std_EntitySelectionFilter", _Command())
