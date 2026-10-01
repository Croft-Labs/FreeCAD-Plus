# SPDX-License-Identifier: LGPL-2.1-or-later
"""Compatibility review for native version-1 CAM setup templates.

Keep model and operation creation in the native Job services. This module reads
and validates portable settings before any document objects are created.
"""
import copy
import json
import math
import re

import FreeCAD
import Path

UNITS = "mm, s, deg"
ROOT_KEYS = {
    "Version", "Desc", "Tolerance", "Post", "PostArgs", "Output", "Fixtures",
    "OrderOutputBy", "SplitOutput", "SetupSheet", "Stock", "ToolController",
    "PostPropertyOverrides", "Machine", "TemplateInfo",
}


def validate(attrs):
    """Return an independent native template; reject known silent fallbacks."""
    if not isinstance(attrs, dict) or attrs.get("Version") not in (1, "1"):
        raise ValueError("Select a supported version-1 CAM job template.")
    extra = set(attrs) - ROOT_KEYS
    if extra:
        raise ValueError("Unsupported template fields: " + ", ".join(sorted(extra)))
    for key in ("Desc", "Post", "PostArgs", "Output", "Machine", "OrderOutputBy"):
        if key in attrs and not isinstance(attrs[key], str):
            raise ValueError("Template %s must be text." % key)
    post = attrs.get("Post")
    if post and post not in Path.Preferences.allEnabledLegacyPostProcessors():
        raise ValueError("Template postprocessor '%s' is not enabled or available." % post)
    if not post and (attrs.get("PostArgs") or attrs.get("PostPropertyOverrides")):
        raise ValueError("Post settings require an explicit template postprocessor.")
    info = attrs.get("TemplateInfo", {})
    if not isinstance(info, dict) or any(
        not isinstance(info.get(k, ""), str) for k in ("Name", "Revision", "Units")
    ):
        raise ValueError("Template name, revision and units must be text.")
    if info.get("Units", UNITS) != UNITS:
        raise ValueError("Unsupported template units; native values use mm, s, deg.")
    if "Tolerance" in attrs:
        tolerance = float(attrs["Tolerance"])
        if not math.isfinite(tolerance) or tolerance <= 0:
            raise ValueError("Template geometry tolerance must be positive and finite.")
    for key in ("SetupSheet", "PostPropertyOverrides"):
        if key in attrs and not isinstance(attrs[key], dict):
            raise ValueError("Template %s must be a settings object." % key)
    stock = attrs.get("Stock")
    if stock:
        if not isinstance(stock, dict) or stock.get("version") not in (1, "1"):
            raise ValueError("Unsupported stock template version.")
        extents = {
            "FromBase": ("xneg", "xpos", "yneg", "ypos", "zneg", "zpos"),
            "CreateBox": ("length", "width", "height"),
            "CreateCylinder": ("radius", "height"),
        }
        if stock.get("create") not in extents:
            raise ValueError("Choose model-bound, box or cylindrical template stock.")
        keys = extents[stock["create"]]
        placement = ("posX", "posY", "posZ", "rotX", "rotY", "rotZ", "rotW")
        for group in (keys, placement):
            if any(k in stock for k in group) and not all(k in stock for k in group):
                raise ValueError("Incomplete template stock dimensions or placement.")
        for key in keys:
            if key in stock:
                value = FreeCAD.Units.Quantity(stock[key]).Value
                if not math.isfinite(value) or value < 0 or (
                    stock["create"] != "FromBase" and value == 0
                ):
                    raise ValueError("Invalid template stock dimension: " + key)
        for key in placement:
            if key in stock and not math.isfinite(float(stock[key])):
                raise ValueError("Template stock placement must be finite.")
    tools = attrs.get("ToolController", [])
    if not isinstance(tools, list):
        raise ValueError("Template tool controllers must be a list.")
    expressions = []
    for tool in tools:
        if not isinstance(tool, dict) or tool.get("version") not in (1, 2, "1", "2"):
            raise ValueError("Unsupported tool-controller template version.")
        if not isinstance(tool.get("tool"), dict) or tool["tool"].get("version") != 2:
            raise ValueError("Template requires an embedded current-format tool; re-export its tools.")
        for expr in tool.get("xengine", []):
            if not isinstance(expr, dict) or not isinstance(expr.get("expr"), str):
                raise ValueError("Invalid template tool expression.")
            expressions.append(expr["expr"])
    for key, value in attrs.get("SetupSheet", {}).items():
        if key.endswith("Expression"):
            expressions.append(value)
    for expr in expressions:
        if not isinstance(expr, str):
            raise ValueError("Template expressions must be text.")
        portable = expr.replace("${SetupSheet}.", "")
        if "#" in portable or "<<" in portable or "${" in portable or re.search(
            r"[A-Za-z_]\w*\s*\.", portable
        ):
            raise ValueError("Model-specific template expression requires remapping: " + expr)
    return copy.deepcopy(attrs)


