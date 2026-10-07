# SPDX-License-Identifier: LGPL-2.1-or-later
"""Legacy inventory, structural migration and explicit evaluated recovery."""
import hashlib
from pathlib import Path

import FreeCAD as App


def _key(obj):
    return obj.Document.Name + ":" + obj.Name


def _references(value):
    if hasattr(value, "Document") and hasattr(value, "Name"):
        return [value]
    if isinstance(value, (tuple, list)):
        return [obj for item in value for obj in _references(item)]
    return []


def _frame(placement):
    return list(placement.toMatrix().A)


def _own_identity(obj):
    # App::Link forwards target properties. A definition UUID must never be
    # mistaken for an occurrence's own UUID.
    try:
        return obj.getPropertyByName("ObjectId", 1) is not None
    except AttributeError:
        return False


class BodyOutputProxy:
    """Native Body Tip bridge; the editable producer lives in component History."""

    def execute(self, obj):
        import Part
        obj.Shape = Part.Shape()
        producer = obj.Producer
        if producer is not None and "Invalid" not in producer.State:
            obj.Placement = producer.Shape.Placement
            obj.Shape = producer.Shape.copy()

    def dumps(self):
        return None

    def loads(self, state):
        pass


def is_datum(obj):
    return (obj.isDerivedFrom("Part::Datum") or obj.isDerivedFrom("App::DatumElement")
            or obj.isDerivedFrom("App::LocalCoordinateSystem"))


def migrate_datum_frames(document, report):
    """Retain native attachment engines and expose Body-owned datums in History.

    Native Origins and their planes/axes are never replaced or reparented. A datum
    link changes access, not source ownership, geometry or attachment definitions.
    """
    import ComponentModel as Model
    meta = Model.metadata(document)
    if getattr(meta, "LegacyFrameVersion", 0) >= 1:
        return
    origins = set()
    for obj in list(document.Objects):
        if obj.TypeId == "App::Origin":
            origins.add(obj)
            origins.update(obj.OriginFeatures)
    for obj in origins:
        if not _own_identity(obj):
            Model._identity(obj, "Internal")
    for source in list(document.Objects):
        if source in origins or not is_datum(source):
            continue
        parent = Model.owner(source)
        component = parent
        while component is not None and not Model.is_component(component):
            component = Model.owner(component)
        if component is None:
            report.append(source.Label + ": native datum retained outside a mapped component; repair ownership before using it.")
            continue
        if not _own_identity(source):
            Model._identity(source, "Internal")
        Model._property(source, "String", "LegacyDatumState", "Retained native attachment", True)
        if parent == component:
            source.ComponentRole = "Object"
            component.ResultObjects = [n for n in component.ResultObjects if n != source.Name]
            report.append(source.Label + ": native datum and attachment references retained in component History.")
            continue
        if parent.TypeId != "PartDesign::Body" or Model.owner(parent) != component:
            report.append(source.Label + ": nested native frame retained; direct History mapping requires repair.")
            continue
        alias = document.addObject("App::Link", "LegacyDatum")
        Model.register_object(component, alias, "Object")
        Model._property(alias, "LinkGlobal", "LegacyDatumSource", source, True)
        Model._property(alias, "String", "LegacyDatumState", "Linked native attachment", True)
        alias.setLink(source)
        # Native attachment engines read a Link's own frame, not its target's
        # placement. Store the complete datum frame and strip target placement.
        alias.LinkTransform = False
        alias.LinkPlacement = parent.Placement.multiply(source.Placement)
        alias.setExpression("LinkPlacement", parent.Name + ".Placement * " + source.Name + ".Placement")
        alias.Label = source.Label
        alias.Visibility = False  # Construction inputs must not compound infinite datum faces into solids.
        # Present datum access before its retained Body result, without claiming
        # the other native Body features have been flattened.
        ordered = [n for n in component.ModelHistory if n != alias.Name]
        index = ordered.index(parent.Name) if parent.Name in ordered else len(ordered)
        ordered.insert(index, alias.Name)
        component.ModelHistory = ordered
        report.append(source.Label + ": native Body ownership/supports retained; component History links the original datum with its Body frame.")
    Model._property(meta, "Integer", "LegacyFrameVersion", 1, True)


def migrate_sketch_inputs(document, report):
    """Expose native inputs without copying constraints or breaking Body consumers.

    Feature adapters own later physical reparenting. A hidden access link keeps
    the original native sketch (including local attachment/external references)
    as the single editable source for every consumer and shared instance.
    """
    import ComponentModel as Model
    meta = Model.metadata(document)
    if getattr(meta, "LegacySketchVersion", 0) >= 1:
        return
    sketches = [o for o in document.Objects if o.isDerivedFrom("Sketcher::SketchObject")
                and not o.isDerivedFrom("App::Link")]
    pending = {o: set(Model.geometry_dependencies(o, include_frames=True)) & set(sketches)
               for o in sketches}
    ordered = []
    while pending:
        ready = [o for o in sketches if o in pending and not pending[o]]
        if not ready:
            report.append("Cyclic native sketch dependencies retained; repair them before feature promotion.")
            ordered.extend(o for o in sketches if o in pending)
            break
        ordered.extend(ready)
        for source in ready:
            del pending[source]
        for dependencies in pending.values():
            dependencies.difference_update(ready)
    for source in ordered:
        parent = Model.owner(source)
        component = parent
        while component is not None and not Model.is_component(component):
            component = Model.owner(component)
        if not _own_identity(source):
            Model._identity(source, "Internal")
        Model._property(source, "String", "LegacySketchState", "Retained native sketch", True)
        if component is None:
            report.append(source.Label + ": native sketch retained outside a mapped component; repair ownership before using it.")
            continue
        if parent == component:
            source.ComponentRole = "Object"
            report.append(source.Label + ": component sketch retains native constraints, expressions, supports and external geometry.")
            continue
        if parent.TypeId != "PartDesign::Body" or Model.owner(parent) != component:
            report.append(source.Label + ": nested native sketch retained; direct History mapping requires repair.")
            continue
        alias = document.addObject("App::Link", "LegacySketch")
        Model.register_object(component, alias, "Object")
        Model._property(alias, "LinkGlobal", "LegacySketchSource", source, True)
        Model._property(alias, "String", "LegacySketchState", "Linked native sketch", True)
        alias.setLink(source)
        alias.LinkTransform = False
        alias.LinkPlacement = parent.Placement.multiply(source.Placement)
        alias.setExpression("LinkPlacement", parent.Name + ".Placement * " + source.Name + ".Placement")
        alias.Label = source.Label
        alias.Visibility = False
        ordered = [n for n in component.ModelHistory if n != alias.Name]
        index = ordered.index(parent.Name) if parent.Name in ordered else len(ordered)
        ordered.insert(index, alias.Name)
        component.ModelHistory = ordered
        report.append(source.Label + ": History links the original native sketch before its Body; attachment, constraints, formulas and shared consumers retained. Feature adapters own later reparenting.")
    Model._property(meta, "Integer", "LegacySketchVersion", 1, True)


def upgrade_datum_frames(document):
    """Upgrade native datum/sketch access after existing manifest validation."""
    import ComponentModel as Model
    meta = Model.metadata(document)
    legacy_report = any(entry.startswith(("Models and linked Part Tree instances converted",
                                         "Structural adapter could not complete:"))
                        for entry in meta.ConversionReport)
    if (not meta.LegacySource and not legacy_report) or (
            getattr(meta, "LegacyFrameVersion", 0) >= 1
            and getattr(meta, "LegacySketchVersion", 0) >= 1
            and getattr(meta, "LegacyExtrudeVersion", 0) >= 1
            and getattr(meta, "LegacyRevolveVersion", 0) >= 1
            and getattr(meta, "LegacyLoftVersion", 0) >= 1
            and getattr(meta, "LegacyPipeVersion", 0) >= 1
            and getattr(meta, "LegacyHelixVersion", 0) >= 1
            and getattr(meta, "LegacyPrimitiveVersion", 0) >= 1):
        return document
    with Model.transaction(document, "Expose retained legacy inputs"):
        report = list(meta.ConversionReport)
        migrate_extrusions(document, report)
        migrate_revolutions(document, report)
        migrate_lofts(document, report)
        migrate_pipes(document, report)
        migrate_helixes(document, report)
        migrate_primitives(document, report)
        migrate_datum_frames(document, report)
        migrate_sketch_inputs(document, report)
        meta.ConversionReport = report
        Model.validate(document, allow_unresolved=True)
    return document


