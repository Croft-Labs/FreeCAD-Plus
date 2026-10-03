# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component Pipe backed by native additive/subtractive sweep features."""
import math
import sys
import FreeCAD as App
import Part
import ComponentModel as Model
import ComponentNativeOperation as Native
from ComponentExtrude import MODES

NAME = "Pipe"
MODE_PROPERTY = "PipeMode"
BOOLEANS = ("Union", "Subtraction", "Common")
ORIENTATIONS = ("Standard", "Fixed", "Frenet", "Auxiliary", "Binormal")
TRANSITIONS = ("Transformed", "Right corner", "Round corner")
TRANSFORMATIONS = ("Constant", "Multisection")
section_shape = Native.section_shape


def defaults():
    return dict(spine=None, auxiliary=None, orientation="Standard", transition="Transformed",
                transformation="Constant", binormal=(0., 0., 1.), curvilinear=True,
                spine_tangent=False, auxiliary_tangent=False, refine=True, fuzzy=0., boolean="Subtraction")


def read(operation):
    values = defaults()
    values.update(spine=(operation.Spine[0], list(operation.Spine[1])) if operation.Spine else None,
                  auxiliary=(operation.AuxiliarySpine[0], list(operation.AuxiliarySpine[1])) if operation.AuxiliarySpine else None,
                  orientation=operation.Mode, transition=operation.Transition, transformation=operation.Transformation,
                  binormal=tuple(operation.Binormal), curvilinear=operation.AuxiliaryCurvilinear,
                  spine_tangent=operation.SpineTangent, auxiliary_tangent=operation.AuxiliarySpineTangent,
                  refine=operation.Refine, fuzzy=operation.FuzzyTolerance,
                  boolean=operation.Operation if operation.PipeMode == "Subtract" else "Subtraction")
    return Native.read_sections(operation), operation.PipeMode, operation.BaseFeature, values


def path_shape(component, reference, operation=None):
    if not reference or reference[0] is None:
        raise ValueError("Choose a path owned by the active component.")
    obj, names = reference
    if Model.owner(obj) != component or getattr(obj, "ComponentRole", "") not in ("Object", "Reference", "Result"):
        raise ValueError("Choose a path owned by the active component.")
    if operation and (obj == operation or operation in obj.OutListRecursive):
        raise ValueError("Pipe cannot reference its own downstream result.")
    shape = Model.current_shape(obj)
    names = [name for name in names if name]
    if names:
        if len(set(names)) != len(names) or any(not name.startswith("Edge") or not name[4:].isdigit() for name in names):
            raise ValueError("Select distinct path edges from one object.")
        edges = [shape.getElement(name) for name in names]
    else:
        if shape.Solids or shape.Faces:
            raise ValueError("Select edges of the body or face, or a whole curve object.")
        edges = shape.Edges
    if not edges:
        raise ValueError("The path has no edges.")
    groups = Part.sortEdges(edges)
    if len(groups) != 1:
        raise ValueError("Path edges must form one connected wire.")
    wire = Part.Wire(groups[0])
    if not wire.isValid():
        raise ValueError("The path must form one valid wire.")
    return wire


