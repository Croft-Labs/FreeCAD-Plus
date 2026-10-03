# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component Loft with ordered associative sections and native add/subtract engines."""
import sys
import ComponentNativeOperation as Native
import math
import FreeCAD as App
import ComponentModel as Model
import ComponentProfile as Profile
from ComponentExtrude import MODES

NAME = "Loft"
MODE_PROPERTY = "LoftMode"
BOOLEANS = ("Union", "Subtraction")


def defaults():
    return dict(ruled=False, closed=False, refine=True, fuzzy=0.)


def read(operation):
    sections = Native.read_sections(operation)
    return sections, operation.LoftMode, operation.BaseFeature, dict(
        ruled=operation.Ruled, closed=operation.Closed, refine=operation.Refine,
        fuzzy=operation.FuzzyTolerance)


section_shape = Native.section_shape


def validate(component, sections, mode, target, options, operation=None):
    if not Model.is_component(component) or mode not in MODES:
        raise ValueError("Choose an active component and a Loft operation.")
    if not math.isfinite(options.get("fuzzy", 0.)) or not -1. <= options.get("fuzzy", 0.) <= 1.:
        raise ValueError("Fuzzy tolerance must be between -1 and 1 mm; zero uses the native default and negative values request automatic tolerance.")
    if len(sections) < 2:
        raise ValueError("Loft needs at least two ordered sections.")
    if options["closed"] and len(sections) < 3:
        raise ValueError("A closed Loft needs at least three sections.")
    keys = [(obj.Name if obj else None, tuple(elements) if elements is not None else None) for obj, elements in sections]
    if len(set(keys)) != len(keys):
        raise ValueError("Do not repeat a section; use Closed to connect last to first.")
    for index, (obj, elements) in enumerate(sections):
        shape = section_shape(component, obj, elements, operation)
        if not shape.Edges and (options["closed"] or index not in (0, len(sections) - 1)):
            raise ValueError("A vertex is supported only at an open Loft's first or last section.")
    if mode == "New Body":
        if target is not None:
            raise ValueError("New Body does not use a target body.")
    else:
        if target is None or Model.owner(target) != component or target.Name not in component.ResultObjects:
            raise ValueError("Choose an explicit target body in the active component.")
        if len(Model.current_shape(target).Solids) != 1:
            raise ValueError("The target must be one current solid body.")
        if operation and (target == operation or operation in target.OutListRecursive):
            raise ValueError("Loft cannot target its own downstream result.")


def feature(doc, mode):
    import PartDesign
    return doc.addObject("PartDesign::SubtractiveLoft" if mode == "Subtract" else "PartDesign::AdditiveLoft", "Loft")


def configure(operation, sections, target, options):
    operation.Profile = sections[0]
    operation.Sections = sections[1:]
    operation.BaseFeature = target
    operation.Ruled, operation.Closed, operation.Refine = options["ruled"], options["closed"], options["refine"]
    operation.FuzzyTolerance = options.get("fuzzy", 0.)


def evaluate(doc, operation, mode, target):
    doc.recompute()
    if "Invalid" in operation.State or operation.Shape.isNull() or Model._shape_kind(operation.Shape) != "Body":
        raise ValueError("Loft requires one valid solid. Check section order, compatible contours and target contact.")
    if mode != "New Body" and abs(operation.Shape.Volume - Model.current_shape(target).Volume) < 1e-9:
        raise ValueError("Loft adds or removes no material from the selected target.")
    return operation.Shape.copy()


def preview(component, sections, mode="New Body", target=None, options=None, volume_only=False):
    options = options or defaults()
    validate(component, sections, mode, target, options)
    scratch = App.newDocument("ComponentLoftPreview", hidden=True, temp=True)
    try:
        copied = []
        for source, elements in sections:
            obj = scratch.addObject("Part::Part2DObjectPython" if source.isDerivedFrom("Part::Part2DObject") else "Part::Feature", "Section")
            # Loft consumes placed section shapes. Normalizing a copied sketch's
            # local frame would collapse sections whose shape already carries placement.
            obj.Shape = section_shape(component, source, elements)
            copied.append((obj, [""]))
        base = None
        if target:
            base = scratch.addObject("Part::Feature", "Target")
            base.Shape = Model.current_shape(target)
        operation = feature(scratch, mode)
        configure(operation, copied, base, options)
        result = evaluate(scratch, operation, mode, base)
        return (base.Shape.cut(result) if mode == "Subtract" else result.cut(base.Shape)) if volume_only and base else result
    finally:
        App.closeDocument(scratch.Name)
        App.setActiveDocument(component.Document.Name)


def input_objects(sections, options):
    return [source for source, elements in sections]


def create(component, sections, mode="New Body", target=None, options=None):
    return Native.create(sys.modules[__name__], component, sections, mode, target, options)


def edit(operation, sections, mode, target=None, options=None):
    return Native.edit(sys.modules[__name__], operation, sections, mode, target, options)