def body_history_plan(body, component, source_ready):
    """Admit only the proven independent Sketch -> first Pad pilot."""
    import ComponentModel as Model
    if not body.Placement.isSame(App.Placement(), 1e-9):
        return None, "Body frame mapping awaits the attachment/frame adapter"
    pad = body.Tip
    if pad is None or pad.TypeId != "PartDesign::Pad":
        return None, "native Tip feature family awaits its adapter"
    sketch = pad.Profile[0]
    if sketch is None or not sketch.isDerivedFrom("Sketcher::SketchObject"):
        return None, "Pad profile is not an independent sketch"
    if set(body.Group) not in ({sketch, pad}, {pad}) or pad.BaseFeature is not None:
        return None, "multi-feature native Body history awaits its adapters"
    if Model.owner(sketch) not in (body, component):
        return None, "profile belongs to another native owner"
    if (str(sketch.MapMode) != "Deactivated" or sketch.AttachmentSupport or pad.Profile[1]):
        return None, "attached/subelement sketch inputs retain native ownership until their feature adapter"
    if any(dep == body or Model.owner(dep) == body
           for dep in Model.geometry_dependencies(sketch, include_frames=True)):
        return None, "sketch depends on its native Body frame/history; retain native ownership"
    if (str(pad.Type) != "Length" or str(pad.SideType) != "One side"
            or pad.UseCustomVector or float(pad.TaperAngle) != 0
            or str(pad.StartType) != "Profile plane"):
        return None, "Pad extent semantics await the full extrusion adapter"
    if body.ExpressionEngine or any(not prop.startswith(("Constraints[", "Constraints."))
                                    for prop, _ in sketch.ExpressionEngine):
        return None, "frame/sketch property expressions retain native ownership until their feature adapter"
    if not source_ready or any("Invalid" in obj.State for obj in (body, pad, sketch)):
        return None, "native history needs recompute or repair; cached output is unverified"
    if body.Shape.isNull() or not body.Shape.isValid() or len(body.Shape.Solids) != 1:
        return None, "native output needs repair; no solid output is fabricated"
    return (sketch, pad), ""


def migrate_body_histories(document, report, readiness):
    """Flatten proven histories, retaining other native histories and final outputs.

    Called inside the structural transaction; no new document or feature identities
    replace legacy objects. Body's native child-scoped Tip uses an internal bridge.
    """
    import ComponentModel as Model
    for component in Model.definitions(document):
        bodies = [obj for obj in Model.history(component) if obj.TypeId == "PartDesign::Body"]
        for body in bodies:
            plan, reason = body_history_plan(body, component, readiness.get(body, False))
            if plan is None:
                Model._property(body, "String", "LegacyHistoryState", "Retained native: " + reason, True)
                report.append(body.Label + ": editable native Body history and available final output retained; " + reason + ".")
                continue
            sketch, pad = plan
            before = body.Shape.copy()
            names = list(component.ModelHistory)
            original_group = [obj.Name for obj in body.Group]
            for obj, role in ((sketch, "Object"), (pad, "Operation")):
                label = obj.Label
                if Model.owner(obj) == body:
                    body.removeObject(obj)
                Model.register_object(component, obj, role)
                obj.Label = label
            Model._property(pad, "String", "OperationKind", "Extrude", True)
            Model._property(pad, "String", "ExtrudeMode", "New Body", True)
            Model._property(pad, "String", "LegacyMigration", "Sketch-Pad pilot", True)
            bridge = body.newObject("PartDesign::FeaturePython", "LegacyBodyOutput")
            Model._identity(bridge, "Internal")
            Model._property(bridge, "LinkGlobal", "Producer", pad, True)
            bridge.Proxy = BodyOutputProxy()
            bridge.Label = body.Label + " native output bridge"
            body.Tip = bridge
            # Explicit migration of the existing semantic role, never replacement
            # of the native Body name/type/ObjectId or its downstream references.
            body.ComponentRole = "Result"
            Model._property(body, "Link", "Producer", pad, True)
            Model._property(body, "Bool", "Frozen", False, True)
            Model._property(body, "String", "GeometryKind", "Body", True)
            Model._property(body, "String", "OutputProperty", "Shape", True)
            Model._property(body, "Bool", "BackgroundResult", False, True)
            Model._property(body, "StringList", "LegacyBodyHistory", original_group, True)
            Model._property(body, "Link", "LegacyTip", pad, True)
            Model._property(body, "String", "LegacyHistoryState", "Mapped Sketch-Pad pilot", True)
            ordered = []
            for name in names:
                if name in (sketch.Name, pad.Name):
                    continue
                ordered.extend([sketch.Name, pad.Name, body.Name] if name == body.Name else [name])
            component.ModelHistory = ordered
            component.ResultObjects = [name for name in component.ResultObjects
                                       if name not in (sketch.Name, pad.Name)]
            if App.GuiUp:
                bridge.Visibility = sketch.Visibility = pad.Visibility = False
                bridge.ViewObject.ShowInTree = False
            document.recompute()
            if "Invalid" in body.State or body.Shape.isNull() or not body.Shape.isValid():
                raise ValueError("Migrated native Body output failed; retain payloads through evaluated recovery.")
            if (abs(before.Volume - body.Shape.Volume) > 1e-8
                    or before.cut(body.Shape).Volume > 1e-8
                    or body.Shape.cut(before).Volume > 1e-8):
                raise ValueError("Migrated Body geometry changed; retain native payloads through evaluated recovery.")
            report.append(body.Label + ": Sketch and Pad precede the original Body result in component History; editable native identities retained.")


def native_sections(feature):
    """Keep native section order and subelement spelling, without UI translation."""
    return ([feature.Profile] if hasattr(feature, "Profile") else []) + (list(feature.Sections) if feature.TypeId in LOFTED + PIPED else [])


def native_inputs(feature):
    links = native_sections(feature)
    if feature.TypeId in PIPED:
        links += [ref for ref in (feature.Spine, feature.AuxiliarySpine) if ref and ref[0]]
    return links


