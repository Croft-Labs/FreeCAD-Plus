# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native enclosure fixture for the bounded T13 parameter benchmark."""
from prototypes.NamedParameters import create_parameter


def make_enclosure(doc, part):
    def add(kind, name):
        obj = doc.addObject(kind, name)
        part.addObject(obj)
        return obj
    params = add("App::FeaturePython", "EnclosureParameters")
    doc.recompute()
    for name, expression in (("Width", "60 mm"), ("LidClearance", "0.5 mm"),
                             ("HoleSpacing", "30 mm")):
        create_parameter(params, name, "Length", expression)
    ref = params.Name + "."
    outer = add("Part::Box", "Outer")
    outer.setExpression("Length", ref + "Width")
    outer.Width, outer.Height = 30, 20
    inner = add("Part::Box", "Inner")
    inner.setExpression("Length", ref + "Width - 4 mm")
    inner.Width, inner.Height = 26, 18
    inner.Placement.Base = (2, 2, 2)
    shell = add("Part::Cut", "EnclosureShell")
    shell.Base, shell.Tool = outer, inner
    holes = []
    for sign in ("-", "+"):
        hole = add("Part::Cylinder", "MountingHole")
        hole.Radius, hole.Height = 2, 2
        hole.Placement.Base = (0, 15, 0)
        hole.setExpression("Placement.Base.x", "(" + ref + "Width " + sign + " " + ref + "HoleSpacing) / 2")
        holes.append(hole)
    first = add("Part::Cut", "FirstHole")
    first.Base, first.Tool = shell, holes[0]
    result = add("Part::Cut", "DrilledEnclosure")
    result.Base, result.Tool = first, holes[1]
    lid = add("Part::Box", "Lid")
    lid.Height = 2
    lid.Placement.Base = (0, 0, 22)
    lid.setExpression("Length", ref + "Width + 2 * " + ref + "LidClearance")
    lid.setExpression("Width", "30 mm + 2 * " + ref + "LidClearance")
    doc.recompute()
    for obj in (outer, inner, shell, first, *holes):
        obj.Visibility = False
    doc.recompute()
    return params, result, lid, holes
