# SPDX-License-Identifier: LGPL-2.1-or-later
"""Independent native sketches owned by a component, with explicit support."""
import FreeCAD as App
import math
import Part
import Sketcher  # Registers the native sketch type.
import ComponentModel as Model

ORIGIN_PLANES = ("XY plane", "XZ plane", "YZ plane")
BASE_PLANES = ORIGIN_PLANES + ("Selected planar face", "User plane")
PLANES = BASE_PLANES + ("Selected two edges", "Independent plane", "Create new plane")


def user_planes(component):
    return [obj for obj in Model.history(component)
            if obj.isDerivedFrom("PartDesign::Plane") or obj.isDerivedFrom("Part::Plane")
            or obj.isDerivedFrom("Part::DatumPlane")
            or (getattr(obj, "LegacyDatumSource", None) is not None
                and (obj.LegacyDatumSource.isDerivedFrom("Part::DatumPlane")
                     or obj.LegacyDatumSource.isDerivedFrom("PartDesign::Plane")))]


def check_plane(component, plane):
    if plane not in user_planes(component):
        raise ValueError("Select a user plane in the active component.")
    if "Invalid" in plane.State:
        raise ValueError("Repair the selected plane before using it.")
    source = getattr(plane, "LegacyDatumSource", plane)
    if "Invalid" in source.State:
        raise ValueError("Repair the retained plane attachment before using it.")
    if not (source.isDerivedFrom("Part::DatumPlane") or source.isDerivedFrom("PartDesign::Plane")):
        check_support(component, (plane, "Face1"))
    return plane


def origin_plane(component, name):
    role = name.split()[0] + "_Plane"
    return next(obj for obj in component.Origin.OriginFeatures if obj.Role == role)


def _attach(obj, component, plane, offset, support=None):
    if plane in ORIGIN_PLANES:
        obj.AttachmentSupport = [(origin_plane(component, plane), "")]
        obj.MapMode = "ObjectXY"
    elif plane == "User plane":
        obj.AttachmentSupport = [(check_plane(component, support), "")]
        obj.MapMode = "ObjectXY"
    elif plane == "Selected planar face":
        source, name = check_support(component, support)
        obj.AttachmentSupport = [(source, name)]
        obj.MapMode = "FlatFace"
    else:
        raise ValueError("Choose a base plane or planar face.")
    obj.AttachmentOffset = App.Placement(App.Vector(0, 0, offset), App.Rotation())


def plane_rotation(angles, directions=None):
    if directions is None:
        return App.Rotation(App.Vector(0, 0, 1), angles[2]).multiply(
            App.Rotation(App.Vector(0, 1, 0), angles[1])).multiply(
            App.Rotation(App.Vector(1, 0, 0), angles[0]))
    axis, direction, normal = directions
    if axis not in ("X", "Y") or not all(math.isfinite(v) for v in (*direction, *normal)):
        raise ValueError("Choose finite X-axis or Y-axis and Z-axis directions.")
    along, z = App.Vector(*direction), App.Vector(*normal)
    if along.Length < 1e-9 or z.Length < 1e-9:
        raise ValueError("Axis directions must be nonzero.")
    along.normalize()
    z.normalize()
    if along.cross(z).Length < 1e-9:
        raise ValueError("The in-plane direction must not be parallel to the Z-axis direction.")
    # Z defines the normal; project the selected X/Y direction onto the plane.
    return App.Rotation(along if axis == "X" else App.Vector(),
                        along if axis == "Y" else App.Vector(), z,
                        "ZXY" if axis == "X" else "ZYX")


def reference_geometry(component, reference, point=False):
    """Resolve a picked point or edge into component-local coordinates."""
    source, names = reference
    name = names[0] if isinstance(names, (list, tuple)) and names else names
    origins = component.Origin.OriginFeatures
    if source is None or (Model.owner(source) != component and source not in origins):
        raise ValueError("Choose geometry in the active component, or add a component reference first.")
    transform = component.getGlobalPlacement().inverse().multiply(source.getGlobalPlacement())
    if point and source.isDerivedFrom("App::Point") and not name:
        return transform.Base
    if not point and source.isDerivedFrom("App::Line") and not name:
        return transform.Rotation.multVec(App.Vector(1, 0, 0))
    shape = Model.current_shape(source)
    element = shape.getElement(name) if name else shape
    # Shape subelements already include the object's local placement.
    transform = transform.multiply(source.Placement.inverse())
    if point:
        if element.ShapeType != "Vertex":
            raise ValueError("Select a vertex or datum point for the projected point.")
        return transform.multVec(element.Point)
    if element.ShapeType != "Edge":
        raise ValueError("Select one edge or datum axis for the X direction.")
    direction = element.tangentAt((element.FirstParameter + element.LastParameter) / 2.)
    return transform.Rotation.multVec(direction)


