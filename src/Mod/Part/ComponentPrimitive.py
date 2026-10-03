# SPDX-License-Identifier: LGPL-2.1-or-later
"""One component operation backed by the eight native Part Design primitives."""
import math
import sys
import FreeCAD as App
import Part
import ComponentModel as Model
import ComponentNativeOperation as Native
from ComponentExtrude import MODES

NAME = "Primitive"
MODE_PROPERTY = "PrimitiveMode"
BOOLEANS = ("Union", "Subtraction", "Common")
# Native property identities and defaults; length units are millimetres.
PARAMETERS = {
    "Box": dict(Length=10., Width=10., Height=10.),
    "Cylinder": dict(Radius=10., Height=10., Angle=360., FirstAngle=0., SecondAngle=0.),
    "Sphere": dict(Radius=5., Angle1=-90., Angle2=90., Angle3=360.),
    "Cone": dict(Radius1=2., Radius2=4., Height=10., Angle=360.),
    "Ellipsoid": dict(Radius1=2., Radius2=4., Radius3=0., Angle1=-90., Angle2=90., Angle3=360.),
    "Torus": dict(Radius1=10., Radius2=2., Angle1=-180., Angle2=180., Angle3=360.),
    "Prism": dict(Polygon=6, Circumradius=2., Height=10., FirstAngle=0., SecondAngle=0.),
    "Wedge": dict(Xmin=0., Ymin=0., Zmin=0., Xmax=10., Ymax=10., Zmax=10.,
                  X2min=2., Z2min=2., X2max=8., Z2max=8.),
}


def defaults(kind="Box"):
    return dict(kind=kind, dimensions=dict(PARAMETERS[kind]), placement=App.Placement(),
                map_mode="Deactivated", support=[], offset=App.Placement(), reverse=False,
                parameter=0., attacher="Attacher::AttachEngine3D", refine=True, fuzzy=0., boolean="Subtraction")


def kind_of(operation):
    return operation.TypeId.split("::")[1].removeprefix("Additive").removeprefix("Subtractive")


def read(operation):
    options = defaults(kind_of(operation))
    options.update(dimensions={name: float(getattr(operation, name)) for name in options["dimensions"]},
                   placement=App.Placement(operation.Placement), map_mode=operation.MapMode,
                   support=list(operation.AttachmentSupport), offset=App.Placement(operation.AttachmentOffset),
                   reverse=operation.MapReversed, parameter=operation.MapPathParameter,
                   attacher=operation.AttacherType, refine=operation.Refine, fuzzy=operation.FuzzyTolerance,
                   boolean=operation.Operation if operation.PrimitiveMode == "Subtract" else "Subtraction")
    return [], operation.PrimitiveMode, operation.BaseFeature, options


def attachment(options):
    engine = Part.AttachEngine(options["attacher"])
    engine.References = options["support"]
    engine.Mode = options["map_mode"]
    engine.AttachmentOffset = options["offset"]
    engine.Reverse = options["reverse"]
    engine.Parameter = options["parameter"]
    return engine


