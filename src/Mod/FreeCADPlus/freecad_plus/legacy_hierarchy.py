# SPDX-License-Identifier: LGPL-2.1-or-later
"""Domestic native Part trees and shared Part links, preserving authored frames."""
import FreeCAD as App


def preflight(doc, error, report):
    parts = [o for o in doc.Objects if o.TypeId == "App::Part"]
    owned, parents = set(), {}
    def own(obj, parent=None):
        if obj in owned:
            raise error("Legacy content has multiple structural owners", report)
        owned.add(obj)
        if parent:
            parents[obj] = parent
    def origin(obj):
        own(obj.Origin)
        for feature in obj.Origin.OriginFeatures:
            own(feature)
    for part in parts:
        own(part)
        origin(part)
    for part in parts:
        for child in part.Group:
            if child in parents:
                raise error("Legacy content has multiple structural owners", report)
            parents[child] = part
            if child.TypeId == "App::Part":
                continue
            own(child)
            if child.TypeId == "PartDesign::Body":
                origin(child)
                for feature in child.Group:
                    if "Python" in feature.TypeId:
                        raise error("Scripted Body features require a separate migration", report)
                    own(feature)
            elif child.TypeId not in ("App::Link", "Part::Box", "Part::Feature"):
                raise error("Unsupported legacy Part content; no output written", report)
    links = [o for o in doc.Objects if o.TypeId == "App::Link"]
    for link in links:
        if link not in owned:
            own(link)
        if (link.LinkedObject not in parts or link.ElementCount or link.LinkCopyOnChange != "Disabled"
                or link.Scale != 1 or not link.ScaleVector.isEqual(App.Vector(1, 1, 1), 1e-9)):
            raise error("Only ordinary domestic links to Part definitions are supported", report)
    if owned != set(doc.Objects):
        raise error("Legacy hierarchy contains unsupported or unowned content", report)
    visiting, complete = set(), set()
    def visit(part):
        if part in visiting:
            raise error("Circular legacy component nesting", report)
        if part in complete:
            return
        visiting.add(part)
        for child in part.Group:
            if child.TypeId == "App::Part":
                visit(child)
            elif child.TypeId == "App::Link":
                visit(child.LinkedObject)
        visiting.remove(part)
        complete.add(part)
    for part in parts:
        visit(part)
    if any("Invalid" in o.State or "Error" in o.State for o in doc.Objects):
        raise error("Repair legacy feature errors before conversion", report)
    return parts


def convert(doc, parts, root, report):
    """Replace structural Part membership with links, keeping definitions intact."""
    original_groups = {part: list(part.Group) for part in parts}
    children = {child for group in original_groups.values() for child in group}
    top_parts = [part for part in parts if part not in children]
    top_links = [o for o in doc.Objects if o.TypeId == "App::Link" and o not in children]
    visible = {part: part.Visibility if App.GuiUp else True for part in parts}
    report["replaced_group_edges"] = {}
    report["part_instances"] = {}
    def instance(part):
        link = doc.addObject("App::Link", part.Name + "Instance")
        link.setLink(part)
        link.LinkTransform = True
        link.LinkPlacement = App.Placement()
        if App.GuiUp:
            link.Visibility = visible[part]
        report["part_instances"][part.Name] = link.Name
        return link
    for part, group in original_groups.items():
        converted = []
        for child in group:
            if child.TypeId == "App::Part":
                link = instance(child)
                report["replaced_group_edges"].setdefault(part.Name, {})[child.Name] = link.Name
                converted.append(link)
            else:
                converted.append(child)
        part.Group = converted
    root.Definitions = parts
    root.Group = [instance(part) for part in top_parts] + top_links
    if App.GuiUp:
        for part in parts:
            part.Visibility = False