def extrusion_chain_plan(body, component, revolved=False, lofted=False, piped=False, helixed=False, primitive=False):
    """Qualify reparenting without rewriting native extent or attachment semantics."""
    import ComponentModel as Model
    if not body.Placement.isSame(App.Placement(), 1e-9) or body.ExpressionEngine:
        return None, "native Body frame/expressions retained"
    piped = piped or helixed or primitive
    families = (("PartDesign::Pad", "PartDesign::Pocket")
                + (REVOLVED if revolved or lofted or piped else ())
                + (LOFTED if lofted or piped else ()) + (PIPED if piped else ())
                + (HELIXED if helixed or primitive else ()) + (PRIMITIVES if primitive else ()))
    features = [o for o in body.Group if o.TypeId in families]
    if not features or body.Tip != features[-1]:
        return None, "mixed or inactive native feature history retained"
    sketches = {obj for feature in features for obj, subs in native_inputs(feature)}
    if any(o is None or not o.isDerivedFrom("Sketcher::SketchObject") for o in sketches):
        return None, "non-sketch profile retained"
    if set(body.Group) != set(features) | {o for o in sketches if Model.owner(o) == body}:
        return None, "native construction/mixed feature history retained"
    for sketch in sketches:
        if (Model.owner(sketch) not in (body, component)
                or str(sketch.MapMode) != "Deactivated" or sketch.AttachmentSupport
                or any(dep == body or Model.owner(dep) == body
                       for dep in Model.geometry_dependencies(sketch, include_frames=True))
                or any(not p.startswith(("Constraints[", "Constraints.")) for p, _ in sketch.ExpressionEngine)):
            return None, "native attached/Body-dependent sketch retained"
    previous = None
    for feature in features:
        expected = "Subtraction" if feature.TypeId in ("PartDesign::Pocket", "PartDesign::Groove") else "Union"
        if feature.TypeId in HELIXED + PRIMITIVES:
            expected = str(feature.Operation)
            if expected not in ("Union", "Subtraction"):
                return None, "native Helix/Primitive Boolean semantics retained"
            if feature.TypeId in HELIXED:
                import ComponentHelix as Helix
                axis = feature.ReferenceAxis
                if (not axis or axis[0] != feature.Profile[0] or len(axis[1]) != 1
                        or not (axis[1][0] in ("V_Axis", "H_Axis", "N_Axis", "Axis")
                                or axis[1][0].startswith("Axis")) or feature.Profile[1]
                        or not feature.HasBeenEdited or feature.Outside):
                    return None, "native Helix axis/profile/initialization semantics retained"
                options = Helix.defaults()
                options.update(input_mode=str(feature.Mode), pitch=feature.Pitch.Value,
                               height=feature.Height.Value, turns=feature.Turns,
                               angle=feature.Angle.Value, growth=feature.Growth.Value,
                               tolerance=feature.Tolerance, fuzzy=feature.FuzzyTolerance)
                try:
                    Helix.normalized(options)
                except ValueError:
                    return None, "native Helix parameter law retained"
            elif (str(feature.MapMode) != "Deactivated" or feature.AttachmentSupport
                  or any(p.startswith(("Placement", "Attachment", "Map")) for p, _ in feature.ExpressionEngine)):
                return None, "native Primitive attachment/frame retained"
        if feature.TypeId in PIPED:
            import Part
            import ComponentPipe as Pipe
            expected = str(feature.Operation)
            sections = native_sections(feature)
            paths = [ref for ref in (feature.Spine, feature.AuxiliarySpine) if ref and ref[0]]
            if (expected not in ("Union", "Subtraction")
                    or str(feature.Mode) not in Pipe.ORIENTATIONS
                    or str(feature.Transition) not in Pipe.TRANSITIONS
                    or str(feature.Transformation) not in Pipe.TRANSFORMATIONS
                    or (str(feature.Transformation) == "Multisection" and len(sections) < 2)
                    or (str(feature.Transformation) == "Constant" and feature.Sections)
                    or not feature.Spine or not feature.Spine[0]
                    or (str(feature.Mode) == "Auxiliary" and len(paths) < 2)
                    or not -1 <= feature.FuzzyTolerance <= 1):
                return None, "native Pipe orientation/section/path/Boolean semantics retained"
            keys = [(obj.Name, tuple(subs)) for obj, subs in sections]
            if len(set(keys)) != len(keys):
                return None, "native repeated Pipe section retained"
            for obj, subs in sections:
                if (any(subs) or obj.Shape.isNull() or not obj.Shape.Wires
                        or any(not wire.isClosed() for wire in obj.Shape.Wires)):
                    return None, "native Pipe point/whole-sketch subelement semantics retained"
            for obj, subs in paths:
                try:
                    edges = [obj.Shape.getElement(sub) for sub in subs if sub] if any(subs) else obj.Shape.Edges
                    if (not edges or obj.Shape.Faces or obj.Shape.Solids
                            or any(not sub.startswith("Edge") for sub in subs if sub)
                            or len(Part.sortEdges(edges)) != 1 or not Part.Wire(edges).isValid()):
                        return None, "native Pipe path semantics retained"
                except Exception:
                    return None, "native Pipe path needs repair"
        if feature.TypeId in LOFTED:
            expected = str(feature.Operation)
            sections = native_sections(feature)
            keys = [(obj.Name, tuple(subs)) for obj, subs in sections]
            if (expected not in ("Union", "Subtraction") or len(sections) < 2
                    or (feature.Closed and len(sections) < 3) or len(set(keys)) != len(keys)
                    or not -1 <= feature.FuzzyTolerance <= 1):
                return None, "native Loft section/Boolean/tolerance semantics retained"
            for index, (obj, subs) in enumerate(sections):
                # Legacy Part2D edge references consume the ENTIRE sketch in
                # native Loft. Shared selected-curve inputs have another contract.
                if any(subs) and not (len(subs) == 1 and subs[0].startswith("Vertex")
                                      and index in (0, len(sections) - 1) and not feature.Closed):
                    return None, "native whole-sketch subelement semantics retained"
        if (feature.BaseFeature != previous or (previous is None and expected != "Union")
                or str(feature.Operation) != expected
                or (feature.TypeId not in LOFTED + PIPED + PRIMITIVES and feature.Profile[1])
                or any(p.startswith(("Placement", "Profile", "Sections", "BaseFeature", "Spine", "AuxiliarySpine")) for p, _ in feature.ExpressionEngine)):
            return None, "native target/profile/axis semantics retained"
        if feature.TypeId in REVOLVED:
            axis = feature.ReferenceAxis
            # Keep exact native sketch axes, including construction geometry.
            # Body Origin/datum/external axes retain their complete native frame.
            if (not axis or axis[0] != feature.Profile[0] or len(axis[1]) != 1
                    or not (axis[1][0] in ("V_Axis", "H_Axis") or axis[1][0].startswith("Axis"))):
                return None, "native reference axis/frame retained"
            allowed = ("Angle", "ThroughAll") if expected == "Subtraction" else ("Angle",)
            if (str(feature.Type) not in allowed or str(feature.Type2) != "Angle"
                    or str(feature.StartType) not in ("Profile plane", "Offset")
                    or not -360 <= feature.StartOffset.Value <= 360
                    or (str(feature.Type) == "Angle" and not 0 < feature.Angle.Value <= 360)
                    or (str(feature.SideType) == "Two sides" and not 0 < feature.Angle2.Value <= 360)):
                return None, "native referenced/signed angular extent retained"
        elif feature.TypeId not in LOFTED + PIPED + HELIXED + PRIMITIVES and (feature.UseCustomVector or (feature.ReferenceAxis and feature.ReferenceAxis[0] is not None)):
            return None, "native target/profile/axis semantics retained"
        # Complex linked start/limit definitions stay on the native engine and
        # editor until their complete reference mapping is qualified.
        if feature.TypeId not in REVOLVED + LOFTED + PIPED + HELIXED + PRIMITIVES and (str(feature.Type) not in ("Length", "ThroughAll", "UpToFirst", "UpToLast")
                or str(feature.Type2) != "Length" or str(feature.StartType) not in ("Profile plane", "Offset")
                or (previous is None and str(feature.Type) != "Length")):
            return None, "native referenced extent retained"
        if feature.TypeId not in REVOLVED + LOFTED + PIPED + HELIXED + PRIMITIVES and ((str(feature.Type) == "Length" and feature.Length.Value <= 0)
                or (str(feature.SideType) == "Two sides" and feature.Length2.Value <= 0)):
            return None, "signed native extent retained"
        if (any("Invalid" in o.State for o in [feature] + [obj for obj, subs in native_inputs(feature)])
                or feature.Shape.isNull() or not feature.Shape.isValid() or len(feature.Shape.Solids) != 1):
            return None, "native output needs repair"
        if (feature.TypeId in LOFTED + PIPED + HELIXED + PRIMITIVES and previous is not None
                and abs(feature.Shape.Volume - previous.Shape.Volume) < 1e-9):
            return None, "native no-material section history retained"
        previous = feature
    return features, ""


REVOLVED = ("PartDesign::Revolution", "PartDesign::Groove")
LOFTED = ("PartDesign::AdditiveLoft", "PartDesign::SubtractiveLoft")
PIPED = ("PartDesign::AdditivePipe", "PartDesign::SubtractivePipe")
HELIXED = ("PartDesign::AdditiveHelix", "PartDesign::SubtractiveHelix")
PRIMITIVE_KINDS = ("Box", "Cylinder", "Sphere", "Cone", "Ellipsoid", "Torus", "Prism", "Wedge")
PRIMITIVES = tuple("PartDesign::" + prefix + kind for prefix in ("Additive", "Subtractive") for kind in PRIMITIVE_KINDS)
PART_PRIMITIVES = tuple("Part::" + kind for kind in PRIMITIVE_KINDS)