def projected_frame(component, surface, origin_reference=None, axis_references=(), reverse_z=False, reverse_x=False):
    """Project component-local references onto the defined flat surface."""
    normal = surface.Rotation.multVec(App.Vector(0, 0, 1))
    normal.normalize()
    point = reference_geometry(component, origin_reference, True) if origin_reference and origin_reference[0] else App.Vector()
    origin = point - normal * ((point - surface.Base).dot(normal))
    if len(axis_references) == 2:
        along = reference_geometry(component, axis_references[1], True) - reference_geometry(component, axis_references[0], True)
    elif len(axis_references) == 1:
        along = reference_geometry(component, axis_references[0])
    elif not axis_references:
        axes = [App.Vector(1, 0, 0), App.Vector(0, 1, 0), App.Vector(0, 0, 1)]
        lengths = [(axis - normal * axis.dot(normal)).Length for axis in axes]
        along = next(axis for axis, length in zip(axes, lengths) if length >= max(lengths) - 1e-12)
    else:
        raise ValueError("Select one edge or exactly two points for X.")
    x = along - normal * along.dot(normal)
    if x.Length < 1e-9:
        raise ValueError("The selected X direction projects to zero. Choose another edge or two distinct projected points.")
    x.normalize()
    if reverse_x:
        x = -x
    if reverse_z:
        normal = -normal
    return App.Placement(origin, App.Rotation(x, normal.cross(x), normal, "ZXY"))


class ProjectedPlaneFrame(Model.PersistentProxy):
    def execute(self, obj):
        try:
            placement = projected_frame(Model.owner(obj), obj.Surface.Placement,
                                        obj.OriginReference, obj.AxisReferences, obj.ReverseZ, obj.ReverseX)
            obj.Shape = Part.makePlane(1, 1)
            obj.Placement = placement
        except Exception:
            obj.Shape = Part.Shape()
            raise


def _projected_plane(component, base, offset, support, angles, frame):
    import PartDesign
    doc = component.Document
    surface = doc.addObject("PartDesign::Plane", "PlaneSurface")
    component.addObject(surface)
    Model._identity(surface, "Internal")
    _attach(surface, component, base, offset, support)
    surface.AttachmentOffset = App.Placement(App.Vector(0, 0, offset), plane_rotation(angles))
    doc.recompute()
    if "Invalid" in surface.State:
        raise ValueError("The flat surface could not attach to the selected support.")
    # Validate before constructing the associative frame; transaction rollback owns failures.
    projected_frame(component, surface.Placement, **frame)
    helper = doc.addObject("Part::FeaturePython", "PlaneFrame")
    component.addObject(helper)
    Model._identity(helper, "Internal")
    Model._property(helper, "Link", "Surface", surface, True)
    Model._property(helper, "LinkSub", "OriginReference", frame.get("origin_reference") or (None, []))
    Model._property(helper, "LinkSubList", "AxisReferences", list(frame.get("axis_references", ())))
    Model._property(helper, "Bool", "ReverseZ", frame.get("reverse_z", False))
    Model._property(helper, "Bool", "ReverseX", frame.get("reverse_x", False))
    helper.Proxy = ProjectedPlaneFrame()
    doc.recompute()
    plane = doc.addObject("PartDesign::Plane", "Plane")
    Model.register_object(component, plane)
    plane.Label = Model.next_label(component, "Plane", plane)
    plane.AttachmentSupport = [(helper, "")]
    plane.MapMode = "ObjectXY"
    Model._property(plane, "Link", "ProjectedFrame", helper, True)
    doc.recompute()
    if "Invalid" in plane.State:
        raise ValueError("The projected plane frame could not be evaluated.")
    if App.GuiUp:
        for obj in (surface, helper):
            obj.Visibility = False
            obj.ViewObject.ShowInTree = False
    return plane


def _new_plane(component, base, offset, support, angles, origin=(0.0, 0.0), directions=None, frame=None):
    if frame is not None:
        return _projected_plane(component, base, offset, support, angles, frame)
    rotation = plane_rotation(angles, directions)
    # Reuse the native datum and attachment engine without introducing a Body.
    import PartDesign  # Registers PartDesign::Plane.
    plane = component.Document.addObject("PartDesign::Plane", "Plane")
    Model.register_object(component, plane)
    plane.Label = Model.next_label(component, "Plane", plane)
    _attach(plane, component, base, offset, support)
    plane.AttachmentOffset = App.Placement(App.Vector(origin[0], origin[1], offset), rotation)
    component.Document.recompute()
    if "Invalid" in plane.State:
        raise ValueError("The new plane could not attach to that support.")
    return plane


