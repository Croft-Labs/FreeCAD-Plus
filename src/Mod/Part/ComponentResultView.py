# SPDX-License-Identifier: LGPL-2.1-or-later
"""One public operation, with a protected result retained for engineering links."""
import FreeCAD as App

_syncing = False
_observer = None


def sync(result):
    global _syncing
    import ComponentModel as Model
    if not App.GuiUp or _syncing or result.Document.Restoring or not Model.background_result(result):
        return
    producer = result.Producer
    if producer is None:
        return
    _syncing = True
    try:
        producer.Visibility = bool(result.Visibility) and Model.history_state(result) == "Ready" and not result.Shape.isNull()
    finally:
        _syncing = False


class ResultViewProvider:
    def attach(self, view):
        from pivy import coin
        view.addDisplayMode(coin.SoSeparator(), "Background")
        view.ShowInTree = False

    def getDisplayModes(self, view):
        return ["Background"]

    def getDefaultDisplayMode(self):
        return "Background"

    def setDisplayMode(self, mode):
        return "Background"

    def updateData(self, obj, prop):
        # ResultProxy publishes availability after the complete recompute, avoiding
        # transient empty geometry hiding its producer halfway through execution.
        if prop in ("Producer", "UserSuppressed", "Frozen"):
            sync(obj)

    def onChanged(self, view, prop):
        if prop == "Visibility":
            sync(view.Object)

    def canDelete(self, obj):
        return True  # Deleting the producing operation is allowed; transaction cleanup owns its result.

    def onDelete(self, view, subelements):
        import ComponentModel as Model
        if Model.background_result(view.Object):
            App.Console.PrintWarning("This is a background result. Delete its producing operation instead.\n")
            return False
        return True

    def dumps(self):
        return None

    def loads(self, state):
        pass


class DisplayObserver:
    def slotChangedObject(self, view, prop):
        if _syncing or prop != "Visibility":
            return
        import ComponentModel as Model
        try:
            obj = view.Object
        except (RuntimeError, App.Base.FreeCADError):
            return  # Native view providers can outlive their object during undo/close.
        if getattr(obj, "ComponentRole", "") != "Operation":
            return
        if obj.Document.Restoring or Model.history_state(obj) != "Ready":
            return
        result = Model.result_for_operation(obj)
        if result != obj and Model.background_result(result) and Model.history_state(result) == "Ready":
            result.Visibility = bool(obj.Visibility)


def install(result):
    global _observer
    import ComponentModel as Model
    if not App.GuiUp:
        return
    view = result.ViewObject
    if Model.background_result(result):
        if not isinstance(view.Proxy, ResultViewProvider):
            view.Proxy = ResultViewProvider()
        view.ShowInTree = False
        if view.DisplayMode != "Background":
            view.DisplayMode = ["Background"]
            view.DisplayMode = "Background"
        sync(result)
    elif isinstance(view.Proxy, ResultViewProvider):
        view.Proxy = 0
        view.ShowInTree = True
        view.DisplayMode = ["Flat Lines", "Shaded", "Wireframe", "Points"]
        view.DisplayMode = "Flat Lines"
    if _observer is None:
        import FreeCADGui as Gui
        _observer = DisplayObserver()
        Gui.addDocumentObserver(_observer)
