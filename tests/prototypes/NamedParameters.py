# SPDX-License-Identifier: LGPL-2.1-or-later
"""Test-only dimensional assignment boundary for roadmap 10.8.

Not installed, not a parameter editor/API or a document schema. Native expressions,
transactions and persistence remain responsible for dependencies and cycle checks.
"""
import FreeCAD as App


def set_length_expression(obj, property_name, expression):
    """Require an explicitly length-valued expression before native assignment.

    Deliberately bounded to App::PropertyLength. Bare numeric expressions and other
    property types need a separate UI/unit-default policy, not silent coercion.
    """
    if obj.getTypeIdOfProperty(property_name) != "App::PropertyLength":
        raise ValueError("Prototype supports length properties only")
    value = obj.evalExpression(expression)
    if getattr(value, "Unit", None) != App.Units.Quantity("1 mm").Unit:
        raise ValueError("Expression must evaluate to a length")
    obj.setExpression(property_name, expression)


def set_angle_expression(obj, property_name, expression):
    """Require an explicitly angular result; do not infer units for bare numbers."""
    if obj.getTypeIdOfProperty(property_name) != "App::PropertyAngle":
        raise ValueError("Prototype supports angle properties only")
    value = obj.evalExpression(expression)
    if getattr(value, "Unit", None) != App.Units.Quantity("1 deg").Unit:
        raise ValueError("Expression must evaluate to an angle")
    obj.setExpression(property_name, expression)
