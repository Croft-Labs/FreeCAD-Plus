# SPDX-License-Identifier: LGPL-2.1-or-later
"""Plus-owned layout. Command implementations and icons belong to FreeCAD."""

DESIGN_TABS = (
    ('Home', 'PartDesignWorkbench'),
    ('Modeling', 'PartDesignWorkbench'),
    ('Sketch', 'SketcherWorkbench'),
    ('Surface', 'SurfaceWorkbench'),
    ('Assembly', 'AssemblyWorkbench'),
    ('Mesh', 'MeshWorkbench'),
    ('View', None),
    ('Part', 'PartWorkbench'),
    ('More', None),
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
        ('Loft', 'medium', ('PartDesign_AdditiveLoft', 'PartDesign_SubtractiveLoft')),
        ('Helix', 'medium', ('PartDesign_AdditiveHelix', 'PartDesign_SubtractiveHelix')),
    )),
    ('Dress-Up', (
        ('Fillet and Chamfer', 'large', ('PartDesign_Fillet', 'PartDesign_Chamfer')),
        ('Draft', 'medium', ('PartDesign_Draft',)),
        ('Shell / Thickness', 'medium', ('PartDesign_Thickness',)),
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
        ('Add Reference Object', 'medium', ()),
    )),
)
