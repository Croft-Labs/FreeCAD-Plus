# SPDX-License-Identifier: LGPL-2.1-or-later
"""Plus-owned layout. Command implementations and icons belong to FreeCAD."""

DESIGN_TABS = (
    ('Home', 'PartDesignWorkbench'),
    ('Modeling', 'PartDesignWorkbench'),
    ('Sketch', 'SketcherWorkbench'),
    ('Assembly', 'AssemblyWorkbench'),
    ('Mesh', 'MeshWorkbench'),
    ('View', None),
    ('Part', 'PartWorkbench'),
    ('All Tools', None),
)
MODE_WORKBENCHES = (
    ('Draft', 'DraftWorkbench'),
    ('Drawing', 'TechDrawWorkbench'),
    ('CAM', 'CAMWorkbench'),
    ('FEM', 'FemWorkbench'),
)
COMMON = ('File', 'Edit', 'Clipboard')
VIEW = ('View', 'Individual Views')
STANDARD = COMMON + VIEW + ('Workbench', 'Macro', 'Structure', 'Help')

# Multiple commands form a split button, retaining their original native tasks.
MODELING = (
    ('Sketch', (
        ('New Sketch', 'large', ('Sketcher_NewSketch',)),
        ('Edit Sketch', 'small', ('Sketcher_EditSketch',)),
        ('Attach Sketch', 'small', ('Sketcher_MapSketch',)),
        ('Coordinate System', 'small', ('PartDesign_CoordinateSystem',
            'PartDesign_Plane', 'PartDesign_Line', 'PartDesign_Point')),
    )),
    ('Modeling', (
        ('Extrude', 'large', ('PartDesign_Pad', 'PartDesign_Pocket')),
        ('Revolve', 'large', ('PartDesign_Revolution', 'PartDesign_Groove')),
        ('Loft', 'medium', ('FreeCADPlus_Loft', 'PartDesign_AdditiveLoft', 'PartDesign_SubtractiveLoft')),
        ('Helix', 'medium', ('PartDesign_AdditiveHelix', 'PartDesign_SubtractiveHelix')),
    )),
    ('Dress-Up', (
        ('Fillet and Chamfer', 'large', ('PartDesign_Fillet', 'PartDesign_Chamfer')),
        ('Draft', 'medium', ('PartDesign_Draft',)),
        ('Shell', 'medium', ('PartDesign_Thickness',)),
    )),
    ('Surface', (
        ('Thicken', 'large', ('Plus_Thicken',)),
        ('Filling', 'small', ('Surface_Filling',)),
        ('Fill Boundary Curves', 'small', ('Surface_GeomFillSurface',)),
        ('Sections', 'small', ('Surface_Sections',)),
        ('Extend Face', 'small', ('Surface_ExtendFace',)),
        ('Curve on Mesh', 'small', ('Surface_CurveOnMesh',)),
        ('Blend Curve', 'small', ('Surface_BlendCurve',)),
    )),
    ('Transformation', (
        ('Mirror Feature', 'medium', ('PartDesign_Mirrored',)),
        ('Linear Pattern', 'medium', ('PartDesign_LinearPattern',)),
        ('Circular Pattern', 'medium', ('PartDesign_PolarPattern',)),
        ('Multi Transform', 'medium', ('PartDesign_MultiTransform',)),
    )),
    ('Primitives', (('Primitives', 'large', ('PartDesign_CompPrimitiveAdditive',)),)),
    ('Other', (
        ('Delete Face / Defeaturing', 'medium', ('PartDesign_Defeaturing',)),
        ('Clone', 'medium', ('Plus_Clone',)),
        ('Extract geometry', 'medium', ('Plus_ExtractGeometry',)),
    )),
)