def map_native_chain(document, component, body, features, report, state):
    """Publish native targets once, preserving original inputs/features/final Body."""
    import json
    import ComponentModel as Model
    originals = list(body.Group)
    labels = {o: o.Label for o in originals}
    shapes = {o: o.Shape.copy() for o in features}
    final_shape = body.Shape.copy()
    profiles = {o: o.Profile for o in features if hasattr(o, "Profile")}
    axes = {o: o.ReferenceAxis for o in features if o.TypeId in HELIXED}
    sections = {o: list(o.Sections) for o in features if o.TypeId in LOFTED + PIPED}
    paths = {o: (o.Spine, o.AuxiliarySpine) for o in features if o.TypeId in PIPED}
    names = list(component.ModelHistory)
    for alias in list(Model.history(component)):
        source = getattr(alias, "LegacySketchSource", getattr(alias, "LegacyExtrudeSource",
                         getattr(alias, "LegacyRevolveSource", getattr(alias, "LegacyLoftSource", getattr(alias, "LegacyPipeSource", getattr(alias, "LegacyHelixSource", getattr(alias, "LegacyPrimitiveSource", None)))))))
        if source in originals:
            # Preserve earlier-file alias identities/references while
            # History now presents the original independent sketch.
            alias.ComponentRole = "Internal"
            alias.setExpression("LinkPlacement", source.Name + ".Placement")
            names = [n for n in names if n != alias.Name]
    for obj in originals:
        body.removeObject(obj)
        component.Group = list(component.Group) + [obj]
        role = "Operation" if obj in features else "Object"
        if _own_identity(obj):
            obj.ComponentRole = role
        Model.register_object(component, obj, role)
        obj.Label = labels[obj]
    chain, previous = [], None
    for feature in features:
        if feature in profiles:
            feature.Profile = profiles[feature]
        if feature in axes:
            feature.ReferenceAxis = axes[feature]
        if feature in sections:
            feature.Sections = sections[feature]
        if feature in paths:
            feature.Spine, feature.AuxiliarySpine = paths[feature]
        feature.BaseFeature = previous
        kind = "Primitive" if feature.TypeId in PRIMITIVES else "Helix" if feature.TypeId in HELIXED else "Pipe" if feature.TypeId in PIPED else "Loft" if feature.TypeId in LOFTED else "Revolve" if feature.TypeId in REVOLVED else "Extrude"
        mode = "Subtract" if feature.TypeId in ("PartDesign::Pocket", "PartDesign::Groove") else "Add" if previous else "New Body"
        if kind in ("Loft", "Pipe", "Helix", "Primitive") and str(feature.Operation) == "Subtraction":
            mode = "Subtract"
        Model._property(feature, "String", "OperationKind", kind, True)
        Model._property(feature, "String", kind + "Mode", mode, True)
        migration = {"Primitive": "Native primitive chain", "Helix": "Native helix chain", "Pipe": "Native pipe chain", "Loft": "Native loft chain", "Revolve": "Native revolve chain", "Extrude": "Native extrusion chain"}[kind]
        Model._property(feature, "String", "LegacyMigration", migration, True)
        Model._property(feature, "LinkList", "ConsumedResults", [previous] if previous else [], True)
        Model._property(feature, "String", "PreviousVisibility",
                        json.dumps({previous.ObjectId: False}) if previous else "{}", True)
        document.recompute()
        before, after = shapes[feature], feature.Shape
        if ("Invalid" in feature.State or after.isNull() or not after.isValid()
                or abs(before.Volume - after.Volume) > 1e-8
                or before.cut(after).Volume > 1e-8 or after.cut(before).Volume > 1e-8):
            raise ValueError("Native feature chain geometry changed; preserve payload through evaluated recovery.")
        for profile, subs in native_inputs(feature):
            if profile.Name not in chain:
                chain.append(profile.Name)
        chain.append(feature.Name)
        if feature != features[-1]:
            previous = Model.publish_result(component, feature)
            document.recompute()
            previous.Visibility = False
            chain.append(previous.Name)
    bridge = body.newObject("PartDesign::FeaturePython", "LegacyBodyOutput")
    Model._identity(bridge, "Internal")
    Model._property(bridge, "LinkGlobal", "Producer", features[-1], True)
    bridge.Proxy = BodyOutputProxy()
    body.Tip = bridge
    body.ComponentRole = "Result"
    Model._property(body, "Link", "Producer", features[-1], True)
    for kind, prop, value in (("Bool", "Frozen", False), ("String", "GeometryKind", "Body"),
                              ("String", "OutputProperty", "Shape"), ("Bool", "BackgroundResult", False),
                              ("StringList", "LegacyBodyHistory", [o.Name for o in originals]),
                              ("Link", "LegacyTip", features[-1]),
                              ("String", "LegacyHistoryState", state)):
        if prop in body.PropertiesList:
            setattr(body, prop, value)
        else:
            Model._property(body, kind, prop, value, True)
    chain.append(body.Name)
    related = set(chain) | {o.Name for o in originals}
    ordered = []
    for name in names:
        if name == body.Name:
            ordered.extend(chain)
        elif name not in related:
            ordered.append(name)
    component.ModelHistory = ordered
    component.ResultObjects = [n for n in component.ResultObjects if n not in {o.Name for o in originals}]
    for obj in originals + [bridge]:
        obj.Visibility = False
    bridge.ViewObject.ShowInTree = False
    document.recompute()
    if (body.Shape.isNull() or not body.Shape.isValid()
            or abs(final_shape.Volume - body.Shape.Volume) > 1e-8
            or final_shape.cut(body.Shape).Volume > 1e-8 or body.Shape.cut(final_shape).Volume > 1e-8):
        raise ValueError("Converted native Body result changed; preserve evaluated recovery.")
    report[:] = [entry for entry in report if not (entry.startswith(body.Label + ":")
                 and ("feature adapters pending" in entry or "editable native Body history" in entry))]
    report.append(body.Label + ": native feature chain mapped to component operations with explicit consumed results; original feature and final Body identities retained.")


def retain_native_operation(document, component, body, source, family, description):
    """Expose one original native editor through a hidden complete-frame link."""
    import ComponentModel as Model
    if not _own_identity(source):
        Model._identity(source, "Internal")
    alias = document.addObject("App::Link", "Legacy" + family)
    Model.register_object(component, alias, "Operation")
    Model._property(alias, "LinkGlobal", "Legacy" + family + "Source", source, True)
    Model._property(alias, "LinkGlobal", "Legacy" + family + "Target", source.BaseFeature, True)
    Model._property(alias, "String", "Legacy" + family + "State", "Retained native " + description, True)
    alias.setLink(source)
    alias.LinkTransform = False
    alias.setExpression("LinkPlacement", body.Name + ".Placement * " + source.Name + ".Placement")
    alias.Label = source.Label
    alias.Visibility = False
    ordered = [n for n in component.ModelHistory if n != alias.Name]
    ordered.insert(ordered.index(body.Name), alias.Name)
    component.ModelHistory = ordered
    return alias


def migrate_extrusions(document, report, readiness=None):
    """Map qualified native chains; expose other extents through native editors."""
    import json
    import ComponentModel as Model
    meta = Model.metadata(document)
    if getattr(meta, "LegacyExtrudeVersion", 0) >= 1:
        return
    for component in Model.definitions(document):
        bodies = [o for o in Model.history(component) if o.TypeId == "PartDesign::Body"
                  and not getattr(o, "Producer", None)]
        for body in bodies:
            features, reason = extrusion_chain_plan(body, component)
            if readiness is not None and not readiness.get(body, False):
                features, reason = None, "source cache is unverified; native output retained for repair/recompute"
            if features is not None:
                map_native_chain(document, component, body, features, report, "Mapped native extrusion chain")
                continue
            for source in body.Group:
                if source.TypeId not in ("PartDesign::Pad", "PartDesign::Pocket"):
                    continue
                retain_native_operation(document, component, body, source, "Extrude", "extrusion")
                report.append(source.Label + ": native parameters, target and available output retained; History opens its native editor; " + reason + ".")
        for source in list(Model.history(component)):
            if source.TypeId != "Part::Extrusion" or getattr(source, "OperationKind", ""):
                continue
            if ((readiness is None or readiness.get(source, False))
                    and str(source.DirMode) == "Normal" and source.Solid and source.LengthFwd.Value > 0
                    and source.LengthRev.Value == 0 and source.TaperAngle.Value == 0
                    and source.TaperAngleRev.Value == 0 and Model.owner(source.Base) == component
                    and not source.Shape.isNull() and source.Shape.isValid() and len(source.Shape.Solids) == 1
                    and "Invalid" not in source.State):
                Model._property(source, "String", "OperationKind", "Extrude", True)
                Model._property(source, "String", "ExtrudeMode", "New Body", True)
                Model._property(source, "String", "LegacyMigration", "Native extrusion chain", True)
                result = Model.publish_result(component, source)
                component.ResultObjects = [n for n in component.ResultObjects if n != source.Name]
                report.append(source.Label + ": independent native Part Extrusion mapped with its original profile/direction and an editable published result.")
            else:
                Model._property(source, "String", "LegacyExtrudeState", "Retained native standalone extrusion", True)
                report.append(source.Label + ": native Part Extrusion parameters and available curve/sheet/solid output retained; edit its native properties without normalizing direction/taper semantics.")
    Model._property(meta, "Integer", "LegacyExtrudeVersion", 1, True)


