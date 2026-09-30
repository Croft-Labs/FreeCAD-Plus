# SPDX-License-Identifier: LGPL-2.1-or-later

"""Shape references and placement dependencies shared by associative Part features."""

import Part


class ReferenceError(ValueError):
    pass


def require_current(obj):
    """Reject stale dependency results after the caller has requested recompute."""
    for dependency in [obj] + list(obj.OutListRecursive):
        if "Invalid" in dependency.State or "Touched" in dependency.State:
            raise ReferenceError(
                "Input is not current: {}. Recompute or repair it before continuing.".format(
                    dependency.Label
                )
            )


def linked_shape(link):
    if not link or not link[0]:
        raise ReferenceError("Select an input object.")
    obj, subs = link
    if len(subs) > 1:
        raise ReferenceError("Select one object or one face for each field.")
    sub = subs[0] if subs else ""
    shape = Part.getShape(obj, sub, needSubElement=True, transform=True)
    # getShape includes the object's placement, but not its enclosing App::Part/Body.
    if hasattr(obj, "getGlobalPlacement") and hasattr(obj, "Placement"):
        parent = obj.getGlobalPlacement().multiply(obj.Placement.inverse())
        shape = shape.copy()
        shape.transformShape(parent.toMatrix())
    return shape


def validate_link(feature, obj):
    if obj is None or obj.Document != feature.Document:
        raise ReferenceError("Select an object in this document.")
    if obj == feature or obj in feature.InListRecursive:
        raise ReferenceError("A feature cannot reference itself or a dependent feature.")


def update_placement_support(obj, links):
    containers = []
    for link in links:
        if not link or not link[0]:
            continue
        parent = link[0].getParentGeoFeatureGroup()
        while parent:
            if parent not in obj.InListRecursive and parent not in containers:
                containers.append(parent)
            parent = parent.getParentGeoFeatureGroup()
    if obj.PlacementSupport != containers:
        obj.PlacementSupport = containers