def create_plane(component, base="XY plane", offset=0.0, support=None,
                 angles=(0.0, 0.0, 0.0), origin=(0.0, 0.0), directions=None, frame=None):
    if not Model.is_component(component):
        raise ValueError("Choose a component for the datum plane.")
    Model.activate(component, strict=False)
    with Model.transaction(component.Document, "New Datum Plane"):
        return _new_plane(component, base, offset, support, angles, origin, directions, frame)


def check_support(component, support):
    if not support or len(support) != 2:
        raise ValueError("Select one planar face in the active component.")
    source, name = support
    if Model.owner(source) != component or getattr(source, "ComponentRole", "") not in ("Object", "Result", "Reference"):
        raise ValueError("Use a local object, or Add Reference Object before attaching to another component.")
    if not name.startswith("Face"):
        raise ValueError("Select one planar face.")
    face = Model.current_shape(source).getElement(name)
    if face.ShapeType != "Face" or not isinstance(face.Surface, Part.Plane):
        raise ValueError("Sketch support must be a planar face.")
    return source, name


def two_edge_frame(component, support, fresh=None):
    if not support or len(support) != 2 or support[0][0] != support[1][0]:
        raise ValueError("Select two different edges of one local body.")
    source = support[0][0]
    if source is None or Model.owner(source) != component or support[0][1] == support[1][1]:
        raise ValueError("Select two different edges of one local body.")
    shape = source.Shape if source == fresh else Model.current_shape(source)
    edges = [shape.getElement(name) for obj, name in support]
    if any(edge.ShapeType != "Edge" for edge in edges):
        raise ValueError("Select two edges defining one flat plane.")
    flat = Part.makeCompound(edges).findPlane()
    points = [point for edge in edges for point in edge.discretize(Number=5)]
    x = edges[0].tangentAt((edges[0].FirstParameter + edges[0].LastParameter) / 2.)
    normal = next((x.cross(point - points[0]) for point in points if x.cross(point - points[0]).Length > 1e-8), None)
    if flat is None or normal is None:
        raise ValueError("The two edges must define one plane; collinear or non-coplanar edges cannot be used.")
    normal.normalize()
    x.normalize()
    local = App.Placement(points[0], App.Rotation(x, normal.cross(x), normal, "ZXY"))
    transform = component.getGlobalPlacement().inverse().multiply(source.getGlobalPlacement()).multiply(source.Placement.inverse())
    return transform.multiply(local)


def remember_support(sketch, mode=None, references=None):
    """Keep native sketch/attacher semantics with non-blocking persistent references."""
    mode = mode or str(sketch.MapMode)
    references = sketch.AttachmentSupport if references is None else references
    values = (("LinkSubListHidden", "FrameSupport", references),
              ("String", "FrameSupportMode", mode),
              ("Placement", "SavedSketchPlacement", sketch.Placement),
              ("Placement", "SavedSupportPlacement", sketch.Placement.multiply(sketch.AttachmentOffset.inverse())),
              ("String", "FrameSupportStatus", "Following support"))
    for kind, name, value in values:
        if name not in sketch.PropertiesList:
            sketch.addProperty("App::Property" + kind, name, "Sketch frame")
        sketch.setPropertyStatus(name, "NoRecompute")
        if name.startswith("Saved") or name == "FrameSupportStatus":
            sketch.setPropertyStatus(name, "Output")
        setattr(sketch, name, value)
        sketch.setEditorMode(name, 1 if name.startswith("Saved") or name == "FrameSupportStatus" else 0)
    sketch.MapMode = "Deactivated"
    sketch.AttachmentSupport = []


def support_references(sketch):
    """References for managed frames or inherited native sketch attachments."""
    return sketch.FrameSupport if hasattr(sketch, "FrameSupport") else sketch.AttachmentSupport