def migrate_revolutions(document, report, readiness=None):
    """Preserve native axes/angles and qualify explicit target/result histories."""
    import ComponentModel as Model
    meta = Model.metadata(document)
    if getattr(meta, "LegacyRevolveVersion", 0) >= 1:
        return
    for component in Model.definitions(document):
        bodies = [o for o in Model.history(component) if o.TypeId == "PartDesign::Body"
                  and not getattr(o, "Producer", None)]
        for body in bodies:
            sources = [o for o in body.Group if o.TypeId in REVOLVED]
            if not sources:
                continue
            features, reason = extrusion_chain_plan(body, component, revolved=True)
            if readiness is not None and not readiness.get(body, False):
                features, reason = None, "source cache is unverified; native output retained for repair/recompute"
            if features is not None:
                map_native_chain(document, component, body, features, report, "Mapped native revolve chain")
                continue
            for source in sources:
                retain_native_operation(document, component, body, source, "Revolve", "revolution")
                report.append(source.Label + ": native axis, angular parameters, target and output retained; History opens its native editor; " + reason + ".")
        for source in list(Model.history(component)):
            if source.TypeId != "Part::Revolution" or getattr(source, "LegacyRevolveState", ""):
                continue
            # Part Revolution has a vector/linked axis and signed angle contract;
            # its original native editor remains authoritative. Never normalize
            # those values to the PartDesign shared task or replace its identity.
            Model._property(source, "String", "LegacyRevolveState", "Retained native standalone revolution", True)
            if ((readiness is None or readiness.get(source, False))
                    and "Invalid" not in source.State and not source.Shape.isNull()
                    and source.Shape.isValid() and len(source.Shape.Solids) == 1):
                Model.publish_result(component, source)
                component.ResultObjects = [n for n in component.ResultObjects if n != source.Name]
                report.append(source.Label + ": native Part Revolution axis/source/signed angle retained with an editable published result.")
            else:
                report.append(source.Label + ": native Part Revolution and available sheet/curve/solid output retained; invalid or unverified output requires repair/recompute.")
    Model._property(meta, "Integer", "LegacyRevolveVersion", 1, True)


def migrate_lofts(document, report, readiness=None):
    """Map ordered native sections/targets without changing original features."""
    import ComponentModel as Model
    meta = Model.metadata(document)
    if getattr(meta, "LegacyLoftVersion", 0) >= 1:
        return
    for component in Model.definitions(document):
        bodies = [o for o in Model.history(component) if o.TypeId == "PartDesign::Body"
                  and not getattr(o, "Producer", None)]
        for body in bodies:
            sources = [o for o in body.Group if o.TypeId in LOFTED]
            if not sources:
                continue
            features, reason = extrusion_chain_plan(body, component, lofted=True)
            if readiness is not None and not readiness.get(body, False):
                features, reason = None, "source cache is unverified; native output retained for repair/recompute"
            if features is not None:
                map_native_chain(document, component, body, features, report, "Mapped native loft chain")
                continue
            for source in sources:
                retain_native_operation(document, component, body, source, "Loft", "loft")
                report.append(source.Label + ": native section order/references, Boolean target and output retained; History opens its native editor; " + reason + ".")
        for source in list(Model.history(component)):
            if source.TypeId != "Part::Loft" or getattr(source, "LegacyLoftState", ""):
                continue
            # Part Loft includes MaxDegree/Linearize/Solid, unlike the shared
            # PartDesign task. Preserve its native engine/settings/editor.
            Model._property(source, "String", "LegacyLoftState", "Retained native standalone loft", True)
            if ((readiness is None or readiness.get(source, False))
                    and "Invalid" not in source.State and not source.Shape.isNull()
                    and source.Shape.isValid() and len(source.Shape.Solids) == 1):
                Model.publish_result(component, source)
                component.ResultObjects = [n for n in component.ResultObjects if n != source.Name]
                report.append(source.Label + ": native Part Loft ordered sections, degree/linearization and other settings retained with a published result.")
            else:
                report.append(source.Label + ": native Part Loft and available sheet/curve/solid output retained; invalid or unverified output needs repair/recompute.")
    Model._property(meta, "Integer", "LegacyLoftVersion", 1, True)


def migrate_pipes(document, report, readiness=None):
    """Map ordered native sections/targets without changing original features."""
    import ComponentModel as Model
    meta = Model.metadata(document)
    if getattr(meta, "LegacyPipeVersion", 0) >= 1:
        return
    for component in Model.definitions(document):
        bodies = [o for o in Model.history(component) if o.TypeId == "PartDesign::Body"
                  and not getattr(o, "Producer", None)]
        for body in bodies:
            sources = [o for o in body.Group if o.TypeId in PIPED]
            if not sources:
                continue
            features, reason = extrusion_chain_plan(body, component, piped=True)
            if readiness is not None and not readiness.get(body, False):
                features, reason = None, "source cache is unverified; native output retained for repair/recompute"
            if features is not None:
                map_native_chain(document, component, body, features, report, "Mapped native pipe chain")
                continue
            for source in sources:
                retain_native_operation(document, component, body, source, "Pipe", "pipe")
                report.append(source.Label + ": native profiles, paths, orientation and Boolean target and output retained; History opens its native editor; " + reason + ".")
        for source in list(Model.history(component)):
            if source.TypeId != "Part::Sweep" or getattr(source, "LegacyPipeState", ""):
                continue
            # Part Sweep has distinct Solid/Frenet/Linearize semantics; retain its engine/editor.
            Model._property(source, "String", "LegacyPipeState", "Retained native standalone pipe", True)
            if ((readiness is None or readiness.get(source, False))
                    and "Invalid" not in source.State and not source.Shape.isNull()
                    and source.Shape.isValid() and len(source.Shape.Solids) == 1):
                Model.publish_result(component, source)
                component.ResultObjects = [n for n in component.ResultObjects if n != source.Name]
                report.append(source.Label + ": native Part Pipe ordered sections, Frenet/linearization and other settings retained with a published result.")
            else:
                report.append(source.Label + ": native Part Pipe and available sheet/curve/solid output retained; invalid or unverified output needs repair/recompute.")
    Model._property(meta, "Integer", "LegacyPipeVersion", 1, True)


def migrate_helixes(document, report, readiness=None):
    migrate_native_family(document, report, "Helix", HELIXED, ("Part::Helix",), readiness)


def migrate_primitives(document, report, readiness=None):
    migrate_native_family(document, report, "Primitive", PRIMITIVES, PART_PRIMITIVES, readiness)


def migrate_native_family(document, report, family, types, standalone, readiness=None):
    """Bounded adapters share publishing/retention, not native parameter laws."""
    import ComponentModel as Model
    meta = Model.metadata(document)
    version = "Legacy" + family + "Version"
    if getattr(meta, version, 0) >= 1:
        return
    for component in Model.definitions(document):
        for body in [o for o in Model.history(component) if o.TypeId == "PartDesign::Body"
                     and not getattr(o, "Producer", None)]:
            sources = [o for o in body.Group if o.TypeId in types]
            if not sources:
                continue
            features, reason = extrusion_chain_plan(body, component, **{"helixed" if family == "Helix" else "primitive": True})
            if readiness is not None and not readiness.get(body, False):
                features, reason = None, "source cache is unverified; native output retained for repair/recompute"
            if features is not None:
                map_native_chain(document, component, body, features, report, "Mapped native " + family.lower() + " chain")
                continue
            for source in sources:
                retain_native_operation(document, component, body, source, family, family.lower())
                report.append(source.Label + ": original native parameters, references, target and available output retained; History opens its native editor; " + reason + ".")
        for source in list(Model.history(component)):
            state = "Legacy" + family + "State"
            if source.TypeId not in standalone or getattr(source, state, ""):
                continue
            Model._property(source, "String", state, "Retained native standalone " + family.lower(), True)
            if ((readiness is None or readiness.get(source, False))
                    and "Invalid" not in source.State and not source.Shape.isNull()
                    and source.Shape.isValid() and len(source.Shape.Solids) == 1):
                # Native Part compounds (including external Links to wrappers)
                # include both a producer and a separate Shape carrier. Keep
                # this original native output directly to avoid double geometry.
                if source.Name not in component.ResultObjects:
                    component.ResultObjects = list(component.ResultObjects) + [source.Name]
            report.append(source.Label + ": standalone native " + family + " settings/editor and available output retained; unverified or invalid geometry requires repair/recompute.")
    Model._property(meta, "Integer", version, 1, True)


