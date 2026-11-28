# SPDX-License-Identifier: LGPL-2.1-or-later
"""Initialize a newly promoted result from the authored source appearance."""
from . import appearance


def copy(source, result, ref=None):
    if source.TypeId=='PartDesign::Body':source=source.Tip
    if source is None:return
    view=source.ViewObject;destination=result.ViewObject
    if hasattr(source,'Shape') and source.Shape.Faces and 'ShapeAppearance' in destination.PropertiesList:
        values=appearance.materials(source)
        if ref:
            import Part
            link,sub=ref;occurrence=link.ViewObject
            if getattr(occurrence,'OverrideMaterial',False):
                values=[appearance.clone(occurrence.ShapeMaterial) for _ in values]
            for path,color in occurrence.getElementColors().items():
                if path=='Face':continue  # Whole override already copied as a full material.
                target=link.getSubObject(path,1)
                if target is not None and target.TypeId=='PartDesign::Body':target=target.Tip
                if target!=source:continue
                element=Part.splitSubname(path)[2]
                indices=[int(element[4:])-1] if element.startswith('Face') and element[4:].isdigit() else range(len(values)) if not element else []
                for i in indices:
                    if 0<=i<len(values):values[i].DiffuseColor=color[:3];values[i].Transparency=1-color[3]
        if len(values)!=len(result.Shape.Faces):
            raise ValueError('Clone face correspondence changed while copying appearance')
        # Rigid occurrence transforms and the clone's frame conversion retain
        # native face enumeration. Copy material values, never shared wrappers.
        destination.ShapeAppearance=[appearance.clone(value) for value in values]
    for name in ('LineColor','PointColor','LineWidth','PointSize','DrawStyle'):
        if name in view.PropertiesList and name in destination.PropertiesList:
            setattr(destination,name,getattr(view,name))
