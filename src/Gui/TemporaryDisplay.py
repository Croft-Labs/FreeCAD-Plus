# SPDX-License-Identifier: LGPL-2.1-or-later
"""Session-local visibility snapshots; modeling state and link definitions are untouched."""
import FreeCAD as App
import FreeCADGui as Gui


def _tr(text):
    return App.Qt.translate("TemporaryDisplay", text)


_stacks = {}


def depth(doc=None):
    doc = doc or App.ActiveDocument
    return len(_stacks.get(doc.Name, [])) if doc else 0


def _context():
    doc = App.ActiveDocument
    if doc is None:
        raise ValueError(_tr("Open a document first."))
    if Gui.Control.activeDialog():
        raise ValueError(_tr("Finish or cancel the active task before changing temporary display."))
    if doc.HasPendingTransaction:
        raise ValueError(_tr("Finish the pending edit transaction before changing temporary display."))
    return doc


def _parents(doc):
    """Native containers only: dependencies are not display ownership."""
    parents = {}
    for obj in doc.Objects:
        if obj.isDerivedFrom("App::Link"):
            continue  # Never walk from an occurrence into its shared definition.
        children = []
        if (obj.isDerivedFrom("App::Part") or obj.isDerivedFrom("PartDesign::Body")
                or obj.isDerivedFrom("App::DocumentObjectGroup")):
            children.extend(obj.Group)
            origin = getattr(obj, "Origin", None)
            if origin:
                children.append(origin)
        elif obj.isDerivedFrom("App::Origin"):
            children.extend(obj.OriginFeatures)
        for child in children:
            if child.Document == doc:
                previous = parents.get(child.Name)
                if previous is not None and previous != obj.Name:
                    raise ValueError(_tr("Temporary display requires unambiguous container ownership."))
                parents[child.Name] = obj.Name
    return parents


def _ancestors(name, parents):
    seen = {name}
    while name in parents:
        name = parents[name]
        if name in seen:
            raise ValueError(_tr("A container cycle prevents temporary display."))
        seen.add(name)
        yield name


def _targets(doc, parents):
    targets = set()
    selection = Gui.Selection.getSelectionEx("*", 0)
    if not selection:
        raise ValueError(_tr("Select objects to isolate or hide."))
    for entry in selection:
        if entry.DocumentName != doc.Name:
            raise ValueError(_tr("Select objects in the active document only."))
        for subname in entry.SubElementNames or [""]:
            path = entry.Object.getSubObjectList(subname)
            if not path:
                raise ValueError(_tr("The selected object is no longer available."))
            # Linked subelements address the whole local occurrence, never its source.
            target = next((obj for obj in path if obj.isDerivedFrom("App::Link")), path[-1])
            if target.Document != doc:
                raise ValueError(_tr("Select the local component occurrence instead of its external source."))
            # A Body displays its result. Do not reveal intermediate history features.
            for parent in _ancestors(target.Name, parents):
                owner = doc.getObject(parent)
                if owner.isDerivedFrom("PartDesign::Body"):
                    target = owner
                    break
            targets.add(target.Name)
    return targets


def _snapshot(doc):
    return [(obj.Name, obj.ID, bool(obj.ViewObject.Visibility)) for obj in doc.Objects
            if obj.ViewObject is not None and hasattr(obj.ViewObject, "Visibility")]


def _restore(doc, snapshot):
    parents = _parents(doc)
    # Restore containers before children; native view providers may propagate state.
    for name, identity, visible in sorted(snapshot, key=lambda row: len(list(_ancestors(row[0], parents)))):
        obj = doc.getObject(name)
        if obj is not None and obj.ID == identity and obj.ViewObject is not None:
            if obj.ViewObject.Visibility != visible:
                obj.ViewObject.Visibility = visible


def _notice(doc):
    count = depth(doc)
    message = (_tr("Temporary display: %1 level(s). Use View > Visibility > Restore previous display.")
               .replace("%1", str(count)) if count else _tr("Previous display restored."))
    Gui.getMainWindow().statusBar().showMessage(message, 15000)
    Gui.Command.update()


def apply(mode):
    if mode not in ("isolate", "hide"):
        raise ValueError("Unknown temporary display action")
    doc = _context()
    parents = _parents(doc)
    targets = _targets(doc, parents)
    snapshot = _snapshot(doc)
    changes = {}
    if mode == "hide":
        changes = {name: False for name in targets}
    else:
        required = set(targets)
        for name in targets:
            required.update(_ancestors(name, parents))
        for name, _, visible in snapshot:
            ancestors = set(_ancestors(name, parents))
            if name in required:
                changes[name] = True
            elif ancestors.intersection(targets):
                continue  # Preserve the selected container's existing internal display.
            elif not ancestors or parents.get(name) in required:
                changes[name] = False
    # A no-op does not consume a restore level.
    changes = {name: value for name, value in changes.items()
               if doc.getObject(name).ViewObject.Visibility != value}
    if not changes:
        return False
    try:
        for name, visible in changes.items():
            doc.getObject(name).ViewObject.Visibility = visible
    except Exception:
        _restore(doc, snapshot)
        raise
    _stacks.setdefault(doc.Name, []).append(snapshot)
    _notice(doc)
    return True


def restore(all_levels=False):
    doc = _context()
    stack = _stacks.get(doc.Name, [])
    if not stack:
        return False
    snapshot = stack[0] if all_levels else stack[-1]
    _restore(doc, snapshot)
    if all_levels:
        stack.clear()
    else:
        stack.pop()
    if not stack:
        _stacks.pop(doc.Name, None)
    _notice(doc)
    return True


class _Observer:
    def slotDeletedDocument(self, doc):
        _stacks.pop(doc.Name, None)


_observer = _Observer()


class _DisplayCommand:
    def __init__(self, mode, title, tooltip):
        self.mode, self.title, self.tooltip = mode, title, tooltip

    def GetResources(self):
        return {"MenuText": _tr(self.title), "ToolTip": _tr(self.tooltip)}

    def IsActive(self):
        if (App.ActiveDocument is None or Gui.Control.activeDialog()
                or App.ActiveDocument.HasPendingTransaction):
            return False
        if self.mode in ("restore", "restore_all"):
            return depth() > 0
        return bool(Gui.Selection.getSelection())

    def Activated(self):
        try:
            if self.mode in ("restore", "restore_all"):
                restore(self.mode == "restore_all")
            else:
                apply(self.mode)
        except (ValueError, RuntimeError) as error:
            App.Console.PrintWarning(str(error) + "\n")
            Gui.getMainWindow().statusBar().showMessage(str(error), 15000)


def registerCommands():
    App.addDocumentObserver(_observer)
    for name, mode, title, tooltip in (
        ("Std_TemporaryIsolate", "isolate", "Temporarily isolate selection",
         "Show only the selected objects or whole components; remember the current display"),
        ("Std_TemporaryHide", "hide", "Temporarily hide selection",
         "Hide the selected objects or whole components; remember the current display"),
        ("Std_RestoreDisplay", "restore", "Restore previous display",
         "Restore one temporary display level; new objects retain their current visibility"),
        ("Std_RestoreAllDisplay", "restore_all", "Restore original display",
         "Restore the display before all temporary isolate/hide actions in this document"),
    ):
        Gui.addCommand(name, _DisplayCommand(mode, title, tooltip))