def recovery_shapes(document):
    """Capture native top-level output before structural edits, for recovery."""
    import Part
    result, hidden = [], []
    for obj in document.Objects:
        if obj.TypeId == "App::Origin" or obj.getParentGeoFeatureGroup() is not None:
            continue
        if not (obj.TypeId == "App::Part" or obj.isDerivedFrom("Part::Feature")
                or obj.isDerivedFrom("App::Link")):
            continue
        try:
            shape = Part.getShape(obj, "", needSubElement=False).copy()
            if not shape.isNull() and shape.isValid():
                bucket = hidden if App.GuiUp and not obj.ViewObject.Visibility else result
                stale = any(flag in ("Touched", "Invalid")
                            for dep in [obj] + list(obj.OutListRecursive) for flag in dep.State)
                bucket.append((obj.Name, shape, stale))
        except (RuntimeError, ValueError):
            pass  # Conversion report below explicitly identifies unavailable output.
    return result or hidden


def recover_structure(document, shapes, error):
    """Retain native payloads and present validated frozen outputs on failure."""
    import ComponentModel as Model
    filename = document.FileName
    originals = list(document.Objects)
    with Model.transaction(document, "Recover legacy evaluated component outputs"):
        meta = Model.initialize(document, document.Label)
        meta.LegacySource = filename
        report = ["Structural adapter could not complete: " + str(error),
                  "Explicit dumb geometry recovery; native feature payloads retained. Parametric component migration is incomplete."]
        for name, shape, stale in shapes:
            obj = document.addObject("Part::Feature", "RecoveredLegacyOutput")
            obj.Label = name + " recovered geometry"
            obj.Shape = shape
            Model.register_object(meta.RootComponent, obj, "Object", True)
            Model._property(obj, "String", "LegacyRecovery", name + ": validated evaluated geometry; parametric history not converted.", True)
            if stale:
                obj.LegacyRecovery = name + ": unverified cached geometry; source requires repair; parametric history not converted."
                report.append(name + ": recovered cached geometry is unverified; original source dependencies require repair.")
        if not shapes:
            report.append("No valid top-level evaluated output was available; native payloads retained for repair.")
        for obj in originals:
            if App.GuiUp:
                obj.ViewObject.Visibility = False
        meta.ConversionReport = report
    document.FileName = ""
    return document


def inventory(document):
    """Snapshot an already-open legacy document without recompute or mutation.

    Keys use native document/object names; no UUIDs are assigned. External
    documents are identified, not opened, saved or converted. Geometry is the
    existing evaluated cache: availability is separate from trusted freshness.
    """
    if any(getattr(o, "ComponentRole", "") == "Document" for o in document.Objects):
        raise ValueError("Inventory the legacy document before component conversion.")
    objects = list(document.Objects)
    local = {_key(o): o for o in objects}
    issues, records, dependencies, native_dependencies = [], {}, {}, {}

    def issue(obj, stage, error):
        issues.append({"object": _key(obj), "stage": stage, "message": str(error)})

    for obj in objects:
        key = _key(obj)
        record = {"name": obj.Name, "label": obj.Label, "type": obj.TypeId,
                  "object_id": getattr(obj, "ObjectId", None), "state": list(obj.State),
                  "properties": {}, "links": {}, "geometry": None,
                  "fallback": {"kind": None, "status": "unavailable"}}
        records[key] = record
        for prop in obj.PropertiesList:
            try:
                kind = obj.getTypeIdOfProperty(prop)
                if prop not in ("Shape", "Proxy"):
                    data = bytes(obj.dumpPropertyContent(prop, 0))
                    record["properties"][prop] = {"type": kind,
                        "sha256": hashlib.sha256(data).hexdigest()}
                if "Link" in kind:
                    record["links"][prop] = [_key(o) for o in _references(getattr(obj, prop))]
            except Exception as error:
                issue(obj, "property:" + prop, error)
        try:
            parent = obj.getParentGeoFeatureGroup()
            record["owner"] = _key(parent) if parent else None
            record["group"] = [_key(o) for o in getattr(obj, "Group", [])]
            record["tip"] = _key(obj.Tip) if getattr(obj, "Tip", None) else None
            if hasattr(obj, "Placement"):
                record["placement"] = _frame(obj.Placement)
                record["world_placement"] = (_frame(obj.getGlobalPlacement())
                    if hasattr(obj, "getGlobalPlacement") else None)
            if hasattr(obj, "LinkPlacement"):
                record["link_placement"] = _frame(obj.LinkPlacement)
                record["link_transform"] = bool(obj.LinkTransform)
                record["link_scale"] = float(obj.Scale)
                record["link_scale_vector"] = list(obj.ScaleVector)
                record["element_count"] = int(obj.ElementCount)
            record["expressions"] = [list(x) for x in getattr(obj, "ExpressionEngine", [])]
            record["visibility"] = bool(obj.Visibility) if hasattr(obj, "Visibility") else None
        except Exception as error:
            issue(obj, "ownership/frame", error)
        try:
            # The synthetic .Shape accessor on Parts/Links can create caches,
            # and native feature access can lazily evaluate touched geometry.
            # Read only the stored property; never invoke that accessor.
            shape = obj.getPropertyByName("Shape") if "Shape" in obj.PropertiesList else None
            if shape is not None and not shape.isNull():
                brep = shape.exportBrepToString()
                valid = shape.isValid()
                record["geometry"] = {"brep_sha256": hashlib.sha256(brep.encode()).hexdigest(),
                    "valid": valid, "solids": len(shape.Solids), "faces": len(shape.Faces),
                    "edges": len(shape.Edges), "vertices": len(shape.Vertexes),
                    "volume": shape.Volume, "area": shape.Area,
                    "bounds": [shape.BoundBox.XMin, shape.BoundBox.YMin, shape.BoundBox.ZMin,
                               shape.BoundBox.XMax, shape.BoundBox.YMax, shape.BoundBox.ZMax]}
                kind = ("dumb_body" if shape.Solids else "dumb_sheet" if shape.Faces
                        else "dumb_curve" if shape.Edges else "dumb_point")
                stale = any(s in ("Touched", "Invalid") for s in obj.State)
                record["fallback"] = {"kind": kind, "status": "invalid" if not valid
                    else "cached_unverified" if stale else "available_cached",
                    "source": key, "preserves_parametrics": False}
        except Exception as error:
            issue(obj, "geometry", error)
        # Ownership links must not turn every Body/Part into a false cycle.
        inputs = {dep for prop, values in record["links"].items()
                  if prop not in ("Group", "Origin", "OriginFeatures", "_Body") for dep in values}
        # OutList includes expression dependencies, including cross-document ones.
        structural = set(record.get("group", []))
        for prop in ("Origin", "OriginFeatures", "_Body"):
            structural.update(record["links"].get(prop, []))
        try:
            native_dependencies[key] = list(obj.OutList)
            inputs.update(_key(o) for o in native_dependencies[key] if _key(o) not in structural)
        except Exception as error:
            native_dependencies[key] = []
            issue(obj, "dependencies", error)
        dependencies[key] = sorted(inputs)

    # Deterministic Kahn order; unresolved nodes are blocked, never silently sorted.
    remaining = {k: set(v) & local.keys() for k, v in dependencies.items()}
    order = []
    while remaining:
        ready = sorted(k for k, v in remaining.items() if not v)
        if not ready:
            break
        order.extend(ready)
        for key in ready:
            del remaining[key]
        for values in remaining.values():
            values.difference_update(ready)
    for key in remaining:
        issues.append({"object": key, "stage": "dependency_order",
                       "message": "Cyclic dependency or dependent on a cycle; conversion blocked."})

    parts = {k for k, o in local.items() if o.TypeId == "App::Part"}
    bodies = {k for k, o in local.items() if o.TypeId == "PartDesign::Body"}

    def enclosing_part(key):
        seen = set()
        while key in records and key not in seen:
            seen.add(key)
            key = records[key].get("owner")
            if key in parts:
                return key
        return None

    boundaries = parts | {k for k in bodies if enclosing_part(k) is None}
    links = {k for k, o in local.items() if o.isDerivedFrom("App::Link")}
    for key in links:
        targets = records[key]["links"].get("LinkedObject", [])
        for target in targets:
            if target in local and target not in links and not records[target].get("owner"):
                boundaries.add(target)
            elif target in local and target not in boundaries and target not in links:
                issues.append({"object": key, "stage": "definition_boundary",
                    "message": "Link targets an internal feature; retain native link until ownership is resolved."})
        if not targets:
            issues.append({"object": key, "stage": "definition_boundary",
                           "message": "Unresolved native link; no target geometry is certified."})

    master = document.Name + ":@master"

    def definition_for(key):
        seen = set()
        while key in records and key not in seen:
            seen.add(key)
            if key in boundaries:
                return key
            key = records[key].get("owner")
        return master

    definitions = [{"source": k, "parent": definition_for(records[k].get("owner")),
                    "policy": "preserve_native_definition_identity"} for k in sorted(boundaries)]
    occurrences = [{"source": k, "definition": k, "parent": d["parent"],
                    "policy": "proposed_instance_from_container_placement"}
                   for d in definitions for k in [d["source"]] if k not in links]
    occurrences.extend({"source": k, "targets": records[k]["links"].get("LinkedObject", []),
                        "parent": definition_for(records[k].get("owner")),
                        "policy": "preserve_native_link_and_placement"} for k in sorted(links))
    external = sorted({dep for deps in dependencies.values() for dep in deps if dep not in local})
    external_files = {}
    for key, deps in native_dependencies.items():
        for dep in deps:
            if _key(dep) in external:
                try:
                    external_files[_key(dep)] = dep.Document.FileName
                except Exception as error:
                    issue(local[key], "external_file", error)
    # Freshness of dependent geometry is not established by its own State alone.
    stale = {k for k, r in records.items() if any(s in ("Touched", "Invalid") for s in r["state"])}
    stale.update(_key(dep) for deps in native_dependencies.values() for dep in deps
                 if any(s in ("Touched", "Invalid") for s in dep.State))
    while True:
        downstream = {k for k, deps in dependencies.items() if stale.intersection(deps)}
        if downstream <= stale:
            break
        stale.update(downstream)
    for key in stale | set(remaining):
        if key in records and records[key]["fallback"]["status"] == "available_cached":
            records[key]["fallback"]["status"] = "cached_unverified"
    source = Path(document.FileName) if document.FileName else None
    source_hash = None
    try:
        if source and source.is_file():
            source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    except OSError as error:
        issues.append({"object": None, "stage": "source_file", "message": str(error)})
    return {"plan_version": 1, "read_only": True, "document": document.Name,
            "source_file": str(source) if source else None,
            "source_sha256": source_hash,
            "master": master, "objects": records, "dependencies": dependencies,
            "dependency_order": order, "blocked_objects": sorted(remaining),
            "definitions": definitions, "occurrences": occurrences,
            "history_owner": {k: definition_for(k) for k in records if k not in links},
            "external_objects": external, "external_files": external_files,
            "issues": issues,
            "recovery_policy": ["convert_with_feature_adapter", "retain_editable_native_feature",
                                "recover_valid_evaluated_dumb_geometry", "report_unavailable_output"],
            "fallback_requires": "Explicit loss-of-parametrics report; validate cached geometry and placements. Never replace failed features during inventory."}


