# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component Helix using native additive/subtractive geometry and parameter laws."""
import math
import sys
import FreeCAD as App
import Part
import ComponentModel as Model
import ComponentProfile as Profile
import ComponentNativeOperation as Native
import ComponentExtrude as Extrude

NAME = "Helix"
MODE_PROPERTY = "HelixMode"
MODES = Extrude.MODES
BOOLEANS = ("Union", "Subtraction", "Common")
INPUT_MODES = ("pitch-height-angle", "pitch-turns-angle", "height-turns-angle", "height-turns-growth")


def defaults():
    return dict(input_mode=INPUT_MODES[0], pitch=10., height=30., turns=3., angle=0., growth=0.,
                axis="V_Axis", axis_reference=None, left=False, reversed=False,
                refine=True, tolerance=0.1, fuzzy=0., boolean="Subtraction")


def read(operation):
    values = defaults()
    reference = operation.ReferenceAxis
    if reference and hasattr(reference[0], "AxisSource"):
        reference = reference[0].AxisSource, [reference[0].AxisName]
    if reference and list(reference[1]) == ["Axis"]:
        # Native LinkSub canonicalization drops the zero in construction Axis0.
        reference = reference[0], ["Axis0"]
    profile = Native.read_sections(operation)[0][0]
    sketch_axis = reference and reference[0] in (operation.Profile[0], profile) and reference[1] and reference[1][0].startswith(("V_Axis", "H_Axis", "N_Axis", "Axis"))
    values.update(input_mode=operation.Mode, pitch=operation.Pitch.Value, height=operation.Height.Value,
                  turns=operation.Turns, angle=operation.Angle.Value, growth=operation.Growth.Value,
                  axis=reference[1][0] if sketch_axis else "Reference",
                  axis_reference=(reference[0], list(reference[1])) if reference else None,
                  left=operation.LeftHanded, reversed=operation.Reversed, refine=operation.Refine,
                  tolerance=operation.Tolerance, fuzzy=operation.FuzzyTolerance,
                  boolean=operation.Operation if operation.HelixMode == "Subtract" else "Subtraction")
    return Native.read_sections(operation), operation.HelixMode, operation.BaseFeature, values


def normalized(values):
    """Match native dependent dimensions without mutating the stored definition."""
    values = dict(values)
    mode = values["input_mode"]
    if mode not in INPUT_MODES:
        raise ValueError("Choose a native Helix parameter mode.")
    for key in ("pitch", "height", "turns", "angle", "growth", "tolerance", "fuzzy"):
        if not math.isfinite(values[key]):
            raise ValueError("Helix dimensions must be finite.")
    if not -89 <= values["angle"] <= 89 or not 0.1 <= values["tolerance"] <= 2147483647 or not -1 <= values["fuzzy"] <= 1:
        raise ValueError("Cone angle must be -89 to 89 degrees, fusion tolerance at least 0.1 and fuzzy tolerance -1 to 1 mm.")
    if mode.startswith("pitch") and values["pitch"] < 1e-7:
        raise ValueError("Pitch must be positive.")
    if mode != INPUT_MODES[1] and (values["height"] < 0 or (mode != INPUT_MODES[3] and values["height"] < 1e-7)):
        raise ValueError("Height must be positive, or zero for a flat spiral in Height-Turns-Growth mode.")
    if mode != INPUT_MODES[0] and not 1e-7 <= values["turns"] <= 2147483647:
        raise ValueError("Turns must be positive.")
    if mode == INPUT_MODES[0]:
        values["turns"] = values["height"] / values["pitch"]
    elif mode == INPUT_MODES[1]:
        values["height"] = values["pitch"] * values["turns"]
    else:
        values["pitch"] = values["height"] / values["turns"]
    if mode != INPUT_MODES[3]:
        values["growth"] = values["pitch"] * math.tan(math.radians(values["angle"]))
    elif values["height"]:
        values["angle"] = math.degrees(math.atan(values["growth"] / values["pitch"]))
    elif abs(values["growth"]) < 1e-7 and values["turns"] > 1:
        raise ValueError("A flat spiral longer than one turn requires radial growth.")
    return values


def validate(component, sections, mode, target, options, operation=None):
    if len(sections) != 1 or sections[0][0] is None:
        raise ValueError("Choose one Helix profile.")
    profile, elements = sections[0]
    Extrude.inputs(component, profile, 1., mode, target, operation, elements)
    normalized(options)
    if options["boolean"] not in ("Subtraction", "Common"):
        raise ValueError("Choose Subtraction or Common.")
    axis = options["axis"]
    if axis in ("V_Axis", "H_Axis", "N_Axis"):
        if not profile.isDerivedFrom("Part::Part2DObject"):
            raise ValueError("Choose a reference axis for a non-sketch profile.")
    elif axis.startswith("Axis") and axis[4:].isdigit():
        if int(axis[4:]) >= getattr(profile, "AxisCount", 0):
            raise ValueError("The sketch construction axis is unavailable.")
    elif axis == "Reference":
        reference = options["axis_reference"]
        if not reference or not reference[0]:
            raise ValueError("Choose a local reference axis.")
        obj, subs = reference
        if obj.Document != component.Document or not (Model.owner(obj) == component or obj in component.Origin.OriginFeatures):
            raise ValueError("Choose an axis owned by the active component.")
        if operation and (obj == operation or operation in obj.OutListRecursive):
            raise ValueError("Helix cannot reference its own downstream result.")
        if obj.isDerivedFrom("App::Line") or obj.isDerivedFrom("PartDesign::Line"):
            pass
        elif hasattr(obj, "Shape") and not obj.Shape.isNull():
            shape = Model.current_shape(obj)
            if len(subs) != 1 or not subs[0].startswith("Edge"):
                raise ValueError("Choose one straight or circular edge as the reference axis.")
            shape.getElement(subs[0])
        else:
            raise ValueError("Choose a datum/origin axis or a straight or circular edge.")
    else:
        raise ValueError("Choose a sketch or reference axis.")