def validate(component, sections, mode, target, options, operation=None):
    if not Model.is_component(component) or mode not in MODES:
        raise ValueError("Choose an active component and a Pipe operation.")
    if not sections:
        raise ValueError("Append a profile section before creating Pipe.")
    if options["transformation"] not in TRANSFORMATIONS:
        raise ValueError("Choose Constant or Multisection; other native scaling laws are not implemented.")
    if options["transformation"] == "Multisection" and len(sections) < 2:
        raise ValueError("Multisection needs a profile and at least one additional section.")
    keys = [(obj.Name if obj else None, tuple(elements) if elements is not None else None) for obj, elements in sections]
    if len(set(keys)) != len(keys):
        raise ValueError("Do not repeat a Pipe section.")
    for obj, elements in sections:
        shape = section_shape(component, obj, elements, operation)
        # The native Pipe reader requires faces, including at section ends.
        # Its dormant point-section branches cannot accept a vertex profile.
        if not shape.Edges:
            raise ValueError("Native Pipe requires closed profile sections; point-ended sections are not supported.")
    path_shape(component, options["spine"], operation)
    if options["orientation"] not in ORIENTATIONS or options["transition"] not in TRANSITIONS:
        raise ValueError("Choose a supported orientation and corner transition.")
    if options["auxiliary"]:
        path_shape(component, options["auxiliary"], operation)
    if options["orientation"] == "Auxiliary" and not options["auxiliary"]:
        raise ValueError("Auxiliary orientation needs an auxiliary path.")
    vector = options["binormal"]
    if len(vector) != 3 or not all(math.isfinite(v) for v in vector):
        raise ValueError("Enter a finite binormal vector.")
    if options["orientation"] == "Binormal" and App.Vector(*vector).Length < 1e-12:
        raise ValueError("Binormal orientation requires a nonzero vector.")
    if not math.isfinite(options["fuzzy"]) or not -1 <= options["fuzzy"] <= 1:
        raise ValueError("Fuzzy tolerance must be between -1 and 1 mm.")
    if options["boolean"] not in ("Subtraction", "Common"):
        raise ValueError("Choose Subtraction or Common for the native subtractive result.")
    if mode == "New Body":
        if target is not None:
            raise ValueError("New Body does not use a target.")
    else:
        if target is None or Model.owner(target) != component or target.Name not in component.ResultObjects:
            raise ValueError("Choose an explicit target body in the active component.")
        if len(Model.current_shape(target).Solids) != 1:
            raise ValueError("Choose one current solid target.")
        if operation and (target == operation or operation in target.OutListRecursive):
            raise ValueError("Pipe cannot target its own downstream result.")


def feature(doc, mode, options=None):
    import PartDesign
    return doc.addObject("PartDesign::SubtractivePipe" if mode == "Subtract" else "PartDesign::AdditivePipe", "Pipe")


def configure(operation, sections, target, options):
    operation.Profile, operation.Sections = sections[0], sections[1:]
    operation.BaseFeature = target
    operation.Spine = options["spine"]
    operation.AuxiliarySpine = options["auxiliary"] or (None, [])
    operation.Mode, operation.Transition, operation.Transformation = options["orientation"], options["transition"], options["transformation"]
    operation.Binormal = App.Vector(*options["binormal"])
    operation.AuxiliaryCurvilinear = options["curvilinear"]
    operation.SpineTangent, operation.AuxiliarySpineTangent = options["spine_tangent"], options["auxiliary_tangent"]
    operation.Refine, operation.FuzzyTolerance = options["refine"], options["fuzzy"]
    if operation.TypeId == "PartDesign::SubtractivePipe":
        operation.Operation = options["boolean"]


def evaluate(doc, operation, mode, target):
    doc.recompute()
    if "Invalid" in operation.State or operation.Shape.isNull() or Model._shape_kind(operation.Shape) != "Body":
        raise ValueError("Pipe requires one valid solid. Check the profile, path, section order, orientation and target contact.")
    if mode != "New Body" and abs(operation.Shape.Volume - Model.current_shape(target).Volume) < 1e-9:
        raise ValueError("Pipe changes no material in the selected target.")
    return operation.Shape.copy()


def preview(component, sections, mode="New Body", target=None, options=None, volume_only=False):
    options = options or defaults()
    validate(component, sections, mode, target, options)
    scratch = App.newDocument("ComponentPipePreview", hidden=True, temp=True)
    try:
        copied = []
        for source, elements in sections:
            obj = scratch.addObject("Part::Part2DObjectPython", "Section")
            obj.Shape = section_shape(component, source, elements)
            copied.append((obj, [""]))
        values = dict(options)
        for key in ("spine", "auxiliary"):
            if options[key]:
                obj = scratch.addObject("Part::Feature", key)
                obj.Shape = path_shape(component, options[key])
                values[key] = (obj, [])
        base = None
        if target:
            base = scratch.addObject("Part::Feature", "Target")
            base.Shape = Model.current_shape(target)
        operation = feature(scratch, mode)
        configure(operation, copied, base, values)
        result = evaluate(scratch, operation, mode, base)
        return (base.Shape.cut(result) if mode == "Subtract" else result.cut(base.Shape)) if volume_only and base else result
    finally:
        App.closeDocument(scratch.Name)
        App.setActiveDocument(component.Document.Name)


def input_objects(sections, options):
    return [obj for obj, elements in sections] + [options[key][0] for key in ("spine", "auxiliary") if options[key]]


def create(component, sections, mode="New Body", target=None, options=None):
    return Native.create(sys.modules[__name__], component, sections, mode, target, options)


def edit(operation, sections, mode, target=None, options=None):
    return Native.edit(sys.modules[__name__], operation, sections, mode, target, options)