def convert_structure(document, extra_targets=(), visiting=None):
    """Convert definition/occurrence ownership, retaining native feature payloads.

    Each file is one native transaction. External dependencies convert in memory
    first; saving them to new cadprt files remains an explicit owner action.
    """
    import ComponentModel as Model
    if any(getattr(o, "ComponentRole", "") == "Document" for o in document.Objects):
        return document
    visiting = set() if visiting is None else visiting
    if document.Name in visiting:
        raise ValueError("Cyclic legacy external files cannot be mapped to component instances.")
    visiting.add(document.Name)
    try:
        plan = inventory(document)
        originals = list(document.Objects)
        links = [o for o in originals if o.isDerivedFrom("App::Link")]
        # Keep a native target/frame snapshot before any source is reparented.
        snapshots = {}
        external = {}
        arrays = {}
        for link in links:
            target = link.LinkedObject
            if target is None:
                continue
            if link.ElementCount:
                import Part
                shape = Part.getShape(link, "", needSubElement=False).copy()
                if shape.isNull() or not shape.isValid() or "Invalid" in link.State:
                    raise ValueError("Legacy link array has no validated recoverable output.")
                arrays[link] = shape
                continue
            snapshots[link] = (target, App.Placement(link.LinkPlacement), bool(link.LinkTransform),
                               App.Placement(target.Placement) if hasattr(target, "Placement") else App.Placement())
            if target.Document != document:
                external.setdefault(target.Document, []).append(target)
        for source, targets in external.items():
            convert_structure(source, targets, visiting)

        parts = [o for o in originals if o.TypeId == "App::Part"]
        boundaries = {document.getObject(d["source"].split(":", 1)[1]) for d in plan["definitions"]}
        boundaries.update(extra_targets)
        boundaries.update(arrays)
        boundaries.update(target for target, _, _, _ in snapshots.values() if target.Document == document)
        boundaries.discard(None)
        # Definition frames are captured in the old ownership hierarchy.
        world = {o: App.Placement(o.getGlobalPlacement()) for o in parts}
        for part in parts:
            if any(prop.lstrip(".").startswith("Placement") for prop, _ in part.ExpressionEngine):
                raise ValueError("Expression-driven Part frames require explicit frame-expression mapping; native source is retained.")
            if not part.Placement.isSame(world[part], 1e-9):
                names = (part.Name + ".Placement", "<<" + part.Label + ">>.Placement")
                if any(any(name in expression for name in names)
                       for obj in originals for _, expression in getattr(obj, "ExpressionEngine", [])):
                    raise ValueError("An expression consumes the legacy local Part frame; preserve native formulas through explicit evaluated recovery.")
        parents = {o: Model.owner(o) for o in originals}
        readiness = {o: not any(flag in ("Invalid", "Touched")
                               for dep in [o] + Model.geometry_dependencies(o) for flag in dep.State)
                     for o in originals if o.TypeId in ("PartDesign::Body", "Part::Extrusion", "Part::Revolution", "Part::Loft", "Part::Sweep", "Part::Helix") + PART_PRIMITIVES}
        local_frames = {o: App.Placement(o.Placement) for o in parts}
        labels = {o: o.Label for o in originals}
        old_filename = document.FileName
        mapping, report = {}, []

        def annotate_definition(obj):
            if _own_identity(obj):
                Model._property(obj, "String", "ComponentRole", "Definition", True)
            else:
                Model._identity(obj, "Definition")
            Model._property(obj, "StringList", "ModelHistory", [], True)
            Model._property(obj, "StringList", "ResultObjects", [], True)
            Model._property(obj, "String", "RepresentationOverrides", "{}", True)

        def register(component, obj, role, result=False):
            target = obj.LinkedObject if obj.isDerivedFrom("App::Link") else None
            if target is not None:
                obj.setLink(None)
            if _own_identity(obj) and not hasattr(obj, "ComponentRole"):
                Model._property(obj, "String", "ComponentRole", role, True)
            elif not _own_identity(obj):
                Model._identity(obj, role)
            if target is not None:
                obj.setLink(target)
            # Native addObject expands local-scope dependencies. Legacy consumers
            # may already cross Parts; do not steal their source Body/feature into
            # the consumer's new definition. Set explicit membership instead.
            if Model.owner(obj) is None:
                component.Group = list(component.Group) + [obj]
            Model.register_object(component, obj, role, result)
            if obj in labels:
                obj.Label = labels[obj]

        def occurrence(parent, link, definition):
            parent.addObject(link)
            placement = App.Placement(link.LinkPlacement)
            transform, scale, vector = link.LinkTransform, link.Scale, App.Vector(link.ScaleVector)
            link.setLink(None)
            if _own_identity(link):
                Model._property(link, "String", "ComponentRole", "Occurrence", True)
            else:
                Model._identity(link, "Occurrence")
            link.setLink(definition)
            link.LinkTransform = transform
            link.LinkPlacement = placement
            link.Scale = scale
            link.ScaleVector = vector
            Model._property(link, "String", "DefinitionId", definition.ObjectId if definition else "legacy-unresolved:" + link.Name, True)
            Model._property(link, "Integer", "InstanceNumber", sum(c.LinkedObject == definition for c in Model.children(parent)), True)
            Model._property(link, "Enumeration", "Representation", list(Model.TYPES))
            link.Representation = "Bodies Only"
            Model._property(link, "Bool", "IncludeInBOM", True)
            Model._property(link, "Bool", "IncludeInMass", True)

        with Model.transaction(document, "Convert legacy component structure"):
            meta = Model.initialize(document, document.Label)
            root = meta.RootComponent
            meta.LegacySource = old_filename
            for part in parts:
                annotate_definition(part)
                mapping[part] = part
            for obj in sorted(boundaries - set(parts), key=lambda x: x.Name):
                definition = Model._definition(document, labels[obj])
                Model._property(definition, "Link", "LegacyDefinitionSource", obj, True)
                mapping[obj] = definition
                if obj in arrays:
                    if not _own_identity(obj):
                        Model._identity(obj, "LegacyPayload")
                    for element in obj.ElementList:
                        if element.TypeId == "App::LinkElement":
                            Model._identity(element, "LegacyPayload")
                    frozen = document.addObject("Part::Feature", "RecoveredArray")
                    frozen.Shape = arrays[obj]
                    frozen.Label = obj.Label + " recovered geometry"
                    register(definition, frozen, "Object", True)
                    Model._property(frozen, "String", "LegacyRecovery", "Dumb evaluated array; native array retained; parametric instance mapping pending.", True)
                    if parents[obj]:
                        parents[obj].removeObject(obj)
                    if App.GuiUp:
                        obj.Visibility = False
                    report.append(obj.Label + ": recovered as explicit dumb array geometry; native array identity retained outside component History.")
                elif parents[obj] is None and not obj.isDerivedFrom("App::Link"):
                    register(definition, obj, "Object" if obj.TypeId == "Part::Feature"
                             or obj.isDerivedFrom("Sketcher::SketchObject") else "Operation")
                else:
                    # Internal features keep their native Body/Part ownership.
                    helper = document.addObject("App::Link", "LegacyGeometry")
                    helper.setLink(obj)
                    helper.LinkTransform = True
                    register(definition, helper, "Object", True)
                    report.append(obj.Label + ": native feature ownership retained through a geometry link.")
            for part in parts:
                if parents[part]:
                    parents[part].removeObject(part)
                part.Placement = world[part]

            def component_for(parent):
                while parent is not None:
                    if parent in mapping:
                        return mapping[parent]
                    parent = parents.get(parent)
                return root

            for source, definition in mapping.items():
                # A real legacy container is also a placed use. Additional
                # native Links remain additional uses of the same definition.
                if source in parts or source in arrays or parents[source] is None:
                    parent = component_for(parents[source])
                    link = document.addObject("App::Link", "ComponentInstance")
                    link.setLink(definition)
                    link.LinkTransform = False
                    link.LinkPlacement = local_frames[source] if source in parts else App.Placement()
                    link.Label = labels[source]
                    occurrence(parent, link, definition)
            for link, (target, placement, transform, old_target_frame) in snapshots.items():
                if target.Document == document:
                    definition = mapping[target]
                elif Model.is_component(target):
                    definition = target
                else:
                    candidates = [d for d in Model.definitions(target.Document)
                                  if getattr(d, "LegacyDefinitionSource", None) == target]
                    if len(candidates) != 1:
                        raise ValueError("External legacy target has no unique converted definition.")
                    definition = candidates[0]
                parent = component_for(parents[link])
                if parents[link]:
                    parents[link].removeObject(link)
                # A native Part is now in its original world frame. A wrapper
                # retains its source's local frame. Compensate, never normalize
                # silently or change shared source geometry.
                if target in parts or (target.Document != document and Model.is_component(target)):
                    if transform:
                        delta = old_target_frame.multiply(definition.Placement.inverse())
                    else:
                        delta = App.Placement()
                elif not transform:
                    delta = old_target_frame.inverse()
                else:
                    delta = App.Placement()
                scale = App.Matrix()
                vector = App.Vector(link.ScaleVector)
                if link.Scale != 1:
                    vector = App.Vector(link.Scale, link.Scale, link.Scale)
                scale.A11, scale.A22, scale.A33 = vector.x, vector.y, vector.z
                matrix = placement.toMatrix().multiply(scale).multiply(delta.toMatrix()).multiply(scale.inverse())
                placement = App.Placement(matrix)
                if max(abs(a - b) for a, b in zip(matrix.A, placement.toMatrix().A)) > 1e-9:
                    raise ValueError("Nonuniform scaled frame compensation requires affine recovery; native payload is retained.")
                link.setLink(definition)
                link.LinkTransform = transform
                link.LinkPlacement = placement
                link.Label = labels[link]
                occurrence(parent, link, definition)

            for link in links:
                if link in arrays or link in snapshots:
                    continue
                parent = component_for(parents[link])
                if parents[link]:
                    parents[link].removeObject(link)
                occurrence(parent, link, None)
                report.append(link.Label + ": unresolved native target retained as a missing Part Tree instance; repair required before saving.")

            for obj in originals:
                if obj in parts or obj in links or hasattr(obj, "ComponentRole"):
                    continue
                owner = Model.owner(obj)
                if obj.TypeId == "App::Origin" or any(obj in p.Origin.OriginFeatures for p in parts):
                    continue
                if owner is None or Model.is_component(owner):
                    component = owner or root
                    if "Shape" in obj.PropertiesList:
                        register(component, obj, "Object" if obj.TypeId == "Part::Feature"
                                 or obj.isDerivedFrom("Sketcher::SketchObject") else "Operation")
            for definition in Model.definitions(document):
                for obj in Model.history(definition):
                    if is_datum(obj):
                        continue  # Datum frames are construction inputs, not solid/sheet results.
                    if "Shape" not in obj.PropertiesList:
                        continue
                    shape = obj.getPropertyByName("Shape")
                    if shape.isNull() or not shape.isValid():
                        report.append(obj.Label + ": native payload retained; evaluated output needs repair.")
                    else:
                        # Structural migration must not duplicate the source
                        # shape in a native Part compound. Task three owns the
                        # operation/result-layer migration; use the retained
                        # editable native output directly in this milestone.
                        definition.ResultObjects = list(definition.ResultObjects) + [obj.Name]
                    if obj.TypeId == "PartDesign::Body":
                        report.append(obj.Label + ": native Body Tip and sketch/feature history retained; feature adapters pending.")
            migrate_body_histories(document, report, readiness)
            migrate_extrusions(document, report, readiness)
            migrate_revolutions(document, report, readiness)
            migrate_lofts(document, report, readiness)
            migrate_pipes(document, report, readiness)
            migrate_helixes(document, report, readiness)
            migrate_primitives(document, report, readiness)
            migrate_datum_frames(document, report)
            migrate_sketch_inputs(document, report)
            meta.ConversionReport = report + ["Models and linked Part Tree instances converted; native features retained.",
                "Recovery policy: retained editable native features before explicit validated dumb geometry; no fallback created in this structural step."]
            if external:
                meta.ConversionReport = list(meta.ConversionReport) + ["Save converted external files as new .cadprt files before saving this parent; legacy originals remain protected."]
            Model.validate(document, allow_unresolved=True)
        # Native external-link relocation needs an owner-file reference base
        # while dependencies are saved first. The manifest's LegacySource guard
        # prohibits writing this legacy path; Save As must choose a new cadprt.
        document.FileName = old_filename if external or extra_targets else ""
        return document
    finally:
        visiting.remove(document.Name)