def validate(component, sections, mode, target, options, operation=None):
    if not Model.is_component(component) or mode not in MODES or sections:
        raise ValueError("Choose an active component and a Primitive operation; no profile is needed.")
    kind = options["kind"]
    if kind not in PARAMETERS or set(options["dimensions"]) != set(PARAMETERS[kind]):
        raise ValueError("Choose a primitive shape and its complete dimensions.")
    dims = options["dimensions"]
    if not all(math.isfinite(value) for value in list(dims.values()) + [options["fuzzy"], options["parameter"]]):
        raise ValueError("Dimensions and tolerances must be finite.")
    if not -1 <= options["fuzzy"] <= 1 or options["boolean"] not in ("Subtraction", "Common"):
        raise ValueError("Choose Subtraction or Common and a fuzzy tolerance from -1 to 1 mm.")
    for name, value in dims.items():
        if "Angle" in name:
            lower, upper = (-89.99, 89.99) if name in ("FirstAngle", "SecondAngle") else ((-180., 180.) if kind == "Torus" else (-90., 90.)) if name in ("Angle1", "Angle2") else (1e-7, 360.)
        elif name == "Polygon":
            lower, upper = 3, 100000
            if value != int(value):
                raise ValueError("The prism needs a whole number of sides.")
        elif kind == "Wedge":
            continue
        else:
            lower = 0. if (kind == "Cone" and name.startswith("Radius")) or name == "Radius3" else 2e-7
            upper = 1e9
        if not lower <= value <= upper:
            raise ValueError(f"{name} must be between {lower:g} and {upper:g}.")
    if "Angle1" in dims and dims["Angle1"] >= dims["Angle2"]:
        raise ValueError("The lower angle must be less than the upper angle.")
    if mode == "New Body":
        if target is not None:
            raise ValueError("New Body does not use a target.")
    else:
        if target is None or Model.owner(target) != component or target.Name not in component.ResultObjects:
            raise ValueError("Choose an explicit target body in the active component.")
        if len(Model.current_shape(target).Solids) != 1:
            raise ValueError("The target must be one current solid body.")
        if operation and (target == operation or operation in target.OutListRecursive):
            raise ValueError("A primitive cannot target its own downstream result.")
    for source, elements in options["support"]:
        if source is None or source.Document != component.Document or not (Model.owner(source) == component or source in component.Origin.OriginFeatures):
            raise ValueError("Attachment references must belong to the active component.")
        if operation and (source == operation or operation in source.OutListRecursive):
            raise ValueError("A primitive cannot attach to its own downstream result.")
        if hasattr(source, "Shape"):
            Model.current_shape(source)
    attachment(options).calculateAttachedPlacement(options["placement"])


def feature(doc, mode, options=None):
    import PartDesign
    kind = (options or defaults())["kind"]
    return doc.addObject("PartDesign::" + ("Subtractive" if mode == "Subtract" else "Additive") + kind, "Primitive")


def needs_replacement(operation, options):
    return kind_of(operation) != options["kind"]


def configure(operation, sections, target, options):
    operation.BaseFeature = target
    for name, value in options["dimensions"].items():
        setattr(operation, name, int(value) if name == "Polygon" else value)
    operation.AttacherType = options["attacher"]
    operation.Placement = options["placement"]
    attachment(options).writeParametersToFeature(operation)
    operation.Refine, operation.FuzzyTolerance = options["refine"], options["fuzzy"]
    if operation.TypeId.startswith("PartDesign::Subtractive"):
        operation.Operation = options["boolean"]


def evaluate(doc, operation, mode, target):
    doc.recompute()
    if "Invalid" in operation.State or operation.Shape.isNull() or Model._shape_kind(operation.Shape) != "Body":
        raise ValueError("Primitive requires one valid solid. Check dimensions, attachment and target contact.")
    if target and abs(operation.Shape.Volume - Model.current_shape(target).Volume) < 1e-9:
        raise ValueError("Primitive changes no material in the selected target.")
    return operation.Shape.copy()


def preview(component, sections, mode="New Body", target=None, options=None, volume_only=False, tool_only=False):
    if tool_only:
        # The overlay is the full native tool, regardless of Boolean contact.
        mode, target = "New Body", None
    options = options or defaults()
    validate(component, sections, mode, target, options)
    # Resolve native attachment before copying: no live document links in the scratch document.
    values = dict(options)
    values["placement"] = attachment(options).calculateAttachedPlacement(options["placement"]) or options["placement"]
    values.update(map_mode="Deactivated", support=[])
    scratch = App.newDocument("ComponentPrimitivePreview", hidden=True, temp=True)
    try:
        base = None
        if target:
            base = scratch.addObject("Part::Feature", "Target")
            base.Shape = Model.current_shape(target)
        operation = feature(scratch, mode, values)
        configure(operation, [], base, values)
        result = evaluate(scratch, operation, mode, base)
        return (base.Shape.cut(result) if mode == "Subtract" else result.cut(base.Shape)) if volume_only and base else result
    finally:
        App.closeDocument(scratch.Name)
        App.setActiveDocument(component.Document.Name)


def input_objects(sections, options):
    return []  # Attachment references remain visible and reusable.


def create(component, sections=(), mode="New Body", target=None, options=None):
    return Native.create(sys.modules[__name__], component, sections, mode, target, options)


def edit(operation, sections, mode, target=None, options=None):
    return Native.edit(sys.modules[__name__], operation, sections, mode, target, options)