def construction_shape(source, name):
    axis = source.getAxis(int(name[4:]))
    base = source.Placement.multVec(axis.Base)
    direction = source.Placement.Rotation.multVec(axis.Direction)
    return Part.makeLine(base, base + direction)


class AxisProxy(Model.PersistentProxy):
    def execute(self, obj):
        obj.Shape = Part.Shape()
        source = obj.AxisSource
        Model.current_shape(source)
        obj.Shape = construction_shape(source, obj.AxisName)


def internal_inputs(operation):
    axis = getattr(operation.Profile[0], "HelixAxis", None)
    return [axis] if axis else []


def feature(doc, mode):
    import PartDesign
    return doc.addObject("PartDesign::SubtractiveHelix" if mode == "Subtract" else "PartDesign::AdditiveHelix", "Helix")


def configure(operation, sections, target, options):
    bound = sections[0][0]
    operation.Profile, operation.BaseFeature = (bound, []), target
    operation.Mode = options["input_mode"]
    for key, prop in (("pitch", "Pitch"), ("height", "Height"), ("turns", "Turns"), ("angle", "Angle"), ("growth", "Growth")):
        setattr(operation, prop, options[key])
    operation.HasBeenEdited = True
    axis = options["axis"]
    if axis == "Reference":
        source, subs = options["axis_reference"]
        operation.ReferenceAxis = (source, subs or [""])
    elif axis.startswith("Axis") and hasattr(bound, "ProfileSource"):
        helper = getattr(bound, "HelixAxis", None)
        if helper is None:
            component = Model.owner(bound)
            helper = operation.Document.addObject("Part::FeaturePython", "HelixAxis")
            component.addObject(helper)
            Model._identity(helper, "Internal")
            Model._property(helper, "Link", "AxisSource", bound.ProfileSource[0])
            Model._property(helper, "String", "AxisName", axis)
            helper.Proxy = AxisProxy()
            Model._property(bound, "Link", "HelixAxis", helper)
            if App.GuiUp:
                helper.ViewObject.Proxy = 0
                helper.ViewObject.ShowInTree = False
                helper.Visibility = False
        operation.ReferenceAxis = (helper, ["Edge1"])
    else:
        operation.ReferenceAxis = (bound, [axis])
    operation.LeftHanded, operation.Reversed = options["left"], options["reversed"]
    operation.Refine, operation.Tolerance, operation.FuzzyTolerance = options["refine"], options["tolerance"], options["fuzzy"]
    if operation.TypeId == "PartDesign::SubtractiveHelix":
        operation.Operation = options["boolean"]


def evaluate(doc, operation, mode, target):
    doc.recompute()
    if "Invalid" in operation.State or operation.Shape.isNull() or Model._shape_kind(operation.Shape) != "Body":
        raise ValueError("Helix requires one valid solid. Check profile, axis, pitch, growth and target contact.")
    if target and abs(operation.Shape.Volume - Model.current_shape(target).Volume) < 1e-9:
        raise ValueError("Helix changes no material in the selected target.")
    return operation.Shape.copy()


def preview(component, sections, mode="New Body", target=None, options=None, volume_only=False):
    options = options or defaults()
    validate(component, sections, mode, target, options)
    profile, elements = sections[0]
    scratch = App.newDocument("ComponentHelixPreview", hidden=True, temp=True)
    try:
        copied = scratch.addObject("Part::Part2DObjectPython", "Profile")
        if elements is None:
            # A whole sketch already carries its placement in the shape location.
            copied.Shape = Model.current_shape(profile)
        else:
            Profile.assign_shape(copied, profile, Profile.face(profile, elements))
        values = dict(options)
        if values["axis"] == "Reference" or values["axis"].startswith("Axis"):
            axis = scratch.addObject("Part::Feature", "Axis")
            if values["axis"].startswith("Axis"):
                axis.Shape = construction_shape(profile, values["axis"])
                subs = ["Edge1"]
            else:
                source, subs = values["axis_reference"]
                if source.isDerivedFrom("App::Line") or source.isDerivedFrom("PartDesign::Line"):
                    direction = App.Vector(1, 0, 0) if source.isDerivedFrom("App::Line") else App.Vector(0, 0, 1)
                    frame = source.Placement
                    axis.Shape = Part.makeLine(frame.Base, frame.Base + frame.Rotation.multVec(direction))
                    subs = ["Edge1"]
                else:
                    axis.Shape = Model.current_shape(source)
            values.update(axis="Reference", axis_reference=(axis, subs))
        base = None
        if target:
            base = scratch.addObject("Part::Feature", "Target")
            base.Shape = Model.current_shape(target)
        operation = feature(scratch, mode)
        configure(operation, [(copied, [])], base, values)
        result = evaluate(scratch, operation, mode, base)
        return (base.Shape.cut(result) if mode == "Subtract" else result.cut(base.Shape)) if volume_only and base else result
    finally:
        App.closeDocument(scratch.Name)
        App.setActiveDocument(component.Document.Name)


def input_objects(sections, options):
    return [sections[0][0]]


def create(component, sections, mode="New Body", target=None, options=None):
    return Native.create(sys.modules[__name__], component, sections, mode, target, options)


def edit(operation, sections, mode, target=None, options=None):
    return Native.edit(sys.modules[__name__], operation, sections, mode, target, options)