def read(filename):
    with open(str(filename), "r", encoding="utf-8-sig") as stream:
        return validate(json.load(stream))


def review(attrs):
    """Human-readable settings inventory, including omitted/default values."""
    info = attrs.get("TemplateInfo", {})
    lines = [
        "Name: " + info.get("Name", "Legacy template (no saved name)"),
        "Revision: " + info.get("Revision", "Not recorded"),
        "Native format: 1; stored units: " + info.get("Units", UNITS + " (legacy convention)"),
        "Machine: " + (attrs.get("Machine") or "Current default; review in Job"),
        "Postprocessor: " + (attrs.get("Post") or "Current default; review in Job"),
        "Post arguments: " + (attrs.get("PostArgs") or ("None" if attrs.get("Post") else "Current default")),
        "Output: " + (attrs.get("Output") or "Current default; choose before posting"),
        "Output order: " + str(attrs.get("OrderOutputBy", "Current default")),
        "Split output: " + str(attrs.get("SplitOutput", "Current default")),
        "Geometry tolerance (mm): " + str(attrs.get("Tolerance", "Current default")),
    ]
    labels = {"Stock": "Stock rules", "ToolController": "Tools and feeds",
              "SetupSheet": "Setup defaults", "PostPropertyOverrides": "Post overrides",
              "hfeed": "Horizontal feed", "vfeed": "Vertical feed", "nr": "Tool number",
              "xengine": "Expressions", "create": "Stock type", "version": "Format",
              "expr": "Expression", "prop": "Property", "label": "Label",
              "xneg": "X negative margin", "xpos": "X positive margin",
              "yneg": "Y negative margin", "ypos": "Y positive margin",
              "zneg": "Z negative margin", "zpos": "Z positive margin",
              "speed": "Spindle speed", "dir": "Spindle direction",
              "tool": "Cutter", "parameter": "Cutter dimensions", "shape-type": "Cutter type"}

    def append(value, depth=0):
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "id" or (key == "shape" and "shape-type" in value):
                    continue
                label = labels.get(key, key)
                if isinstance(child, (dict, list)):
                    lines.append("  " * depth + label + ":")
                    append(child, depth + 1)
                else:
                    lines.append("  " * depth + label + ": " + str(child))
        elif isinstance(value, list):
            for index, child in enumerate(value, 1):
                lines.append("  " * depth + str(index) + ":")
                append(child, depth + 1)

    for key in ("Stock", "ToolController", "SetupSheet", "PostPropertyOverrides", "Fixtures"):
        if attrs.get(key):
            append({key: attrs[key]})
        elif key != "PostPropertyOverrides":
            lines.append(labels.get(key, key) + ": Current defaults")
    lines += [
        "New model links and stock are created for the selected models.",
        "Fixed stock sizes/placements may need adjustment for a different model.",
        "No operation sequence or generated toolpath is copied. Review the new job before machining.",
        "Later template-file edits do not update jobs already created.",
    ]
    return "\n".join(lines)
