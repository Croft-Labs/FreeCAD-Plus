# SPDX-License-Identifier: LGPL-2.1-or-later
"""Prepare complete CAM simulator inputs before touching its native session."""
import hashlib
import math
import FreeCAD as App
import Part
import Path.Base.Util as Util
import Path.Dressup.Utils as Dressup
from PathScripts import PathUtils


def tr(text):
    return App.Qt.translate("CAMSimulationReview", text)


def prepare(job, operations, quality, profile):
    if job.Document != App.ActiveDocument:
        raise ValueError(tr("Activate the job document before reviewing simulation."))
    if not operations:
        raise ValueError(tr("Check at least one operation to simulate."))
    if len(set(operations)) != len(operations):
        raise ValueError(tr("An operation is selected more than once."))
    stock_obj = job.Stock
    if stock_obj is None:
        raise ValueError(tr("The job has no stock."))
    Dressup.requireCurrent(stock_obj)
    stock = stock_obj.Shape.copy()
    if stock.isNull() or not stock.isValid() or stock.Volume <= 0:
        raise ValueError(tr("Recompute a valid solid stock before simulation."))
    models = []
    for obj in job.Model.Group:
        Dressup.requireCurrent(obj)
        if not hasattr(obj, "Shape") or obj.Shape.isNull():
            raise ValueError(tr("This simulator review requires BRep model shapes."))
        models.append(obj.Shape.copy())
    available = list(job.Operations.Group)
    if any(op not in available for op in operations):
        raise ValueError(tr("A selected operation no longer belongs to this job's operation list."))
    # An open task can retain its checkbox order after the job is reordered.
    # Submission and the explicit review always follow the current saved Group.
    operations = [op for op in available if op in operations]
    tools, entries, signatures = {}, [], [stock.exportBrepToString(), str(quality)]
    for op in operations:
        if op not in available or not Util.opProperty(op, "Active"):
            raise ValueError(tr("A selected operation is inactive or no longer belongs to this job."))
        Dressup.requireCurrent(op)
        controller = Dressup.toolController(op)
        tool = controller.Tool if controller else None
        if tool is None:
            raise ValueError(tr("Missing tool for operation: ") + op.Label)
        Dressup.requireCurrent(tool)
        shape = tool.Shape
        diameter = float(tool.Diameter)
        if (shape.isNull() or not shape.isValid() or not shape.Solids
                or not math.isfinite(diameter) or diameter <= 0):
            raise ValueError(tr("Invalid cutter geometry for operation: ") + op.Label)
        number = int(controller.ToolNumber)
        if number < 0:
            raise ValueError(tr("Tool numbers must be nonnegative."))
        key = (tool.Document.Name, tool.Name, tool.ID)
        if number in tools and tools[number]["key"] != key:
            raise ValueError(tr("Different cutters share tool number %1. Assign distinct numbers before simulation.").replace("%1", str(number)))
        if number not in tools:
            points = list(profile(tool, 0.5))
            if len(points) < 4 or len(points) % 2 or not all(math.isfinite(v) for v in points):
                raise ValueError(tr("The native cutter profile is empty or invalid: ") + tool.Label)
            tools[number] = {"key": key, "number": number, "profile": points,
                             "diameter": diameter, "label": tool.Label}
            signatures += [str(key), str(number), str(diameter), repr(points), shape.exportBrepToString()]
        path = PathUtils.getPathWithPlacement(op)
        commands = list(path.Commands)
        if not commands:
            raise ValueError(tr("The selected operation has no toolpath: ") + op.Label)
        for command in commands:
            if not all(math.isfinite(value) for value in command.Parameters.values()):
                raise ValueError(tr("Non-finite toolpath coordinates or parameters: ") + op.Label)
        entries.append({"object": op, "label": op.Label, "name": op.Name,
                        "tool": number, "commands": commands})
        signatures += [str((op.Name, op.ID)), path.toGCode()]
    model = Part.makeCompound(models) if models else None
    if model is not None:
        signatures.append(model.exportBrepToString())
    signatures.append(str((job.Document.Name, job.Name, job.ID)))
    return {"job": job, "stock": stock, "model": model, "tools": list(tools.values()),
            "operations": entries, "quality": quality,
            "fingerprint": hashlib.sha256("\n".join(signatures).encode("utf-8")).hexdigest()}


def describe(review):
    box = review["stock"].BoundBox
    lines = [tr("Job: {label} [{name}]").format(label=review["job"].Label, name=review["job"].Name),
             tr("Stock: {x:.6g} x {y:.6g} x {z:.6g} mm").format(x=box.XLength,y=box.YLength,z=box.ZLength),
             tr("Quality level: %1 (display setting, not a certified tolerance)").replace("%1", str(review["quality"])),
             tr("Selected operations, in job order:")]
    for index, entry in enumerate(review["operations"], 1):
        lines.append("{}. {} [{}] - T{}, {} {}".format(index, entry["label"], entry["name"],
                     entry["tool"], len(entry["commands"]), tr("commands")))
    lines.append(tr("Cutters:"))
    for tool in review["tools"]:
        lines.append("T{}: {}, {:.6g} mm".format(tool["number"], tool["label"], tool["diameter"]))
    return "\n".join(lines)