def sync_support(sketch, fresh=None):
    if not hasattr(sketch, "FrameSupport") or Model.edit_suppressed(sketch):
        return
    # Native Attach Sketch/property edits are adopted rather than silently discarded.
    if str(sketch.MapMode) != "Deactivated" and sketch.AttachmentSupport:
        remember_support(sketch)
    try:
        refs = sketch.FrameSupport
        if not refs:
            raise ValueError("Support deleted")
        for source, names in refs:
            if source is None:
                raise ValueError("Support missing")
            if source == sketch or sketch in Model.geometry_dependencies(source, include_frames=True):
                raise ValueError("Support would create a circular dependency")
            dependencies = [source] + Model.geometry_dependencies(source)
            for obj in dependencies:
                if "Invalid" in obj.State or getattr(obj, "UserSuppressed", False) or getattr(obj, "ResultStatus", "Ready") != "Ready":
                    raise ValueError("Support unavailable")
            if any("Touched" in obj.State and obj != fresh for obj in dependencies):
                return  # Never replace a valid snapshot with an intermediate result.
            if hasattr(source, "Shape") and not source.isDerivedFrom("Part::Datum") and source.Shape.isNull():
                raise ValueError("Support geometry missing")
        if sketch.FrameSupportMode == "TwoEdges":
            pairs = [(obj, name) for obj, names in refs for name in names]
            base = two_edge_frame(Model.owner(sketch), pairs, fresh)
            placement = base.multiply(sketch.AttachmentOffset)
        else:
            engine = Part.AttachEngine(sketch.Attacher)
            engine.References = refs
            engine.Mode = sketch.FrameSupportMode
            engine.AttachmentOffset = App.Placement()
            engine.Reverse = sketch.MapReversed
            engine.Parameter = sketch.MapPathParameter
            base = engine.calculateAttachedPlacement(sketch.SavedSupportPlacement)
            engine.AttachmentOffset = sketch.AttachmentOffset
            placement = engine.calculateAttachedPlacement(sketch.SavedSketchPlacement)
        if not sketch.Placement.isSame(placement, 1e-10):
            sketch.Placement = placement
        if not sketch.SavedSketchPlacement.isSame(placement, 1e-10):
            sketch.SavedSketchPlacement = placement
        if not sketch.SavedSupportPlacement.isSame(base, 1e-10):
            sketch.SavedSupportPlacement = base
        if sketch.FrameSupportStatus != "Following support":
            sketch.FrameSupportStatus = "Following support"
    except (ValueError, RuntimeError, AttributeError, IndexError, Part.OCCError) as error:
        if not sketch.Placement.isSame(sketch.SavedSketchPlacement, 1e-10):
            sketch.Placement = sketch.SavedSketchPlacement
        status = "Saved frame - " + str(error)
        if sketch.FrameSupportStatus != status:
            sketch.FrameSupportStatus = status


def sync_supports(doc, fresh=None):
    for sketch in doc.Objects:
        if hasattr(sketch, "FrameSupport"):
            sync_support(sketch, fresh)


def create(component, plane="XY plane", offset=0.0, support=None,
           new_plane_base="XY plane", angles=(0.0, 0.0, 0.0), origin=(0.0, 0.0), directions=None, frame=None, follow_support=True):
    if not Model.is_component(component) or plane not in PLANES:
        raise ValueError("Choose a component and a sketch plane.")
    Model.activate(component, strict=False)
    with Model.transaction(component.Document, "New Sketch"):
        if plane == "Create new plane":
            support = _new_plane(component, new_plane_base, offset, support, angles, origin, directions, frame)
            plane, offset = "User plane", 0.0
        sketch = component.Document.addObject("Sketcher::SketchObject", "Sketch")
        Model.register_object(component, sketch)
        sketch.Label = Model.next_label(component, "Sketch", sketch)
        if plane == "Independent plane":
            sketch.Placement = App.Placement(App.Vector(origin[0], origin[1], offset), plane_rotation(angles, directions))
        elif plane == "Selected two edges":
            placement = two_edge_frame(component, support)
            sketch.AttachmentOffset = App.Placement(App.Vector(0, 0, offset), App.Rotation())
            sketch.Placement = placement.multiply(sketch.AttachmentOffset)
            if follow_support:
                remember_support(sketch, "TwoEdges", [(obj, [name]) for obj, name in support])
        else:
            _attach(sketch, component, plane, offset, support)
        component.Document.recompute()
        if "Invalid" in sketch.State:
            raise ValueError("The sketch could not attach to that support.")
        if plane != "Independent plane" and plane != "Selected two edges":
            if follow_support and plane not in ORIGIN_PLANES:
                remember_support(sketch)
            elif not follow_support:
                saved = App.Placement(sketch.Placement)
                sketch.MapMode = "Deactivated"
                sketch.AttachmentSupport = []
                sketch.Placement = saved
        component.Document.recompute()
    return sketch
