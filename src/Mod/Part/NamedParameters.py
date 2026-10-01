# SPDX-License-Identifier: LGPL-2.1-or-later
"""Part-owned named length/angle parameters using native expressions and properties.

Native transactions, dependency tracking and persistence own model behavior.
ParameterSetVersion identifies containers created by this bounded editor; no
custom document proxy or history/result schema is required.
"""
import FreeCAD as App


def set_length_expression(obj, property_name, expression):
    """Require an explicitly length-valued expression before native assignment.

    Deliberately bounded to App::PropertyLength. Bare numeric expressions and other
    property types need a separate UI/unit-default policy, not silent coercion.
    """
    if obj.getTypeIdOfProperty(property_name) != "App::PropertyLength":
        raise ValueError("Named parameters support length properties only")
    value = obj.evalExpression(expression)
    if getattr(value, "Unit", None) != App.Units.Quantity("1 mm").Unit:
        raise ValueError("Expression must evaluate to a length")
    obj.setExpression(property_name, expression)


def set_angle_expression(obj, property_name, expression):
    """Require an explicitly angular result; do not infer units for bare numbers."""
    if obj.getTypeIdOfProperty(property_name) != "App::PropertyAngle":
        raise ValueError("Named parameters support angle properties only")
    value = obj.evalExpression(expression)
    if getattr(value, "Unit", None) != App.Units.Quantity("1 deg").Unit:
        raise ValueError("Expression must evaluate to an angle")
    obj.setExpression(property_name, expression)


def rename_parameter(obj, old_name, new_name):
    """Atomically rename a native length/angle parameter; own the transaction.

    Native validation defines legal names and locked/dynamic-property rules.
    Abort is essential: native rename may remove an owned expression before a
    naming error is raised. Never adopt another editor's pending transaction.
    """
    doc = obj.Document
    if doc.HasPendingTransaction:
        raise ValueError("Finish the current transaction before renaming a parameter")
    if obj.getTypeIdOfProperty(old_name) not in ("App::PropertyLength", "App::PropertyAngle"):
        raise ValueError("Named parameters support length and angle parameters only")
    doc.openTransaction("Rename parameter")
    try:
        obj.renameProperty(old_name, new_name)
        doc.recompute()
        doc.commitTransaction()
    except Exception:
        doc.abortTransaction()
        doc.recompute()
        raise


def edit_parameter_expression(obj, property_name, expression):
    """Atomic edit, restricted to current native length/angle consumers.

    Readiness is object-level and includes recursive dependents and their inputs.
    Unrelated document failures do not veto the edit. No implicit recompute/repair
    is performed before opening the transaction.
    """
    doc = obj.Document
    if doc.HasPendingTransaction:
        raise ValueError("Finish the current transaction before editing a parameter")
    setters = {"App::PropertyLength": set_length_expression,
               "App::PropertyAngle": set_angle_expression}
    setter = setters.get(obj.getTypeIdOfProperty(property_name))
    if setter is None:
        raise ValueError("Named parameters support length and angle parameters only")
    affected = [obj] + list(obj.InListRecursive)
    def require_current():
        for consumer in affected:
            for dependency in [consumer] + list(consumer.OutListRecursive):
                if "Invalid" in dependency.State or "Touched" in dependency.State:
                    raise ValueError("Parameter consumer is not current: " + dependency.Label)
    require_current()
    doc.openTransaction("Edit parameter expression")
    try:
        setter(obj, property_name, expression)
        doc.recompute()
        require_current()
        doc.commitTransaction()
    except Exception:
        doc.abortTransaction()
        doc.recompute()
        raise


def create_parameter(obj, name, kind, expression, description=""):
    """Create a typed parameter atomically; parameter names use ASCII identifiers."""
    import re
    doc = obj.Document
    if doc.HasPendingTransaction:
        raise ValueError("Finish the current transaction before creating a parameter")
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
        raise ValueError("Use a parameter name starting with a letter or underscore, followed by letters, digits or underscores")
    if name in obj.PropertiesList:
        raise ValueError("A property with that name already exists")
    types = {"Length": ("App::PropertyLength", set_length_expression),
             "Angle": ("App::PropertyAngle", set_angle_expression)}
    if kind not in types:
        raise ValueError("Choose Length or Angle")
    if any("Invalid" in dep.State or "Touched" in dep.State
           for dep in [obj] + list(obj.OutListRecursive)):
        raise ValueError("Parameter object is not current")
    property_type, setter = types[kind]
    doc.openTransaction("Create parameter")
    try:
        obj.addProperty(property_type, name, "Dimensions", description)
        setter(obj, name, expression)
        doc.recompute()
        if "Invalid" in obj.State or "Touched" in obj.State:
            raise ValueError("New parameter did not recompute successfully")
        doc.commitTransaction()
    except Exception:
        doc.abortTransaction()
        doc.recompute()
        raise


def create_parameter_set(part):
    """Create an explicit native parameter container in one Part definition.

    This editor does not resolve occurrences or infer scope from active state.
    Container creation is its own undoable operation, separate from editing it.
    """
    if part.TypeId != "App::Part":
        raise ValueError("Choose an explicit Part definition, not a Body or occurrence")
    doc = part.Document
    if doc.HasPendingTransaction:
        raise ValueError("Finish the current transaction before creating a parameter set")
    doc.openTransaction("Create parameter set")
    try:
        parameters = doc.addObject("App::FeaturePython", "Parameters")
        parameters.Label = "Parameters"
        parameters.addProperty("App::PropertyInteger", "ParameterSetVersion", "Parameters",
                               "Named parameter container version")
        parameters.ParameterSetVersion = 1
        parameters.setEditorMode("ParameterSetVersion", 1)
        part.addObject(parameters)
        doc.recompute()
        doc.commitTransaction()
        return parameters
    except Exception:
        doc.abortTransaction()
        doc.recompute()
        raise


def is_parameter_set(obj):
    """Recognize only an explicitly marked, directly Part-owned container."""
    if obj is None or obj.TypeId != "App::FeaturePython":
        return False
    if "ParameterSetVersion" not in obj.PropertiesList:
        return False
    owner = obj.getParentGeoFeatureGroup()
    return (obj.getTypeIdOfProperty("ParameterSetVersion") == "App::PropertyInteger"
            and obj.ParameterSetVersion == 1 and owner is not None
            and owner.TypeId == "App::Part")
