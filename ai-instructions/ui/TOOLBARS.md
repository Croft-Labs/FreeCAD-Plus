# FreeCAD Plus toolbar reference

Classic inventory comes first, followed by the implemented Plus layout, the change map, and the function catalog. Each command has its own row. Reference icons are displayed at **11 Ã— 11 px**, approximately one third of the previous 32 px renders.

The Plus layout implements the owner's revised direction and completes the incomplete outline with native command placements. **The revised Design Home, Modeling, Sketch and Assembly layouts are source-validated and awaits the next build; the October 2 audit executable retains its prior layout.** Native IDs, icons and command descriptions come from the inspected payload. [UI rules](../UI_UX_SPEC.md#toolbar-ui-styles) govern interaction; [WORK_STATE](../WORK_STATE.md) records implementation/build acceptance.

- [Classic toolbars](#classic-toolbars)
- [Plus UI target layout](#plus-ui-target-layout)
- [Changes and retained access](#changes-and-retained-access)
- [Complete function catalog](#complete-toolbar-buttonfunction-catalog)

## Design Move Components

The Design Assembly group includes **Move Components** (`Std_MoveComponents`).
The Part Tree instance context menu opens the same task. Its ordered workflow
dropdown starts with Translate; the remaining five workflows await their queued
implementations. See [Move Components](../UI_UX_SPEC.md#move-components).

## Classic toolbars

Recorded upstream source: `b9609745048b`. Native metadata: application `6be8eda4246a`. Conditional/edit-only toolbars are included; they are not all shown simultaneously. Shared desktop groups are listed once. Classic location mappings record the prior audit layout; the revised Design Home section below governs current source placement. Removed Home actions retain specialist tabs or native menus.

### All workbenches â€” shared desktop

#### File

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Std_New.png" width="11" height="11" alt="New Document"> [New Document](#button-std_new) | All | Common toolbar |
| <img src="toolbar-icons/Std_Open.png" width="11" height="11" alt="Openâ€¦"> [Openâ€¦](#button-std_open) | All | Common toolbar |
| <img src="toolbar-icons/Std_Save.png" width="11" height="11" alt="Save"> [Save](#button-std_save) | All | Common toolbar |

#### Edit

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Undo.png" width="11" height="11" alt="Undo"> [Undo](#button-std_undo) | All | Common toolbar |
| <img src="toolbar-icons/Std_Redo.png" width="11" height="11" alt="Redo"> [Redo](#button-std_redo) | All | Common toolbar |
| <img src="toolbar-icons/Std_Refresh.png" width="11" height="11" alt="Recompute"> [Recompute](#button-std_refresh) | All | Common toolbar |

#### Clipboard

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Cut.png" width="11" height="11" alt="Cut"> [Cut](#button-std_cut) | All | Common toolbar |
| <img src="toolbar-icons/Std_Copy.png" width="11" height="11" alt="Copy"> [Copy](#button-std_copy) | All | Common toolbar |
| <img src="toolbar-icons/Std_Paste.png" width="11" height="11" alt="Paste"> [Paste](#button-std_paste) | All | Common toolbar |

#### Workbench

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Workbench.png" width="11" height="11" alt="Assembly"> [Workbench selector](#button-std_workbench) | All | Mode selector |

#### Macro

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> [Record Macro](#button-std_dlgmacrorecord) | Design | Home |
| <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> [Macros](#button-std_dlgmacroexecute) | Design | Home |
| <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> [Execute Macro](#button-std_dlgmacroexecutedirect) | Design | Home |

#### View

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Std_ViewFitAll.png" width="11" height="11" alt="Fit All"> [Fit All](#button-std_viewfitall) | All | View |
| <img src="toolbar-icons/Std_ViewFitSelection.png" width="11" height="11" alt="Fit Selection"> [Fit Selection](#button-std_viewfitselection) | All | View |
| <img src="toolbar-icons/Std_ViewGroup.png" width="11" height="11" alt="Isometric"> [Isometric](#button-std_viewgroup) | All | View |
| <img src="toolbar-icons/Std_AlignToSelection.png" width="11" height="11" alt="Align to Selection"> [Align to Selection](#button-std_aligntoselection) | All | View |
| <img src="toolbar-icons/Std_DrawStyle.png" width="11" height="11" alt="As Is"> [As Is](#button-std_drawstyle) | All | View |
| <img src="toolbar-icons/Part_SelectFilter.png" width="11" height="11" alt="Vertex Selection"> [Vertex Selection](#button-part_selectfilter) | All | View |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | All | View |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | All | View |

#### Individual Views

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Std_ViewIsometric.png" width="11" height="11" alt="Isometric"> [Isometric](#button-std_viewisometric) | All | View |
| <img src="toolbar-icons/Std_ViewFront.png" width="11" height="11" alt="Front"> [Front](#button-std_viewfront) | All | View |
| <img src="toolbar-icons/Std_ViewTop.png" width="11" height="11" alt="Top"> [Top](#button-std_viewtop) | All | View |
| <img src="toolbar-icons/Std_ViewRight.png" width="11" height="11" alt="Right"> [Right](#button-std_viewright) | All | View |
| <img src="toolbar-icons/Std_ViewRear.png" width="11" height="11" alt="Rear"> [Rear](#button-std_viewrear) | All | View |
| <img src="toolbar-icons/Std_ViewBottom.png" width="11" height="11" alt="Bottom"> [Bottom](#button-std_viewbottom) | All | View |
| <img src="toolbar-icons/Std_ViewLeft.png" width="11" height="11" alt="Left"> [Left](#button-std_viewleft) | All | View |

#### Structure

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [New Part](#button-std_part) | Design | Home |
| <img src="toolbar-icons/Part_Datums.png" width="11" height="11" alt="Coordinate System"> [Datums](#button-part_datums) | Design | Home â†’ Coordinate System dropdown |
| <img src="toolbar-icons/Std_Group.png" width="11" height="11" alt="New Group"> [New Group](#button-std_group) | Design | Home |
| <img src="toolbar-icons/Std_LinkActions.png" width="11" height="11" alt="Make Link"> [Make Link](#button-std_linkactions) | Design | Home |
| <img src="toolbar-icons/Std_VarSet.png" width="11" height="11" alt="Variable Set"> [Variable Set](#button-std_varset) | Design | Home |

#### Help

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> [What's This?](#button-std_whatsthis) | Design | Home |

<a id="workbench-partdesignworkbench"></a>
### Part Design workbench

Definition: [`src/Mod/PartDesign/Gui/Workbench.cpp`](../../../src/Mod/PartDesign/Gui/Workbench.cpp).

#### Part Design Helper Features

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/PartDesign_Body.png" width="11" height="11" alt="New Body"> [New Body](#button-partdesign_body) | Design | Modeling |
| <img src="toolbar-icons/PartDesign_CompSketches.png" width="11" height="11" alt="New Sketch"> [New Sketch](#button-partdesign_compsketches) | Design | Modeling |
| <img src="toolbar-icons/Sketcher_ValidateSketch.png" width="11" height="11" alt="Validate Sketch"> [Validate Sketch](#button-sketcher_validatesketch) | Design | Modeling; Sketch |
| <img src="toolbar-icons/Part_CheckGeometry.png" width="11" height="11" alt="Check Geometry"> [Check Geometry](#button-part_checkgeometry) | Design / Part / OpenSCAD | Modeling; Tools |
| <img src="toolbar-icons/PartDesign_SubShapeBinder.png" width="11" height="11" alt="Sub-Shape Binder"> [Sub-Shape Binder](#button-partdesign_subshapebinder) | Design | Modeling |
| <img src="toolbar-icons/PartDesign_Clone.png" width="11" height="11" alt="Clone"> [Clone](#button-partdesign_clone) | Design | Modeling |

#### Part Design Modeling Features

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/PartDesign_Pad.png" width="11" height="11" alt="Pad"> [Pad](#button-partdesign_pad) | Design | Home / Modeling â†’ Extrude |
| <img src="toolbar-icons/PartDesign_Revolution.png" width="11" height="11" alt="Revolve"> [Revolve](#button-partdesign_revolution) | Design | Home; Modeling |
| <img src="toolbar-icons/PartDesign_AdditiveLoft.png" width="11" height="11" alt="Additive Loft"> [Additive Loft](#button-partdesign_additiveloft) | Design | Modeling |
| <img src="toolbar-icons/PartDesign_AdditivePipe.png" width="11" height="11" alt="Additive Pipe"> [Additive Pipe](#button-partdesign_additivepipe) | Design | Modeling |
| <img src="toolbar-icons/PartDesign_AdditiveHelix.png" width="11" height="11" alt="Additive Helix"> [Additive Helix](#button-partdesign_additivehelix) | Design | Modeling |
| <img src="toolbar-icons/PartDesign_CompPrimitiveAdditive.png" width="11" height="11" alt="Additive Box"> [Additive Box](#button-partdesign_compprimitiveadditive) | Design | Modeling |
| <img src="toolbar-icons/PartDesign_Pocket.png" width="11" height="11" alt="Pocket"> [Pocket](#button-partdesign_pocket) | Design | Home / Modeling â†’ Extrude |
| <img src="toolbar-icons/PartDesign_Hole.png" width="11" height="11" alt="Hole"> [Hole](#button-partdesign_hole) | Design | Modeling |
| <img src="toolbar-icons/PartDesign_Groove.png" width="11" height="11" alt="Groove"> [Groove](#button-partdesign_groove) | Design | Modeling |
| <img src="toolbar-icons/PartDesign_SubtractiveLoft.png" width="11" height="11" alt="Subtractive Loft"> [Subtractive Loft](#button-partdesign_subtractiveloft) | Design | Modeling |
| <img src="toolbar-icons/PartDesign_SubtractivePipe.png" width="11" height="11" alt="Subtractive Pipe"> [Subtractive Pipe](#button-partdesign_subtractivepipe) | Design | Modeling |
| <img src="toolbar-icons/PartDesign_SubtractiveHelix.png" width="11" height="11" alt="Subtractive Helix"> [Subtractive Helix](#button-partdesign_subtractivehelix) | Design | Modeling |
| <img src="toolbar-icons/PartDesign_CompPrimitiveSubtractive.png" width="11" height="11" alt="Subtractive Box"> [Subtractive Box](#button-partdesign_compprimitivesubtractive) | Design | Modeling |
| <img src="toolbar-icons/PartDesign_Boolean.png" width="11" height="11" alt="Boolean Operation"> [Boolean Operation](#button-partdesign_boolean) | Design | Modeling |

#### Part Design Dress-Up Features

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/PartDesign_Fillet.png" width="11" height="11" alt="Fillet"> [Fillet](#button-partdesign_fillet) | Design | Home; Modeling |
| <img src="toolbar-icons/PartDesign_Chamfer.png" width="11" height="11" alt="Chamfer"> [Chamfer](#button-partdesign_chamfer) | Design | Modeling |
| <img src="toolbar-icons/PartDesign_Draft.png" width="11" height="11" alt="Draft"> [Draft](#button-partdesign_draft) | Design | Modeling |
| <img src="toolbar-icons/PartDesign_Thickness.png" width="11" height="11" alt="Thickness"> [Thickness](#button-partdesign_thickness) | Design | Modeling |
| <img src="toolbar-icons/PartDesign_Defeaturing.png" width="11" height="11" alt="Defeaturing"> [Defeaturing](#button-partdesign_defeaturing) | Design | Modeling |

#### Part Design Transformation Features

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/PartDesign_Mirrored.png" width="11" height="11" alt="Mirror"> [Mirror](#button-partdesign_mirrored) | Design | Modeling |
| <img src="toolbar-icons/PartDesign_LinearPattern.png" width="11" height="11" alt="Linear Pattern"> [Linear Pattern](#button-partdesign_linearpattern) | Design | Home / Modeling â†’ Pattern task |
| <img src="toolbar-icons/PartDesign_PolarPattern.png" width="11" height="11" alt="Polar Pattern"> [Polar Pattern](#button-partdesign_polarpattern) | Design | Home / Modeling â†’ Pattern task |
| <img src="toolbar-icons/PartDesign_CircularPattern.png" width="11" height="11" alt="Circular Pattern"> [Circular Pattern](#button-partdesign_circularpattern) | Design | Home; Modeling |
| <img src="toolbar-icons/PartDesign_PathPattern.png" width="11" height="11" alt="Path Pattern"> [Path Pattern](#button-partdesign_pathpattern) | Design | Home; Modeling |
| <img src="toolbar-icons/PartDesign_PointPattern.png" width="11" height="11" alt="Point Pattern"> [Point Pattern](#button-partdesign_pointpattern) | Design | Home; Modeling |
| <img src="toolbar-icons/PartDesign_MultiTransform.png" width="11" height="11" alt="Multi-Transform"> [Multi-Transform](#button-partdesign_multitransform) | Design | Modeling |

<a id="workbench-partworkbench"></a>
### Part workbench

Definition: [`src/Mod/Part/Gui/Workbench.cpp`](../../../src/Mod/Part/Gui/Workbench.cpp).

#### Solids

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Part_Box.png" width="11" height="11" alt="Cube"> [Cube](#button-part_box) | Part | Tools |
| <img src="toolbar-icons/Part_Cylinder.png" width="11" height="11" alt="Cylinder"> [Cylinder](#button-part_cylinder) | Part | Tools |
| <img src="toolbar-icons/Part_Sphere.png" width="11" height="11" alt="Sphere"> [Sphere](#button-part_sphere) | Part | Tools |
| <img src="toolbar-icons/Part_Cone.png" width="11" height="11" alt="Cone"> [Cone](#button-part_cone) | Part | Tools |
| <img src="toolbar-icons/Part_Torus.png" width="11" height="11" alt="Torus"> [Torus](#button-part_torus) | Part | Tools |
| <img src="toolbar-icons/Part_Tube.png" width="11" height="11" alt="Tube"> [Tube](#button-part_tube) | Part | Tools |
| <img src="toolbar-icons/Part_Primitives.png" width="11" height="11" alt="Primitive"> [Primitive](#button-part_primitives) | Part / OpenSCAD | Tools |
| <img src="toolbar-icons/Part_Builder.png" width="11" height="11" alt="Shape Builder"> [Shape Builder](#button-part_builder) | Part / OpenSCAD | Tools |

#### Part Tools

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Sketcher_NewSketch.png" width="11" height="11" alt="New Sketch"> [New Sketch](#button-sketcher_newsketch) | Design / Part | Sketch; Tools |
| <img src="toolbar-icons/Part_Extrude.png" width="11" height="11" alt="Extrude"> [Extrude](#button-part_extrude) | Part / OpenSCAD | Tools |
| <img src="toolbar-icons/Part_Revolve.png" width="11" height="11" alt="Revolve"> [Revolve](#button-part_revolve) | Part / OpenSCAD | Tools |
| <img src="toolbar-icons/Part_Mirror.png" width="11" height="11" alt="Mirror"> [Mirror](#button-part_mirror) | Part | Tools |
| <img src="toolbar-icons/Part_Scale.png" width="11" height="11" alt="Scale"> [Scale](#button-part_scale) | Part | Tools |
| <img src="toolbar-icons/Part_Fillet.png" width="11" height="11" alt="Fillet"> [Fillet](#button-part_fillet) | Part | Tools |
| <img src="toolbar-icons/Part_Chamfer.png" width="11" height="11" alt="Chamfer"> [Chamfer](#button-part_chamfer) | Part | Tools |
| <img src="toolbar-icons/Part_MakeFace.png" width="11" height="11" alt="Face From Wires"> [Face From Wires](#button-part_makeface) | Part | Tools |
| <img src="toolbar-icons/Part_RuledSurface.png" width="11" height="11" alt="Ruled Surface"> [Ruled Surface](#button-part_ruledsurface) | Part | Tools |
| <img src="toolbar-icons/Part_Loft.png" width="11" height="11" alt="Loft"> [Loft](#button-part_loft) | Part | Tools |
| <img src="toolbar-icons/Part_Sweep.png" width="11" height="11" alt="Sweep"> [Sweep](#button-part_sweep) | Part | Tools |
| <img src="toolbar-icons/Part_Section.png" width="11" height="11" alt="Section"> [Section](#button-part_section) | Part | Tools |
| <img src="toolbar-icons/Part_CrossSections.png" width="11" height="11" alt="Cross-Sections"> [Cross-Sections](#button-part_crosssections) | Part | Tools |
| <img src="toolbar-icons/Part_CompOffset.png" width="11" height="11" alt="3D Offset"> [3D Offset](#button-part_compoffset) | Part | Tools |
| <img src="toolbar-icons/Part_Thickness.png" width="11" height="11" alt="Thickness"> [Thickness](#button-part_thickness) | Part | Tools |
| <img src="toolbar-icons/Part_ProjectionOnSurface.png" width="11" height="11" alt="Project on Surface"> [Project on Surface](#button-part_projectiononsurface) | Part | Tools |
| <img src="toolbar-icons/Part_ColorPerFace.png" width="11" height="11" alt="Appearance per Face"> [Appearance per Face](#button-part_colorperface) | Part | Tools |

#### Boolean Tools

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Part_CompCompoundTools.png" width="11" height="11" alt="Compound"> [Compound](#button-part_compcompoundtools) | Part | Tools |
| <img src="toolbar-icons/Part_Boolean.png" width="11" height="11" alt="Boolean Operation"> [Boolean Operation](#button-part_boolean) | Part | Tools |
| <img src="toolbar-icons/Part_Cut.png" width="11" height="11" alt="Cut"> [Cut](#button-part_cut) | Part / OpenSCAD | Tools |
| <img src="toolbar-icons/Part_Fuse.png" width="11" height="11" alt="Union"> [Union](#button-part_fuse) | Part / OpenSCAD | Tools |
| <img src="toolbar-icons/Part_Common.png" width="11" height="11" alt="Intersection"> [Intersection](#button-part_common) | Part / OpenSCAD | Tools |
| <img src="toolbar-icons/Part_CompJoinFeatures.png" width="11" height="11" alt="Connect Shapes"> [Connect Shapes](#button-part_compjoinfeatures) | Part | Tools |
| <img src="toolbar-icons/Part_CompSplitFeatures.png" width="11" height="11" alt="Boolean Fragments"> [Boolean Fragments](#button-part_compsplitfeatures) | Part | Tools |
| <img src="toolbar-icons/Part_CheckGeometry.png" width="11" height="11" alt="Check Geometry"> [Check Geometry](#button-part_checkgeometry) | Design / Part / OpenSCAD | Modeling; Tools |
| <img src="toolbar-icons/Part_Defeaturing.png" width="11" height="11" alt="Defeaturing"> [Defeaturing](#button-part_defeaturing) | Part | Tools |

<a id="workbench-sketcherworkbench"></a>
### Sketcher workbench

Definition: [`src/Mod/Sketcher/Gui/Workbench.cpp`](../../../src/Mod/Sketcher/Gui/Workbench.cpp).

#### Sketcher

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Sketcher_NewSketch.png" width="11" height="11" alt="New Sketch"> [New Sketch](#button-sketcher_newsketch) | Design / Part | Sketch; Tools |
| <img src="toolbar-icons/Sketcher_EditSketch.png" width="11" height="11" alt="Edit Sketch"> [Edit Sketch](#button-sketcher_editsketch) | Design | Home; Sketch |
| <img src="toolbar-icons/Sketcher_MapSketch.png" width="11" height="11" alt="Attach Sketch"> [Attach Sketch](#button-sketcher_mapsketch) | Design | Home; Sketch |
| <img src="toolbar-icons/Sketcher_ReorientSketch.png" width="11" height="11" alt="Reorient Sketch"> [Reorient Sketch](#button-sketcher_reorientsketch) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_ValidateSketch.png" width="11" height="11" alt="Validate Sketch"> [Validate Sketch](#button-sketcher_validatesketch) | Design | Modeling; Sketch |
| <img src="toolbar-icons/Sketcher_MergeSketches.png" width="11" height="11" alt="Merge Sketches"> [Merge Sketches](#button-sketcher_mergesketches) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_MirrorSketch.png" width="11" height="11" alt="Mirror Sketch"> [Mirror Sketch](#button-sketcher_mirrorsketch) | Design | Sketch |

#### Edit Mode

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Sketcher_LeaveSketch.png" width="11" height="11" alt="Leave Sketch"> [Leave Sketch](#button-sketcher_leavesketch) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_ViewSketch.png" width="11" height="11" alt="Align View to Sketch"> [Align View to Sketch](#button-sketcher_viewsketch) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_ViewSection.png" width="11" height="11" alt="Toggle Section View"> [Toggle Section View](#button-sketcher_viewsection) | Design | Sketch |

#### Geometries

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Sketcher_CreatePoint.png" width="11" height="11" alt="Point"> [Point](#button-sketcher_createpoint) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_CompLine.png" width="11" height="11" alt="Polyline"> [Polyline](#button-sketcher_compline) | Design | Home; Sketch |
| <img src="toolbar-icons/Sketcher_CompCreateArc.png" width="11" height="11" alt="Arc From Center"> [Arc From Center](#button-sketcher_compcreatearc) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_CompCreateConic.png" width="11" height="11" alt="Circle From Center"> [Circle From Center](#button-sketcher_compcreateconic) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_CompCreateRectangles.png" width="11" height="11" alt="Rectangle"> [Rectangle](#button-sketcher_compcreaterectangles) | Design | Home; Sketch |
| <img src="toolbar-icons/Sketcher_CompCreateRegularPolygon.png" width="11" height="11" alt="Triangle"> [Triangle](#button-sketcher_compcreateregularpolygon) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_CompSlot.png" width="11" height="11" alt="Slot"> [Slot](#button-sketcher_compslot) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_CompCreateBSpline.png" width="11" height="11" alt="B-Spline"> [B-Spline](#button-sketcher_compcreatebspline) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_CreateText.png" width="11" height="11" alt="Text (Experimental)"> [Text (Experimental)](#button-sketcher_createtext) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_ToggleConstruction.png" width="11" height="11" alt="Toggle Construction Geometry"> [Toggle Construction Geometry](#button-sketcher_toggleconstruction) | Design | Home; Sketch |

#### Constraints

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Sketcher_CompDimensionTools.png" width="11" height="11" alt="Dimension"> [Dimension](#button-sketcher_compdimensiontools) | Menus / shortcuts | No dedicated ribbon button |
| <img src="toolbar-icons/Sketcher_ConstrainCoincidentUnified.png" width="11" height="11" alt="Coincident Constraint"> [Coincident Constraint](#button-sketcher_constraincoincidentunified) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_CompHorVer.png" width="11" height="11" alt="Horizontal Constraint"> [Horizontal Constraint](#button-sketcher_comphorver) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_ConstrainParallel.png" width="11" height="11" alt="Parallel Constraint"> [Parallel Constraint](#button-sketcher_constrainparallel) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_ConstrainPerpendicular.png" width="11" height="11" alt="Perpendicular Constraint"> [Perpendicular Constraint](#button-sketcher_constrainperpendicular) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_ConstrainTangent.png" width="11" height="11" alt="Tangent/Collinear Constraint"> [Tangent/Collinear Constraint](#button-sketcher_constraintangent) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_ConstrainEqual.png" width="11" height="11" alt="Equal Constraint"> [Equal Constraint](#button-sketcher_constrainequal) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_ConstrainSymmetric.png" width="11" height="11" alt="Symmetric Constraint"> [Symmetric Constraint](#button-sketcher_constrainsymmetric) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_ConstrainBlock.png" width="11" height="11" alt="Block Constraint"> [Block Constraint](#button-sketcher_constrainblock) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_ConstrainGroup.png" width="11" height="11" alt="Group Constraint (Development preview)"> [Group Constraint (Development preview)](#button-sketcher_constraingroup) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_CompToggleConstraints.png" width="11" height="11" alt="Toggle Driving/Reference Constraints"> [Toggle Driving/Reference Constraints](#button-sketcher_comptoggleconstraints) | Design | Sketch |

#### Sketcher Tools

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Sketcher_CompCreateFillets.png" width="11" height="11" alt="Fillet"> [Fillet](#button-sketcher_compcreatefillets) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_CompCurveEdition.png" width="11" height="11" alt="Trim Edge"> [Trim Edge](#button-sketcher_compcurveedition) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_CompExternal.png" width="11" height="11" alt="External Projection"> [External Projection](#button-sketcher_compexternal) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_CarbonCopy.png" width="11" height="11" alt="Carbon Copy"> [Carbon Copy](#button-sketcher_carboncopy) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_Translate.png" width="11" height="11" alt="Move / Array Transform"> [Move / Array Transform](#button-sketcher_translate) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_Rotate.png" width="11" height="11" alt="Rotate / Polar Transform"> [Rotate / Polar Transform](#button-sketcher_rotate) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_Scale.png" width="11" height="11" alt="Scale"> [Scale](#button-sketcher_scale) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_Offset.png" width="11" height="11" alt="Offset"> [Offset](#button-sketcher_offset) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_Symmetry.png" width="11" height="11" alt="Mirror"> [Mirror](#button-sketcher_symmetry) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_RemoveAxesAlignment.png" width="11" height="11" alt="Remove Axes Alignment"> [Remove Axes Alignment](#button-sketcher_removeaxesalignment) | Design | Sketch |

#### B-Spline Tools

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Sketcher_BSplineConvertToNURBS.png" width="11" height="11" alt="Geometry to B-Spline"> [Geometry to B-Spline](#button-sketcher_bsplineconverttonurbs) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_BSplineIncreaseDegree.png" width="11" height="11" alt="Increase B-Spline Degree"> [Increase B-Spline Degree](#button-sketcher_bsplineincreasedegree) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_BSplineDecreaseDegree.png" width="11" height="11" alt="Decrease B-Spline Degree"> [Decrease B-Spline Degree](#button-sketcher_bsplinedecreasedegree) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_CompModifyKnotMultiplicity.png" width="11" height="11" alt="Increase knot multiplicity"> [Increase knot multiplicity](#button-sketcher_compmodifyknotmultiplicity) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_BSplineInsertKnot.png" width="11" height="11" alt="Insert Knot"> [Insert Knot](#button-sketcher_bsplineinsertknot) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_JoinCurves.png" width="11" height="11" alt="Join Curves"> [Join Curves](#button-sketcher_joincurves) | Design | Sketch |

#### Visual Helpers

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Sketcher_SelectConstraints.png" width="11" height="11" alt="Select Associated Constraints"> [Select Associated Constraints](#button-sketcher_selectconstraints) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_SelectElementsAssociatedWithConstraints.png" width="11" height="11" alt="Select Associated Geometry"> [Select Associated Geometry](#button-sketcher_selectelementsassociatedwithconstraints) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_ArcOverlay.png" width="11" height="11" alt="Toggle Circular Helper for Arcs"> [Toggle Circular Helper for Arcs](#button-sketcher_arcoverlay) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_CompBSplineShowHideGeometryInformation.png" width="11" height="11" alt="Toggle B-Spline Degree"> [Toggle B-Spline Degree](#button-sketcher_compbsplineshowhidegeometryinformation) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_RestoreInternalAlignmentGeometry.png" width="11" height="11" alt="Toggle Internal Geometry"> [Toggle Internal Geometry](#button-sketcher_restoreinternalalignmentgeometry) | Design | Sketch |
| <img src="toolbar-icons/Sketcher_SwitchVirtualSpace.png" width="11" height="11" alt="Switch Virtual Space"> [Switch Virtual Space](#button-sketcher_switchvirtualspace) | Design | Sketch |

<a id="workbench-surfaceworkbench"></a>
### Surface workbench

Definition: [`src/Mod/Surface/Gui/Workbench.cpp`](../../../src/Mod/Surface/Gui/Workbench.cpp).

#### Surface

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Surface_Filling.png" width="11" height="11" alt="Filling"> [Filling](#button-surface_filling) | Design | Home; Surface |
| <img src="toolbar-icons/Surface_GeomFillSurface.png" width="11" height="11" alt="Fill Boundary Curves"> [Fill Boundary Curves](#button-surface_geomfillsurface) | Design | Home; Surface |
| <img src="toolbar-icons/Surface_Sections.png" width="11" height="11" alt="Sections"> [Sections](#button-surface_sections) | Design | Surface |
| <img src="toolbar-icons/Surface_ExtendFace.png" width="11" height="11" alt="Extend Face"> [Extend Face](#button-surface_extendface) | Design | Home; Surface |
| <img src="toolbar-icons/Surface_CurveOnMesh.png" width="11" height="11" alt="Curve on Mesh"> [Curve on Mesh](#button-surface_curveonmesh) | Design | Surface |
| <img src="toolbar-icons/Surface_BlendCurve.png" width="11" height="11" alt="Blend Curve"> [Blend Curve](#button-surface_blendcurve) | Design | Surface |

<a id="workbench-meshworkbench"></a>
### Mesh workbench

Definition: [`src/Mod/Mesh/Gui/Workbench.cpp`](../../../src/Mod/Mesh/Gui/Workbench.cpp).

#### Mesh Tools

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Mesh_Import.png" width="11" height="11" alt="Import Meshâ€¦"> [Import Meshâ€¦](#button-mesh_import) | Design | Home; Mesh |
| <img src="toolbar-icons/Mesh_Export.png" width="11" height="11" alt="Export Meshâ€¦"> [Export Meshâ€¦](#button-mesh_export) | Design | Mesh |
| <img src="toolbar-icons/Mesh_FromPartShape.png" width="11" height="11" alt="Mesh From Shape"> [Mesh From Shape](#button-mesh_frompartshape) | Design | Home; Mesh |
| <img src="toolbar-icons/Mesh_BuildRegularSolid.png" width="11" height="11" alt="Regular Solid"> [Regular Solid](#button-mesh_buildregularsolid) | Design | Mesh |

#### Mesh Modify

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Mesh_HarmonizeNormals.png" width="11" height="11" alt="Harmonize Normals"> [Harmonize Normals](#button-mesh_harmonizenormals) | Design | Mesh |
| <img src="toolbar-icons/Mesh_FlipNormals.png" width="11" height="11" alt="Flip Normals"> [Flip Normals](#button-mesh_flipnormals) | Design | Mesh |
| <img src="toolbar-icons/Mesh_FillupHoles.png" width="11" height="11" alt="Fill Holes"> [Fill Holes](#button-mesh_fillupholes) | Design | Mesh |
| <img src="toolbar-icons/Mesh_FillInteractiveHole.png" width="11" height="11" alt="Close Hole"> [Close Hole](#button-mesh_fillinteractivehole) | Design | Mesh |
| <img src="toolbar-icons/Mesh_AddFacet.png" width="11" height="11" alt="Add Triangle"> [Add Triangle](#button-mesh_addfacet) | Design | Mesh |
| <img src="toolbar-icons/Mesh_RemoveComponents.png" width="11" height="11" alt="Remove Components"> [Remove Components](#button-mesh_removecomponents) | Design | Mesh |
| <img src="toolbar-icons/Mesh_Smoothing.png" width="11" height="11" alt="Smooth"> [Smooth](#button-mesh_smoothing) | Design | Mesh |
| <img src="toolbar-icons/Mesh_RemeshGmsh.png" width="11" height="11" alt="Refinement"> [Refinement](#button-mesh_remeshgmsh) | Design | Mesh |
| <img src="toolbar-icons/Mesh_Decimating.png" width="11" height="11" alt="Decimate"> [Decimate](#button-mesh_decimating) | Design | Mesh |
| <img src="toolbar-icons/Mesh_Scale.png" width="11" height="11" alt="Scale"> [Scale](#button-mesh_scale) | Design | Mesh |

#### Mesh Boolean

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Mesh_Union.png" width="11" height="11" alt="Union"> [Union](#button-mesh_union) | Design | Mesh |
| <img src="toolbar-icons/Mesh_Intersection.png" width="11" height="11" alt="Intersection"> [Intersection](#button-mesh_intersection) | Design | Mesh |
| <img src="toolbar-icons/Mesh_Difference.png" width="11" height="11" alt="Difference"> [Difference](#button-mesh_difference) | Design | Mesh |

#### Mesh Cutting

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Mesh_PolyCut.png" width="11" height="11" alt="Cut"> [Cut](#button-mesh_polycut) | Design | Mesh |
| <img src="toolbar-icons/Mesh_PolyTrim.png" width="11" height="11" alt="Trim"> [Trim](#button-mesh_polytrim) | Design | Mesh |
| <img src="toolbar-icons/Mesh_TrimByPlane.png" width="11" height="11" alt="Trim With Plane"> [Trim With Plane](#button-mesh_trimbyplane) | Design | Mesh |
| <img src="toolbar-icons/Mesh_SectionByPlane.png" width="11" height="11" alt="Section From Plane"> [Section From Plane](#button-mesh_sectionbyplane) | Design | Mesh |
| <img src="toolbar-icons/Mesh_CrossSections.png" width="11" height="11" alt="Cross-Sections"> [Cross-Sections](#button-mesh_crosssections) | Design | Mesh |

#### Mesh Segmentation

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Mesh_Merge.png" width="11" height="11" alt="Merge"> [Merge](#button-mesh_merge) | Design | Mesh |
| <img src="toolbar-icons/Mesh_SplitComponents.png" width="11" height="11" alt="Split by Components"> [Split by Components](#button-mesh_splitcomponents) | Design | Mesh |
| <img src="toolbar-icons/Mesh_Segmentation.png" width="11" height="11" alt="Segmentation"> [Segmentation](#button-mesh_segmentation) | Design | Mesh |
| <img src="toolbar-icons/Mesh_SegmentationBestFit.png" width="11" height="11" alt="Segmentation From Best-Fit Surfaces"> [Segmentation From Best-Fit Surfaces](#button-mesh_segmentationbestfit) | Design | Mesh |

#### Mesh Analyze

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Mesh_Evaluation.png" width="11" height="11" alt="Evaluate and Repair"> [Evaluate and Repair](#button-mesh_evaluation) | Design | Home; Mesh |
| <img src="toolbar-icons/Mesh_EvaluateFacet.png" width="11" height="11" alt="Face Info"> [Face Info](#button-mesh_evaluatefacet) | Design | Mesh |
| <img src="toolbar-icons/Mesh_VertexCurvature.png" width="11" height="11" alt="Curvature Plot"> [Curvature Plot](#button-mesh_vertexcurvature) | Design | Mesh |
| <img src="toolbar-icons/Mesh_CurvatureInfo.png" width="11" height="11" alt="Curvature Info"> [Curvature Info](#button-mesh_curvatureinfo) | Design | Mesh |
| <img src="toolbar-icons/Mesh_EvaluateSolid.png" width="11" height="11" alt="Evaluate Solid"> [Evaluate Solid](#button-mesh_evaluatesolid) | Design | Mesh |
| <img src="toolbar-icons/Mesh_BoundingBox.png" width="11" height="11" alt="Bounding Box Info"> [Bounding Box Info](#button-mesh_boundingbox) | Design | Mesh |

<a id="workbench-draftworkbench"></a>
### Draft workbench

Definition: [`src/Mod/Draft/InitGui.py`](../../../src/Mod/Draft/InitGui.py).

#### Draft Creation

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Draft_Line.png" width="11" height="11" alt="Line"> [Line](#button-draft_line) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Wire.png" width="11" height="11" alt="Polyline"> [Polyline](#button-draft_wire) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Fillet.png" width="11" height="11" alt="Fillet"> [Fillet](#button-draft_fillet) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_ArcTools.png" width="11" height="11" alt="Arc"> [Arc](#button-draft_arctools) | Draft | Tools |
| <img src="toolbar-icons/Draft_Circle.png" width="11" height="11" alt="Circle"> [Circle](#button-draft_circle) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Ellipse.png" width="11" height="11" alt="Ellipse"> [Ellipse](#button-draft_ellipse) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Rectangle.png" width="11" height="11" alt="Rectangle"> [Rectangle](#button-draft_rectangle) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Polygon.png" width="11" height="11" alt="Polygon"> [Polygon](#button-draft_polygon) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_BSpline.png" width="11" height="11" alt="B-Spline"> [B-Spline](#button-draft_bspline) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_BezierTools.png" width="11" height="11" alt="Cubic BÃ©zier Curve"> [Cubic BÃ©zier Curve](#button-draft_beziertools) | Draft | Tools |
| <img src="toolbar-icons/Draft_Point.png" width="11" height="11" alt="Point"> [Point](#button-draft_point) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Facebinder.png" width="11" height="11" alt="Facebinder"> [Facebinder](#button-draft_facebinder) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_ShapeString.png" width="11" height="11" alt="Shape From Text"> [Shape From Text](#button-draft_shapestring) | Draft | Tools |
| <img src="toolbar-icons/Draft_Hatch.png" width="11" height="11" alt="Hatch"> [Hatch](#button-draft_hatch) | Draft / BIM | Tools |

#### Draft Annotation

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Draft_Text.png" width="11" height="11" alt="Text"> [Text](#button-draft_text) | Draft | Tools |
| <img src="toolbar-icons/Draft_Dimension.png" width="11" height="11" alt="Dimension"> [Dimension](#button-draft_dimension) | Draft | Tools |
| <img src="toolbar-icons/Draft_Label.png" width="11" height="11" alt="Label"> [Label](#button-draft_label) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_AnnotationStyleEditor.png" width="11" height="11" alt="Annotation Styles"> [Annotation Styles](#button-draft_annotationstyleeditor) | Draft / BIM | Tools |

#### Draft Modification

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Draft_Move.png" width="11" height="11" alt="Move"> [Move](#button-draft_move) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Rotate.png" width="11" height="11" alt="Rotate"> [Rotate](#button-draft_rotate) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Scale.png" width="11" height="11" alt="Scale"> [Scale](#button-draft_scale) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Mirror.png" width="11" height="11" alt="Mirror"> [Mirror](#button-draft_mirror) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Offset.png" width="11" height="11" alt="Offset"> [Offset](#button-draft_offset) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Trimex.png" width="11" height="11" alt="Trimex"> [Trimex](#button-draft_trimex) | Draft | Tools |
| <img src="toolbar-icons/Draft_Stretch.png" width="11" height="11" alt="Stretch"> [Stretch](#button-draft_stretch) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Clone.png" width="11" height="11" alt="Clone"> [Clone](#button-draft_clone) | Draft | Tools |
| <img src="toolbar-icons/Draft_ArrayTools.png" width="11" height="11" alt="Array"> [Array](#button-draft_arraytools) | Draft | Tools |
| <img src="toolbar-icons/Draft_Edit.png" width="11" height="11" alt="Edit"> [Edit](#button-draft_edit) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_SubelementHighlight.png" width="11" height="11" alt="Highlight Subelements"> [Highlight Subelements](#button-draft_subelementhighlight) | Draft | Tools |
| <img src="toolbar-icons/Draft_Join.png" width="11" height="11" alt="Join"> [Join](#button-draft_join) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Split.png" width="11" height="11" alt="Split"> [Split](#button-draft_split) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Upgrade.png" width="11" height="11" alt="Upgrade"> [Upgrade](#button-draft_upgrade) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Downgrade.png" width="11" height="11" alt="Downgrade"> [Downgrade](#button-draft_downgrade) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_WireToBSpline.png" width="11" height="11" alt="Convert Wire/B-Spline"> [Convert Wire/B-Spline](#button-draft_wiretobspline) | Draft | Tools |
| <img src="toolbar-icons/Draft_Draft2Sketch.png" width="11" height="11" alt="Draft to Sketch"> [Draft to Sketch](#button-draft_draft2sketch) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Slope.png" width="11" height="11" alt="Set Slope"> [Set Slope](#button-draft_slope) | Draft | Tools |
| <img src="toolbar-icons/Draft_FlipDimension.png" width="11" height="11" alt="Flip Dimension"> [Flip Dimension](#button-draft_flipdimension) | Draft | Tools |
| <img src="toolbar-icons/Draft_Shape2DView.png" width="11" height="11" alt="Shape 2D View"> [Shape 2D View](#button-draft_shape2dview) | Draft | Tools |

#### Draft Utility

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Draft_LayerManager.png" width="11" height="11" alt="Manage Layers"> [Manage Layers](#button-draft_layermanager) | Draft | Tools |
| <img src="toolbar-icons/Draft_AddNamedGroup.png" width="11" height="11" alt="New Named Group"> [New Named Group](#button-draft_addnamedgroup) | Draft | Tools |
| <img src="toolbar-icons/Draft_SelectGroup.png" width="11" height="11" alt="Select Group"> [Select Group](#button-draft_selectgroup) | Draft | Tools |
| <img src="toolbar-icons/Draft_AddToLayer.png" width="11" height="11" alt="Add to Layer"> [Add to Layer](#button-draft_addtolayer) | Draft | Tools |
| <img src="toolbar-icons/Draft_AddToGroup.png" width="11" height="11" alt="Add to Group"> [Add to Group](#button-draft_addtogroup) | Draft | Tools |
| <img src="toolbar-icons/Draft_AddConstruction.png" width="11" height="11" alt="Add to Construction Group"> [Add to Construction Group](#button-draft_addconstruction) | Draft | Tools |
| <img src="toolbar-icons/Draft_ToggleDisplayMode.png" width="11" height="11" alt="Toggle Wireframe"> [Toggle Wireframe](#button-draft_toggledisplaymode) | Draft | Tools |
| <img src="toolbar-icons/Draft_WorkingPlaneProxy.png" width="11" height="11" alt="Working Plane Proxy"> [Working Plane Proxy](#button-draft_workingplaneproxy) | Draft | Tools |

#### Draft Snap

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Draft_Snap_Lock.png" width="11" height="11" alt="Snap Lock"> [Snap Lock](#button-draft_snap_lock) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Endpoint.png" width="11" height="11" alt="Snap Endpoint"> [Snap Endpoint](#button-draft_snap_endpoint) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Midpoint.png" width="11" height="11" alt="Snap Midpoint"> [Snap Midpoint](#button-draft_snap_midpoint) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Center.png" width="11" height="11" alt="Snap Center"> [Snap Center](#button-draft_snap_center) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Angle.png" width="11" height="11" alt="Snap Angle"> [Snap Angle](#button-draft_snap_angle) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Intersection.png" width="11" height="11" alt="Snap Intersection"> [Snap Intersection](#button-draft_snap_intersection) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Perpendicular.png" width="11" height="11" alt="Snap Perpendicular"> [Snap Perpendicular](#button-draft_snap_perpendicular) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Extension.png" width="11" height="11" alt="Snap Extension"> [Snap Extension](#button-draft_snap_extension) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Parallel.png" width="11" height="11" alt="Snap Parallel"> [Snap Parallel](#button-draft_snap_parallel) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Special.png" width="11" height="11" alt="Snap Special"> [Snap Special](#button-draft_snap_special) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Near.png" width="11" height="11" alt="Snap Near"> [Snap Near](#button-draft_snap_near) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Ortho.png" width="11" height="11" alt="Snap Ortho"> [Snap Ortho](#button-draft_snap_ortho) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Grid.png" width="11" height="11" alt="Snap Grid"> [Snap Grid](#button-draft_snap_grid) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_WorkingPlane.png" width="11" height="11" alt="Snap Working Plane"> [Snap Working Plane](#button-draft_snap_workingplane) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Dimensions.png" width="11" height="11" alt="Snap Dimensions"> [Snap Dimensions](#button-draft_snap_dimensions) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_ToggleGrid.png" width="11" height="11" alt="Toggle Grid"> [Toggle Grid](#button-draft_togglegrid) | Draft / BIM | Tools |

<a id="workbench-assemblyworkbench"></a>
### Assembly workbench

Definition: [`src/Mod/Assembly/InitGui.py`](../../../src/Mod/Assembly/InitGui.py).

#### Assembly

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Assembly_CreateAssembly.png" width="11" height="11" alt="New Assembly"> [New Assembly](#button-assembly_createassembly) | Design / Assembly | Home; Assembly; Tools |
| <img src="toolbar-icons/Assembly_Insert.png" width="11" height="11" alt="Insert Component"> [Insert Component](#button-assembly_insert) | Design / Assembly | Home; Assembly; Tools |
| <img src="toolbar-icons/Part_LinkArrays.png" width="11" height="11" alt="Circular Link Array"> [Circular Link Array](#button-part_linkarrays) | Design / Assembly | Assembly; Tools |
| <img src="toolbar-icons/Assembly_SolveAssembly.png" width="11" height="11" alt="Solve Assembly"> [Solve Assembly](#button-assembly_solveassembly) | Design / Assembly | Home; Assembly; Tools |
| <img src="toolbar-icons/Assembly_CreateView.png" width="11" height="11" alt="Exploded View"> [Exploded View](#button-assembly_createview) | Design / Assembly | Assembly; Tools |
| <img src="toolbar-icons/Assembly_CreateSnapshot.png" width="11" height="11" alt="Snapshot"> [Snapshot](#button-assembly_createsnapshot) | Design / Assembly | Assembly; Tools |
| <img src="toolbar-icons/Assembly_CreateSimulation.png" width="11" height="11" alt="Simulation"> [Simulation](#button-assembly_createsimulation) | Design / Assembly | Assembly; Tools |
| <img src="toolbar-icons/Assembly_CreateBom.png" width="11" height="11" alt="Bill of Materials"> [Bill of Materials](#button-assembly_createbom) | Design / Assembly | Assembly; Tools |

#### Assembly Joints

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Assembly_ToggleGrounded.png" width="11" height="11" alt="Toggle Grounded"> [Toggle Grounded](#button-assembly_togglegrounded) | Design / Assembly | Assembly; Tools |
| <img src="toolbar-icons/Assembly_CreateJointRigidGroup.png" width="11" height="11" alt="Create Rigid Group"> [Create Rigid Group](#button-assembly_createjointrigidgroup) | Design / Assembly | Home; Assembly; Tools |
| <img src="toolbar-icons/Assembly_CreateJointFixed.png" width="11" height="11" alt="Fixed Joint"> [Fixed Joint](#button-assembly_createjointfixed) | Design / Assembly | Home; Assembly; Tools |
| <img src="toolbar-icons/Assembly_CreateJointRevolute.png" width="11" height="11" alt="Revolute Joint"> [Revolute Joint](#button-assembly_createjointrevolute) | Design / Assembly | Home; Assembly; Tools |
| <img src="toolbar-icons/Assembly_CreateJointCylindrical.png" width="11" height="11" alt="Cylindrical Joint"> [Cylindrical Joint](#button-assembly_createjointcylindrical) | Design / Assembly | Home; Assembly; Tools |
| <img src="toolbar-icons/Assembly_CreateJointSlider.png" width="11" height="11" alt="Slider Joint"> [Slider Joint](#button-assembly_createjointslider) | Design / Assembly | Home; Assembly; Tools |
| <img src="toolbar-icons/Assembly_CreateJointBall.png" width="11" height="11" alt="Ball Joint"> [Ball Joint](#button-assembly_createjointball) | Design / Assembly | Home; Assembly; Tools |
| <img src="toolbar-icons/Assembly_CreateJointDistance.png" width="11" height="11" alt="Distance Joint"> [Distance Joint](#button-assembly_createjointdistance) | Design / Assembly | Home; Assembly; Tools |
| <img src="toolbar-icons/Assembly_CreateJointParallel.png" width="11" height="11" alt="Parallel Joint"> [Parallel Joint](#button-assembly_createjointparallel) | Design / Assembly | Home; Assembly; Tools |
| <img src="toolbar-icons/Assembly_CreateJointPerpendicular.png" width="11" height="11" alt="Perpendicular Joint"> [Perpendicular Joint](#button-assembly_createjointperpendicular) | Design / Assembly | Home; Assembly; Tools |
| <img src="toolbar-icons/Assembly_CreateJointAngle.png" width="11" height="11" alt="Angle Joint"> [Angle Joint](#button-assembly_createjointangle) | Design / Assembly | Home; Assembly; Tools |
| <img src="toolbar-icons/Assembly_CreateJointRackPinion.png" width="11" height="11" alt="Rack and Pinion Joint"> [Rack and Pinion Joint](#button-assembly_createjointrackpinion) | Design / Assembly | Home; Assembly; Tools |
| <img src="toolbar-icons/Assembly_CreateJointScrew.png" width="11" height="11" alt="Screw Joint"> [Screw Joint](#button-assembly_createjointscrew) | Design / Assembly | Home; Assembly; Tools |
| <img src="toolbar-icons/Assembly_CreateJointGearBelt.png" width="11" height="11" alt="Gears Joint"> [Gears Joint](#button-assembly_createjointgearbelt) | Design / Assembly | Assembly; Tools |

<a id="workbench-camworkbench"></a>
### CAM workbench

Definition: [`src/Mod/CAM/InitGui.py`](../../../src/Mod/CAM/InitGui.py).

#### Project Setup

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/CAM_Job.png" width="11" height="11" alt="New Job"> [New Job](#button-cam_job) | CAM | Tools |
| <img src="toolbar-icons/CAM_Workplane.png" width="11" height="11" alt="Work Plane"> [Work Plane](#button-cam_workplane) | CAM | Tools |
| <img src="toolbar-icons/CAM_Sanity.png" width="11" height="11" alt="Sanity Check"> [Sanity Check](#button-cam_sanity) | CAM | Tools |
| <img src="toolbar-icons/CAM_PostTools.png" width="11" height="11" alt="Post Process"> [Post Process](#button-cam_posttools) | CAM | Tools |

#### Tool Commands

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/CAM_SimTools.png" width="11" height="11" alt="CAM Simulator"> [CAM Simulator](#button-cam_simtools) | CAM | Tools |
| <img src="toolbar-icons/CAM_Inspect.png" width="11" height="11" alt="Inspect Toolpath"> [Inspect Toolpath](#button-cam_inspect) | CAM | Tools |
| <img src="toolbar-icons/CAM_SelectLoop.png" width="11" height="11" alt="Finish Selecting Loop"> [Finish Selecting Loop](#button-cam_selectloop) | CAM | Tools |
| <img src="toolbar-icons/CAM_OpActiveToggle.png" width="11" height="11" alt="Toggle Operation"> [Toggle Operation](#button-cam_opactivetoggle) | CAM | Tools |
| <img src="toolbar-icons/CAM_ToolBitDock.png" width="11" height="11" alt="Add Toolbitâ€¦"> [Add Toolbitâ€¦](#button-cam_toolbitdock) | CAM | Tools |

#### New Operations

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/CAM_Profile.png" width="11" height="11" alt="Profile"> [Profile](#button-cam_profile) | CAM | Tools |
| <img src="toolbar-icons/CAM_Pocket_Shape.png" width="11" height="11" alt="Pocket Shape"> [Pocket Shape](#button-cam_pocket_shape) | CAM | Tools |
| <img src="toolbar-icons/CAM_MillFacing.png" width="11" height="11" alt="Mill Facing"> [Mill Facing](#button-cam_millfacing) | CAM | Tools |
| <img src="toolbar-icons/CAM_Helix.png" width="11" height="11" alt="Helix"> [Helix](#button-cam_helix) | CAM | Tools |
| <img src="toolbar-icons/CAM_Adaptive.png" width="11" height="11" alt="Adaptive"> [Adaptive](#button-cam_adaptive) | CAM | Tools |
| <img src="toolbar-icons/CAM_Slot.png" width="11" height="11" alt="Slot"> [Slot](#button-cam_slot) | CAM | Tools |
| <img src="toolbar-icons/CAM_DrillingTools.png" width="11" height="11" alt="Drilling"> [Drilling](#button-cam_drillingtools) | CAM | Tools |
| <img src="toolbar-icons/CAM_EngraveTools.png" width="11" height="11" alt="Engrave"> [Engrave](#button-cam_engravetools) | CAM | Tools |

#### Path Modification

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/CAM_OperationCopy.png" width="11" height="11" alt="Copy Operation"> [Copy Operation](#button-cam_operationcopy) | CAM | Tools |
| <img src="toolbar-icons/CAM_Array.png" width="11" height="11" alt="Array"> [Array](#button-cam_array) | CAM | Tools |
| <img src="toolbar-icons/CAM_SimpleCopy.png" width="11" height="11" alt="Simple Copy"> [Simple Copy](#button-cam_simplecopy) | CAM | Tools |
| <img src="toolbar-icons/CAM_DressupTools.png" width="11" height="11" alt="Array"> [Array](#button-cam_dressuptools) | CAM | Tools |

<a id="workbench-techdrawworkbench"></a>
### TechDraw workbench

Definition: [`src/Mod/TechDraw/Gui/Workbench.cpp`](../../../src/Mod/TechDraw/Gui/Workbench.cpp).

#### TechDraw Pages

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_PageDefault.png" width="11" height="11" alt="New Page"> [New Page](#button-techdraw_pagedefault) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_PageTemplate.png" width="11" height="11" alt="New Page From Template"> [New Page From Template](#button-techdraw_pagetemplate) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_FillTemplateFields.png" width="11" height="11" alt="Update Template Fields"> [Update Template Fields](#button-techdraw_filltemplatefields) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_RedrawPage.png" width="11" height="11" alt="Redraw Page"> [Redraw Page](#button-techdraw_redrawpage) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_PrintAll.png" width="11" height="11" alt="Print All Pages"> [Print All Pages](#button-techdraw_printall) | TechDraw | Tools |

#### TechDraw Views

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_View.png" width="11" height="11" alt="New View"> [New View](#button-techdraw_view) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_BrokenView.png" width="11" height="11" alt="Broken View"> [Broken View](#button-techdraw_brokenview) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_ActiveView.png" width="11" height="11" alt="Active View"> [Active View](#button-techdraw_activeview) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_SectionGroup.png" width="11" height="11" alt="Section View"> [Section View](#button-techdraw_sectiongroup) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_DetailView.png" width="11" height="11" alt="Detail View"> [Detail View](#button-techdraw_detailview) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_DraftView.png" width="11" height="11" alt="Draft View"> [Draft View](#button-techdraw_draftview) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_SpreadsheetView.png" width="11" height="11" alt="Spreadsheet View"> [Spreadsheet View](#button-techdraw_spreadsheetview) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_ClipGroup.png" width="11" height="11" alt="Clip Group"> [Clip Group](#button-techdraw_clipgroup) | TechDraw | Tools |

#### TechDraw Stacking

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_StackGroup.png" width="11" height="11" alt="Stack Top"> [Stack Top](#button-techdraw_stackgroup) | TechDraw | Tools |

#### TechDraw Dimensions

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_Dimension.png" width="11" height="11" alt="Dimension"> [Dimension](#button-techdraw_dimension) | Menus / shortcuts | No dedicated ribbon button |
| <img src="toolbar-icons/TechDraw_CompDimensionTools.png" width="11" height="11" alt="Dimension"> [Dimension](#button-techdraw_compdimensiontools) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_LengthDimension.png" width="11" height="11" alt="Length Dimension"> [Length Dimension](#button-techdraw_lengthdimension) | Menus / shortcuts | No dedicated ribbon button |
| <img src="toolbar-icons/TechDraw_HorizontalDimension.png" width="11" height="11" alt="Horizontal Length Dimension"> [Horizontal Length Dimension](#button-techdraw_horizontaldimension) | Menus / shortcuts | No dedicated ribbon button |
| <img src="toolbar-icons/TechDraw_VerticalDimension.png" width="11" height="11" alt="Vertical Length Dimension"> [Vertical Length Dimension](#button-techdraw_verticaldimension) | Menus / shortcuts | No dedicated ribbon button |
| <img src="toolbar-icons/TechDraw_RadiusDimension.png" width="11" height="11" alt="Radius Dimension"> [Radius Dimension](#button-techdraw_radiusdimension) | Menus / shortcuts | No dedicated ribbon button |
| <img src="toolbar-icons/TechDraw_DiameterDimension.png" width="11" height="11" alt="Diameter Dimension"> [Diameter Dimension](#button-techdraw_diameterdimension) | Menus / shortcuts | No dedicated ribbon button |
| <img src="toolbar-icons/TechDraw_AngleDimension.png" width="11" height="11" alt="Angle Dimension"> [Angle Dimension](#button-techdraw_angledimension) | Menus / shortcuts | No dedicated ribbon button |
| <img src="toolbar-icons/TechDraw_3PtAngleDimension.png" width="11" height="11" alt="Angle Dimension From 3 Points"> [Angle Dimension From 3 Points](#button-techdraw_3ptangledimension) | Menus / shortcuts | No dedicated ribbon button |
| <img src="toolbar-icons/TechDraw_AreaDimension.png" width="11" height="11" alt="Area Annotation"> [Area Annotation](#button-techdraw_areadimension) | Menus / shortcuts | No dedicated ribbon button |
| <img src="toolbar-icons/TechDraw_ExtentGroup.png" width="11" height="11" alt="Horizontal extent"> [Horizontal extent](#button-techdraw_extentgroup) | Menus / shortcuts | No dedicated ribbon button |
| <img src="toolbar-icons/TechDraw_Balloon.png" width="11" height="11" alt="Balloon Annotation"> [Balloon Annotation](#button-techdraw_balloon) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_AxoLengthDimension.png" width="11" height="11" alt="Axonometric Length Dimension"> [Axonometric Length Dimension](#button-techdraw_axolengthdimension) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_DimensionRepair.png" width="11" height="11" alt="Repair Dimension References"> [Repair Dimension References](#button-techdraw_dimensionrepair) | TechDraw | Tools |

#### TechDraw Attributes

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_ExtensionSelectLineAttributes.png" width="11" height="11" alt="Select Line Attributes, Cascade Spacing and Delta Distance"> [Select Line Attributes, Cascade Spacing and Delta Distance](#button-techdraw_extensionselectlineattributes) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_ExtensionChangeLineAttributes.png" width="11" height="11" alt="Change Line Attributes"> [Change Line Attributes](#button-techdraw_extensionchangelineattributes) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_ExtensionExtendShortenLineGroup.png" width="11" height="11" alt="Extend Line"> [Extend Line](#button-techdraw_extensionextendshortenlinegroup) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_ExtensionLockUnlockView.png" width="11" height="11" alt="Toggle View Lock"> [Toggle View Lock](#button-techdraw_extensionlockunlockview) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_ExtensionPositionSectionView.png" width="11" height="11" alt="Position Section View"> [Position Section View](#button-techdraw_extensionpositionsectionview) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_ExtensionAreaAnnotation.png" width="11" height="11" alt="Area Annotation"> [Area Annotation](#button-techdraw_extensionareaannotation) | Menus / shortcuts | No dedicated ribbon button |
| <img src="toolbar-icons/TechDraw_ExtensionArcLengthAnnotation.png" width="11" height="11" alt="Arc Length Annotation"> [Arc Length Annotation](#button-techdraw_extensionarclengthannotation) | Menus / shortcuts | No dedicated ribbon button |
| <img src="toolbar-icons/TechDraw_ExtensionCustomizeFormat.png" width="11" height="11" alt="Customize Format Label"> [Customize Format Label](#button-techdraw_extensioncustomizeformat) | TechDraw | Tools |

#### TechDraw Centerlines

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_ExtensionCircleCenterLinesGroup.png" width="11" height="11" alt="Circle Centerlines"> [Circle Centerlines](#button-techdraw_extensioncirclecenterlinesgroup) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_ExtensionThreadsGroup.png" width="11" height="11" alt="Cosmetic Thread Hole Side View"> [Cosmetic Thread Hole Side View](#button-techdraw_extensionthreadsgroup) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_CommandVertexCreationGroup.png" width="11" height="11" alt="Cosmetic Intersection Vertices"> [Cosmetic Intersection Vertices](#button-techdraw_commandvertexcreationgroup) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_ExtensionDrawCirclesGroup.png" width="11" height="11" alt="Cosmetic 1 Point Circle"> [Cosmetic 1 Point Circle](#button-techdraw_extensiondrawcirclesgroup) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_ExtensionLinePPGroup.png" width="11" height="11" alt="Cosmetic Parallel Line"> [Cosmetic Parallel Line](#button-techdraw_extensionlineppgroup) | TechDraw | Tools |

#### TechDraw Extend Dimensions

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_ExtensionCreateChainDimensionGroup.png" width="11" height="11" alt="Horizontal Chain Dimension"> [Horizontal Chain Dimension](#button-techdraw_extensioncreatechaindimensiongroup) | Menus / shortcuts | No dedicated ribbon button |
| <img src="toolbar-icons/TechDraw_ExtensionCreateCoordDimensionGroup.png" width="11" height="11" alt="Horizontal Coordinate Dimension"> [Horizontal Coordinate Dimension](#button-techdraw_extensioncreatecoorddimensiongroup) | Menus / shortcuts | No dedicated ribbon button |
| <img src="toolbar-icons/TechDraw_ExtensionChamferDimensionGroup.png" width="11" height="11" alt="Horizontal Chamfer Dimension"> [Horizontal Chamfer Dimension](#button-techdraw_extensionchamferdimensiongroup) | Menus / shortcuts | No dedicated ribbon button |
| <img src="toolbar-icons/TechDraw_ExtensionCreateLengthArc.png" width="11" height="11" alt="Arc Length Dimension"> [Arc Length Dimension](#button-techdraw_extensioncreatelengtharc) | Menus / shortcuts | No dedicated ribbon button |
| <img src="toolbar-icons/TechDraw_ExtensionInsertPrefixGroup.png" width="11" height="11" alt="Insert &#x27;âŒ€&#x27; Prefix"> [Insert 'âŒ€' Prefix](#button-techdraw_extensioninsertprefixgroup) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_ExtensionIncreaseDecreaseGroup.png" width="11" height="11" alt="Increase Decimal Places"> [Increase Decimal Places](#button-techdraw_extensionincreasedecreasegroup) | TechDraw | Tools |

#### TechDraw File Access

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_ExportPageSVG.png" width="11" height="11" alt="Export Page as SVG"> [Export Page as SVG](#button-techdraw_exportpagesvg) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_ExportPageDXF.png" width="11" height="11" alt="Export Page as DXF"> [Export Page as DXF](#button-techdraw_exportpagedxf) | TechDraw | Tools |

#### TechDraw Decoration

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_ToggleFrame.png" width="11" height="11" alt="Toggle View Frames"> [Toggle View Frames](#button-techdraw_toggleframe) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_Hatch.png" width="11" height="11" alt="Image Hatch"> [Image Hatch](#button-techdraw_hatch) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_GeometricHatch.png" width="11" height="11" alt="Geometric Hatch"> [Geometric Hatch](#button-techdraw_geometrichatch) | TechDraw | Tools |

#### TechDraw Annotation

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_RichTextAnnotation.png" width="11" height="11" alt="Rich Text Annotation"> [Rich Text Annotation](#button-techdraw_richtextannotation) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_LeaderLine.png" width="11" height="11" alt="Leader Line"> [Leader Line](#button-techdraw_leaderline) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_CosmeticVertexGroup.png" width="11" height="11" alt="Cosmetic Vertex"> [Cosmetic Vertex](#button-techdraw_cosmeticvertexgroup) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_CenterLineGroup.png" width="11" height="11" alt="Centerline on Face"> [Centerline on Face](#button-techdraw_centerlinegroup) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_2PointCosmeticLine.png" width="11" height="11" alt="Cosmetic Line Through 2 Points"> [Cosmetic Line Through 2 Points](#button-techdraw_2pointcosmeticline) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_DecorateLine.png" width="11" height="11" alt="Edit Line Appearance"> [Edit Line Appearance](#button-techdraw_decorateline) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_ShowAll.png" width="11" height="11" alt="Toggle Edge Visibility"> [Toggle Edge Visibility](#button-techdraw_showall) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_WeldSymbol.png" width="11" height="11" alt="Weld Symbol"> [Weld Symbol](#button-techdraw_weldsymbol) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_SurfaceFinishSymbols.png" width="11" height="11" alt="Surface Finish Symbol"> [Surface Finish Symbol](#button-techdraw_surfacefinishsymbols) | TechDraw | Tools |
| <img src="toolbar-icons/TechDraw_HoleShaftFit.png" width="11" height="11" alt="Hole/Shaft Fit"> [Hole/Shaft Fit](#button-techdraw_holeshaftfit) | TechDraw | Tools |

<a id="workbench-femworkbench"></a>
### FEM workbench

Definition: [`src/Mod/Fem/Gui/Workbench.cpp`](../../../src/Mod/Fem/Gui/Workbench.cpp). **Source-only; unavailable in the inspected build.**

#### Model

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_Analysis.svg" width="11" height="11" alt="New Analysis"> [New Analysis](#button-fem_analysis) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialSolid.svg" width="11" height="11" alt="Solid Material"> [Solid Material](#button-fem_materialsolid) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialFluid.svg" width="11" height="11" alt="Fluid Material"> [Fluid Material](#button-fem_materialfluid) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialMechanicalNonlinear.svg" width="11" height="11" alt="Non-Linear Mechanical Material"> [Non-Linear Mechanical Material](#button-fem_materialmechanicalnonlinear) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialReinforced.svg" width="11" height="11" alt="Reinforced Material (Concrete)"> [Reinforced Material (Concrete)](#button-fem_materialreinforced) | FEM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Material_Group.svg" width="11" height="11" alt="Material Editor"> [Material Editor](#button-fem_materialeditor) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementGeometry1D.svg" width="11" height="11" alt="Beam Cross Section"> [Beam Cross Section](#button-fem_elementgeometry1d) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementRotation1D.svg" width="11" height="11" alt="Beam Rotation"> [Beam Rotation](#button-fem_elementrotation1d) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementGeometry2D.svg" width="11" height="11" alt="Shell Plate Thickness"> [Shell Plate Thickness](#button-fem_elementgeometry2d) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementFluid1D.svg" width="11" height="11" alt="Fluid Section for 1D Flow"> [Fluid Section for 1D Flow](#button-fem_elementfluid1d) | FEM | Tools |

#### Electromagnetic Boundary Conditions

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| â€” [Electromagnetic Boundary Conditions](#button-fem_compemconstraints) | FEM | Tools |

#### Fluid Boundary Conditions

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialFlowVelocity.svg" width="11" height="11" alt="Initial Flow Velocity Condition"> [Initial Flow Velocity Condition](#button-fem_constraintinitialflowvelocity) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialPressure.svg" width="11" height="11" alt="Initial Pressure Condition"> [Initial Pressure Condition](#button-fem_constraintinitialpressure) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintFlowVelocity.svg" width="11" height="11" alt="Flow Velocity Boundary Condition"> [Flow Velocity Boundary Condition](#button-fem_constraintflowvelocity) | FEM | Tools |

#### Geometrical Analysis Features

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintPlaneRotation.svg" width="11" height="11" alt="Plane Multi-Point Constraint"> [Plane Multi-Point Constraint](#button-fem_constraintplanerotation) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSectionPrint.svg" width="11" height="11" alt="Section Print Feature"> [Section Print Feature](#button-fem_constraintsectionprint) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTransform.svg" width="11" height="11" alt="Local Coordinate System"> [Local Coordinate System](#button-fem_constrainttransform) | FEM | Tools |

#### Mechanical Boundary Conditions and Loads

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintFixed.svg" width="11" height="11" alt="Fixed Boundary Condition"> [Fixed Boundary Condition](#button-fem_constraintfixed) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintRigidBody.svg" width="11" height="11" alt="Rigid Body Constraint"> [Rigid Body Constraint](#button-fem_constraintrigidbody) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintDisplacement.svg" width="11" height="11" alt="Displacement Boundary Condition"> [Displacement Boundary Condition](#button-fem_constraintdisplacement) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintContact.svg" width="11" height="11" alt="Contact Constraint"> [Contact Constraint](#button-fem_constraintcontact) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTie.svg" width="11" height="11" alt="Tie Constraint"> [Tie Constraint](#button-fem_constrainttie) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSpring.svg" width="11" height="11" alt="Spring Boundary Condition"> [Spring Boundary Condition](#button-fem_constraintspring) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintForce.svg" width="11" height="11" alt="Force Load"> [Force Load](#button-fem_constraintforce) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintPressure.svg" width="11" height="11" alt="Pressure Load"> [Pressure Load](#button-fem_constraintpressure) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintCentrif.svg" width="11" height="11" alt="Centrifugal Load"> [Centrifugal Load](#button-fem_constraintcentrif) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSelfWeight.svg" width="11" height="11" alt="Gravity Load"> [Gravity Load](#button-fem_constraintselfweight) | FEM | Tools |

#### Thermal Boundary Conditions and Loads

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialTemperature.svg" width="11" height="11" alt="Initial Temperature"> [Initial Temperature](#button-fem_constraintinitialtemperature) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintHeatflux.svg" width="11" height="11" alt="Heat Flux Load"> [Heat Flux Load](#button-fem_constraintheatflux) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTemperature.svg" width="11" height="11" alt="Temperature Boundary Condition"> [Temperature Boundary Condition](#button-fem_constrainttemperature) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintBodyHeatSource.svg" width="11" height="11" alt="Body Heat Source"> [Body Heat Source](#button-fem_constraintbodyheatsource) | FEM | Tools |

#### Mesh

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshNetgenFromShape.svg" width="11" height="11" alt="Mesh From Shape by Netgen"> [Mesh From Shape by Netgen](#button-fem_meshnetgenfromshape) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshGmshFromShape.svg" width="11" height="11" alt="Mesh From Shape by Gmsh"> [Mesh From Shape by Gmsh](#button-fem_meshgmshfromshape) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshRegion.svg" width="11" height="11" alt="Mesh Refinement"> [Mesh Refinement](#button-fem_meshregion) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshGroup.svg" width="11" height="11" alt="Mesh Group"> [Mesh Group](#button-fem_meshgroup) | FEM | Tools |
| â€” [GMSH Refinements](#button-fem_meshgmshrefinement) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_FEMMesh2Mesh.svg" width="11" height="11" alt="FEM Mesh to Mesh"> [FEM Mesh to Mesh](#button-fem_femmesh2mesh) | FEM | Tools |

#### Solve

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| â€” [Solvers](#button-fem_compsolvers) | FEM | Tools |
| â€” [Mechanical Equations](#button-fem_compmechequations) | FEM | Tools |
| â€” [Electromagnetic Equations](#button-fem_compemequations) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationFlow.svg" width="11" height="11" alt="Flow Equation"> [Flow Equation](#button-fem_equationflow) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationFlux.svg" width="11" height="11" alt="Flux Equation"> [Flux Equation](#button-fem_equationflux) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationHeat.svg" width="11" height="11" alt="Heat Equation"> [Heat Equation](#button-fem_equationheat) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverControl.svg" width="11" height="11" alt="Solver Job Control"> [Solver Job Control](#button-fem_solvercontrol) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverRun.svg" width="11" height="11" alt="Run Solver"> [Run Solver](#button-fem_solverrun) | FEM | Tools |

#### Results

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ResultsPurge.svg" width="11" height="11" alt="Purge Results"> [Purge Results](#button-fem_resultspurge) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ResultShow.svg" width="11" height="11" alt="Show Result"> [Show Result](#button-fem_resultshow) | FEM | Tools |
| <img src="../../../src/Gui/Icons/view-refresh.svg" width="11" height="11" alt="Apply Changes to Pipeline"> [Apply Changes to Pipeline](#button-fem_postapplychanges) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostPipelineFromResult.svg" width="11" height="11" alt="Post Pipeline From Result"> [Post Pipeline From Result](#button-fem_postpipelinefromresult) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostBranchFilter.svg" width="11" height="11" alt="Pipeline Branch"> [Pipeline Branch](#button-fem_postbranchfilter) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterWarp.svg" width="11" height="11" alt="Warp Filter"> [Warp Filter](#button-fem_postfilterwarp) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterClipScalar.svg" width="11" height="11" alt="Scalar Clip Filter"> [Scalar Clip Filter](#button-fem_postfilterclipscalar) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterCutFunction.svg" width="11" height="11" alt="Function Cut Filter"> [Function Cut Filter](#button-fem_postfiltercutfunction) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterClipRegion.svg" width="11" height="11" alt="Region Clip Filter"> [Region Clip Filter](#button-fem_postfilterclipregion) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterContours.svg" width="11" height="11" alt="Contours Filter"> [Contours Filter](#button-fem_postfiltercontours) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterGlyph.svg" width="11" height="11" alt="Glyph Filter"> [Glyph Filter](#button-fem_postfilterglyph) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterDataAlongLine.svg" width="11" height="11" alt="Line Clip Filter"> [Line Clip Filter](#button-fem_postfilterdataalongline) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterLinearizedStresses.svg" width="11" height="11" alt="Stress Linearization Plot"> [Stress Linearization Plot](#button-fem_postfilterlinearizedstresses) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterDataAtPoint.svg" width="11" height="11" alt="Data at Point Clip Filter"> [Data at Point Clip Filter](#button-fem_postfilterdataatpoint) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterCalculator.svg" width="11" height="11" alt="Calculator Filter"> [Calculator Filter](#button-fem_postfiltercalculator) | FEM | Tools |
| â€” [Filter Functions](#button-fem_postcreatefunctions) | FEM | Tools |
| â€” [Data Visualizations](#button-fem_postvisualization) | FEM | Tools |

#### Utilities

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ClippingPlaneAdd.svg" width="11" height="11" alt="Clipping Plane on Face"> [Clipping Plane on Face](#button-fem_clippingplaneadd) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ClippingPlaneRemoveAll.svg" width="11" height="11" alt="Remove All Clipping Planes"> [Remove All Clipping Planes](#button-fem_clippingplaneremoveall) | FEM | Tools |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FemWorkbench.svg" width="11" height="11" alt="FEM Examples"> [FEM Examples](#button-fem_examples) | FEM | Tools |

<a id="workbench-spreadsheetworkbench"></a>
### Spreadsheet workbench

Definition: [`src/Mod/Spreadsheet/Gui/Workbench.cpp`](../../../src/Mod/Spreadsheet/Gui/Workbench.cpp).

#### Spreadsheet

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Spreadsheet_CreateSheet.png" width="11" height="11" alt="New Spreadsheet"> [New Spreadsheet](#button-spreadsheet_createsheet) | Spreadsheet | Tools |
| <img src="toolbar-icons/Spreadsheet_Import.png" width="11" height="11" alt="Import Spreadsheet"> [Import Spreadsheet](#button-spreadsheet_import) | Spreadsheet | Tools |
| <img src="toolbar-icons/Spreadsheet_Export.png" width="11" height="11" alt="Export Spreadsheet"> [Export Spreadsheet](#button-spreadsheet_export) | Spreadsheet | Tools |
| <img src="toolbar-icons/Spreadsheet_MergeCells.png" width="11" height="11" alt="Merge Cells"> [Merge Cells](#button-spreadsheet_mergecells) | Spreadsheet | Tools |
| <img src="toolbar-icons/Spreadsheet_SplitCell.png" width="11" height="11" alt="Split Cell"> [Split Cell](#button-spreadsheet_splitcell) | Spreadsheet | Tools |
| <img src="toolbar-icons/Spreadsheet_AlignLeft.png" width="11" height="11" alt="Align Left"> [Align Left](#button-spreadsheet_alignleft) | Spreadsheet | Tools |
| <img src="toolbar-icons/Spreadsheet_AlignCenter.png" width="11" height="11" alt="Align Horizontal Center"> [Align Horizontal Center](#button-spreadsheet_aligncenter) | Spreadsheet | Tools |
| <img src="toolbar-icons/Spreadsheet_AlignRight.png" width="11" height="11" alt="Align Right"> [Align Right](#button-spreadsheet_alignright) | Spreadsheet | Tools |
| <img src="toolbar-icons/Spreadsheet_AlignTop.png" width="11" height="11" alt="Align Top"> [Align Top](#button-spreadsheet_aligntop) | Spreadsheet | Tools |
| <img src="toolbar-icons/Spreadsheet_AlignVCenter.png" width="11" height="11" alt="Align Vertical Center"> [Align Vertical Center](#button-spreadsheet_alignvcenter) | Spreadsheet | Tools |
| <img src="toolbar-icons/Spreadsheet_AlignBottom.png" width="11" height="11" alt="Align Bottom"> [Align Bottom](#button-spreadsheet_alignbottom) | Spreadsheet | Tools |
| <img src="toolbar-icons/Spreadsheet_StyleBold.png" width="11" height="11" alt="Bold Text"> [Bold Text](#button-spreadsheet_stylebold) | Spreadsheet | Tools |
| <img src="toolbar-icons/Spreadsheet_StyleItalic.png" width="11" height="11" alt="Italic Text"> [Italic Text](#button-spreadsheet_styleitalic) | Spreadsheet | Tools |
| <img src="toolbar-icons/Spreadsheet_StyleUnderline.png" width="11" height="11" alt="Underline Text"> [Underline Text](#button-spreadsheet_styleunderline) | Spreadsheet | Tools |
| <img src="toolbar-icons/Spreadsheet_SetAlias.png" width="11" height="11" alt="Set Alias"> [Set Alias](#button-spreadsheet_setalias) | Spreadsheet | Tools |

<a id="workbench-materialworkbench"></a>
### Material workbench

Definition: [`src/Mod/Material/Gui/Workbench.cpp`](../../../src/Mod/Material/Gui/Workbench.cpp).

#### Material

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Material_Edit.png" width="11" height="11" alt="Edit"> [Edit](#button-material_edit) | Material | Tools |

<a id="workbench-meshpartworkbench"></a>
### MeshPart workbench

Definition: [`src/Mod/MeshPart/Gui/Workbench.cpp`](../../../src/Mod/MeshPart/Gui/Workbench.cpp). **Source-only; unavailable in the inspected build.**

#### MeshPart

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Gui/Icons/preferences-general.svg" width="11" height="11" alt="Mesh From Shape"> [Mesh From Shape](#button-meshpart_mesher) | MeshPart | Tools |

<a id="workbench-pointsworkbench"></a>
### Points workbench

Definition: [`src/Mod/Points/Gui/Workbench.cpp`](../../../src/Mod/Points/Gui/Workbench.cpp). **Source-only; unavailable in the inspected build.**

#### Points Tools

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Import_Point_cloud.svg" width="11" height="11" alt="Import Pointsâ€¦"> [Import Pointsâ€¦](#button-points_import) | Points | Tools |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Export_Point_cloud.svg" width="11" height="11" alt="Export Pointsâ€¦"> [Export Pointsâ€¦](#button-points_export) | Points | Tools |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Convert.svg" width="11" height="11" alt="Convert to Points"> [Convert to Points](#button-points_convert) | Points | Tools |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Structure.svg" width="11" height="11" alt="Structured Point Cloud"> [Structured Point Cloud](#button-points_structure) | Points | Tools |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Merge.svg" width="11" height="11" alt="Merge Point Clouds"> [Merge Point Clouds](#button-points_merge) | Points | Tools |
| <img src="../../../src/Gui/Icons/PolygonPick.svg" width="11" height="11" alt="Cut Point Cloud"> [Cut Point Cloud](#button-points_polycut) | Points | Tools |

<a id="workbench-robotworkbench"></a>
### Robot workbench

Definition: [`src/Mod/Robot/Gui/Workbench.cpp`](../../../src/Mod/Robot/Gui/Workbench.cpp). **Source-only; unavailable in the inspected build.**

#### Robot

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_CreateRobot.svg" width="11" height="11" alt="Place Robot"> [Place Robot](#button-robot_create) | Robot | Tools |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_CreateTrajectory.svg" width="11" height="11" alt="Trajectory"> [Trajectory](#button-robot_createtrajectory) | Robot | Tools |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_InsertWaypoint.svg" width="11" height="11" alt="Insert in Trajectory"> [Insert in Trajectory](#button-robot_insertwaypoint) | Robot | Tools |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_InsertWaypointPre.svg" width="11" height="11" alt="Insert in Trajectory"> [Insert in Trajectory](#button-robot_insertwaypointpreselect) | Robot | Tools |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_Edge2Trac.svg" width="11" height="11" alt="Edge to Trajectory"> [Edge to Trajectory](#button-robot_edge2trac) | Robot | Tools |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_TrajectoryDressUp.svg" width="11" height="11" alt="Dress-Up Trajectory"> [Dress-Up Trajectory](#button-robot_trajectorydressup) | Robot | Tools |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_TrajectoryCompound.svg" width="11" height="11" alt="Trajectory Compound"> [Trajectory Compound](#button-robot_trajectorycompound) | Robot | Tools |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_SetHomePos.svg" width="11" height="11" alt="Set Home Position"> [Set Home Position](#button-robot_sethomepos) | Robot | Tools |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_RestoreHomePos.svg" width="11" height="11" alt="Move to Home"> [Move to Home](#button-robot_restorehomepos) | Robot | Tools |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_Simulate.svg" width="11" height="11" alt="Simulate Trajectory"> [Simulate Trajectory](#button-robot_simulate) | Robot | Tools |

<a id="workbench-reverseengineeringworkbench"></a>
### ReverseEngineering workbench

Definition: [`src/Mod/ReverseEngineering/Gui/Workbench.cpp`](../../../src/Mod/ReverseEngineering/Gui/Workbench.cpp). **Source-only; unavailable in the inspected build.**

#### Reverse Engineering

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Mod/ReverseEngineering/Gui/Resources/icons/actions/FitSurface.svg" width="11" height="11" alt="Approximate B-Spline Surfaceâ€¦"> [Approximate B-Spline Surfaceâ€¦](#button-reen_approxsurface) | ReverseEngineering | Tools |

<a id="workbench-inspectionworkbench"></a>
### Inspection workbench

Definition: [`src/Mod/Inspection/Gui/Workbench.cpp`](../../../src/Mod/Inspection/Gui/Workbench.cpp). **Source-only; unavailable in the inspected build.**

#### Inspection

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Mod/Inspection/Gui/Resources/icons/InspectionWorkbench.svg" width="11" height="11" alt="Visual Inspection"> [Visual Inspection](#button-inspection_visualinspection) | Inspection | Tools |
| <img src="../../../src/Mod/Inspection/Gui/Resources/icons/inspect_pipette.svg" width="11" height="11" alt="Inspectionâ€¦"> [Inspectionâ€¦](#button-inspection_inspectelement) | Inspection | Tools |

<a id="workbench-bimworkbench"></a>
### BIM workbench

Definition: [`src/Mod/BIM/InitGui.py`](../../../src/Mod/BIM/InitGui.py). **Source-only; unavailable in the inspected build.**

#### Drafting Tools

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Mod/BIM/Resources/icons/Sketch.svg" width="11" height="11" alt="New Sketch"> [New Sketch](#button-bim_sketch) | BIM | Tools |
| <img src="toolbar-icons/Draft_Line.png" width="11" height="11" alt="Line"> [Line](#button-draft_line) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Wire.png" width="11" height="11" alt="Polyline"> [Polyline](#button-draft_wire) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Rectangle.png" width="11" height="11" alt="Rectangle"> [Rectangle](#button-draft_rectangle) | Draft / BIM | Tools |
| <img src="../../../src/Mod/Draft/Resources/icons/Draft_Arc.svg" width="11" height="11" alt="Arc Tools"> [Arc Tools](#button-bim_arctools) | BIM | Tools |
| <img src="toolbar-icons/Draft_Circle.png" width="11" height="11" alt="Circle"> [Circle](#button-draft_circle) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Ellipse.png" width="11" height="11" alt="Ellipse"> [Ellipse](#button-draft_ellipse) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Polygon.png" width="11" height="11" alt="Polygon"> [Polygon](#button-draft_polygon) | Draft / BIM | Tools |
| <img src="../../../src/Mod/Draft/Resources/icons/Draft_BSpline.svg" width="11" height="11" alt="Spline Tools"> [Spline Tools](#button-bim_splinetools) | BIM | Tools |
| <img src="toolbar-icons/Draft_Point.png" width="11" height="11" alt="Point"> [Point](#button-draft_point) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Fillet.png" width="11" height="11" alt="Fillet"> [Fillet](#button-draft_fillet) | Draft / BIM | Tools |

#### Draft Snap

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Draft_Snap_Lock.png" width="11" height="11" alt="Snap Lock"> [Snap Lock](#button-draft_snap_lock) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Endpoint.png" width="11" height="11" alt="Snap Endpoint"> [Snap Endpoint](#button-draft_snap_endpoint) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Midpoint.png" width="11" height="11" alt="Snap Midpoint"> [Snap Midpoint](#button-draft_snap_midpoint) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Center.png" width="11" height="11" alt="Snap Center"> [Snap Center](#button-draft_snap_center) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Angle.png" width="11" height="11" alt="Snap Angle"> [Snap Angle](#button-draft_snap_angle) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Intersection.png" width="11" height="11" alt="Snap Intersection"> [Snap Intersection](#button-draft_snap_intersection) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Perpendicular.png" width="11" height="11" alt="Snap Perpendicular"> [Snap Perpendicular](#button-draft_snap_perpendicular) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Extension.png" width="11" height="11" alt="Snap Extension"> [Snap Extension](#button-draft_snap_extension) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Parallel.png" width="11" height="11" alt="Snap Parallel"> [Snap Parallel](#button-draft_snap_parallel) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Special.png" width="11" height="11" alt="Snap Special"> [Snap Special](#button-draft_snap_special) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Near.png" width="11" height="11" alt="Snap Near"> [Snap Near](#button-draft_snap_near) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Ortho.png" width="11" height="11" alt="Snap Ortho"> [Snap Ortho](#button-draft_snap_ortho) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Grid.png" width="11" height="11" alt="Snap Grid"> [Snap Grid](#button-draft_snap_grid) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_WorkingPlane.png" width="11" height="11" alt="Snap Working Plane"> [Snap Working Plane](#button-draft_snap_workingplane) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Snap_Dimensions.png" width="11" height="11" alt="Snap Dimensions"> [Snap Dimensions](#button-draft_snap_dimensions) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_ToggleGrid.png" width="11" height="11" alt="Toggle Grid"> [Toggle Grid](#button-draft_togglegrid) | Draft / BIM | Tools |

#### 3D/BIM Tools

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Site.svg" width="11" height="11" alt="Site"> [Site](#button-arch_site) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Building.svg" width="11" height="11" alt="Building"> [Building](#button-arch_building) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Floor.svg" width="11" height="11" alt="Level"> [Level](#button-arch_level) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Space.svg" width="11" height="11" alt="Space"> [Space](#button-arch_space) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Wall.svg" width="11" height="11" alt="Wall"> [Wall](#button-arch_wall) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_CurtainWall.svg" width="11" height="11" alt="Curtain Wall"> [Curtain Wall](#button-arch_curtainwall) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Column.svg" width="11" height="11" alt="Column"> [Column](#button-bim_column) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Beam.svg" width="11" height="11" alt="Beam"> [Beam](#button-bim_beam) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Slab.svg" width="11" height="11" alt="Slab"> [Slab](#button-bim_slab) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Door.svg" width="11" height="11" alt="Door"> [Door](#button-bim_door) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Window.svg" width="11" height="11" alt="Window"> [Window](#button-arch_window) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Covering.svg" width="11" height="11" alt="Covering"> [Covering](#button-bim_covering) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Pipe.svg" width="11" height="11" alt="Pipe"> [Pipe](#button-arch_pipe) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_PipeConnector.svg" width="11" height="11" alt="Connector"> [Connector](#button-arch_pipeconnector) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Stairs.svg" width="11" height="11" alt="Stairs"> [Stairs](#button-arch_stairs) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Roof.svg" width="11" height="11" alt="Roof"> [Roof](#button-arch_roof) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Panel.svg" width="11" height="11" alt="Panel"> [Panel](#button-arch_panel) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Frame.svg" width="11" height="11" alt="Frame"> [Frame](#button-arch_frame) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Fence.svg" width="11" height="11" alt="Fence"> [Fence](#button-arch_fence) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Truss.svg" width="11" height="11" alt="Truss"> [Truss](#button-arch_truss) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Equipment.svg" width="11" height="11" alt="Equipment"> [Equipment](#button-arch_equipment) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Rebar.svg" width="11" height="11" alt="Custom Rebar"> [Custom Rebar](#button-arch_rebar) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Box.svg" width="11" height="11" alt="Generic 3D Tools"> [Generic 3D Tools](#button-bim_generictools) | BIM | Tools |

#### Annotation Tools

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_DimensionAligned.svg" width="11" height="11" alt="Aligned Dimension"> [Aligned Dimension](#button-bim_dimensionaligned) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_DimensionHorizontal.svg" width="11" height="11" alt="Horizontal Dimension"> [Horizontal Dimension](#button-bim_dimensionhorizontal) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_DimensionVertical.svg" width="11" height="11" alt="Vertical Dimension"> [Vertical Dimension](#button-bim_dimensionvertical) | BIM | Tools |
| <img src="../../../src/Mod/Draft/Resources/icons/Draft_Text.svg" width="11" height="11" alt="Text"> [Text](#button-bim_text) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Leader.svg" width="11" height="11" alt="Leader"> [Leader](#button-bim_leader) | BIM | Tools |
| <img src="toolbar-icons/Draft_Label.png" width="11" height="11" alt="Label"> [Label](#button-draft_label) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Hatch.png" width="11" height="11" alt="Hatch"> [Hatch](#button-draft_hatch) | Draft / BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Axis.svg" width="11" height="11" alt="Axis Tools"> [Axis Tools](#button-bim_axistools) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Grid.svg" width="11" height="11" alt="Grid"> [Grid](#button-arch_grid) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_SectionPlane.svg" width="11" height="11" alt="Section Plane"> [Section Plane](#button-arch_sectionplane) | BIM | Tools |
| â€” [Create 2D Views](#button-bim_create2dviews) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_PageDefault.svg" width="11" height="11" alt="New Page"> [New Page](#button-bim_tdpage) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_InsertView.svg" width="11" height="11" alt="New View"> [New View](#button-bim_tdview) | BIM | Tools |

#### General Tools

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Draft_Move.png" width="11" height="11" alt="Move"> [Move](#button-draft_move) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Rotate.png" width="11" height="11" alt="Rotate"> [Rotate](#button-draft_rotate) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Scale.png" width="11" height="11" alt="Scale"> [Scale](#button-draft_scale) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Mirror.png" width="11" height="11" alt="Mirror"> [Mirror](#button-draft_mirror) | Draft / BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Clone.svg" width="11" height="11" alt="Cloning Tools"> [Cloning Tools](#button-bim_clonetools) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Copy.svg" width="11" height="11" alt="Copy"> [Copy](#button-bim_copy) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Tree_Part.svg" width="11" height="11" alt="Simple Copy"> [Simple Copy](#button-bim_simplecopy) | BIM | Tools |
| <img src="../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Compound.svg" width="11" height="11" alt="Compound"> [Compound](#button-bim_compound) | BIM | Tools |

#### 2D Tools

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| â€” [Offset Tools](#button-bim_offsettools) | BIM | Tools |
| <img src="../../../src/Mod/Draft/Resources/icons/Draft_Trimex.svg" width="11" height="11" alt="Trimex"> [Trimex](#button-bim_trimex) | BIM | Tools |
| <img src="toolbar-icons/Draft_Join.png" width="11" height="11" alt="Join"> [Join](#button-draft_join) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Split.png" width="11" height="11" alt="Split"> [Split](#button-draft_split) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Stretch.png" width="11" height="11" alt="Stretch"> [Stretch](#button-draft_stretch) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Draft2Sketch.png" width="11" height="11" alt="Draft to Sketch"> [Draft to Sketch](#button-draft_draft2sketch) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Edit.png" width="11" height="11" alt="Edit"> [Edit](#button-draft_edit) | Draft / BIM | Tools |

#### Object Tools

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Draft_Upgrade.png" width="11" height="11" alt="Upgrade"> [Upgrade](#button-draft_upgrade) | Draft / BIM | Tools |
| <img src="toolbar-icons/Draft_Downgrade.png" width="11" height="11" alt="Downgrade"> [Downgrade](#button-draft_downgrade) | Draft / BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Add.svg" width="11" height="11" alt="Add Component"> [Add Component](#button-arch_add) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Remove.svg" width="11" height="11" alt="Remove Component"> [Remove Component](#button-arch_remove) | BIM | Tools |

#### 3D Tools

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Mod/Draft/Resources/icons/Draft_Array.svg" width="11" height="11" alt="Array Tools"> [Array Tools](#button-bim_arraytools) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_CutPlane.svg" width="11" height="11" alt="Cut With Plane"> [Cut With Plane](#button-arch_cutplane) | BIM | Tools |
| <img src="../../../src/Mod/Part/Gui/Resources/icons/tools/Part_Extrude.svg" width="11" height="11" alt="Extrude"> [Extrude](#button-bim_extrude) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_ExtrudeFace.svg" width="11" height="11" alt="Extrude Face"> [Extrude Face](#button-bim_extrudeface) | BIM | Tools |
| â€” [Boolean Tools](#button-bim_booleantools) | BIM | Tools |

#### Manage Tools

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Gui/Icons/preferences-system.svg" width="11" height="11" alt="BIM Setup"> [BIM Setup](#button-bim_setup) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_ProjectManager.svg" width="11" height="11" alt="Setup Project"> [Setup Project](#button-bim_projectmanager) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Windows.svg" width="11" height="11" alt="Manage Doors and Windows"> [Manage Doors and Windows](#button-bim_windows) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_IfcElements.svg" width="11" height="11" alt="IFC Management"> [IFC Management](#button-bim_ifcmanagetools) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Layers.svg" width="11" height="11" alt="Manage Layers"> [Manage Layers](#button-bim_layers) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Material.svg" width="11" height="11" alt="Material"> [Material](#button-bim_material) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Report.svg" width="11" height="11" alt="Report Tools"> [Report Tools](#button-bim_reporttools) | BIM | Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Preflight.svg" width="11" height="11" alt="Preflight Checks"> [Preflight Checks](#button-bim_preflight) | BIM | Tools |
| <img src="toolbar-icons/Draft_AnnotationStyleEditor.png" width="11" height="11" alt="Annotation Styles"> [Annotation Styles](#button-draft_annotationstyleeditor) | Draft / BIM | Tools |

<a id="workbench-openscadworkbench"></a>
### OpenSCAD workbench

Definition: [`src/Mod/OpenSCAD/InitGui.py`](../../../src/Mod/OpenSCAD/InitGui.py). **Source-only; unavailable in the inspected build.**

#### OpenSCAD Tools

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_ReplaceObject.svg" width="11" height="11" alt="Replace Object"> [Replace Object](#button-openscad_replaceobject) | OpenSCAD | Tools |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_RemoveSubtree.svg" width="11" height="11" alt="Remove Objects and Children"> [Remove Objects and Children](#button-openscad_removesubtree) | OpenSCAD | Tools |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Explode_Group.svg" width="11" height="11" alt="Explode Group"> [Explode Group](#button-openscad_explodegroup) | OpenSCAD | Tools |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_RefineShapeFeature.svg" width="11" height="11" alt="Refine Shape Feature"> [Refine Shape Feature](#button-openscad_refineshapefeature) | OpenSCAD | Tools |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_IncreaseToleranceFeature.svg" width="11" height="11" alt="Increase Tolerance Feature"> [Increase Tolerance Feature](#button-openscad_increasetolerancefeature) | OpenSCAD | Tools |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_AddOpenSCADElement.svg" width="11" height="11" alt="Add OpenSCAD Element"> [Add OpenSCAD Element](#button-openscad_addopenscadelement) | OpenSCAD | Tools |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_MeshBooleans.svg" width="11" height="11" alt="Mesh Boolean"> [Mesh Boolean](#button-openscad_meshboolean) | OpenSCAD | Tools |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Hull.svg" width="11" height="11" alt="Hull"> [Hull](#button-openscad_hull) | OpenSCAD | Tools |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Minkowski.svg" width="11" height="11" alt="Minkowski Sum"> [Minkowski Sum](#button-openscad_minkowski) | OpenSCAD | Tools |

#### Frequently-used Part WB tools

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="toolbar-icons/Part_CheckGeometry.png" width="11" height="11" alt="Check Geometry"> [Check Geometry](#button-part_checkgeometry) | Design / Part / OpenSCAD | Modeling; Tools |
| <img src="toolbar-icons/Part_Primitives.png" width="11" height="11" alt="Primitive"> [Primitive](#button-part_primitives) | Part / OpenSCAD | Tools |
| <img src="toolbar-icons/Part_Builder.png" width="11" height="11" alt="Shape Builder"> [Shape Builder](#button-part_builder) | Part / OpenSCAD | Tools |
| <img src="toolbar-icons/Part_Cut.png" width="11" height="11" alt="Cut"> [Cut](#button-part_cut) | Part / OpenSCAD | Tools |
| <img src="toolbar-icons/Part_Fuse.png" width="11" height="11" alt="Union"> [Union](#button-part_fuse) | Part / OpenSCAD | Tools |
| <img src="toolbar-icons/Part_Common.png" width="11" height="11" alt="Intersection"> [Intersection](#button-part_common) | Part / OpenSCAD | Tools |
| <img src="toolbar-icons/Part_Extrude.png" width="11" height="11" alt="Extrude"> [Extrude](#button-part_extrude) | Part / OpenSCAD | Tools |
| <img src="toolbar-icons/Part_Revolve.png" width="11" height="11" alt="Revolve"> [Revolve](#button-part_revolve) | Part / OpenSCAD | Tools |

<a id="workbench-testworkbench"></a>
### Test Framework workbench

Definition: [`src/Mod/Test/InitGui.py`](../../../src/Mod/Test/InitGui.py).

#### TestTools

| Command | Plus mode | Plus tab / location |
| --- | --- | --- |
| <img src="../../../src/Gui/Icons/preferences-general.svg" width="11" height="11" alt="Self-test..."> [Self-test...](#button-test_test) | Test Framework | Tools |
| <img src="toolbar-icons/Test_TestAll.png" width="11" height="11" alt="Test all"> [Test all](#button-test_testall) | Test Framework | Tools |
| <img src="toolbar-icons/Test_TestDoc.png" width="11" height="11" alt="Test Document"> [Test Document](#button-test_testdoc) | Test Framework | Tools |
| <img src="toolbar-icons/Test_TestBase.png" width="11" height="11" alt="Test base"> [Test base](#button-test_testbase) | Test Framework | Tools |

## Plus UI target layout

### Design Layers toolbar

Visible only in Plus Design mode, beside Save/Edit and Selection: **Layers** opens
the task panel; **Move to Layer** and **Change Active Layer** use fixed-label,
whole-button dropdown menus. Move is disabled without eligible preselection;
active-layer choices have check marks. No split default action or wide current-value
combo box is used. The panel provides creation, rename, deletion, assignment, active
choice and eye controls. Base/origin protection and body/sketch independence follow
[the interaction requirements](../UI_UX_SPEC.md#design-layers).

The Contextual Constraint Palette is a viewport overlay, not another top toolbar.
It appears only after sketch selection clicks and uses the shared persistent
selection policy. See [palette interaction requirements](../UI_UX_SPEC.md#contextual-constraint-palette).

### Design Selection toolbar

Source addition, October 3: `FreeCADPlusSelection` appears alongside the common
Save/Edit row above the ribbon only in Design mode. Its ordered controls are
Single Curve / Connected Curves / Tangent Curves; Selection Filter with independent
Planes, Bodies, Surfaces, Faces, Edges, Curves, Points, Vertices checkboxes;
Directional Selection; Persistent Selection. Both toggles default on and retain
saved choices. This is a dedicated toolbar, not an additional ribbon group.
Classic and non-Design modes hide it and deactivate its policy. See
[interaction contract](../UI_UX_SPEC.md#design-selection-toolbar) and WORK_STATE
for source checks and pending grouped native acceptance.

### Size and dropdown key

| Treatment | Use |
| --- | --- |
| Full size / big | Primary operations; one row, bounded captions |
| Medium / half size | Frequently used actions that need less visual weight; bounded captions |
| Small | Secondary actions; no visible caption; three-row grid inside the ribbon |
| Dropdown | A separate property, compatible with any icon size; related or rare choices appear in its menu |

Full icons are 40 logical pixels, medium icons 20, and small icons 16. Full buttons span the 76px grid; two medium buttons (38px each) or three small buttons (24px each) fit a column. Documentation icon size is independent of application button size. Every icon retains a tooltip and accessible name.

### All Modes

**Horizontal common toolbar above the ribbon.** These native actions remain visible when modes or tabs change. All use small icons in one horizontal row. They belong to Plus UI; Classic toolbar restoration must not duplicate them.

#### File group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_New.png" width="11" height="11" alt="New Document"> [New File](#button-std_new) | Small | â€” |
| <img src="toolbar-icons/Std_Open.png" width="11" height="11" alt="Openâ€¦"> [Openâ€¦](#button-std_open) | Small | â€” |
| <img src="toolbar-icons/Std_Save.png" width="11" height="11" alt="Save"> [Save](#button-std_save) | Small | â€” |
| <img src="toolbar-icons/Std_SaveAs.png" width="11" height="11" alt="Save Asâ€¦"> [Save Asâ€¦](#button-std_saveas) | Small | â€” |

#### Edit group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Undo.png" width="11" height="11" alt="Undo"> [Undo](#button-std_undo) | Small | â€” |
| <img src="toolbar-icons/Std_Redo.png" width="11" height="11" alt="Redo"> [Redo](#button-std_redo) | Small | â€” |
| <img src="toolbar-icons/Std_Refresh.png" width="11" height="11" alt="Recompute"> [Recompute](#button-std_refresh) | Small | â€” |

#### Clipboard group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Cut.png" width="11" height="11" alt="Cut"> [Cut](#button-std_cut) | Small | â€” |
| <img src="toolbar-icons/Std_Copy.png" width="11" height="11" alt="Copy"> [Copy](#button-std_copy) | Small | â€” |
| <img src="toolbar-icons/Std_Paste.png" width="11" height="11" alt="Paste"> [Paste](#button-std_paste) | Small | â€” |

### Design Mode

Tabs: **Home â†’ Modeling â†’ Surface â†’ Sketch â†’ Assembly â†’ Mesh â†’ View**. Sketch is retained from the earlier design because the owner's new outline is incomplete. Assembly is added to Design. Home contains curated frequent actions from the other tabs; specialist groups remain in their own tabs.

#### Home tab

Exactly three groups in this order. This revision awaits the next owner build. Common File/Edit/Clipboard remains above the ribbon.

##### Main group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_NewComponent.png" width="11" height="11" alt="New Component"> [New Component](#button-std_newcomponent) | Medium | â€” |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [Add Component](#button-std_part) | Medium | â€” |

##### Modeling group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/PartDesign_Extrude.png" width="11" height="11" alt="Extrude"> [Extrude](#button-partdesign_extrude) | Full size | â€” |
| <img src="toolbar-icons/PartDesign_Revolution.png" width="11" height="11" alt="Revolve"> [Revolve](#button-partdesign_revolution) | Full size | â€” |
| <img src="toolbar-icons/PartDesign_Fillet.png" width="11" height="11" alt="Fillet/Chamfer"> [Fillet/Chamfer](#button-partdesign_fillet) | Medium; dropdown: Fillet, Chamfer | â€” |

##### Sketch group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/PartDesign_NewSketch.png" width="11" height="11" alt="New Sketch"> [New Sketch](#button-partdesign_newsketch) | Medium | â€” |
| <img src="toolbar-icons/Part_CoordinateSystem.png" width="11" height="11" alt="Coordinate System"> [Coordinate System](#button-part_coordinatesystem) | Medium; dropdown: Coordinate System, Plane, Axis, Point | â€” |

#### Modeling tab

October 6 owner layout; medium and small buttons show icons only. Large captions and group labels retain complete names, using two lines when needed. Gray vertical dividers separate adjacent groups on every tab. Native actions, tooltips and geometry workflows are retained.

| Group | Large buttons | Medium button clusters (two per column) | Small button cluster |
| --- | --- | --- | --- |
| Sketch | New Sketch | — | Edit Sketch; Attach Sketch; Coordinate System dropdown |
| Modeling | Extrude; Revolve | Loft; Helix | — |
| Dress-Up | Fillet and Chamfer split button (default Fillet; Chamfer menu choice) | Draft; Shell/Thickness | — |
| Transformation | — | Mirror Feature; Linear Pattern / Circular Pattern; Multi Transform | — |
| Primitives | Primitives split dropdown, default Box | — | — |
| Other | — | Delete Face/Defeaturing; Add Reference Object | — |

Coordinate System choices: **Coordinate System (default), Plane, Axis, Point**.
Primitives choices: **Box (default), Cylinder, Sphere, Cone, Ellipsoid, Torus, Prism, Wedge, Tab**. Tab remains disabled/unimplemented. Native additive/subtractive primitive tasks are retained. Pipe and the standalone Chamfer/Primitive native commands remain available outside this revised ribbon membership.

#### Surface tab

##### Surface group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Surface_Filling.png" width="11" height="11" alt="Filling"> [Filling](#button-surface_filling) | Small | â€” |
| <img src="toolbar-icons/Surface_GeomFillSurface.png" width="11" height="11" alt="Fill Boundary Curves"> [Fill Boundary Curves](#button-surface_geomfillsurface) | Small | â€” |
| <img src="toolbar-icons/Surface_Sections.png" width="11" height="11" alt="Sections"> [Sections](#button-surface_sections) | Small | â€” |
| <img src="toolbar-icons/Surface_ExtendFace.png" width="11" height="11" alt="Extend Face"> [Extend Face](#button-surface_extendface) | Full size | â€” |
| <img src="toolbar-icons/Surface_CurveOnMesh.png" width="11" height="11" alt="Curve on Mesh"> [Curve on Mesh](#button-surface_curveonmesh) | Small | â€” |
| <img src="toolbar-icons/Surface_BlendCurve.png" width="11" height="11" alt="Blend Curve"> [Blend Curve](#button-surface_blendcurve) | Small | â€” |

#### Sketch tab

Exact owner layout, source-validated and awaiting the next build. All listed individual buttons remain alongside their dropdowns. Local captions preserve native command names, execution, enabled states and checked states.

##### Sketcher group

| Command | Icon size | Choices |
| --- | --- | --- |
| <img src="toolbar-icons/Sketcher_NewSketch.png" width="11" height="11" alt="New Sketch"> [New Sketch](#button-sketcher_newsketch) | Full | â€” |
| <img src="toolbar-icons/Sketcher_EditSketch.png" width="11" height="11" alt="Edit Sketch"> [Edit Sketch](#button-sketcher_editsketch) | Full | â€” |
| <img src="toolbar-icons/Sketcher_MapSketch.png" width="11" height="11" alt="Attach Sketch"> [Attach Sketch](#button-sketcher_mapsketch) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ReorientSketch.png" width="11" height="11" alt="Reorient Sketch"> [Reorient Sketch](#button-sketcher_reorientsketch) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ValidateSketch.png" width="11" height="11" alt="Validate Sketch"> [Validate Sketch](#button-sketcher_validatesketch) | Small | â€” |
| <img src="toolbar-icons/Sketcher_MergeSketches.png" width="11" height="11" alt="Merge Sketches"> [Merge Sketches](#button-sketcher_mergesketches) | Small | â€” |
| <img src="toolbar-icons/Sketcher_MirrorSketch.png" width="11" height="11" alt="Mirror Sketch"> [Mirror Sketch](#button-sketcher_mirrorsketch) | Small | â€” |

##### Edit Mode group

| Command | Icon size | Choices |
| --- | --- | --- |
| <img src="toolbar-icons/Sketcher_LeaveSketch.png" width="11" height="11" alt="Leave Sketch"> [Leave Sketch](#button-sketcher_leavesketch) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ViewSketch.png" width="11" height="11" alt="Align View to Sketch"> [Align View to Sketch](#button-sketcher_viewsketch) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ViewSection.png" width="11" height="11" alt="Toggle Section View"> [Toggle Section View](#button-sketcher_viewsection) | Small | â€” |

##### Geometries group

| Command | Icon size | Choices |
| --- | --- | --- |
| <img src="toolbar-icons/Sketcher_CreatePoint.png" width="11" height="11" alt="Point"> [Point](#button-sketcher_createpoint) | Small | â€” |
| <img src="toolbar-icons/Sketcher_CreateText.png" width="11" height="11" alt="Text (Experimental)"> [Text (Experimental)](#button-sketcher_createtext) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ToggleConstruction.png" width="11" height="11" alt="Toggle Construction Geometry"> [Toggle Construction Geometry](#button-sketcher_toggleconstruction) | Small | â€” |
| <img src="toolbar-icons/Sketcher_CompLine.png" width="11" height="11" alt="Line Tools"> [Line Tools](#button-sketcher_compline) | Small dropdown | Polyline; Line |
| <img src="toolbar-icons/Sketcher_CreatePolyline.png" width="11" height="11" alt="Polyline"> [Polyline](#button-sketcher_createpolyline) | Full | â€” |
| <img src="toolbar-icons/Sketcher_CreateLine.png" width="11" height="11" alt="Line"> [Line](#button-sketcher_createline) | Small | â€” |
| <img src="toolbar-icons/Sketcher_CompCreateArc.png" width="11" height="11" alt="Arc Tools"> [Arc Tools](#button-sketcher_compcreatearc) | Small dropdown | Arc From Center; Arc From 3 Points; Elliptical Arc; Hyperbolic Arc; Parabolic Arc |
| <img src="toolbar-icons/Sketcher_CompCreateConic.png" width="11" height="11" alt="Circle and Conic Tools"> [Circle and Conic Tools](#button-sketcher_compcreateconic) | Small dropdown | Circle From Center; Circle From 3 Points; Ellipse From Center; Ellipse From 3 Points |
| <img src="toolbar-icons/Sketcher_CompCreateRectangles.png" width="11" height="11" alt="Rectangle Tools"> [Rectangle Tools](#button-sketcher_compcreaterectangles) | Small dropdown | Rectangle; Centered Rectangle; Rounded Rectangle |
| <img src="toolbar-icons/Sketcher_CompCreateRegularPolygon.png" width="11" height="11" alt="Regular Polygon Tools"> [Regular Polygon Tools](#button-sketcher_compcreateregularpolygon) | Small dropdown | Triangle; Square; Pentagon; Hexagon; Heptagon; Octagon; Polygon |
| <img src="toolbar-icons/Sketcher_CompSlot.png" width="11" height="11" alt="Slot Tools"> [Slot Tools](#button-sketcher_compslot) | Small dropdown | Slot; Arc Slot |
| <img src="toolbar-icons/Sketcher_CompCreateBSpline.png" width="11" height="11" alt="B-Spline Creation Tools"> [B-Spline Creation Tools](#button-sketcher_compcreatebspline) | Small dropdown | B-Spline; Periodic B-Spline; B-Spline From Knots; Periodic B-Spline From Knots |

##### Constraints group

| Command | Icon size | Choices |
| --- | --- | --- |
| <img src="toolbar-icons/Sketcher_CompDimensionTools.png" width="11" height="11" alt="Dimension Tools"> [Dimension Tools](#button-sketcher_compdimensiontools) | Full dropdown | Dimension; Horizontal Dimension; Vertical Dimension; Distance Dimension; Radius/Diameter Dimension; Radius Dimension; Diameter Dimension; Angle Dimension; Lock Position |
| <img src="toolbar-icons/Sketcher_Dimension.png" width="11" height="11" alt="Dimension"> [Dimension](#button-sketcher_dimension) | Full | â€” |
| <img src="toolbar-icons/Sketcher_ConstrainDistanceX.png" width="11" height="11" alt="Horizontal Dimension"> [Horizontal Dimension](#button-sketcher_constraindistancex) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ConstrainDistanceY.png" width="11" height="11" alt="Vertical Dimension"> [Vertical Dimension](#button-sketcher_constraindistancey) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ConstrainDistance.png" width="11" height="11" alt="Distance Dimension"> [Distance Dimension](#button-sketcher_constraindistance) | Small | â€” |
| <img src="toolbar-icons/Sketcher_CompConstrainRadDia.png" width="11" height="11" alt="Radius and Diameter Constraints"> [Radius and Diameter Constraints](#button-sketcher_compconstrainraddia) | Small dropdown | Constrain radius; Constrain diameter; Constrain auto radius/diameter |
| <img src="toolbar-icons/Sketcher_ConstrainAngle.png" width="11" height="11" alt="Angle Dimension"> [Angle Dimension](#button-sketcher_constrainangle) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ConstrainLock.png" width="11" height="11" alt="Lock Position"> [Lock Position](#button-sketcher_constrainlock) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ConstrainCoincidentUnified.png" width="11" height="11" alt="Coincident / Point-on-object"> [Coincident / Point-on-object](#button-sketcher_constraincoincidentunified) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ConstrainCoincident.png" width="11" height="11" alt="Coincident Constraint"> [Coincident Constraint](#button-sketcher_constraincoincident) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ConstrainPointOnObject.png" width="11" height="11" alt="Point-on-object Constraint"> [Point-on-object Constraint](#button-sketcher_constrainpointonobject) | Small | â€” |
| <img src="toolbar-icons/Sketcher_CompHorVer.png" width="11" height="11" alt="Horizontal and Vertical Constraints"> [Horizontal and Vertical Constraints](#button-sketcher_comphorver) | Small dropdown | Horizontal Constraint; Vertical Constraint |
| <img src="toolbar-icons/Sketcher_ConstrainHorizontal.png" width="11" height="11" alt="Horizontal Constraint"> [Horizontal Constraint](#button-sketcher_constrainhorizontal) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ConstrainVertical.png" width="11" height="11" alt="Vertical Constraint"> [Vertical Constraint](#button-sketcher_constrainvertical) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ConstrainParallel.png" width="11" height="11" alt="Parallel Constraint"> [Parallel Constraint](#button-sketcher_constrainparallel) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ConstrainPerpendicular.png" width="11" height="11" alt="Perpendicular Constraint"> [Perpendicular Constraint](#button-sketcher_constrainperpendicular) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ConstrainTangent.png" width="11" height="11" alt="Tangent/Collinear Constraint"> [Tangent/Collinear Constraint](#button-sketcher_constraintangent) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ConstrainEqual.png" width="11" height="11" alt="Equal Constraint"> [Equal Constraint](#button-sketcher_constrainequal) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ConstrainSymmetric.png" width="11" height="11" alt="Symmetric Constraint"> [Symmetric Constraint](#button-sketcher_constrainsymmetric) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ConstrainBlock.png" width="11" height="11" alt="Block Constraint"> [Block Constraint](#button-sketcher_constrainblock) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ConstrainGroup.png" width="11" height="11" alt="Group Constraint (Development preview)"> [Group Constraint (Development preview)](#button-sketcher_constraingroup) | Small | â€” |
| <img src="toolbar-icons/Sketcher_CompToggleConstraints.png" width="11" height="11" alt="Constraint State"> [Constraint State](#button-sketcher_comptoggleconstraints) | Small dropdown | Toggle Driving/Reference Constraints; Toggle Constraints |

##### Tools group

| Command | Icon size | Choices |
| --- | --- | --- |
| <img src="toolbar-icons/Sketcher_CompExternal.png" width="11" height="11" alt="External Geometry"> [External Geometry](#button-sketcher_compexternal) | Small dropdown | External Projection; External Intersection |
| <img src="toolbar-icons/Sketcher_CarbonCopy.png" width="11" height="11" alt="Carbon Copy"> [Carbon Copy](#button-sketcher_carboncopy) | Small | â€” |
| <img src="toolbar-icons/Sketcher_Translate.png" width="11" height="11" alt="Move / Array Transform"> [Move / Array Transform](#button-sketcher_translate) | Small | â€” |
| <img src="toolbar-icons/Sketcher_Rotate.png" width="11" height="11" alt="Rotate / Polar Transform"> [Rotate / Polar Transform](#button-sketcher_rotate) | Small | â€” |
| <img src="toolbar-icons/Sketcher_Scale.png" width="11" height="11" alt="Scale"> [Scale](#button-sketcher_scale) | Small | â€” |
| <img src="toolbar-icons/Sketcher_Offset.png" width="11" height="11" alt="Offset"> [Offset](#button-sketcher_offset) | Small | â€” |
| <img src="toolbar-icons/Sketcher_Symmetry.png" width="11" height="11" alt="Mirror"> [Mirror](#button-sketcher_symmetry) | Small | â€” |
| <img src="toolbar-icons/Sketcher_RemoveAxesAlignment.png" width="11" height="11" alt="Remove Axes Alignment"> [Remove Axes Alignment](#button-sketcher_removeaxesalignment) | Small | â€” |
| <img src="toolbar-icons/Sketcher_CompCreateFillets.png" width="11" height="11" alt="Fillet and Chamfer Tools"> [Fillet and Chamfer Tools](#button-sketcher_compcreatefillets) | Small dropdown | Fillet; Chamfer |
| <img src="toolbar-icons/Sketcher_CompCurveEdition.png" width="11" height="11" alt="Curve Editing Tools"> [Curve Editing Tools](#button-sketcher_compcurveedition) | Small dropdown | Trim Edge; Split Edge; Extend Edge |

##### B-Spline group

| Command | Icon size | Choices |
| --- | --- | --- |
| <img src="toolbar-icons/Sketcher_BSplineConvertToNURBS.png" width="11" height="11" alt="Geometry to B-Spline"> [Geometry to B-Spline](#button-sketcher_bsplineconverttonurbs) | Small | â€” |
| <img src="toolbar-icons/Sketcher_BSplineIncreaseDegree.png" width="11" height="11" alt="Increase B-Spline Degree"> [Increase B-Spline Degree](#button-sketcher_bsplineincreasedegree) | Small | â€” |
| <img src="toolbar-icons/Sketcher_BSplineDecreaseDegree.png" width="11" height="11" alt="Decrease B-Spline Degree"> [Decrease B-Spline Degree](#button-sketcher_bsplinedecreasedegree) | Small | â€” |
| <img src="toolbar-icons/Sketcher_CompModifyKnotMultiplicity.png" width="11" height="11" alt="Knot Multiplicity"> [Knot Multiplicity](#button-sketcher_compmodifyknotmultiplicity) | Small dropdown | Increase knot multiplicity; Decrease knot multiplicity |
| <img src="toolbar-icons/Sketcher_BSplineInsertKnot.png" width="11" height="11" alt="Insert Knot"> [Insert Knot](#button-sketcher_bsplineinsertknot) | Small | â€” |
| <img src="toolbar-icons/Sketcher_JoinCurves.png" width="11" height="11" alt="Join Curves"> [Join Curves](#button-sketcher_joincurves) | Small | â€” |

##### Helpers group

| Command | Icon size | Choices |
| --- | --- | --- |
| <img src="toolbar-icons/Sketcher_SelectConstraints.png" width="11" height="11" alt="Select Associated Constraints"> [Select Associated Constraints](#button-sketcher_selectconstraints) | Small | â€” |
| <img src="toolbar-icons/Sketcher_SelectElementsAssociatedWithConstraints.png" width="11" height="11" alt="Select Associated Geometry"> [Select Associated Geometry](#button-sketcher_selectelementsassociatedwithconstraints) | Small | â€” |
| <img src="toolbar-icons/Sketcher_ArcOverlay.png" width="11" height="11" alt="Toggle Circular Helper for Arcs"> [Toggle Circular Helper for Arcs](#button-sketcher_arcoverlay) | Small | â€” |
| <img src="toolbar-icons/Sketcher_CompBSplineShowHideGeometryInformation.png" width="11" height="11" alt="B-Spline Geometry Information"> [B-Spline Geometry Information](#button-sketcher_compbsplineshowhidegeometryinformation) | Small dropdown | Toggle B-Spline Degree; Toggle B-Spline Control Polygon; Toggle B-Spline Curvature Comb; Toggle B-Spline Knot Multiplicity; Toggle B-Spline Control Point Weight |
| <img src="toolbar-icons/Sketcher_RestoreInternalAlignmentGeometry.png" width="11" height="11" alt="Toggle Internal Geometry"> [Toggle Internal Geometry](#button-sketcher_restoreinternalalignmentgeometry) | Small | â€” |
| <img src="toolbar-icons/Sketcher_SwitchVirtualSpace.png" width="11" height="11" alt="Switch Virtual Space"> [Switch Virtual Space](#button-sketcher_switchvirtualspace) | Small | â€” |

#### Assembly tab

##### Assembly group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Assembly_CreateAssembly.png" width="11" height="11" alt="Create Assembly"> [Create Assembly](#button-assembly_createassembly) | Full | â€” |
| <img src="toolbar-icons/Assembly_Insert.png" width="11" height="11" alt="Insert Component"> [Insert Component](#button-assembly_insert) | Full | Dropdown |
| â†³ <img src="toolbar-icons/Assembly_InsertLink.png" width="11" height="11" alt="Insert Component"> [Insert Component](#button-assembly_insertlink) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_InsertNewPart.png" width="11" height="11" alt="Insert New Part"> [Insert New Part](#button-assembly_insertnewpart) | Menu item | â€” |
| <img src="toolbar-icons/Part_LinkArrays.png" width="11" height="11" alt="Link Arrays"> [Link Arrays](#button-part_linkarrays) | Small | Dropdown |
| â†³ <img src="toolbar-icons/Part_LinkArrayCircular.png" width="11" height="11" alt="Circular Link Array"> [Circular Link Array](#button-part_linkarraycircular) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Part_LinkArrayLinear.png" width="11" height="11" alt="Linear Link Array"> [Linear Link Array](#button-part_linkarraylinear) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Part_LinkArrayPath.png" width="11" height="11" alt="Path Link Array"> [Path Link Array](#button-part_linkarraypath) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Part_LinkArrayPoint.png" width="11" height="11" alt="Point Link Array"> [Point Link Array](#button-part_linkarraypoint) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Part_LinkArrayPolar.png" width="11" height="11" alt="Polar Link Array"> [Polar Link Array](#button-part_linkarraypolar) | Menu item | â€” |
| <img src="toolbar-icons/Assembly_SolveAssembly.png" width="11" height="11" alt="Solve Assembly"> [Solve Assembly](#button-assembly_solveassembly) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateView.png" width="11" height="11" alt="Exploded View"> [Exploded View](#button-assembly_createview) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateSnapshot.png" width="11" height="11" alt="Snapshot"> [Snapshot](#button-assembly_createsnapshot) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateSimulation.png" width="11" height="11" alt="Simulation"> [Simulation](#button-assembly_createsimulation) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateBom.png" width="11" height="11" alt="Bill of Materials"> [Bill of Materials](#button-assembly_createbom) | Small | â€” |

##### Assembly Joints group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Assembly_ToggleGrounded.png" width="11" height="11" alt="Toggle Grounded"> [Toggle Grounded](#button-assembly_togglegrounded) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointRigidGroup.png" width="11" height="11" alt="Create Rigid Group"> [Create Rigid Group](#button-assembly_createjointrigidgroup) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointFixed.png" width="11" height="11" alt="Fixed Joint"> [Fixed Joint](#button-assembly_createjointfixed) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointRevolute.png" width="11" height="11" alt="Revolute Joint"> [Revolute Joint](#button-assembly_createjointrevolute) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointCylindrical.png" width="11" height="11" alt="Cylindrical Joint"> [Cylindrical Joint](#button-assembly_createjointcylindrical) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointSlider.png" width="11" height="11" alt="Slider Joint"> [Slider Joint](#button-assembly_createjointslider) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointBall.png" width="11" height="11" alt="Ball Joint"> [Ball Joint](#button-assembly_createjointball) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointDistance.png" width="11" height="11" alt="Distance Joint"> [Distance Joint](#button-assembly_createjointdistance) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointParallel.png" width="11" height="11" alt="Parallel Joint"> [Parallel Joint](#button-assembly_createjointparallel) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointPerpendicular.png" width="11" height="11" alt="Perpendicular Joint"> [Perpendicular Joint](#button-assembly_createjointperpendicular) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointAngle.png" width="11" height="11" alt="Angle Joint"> [Angle Joint](#button-assembly_createjointangle) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointRackPinion.png" width="11" height="11" alt="Rack and Pinion Joint"> [Rack and Pinion Joint](#button-assembly_createjointrackpinion) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointScrew.png" width="11" height="11" alt="Screw Joint"> [Screw Joint](#button-assembly_createjointscrew) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointGearBelt.png" width="11" height="11" alt="Gears Joint"> [Gears Joint](#button-assembly_createjointgearbelt) | Small | Dropdown |
| â†³ <img src="toolbar-icons/Assembly_CreateJointGears.png" width="11" height="11" alt="Gears Joint"> [Gears Joint](#button-assembly_createjointgears) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointBelt.png" width="11" height="11" alt="Belt Join"> [Belt Join](#button-assembly_createjointbelt) | Menu item | â€” |

#### Mesh tab

##### Mesh Tools group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Mesh_Import.png" width="11" height="11" alt="Import Meshâ€¦"> [Import Meshâ€¦](#button-mesh_import) | Full size | â€” |
| <img src="toolbar-icons/Mesh_Export.png" width="11" height="11" alt="Export Meshâ€¦"> [Export Meshâ€¦](#button-mesh_export) | Small | â€” |
| <img src="toolbar-icons/Mesh_FromPartShape.png" width="11" height="11" alt="Mesh From Shape"> [Mesh From Shape](#button-mesh_frompartshape) | Small | â€” |
| <img src="toolbar-icons/Mesh_BuildRegularSolid.png" width="11" height="11" alt="Regular Solid"> [Regular Solid](#button-mesh_buildregularsolid) | Small | â€” |

##### Mesh Modify group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Mesh_HarmonizeNormals.png" width="11" height="11" alt="Harmonize Normals"> [Harmonize Normals](#button-mesh_harmonizenormals) | Small | â€” |
| <img src="toolbar-icons/Mesh_FlipNormals.png" width="11" height="11" alt="Flip Normals"> [Flip Normals](#button-mesh_flipnormals) | Small | â€” |
| <img src="toolbar-icons/Mesh_FillupHoles.png" width="11" height="11" alt="Fill Holes"> [Fill Holes](#button-mesh_fillupholes) | Small | â€” |
| <img src="toolbar-icons/Mesh_FillInteractiveHole.png" width="11" height="11" alt="Close Hole"> [Close Hole](#button-mesh_fillinteractivehole) | Small | â€” |
| <img src="toolbar-icons/Mesh_AddFacet.png" width="11" height="11" alt="Add Triangle"> [Add Triangle](#button-mesh_addfacet) | Small | â€” |
| <img src="toolbar-icons/Mesh_RemoveComponents.png" width="11" height="11" alt="Remove Components"> [Remove Components](#button-mesh_removecomponents) | Small | â€” |
| <img src="toolbar-icons/Mesh_Smoothing.png" width="11" height="11" alt="Smooth"> [Smooth](#button-mesh_smoothing) | Small | â€” |
| <img src="toolbar-icons/Mesh_RemeshGmsh.png" width="11" height="11" alt="Refinement"> [Refinement](#button-mesh_remeshgmsh) | Small | â€” |
| <img src="toolbar-icons/Mesh_Decimating.png" width="11" height="11" alt="Decimate"> [Decimate](#button-mesh_decimating) | Small | â€” |
| <img src="toolbar-icons/Mesh_Scale.png" width="11" height="11" alt="Scale"> [Scale](#button-mesh_scale) | Small | â€” |

##### Mesh Boolean group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Mesh_Union.png" width="11" height="11" alt="Union"> [Union](#button-mesh_union) | Small | â€” |
| <img src="toolbar-icons/Mesh_Intersection.png" width="11" height="11" alt="Intersection"> [Intersection](#button-mesh_intersection) | Small | â€” |
| <img src="toolbar-icons/Mesh_Difference.png" width="11" height="11" alt="Difference"> [Difference](#button-mesh_difference) | Small | â€” |

##### Mesh Cutting group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Mesh_PolyCut.png" width="11" height="11" alt="Cut"> [Cut](#button-mesh_polycut) | Small | â€” |
| <img src="toolbar-icons/Mesh_PolyTrim.png" width="11" height="11" alt="Trim"> [Trim](#button-mesh_polytrim) | Small | â€” |
| <img src="toolbar-icons/Mesh_TrimByPlane.png" width="11" height="11" alt="Trim With Plane"> [Trim With Plane](#button-mesh_trimbyplane) | Small | â€” |
| <img src="toolbar-icons/Mesh_SectionByPlane.png" width="11" height="11" alt="Section From Plane"> [Section From Plane](#button-mesh_sectionbyplane) | Small | â€” |
| <img src="toolbar-icons/Mesh_CrossSections.png" width="11" height="11" alt="Cross-Sections"> [Cross-Sections](#button-mesh_crosssections) | Small | â€” |

##### Mesh Segmentation group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Mesh_Merge.png" width="11" height="11" alt="Merge"> [Merge](#button-mesh_merge) | Small | â€” |
| <img src="toolbar-icons/Mesh_SplitComponents.png" width="11" height="11" alt="Split by Components"> [Split by Components](#button-mesh_splitcomponents) | Small | â€” |
| <img src="toolbar-icons/Mesh_Segmentation.png" width="11" height="11" alt="Segmentation"> [Segmentation](#button-mesh_segmentation) | Small | â€” |
| <img src="toolbar-icons/Mesh_SegmentationBestFit.png" width="11" height="11" alt="Segmentation From Best-Fit Surfaces"> [Segmentation From Best-Fit Surfaces](#button-mesh_segmentationbestfit) | Small | â€” |

##### Mesh Analyze group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Mesh_Evaluation.png" width="11" height="11" alt="Evaluate and Repair"> [Evaluate and Repair](#button-mesh_evaluation) | Small | â€” |
| <img src="toolbar-icons/Mesh_EvaluateFacet.png" width="11" height="11" alt="Face Info"> [Face Info](#button-mesh_evaluatefacet) | Small | â€” |
| <img src="toolbar-icons/Mesh_VertexCurvature.png" width="11" height="11" alt="Curvature Plot"> [Curvature Plot](#button-mesh_vertexcurvature) | Small | â€” |
| <img src="toolbar-icons/Mesh_CurvatureInfo.png" width="11" height="11" alt="Curvature Info"> [Curvature Info](#button-mesh_curvatureinfo) | Small | â€” |
| <img src="toolbar-icons/Mesh_EvaluateSolid.png" width="11" height="11" alt="Evaluate Solid"> [Evaluate Solid](#button-mesh_evaluatesolid) | Small | â€” |
| <img src="toolbar-icons/Mesh_BoundingBox.png" width="11" height="11" alt="Bounding Box Info"> [Bounding Box Info](#button-mesh_boundingbox) | Small | â€” |

#### View tab

##### View group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_ViewFitAll.png" width="11" height="11" alt="Fit All"> [Fit All](#button-std_viewfitall) | Full size | â€” |
| <img src="toolbar-icons/Std_ViewFitSelection.png" width="11" height="11" alt="Fit Selection"> [Fit Selection](#button-std_viewfitselection) | Small | â€” |
| <img src="toolbar-icons/Std_ViewGroup.png" width="11" height="11" alt="Standard Views"> [Standard Views](#button-std_viewgroup) | Small | Dropdown |
| â†³ Choices for Standard Views | Menu items | Isometric; Front; Top; Right; Rear; Bottom; Left |
| <img src="toolbar-icons/Std_AlignToSelection.png" width="11" height="11" alt="Align to Selection"> [Align to Selection](#button-std_aligntoselection) | Small | â€” |
| <img src="toolbar-icons/Std_DrawStyle.png" width="11" height="11" alt="Draw Style"> [Draw Style](#button-std_drawstyle) | Small | Dropdown |
| â†³ Choices for Draw Style | Menu items | As Is; Points; Wireframe; Hidden Line; No Shading; Shaded; Flat Lines |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | Small | â€” |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | Small | â€” |

##### Individual Views group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_ViewIsometric.png" width="11" height="11" alt="Isometric"> [Isometric](#button-std_viewisometric) | Small | â€” |
| <img src="toolbar-icons/Std_ViewFront.png" width="11" height="11" alt="Front"> [Front](#button-std_viewfront) | Small | â€” |
| <img src="toolbar-icons/Std_ViewTop.png" width="11" height="11" alt="Top"> [Top](#button-std_viewtop) | Small | â€” |
| <img src="toolbar-icons/Std_ViewRight.png" width="11" height="11" alt="Right"> [Right](#button-std_viewright) | Small | â€” |
| <img src="toolbar-icons/Std_ViewRear.png" width="11" height="11" alt="Rear"> [Rear](#button-std_viewrear) | Small | â€” |
| <img src="toolbar-icons/Std_ViewBottom.png" width="11" height="11" alt="Bottom"> [Bottom](#button-std_viewbottom) | Small | â€” |
| <img src="toolbar-icons/Std_ViewLeft.png" width="11" height="11" alt="Left"> [Left](#button-std_viewleft) | Small | â€” |

### Part Mode

#### Home tab

Component access, this mode's frequent operations, and shared utilities. File/Edit/Clipboard stay in the common toolbar above the ribbon.

##### Main group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [Add Component](#button-std_part) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Medium (half size) | â€” |

##### Frequent operations group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Part_Box.png" width="11" height="11" alt="Cube"> [Cube](#button-part_box) | Medium (half size) | â€” |
| <img src="toolbar-icons/Part_Cylinder.png" width="11" height="11" alt="Cylinder"> [Cylinder](#button-part_cylinder) | Medium (half size) | â€” |
| <img src="toolbar-icons/Part_Sphere.png" width="11" height="11" alt="Sphere"> [Sphere](#button-part_sphere) | Medium (half size) | â€” |

##### Structure group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Small | â€” |
| <img src="toolbar-icons/Std_Group.png" width="11" height="11" alt="New Group"> [New Group](#button-std_group) | Small | â€” |
| <img src="toolbar-icons/Std_LinkActions.png" width="11" height="11" alt="Make Link"> [Make Link](#button-std_linkactions) | Small | Dropdown |
| â†³ Native choices for [Make Link](#button-std_linkactions) | Menu items | See function catalog |
| <img src="toolbar-icons/Std_VarSet.png" width="11" height="11" alt="Variable Set"> [Variable Set](#button-std_varset) | Small | â€” |
| <img src="toolbar-icons/PartDesign_AddReferenceObject.png" width="11" height="11" alt="Add Reference Object"> [Add Reference Object](#button-partdesign_addreferenceobject) | Small | â€” |

##### Utilities group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Import.png" width="11" height="11" alt="Importâ€¦"> [Importâ€¦](#button-std_import) | Small | â€” |
| <img src="toolbar-icons/Std_Export.png" width="11" height="11" alt="Exportâ€¦"> [Exportâ€¦](#button-std_export) | Small | â€” |
| <img src="toolbar-icons/Std_DlgPreferences.png" width="11" height="11" alt="Preferences"> [Preferences](#button-std_dlgpreferences) | Small | â€” |
| <img src="../../../src/Gui/Icons/zoom-in.svg" width="11" height="11" alt="Command search..."> [Command search...](#button-std_commandsearch) | Small | â€” |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | Small | â€” |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | Small | â€” |
| <img src="toolbar-icons/Std_Delete.png" width="11" height="11" alt="Delete"> [Delete](#button-std_delete) | Small | â€” |

##### Help group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Help | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> [What's This?](#button-std_whatsthis) | Menu item | â€” |

##### Macro group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Macro | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> [Record Macro](#button-std_dlgmacrorecord) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> [Macros](#button-std_dlgmacroexecute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> [Execute Macro](#button-std_dlgmacroexecutedirect) | Menu item | â€” |

#### Tools tab

##### Solids group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Part_Box.png" width="11" height="11" alt="Cube"> [Cube](#button-part_box) | Small | â€” |
| <img src="toolbar-icons/Part_Cylinder.png" width="11" height="11" alt="Cylinder"> [Cylinder](#button-part_cylinder) | Small | â€” |
| <img src="toolbar-icons/Part_Sphere.png" width="11" height="11" alt="Sphere"> [Sphere](#button-part_sphere) | Small | â€” |
| <img src="toolbar-icons/Part_Cone.png" width="11" height="11" alt="Cone"> [Cone](#button-part_cone) | Small | â€” |
| <img src="toolbar-icons/Part_Torus.png" width="11" height="11" alt="Torus"> [Torus](#button-part_torus) | Small | â€” |
| <img src="toolbar-icons/Part_Tube.png" width="11" height="11" alt="Tube"> [Tube](#button-part_tube) | Small | â€” |
| <img src="toolbar-icons/Part_Primitives.png" width="11" height="11" alt="Primitive"> [Primitive](#button-part_primitives) | Small | â€” |
| <img src="toolbar-icons/Part_Builder.png" width="11" height="11" alt="Shape Builder"> [Shape Builder](#button-part_builder) | Small | â€” |

##### Part Tools group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Sketcher_NewSketch.png" width="11" height="11" alt="New Sketch"> [New Sketch](#button-sketcher_newsketch) | Full size | â€” |
| <img src="toolbar-icons/Part_Extrude.png" width="11" height="11" alt="Extrude"> [Extrude](#button-part_extrude) | Small | â€” |
| <img src="toolbar-icons/PartDesign_AddReferenceObject.png" width="11" height="11" alt="Add Reference Object"> [Add Reference Object](#button-partdesign_addreferenceobject) | Small | â€” |
| <img src="toolbar-icons/Part_Revolve.png" width="11" height="11" alt="Revolve"> [Revolve](#button-part_revolve) | Small | â€” |
| <img src="toolbar-icons/Part_Mirror.png" width="11" height="11" alt="Mirror"> [Mirror](#button-part_mirror) | Small | â€” |
| <img src="toolbar-icons/Part_Scale.png" width="11" height="11" alt="Scale"> [Scale](#button-part_scale) | Small | â€” |
| <img src="toolbar-icons/Part_Fillet.png" width="11" height="11" alt="Fillet"> [Fillet](#button-part_fillet) | Small | â€” |
| <img src="toolbar-icons/Part_Chamfer.png" width="11" height="11" alt="Chamfer"> [Chamfer](#button-part_chamfer) | Small | â€” |
| <img src="toolbar-icons/Part_MakeFace.png" width="11" height="11" alt="Face From Wires"> [Face From Wires](#button-part_makeface) | Small | â€” |
| <img src="toolbar-icons/Part_RuledSurface.png" width="11" height="11" alt="Ruled Surface"> [Ruled Surface](#button-part_ruledsurface) | Small | â€” |
| <img src="toolbar-icons/Part_Loft.png" width="11" height="11" alt="Loft"> [Loft](#button-part_loft) | Small | â€” |
| <img src="toolbar-icons/Part_Sweep.png" width="11" height="11" alt="Sweep"> [Sweep](#button-part_sweep) | Small | â€” |
| <img src="toolbar-icons/Part_Section.png" width="11" height="11" alt="Section"> [Section](#button-part_section) | Small | â€” |
| <img src="toolbar-icons/Part_CrossSections.png" width="11" height="11" alt="Cross-Sections"> [Cross-Sections](#button-part_crosssections) | Small | â€” |
| <img src="toolbar-icons/Part_CompOffset.png" width="11" height="11" alt="3D Offset"> [3D Offset](#button-part_compoffset) | Small | Dropdown |
| â†³ <img src="toolbar-icons/Part_Offset.png" width="11" height="11" alt="3D Offset"> [3D Offset](#button-part_offset) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Part_Offset2D.png" width="11" height="11" alt="2D Offset"> [2D Offset](#button-part_offset2d) | Menu item | â€” |
| <img src="toolbar-icons/Part_Thickness.png" width="11" height="11" alt="Thickness"> [Thickness](#button-part_thickness) | Small | â€” |
| <img src="toolbar-icons/Part_ProjectionOnSurface.png" width="11" height="11" alt="Project on Surface"> [Project on Surface](#button-part_projectiononsurface) | Small | â€” |
| <img src="toolbar-icons/Part_IsoclineCurve.png" width="11" height="11" alt="Isocline Curve"> [Isocline Curve](#button-part_isoclinecurve) | Small | â€” |
| <img src="toolbar-icons/Part_ColorPerFace.png" width="11" height="11" alt="Appearance per Face"> [Appearance per Face](#button-part_colorperface) | Small | â€” |

##### Boolean Tools group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Part_CompCompoundTools.png" width="11" height="11" alt="Compound"> [Compound](#button-part_compcompoundtools) | Small | Dropdown |
| â†³ <img src="toolbar-icons/Part_Compound.png" width="11" height="11" alt="Compound"> [Compound](#button-part_compound) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Part_ExplodeCompound.png" width="11" height="11" alt="Explode Compound"> [Explode Compound](#button-part_explodecompound) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Part_CompoundFilter.png" width="11" height="11" alt="Compound Filter"> [Compound Filter](#button-part_compoundfilter) | Menu item | â€” |
| <img src="toolbar-icons/Part_Boolean.png" width="11" height="11" alt="Boolean Operation"> [Boolean Operation](#button-part_boolean) | Small | â€” |
| <img src="toolbar-icons/Part_Cut.png" width="11" height="11" alt="Cut"> [Cut](#button-part_cut) | Small | â€” |
| <img src="toolbar-icons/Part_Fuse.png" width="11" height="11" alt="Union"> [Union](#button-part_fuse) | Small | â€” |
| <img src="toolbar-icons/Part_Common.png" width="11" height="11" alt="Intersection"> [Intersection](#button-part_common) | Small | â€” |
| <img src="toolbar-icons/Part_TrimBody.png" width="11" height="11" alt="Trim Body"> [Trim Body](#button-part_trimbody) | Small | â€” |
| <img src="toolbar-icons/Part_CompJoinFeatures.png" width="11" height="11" alt="Connect Shapes"> [Connect Shapes](#button-part_compjoinfeatures) | Small | Dropdown |
| â†³ <img src="toolbar-icons/Part_JoinConnect.png" width="11" height="11" alt="Connect Shapes"> [Connect Shapes](#button-part_joinconnect) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Part_JoinEmbed.png" width="11" height="11" alt="Embed Shapes"> [Embed Shapes](#button-part_joinembed) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Part_JoinCutout.png" width="11" height="11" alt="Cutout Shape"> [Cutout Shape](#button-part_joincutout) | Menu item | â€” |
| <img src="toolbar-icons/Part_CompSplitFeatures.png" width="11" height="11" alt="Boolean Fragments"> [Boolean Fragments](#button-part_compsplitfeatures) | Small | Dropdown |
| â†³ <img src="toolbar-icons/Part_BooleanFragments.png" width="11" height="11" alt="Boolean Fragments"> [Boolean Fragments](#button-part_booleanfragments) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Part_SliceApart.png" width="11" height="11" alt="Slice Apart"> [Slice Apart](#button-part_sliceapart) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Part_Slice.png" width="11" height="11" alt="Slice to Compound"> [Slice to Compound](#button-part_slice) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Part_XOR.png" width="11" height="11" alt="Boolean XOR"> [Boolean XOR](#button-part_xor) | Menu item | â€” |
| <img src="toolbar-icons/Part_CheckGeometry.png" width="11" height="11" alt="Check Geometry"> [Check Geometry](#button-part_checkgeometry) | Small | â€” |
| <img src="toolbar-icons/Part_Defeaturing.png" width="11" height="11" alt="Defeaturing"> [Defeaturing](#button-part_defeaturing) | Small | â€” |

#### View tab

Use the **Design â†’ View** groups and sizes above; each mode activates its native view actions.

### Draft Mode

#### Home tab

Component access, this mode's frequent operations, and shared utilities. File/Edit/Clipboard stay in the common toolbar above the ribbon.

##### Main group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [Add Component](#button-std_part) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Medium (half size) | â€” |

##### Frequent operations group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Draft_Line.png" width="11" height="11" alt="Line"> [Line](#button-draft_line) | Medium (half size) | â€” |
| <img src="toolbar-icons/Draft_Wire.png" width="11" height="11" alt="Polyline"> [Polyline](#button-draft_wire) | Medium (half size) | â€” |
| <img src="toolbar-icons/Draft_Fillet.png" width="11" height="11" alt="Fillet"> [Fillet](#button-draft_fillet) | Medium (half size) | â€” |

##### Structure group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Small | â€” |
| <img src="toolbar-icons/Std_Group.png" width="11" height="11" alt="New Group"> [New Group](#button-std_group) | Small | â€” |
| <img src="toolbar-icons/Std_LinkActions.png" width="11" height="11" alt="Make Link"> [Make Link](#button-std_linkactions) | Small | Dropdown |
| â†³ Native choices for [Make Link](#button-std_linkactions) | Menu items | See function catalog |
| <img src="toolbar-icons/Std_VarSet.png" width="11" height="11" alt="Variable Set"> [Variable Set](#button-std_varset) | Small | â€” |
| <img src="toolbar-icons/PartDesign_AddReferenceObject.png" width="11" height="11" alt="Add Reference Object"> [Add Reference Object](#button-partdesign_addreferenceobject) | Small | â€” |

##### Utilities group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Import.png" width="11" height="11" alt="Importâ€¦"> [Importâ€¦](#button-std_import) | Small | â€” |
| <img src="toolbar-icons/Std_Export.png" width="11" height="11" alt="Exportâ€¦"> [Exportâ€¦](#button-std_export) | Small | â€” |
| <img src="toolbar-icons/Std_DlgPreferences.png" width="11" height="11" alt="Preferences"> [Preferences](#button-std_dlgpreferences) | Small | â€” |
| <img src="../../../src/Gui/Icons/zoom-in.svg" width="11" height="11" alt="Command search..."> [Command search...](#button-std_commandsearch) | Small | â€” |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | Small | â€” |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | Small | â€” |
| <img src="toolbar-icons/Std_Delete.png" width="11" height="11" alt="Delete"> [Delete](#button-std_delete) | Small | â€” |

##### Help group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Help | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> [What's This?](#button-std_whatsthis) | Menu item | â€” |

##### Macro group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Macro | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> [Record Macro](#button-std_dlgmacrorecord) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> [Macros](#button-std_dlgmacroexecute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> [Execute Macro](#button-std_dlgmacroexecutedirect) | Menu item | â€” |

#### Tools tab

##### Draft Creation group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Draft_Line.png" width="11" height="11" alt="Line"> [Line](#button-draft_line) | Full size | â€” |
| <img src="toolbar-icons/Draft_Wire.png" width="11" height="11" alt="Polyline"> [Polyline](#button-draft_wire) | Full size | â€” |
| <img src="toolbar-icons/Draft_Fillet.png" width="11" height="11" alt="Fillet"> [Fillet](#button-draft_fillet) | Small | â€” |
| <img src="toolbar-icons/Draft_ArcTools.png" width="11" height="11" alt="Arc"> [Arc](#button-draft_arctools) | Small | Dropdown |
| â†³ <img src="toolbar-icons/Draft_Arc.png" width="11" height="11" alt="Arc"> [Arc](#button-draft_arc) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_Arc_3Points.png" width="11" height="11" alt="Arc From 3 Points"> [Arc From 3 Points](#button-draft_arc_3points) | Menu item | â€” |
| <img src="toolbar-icons/Draft_Circle.png" width="11" height="11" alt="Circle"> [Circle](#button-draft_circle) | Small | â€” |
| <img src="toolbar-icons/Draft_Ellipse.png" width="11" height="11" alt="Ellipse"> [Ellipse](#button-draft_ellipse) | Small | â€” |
| <img src="toolbar-icons/Draft_Rectangle.png" width="11" height="11" alt="Rectangle"> [Rectangle](#button-draft_rectangle) | Small | â€” |
| <img src="toolbar-icons/Draft_Polygon.png" width="11" height="11" alt="Polygon"> [Polygon](#button-draft_polygon) | Small | â€” |
| <img src="toolbar-icons/Draft_BSpline.png" width="11" height="11" alt="B-Spline"> [B-Spline](#button-draft_bspline) | Small | â€” |
| <img src="toolbar-icons/Draft_BezierTools.png" width="11" height="11" alt="Cubic BÃ©zier Curve"> [Cubic BÃ©zier Curve](#button-draft_beziertools) | Small | Dropdown |
| â†³ <img src="toolbar-icons/Draft_CubicBezCurve.png" width="11" height="11" alt="Cubic BÃ©zier Curve"> [Cubic BÃ©zier Curve](#button-draft_cubicbezcurve) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_BezCurve.png" width="11" height="11" alt="BÃ©zier Curve"> [BÃ©zier Curve](#button-draft_bezcurve) | Menu item | â€” |
| <img src="toolbar-icons/Draft_Point.png" width="11" height="11" alt="Point"> [Point](#button-draft_point) | Small | â€” |
| <img src="toolbar-icons/Draft_Facebinder.png" width="11" height="11" alt="Facebinder"> [Facebinder](#button-draft_facebinder) | Small | â€” |
| <img src="toolbar-icons/Draft_ShapeString.png" width="11" height="11" alt="Shape From Text"> [Shape From Text](#button-draft_shapestring) | Small | â€” |
| <img src="toolbar-icons/Draft_Hatch.png" width="11" height="11" alt="Hatch"> [Hatch](#button-draft_hatch) | Small | â€” |

##### Draft Annotation group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Draft_Text.png" width="11" height="11" alt="Text"> [Text](#button-draft_text) | Small | â€” |
| <img src="toolbar-icons/Draft_Dimension.png" width="11" height="11" alt="Dimension"> [Dimension](#button-draft_dimension) | Small | â€” |
| <img src="toolbar-icons/Draft_Label.png" width="11" height="11" alt="Label"> [Label](#button-draft_label) | Small | â€” |
| <img src="toolbar-icons/Draft_AnnotationStyleEditor.png" width="11" height="11" alt="Annotation Styles"> [Annotation Styles](#button-draft_annotationstyleeditor) | Small | â€” |

##### Draft Modification group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Draft_Move.png" width="11" height="11" alt="Move"> [Move](#button-draft_move) | Small | â€” |
| <img src="toolbar-icons/Draft_Rotate.png" width="11" height="11" alt="Rotate"> [Rotate](#button-draft_rotate) | Small | â€” |
| <img src="toolbar-icons/Draft_Scale.png" width="11" height="11" alt="Scale"> [Scale](#button-draft_scale) | Small | â€” |
| <img src="toolbar-icons/Draft_Mirror.png" width="11" height="11" alt="Mirror"> [Mirror](#button-draft_mirror) | Small | â€” |
| <img src="toolbar-icons/Draft_Offset.png" width="11" height="11" alt="Offset"> [Offset](#button-draft_offset) | Small | â€” |
| <img src="toolbar-icons/Draft_Trimex.png" width="11" height="11" alt="Trimex"> [Trimex](#button-draft_trimex) | Small | â€” |
| <img src="toolbar-icons/Draft_Stretch.png" width="11" height="11" alt="Stretch"> [Stretch](#button-draft_stretch) | Small | â€” |
| <img src="toolbar-icons/Draft_Clone.png" width="11" height="11" alt="Clone"> [Clone](#button-draft_clone) | Small | â€” |
| <img src="toolbar-icons/Draft_ArrayTools.png" width="11" height="11" alt="Array"> [Array](#button-draft_arraytools) | Small | Dropdown |
| â†³ <img src="toolbar-icons/Draft_OrthoArray.png" width="11" height="11" alt="Array"> [Array](#button-draft_orthoarray) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_PolarArray.png" width="11" height="11" alt="Polar Array"> [Polar Array](#button-draft_polararray) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_CircularArray.png" width="11" height="11" alt="Circular Array"> [Circular Array](#button-draft_circulararray) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_PathArray.png" width="11" height="11" alt="Path Array"> [Path Array](#button-draft_patharray) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_PathLinkArray.png" width="11" height="11" alt="Path Link Array"> [Path Link Array](#button-draft_pathlinkarray) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_PointArray.png" width="11" height="11" alt="Point Array"> [Point Array](#button-draft_pointarray) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_PointLinkArray.png" width="11" height="11" alt="Point Link Array"> [Point Link Array](#button-draft_pointlinkarray) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_PathTwistedArray.png" width="11" height="11" alt="Twisted Path Array"> [Twisted Path Array](#button-draft_pathtwistedarray) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_PathTwistedLinkArray.png" width="11" height="11" alt="Twisted Path Link Array"> [Twisted Path Link Array](#button-draft_pathtwistedlinkarray) | Menu item | â€” |
| <img src="toolbar-icons/Draft_Edit.png" width="11" height="11" alt="Edit"> [Edit](#button-draft_edit) | Small | â€” |
| <img src="toolbar-icons/Draft_SubelementHighlight.png" width="11" height="11" alt="Highlight Subelements"> [Highlight Subelements](#button-draft_subelementhighlight) | Small | â€” |
| <img src="toolbar-icons/Draft_Join.png" width="11" height="11" alt="Join"> [Join](#button-draft_join) | Small | â€” |
| <img src="toolbar-icons/Draft_Split.png" width="11" height="11" alt="Split"> [Split](#button-draft_split) | Small | â€” |
| <img src="toolbar-icons/Draft_Upgrade.png" width="11" height="11" alt="Upgrade"> [Upgrade](#button-draft_upgrade) | Small | â€” |
| <img src="toolbar-icons/Draft_Downgrade.png" width="11" height="11" alt="Downgrade"> [Downgrade](#button-draft_downgrade) | Small | â€” |
| <img src="toolbar-icons/Draft_WireToBSpline.png" width="11" height="11" alt="Convert Wire/B-Spline"> [Convert Wire/B-Spline](#button-draft_wiretobspline) | Small | â€” |
| <img src="toolbar-icons/Draft_Draft2Sketch.png" width="11" height="11" alt="Draft to Sketch"> [Draft to Sketch](#button-draft_draft2sketch) | Small | â€” |
| <img src="toolbar-icons/Draft_Slope.png" width="11" height="11" alt="Set Slope"> [Set Slope](#button-draft_slope) | Small | â€” |
| <img src="toolbar-icons/Draft_FlipDimension.png" width="11" height="11" alt="Flip Dimension"> [Flip Dimension](#button-draft_flipdimension) | Small | â€” |
| <img src="toolbar-icons/Draft_Shape2DView.png" width="11" height="11" alt="Shape 2D View"> [Shape 2D View](#button-draft_shape2dview) | Small | â€” |

##### Draft Utility group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Draft_LayerManager.png" width="11" height="11" alt="Manage Layers"> [Manage Layers](#button-draft_layermanager) | Small | â€” |
| <img src="toolbar-icons/Draft_AddNamedGroup.png" width="11" height="11" alt="New Named Group"> [New Named Group](#button-draft_addnamedgroup) | Small | â€” |
| <img src="toolbar-icons/Draft_SelectGroup.png" width="11" height="11" alt="Select Group"> [Select Group](#button-draft_selectgroup) | Small | â€” |
| <img src="toolbar-icons/Draft_AddToLayer.png" width="11" height="11" alt="Add to Layer"> [Add to Layer](#button-draft_addtolayer) | Small | â€” |
| <img src="toolbar-icons/Draft_AddToGroup.png" width="11" height="11" alt="Add to Group"> [Add to Group](#button-draft_addtogroup) | Small | â€” |
| <img src="toolbar-icons/Draft_AddConstruction.png" width="11" height="11" alt="Add to Construction Group"> [Add to Construction Group](#button-draft_addconstruction) | Small | â€” |
| <img src="toolbar-icons/Draft_ToggleDisplayMode.png" width="11" height="11" alt="Toggle Wireframe"> [Toggle Wireframe](#button-draft_toggledisplaymode) | Small | â€” |
| <img src="toolbar-icons/Draft_WorkingPlaneProxy.png" width="11" height="11" alt="Working Plane Proxy"> [Working Plane Proxy](#button-draft_workingplaneproxy) | Small | â€” |

##### Draft Snap group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Draft_Snap_Lock.png" width="11" height="11" alt="Snap Lock"> [Snap Lock](#button-draft_snap_lock) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Endpoint.png" width="11" height="11" alt="Snap Endpoint"> [Snap Endpoint](#button-draft_snap_endpoint) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Midpoint.png" width="11" height="11" alt="Snap Midpoint"> [Snap Midpoint](#button-draft_snap_midpoint) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Center.png" width="11" height="11" alt="Snap Center"> [Snap Center](#button-draft_snap_center) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Angle.png" width="11" height="11" alt="Snap Angle"> [Snap Angle](#button-draft_snap_angle) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Intersection.png" width="11" height="11" alt="Snap Intersection"> [Snap Intersection](#button-draft_snap_intersection) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Perpendicular.png" width="11" height="11" alt="Snap Perpendicular"> [Snap Perpendicular](#button-draft_snap_perpendicular) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Extension.png" width="11" height="11" alt="Snap Extension"> [Snap Extension](#button-draft_snap_extension) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Parallel.png" width="11" height="11" alt="Snap Parallel"> [Snap Parallel](#button-draft_snap_parallel) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Special.png" width="11" height="11" alt="Snap Special"> [Snap Special](#button-draft_snap_special) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Near.png" width="11" height="11" alt="Snap Near"> [Snap Near](#button-draft_snap_near) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Ortho.png" width="11" height="11" alt="Snap Ortho"> [Snap Ortho](#button-draft_snap_ortho) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Grid.png" width="11" height="11" alt="Snap Grid"> [Snap Grid](#button-draft_snap_grid) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_WorkingPlane.png" width="11" height="11" alt="Snap Working Plane"> [Snap Working Plane](#button-draft_snap_workingplane) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Dimensions.png" width="11" height="11" alt="Snap Dimensions"> [Snap Dimensions](#button-draft_snap_dimensions) | Small | â€” |
| <img src="toolbar-icons/Draft_ToggleGrid.png" width="11" height="11" alt="Toggle Grid"> [Toggle Grid](#button-draft_togglegrid) | Small | â€” |

#### View tab

Use the **Design â†’ View** groups and sizes above; each mode activates its native view actions.

### Assembly Mode

#### Home tab

Component access, this mode's frequent operations, and shared utilities. File/Edit/Clipboard stay in the common toolbar above the ribbon.

##### Main group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_NewComponent.png" width="11" height="11" alt="New Component"> [New Component](#button-std_newcomponent) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [Add Component](#button-std_part) | Medium (half size) | â€” |
| <img src="toolbar-icons/PartDesign_NewSketch.png" width="11" height="11" alt="New Sketch"> [New Sketch](#button-partdesign_newsketch) | Medium (half size) | â€” |
| <img src="toolbar-icons/Part_CoordinateSystem.png" width="11" height="11" alt="Coordinate System"> [Coordinate System](#button-part_coordinatesystem) | Medium (half size) | Dropdown |
| â†³ <img src="toolbar-icons/Part_CoordinateSystem.png" width="11" height="11" alt="Coordinate System"> [Coordinate System](#button-part_coordinatesystem) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Part_DatumPlane.png" width="11" height="11" alt="Datum Plane"> [Datum Plane](#button-part_datumplane) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Part_DatumLine.png" width="11" height="11" alt="Datum Line"> [Datum Line](#button-part_datumline) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Part_DatumPoint.png" width="11" height="11" alt="Datum Point"> [Datum Point](#button-part_datumpoint) | Menu item | â€” |

##### Modeling group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/PartDesign_Extrude.png" width="11" height="11" alt="Extrude"> [Extrude](#button-partdesign_extrude) | Full size | â€” |
| <img src="toolbar-icons/PartDesign_Revolution.png" width="11" height="11" alt="Revolve"> [Revolve](#button-partdesign_revolution) | Full size | â€” |
| <img src="toolbar-icons/PartDesign_Fillet.png" width="11" height="11" alt="Fillet"> [Fillet](#button-partdesign_fillet) | Medium (half size) | â€” |
| <img src="toolbar-icons/PartDesign_Pattern.png" width="11" height="11" alt="Pattern"> [Pattern](#button-partdesign_pattern) | Medium (half size) | Dropdown |
| â†³ <img src="toolbar-icons/PartDesign_Pattern.png" width="11" height="11" alt="Pattern"> [Pattern](#button-partdesign_pattern) | Menu item | â€” |
| â†³ <img src="toolbar-icons/PartDesign_CircularPattern.png" width="11" height="11" alt="Circular Pattern"> [Circular Pattern](#button-partdesign_circularpattern) | Menu item | â€” |
| â†³ <img src="toolbar-icons/PartDesign_PathPattern.png" width="11" height="11" alt="Path Pattern"> [Path Pattern](#button-partdesign_pathpattern) | Menu item | â€” |
| â†³ <img src="toolbar-icons/PartDesign_PointPattern.png" width="11" height="11" alt="Point Pattern"> [Point Pattern](#button-partdesign_pointpattern) | Menu item | â€” |

##### Surface group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Surface_Filling.png" width="11" height="11" alt="Filling"> [Filling](#button-surface_filling) | Medium (half size) | â€” |
| <img src="toolbar-icons/Surface_GeomFillSurface.png" width="11" height="11" alt="Fill Boundary Curves"> [Fill Boundary Curves](#button-surface_geomfillsurface) | Medium (half size) | â€” |
| <img src="toolbar-icons/Surface_ExtendFace.png" width="11" height="11" alt="Extend Face"> [Extend Face](#button-surface_extendface) | Medium (half size) | â€” |

##### Sketch group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Sketcher_EditSketch.png" width="11" height="11" alt="Edit Sketch"> [Edit Sketch](#button-sketcher_editsketch) | Medium (half size) | â€” |
| <img src="toolbar-icons/Sketcher_MapSketch.png" width="11" height="11" alt="Attach Sketch"> [Attach Sketch](#button-sketcher_mapsketch) | Medium (half size) | â€” |
| <img src="toolbar-icons/Sketcher_CompLine.png" width="11" height="11" alt="Polyline"> [Polyline](#button-sketcher_compline) | Medium (half size) | Dropdown |
| â†³ Native choices for [Polyline](#button-sketcher_compline) | Menu items | See function catalog |
| <img src="toolbar-icons/Sketcher_CompCreateRectangles.png" width="11" height="11" alt="Rectangle"> [Rectangle](#button-sketcher_compcreaterectangles) | Medium (half size) | Dropdown |
| â†³ Native choices for [Rectangle](#button-sketcher_compcreaterectangles) | Menu items | See function catalog |
| <img src="toolbar-icons/Sketcher_Dimension.png" width="11" height="11" alt="Dimension"> [Auto Dimension](#button-sketcher_dimension) | Medium (half size) | Dropdown |
| â†³ <img src="toolbar-icons/Sketcher_Dimension.png" width="11" height="11" alt="Dimension"> [Auto Dimension](#button-sketcher_dimension) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Sketcher_ConstrainDistanceY.png" width="11" height="11" alt="Vertical Dimension"> [Vertical Dimension](#button-sketcher_constraindistancey) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Sketcher_ConstrainDistanceX.png" width="11" height="11" alt="Horizontal Dimension"> [Horizontal Dimension](#button-sketcher_constraindistancex) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Sketcher_ConstrainAngle.png" width="11" height="11" alt="Angle Dimension"> [Angle Dimension](#button-sketcher_constrainangle) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Sketcher_ConstrainRadius.png" width="11" height="11" alt="Radius Dimension"> [Radius Dimension](#button-sketcher_constrainradius) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Sketcher_ConstrainDiameter.png" width="11" height="11" alt="Diameter Dimension"> [Diameter Dimension](#button-sketcher_constraindiameter) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Sketcher_ConstrainDistance.png" width="11" height="11" alt="Distance Dimension"> [Distance Dimension](#button-sketcher_constraindistance) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Sketcher_ConstrainRadiam.png" width="11" height="11" alt="Radius/Diameter Dimension"> [Radius/Diameter Dimension](#button-sketcher_constrainradiam) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Sketcher_ConstrainLock.png" width="11" height="11" alt="Lock Position"> [Lock Position](#button-sketcher_constrainlock) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Sketcher_ConstrainSnellsLaw.png" width="11" height="11" alt="Refraction Constraint"> [Refraction Constraint](#button-sketcher_constrainsnellslaw) | Menu item | â€” |
| <img src="toolbar-icons/Sketcher_ToggleConstruction.png" width="11" height="11" alt="Toggle Construction Geometry"> [Toggle Construction Geometry](#button-sketcher_toggleconstruction) | Medium (half size) | â€” |

##### Assembly group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Assembly_CreateAssembly.png" width="11" height="11" alt="New Assembly"> [New Assembly](#button-assembly_createassembly) | Medium (half size) | â€” |
| <img src="toolbar-icons/Assembly_Insert.png" width="11" height="11" alt="Insert Component"> [Insert Component](#button-assembly_insert) | Medium (half size) | Dropdown |
| â†³ <img src="toolbar-icons/Assembly_InsertLink.png" width="11" height="11" alt="Insert Component"> [Insert Component](#button-assembly_insertlink) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_InsertNewPart.png" width="11" height="11" alt="Add Component"> [Add Component](#button-assembly_insertnewpart) | Menu item | â€” |
| <img src="toolbar-icons/Assembly_SolveAssembly.png" width="11" height="11" alt="Solve Assembly"> [Solve Assembly](#button-assembly_solveassembly) | Medium (half size) | â€” |
| <img src="toolbar-icons/Assembly_CreateJointFixed.png" width="11" height="11" alt="Fixed Joint"> [Fixed Joint](#button-assembly_createjointfixed) | Medium (half size) | Dropdown |
| â†³ <img src="toolbar-icons/Assembly_CreateJointRigidGroup.png" width="11" height="11" alt="Create Rigid Group"> [Create Rigid Group](#button-assembly_createjointrigidgroup) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointFixed.png" width="11" height="11" alt="Fixed Joint"> [Fixed Joint](#button-assembly_createjointfixed) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointRevolute.png" width="11" height="11" alt="Revolute Joint"> [Revolute Joint](#button-assembly_createjointrevolute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointCylindrical.png" width="11" height="11" alt="Cylindrical Joint"> [Cylindrical Joint](#button-assembly_createjointcylindrical) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointSlider.png" width="11" height="11" alt="Slider Joint"> [Slider Joint](#button-assembly_createjointslider) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointBall.png" width="11" height="11" alt="Ball Joint"> [Ball Joint](#button-assembly_createjointball) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointDistance.png" width="11" height="11" alt="Distance Joint"> [Distance Joint](#button-assembly_createjointdistance) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointParallel.png" width="11" height="11" alt="Parallel Joint"> [Parallel Joint](#button-assembly_createjointparallel) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointPerpendicular.png" width="11" height="11" alt="Perpendicular Joint"> [Perpendicular Joint](#button-assembly_createjointperpendicular) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointAngle.png" width="11" height="11" alt="Angle Joint"> [Angle Joint](#button-assembly_createjointangle) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointRackPinion.png" width="11" height="11" alt="Rack and Pinion Joint"> [Rack and Pinion Joint](#button-assembly_createjointrackpinion) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointScrew.png" width="11" height="11" alt="Screw Joint"> [Screw Joint](#button-assembly_createjointscrew) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointGears.png" width="11" height="11" alt="Gears Joint"> [Gears Joint](#button-assembly_createjointgears) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointBelt.png" width="11" height="11" alt="Belt Joint"> [Belt Joint](#button-assembly_createjointbelt) | Menu item | â€” |

##### Mesh group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Mesh_Import.png" width="11" height="11" alt="Import Meshâ€¦"> [Import Meshâ€¦](#button-mesh_import) | Medium (half size) | â€” |
| <img src="toolbar-icons/Mesh_FromPartShape.png" width="11" height="11" alt="Mesh From Shape"> [Mesh From Shape](#button-mesh_frompartshape) | Medium (half size) | â€” |
| <img src="toolbar-icons/Mesh_Evaluation.png" width="11" height="11" alt="Evaluate and Repair"> [Evaluate and Repair](#button-mesh_evaluation) | Medium (half size) | â€” |

##### View group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_ViewFitAll.png" width="11" height="11" alt="Fit All"> [Fit All](#button-std_viewfitall) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_ViewIsometric.png" width="11" height="11" alt="Isometric"> [Isometric](#button-std_viewisometric) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_DrawStyle.png" width="11" height="11" alt="As Is"> [As Is](#button-std_drawstyle) | Medium (half size) | Dropdown |
| â†³ Native choices for [As Is](#button-std_drawstyle) | Menu items | See function catalog |
| <img src="../../../src/Gui/Icons/view-select.svg" width="11" height="11" alt="Selection filtersâ€¦"> [Selection filtersâ€¦](#button-std_entityselectionfilter) | Medium (half size) | â€” |

##### Structure group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Small | â€” |
| <img src="toolbar-icons/Std_Group.png" width="11" height="11" alt="New Group"> [New Group](#button-std_group) | Small | â€” |
| <img src="toolbar-icons/Std_LinkActions.png" width="11" height="11" alt="Make Link"> [Make Link](#button-std_linkactions) | Small | Dropdown |
| â†³ Native choices for [Make Link](#button-std_linkactions) | Menu items | See function catalog |
| <img src="toolbar-icons/Std_VarSet.png" width="11" height="11" alt="Variable Set"> [Variable Set](#button-std_varset) | Small | â€” |
| <img src="toolbar-icons/PartDesign_AddReferenceObject.png" width="11" height="11" alt="Add Reference Object"> [Add Reference Object](#button-partdesign_addreferenceobject) | Small | â€” |

##### Utilities group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Import.png" width="11" height="11" alt="Importâ€¦"> [Importâ€¦](#button-std_import) | Small | â€” |
| <img src="toolbar-icons/Std_Export.png" width="11" height="11" alt="Exportâ€¦"> [Exportâ€¦](#button-std_export) | Small | â€” |
| <img src="toolbar-icons/Std_DlgPreferences.png" width="11" height="11" alt="Preferences"> [Preferences](#button-std_dlgpreferences) | Small | â€” |
| <img src="../../../src/Gui/Icons/zoom-in.svg" width="11" height="11" alt="Command search..."> [Command search...](#button-std_commandsearch) | Small | â€” |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | Small | â€” |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | Small | â€” |
| <img src="toolbar-icons/Std_Delete.png" width="11" height="11" alt="Delete"> [Delete](#button-std_delete) | Small | â€” |

##### Help group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Help | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> [What's This?](#button-std_whatsthis) | Menu item | â€” |

##### Macro group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Macro | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> [Record Macro](#button-std_dlgmacrorecord) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> [Macros](#button-std_dlgmacroexecute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> [Execute Macro](#button-std_dlgmacroexecutedirect) | Menu item | â€” |

#### Tools tab

##### Assembly group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Assembly_CreateAssembly.png" width="11" height="11" alt="New Assembly"> [New Assembly](#button-assembly_createassembly) | Small | â€” |
| <img src="toolbar-icons/Assembly_Insert.png" width="11" height="11" alt="Insert Component"> [Insert Component](#button-assembly_insert) | Small | Dropdown |
| â†³ <img src="toolbar-icons/Assembly_InsertLink.png" width="11" height="11" alt="Insert Component"> [Insert Component](#button-assembly_insertlink) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_InsertNewPart.png" width="11" height="11" alt="Add Component"> [Add Component](#button-assembly_insertnewpart) | Menu item | â€” |
| <img src="toolbar-icons/Part_LinkArrays.png" width="11" height="11" alt="Circular Link Array"> [Circular Link Array](#button-part_linkarrays) | Small | Dropdown |
| â†³ Native choices for [Circular Link Array](#button-part_linkarrays) | Menu items | See function catalog |
| <img src="toolbar-icons/Assembly_SolveAssembly.png" width="11" height="11" alt="Solve Assembly"> [Solve Assembly](#button-assembly_solveassembly) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateView.png" width="11" height="11" alt="Exploded View"> [Exploded View](#button-assembly_createview) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateSnapshot.png" width="11" height="11" alt="Snapshot"> [Snapshot](#button-assembly_createsnapshot) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateSimulation.png" width="11" height="11" alt="Simulation"> [Simulation](#button-assembly_createsimulation) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateBom.png" width="11" height="11" alt="Bill of Materials"> [Bill of Materials](#button-assembly_createbom) | Small | â€” |

##### Assembly Joints group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Assembly_ToggleGrounded.png" width="11" height="11" alt="Toggle Grounded"> [Toggle Grounded](#button-assembly_togglegrounded) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointRigidGroup.png" width="11" height="11" alt="Create Rigid Group"> [Create Rigid Group](#button-assembly_createjointrigidgroup) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointFixed.png" width="11" height="11" alt="Fixed Joint"> [Fixed Joint](#button-assembly_createjointfixed) | Small | Dropdown |
| â†³ <img src="toolbar-icons/Assembly_CreateJointRigidGroup.png" width="11" height="11" alt="Create Rigid Group"> [Create Rigid Group](#button-assembly_createjointrigidgroup) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointFixed.png" width="11" height="11" alt="Fixed Joint"> [Fixed Joint](#button-assembly_createjointfixed) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointRevolute.png" width="11" height="11" alt="Revolute Joint"> [Revolute Joint](#button-assembly_createjointrevolute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointCylindrical.png" width="11" height="11" alt="Cylindrical Joint"> [Cylindrical Joint](#button-assembly_createjointcylindrical) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointSlider.png" width="11" height="11" alt="Slider Joint"> [Slider Joint](#button-assembly_createjointslider) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointBall.png" width="11" height="11" alt="Ball Joint"> [Ball Joint](#button-assembly_createjointball) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointDistance.png" width="11" height="11" alt="Distance Joint"> [Distance Joint](#button-assembly_createjointdistance) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointParallel.png" width="11" height="11" alt="Parallel Joint"> [Parallel Joint](#button-assembly_createjointparallel) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointPerpendicular.png" width="11" height="11" alt="Perpendicular Joint"> [Perpendicular Joint](#button-assembly_createjointperpendicular) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointAngle.png" width="11" height="11" alt="Angle Joint"> [Angle Joint](#button-assembly_createjointangle) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointRackPinion.png" width="11" height="11" alt="Rack and Pinion Joint"> [Rack and Pinion Joint](#button-assembly_createjointrackpinion) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointScrew.png" width="11" height="11" alt="Screw Joint"> [Screw Joint](#button-assembly_createjointscrew) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointGears.png" width="11" height="11" alt="Gears Joint"> [Gears Joint](#button-assembly_createjointgears) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointBelt.png" width="11" height="11" alt="Belt Joint"> [Belt Joint](#button-assembly_createjointbelt) | Menu item | â€” |
| <img src="toolbar-icons/Assembly_CreateJointRevolute.png" width="11" height="11" alt="Revolute Joint"> [Revolute Joint](#button-assembly_createjointrevolute) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointCylindrical.png" width="11" height="11" alt="Cylindrical Joint"> [Cylindrical Joint](#button-assembly_createjointcylindrical) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointSlider.png" width="11" height="11" alt="Slider Joint"> [Slider Joint](#button-assembly_createjointslider) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointBall.png" width="11" height="11" alt="Ball Joint"> [Ball Joint](#button-assembly_createjointball) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointDistance.png" width="11" height="11" alt="Distance Joint"> [Distance Joint](#button-assembly_createjointdistance) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointParallel.png" width="11" height="11" alt="Parallel Joint"> [Parallel Joint](#button-assembly_createjointparallel) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointPerpendicular.png" width="11" height="11" alt="Perpendicular Joint"> [Perpendicular Joint](#button-assembly_createjointperpendicular) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointAngle.png" width="11" height="11" alt="Angle Joint"> [Angle Joint](#button-assembly_createjointangle) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointRackPinion.png" width="11" height="11" alt="Rack and Pinion Joint"> [Rack and Pinion Joint](#button-assembly_createjointrackpinion) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointScrew.png" width="11" height="11" alt="Screw Joint"> [Screw Joint](#button-assembly_createjointscrew) | Small | â€” |
| <img src="toolbar-icons/Assembly_CreateJointGearBelt.png" width="11" height="11" alt="Gears Joint"> [Gears Joint](#button-assembly_createjointgearbelt) | Small | Dropdown |
| â†³ <img src="toolbar-icons/Assembly_CreateJointGears.png" width="11" height="11" alt="Gears Joint"> [Gears Joint](#button-assembly_createjointgears) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Assembly_CreateJointBelt.png" width="11" height="11" alt="Belt Joint"> [Belt Joint](#button-assembly_createjointbelt) | Menu item | â€” |

#### View tab

Use the **Design â†’ View** groups and sizes above; each mode activates its native view actions.

### CAM Mode

#### Home tab

Component access, this mode's frequent operations, and shared utilities. File/Edit/Clipboard stay in the common toolbar above the ribbon.

##### Main group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [Add Component](#button-std_part) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Medium (half size) | â€” |

##### Frequent operations group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/CAM_Job.png" width="11" height="11" alt="New Job"> [New Job](#button-cam_job) | Medium (half size) | â€” |
| <img src="toolbar-icons/CAM_MeshPreparation.png" width="11" height="11" alt="Review CAM mesh..."> [Review CAM mesh...](#button-cam_meshpreparation) | Medium (half size) | â€” |
| <img src="toolbar-icons/CAM_Workplane.png" width="11" height="11" alt="Work Plane"> [Work Plane](#button-cam_workplane) | Medium (half size) | â€” |

##### Structure group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Small | â€” |
| <img src="toolbar-icons/Std_Group.png" width="11" height="11" alt="New Group"> [New Group](#button-std_group) | Small | â€” |
| <img src="toolbar-icons/Std_LinkActions.png" width="11" height="11" alt="Make Link"> [Make Link](#button-std_linkactions) | Small | Dropdown |
| â†³ Native choices for [Make Link](#button-std_linkactions) | Menu items | See function catalog |
| <img src="toolbar-icons/Std_VarSet.png" width="11" height="11" alt="Variable Set"> [Variable Set](#button-std_varset) | Small | â€” |
| <img src="toolbar-icons/PartDesign_AddReferenceObject.png" width="11" height="11" alt="Add Reference Object"> [Add Reference Object](#button-partdesign_addreferenceobject) | Small | â€” |

##### Utilities group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Import.png" width="11" height="11" alt="Importâ€¦"> [Importâ€¦](#button-std_import) | Small | â€” |
| <img src="toolbar-icons/Std_Export.png" width="11" height="11" alt="Exportâ€¦"> [Exportâ€¦](#button-std_export) | Small | â€” |
| <img src="toolbar-icons/Std_DlgPreferences.png" width="11" height="11" alt="Preferences"> [Preferences](#button-std_dlgpreferences) | Small | â€” |
| <img src="../../../src/Gui/Icons/zoom-in.svg" width="11" height="11" alt="Command search..."> [Command search...](#button-std_commandsearch) | Small | â€” |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | Small | â€” |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | Small | â€” |
| <img src="toolbar-icons/Std_Delete.png" width="11" height="11" alt="Delete"> [Delete](#button-std_delete) | Small | â€” |

##### Help group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Help | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> [What's This?](#button-std_whatsthis) | Menu item | â€” |

##### Macro group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Macro | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> [Record Macro](#button-std_dlgmacrorecord) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> [Macros](#button-std_dlgmacroexecute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> [Execute Macro](#button-std_dlgmacroexecutedirect) | Menu item | â€” |

#### Tools tab

##### Project Setup group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/CAM_Job.png" width="11" height="11" alt="New Job"> [New Job](#button-cam_job) | Full size | â€” |
| <img src="toolbar-icons/CAM_MeshPreparation.png" width="11" height="11" alt="Review CAM mesh..."> [Review CAM mesh...](#button-cam_meshpreparation) | Small | â€” |
| <img src="toolbar-icons/CAM_Workplane.png" width="11" height="11" alt="Work Plane"> [Work Plane](#button-cam_workplane) | Small | â€” |
| <img src="../../../src/Gui/Icons/preferences-general.svg" width="11" height="11" alt="Holding Tab"> [Holding Tab](#button-cam_holdingtab) | Small | â€” |
| <img src="toolbar-icons/CAM_IndexedSetup.png" width="11" height="11" alt="Indexed Setup"> [Indexed Setup](#button-cam_indexedsetup) | Small | â€” |
| <img src="toolbar-icons/CAM_Sanity.png" width="11" height="11" alt="Sanity Check"> [Sanity Check](#button-cam_sanity) | Small | â€” |
| <img src="toolbar-icons/CAM_PostTools.png" width="11" height="11" alt="Post Process"> [Post Process](#button-cam_posttools) | Small | Dropdown |
| â†³ Native choices for [Post Process](#button-cam_posttools) | Menu items | See function catalog |

##### Tool Commands group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/CAM_SimTools.png" width="11" height="11" alt="CAM Simulator"> [CAM Simulator](#button-cam_simtools) | Small | Dropdown |
| â†³ Native choices for [CAM Simulator](#button-cam_simtools) | Menu items | See function catalog |
| <img src="toolbar-icons/CAM_Inspect.png" width="11" height="11" alt="Inspect Toolpath"> [Inspect Toolpath](#button-cam_inspect) | Small | â€” |
| <img src="toolbar-icons/CAM_SelectLoop.png" width="11" height="11" alt="Finish Selecting Loop"> [Finish Selecting Loop](#button-cam_selectloop) | Small | â€” |
| <img src="toolbar-icons/CAM_OpActiveToggle.png" width="11" height="11" alt="Toggle Operation"> [Toggle Operation](#button-cam_opactivetoggle) | Small | â€” |
| <img src="toolbar-icons/CAM_ToolBitDock.png" width="11" height="11" alt="Add Toolbitâ€¦"> [Add Toolbitâ€¦](#button-cam_toolbitdock) | Small | â€” |

##### New Operations group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/CAM_Profile.png" width="11" height="11" alt="Profile"> [Profile](#button-cam_profile) | Small | â€” |
| <img src="toolbar-icons/CAM_Pocket_Shape.png" width="11" height="11" alt="Pocket Shape"> [Pocket Shape](#button-cam_pocket_shape) | Small | â€” |
| <img src="toolbar-icons/CAM_MillFacing.png" width="11" height="11" alt="Mill Facing"> [Mill Facing](#button-cam_millfacing) | Small | â€” |
| <img src="toolbar-icons/CAM_Helix.png" width="11" height="11" alt="Helix"> [Helix](#button-cam_helix) | Small | â€” |
| <img src="toolbar-icons/CAM_Adaptive.png" width="11" height="11" alt="Adaptive"> [Adaptive](#button-cam_adaptive) | Small | â€” |
| <img src="toolbar-icons/CAM_Slot.png" width="11" height="11" alt="Slot"> [Slot](#button-cam_slot) | Small | â€” |
| <img src="toolbar-icons/CAM_DrillingTools.png" width="11" height="11" alt="Drilling"> [Drilling](#button-cam_drillingtools) | Small | Dropdown |
| â†³ Native choices for [Drilling](#button-cam_drillingtools) | Menu items | See function catalog |
| <img src="toolbar-icons/CAM_EngraveTools.png" width="11" height="11" alt="Engrave"> [Engrave](#button-cam_engravetools) | Small | Dropdown |
| â†³ Native choices for [Engrave](#button-cam_engravetools) | Menu items | See function catalog |
| <img src="toolbar-icons/CAM_PlanarSurface.png" width="11" height="11" alt="Parallel / Waterline"> [Parallel / Waterline](#button-cam_planarsurface) | Small | â€” |

##### Path Modification group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/CAM_OperationCopy.png" width="11" height="11" alt="Copy Operation"> [Copy Operation](#button-cam_operationcopy) | Small | â€” |
| <img src="toolbar-icons/CAM_Array.png" width="11" height="11" alt="Array"> [Array](#button-cam_array) | Small | â€” |
| <img src="toolbar-icons/CAM_SimpleCopy.png" width="11" height="11" alt="Simple Copy"> [Simple Copy](#button-cam_simplecopy) | Small | â€” |
| <img src="toolbar-icons/CAM_DressupTools.png" width="11" height="11" alt="Array"> [Array](#button-cam_dressuptools) | Small | Dropdown |
| â†³ Native choices for [Array](#button-cam_dressuptools) | Menu items | See function catalog |

#### View tab

Use the **Design â†’ View** groups and sizes above; each mode activates its native view actions.

### TechDraw Mode

#### Home tab

Component access, this mode's frequent operations, and shared utilities. File/Edit/Clipboard stay in the common toolbar above the ribbon.

##### Main group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [Add Component](#button-std_part) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Medium (half size) | â€” |

##### Frequent operations group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_PageDefault.png" width="11" height="11" alt="New Page"> [New Page](#button-techdraw_pagedefault) | Medium (half size) | â€” |
| <img src="toolbar-icons/TechDraw_PageTemplate.png" width="11" height="11" alt="New Page From Template"> [New Page From Template](#button-techdraw_pagetemplate) | Medium (half size) | â€” |
| <img src="toolbar-icons/TechDraw_FillTemplateFields.png" width="11" height="11" alt="Update Template Fields"> [Update Template Fields](#button-techdraw_filltemplatefields) | Medium (half size) | â€” |

##### Structure group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Small | â€” |
| <img src="toolbar-icons/Std_Group.png" width="11" height="11" alt="New Group"> [New Group](#button-std_group) | Small | â€” |
| <img src="toolbar-icons/Std_LinkActions.png" width="11" height="11" alt="Make Link"> [Make Link](#button-std_linkactions) | Small | Dropdown |
| â†³ Native choices for [Make Link](#button-std_linkactions) | Menu items | See function catalog |
| <img src="toolbar-icons/Std_VarSet.png" width="11" height="11" alt="Variable Set"> [Variable Set](#button-std_varset) | Small | â€” |
| <img src="toolbar-icons/PartDesign_AddReferenceObject.png" width="11" height="11" alt="Add Reference Object"> [Add Reference Object](#button-partdesign_addreferenceobject) | Small | â€” |

##### Utilities group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Import.png" width="11" height="11" alt="Importâ€¦"> [Importâ€¦](#button-std_import) | Small | â€” |
| <img src="toolbar-icons/Std_Export.png" width="11" height="11" alt="Exportâ€¦"> [Exportâ€¦](#button-std_export) | Small | â€” |
| <img src="toolbar-icons/Std_DlgPreferences.png" width="11" height="11" alt="Preferences"> [Preferences](#button-std_dlgpreferences) | Small | â€” |
| <img src="../../../src/Gui/Icons/zoom-in.svg" width="11" height="11" alt="Command search..."> [Command search...](#button-std_commandsearch) | Small | â€” |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | Small | â€” |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | Small | â€” |
| <img src="toolbar-icons/Std_Delete.png" width="11" height="11" alt="Delete"> [Delete](#button-std_delete) | Small | â€” |

##### Help group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Help | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> [What's This?](#button-std_whatsthis) | Menu item | â€” |

##### Macro group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Macro | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> [Record Macro](#button-std_dlgmacrorecord) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> [Macros](#button-std_dlgmacroexecute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> [Execute Macro](#button-std_dlgmacroexecutedirect) | Menu item | â€” |

#### Tools tab

##### TechDraw Pages group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_PageDefault.png" width="11" height="11" alt="New Page"> [New Page](#button-techdraw_pagedefault) | Full size | â€” |
| <img src="toolbar-icons/TechDraw_PageTemplate.png" width="11" height="11" alt="New Page From Template"> [New Page From Template](#button-techdraw_pagetemplate) | Small | â€” |
| <img src="toolbar-icons/TechDraw_FillTemplateFields.png" width="11" height="11" alt="Update Template Fields"> [Update Template Fields](#button-techdraw_filltemplatefields) | Small | â€” |
| <img src="toolbar-icons/TechDraw_RedrawPage.png" width="11" height="11" alt="Redraw Page"> [Redraw Page](#button-techdraw_redrawpage) | Small | â€” |
| <img src="toolbar-icons/TechDraw_PrintAll.png" width="11" height="11" alt="Print All Pages"> [Print All Pages](#button-techdraw_printall) | Small | â€” |

##### TechDraw Views group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_View.png" width="11" height="11" alt="New View"> [New View](#button-techdraw_view) | Small | â€” |
| <img src="toolbar-icons/TechDraw_BrokenView.png" width="11" height="11" alt="Broken View"> [Broken View](#button-techdraw_brokenview) | Small | â€” |
| <img src="toolbar-icons/TechDraw_ActiveView.png" width="11" height="11" alt="Active View"> [Active View](#button-techdraw_activeview) | Small | â€” |
| <img src="toolbar-icons/TechDraw_SectionGroup.png" width="11" height="11" alt="Section View"> [Section View](#button-techdraw_sectiongroup) | Small | Dropdown |
| â†³ Native choices for [Section View](#button-techdraw_sectiongroup) | Menu items | See function catalog |
| <img src="toolbar-icons/TechDraw_DetailView.png" width="11" height="11" alt="Detail View"> [Detail View](#button-techdraw_detailview) | Small | â€” |
| <img src="toolbar-icons/TechDraw_DraftView.png" width="11" height="11" alt="Draft View"> [Draft View](#button-techdraw_draftview) | Small | â€” |
| <img src="toolbar-icons/TechDraw_SpreadsheetView.png" width="11" height="11" alt="Spreadsheet View"> [Spreadsheet View](#button-techdraw_spreadsheetview) | Small | â€” |
| <img src="toolbar-icons/TechDraw_ClipGroup.png" width="11" height="11" alt="Clip Group"> [Clip Group](#button-techdraw_clipgroup) | Small | â€” |

##### TechDraw Stacking group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_StackGroup.png" width="11" height="11" alt="Stack Top"> [Stack Top](#button-techdraw_stackgroup) | Small | Dropdown |
| â†³ Native choices for [Stack Top](#button-techdraw_stackgroup) | Menu items | See function catalog |

##### TechDraw Dimensions group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_CompDimensionTools.png" width="11" height="11" alt="Dimension"> [Dimension](#button-techdraw_compdimensiontools) | Small | Dropdown |
| â†³ Native choices for [Dimension](#button-techdraw_compdimensiontools) | Menu items | See function catalog |
| <img src="toolbar-icons/TechDraw_Balloon.png" width="11" height="11" alt="Balloon Annotation"> [Balloon Annotation](#button-techdraw_balloon) | Small | â€” |
| <img src="toolbar-icons/TechDraw_AxoLengthDimension.png" width="11" height="11" alt="Axonometric Length Dimension"> [Axonometric Length Dimension](#button-techdraw_axolengthdimension) | Small | â€” |
| <img src="toolbar-icons/TechDraw_DimensionRepair.png" width="11" height="11" alt="Repair Dimension References"> [Repair Dimension References](#button-techdraw_dimensionrepair) | Small | â€” |

##### TechDraw Attributes group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_ExtensionSelectLineAttributes.png" width="11" height="11" alt="Select Line Attributes, Cascade Spacing and Delta Distance"> [Select Line Attributes, Cascade Spacing and Delta Distance](#button-techdraw_extensionselectlineattributes) | Small | â€” |
| <img src="toolbar-icons/TechDraw_ExtensionChangeLineAttributes.png" width="11" height="11" alt="Change Line Attributes"> [Change Line Attributes](#button-techdraw_extensionchangelineattributes) | Small | â€” |
| <img src="toolbar-icons/TechDraw_ExtensionExtendShortenLineGroup.png" width="11" height="11" alt="Extend Line"> [Extend Line](#button-techdraw_extensionextendshortenlinegroup) | Small | Dropdown |
| â†³ Native choices for [Extend Line](#button-techdraw_extensionextendshortenlinegroup) | Menu items | See function catalog |
| <img src="toolbar-icons/TechDraw_ExtensionLockUnlockView.png" width="11" height="11" alt="Toggle View Lock"> [Toggle View Lock](#button-techdraw_extensionlockunlockview) | Small | â€” |
| <img src="toolbar-icons/TechDraw_ExtensionPositionSectionView.png" width="11" height="11" alt="Position Section View"> [Position Section View](#button-techdraw_extensionpositionsectionview) | Small | â€” |
| <img src="toolbar-icons/TechDraw_ExtensionCustomizeFormat.png" width="11" height="11" alt="Customize Format Label"> [Customize Format Label](#button-techdraw_extensioncustomizeformat) | Small | â€” |

##### TechDraw Centerlines group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_ExtensionCircleCenterLinesGroup.png" width="11" height="11" alt="Circle Centerlines"> [Circle Centerlines](#button-techdraw_extensioncirclecenterlinesgroup) | Small | Dropdown |
| â†³ Native choices for [Circle Centerlines](#button-techdraw_extensioncirclecenterlinesgroup) | Menu items | See function catalog |
| <img src="toolbar-icons/TechDraw_ExtensionThreadsGroup.png" width="11" height="11" alt="Cosmetic Thread Hole Side View"> [Cosmetic Thread Hole Side View](#button-techdraw_extensionthreadsgroup) | Small | Dropdown |
| â†³ Native choices for [Cosmetic Thread Hole Side View](#button-techdraw_extensionthreadsgroup) | Menu items | See function catalog |
| <img src="toolbar-icons/TechDraw_CommandVertexCreationGroup.png" width="11" height="11" alt="Cosmetic Intersection Vertices"> [Cosmetic Intersection Vertices](#button-techdraw_commandvertexcreationgroup) | Small | Dropdown |
| â†³ <img src="toolbar-icons/TechDraw_ExtensionVertexAtIntersection.png" width="11" height="11" alt="Cosmetic Intersection Vertices"> [Cosmetic Intersection Vertices](#button-techdraw_extensionvertexatintersection) | Menu item | â€” |
| â†³ <img src="toolbar-icons/TechDraw_CommandAddOffsetVertex.png" width="11" height="11" alt="Offset Vertex"> [Offset Vertex](#button-techdraw_commandaddoffsetvertex) | Menu item | â€” |
| <img src="toolbar-icons/TechDraw_ExtensionDrawCirclesGroup.png" width="11" height="11" alt="Cosmetic 1 Point Circle"> [Cosmetic 1 Point Circle](#button-techdraw_extensiondrawcirclesgroup) | Small | Dropdown |
| â†³ Native choices for [Cosmetic 1 Point Circle](#button-techdraw_extensiondrawcirclesgroup) | Menu items | See function catalog |
| <img src="toolbar-icons/TechDraw_ExtensionLinePPGroup.png" width="11" height="11" alt="Cosmetic Parallel Line"> [Cosmetic Parallel Line](#button-techdraw_extensionlineppgroup) | Small | Dropdown |
| â†³ Native choices for [Cosmetic Parallel Line](#button-techdraw_extensionlineppgroup) | Menu items | See function catalog |

##### TechDraw Extend Dimensions group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_ExtensionInsertPrefixGroup.png" width="11" height="11" alt="Insert &#x27;âŒ€&#x27; Prefix"> [Insert 'âŒ€' Prefix](#button-techdraw_extensioninsertprefixgroup) | Small | Dropdown |
| â†³ Native choices for [Insert 'âŒ€' Prefix](#button-techdraw_extensioninsertprefixgroup) | Menu items | See function catalog |
| <img src="toolbar-icons/TechDraw_ExtensionIncreaseDecreaseGroup.png" width="11" height="11" alt="Increase Decimal Places"> [Increase Decimal Places](#button-techdraw_extensionincreasedecreasegroup) | Small | Dropdown |
| â†³ Native choices for [Increase Decimal Places](#button-techdraw_extensionincreasedecreasegroup) | Menu items | See function catalog |

##### TechDraw File Access group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_ExportPageSVG.png" width="11" height="11" alt="Export Page as SVG"> [Export Page as SVG](#button-techdraw_exportpagesvg) | Small | â€” |
| <img src="toolbar-icons/TechDraw_ExportPageDXF.png" width="11" height="11" alt="Export Page as DXF"> [Export Page as DXF](#button-techdraw_exportpagedxf) | Small | â€” |

##### TechDraw Decoration group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_ToggleFrame.png" width="11" height="11" alt="Toggle View Frames"> [Toggle View Frames](#button-techdraw_toggleframe) | Small | â€” |
| <img src="toolbar-icons/TechDraw_Hatch.png" width="11" height="11" alt="Image Hatch"> [Image Hatch](#button-techdraw_hatch) | Small | â€” |
| <img src="toolbar-icons/TechDraw_GeometricHatch.png" width="11" height="11" alt="Geometric Hatch"> [Geometric Hatch](#button-techdraw_geometrichatch) | Small | â€” |

##### TechDraw Annotation group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/TechDraw_RichTextAnnotation.png" width="11" height="11" alt="Rich Text Annotation"> [Rich Text Annotation](#button-techdraw_richtextannotation) | Small | â€” |
| <img src="toolbar-icons/TechDraw_LeaderLine.png" width="11" height="11" alt="Leader Line"> [Leader Line](#button-techdraw_leaderline) | Small | â€” |
| <img src="toolbar-icons/TechDraw_CosmeticVertexGroup.png" width="11" height="11" alt="Cosmetic Vertex"> [Cosmetic Vertex](#button-techdraw_cosmeticvertexgroup) | Small | Dropdown |
| â†³ Native choices for [Cosmetic Vertex](#button-techdraw_cosmeticvertexgroup) | Menu items | See function catalog |
| <img src="toolbar-icons/TechDraw_CenterLineGroup.png" width="11" height="11" alt="Centerline on Face"> [Centerline on Face](#button-techdraw_centerlinegroup) | Small | Dropdown |
| â†³ Native choices for [Centerline on Face](#button-techdraw_centerlinegroup) | Menu items | See function catalog |
| <img src="toolbar-icons/TechDraw_2PointCosmeticLine.png" width="11" height="11" alt="Cosmetic Line Through 2 Points"> [Cosmetic Line Through 2 Points](#button-techdraw_2pointcosmeticline) | Small | â€” |
| <img src="toolbar-icons/TechDraw_DecorateLine.png" width="11" height="11" alt="Edit Line Appearance"> [Edit Line Appearance](#button-techdraw_decorateline) | Small | â€” |
| <img src="toolbar-icons/TechDraw_ShowAll.png" width="11" height="11" alt="Toggle Edge Visibility"> [Toggle Edge Visibility](#button-techdraw_showall) | Small | â€” |
| <img src="toolbar-icons/TechDraw_WeldSymbol.png" width="11" height="11" alt="Weld Symbol"> [Weld Symbol](#button-techdraw_weldsymbol) | Small | â€” |
| <img src="toolbar-icons/TechDraw_SurfaceFinishSymbols.png" width="11" height="11" alt="Surface Finish Symbol"> [Surface Finish Symbol](#button-techdraw_surfacefinishsymbols) | Small | â€” |
| <img src="toolbar-icons/TechDraw_HoleShaftFit.png" width="11" height="11" alt="Hole/Shaft Fit"> [Hole/Shaft Fit](#button-techdraw_holeshaftfit) | Small | â€” |

#### View tab

Use the **Design â†’ View** groups and sizes above; each mode activates its native view actions.

### FEM Mode

**Conditional / source-only:** show this mode only when its workbench is installed and registered.

#### Home tab

Component access, this mode's frequent operations, and shared utilities. File/Edit/Clipboard stay in the common toolbar above the ribbon.

##### Main group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [Add Component](#button-std_part) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Medium (half size) | â€” |

##### Frequent operations group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_Analysis.svg" width="11" height="11" alt="New Analysis"> [New Analysis](#button-fem_analysis) | Medium (half size) | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialSolid.svg" width="11" height="11" alt="Solid Material"> [Solid Material](#button-fem_materialsolid) | Medium (half size) | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialFluid.svg" width="11" height="11" alt="Fluid Material"> [Fluid Material](#button-fem_materialfluid) | Medium (half size) | â€” |

##### Utilities group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Import.png" width="11" height="11" alt="Importâ€¦"> [Importâ€¦](#button-std_import) | Small | â€” |
| <img src="toolbar-icons/Std_Export.png" width="11" height="11" alt="Exportâ€¦"> [Exportâ€¦](#button-std_export) | Small | â€” |
| <img src="toolbar-icons/Std_DlgPreferences.png" width="11" height="11" alt="Preferences"> [Preferences](#button-std_dlgpreferences) | Small | â€” |
| <img src="../../../src/Gui/Icons/zoom-in.svg" width="11" height="11" alt="Command search..."> [Command search...](#button-std_commandsearch) | Small | â€” |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | Small | â€” |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | Small | â€” |
| <img src="toolbar-icons/Std_Delete.png" width="11" height="11" alt="Delete"> [Delete](#button-std_delete) | Small | â€” |

##### Help group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Help | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> [What's This?](#button-std_whatsthis) | Menu item | â€” |

##### Macro group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Macro | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> [Record Macro](#button-std_dlgmacrorecord) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> [Macros](#button-std_dlgmacroexecute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> [Execute Macro](#button-std_dlgmacroexecutedirect) | Menu item | â€” |

#### Tools tab

##### Model group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_Analysis.svg" width="11" height="11" alt="New Analysis"> [New Analysis](#button-fem_analysis) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialSolid.svg" width="11" height="11" alt="Solid Material"> [Solid Material](#button-fem_materialsolid) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialFluid.svg" width="11" height="11" alt="Fluid Material"> [Fluid Material](#button-fem_materialfluid) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialMechanicalNonlinear.svg" width="11" height="11" alt="Non-Linear Mechanical Material"> [Non-Linear Mechanical Material](#button-fem_materialmechanicalnonlinear) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialReinforced.svg" width="11" height="11" alt="Reinforced Material (Concrete)"> [Reinforced Material (Concrete)](#button-fem_materialreinforced) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Material_Group.svg" width="11" height="11" alt="Material Editor"> [Material Editor](#button-fem_materialeditor) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementGeometry1D.svg" width="11" height="11" alt="Beam Cross Section"> [Beam Cross Section](#button-fem_elementgeometry1d) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementRotation1D.svg" width="11" height="11" alt="Beam Rotation"> [Beam Rotation](#button-fem_elementrotation1d) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementGeometry2D.svg" width="11" height="11" alt="Shell Plate Thickness"> [Shell Plate Thickness](#button-fem_elementgeometry2d) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementFluid1D.svg" width="11" height="11" alt="Fluid Section for 1D Flow"> [Fluid Section for 1D Flow](#button-fem_elementfluid1d) | Small | â€” |

##### Electromagnetic Boundary Conditions group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| â€” [Electromagnetic Boundary Conditions](#button-fem_compemconstraints) | Small | Dropdown |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintElectromagnetic.svg" width="11" height="11" alt="Electromagnetic Boundary Condition"> [Electromagnetic Boundary Condition](#button-fem_constraintelectromagnetic) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintCurrentDensity.svg" width="11" height="11" alt="Current Density Boundary Condition"> [Current Density Boundary Condition](#button-fem_constraintcurrentdensity) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintMagnetization.svg" width="11" height="11" alt="Magnetization Boundary Condition"> [Magnetization Boundary Condition](#button-fem_constraintmagnetization) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintElectricChargeDensity.svg" width="11" height="11" alt="Electric Charge Density"> [Electric Charge Density](#button-fem_constraintelectricchargedensity) | Menu item | â€” |

##### Fluid Boundary Conditions group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialFlowVelocity.svg" width="11" height="11" alt="Initial Flow Velocity Condition"> [Initial Flow Velocity Condition](#button-fem_constraintinitialflowvelocity) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialPressure.svg" width="11" height="11" alt="Initial Pressure Condition"> [Initial Pressure Condition](#button-fem_constraintinitialpressure) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintFlowVelocity.svg" width="11" height="11" alt="Flow Velocity Boundary Condition"> [Flow Velocity Boundary Condition](#button-fem_constraintflowvelocity) | Small | â€” |

##### Geometrical Analysis Features group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintPlaneRotation.svg" width="11" height="11" alt="Plane Multi-Point Constraint"> [Plane Multi-Point Constraint](#button-fem_constraintplanerotation) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSectionPrint.svg" width="11" height="11" alt="Section Print Feature"> [Section Print Feature](#button-fem_constraintsectionprint) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTransform.svg" width="11" height="11" alt="Local Coordinate System"> [Local Coordinate System](#button-fem_constrainttransform) | Small | â€” |

##### Mechanical Boundary Conditions and Loads group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintFixed.svg" width="11" height="11" alt="Fixed Boundary Condition"> [Fixed Boundary Condition](#button-fem_constraintfixed) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintRigidBody.svg" width="11" height="11" alt="Rigid Body Constraint"> [Rigid Body Constraint](#button-fem_constraintrigidbody) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintDisplacement.svg" width="11" height="11" alt="Displacement Boundary Condition"> [Displacement Boundary Condition](#button-fem_constraintdisplacement) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintContact.svg" width="11" height="11" alt="Contact Constraint"> [Contact Constraint](#button-fem_constraintcontact) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTie.svg" width="11" height="11" alt="Tie Constraint"> [Tie Constraint](#button-fem_constrainttie) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSpring.svg" width="11" height="11" alt="Spring Boundary Condition"> [Spring Boundary Condition](#button-fem_constraintspring) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintForce.svg" width="11" height="11" alt="Force Load"> [Force Load](#button-fem_constraintforce) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintPressure.svg" width="11" height="11" alt="Pressure Load"> [Pressure Load](#button-fem_constraintpressure) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintCentrif.svg" width="11" height="11" alt="Centrifugal Load"> [Centrifugal Load](#button-fem_constraintcentrif) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSelfWeight.svg" width="11" height="11" alt="Gravity Load"> [Gravity Load](#button-fem_constraintselfweight) | Small | â€” |

##### Thermal Boundary Conditions and Loads group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialTemperature.svg" width="11" height="11" alt="Initial Temperature"> [Initial Temperature](#button-fem_constraintinitialtemperature) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintHeatflux.svg" width="11" height="11" alt="Heat Flux Load"> [Heat Flux Load](#button-fem_constraintheatflux) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTemperature.svg" width="11" height="11" alt="Temperature Boundary Condition"> [Temperature Boundary Condition](#button-fem_constrainttemperature) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintBodyHeatSource.svg" width="11" height="11" alt="Body Heat Source"> [Body Heat Source](#button-fem_constraintbodyheatsource) | Small | â€” |

##### Mesh group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshNetgenFromShape.svg" width="11" height="11" alt="Mesh From Shape by Netgen"> [Mesh From Shape by Netgen](#button-fem_meshnetgenfromshape) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshGmshFromShape.svg" width="11" height="11" alt="Mesh From Shape by Gmsh"> [Mesh From Shape by Gmsh](#button-fem_meshgmshfromshape) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshRegion.svg" width="11" height="11" alt="Mesh Refinement"> [Mesh Refinement](#button-fem_meshregion) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshGroup.svg" width="11" height="11" alt="Mesh Group"> [Mesh Group](#button-fem_meshgroup) | Small | â€” |
| â€” [GMSH Refinements](#button-fem_meshgmshrefinement) | Small | Dropdown |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshDistance.svg" width="11" height="11" alt="Distance-Based Refinement"> [Distance-Based Refinement](#button-fem_meshdistance) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshBoundaryLayer.svg" width="11" height="11" alt="2D Boundary Layer"> [2D Boundary Layer](#button-fem_meshboundarylayer) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshShape.svg" width="11" height="11" alt="Shape-Based Refinement"> [Shape-Based Refinement](#button-fem_meshshape) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshManipulate.svg" width="11" height="11" alt="Manipulate Refinement"> [Manipulate Refinement](#button-fem_meshmanipulate) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshAdvanced.svg" width="11" height="11" alt="Advanced Refinement Types"> [Advanced Refinement Types](#button-fem_meshadvanced) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshTransfiniteCurve.svg" width="11" height="11" alt="Structured Transfinite Curve"> [Structured Transfinite Curve](#button-fem_meshtransfinitecurve) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshTransfiniteSurface.svg" width="11" height="11" alt="Structured Transfinite Surface"> [Structured Transfinite Surface](#button-fem_meshtransfinitesurface) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshTransfiniteVolume.svg" width="11" height="11" alt="Structured Transfinite Volume"> [Structured Transfinite Volume](#button-fem_meshtransfinitevolume) | Menu item | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_FEMMesh2Mesh.svg" width="11" height="11" alt="FEM Mesh to Mesh"> [FEM Mesh to Mesh](#button-fem_femmesh2mesh) | Small | â€” |

##### Solve group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| â€” [Solvers](#button-fem_compsolvers) | Small | Dropdown |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverStandard.svg" width="11" height="11" alt="Solver CalculiX"> [Solver CalculiX](#button-fem_solvercalculix) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverElmer.svg" width="11" height="11" alt="Solver Elmer"> [Solver Elmer](#button-fem_solverelmer) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverMystran.svg" width="11" height="11" alt="Solver Mystran"> [Solver Mystran](#button-fem_solvermystran) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverZ88.svg" width="11" height="11" alt="Solver Z88"> [Solver Z88](#button-fem_solverz88) | Menu item | â€” |
| â€” [Mechanical Equations](#button-fem_compmechequations) | Small | Dropdown |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationElasticity.svg" width="11" height="11" alt="Elasticity Equation"> [Elasticity Equation](#button-fem_equationelasticity) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationDeformation.svg" width="11" height="11" alt="Deformation Equation"> [Deformation Equation](#button-fem_equationdeformation) | Menu item | â€” |
| â€” [Electromagnetic Equations](#button-fem_compemequations) | Small | Dropdown |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationElectrostatic.svg" width="11" height="11" alt="Electrostatic Equation"> [Electrostatic Equation](#button-fem_equationelectrostatic) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationElectricforce.svg" width="11" height="11" alt="Electricforce Equation"> [Electricforce Equation](#button-fem_equationelectricforce) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationMagnetodynamic.svg" width="11" height="11" alt="Magnetodynamic Equation"> [Magnetodynamic Equation](#button-fem_equationmagnetodynamic) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationMagnetodynamic2D.svg" width="11" height="11" alt="Magnetodynamic 2D Equation"> [Magnetodynamic 2D Equation](#button-fem_equationmagnetodynamic2d) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationStaticCurrent.svg" width="11" height="11" alt="Static Current Equation"> [Static Current Equation](#button-fem_equationstaticcurrent) | Menu item | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationFlow.svg" width="11" height="11" alt="Flow Equation"> [Flow Equation](#button-fem_equationflow) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationFlux.svg" width="11" height="11" alt="Flux Equation"> [Flux Equation](#button-fem_equationflux) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationHeat.svg" width="11" height="11" alt="Heat Equation"> [Heat Equation](#button-fem_equationheat) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverControl.svg" width="11" height="11" alt="Solver Job Control"> [Solver Job Control](#button-fem_solvercontrol) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverRun.svg" width="11" height="11" alt="Run Solver"> [Run Solver](#button-fem_solverrun) | Small | â€” |

##### Results group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ResultsPurge.svg" width="11" height="11" alt="Purge Results"> [Purge Results](#button-fem_resultspurge) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ResultShow.svg" width="11" height="11" alt="Show Result"> [Show Result](#button-fem_resultshow) | Small | â€” |
| <img src="../../../src/Gui/Icons/view-refresh.svg" width="11" height="11" alt="Apply Changes to Pipeline"> [Apply Changes to Pipeline](#button-fem_postapplychanges) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostPipelineFromResult.svg" width="11" height="11" alt="Post Pipeline From Result"> [Post Pipeline From Result](#button-fem_postpipelinefromresult) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostBranchFilter.svg" width="11" height="11" alt="Pipeline Branch"> [Pipeline Branch](#button-fem_postbranchfilter) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterWarp.svg" width="11" height="11" alt="Warp Filter"> [Warp Filter](#button-fem_postfilterwarp) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterClipScalar.svg" width="11" height="11" alt="Scalar Clip Filter"> [Scalar Clip Filter](#button-fem_postfilterclipscalar) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterCutFunction.svg" width="11" height="11" alt="Function Cut Filter"> [Function Cut Filter](#button-fem_postfiltercutfunction) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterClipRegion.svg" width="11" height="11" alt="Region Clip Filter"> [Region Clip Filter](#button-fem_postfilterclipregion) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterContours.svg" width="11" height="11" alt="Contours Filter"> [Contours Filter](#button-fem_postfiltercontours) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterGlyph.svg" width="11" height="11" alt="Glyph Filter"> [Glyph Filter](#button-fem_postfilterglyph) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterDataAlongLine.svg" width="11" height="11" alt="Line Clip Filter"> [Line Clip Filter](#button-fem_postfilterdataalongline) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterLinearizedStresses.svg" width="11" height="11" alt="Stress Linearization Plot"> [Stress Linearization Plot](#button-fem_postfilterlinearizedstresses) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterDataAtPoint.svg" width="11" height="11" alt="Data at Point Clip Filter"> [Data at Point Clip Filter](#button-fem_postfilterdataatpoint) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterCalculator.svg" width="11" height="11" alt="Calculator Filter"> [Calculator Filter](#button-fem_postfiltercalculator) | Small | â€” |
| â€” [Filter Functions](#button-fem_postcreatefunctions) | Small | â€” |
| â€” [Data Visualizations](#button-fem_postvisualization) | Small | â€” |

##### Utilities group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ClippingPlaneAdd.svg" width="11" height="11" alt="Clipping Plane on Face"> [Clipping Plane on Face](#button-fem_clippingplaneadd) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ClippingPlaneRemoveAll.svg" width="11" height="11" alt="Remove All Clipping Planes"> [Remove All Clipping Planes](#button-fem_clippingplaneremoveall) | Small | â€” |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FemWorkbench.svg" width="11" height="11" alt="FEM Examples"> [FEM Examples](#button-fem_examples) | Small | â€” |

#### View tab

Use the **Design â†’ View** groups and sizes above; each mode activates its native view actions.

### Spreadsheet Mode

#### Home tab

Component access, this mode's frequent operations, and shared utilities. File/Edit/Clipboard stay in the common toolbar above the ribbon.

##### Main group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [Add Component](#button-std_part) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Medium (half size) | â€” |

##### Frequent operations group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Spreadsheet_CreateSheet.png" width="11" height="11" alt="New Spreadsheet"> [New Spreadsheet](#button-spreadsheet_createsheet) | Medium (half size) | â€” |
| <img src="toolbar-icons/Spreadsheet_Import.png" width="11" height="11" alt="Import Spreadsheet"> [Import Spreadsheet](#button-spreadsheet_import) | Medium (half size) | â€” |
| <img src="toolbar-icons/Spreadsheet_Export.png" width="11" height="11" alt="Export Spreadsheet"> [Export Spreadsheet](#button-spreadsheet_export) | Medium (half size) | â€” |

##### Structure group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Small | â€” |
| <img src="toolbar-icons/Std_Group.png" width="11" height="11" alt="New Group"> [New Group](#button-std_group) | Small | â€” |
| <img src="toolbar-icons/Std_LinkActions.png" width="11" height="11" alt="Make Link"> [Make Link](#button-std_linkactions) | Small | Dropdown |
| â†³ Native choices for [Make Link](#button-std_linkactions) | Menu items | See function catalog |
| <img src="toolbar-icons/Std_VarSet.png" width="11" height="11" alt="Variable Set"> [Variable Set](#button-std_varset) | Small | â€” |
| <img src="toolbar-icons/PartDesign_AddReferenceObject.png" width="11" height="11" alt="Add Reference Object"> [Add Reference Object](#button-partdesign_addreferenceobject) | Small | â€” |

##### Utilities group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Import.png" width="11" height="11" alt="Importâ€¦"> [Importâ€¦](#button-std_import) | Small | â€” |
| <img src="toolbar-icons/Std_Export.png" width="11" height="11" alt="Exportâ€¦"> [Exportâ€¦](#button-std_export) | Small | â€” |
| <img src="toolbar-icons/Std_DlgPreferences.png" width="11" height="11" alt="Preferences"> [Preferences](#button-std_dlgpreferences) | Small | â€” |
| <img src="../../../src/Gui/Icons/zoom-in.svg" width="11" height="11" alt="Command search..."> [Command search...](#button-std_commandsearch) | Small | â€” |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | Small | â€” |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | Small | â€” |
| <img src="toolbar-icons/Std_Delete.png" width="11" height="11" alt="Delete"> [Delete](#button-std_delete) | Small | â€” |

##### Help group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Help | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> [What's This?](#button-std_whatsthis) | Menu item | â€” |

##### Macro group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Macro | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> [Record Macro](#button-std_dlgmacrorecord) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> [Macros](#button-std_dlgmacroexecute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> [Execute Macro](#button-std_dlgmacroexecutedirect) | Menu item | â€” |

#### Tools tab

##### Spreadsheet group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Spreadsheet_CreateSheet.png" width="11" height="11" alt="New Spreadsheet"> [New Spreadsheet](#button-spreadsheet_createsheet) | Small | â€” |
| <img src="toolbar-icons/Spreadsheet_Import.png" width="11" height="11" alt="Import Spreadsheet"> [Import Spreadsheet](#button-spreadsheet_import) | Small | â€” |
| <img src="toolbar-icons/Spreadsheet_Export.png" width="11" height="11" alt="Export Spreadsheet"> [Export Spreadsheet](#button-spreadsheet_export) | Small | â€” |
| <img src="toolbar-icons/Spreadsheet_MergeCells.png" width="11" height="11" alt="Merge Cells"> [Merge Cells](#button-spreadsheet_mergecells) | Small | â€” |
| <img src="toolbar-icons/Spreadsheet_SplitCell.png" width="11" height="11" alt="Split Cell"> [Split Cell](#button-spreadsheet_splitcell) | Small | â€” |
| <img src="toolbar-icons/Spreadsheet_AlignLeft.png" width="11" height="11" alt="Align Left"> [Align Left](#button-spreadsheet_alignleft) | Small | â€” |
| <img src="toolbar-icons/Spreadsheet_AlignCenter.png" width="11" height="11" alt="Align Horizontal Center"> [Align Horizontal Center](#button-spreadsheet_aligncenter) | Small | â€” |
| <img src="toolbar-icons/Spreadsheet_AlignRight.png" width="11" height="11" alt="Align Right"> [Align Right](#button-spreadsheet_alignright) | Small | â€” |
| <img src="toolbar-icons/Spreadsheet_AlignTop.png" width="11" height="11" alt="Align Top"> [Align Top](#button-spreadsheet_aligntop) | Small | â€” |
| <img src="toolbar-icons/Spreadsheet_AlignVCenter.png" width="11" height="11" alt="Align Vertical Center"> [Align Vertical Center](#button-spreadsheet_alignvcenter) | Small | â€” |
| <img src="toolbar-icons/Spreadsheet_AlignBottom.png" width="11" height="11" alt="Align Bottom"> [Align Bottom](#button-spreadsheet_alignbottom) | Small | â€” |
| <img src="toolbar-icons/Spreadsheet_StyleBold.png" width="11" height="11" alt="Bold Text"> [Bold Text](#button-spreadsheet_stylebold) | Small | â€” |
| <img src="toolbar-icons/Spreadsheet_StyleItalic.png" width="11" height="11" alt="Italic Text"> [Italic Text](#button-spreadsheet_styleitalic) | Small | â€” |
| <img src="toolbar-icons/Spreadsheet_StyleUnderline.png" width="11" height="11" alt="Underline Text"> [Underline Text](#button-spreadsheet_styleunderline) | Small | â€” |
| <img src="toolbar-icons/Spreadsheet_SetAlias.png" width="11" height="11" alt="Set Alias"> [Set Alias](#button-spreadsheet_setalias) | Small | â€” |

#### View tab

Use the **Design â†’ View** groups and sizes above; each mode activates its native view actions.

### Material Mode

#### Home tab

Component access, this mode's frequent operations, and shared utilities. File/Edit/Clipboard stay in the common toolbar above the ribbon.

##### Main group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [Add Component](#button-std_part) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Medium (half size) | â€” |

##### Frequent operations group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Material_Edit.png" width="11" height="11" alt="Edit"> [Edit](#button-material_edit) | Medium (half size) | â€” |

##### Structure group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Small | â€” |
| <img src="toolbar-icons/Std_Group.png" width="11" height="11" alt="New Group"> [New Group](#button-std_group) | Small | â€” |
| <img src="toolbar-icons/Std_LinkActions.png" width="11" height="11" alt="Make Link"> [Make Link](#button-std_linkactions) | Small | Dropdown |
| â†³ Native choices for [Make Link](#button-std_linkactions) | Menu items | See function catalog |
| <img src="toolbar-icons/Std_VarSet.png" width="11" height="11" alt="Variable Set"> [Variable Set](#button-std_varset) | Small | â€” |
| <img src="toolbar-icons/PartDesign_AddReferenceObject.png" width="11" height="11" alt="Add Reference Object"> [Add Reference Object](#button-partdesign_addreferenceobject) | Small | â€” |

##### Utilities group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Import.png" width="11" height="11" alt="Importâ€¦"> [Importâ€¦](#button-std_import) | Small | â€” |
| <img src="toolbar-icons/Std_Export.png" width="11" height="11" alt="Exportâ€¦"> [Exportâ€¦](#button-std_export) | Small | â€” |
| <img src="toolbar-icons/Std_DlgPreferences.png" width="11" height="11" alt="Preferences"> [Preferences](#button-std_dlgpreferences) | Small | â€” |
| <img src="../../../src/Gui/Icons/zoom-in.svg" width="11" height="11" alt="Command search..."> [Command search...](#button-std_commandsearch) | Small | â€” |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | Small | â€” |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | Small | â€” |
| <img src="toolbar-icons/Std_Delete.png" width="11" height="11" alt="Delete"> [Delete](#button-std_delete) | Small | â€” |

##### Help group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Help | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> [What's This?](#button-std_whatsthis) | Menu item | â€” |

##### Macro group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Macro | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> [Record Macro](#button-std_dlgmacrorecord) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> [Macros](#button-std_dlgmacroexecute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> [Execute Macro](#button-std_dlgmacroexecutedirect) | Menu item | â€” |

#### Tools tab

##### Material group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Material_Edit.png" width="11" height="11" alt="Edit"> [Edit](#button-material_edit) | Small | â€” |

#### View tab

Use the **Design â†’ View** groups and sizes above; each mode activates its native view actions.

### MeshPart Mode

**Conditional / source-only:** show this mode only when its workbench is installed and registered.

#### Home tab

Component access, this mode's frequent operations, and shared utilities. File/Edit/Clipboard stay in the common toolbar above the ribbon.

##### Main group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [Add Component](#button-std_part) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Medium (half size) | â€” |

##### Frequent operations group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Gui/Icons/preferences-general.svg" width="11" height="11" alt="Mesh From Shape"> [Mesh From Shape](#button-meshpart_mesher) | Medium (half size) | â€” |

##### Utilities group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Import.png" width="11" height="11" alt="Importâ€¦"> [Importâ€¦](#button-std_import) | Small | â€” |
| <img src="toolbar-icons/Std_Export.png" width="11" height="11" alt="Exportâ€¦"> [Exportâ€¦](#button-std_export) | Small | â€” |
| <img src="toolbar-icons/Std_DlgPreferences.png" width="11" height="11" alt="Preferences"> [Preferences](#button-std_dlgpreferences) | Small | â€” |
| <img src="../../../src/Gui/Icons/zoom-in.svg" width="11" height="11" alt="Command search..."> [Command search...](#button-std_commandsearch) | Small | â€” |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | Small | â€” |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | Small | â€” |
| <img src="toolbar-icons/Std_Delete.png" width="11" height="11" alt="Delete"> [Delete](#button-std_delete) | Small | â€” |

##### Help group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Help | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> [What's This?](#button-std_whatsthis) | Menu item | â€” |

##### Macro group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Macro | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> [Record Macro](#button-std_dlgmacrorecord) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> [Macros](#button-std_dlgmacroexecute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> [Execute Macro](#button-std_dlgmacroexecutedirect) | Menu item | â€” |

#### Tools tab

##### MeshPart group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Gui/Icons/preferences-general.svg" width="11" height="11" alt="Mesh From Shape"> [Mesh From Shape](#button-meshpart_mesher) | Small | â€” |

#### View tab

Use the **Design â†’ View** groups and sizes above; each mode activates its native view actions.

### Points Mode

**Conditional / source-only:** show this mode only when its workbench is installed and registered.

#### Home tab

Component access, this mode's frequent operations, and shared utilities. File/Edit/Clipboard stay in the common toolbar above the ribbon.

##### Main group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [Add Component](#button-std_part) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Medium (half size) | â€” |

##### Frequent operations group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Import_Point_cloud.svg" width="11" height="11" alt="Import Pointsâ€¦"> [Import Pointsâ€¦](#button-points_import) | Medium (half size) | â€” |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Export_Point_cloud.svg" width="11" height="11" alt="Export Pointsâ€¦"> [Export Pointsâ€¦](#button-points_export) | Medium (half size) | â€” |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Convert.svg" width="11" height="11" alt="Convert to Points"> [Convert to Points](#button-points_convert) | Medium (half size) | â€” |

##### Utilities group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Import.png" width="11" height="11" alt="Importâ€¦"> [Importâ€¦](#button-std_import) | Small | â€” |
| <img src="toolbar-icons/Std_Export.png" width="11" height="11" alt="Exportâ€¦"> [Exportâ€¦](#button-std_export) | Small | â€” |
| <img src="toolbar-icons/Std_DlgPreferences.png" width="11" height="11" alt="Preferences"> [Preferences](#button-std_dlgpreferences) | Small | â€” |
| <img src="../../../src/Gui/Icons/zoom-in.svg" width="11" height="11" alt="Command search..."> [Command search...](#button-std_commandsearch) | Small | â€” |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | Small | â€” |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | Small | â€” |
| <img src="toolbar-icons/Std_Delete.png" width="11" height="11" alt="Delete"> [Delete](#button-std_delete) | Small | â€” |

##### Help group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Help | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> [What's This?](#button-std_whatsthis) | Menu item | â€” |

##### Macro group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Macro | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> [Record Macro](#button-std_dlgmacrorecord) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> [Macros](#button-std_dlgmacroexecute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> [Execute Macro](#button-std_dlgmacroexecutedirect) | Menu item | â€” |

#### Tools tab

##### Points Tools group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Import_Point_cloud.svg" width="11" height="11" alt="Import Pointsâ€¦"> [Import Pointsâ€¦](#button-points_import) | Small | â€” |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Export_Point_cloud.svg" width="11" height="11" alt="Export Pointsâ€¦"> [Export Pointsâ€¦](#button-points_export) | Small | â€” |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Convert.svg" width="11" height="11" alt="Convert to Points"> [Convert to Points](#button-points_convert) | Small | â€” |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Structure.svg" width="11" height="11" alt="Structured Point Cloud"> [Structured Point Cloud](#button-points_structure) | Small | â€” |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Merge.svg" width="11" height="11" alt="Merge Point Clouds"> [Merge Point Clouds](#button-points_merge) | Small | â€” |
| <img src="../../../src/Gui/Icons/PolygonPick.svg" width="11" height="11" alt="Cut Point Cloud"> [Cut Point Cloud](#button-points_polycut) | Small | â€” |

#### View tab

Use the **Design â†’ View** groups and sizes above; each mode activates its native view actions.

### Robot Mode

**Conditional / source-only:** show this mode only when its workbench is installed and registered.

#### Home tab

Component access, this mode's frequent operations, and shared utilities. File/Edit/Clipboard stay in the common toolbar above the ribbon.

##### Main group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [Add Component](#button-std_part) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Medium (half size) | â€” |

##### Frequent operations group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_CreateRobot.svg" width="11" height="11" alt="Place Robot"> [Place Robot](#button-robot_create) | Medium (half size) | â€” |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_CreateTrajectory.svg" width="11" height="11" alt="Trajectory"> [Trajectory](#button-robot_createtrajectory) | Medium (half size) | â€” |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_InsertWaypoint.svg" width="11" height="11" alt="Insert in Trajectory"> [Insert in Trajectory](#button-robot_insertwaypoint) | Medium (half size) | â€” |

##### Utilities group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Import.png" width="11" height="11" alt="Importâ€¦"> [Importâ€¦](#button-std_import) | Small | â€” |
| <img src="toolbar-icons/Std_Export.png" width="11" height="11" alt="Exportâ€¦"> [Exportâ€¦](#button-std_export) | Small | â€” |
| <img src="toolbar-icons/Std_DlgPreferences.png" width="11" height="11" alt="Preferences"> [Preferences](#button-std_dlgpreferences) | Small | â€” |
| <img src="../../../src/Gui/Icons/zoom-in.svg" width="11" height="11" alt="Command search..."> [Command search...](#button-std_commandsearch) | Small | â€” |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | Small | â€” |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | Small | â€” |
| <img src="toolbar-icons/Std_Delete.png" width="11" height="11" alt="Delete"> [Delete](#button-std_delete) | Small | â€” |

##### Help group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Help | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> [What's This?](#button-std_whatsthis) | Menu item | â€” |

##### Macro group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Macro | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> [Record Macro](#button-std_dlgmacrorecord) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> [Macros](#button-std_dlgmacroexecute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> [Execute Macro](#button-std_dlgmacroexecutedirect) | Menu item | â€” |

#### Tools tab

##### Robot group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_CreateRobot.svg" width="11" height="11" alt="Place Robot"> [Place Robot](#button-robot_create) | Small | â€” |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_CreateTrajectory.svg" width="11" height="11" alt="Trajectory"> [Trajectory](#button-robot_createtrajectory) | Small | â€” |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_InsertWaypoint.svg" width="11" height="11" alt="Insert in Trajectory"> [Insert in Trajectory](#button-robot_insertwaypoint) | Small | â€” |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_InsertWaypointPre.svg" width="11" height="11" alt="Insert in Trajectory"> [Insert in Trajectory](#button-robot_insertwaypointpreselect) | Small | â€” |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_Edge2Trac.svg" width="11" height="11" alt="Edge to Trajectory"> [Edge to Trajectory](#button-robot_edge2trac) | Small | â€” |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_TrajectoryDressUp.svg" width="11" height="11" alt="Dress-Up Trajectory"> [Dress-Up Trajectory](#button-robot_trajectorydressup) | Small | â€” |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_TrajectoryCompound.svg" width="11" height="11" alt="Trajectory Compound"> [Trajectory Compound](#button-robot_trajectorycompound) | Small | â€” |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_SetHomePos.svg" width="11" height="11" alt="Set Home Position"> [Set Home Position](#button-robot_sethomepos) | Small | â€” |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_RestoreHomePos.svg" width="11" height="11" alt="Move to Home"> [Move to Home](#button-robot_restorehomepos) | Small | â€” |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_Simulate.svg" width="11" height="11" alt="Simulate Trajectory"> [Simulate Trajectory](#button-robot_simulate) | Small | â€” |

#### View tab

Use the **Design â†’ View** groups and sizes above; each mode activates its native view actions.

### ReverseEngineering Mode

**Conditional / source-only:** show this mode only when its workbench is installed and registered.

#### Home tab

Component access, this mode's frequent operations, and shared utilities. File/Edit/Clipboard stay in the common toolbar above the ribbon.

##### Main group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [Add Component](#button-std_part) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Medium (half size) | â€” |

##### Frequent operations group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/ReverseEngineering/Gui/Resources/icons/actions/FitSurface.svg" width="11" height="11" alt="Approximate B-Spline Surfaceâ€¦"> [Approximate B-Spline Surfaceâ€¦](#button-reen_approxsurface) | Medium (half size) | â€” |

##### Utilities group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Import.png" width="11" height="11" alt="Importâ€¦"> [Importâ€¦](#button-std_import) | Small | â€” |
| <img src="toolbar-icons/Std_Export.png" width="11" height="11" alt="Exportâ€¦"> [Exportâ€¦](#button-std_export) | Small | â€” |
| <img src="toolbar-icons/Std_DlgPreferences.png" width="11" height="11" alt="Preferences"> [Preferences](#button-std_dlgpreferences) | Small | â€” |
| <img src="../../../src/Gui/Icons/zoom-in.svg" width="11" height="11" alt="Command search..."> [Command search...](#button-std_commandsearch) | Small | â€” |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | Small | â€” |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | Small | â€” |
| <img src="toolbar-icons/Std_Delete.png" width="11" height="11" alt="Delete"> [Delete](#button-std_delete) | Small | â€” |

##### Help group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Help | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> [What's This?](#button-std_whatsthis) | Menu item | â€” |

##### Macro group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Macro | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> [Record Macro](#button-std_dlgmacrorecord) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> [Macros](#button-std_dlgmacroexecute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> [Execute Macro](#button-std_dlgmacroexecutedirect) | Menu item | â€” |

#### Tools tab

##### Reverse Engineering group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/ReverseEngineering/Gui/Resources/icons/actions/FitSurface.svg" width="11" height="11" alt="Approximate B-Spline Surfaceâ€¦"> [Approximate B-Spline Surfaceâ€¦](#button-reen_approxsurface) | Small | â€” |

#### View tab

Use the **Design â†’ View** groups and sizes above; each mode activates its native view actions.

### Inspection Mode

**Conditional / source-only:** show this mode only when its workbench is installed and registered.

#### Home tab

Component access, this mode's frequent operations, and shared utilities. File/Edit/Clipboard stay in the common toolbar above the ribbon.

##### Main group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [Add Component](#button-std_part) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Medium (half size) | â€” |

##### Frequent operations group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/Inspection/Gui/Resources/icons/InspectionWorkbench.svg" width="11" height="11" alt="Visual Inspection"> [Visual Inspection](#button-inspection_visualinspection) | Medium (half size) | â€” |
| <img src="../../../src/Mod/Inspection/Gui/Resources/icons/inspect_pipette.svg" width="11" height="11" alt="Inspectionâ€¦"> [Inspectionâ€¦](#button-inspection_inspectelement) | Medium (half size) | â€” |

##### Utilities group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Import.png" width="11" height="11" alt="Importâ€¦"> [Importâ€¦](#button-std_import) | Small | â€” |
| <img src="toolbar-icons/Std_Export.png" width="11" height="11" alt="Exportâ€¦"> [Exportâ€¦](#button-std_export) | Small | â€” |
| <img src="toolbar-icons/Std_DlgPreferences.png" width="11" height="11" alt="Preferences"> [Preferences](#button-std_dlgpreferences) | Small | â€” |
| <img src="../../../src/Gui/Icons/zoom-in.svg" width="11" height="11" alt="Command search..."> [Command search...](#button-std_commandsearch) | Small | â€” |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | Small | â€” |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | Small | â€” |
| <img src="toolbar-icons/Std_Delete.png" width="11" height="11" alt="Delete"> [Delete](#button-std_delete) | Small | â€” |

##### Help group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Help | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> [What's This?](#button-std_whatsthis) | Menu item | â€” |

##### Macro group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Macro | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> [Record Macro](#button-std_dlgmacrorecord) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> [Macros](#button-std_dlgmacroexecute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> [Execute Macro](#button-std_dlgmacroexecutedirect) | Menu item | â€” |

#### Tools tab

##### Inspection group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/Inspection/Gui/Resources/icons/InspectionWorkbench.svg" width="11" height="11" alt="Visual Inspection"> [Visual Inspection](#button-inspection_visualinspection) | Small | â€” |
| <img src="../../../src/Mod/Inspection/Gui/Resources/icons/inspect_pipette.svg" width="11" height="11" alt="Inspectionâ€¦"> [Inspectionâ€¦](#button-inspection_inspectelement) | Small | â€” |

#### View tab

Use the **Design â†’ View** groups and sizes above; each mode activates its native view actions.

### BIM Mode

**Conditional / source-only:** show this mode only when its workbench is installed and registered.

#### Home tab

Component access, this mode's frequent operations, and shared utilities. File/Edit/Clipboard stay in the common toolbar above the ribbon.

##### Main group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [Add Component](#button-std_part) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Medium (half size) | â€” |

##### Frequent operations group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/BIM/Resources/icons/Sketch.svg" width="11" height="11" alt="New Sketch"> [New Sketch](#button-bim_sketch) | Medium (half size) | â€” |
| <img src="toolbar-icons/Draft_Line.png" width="11" height="11" alt="Line"> [Line](#button-draft_line) | Medium (half size) | â€” |
| <img src="toolbar-icons/Draft_Wire.png" width="11" height="11" alt="Polyline"> [Polyline](#button-draft_wire) | Medium (half size) | â€” |

##### Utilities group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Import.png" width="11" height="11" alt="Importâ€¦"> [Importâ€¦](#button-std_import) | Small | â€” |
| <img src="toolbar-icons/Std_Export.png" width="11" height="11" alt="Exportâ€¦"> [Exportâ€¦](#button-std_export) | Small | â€” |
| <img src="toolbar-icons/Std_DlgPreferences.png" width="11" height="11" alt="Preferences"> [Preferences](#button-std_dlgpreferences) | Small | â€” |
| <img src="../../../src/Gui/Icons/zoom-in.svg" width="11" height="11" alt="Command search..."> [Command search...](#button-std_commandsearch) | Small | â€” |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | Small | â€” |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | Small | â€” |
| <img src="toolbar-icons/Std_Delete.png" width="11" height="11" alt="Delete"> [Delete](#button-std_delete) | Small | â€” |

##### Help group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Help | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> [What's This?](#button-std_whatsthis) | Menu item | â€” |

##### Macro group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Macro | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> [Record Macro](#button-std_dlgmacrorecord) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> [Macros](#button-std_dlgmacroexecute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> [Execute Macro](#button-std_dlgmacroexecutedirect) | Menu item | â€” |

#### Tools tab

##### Drafting Tools group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/BIM/Resources/icons/Sketch.svg" width="11" height="11" alt="New Sketch"> [New Sketch](#button-bim_sketch) | Small | â€” |
| <img src="toolbar-icons/Draft_Line.png" width="11" height="11" alt="Line"> [Line](#button-draft_line) | Full size | â€” |
| <img src="toolbar-icons/Draft_Wire.png" width="11" height="11" alt="Polyline"> [Polyline](#button-draft_wire) | Full size | â€” |
| <img src="toolbar-icons/Draft_Rectangle.png" width="11" height="11" alt="Rectangle"> [Rectangle](#button-draft_rectangle) | Small | â€” |
| <img src="../../../src/Mod/Draft/Resources/icons/Draft_Arc.svg" width="11" height="11" alt="Arc Tools"> [Arc Tools](#button-bim_arctools) | Small | Dropdown |
| â†³ <img src="toolbar-icons/Draft_Arc.png" width="11" height="11" alt="Arc"> [Arc](#button-draft_arc) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_Arc_3Points.png" width="11" height="11" alt="Arc From 3 Points"> [Arc From 3 Points](#button-draft_arc_3points) | Menu item | â€” |
| <img src="toolbar-icons/Draft_Circle.png" width="11" height="11" alt="Circle"> [Circle](#button-draft_circle) | Small | â€” |
| <img src="toolbar-icons/Draft_Ellipse.png" width="11" height="11" alt="Ellipse"> [Ellipse](#button-draft_ellipse) | Small | â€” |
| <img src="toolbar-icons/Draft_Polygon.png" width="11" height="11" alt="Polygon"> [Polygon](#button-draft_polygon) | Small | â€” |
| <img src="../../../src/Mod/Draft/Resources/icons/Draft_BSpline.svg" width="11" height="11" alt="Spline Tools"> [Spline Tools](#button-bim_splinetools) | Small | Dropdown |
| â†³ <img src="toolbar-icons/Draft_BSpline.png" width="11" height="11" alt="B-Spline"> [B-Spline](#button-draft_bspline) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_BezCurve.png" width="11" height="11" alt="BÃ©zier Curve"> [BÃ©zier Curve](#button-draft_bezcurve) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_CubicBezCurve.png" width="11" height="11" alt="Cubic BÃ©zier Curve"> [Cubic BÃ©zier Curve](#button-draft_cubicbezcurve) | Menu item | â€” |
| <img src="toolbar-icons/Draft_Point.png" width="11" height="11" alt="Point"> [Point](#button-draft_point) | Small | â€” |
| <img src="toolbar-icons/Draft_Fillet.png" width="11" height="11" alt="Fillet"> [Fillet](#button-draft_fillet) | Small | â€” |

##### Draft Snap group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Draft_Snap_Lock.png" width="11" height="11" alt="Snap Lock"> [Snap Lock](#button-draft_snap_lock) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Endpoint.png" width="11" height="11" alt="Snap Endpoint"> [Snap Endpoint](#button-draft_snap_endpoint) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Midpoint.png" width="11" height="11" alt="Snap Midpoint"> [Snap Midpoint](#button-draft_snap_midpoint) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Center.png" width="11" height="11" alt="Snap Center"> [Snap Center](#button-draft_snap_center) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Angle.png" width="11" height="11" alt="Snap Angle"> [Snap Angle](#button-draft_snap_angle) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Intersection.png" width="11" height="11" alt="Snap Intersection"> [Snap Intersection](#button-draft_snap_intersection) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Perpendicular.png" width="11" height="11" alt="Snap Perpendicular"> [Snap Perpendicular](#button-draft_snap_perpendicular) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Extension.png" width="11" height="11" alt="Snap Extension"> [Snap Extension](#button-draft_snap_extension) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Parallel.png" width="11" height="11" alt="Snap Parallel"> [Snap Parallel](#button-draft_snap_parallel) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Special.png" width="11" height="11" alt="Snap Special"> [Snap Special](#button-draft_snap_special) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Near.png" width="11" height="11" alt="Snap Near"> [Snap Near](#button-draft_snap_near) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Ortho.png" width="11" height="11" alt="Snap Ortho"> [Snap Ortho](#button-draft_snap_ortho) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Grid.png" width="11" height="11" alt="Snap Grid"> [Snap Grid](#button-draft_snap_grid) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_WorkingPlane.png" width="11" height="11" alt="Snap Working Plane"> [Snap Working Plane](#button-draft_snap_workingplane) | Small | â€” |
| <img src="toolbar-icons/Draft_Snap_Dimensions.png" width="11" height="11" alt="Snap Dimensions"> [Snap Dimensions](#button-draft_snap_dimensions) | Small | â€” |
| <img src="toolbar-icons/Draft_ToggleGrid.png" width="11" height="11" alt="Toggle Grid"> [Toggle Grid](#button-draft_togglegrid) | Small | â€” |

##### 3D/BIM Tools group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Site.svg" width="11" height="11" alt="Site"> [Site](#button-arch_site) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Building.svg" width="11" height="11" alt="Building"> [Building](#button-arch_building) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Floor.svg" width="11" height="11" alt="Level"> [Level](#button-arch_level) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Space.svg" width="11" height="11" alt="Space"> [Space](#button-arch_space) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Wall.svg" width="11" height="11" alt="Wall"> [Wall](#button-arch_wall) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_CurtainWall.svg" width="11" height="11" alt="Curtain Wall"> [Curtain Wall](#button-arch_curtainwall) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Column.svg" width="11" height="11" alt="Column"> [Column](#button-bim_column) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Beam.svg" width="11" height="11" alt="Beam"> [Beam](#button-bim_beam) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Slab.svg" width="11" height="11" alt="Slab"> [Slab](#button-bim_slab) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Door.svg" width="11" height="11" alt="Door"> [Door](#button-bim_door) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Window.svg" width="11" height="11" alt="Window"> [Window](#button-arch_window) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Covering.svg" width="11" height="11" alt="Covering"> [Covering](#button-bim_covering) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Pipe.svg" width="11" height="11" alt="Pipe"> [Pipe](#button-arch_pipe) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_PipeConnector.svg" width="11" height="11" alt="Connector"> [Connector](#button-arch_pipeconnector) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Stairs.svg" width="11" height="11" alt="Stairs"> [Stairs](#button-arch_stairs) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Roof.svg" width="11" height="11" alt="Roof"> [Roof](#button-arch_roof) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Panel.svg" width="11" height="11" alt="Panel"> [Panel](#button-arch_panel) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Frame.svg" width="11" height="11" alt="Frame"> [Frame](#button-arch_frame) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Fence.svg" width="11" height="11" alt="Fence"> [Fence](#button-arch_fence) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Truss.svg" width="11" height="11" alt="Truss"> [Truss](#button-arch_truss) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Equipment.svg" width="11" height="11" alt="Equipment"> [Equipment](#button-arch_equipment) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Rebar.svg" width="11" height="11" alt="Custom Rebar"> [Custom Rebar](#button-arch_rebar) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Box.svg" width="11" height="11" alt="Generic 3D Tools"> [Generic 3D Tools](#button-bim_generictools) | Small | Dropdown |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/Arch_Profile.svg" width="11" height="11" alt="Profile"> [Profile](#button-arch_profile) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/BIM_Box.svg" width="11" height="11" alt="Box"> [Box](#button-bim_box) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Part/Gui/Resources/icons/create/Part_Shapebuilder.svg" width="11" height="11" alt="Shape Builder"> [Shape Builder](#button-bim_builder) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_Facebinder.png" width="11" height="11" alt="Facebinder"> [Facebinder](#button-draft_facebinder) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/BIM_Library.svg" width="11" height="11" alt="Objects Library"> [Objects Library](#button-bim_library) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/Arch_Component.svg" width="11" height="11" alt="Component"> [Component](#button-arch_component) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/Arch_Reference.svg" width="11" height="11" alt="External Reference"> [External Reference](#button-arch_reference) | Menu item | â€” |

##### Annotation Tools group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_DimensionAligned.svg" width="11" height="11" alt="Aligned Dimension"> [Aligned Dimension](#button-bim_dimensionaligned) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_DimensionHorizontal.svg" width="11" height="11" alt="Horizontal Dimension"> [Horizontal Dimension](#button-bim_dimensionhorizontal) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_DimensionVertical.svg" width="11" height="11" alt="Vertical Dimension"> [Vertical Dimension](#button-bim_dimensionvertical) | Small | â€” |
| <img src="../../../src/Mod/Draft/Resources/icons/Draft_Text.svg" width="11" height="11" alt="Text"> [Text](#button-bim_text) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Leader.svg" width="11" height="11" alt="Leader"> [Leader](#button-bim_leader) | Small | â€” |
| <img src="toolbar-icons/Draft_Label.png" width="11" height="11" alt="Label"> [Label](#button-draft_label) | Small | â€” |
| <img src="toolbar-icons/Draft_Hatch.png" width="11" height="11" alt="Hatch"> [Hatch](#button-draft_hatch) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Axis.svg" width="11" height="11" alt="Axis Tools"> [Axis Tools](#button-bim_axistools) | Small | Dropdown |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/Arch_Axis.svg" width="11" height="11" alt="Axis"> [Axis](#button-arch_axis) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/Arch_Axis_System.svg" width="11" height="11" alt="Axis System"> [Axis System](#button-arch_axissystem) | Menu item | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Grid.svg" width="11" height="11" alt="Grid"> [Grid](#button-arch_grid) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_SectionPlane.svg" width="11" height="11" alt="Section Plane"> [Section Plane](#button-arch_sectionplane) | Small | â€” |
| â€” [Create 2D Views](#button-bim_create2dviews) | Small | Dropdown |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/BIM_ArchView.svg" width="11" height="11" alt="2D Drawing"> [2D Drawing](#button-bim_drawingview) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/Arch_BuildingPart_Tree.svg" width="11" height="11" alt="Section View"> [Section View](#button-bim_shape2dview) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/Arch_View_Cut.svg" width="11" height="11" alt="Section Cut"> [Section Cut](#button-bim_shape2dcut) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_UpdateShape2DView.png" width="11" height="11" alt="Force 2D View Update"> [Force 2D View Update](#button-draft_updateshape2dview) | Menu item | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_PageDefault.svg" width="11" height="11" alt="New Page"> [New Page](#button-bim_tdpage) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_InsertView.svg" width="11" height="11" alt="New View"> [New View](#button-bim_tdview) | Small | â€” |

##### General Tools group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Draft_Move.png" width="11" height="11" alt="Move"> [Move](#button-draft_move) | Small | â€” |
| <img src="toolbar-icons/Draft_Rotate.png" width="11" height="11" alt="Rotate"> [Rotate](#button-draft_rotate) | Small | â€” |
| <img src="toolbar-icons/Draft_Scale.png" width="11" height="11" alt="Scale"> [Scale](#button-draft_scale) | Small | â€” |
| <img src="toolbar-icons/Draft_Mirror.png" width="11" height="11" alt="Mirror"> [Mirror](#button-draft_mirror) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Clone.svg" width="11" height="11" alt="Cloning Tools"> [Cloning Tools](#button-bim_clonetools) | Small | Dropdown |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/BIM_Clone.svg" width="11" height="11" alt="Clone"> [Clone](#button-bim_clone) | Menu item | â€” |
| â†³ <img src="../../../src/Gui/Icons/Link.svg" width="11" height="11" alt="Make Link"> [Make Link](#button-bim_linkmake) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/BIM_Unclone.svg" width="11" height="11" alt="Unclone"> [Unclone](#button-bim_unclone) | Menu item | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Copy.svg" width="11" height="11" alt="Copy"> [Copy](#button-bim_copy) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Tree_Part.svg" width="11" height="11" alt="Simple Copy"> [Simple Copy](#button-bim_simplecopy) | Small | â€” |
| <img src="../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Compound.svg" width="11" height="11" alt="Compound"> [Compound](#button-bim_compound) | Small | â€” |

##### 2D Tools group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| â€” [Offset Tools](#button-bim_offsettools) | Small | Dropdown |
| â†³ <img src="../../../src/Mod/Part/Gui/Resources/icons/tools/Part_Offset2D.svg" width="11" height="11" alt="2D Offset"> [2D Offset](#button-bim_offset2d) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_Offset.png" width="11" height="11" alt="Offset"> [Offset](#button-draft_offset) | Menu item | â€” |
| <img src="../../../src/Mod/Draft/Resources/icons/Draft_Trimex.svg" width="11" height="11" alt="Trimex"> [Trimex](#button-bim_trimex) | Small | â€” |
| <img src="toolbar-icons/Draft_Join.png" width="11" height="11" alt="Join"> [Join](#button-draft_join) | Small | â€” |
| <img src="toolbar-icons/Draft_Split.png" width="11" height="11" alt="Split"> [Split](#button-draft_split) | Small | â€” |
| <img src="toolbar-icons/Draft_Stretch.png" width="11" height="11" alt="Stretch"> [Stretch](#button-draft_stretch) | Small | â€” |
| <img src="toolbar-icons/Draft_Draft2Sketch.png" width="11" height="11" alt="Draft to Sketch"> [Draft to Sketch](#button-draft_draft2sketch) | Small | â€” |
| <img src="toolbar-icons/Draft_Edit.png" width="11" height="11" alt="Edit"> [Edit](#button-draft_edit) | Small | â€” |

##### Object Tools group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Draft_Upgrade.png" width="11" height="11" alt="Upgrade"> [Upgrade](#button-draft_upgrade) | Small | â€” |
| <img src="toolbar-icons/Draft_Downgrade.png" width="11" height="11" alt="Downgrade"> [Downgrade](#button-draft_downgrade) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Add.svg" width="11" height="11" alt="Add Component"> [Add Component](#button-arch_add) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Remove.svg" width="11" height="11" alt="Remove Component"> [Remove Component](#button-arch_remove) | Small | â€” |

##### 3D Tools group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/Draft/Resources/icons/Draft_Array.svg" width="11" height="11" alt="Array Tools"> [Array Tools](#button-bim_arraytools) | Small | Dropdown |
| â†³ <img src="toolbar-icons/Draft_OrthoArray.png" width="11" height="11" alt="Array"> [Array](#button-draft_orthoarray) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_PathLinkArray.png" width="11" height="11" alt="Path Link Array"> [Path Link Array](#button-draft_pathlinkarray) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_PolarArray.png" width="11" height="11" alt="Polar Array"> [Polar Array](#button-draft_polararray) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Draft_PointLinkArray.png" width="11" height="11" alt="Point Link Array"> [Point Link Array](#button-draft_pointlinkarray) | Menu item | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_CutPlane.svg" width="11" height="11" alt="Cut With Plane"> [Cut With Plane](#button-arch_cutplane) | Small | â€” |
| <img src="../../../src/Mod/Part/Gui/Resources/icons/tools/Part_Extrude.svg" width="11" height="11" alt="Extrude"> [Extrude](#button-bim_extrude) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_ExtrudeFace.svg" width="11" height="11" alt="Extrude Face"> [Extrude Face](#button-bim_extrudeface) | Small | â€” |
| â€” [Boolean Tools](#button-bim_booleantools) | Small | Dropdown |
| â†³ <img src="../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Fuse.svg" width="11" height="11" alt="Union"> [Union](#button-bim_fuse) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Cut.svg" width="11" height="11" alt="Difference"> [Difference](#button-bim_cut) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Common.svg" width="11" height="11" alt="Intersection"> [Intersection](#button-bim_common) | Menu item | â€” |

##### Manage Tools group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Gui/Icons/preferences-system.svg" width="11" height="11" alt="BIM Setup"> [BIM Setup](#button-bim_setup) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_ProjectManager.svg" width="11" height="11" alt="Setup Project"> [Setup Project](#button-bim_projectmanager) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Windows.svg" width="11" height="11" alt="Manage Doors and Windows"> [Manage Doors and Windows](#button-bim_windows) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_IfcElements.svg" width="11" height="11" alt="IFC Management"> [IFC Management](#button-bim_ifcmanagetools) | Small | Dropdown |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/BIM_IfcElements.svg" width="11" height="11" alt="Manage IFC Elements"> [Manage IFC Elements](#button-bim_ifcelements) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/BIM_IfcQuantities.svg" width="11" height="11" alt="Manage IFC Quantities"> [Manage IFC Quantities](#button-bim_ifcquantities) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/BIM_IfcProperties.svg" width="11" height="11" alt="Manage IFC Properties"> [Manage IFC Properties](#button-bim_ifcproperties) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/BIM_Classification.svg" width="11" height="11" alt="Manage Classification"> [Manage Classification](#button-bim_classification) | Menu item | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Layers.svg" width="11" height="11" alt="Manage Layers"> [Manage Layers](#button-bim_layers) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Material.svg" width="11" height="11" alt="Material"> [Material](#button-bim_material) | Small | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Report.svg" width="11" height="11" alt="Report Tools"> [Report Tools](#button-bim_reporttools) | Small | Dropdown |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/BIM_Report.svg" width="11" height="11" alt="Report"> [Report](#button-bim_report) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/Arch_Schedule.svg" width="11" height="11" alt="Schedule"> [Schedule](#button-arch_schedule) | Menu item | â€” |
| â†³ <img src="../../../src/Mod/BIM/Resources/icons/Arch_Survey.svg" width="11" height="11" alt="Survey"> [Survey](#button-arch_survey) | Menu item | â€” |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Preflight.svg" width="11" height="11" alt="Preflight Checks"> [Preflight Checks](#button-bim_preflight) | Small | â€” |
| <img src="toolbar-icons/Draft_AnnotationStyleEditor.png" width="11" height="11" alt="Annotation Styles"> [Annotation Styles](#button-draft_annotationstyleeditor) | Small | â€” |

#### View tab

Use the **Design â†’ View** groups and sizes above; each mode activates its native view actions.

### OpenSCAD Mode

**Conditional / source-only:** show this mode only when its workbench is installed and registered.

#### Home tab

Component access, this mode's frequent operations, and shared utilities. File/Edit/Clipboard stay in the common toolbar above the ribbon.

##### Main group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [Add Component](#button-std_part) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Medium (half size) | â€” |

##### Frequent operations group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_ReplaceObject.svg" width="11" height="11" alt="Replace Object"> [Replace Object](#button-openscad_replaceobject) | Medium (half size) | â€” |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_RemoveSubtree.svg" width="11" height="11" alt="Remove Objects and Children"> [Remove Objects and Children](#button-openscad_removesubtree) | Medium (half size) | â€” |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Explode_Group.svg" width="11" height="11" alt="Explode Group"> [Explode Group](#button-openscad_explodegroup) | Medium (half size) | â€” |

##### Utilities group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Import.png" width="11" height="11" alt="Importâ€¦"> [Importâ€¦](#button-std_import) | Small | â€” |
| <img src="toolbar-icons/Std_Export.png" width="11" height="11" alt="Exportâ€¦"> [Exportâ€¦](#button-std_export) | Small | â€” |
| <img src="toolbar-icons/Std_DlgPreferences.png" width="11" height="11" alt="Preferences"> [Preferences](#button-std_dlgpreferences) | Small | â€” |
| <img src="../../../src/Gui/Icons/zoom-in.svg" width="11" height="11" alt="Command search..."> [Command search...](#button-std_commandsearch) | Small | â€” |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | Small | â€” |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | Small | â€” |
| <img src="toolbar-icons/Std_Delete.png" width="11" height="11" alt="Delete"> [Delete](#button-std_delete) | Small | â€” |

##### Help group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Help | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> [What's This?](#button-std_whatsthis) | Menu item | â€” |

##### Macro group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Macro | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> [Record Macro](#button-std_dlgmacrorecord) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> [Macros](#button-std_dlgmacroexecute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> [Execute Macro](#button-std_dlgmacroexecutedirect) | Menu item | â€” |

#### Tools tab

##### OpenSCAD Tools group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_ReplaceObject.svg" width="11" height="11" alt="Replace Object"> [Replace Object](#button-openscad_replaceobject) | Small | â€” |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_RemoveSubtree.svg" width="11" height="11" alt="Remove Objects and Children"> [Remove Objects and Children](#button-openscad_removesubtree) | Small | â€” |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Explode_Group.svg" width="11" height="11" alt="Explode Group"> [Explode Group](#button-openscad_explodegroup) | Small | â€” |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_RefineShapeFeature.svg" width="11" height="11" alt="Refine Shape Feature"> [Refine Shape Feature](#button-openscad_refineshapefeature) | Small | â€” |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_IncreaseToleranceFeature.svg" width="11" height="11" alt="Increase Tolerance Feature"> [Increase Tolerance Feature](#button-openscad_increasetolerancefeature) | Small | â€” |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_AddOpenSCADElement.svg" width="11" height="11" alt="Add OpenSCAD Element"> [Add OpenSCAD Element](#button-openscad_addopenscadelement) | Small | â€” |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_MeshBooleans.svg" width="11" height="11" alt="Mesh Boolean"> [Mesh Boolean](#button-openscad_meshboolean) | Small | â€” |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Hull.svg" width="11" height="11" alt="Hull"> [Hull](#button-openscad_hull) | Small | â€” |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Minkowski.svg" width="11" height="11" alt="Minkowski Sum"> [Minkowski Sum](#button-openscad_minkowski) | Small | â€” |

##### Frequently-used Part WB tools group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Part_CheckGeometry.png" width="11" height="11" alt="Check Geometry"> [Check Geometry](#button-part_checkgeometry) | Small | â€” |
| <img src="toolbar-icons/Part_Primitives.png" width="11" height="11" alt="Primitive"> [Primitive](#button-part_primitives) | Small | â€” |
| <img src="toolbar-icons/Part_Builder.png" width="11" height="11" alt="Shape Builder"> [Shape Builder](#button-part_builder) | Small | â€” |
| <img src="toolbar-icons/Part_Cut.png" width="11" height="11" alt="Cut"> [Cut](#button-part_cut) | Small | â€” |
| <img src="toolbar-icons/Part_Fuse.png" width="11" height="11" alt="Union"> [Union](#button-part_fuse) | Small | â€” |
| <img src="toolbar-icons/Part_Common.png" width="11" height="11" alt="Intersection"> [Intersection](#button-part_common) | Small | â€” |
| <img src="toolbar-icons/Part_Extrude.png" width="11" height="11" alt="Extrude"> [Extrude](#button-part_extrude) | Small | â€” |
| <img src="toolbar-icons/Part_Revolve.png" width="11" height="11" alt="Revolve"> [Revolve](#button-part_revolve) | Small | â€” |

#### View tab

Use the **Design â†’ View** groups and sizes above; each mode activates its native view actions.

### Test Framework Mode

#### Home tab

Component access, this mode's frequent operations, and shared utilities. File/Edit/Clipboard stay in the common toolbar above the ribbon.

##### Main group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> [Add Component](#button-std_part) | Medium (half size) | â€” |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Medium (half size) | â€” |

##### Frequent operations group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Gui/Icons/preferences-general.svg" width="11" height="11" alt="Self-test..."> [Self-test...](#button-test_test) | Medium (half size) | â€” |
| <img src="toolbar-icons/Test_TestAll.png" width="11" height="11" alt="Test all"> [Test all](#button-test_testall) | Medium (half size) | â€” |
| <img src="toolbar-icons/Test_TestDoc.png" width="11" height="11" alt="Test Document"> [Test Document](#button-test_testdoc) | Medium (half size) | â€” |

##### Structure group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> [Components](#button-std_componentstructure) | Small | â€” |
| <img src="toolbar-icons/Std_Group.png" width="11" height="11" alt="New Group"> [New Group](#button-std_group) | Small | â€” |
| <img src="toolbar-icons/Std_LinkActions.png" width="11" height="11" alt="Make Link"> [Make Link](#button-std_linkactions) | Small | Dropdown |
| â†³ Native choices for [Make Link](#button-std_linkactions) | Menu items | See function catalog |
| <img src="toolbar-icons/Std_VarSet.png" width="11" height="11" alt="Variable Set"> [Variable Set](#button-std_varset) | Small | â€” |
| <img src="toolbar-icons/PartDesign_AddReferenceObject.png" width="11" height="11" alt="Add Reference Object"> [Add Reference Object](#button-partdesign_addreferenceobject) | Small | â€” |

##### Utilities group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="toolbar-icons/Std_Import.png" width="11" height="11" alt="Importâ€¦"> [Importâ€¦](#button-std_import) | Small | â€” |
| <img src="toolbar-icons/Std_Export.png" width="11" height="11" alt="Exportâ€¦"> [Exportâ€¦](#button-std_export) | Small | â€” |
| <img src="toolbar-icons/Std_DlgPreferences.png" width="11" height="11" alt="Preferences"> [Preferences](#button-std_dlgpreferences) | Small | â€” |
| <img src="../../../src/Gui/Icons/zoom-in.svg" width="11" height="11" alt="Command search..."> [Command search...](#button-std_commandsearch) | Small | â€” |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> [Measure](#button-std_measure) | Small | â€” |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> [Mass Properties](#button-std_massproperties) | Small | â€” |
| <img src="toolbar-icons/Std_Delete.png" width="11" height="11" alt="Delete"> [Delete](#button-std_delete) | Small | â€” |

##### Help group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Help | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> [What's This?](#button-std_whatsthis) | Menu item | â€” |

##### Macro group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| Macro | Small | Dropdown |
| â†³ <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> [Record Macro](#button-std_dlgmacrorecord) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> [Macros](#button-std_dlgmacroexecute) | Menu item | â€” |
| â†³ <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> [Execute Macro](#button-std_dlgmacroexecutedirect) | Menu item | â€” |

#### Tools tab

##### TestTools group

| Command | Icon size | Dropdown / choices |
| --- | --- | --- |
| <img src="../../../src/Gui/Icons/preferences-general.svg" width="11" height="11" alt="Self-test..."> [Self-test...](#button-test_test) | Small | â€” |
| <img src="toolbar-icons/Test_TestAll.png" width="11" height="11" alt="Test all"> [Test all](#button-test_testall) | Small | â€” |
| <img src="toolbar-icons/Test_TestDoc.png" width="11" height="11" alt="Test Document"> [Test Document](#button-test_testdoc) | Small | â€” |
| <img src="toolbar-icons/Test_TestBase.png" width="11" height="11" alt="Test base"> [Test base](#button-test_testbase) | Small | â€” |

#### View tab

Use the **Design â†’ View** groups and sizes above; each mode activates its native view actions.

### 3D Printing and other addon modes

Only show a mode when an installed workbench registers it. Use the common toolbar, Home/Tools/View structure, and the same size hierarchy. Populate Tools from that workbench's actual groups; addon command lists remain unknown until installed. OpenSCAD's external-tool operations and BIM's reinforcement addons remain conditional.

## Changes and retained access

### Owner changes and completion of the outline

| Change | Status / effect |
| --- | --- |
| Common toolbar above ribbon | Owner direction; File/Edit/Clipboard move out of Home and stay available in all modes |
| Medium / half size | Owner direction; added between full and small, independent of dropdown behavior |
| Home Main | Owner direction: New Component, Add Component, New Sketch, Coordinate System; medium icons |
| Coordinate System dropdown | Owner direction: coordinate system, plane, axis, point; mapped to existing Part datum commands |
| Home domain groups | Owner direction; individual common commands and sizes complete the outline |
| Design Assembly tab | Owner outline; populated with existing Assembly and Assembly Joints groups |
| Design Sketch tab | Retained as a completion of the incomplete outline |
| Other modes | Existing native Tools groups retained; frequent Home subsets and sizes complete the outline |
| New Component | Std_NewComponent creates an embedded model with zero instances and opens its editing tab; Add Component inserts an occurrence |

### Classic-to-Plus consolidations

| Classic commands | Plus access |
| --- | --- |
| <img src="toolbar-icons/PartDesign_Pad.png" width="11" height="11" alt="Pad"> [Pad](#button-partdesign_pad) | Extrude â†’ Add |
| <img src="toolbar-icons/PartDesign_Pocket.png" width="11" height="11" alt="Pocket"> [Pocket](#button-partdesign_pocket) | Extrude â†’ Subtract |
| <img src="toolbar-icons/PartDesign_LinearPattern.png" width="11" height="11" alt="Linear Pattern"> [Linear Pattern](#button-partdesign_linearpattern) | Pattern task â†’ Linear / Circular type |
| <img src="toolbar-icons/PartDesign_PolarPattern.png" width="11" height="11" alt="Polar Pattern"> [Polar Pattern](#button-partdesign_polarpattern) | Pattern task â†’ Linear / Circular type |
| <img src="toolbar-icons/Part_CoordinateSystem.png" width="11" height="11" alt="Coordinate System"> [Coordinate System](#button-part_coordinatesystem) | Coordinate System dropdown / task choices |
| <img src="toolbar-icons/Assembly_CreateJointFixed.png" width="11" height="11" alt="Fixed Joint"> [Fixed Joint](#button-assembly_createjointfixed) | Fixed Joint dropdown / task choices |
| <img src="toolbar-icons/PartDesign_Pattern.png" width="11" height="11" alt="Pattern"> [Pattern](#button-partdesign_pattern) | Pattern dropdown / task choices |
| <img src="toolbar-icons/PartDesign_CircularPattern.png" width="11" height="11" alt="Circular Pattern"> [Circular Pattern](#button-partdesign_circularpattern) | Pattern dropdown / task choices |
| <img src="toolbar-icons/PartDesign_PathPattern.png" width="11" height="11" alt="Path Pattern"> [Path Pattern](#button-partdesign_pathpattern) | Pattern dropdown / task choices |
| <img src="toolbar-icons/PartDesign_PointPattern.png" width="11" height="11" alt="Point Pattern"> [Point Pattern](#button-partdesign_pointpattern) | Pattern dropdown / task choices |
| <img src="toolbar-icons/Sketcher_Dimension.png" width="11" height="11" alt="Dimension"> [Auto Dimension](#button-sketcher_dimension) | Auto Dimension dropdown / task choices |
| <img src="toolbar-icons/Sketcher_ConstrainDistanceY.png" width="11" height="11" alt="Vertical Dimension"> [Vertical Dimension](#button-sketcher_constraindistancey) | Auto Dimension dropdown / task choices |
| <img src="toolbar-icons/Sketcher_ConstrainDistanceX.png" width="11" height="11" alt="Horizontal Dimension"> [Horizontal Dimension](#button-sketcher_constraindistancex) | Auto Dimension dropdown / task choices |
| <img src="toolbar-icons/Sketcher_ConstrainAngle.png" width="11" height="11" alt="Angle Dimension"> [Angle Dimension](#button-sketcher_constrainangle) | Auto Dimension dropdown / task choices |
| <img src="toolbar-icons/Sketcher_ConstrainRadius.png" width="11" height="11" alt="Radius Dimension"> [Radius Dimension](#button-sketcher_constrainradius) | Auto Dimension dropdown / task choices |
| <img src="toolbar-icons/Sketcher_ConstrainDiameter.png" width="11" height="11" alt="Diameter Dimension"> [Diameter Dimension](#button-sketcher_constraindiameter) | Auto Dimension dropdown / task choices |
| <img src="toolbar-icons/Sketcher_ConstrainDistance.png" width="11" height="11" alt="Distance Dimension"> [Distance Dimension](#button-sketcher_constraindistance) | Auto Dimension dropdown / task choices |
| <img src="toolbar-icons/Sketcher_ConstrainRadiam.png" width="11" height="11" alt="Radius/Diameter Dimension"> [Radius/Diameter Dimension](#button-sketcher_constrainradiam) | Auto Dimension dropdown / task choices |
| <img src="toolbar-icons/Sketcher_ConstrainLock.png" width="11" height="11" alt="Lock Position"> [Lock Position](#button-sketcher_constrainlock) | Auto Dimension dropdown / task choices |
| <img src="toolbar-icons/Sketcher_ConstrainSnellsLaw.png" width="11" height="11" alt="Refraction Constraint"> [Refraction Constraint](#button-sketcher_constrainsnellslaw) | Auto Dimension dropdown / task choices |
| <img src="toolbar-icons/Sketcher_CompDimensionTools.png" width="11" height="11" alt="Dimension"> [Dimension](#button-sketcher_compdimensiontools) | Auto Dimension dropdown / task choices |
| <img src="toolbar-icons/Sketcher_CompConstrainRadDia.png" width="11" height="11" alt="Constrain radius"> [Constrain radius](#button-sketcher_compconstrainraddia) | Auto Dimension dropdown / task choices |
| <img src="toolbar-icons/PartDesign_AdditiveLoft.png" width="11" height="11" alt="Additive Loft"> [Additive Loft](#button-partdesign_additiveloft) | Unified Loft task operation choices |
| <img src="toolbar-icons/PartDesign_SubtractiveLoft.png" width="11" height="11" alt="Subtractive Loft"> [Subtractive Loft](#button-partdesign_subtractiveloft) | Unified Loft task operation choices |
| <img src="toolbar-icons/PartDesign_AdditivePipe.png" width="11" height="11" alt="Additive Pipe"> [Additive Pipe](#button-partdesign_additivepipe) | Unified Pipe task operation choices |
| <img src="toolbar-icons/PartDesign_SubtractivePipe.png" width="11" height="11" alt="Subtractive Pipe"> [Subtractive Pipe](#button-partdesign_subtractivepipe) | Unified Pipe task operation choices |
| <img src="toolbar-icons/PartDesign_AdditiveHelix.png" width="11" height="11" alt="Additive Helix"> [Additive Helix](#button-partdesign_additivehelix) | Unified Helix task operation choices |
| <img src="toolbar-icons/PartDesign_SubtractiveHelix.png" width="11" height="11" alt="Subtractive Helix"> [Subtractive Helix](#button-partdesign_subtractivehelix) | Unified Helix task operation choices |
| <img src="toolbar-icons/Std_Workbench.png" width="11" height="11" alt="Assembly"> [Workbench selector](#button-std_workbench) | Plus mode selector |

Shared native menus and shortcuts remain available. A toolbar omission is not removal of the underlying function. Legacy Body creation is not promoted in Home; component results remain background objects. The restored Circular/Path/Point bindings exist in the inspected build. Toolbar placement here does not expand their geometry scope.

### Part Design native toolbar differences

| Command | Native toolbar change |
| --- | --- |
| <img src="toolbar-icons/PartDesign_AddReferenceObject.png" width="11" height="11" alt="Add Reference Object"> [Add Reference Object](#button-partdesign_addreferenceobject) | Added in fork |
| <img src="toolbar-icons/PartDesign_Extrude.png" width="11" height="11" alt="Extrude"> [Extrude](#button-partdesign_extrude) | Added in fork |
| <img src="toolbar-icons/PartDesign_Pattern.png" width="11" height="11" alt="Pattern"> [Pattern](#button-partdesign_pattern) | Added in fork |
| <img src="toolbar-icons/Part_IsoclineCurve.png" width="11" height="11" alt="Isocline Curve"> [Isocline Curve](#button-part_isoclinecurve) | Added in fork |
| <img src="toolbar-icons/Part_TrimBody.png" width="11" height="11" alt="Trim Body"> [Trim Body](#button-part_trimbody) | Added in fork |
| <img src="toolbar-icons/PartDesign_LinearPattern.png" width="11" height="11" alt="Linear Pattern"> [Linear Pattern](#button-partdesign_linearpattern) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/PartDesign_Pad.png" width="11" height="11" alt="Pad"> [Pad](#button-partdesign_pad) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/PartDesign_Pocket.png" width="11" height="11" alt="Pocket"> [Pocket](#button-partdesign_pocket) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/PartDesign_PolarPattern.png" width="11" height="11" alt="Polar Pattern"> [Polar Pattern](#button-partdesign_polarpattern) | Omitted from fork toolbar; consolidation/menu access noted above |

### Part native toolbar differences

| Command | Native toolbar change |
| --- | --- |
| <img src="toolbar-icons/PartDesign_AddReferenceObject.png" width="11" height="11" alt="Add Reference Object"> [Add Reference Object](#button-partdesign_addreferenceobject) | Added in fork |
| <img src="toolbar-icons/Part_IsoclineCurve.png" width="11" height="11" alt="Isocline Curve"> [Isocline Curve](#button-part_isoclinecurve) | Added in fork |
| <img src="toolbar-icons/Part_TrimBody.png" width="11" height="11" alt="Trim Body"> [Trim Body](#button-part_trimbody) | Added in fork |

### Sketcher native toolbar differences

No native command addition/removal in the compared toolbar definitions. Plus changes placement and presentation.

### Surface native toolbar differences

No native command addition/removal in the compared toolbar definitions. Plus changes placement and presentation.

### Mesh native toolbar differences

No native command addition/removal in the compared toolbar definitions. Plus changes placement and presentation.

### Draft native toolbar differences

No native command addition/removal in the compared toolbar definitions. Plus changes placement and presentation.

### Assembly native toolbar differences

No native command addition/removal in the compared toolbar definitions. Plus changes placement and presentation.

### CAM native toolbar differences

| Command | Native toolbar change |
| --- | --- |
| <img src="../../../src/Gui/Icons/preferences-general.svg" width="11" height="11" alt="Holding Tab"> [Holding Tab](#button-cam_holdingtab) | Added in fork |
| <img src="toolbar-icons/CAM_IndexedSetup.png" width="11" height="11" alt="Indexed Setup"> [Indexed Setup](#button-cam_indexedsetup) | Added in fork |
| <img src="toolbar-icons/CAM_MeshPreparation.png" width="11" height="11" alt="Review CAM mesh..."> [Review CAM mesh...](#button-cam_meshpreparation) | Added in fork |
| <img src="toolbar-icons/CAM_PlanarSurface.png" width="11" height="11" alt="Parallel / Waterline"> [Parallel / Waterline](#button-cam_planarsurface) | Added in fork |

### TechDraw native toolbar differences

| Command | Native toolbar change |
| --- | --- |
| <img src="toolbar-icons/TechDraw_3PtAngleDimension.png" width="11" height="11" alt="Angle Dimension From 3 Points"> [Angle Dimension From 3 Points](#button-techdraw_3ptangledimension) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/TechDraw_AngleDimension.png" width="11" height="11" alt="Angle Dimension"> [Angle Dimension](#button-techdraw_angledimension) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/TechDraw_AreaDimension.png" width="11" height="11" alt="Area Annotation"> [Area Annotation](#button-techdraw_areadimension) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/TechDraw_DiameterDimension.png" width="11" height="11" alt="Diameter Dimension"> [Diameter Dimension](#button-techdraw_diameterdimension) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/TechDraw_Dimension.png" width="11" height="11" alt="Dimension"> [Dimension](#button-techdraw_dimension) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/TechDraw_ExtensionArcLengthAnnotation.png" width="11" height="11" alt="Arc Length Annotation"> [Arc Length Annotation](#button-techdraw_extensionarclengthannotation) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/TechDraw_ExtensionAreaAnnotation.png" width="11" height="11" alt="Area Annotation"> [Area Annotation](#button-techdraw_extensionareaannotation) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/TechDraw_ExtensionChamferDimensionGroup.png" width="11" height="11" alt="Horizontal Chamfer Dimension"> [Horizontal Chamfer Dimension](#button-techdraw_extensionchamferdimensiongroup) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/TechDraw_ExtensionCreateChainDimensionGroup.png" width="11" height="11" alt="Horizontal Chain Dimension"> [Horizontal Chain Dimension](#button-techdraw_extensioncreatechaindimensiongroup) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/TechDraw_ExtensionCreateCoordDimensionGroup.png" width="11" height="11" alt="Horizontal Coordinate Dimension"> [Horizontal Coordinate Dimension](#button-techdraw_extensioncreatecoorddimensiongroup) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/TechDraw_ExtensionCreateLengthArc.png" width="11" height="11" alt="Arc Length Dimension"> [Arc Length Dimension](#button-techdraw_extensioncreatelengtharc) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/TechDraw_ExtentGroup.png" width="11" height="11" alt="Horizontal extent"> [Horizontal extent](#button-techdraw_extentgroup) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/TechDraw_HorizontalDimension.png" width="11" height="11" alt="Horizontal Length Dimension"> [Horizontal Length Dimension](#button-techdraw_horizontaldimension) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/TechDraw_LengthDimension.png" width="11" height="11" alt="Length Dimension"> [Length Dimension](#button-techdraw_lengthdimension) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/TechDraw_RadiusDimension.png" width="11" height="11" alt="Radius Dimension"> [Radius Dimension](#button-techdraw_radiusdimension) | Omitted from fork toolbar; consolidation/menu access noted above |
| <img src="toolbar-icons/TechDraw_VerticalDimension.png" width="11" height="11" alt="Vertical Length Dimension"> [Vertical Length Dimension](#button-techdraw_verticaldimension) | Omitted from fork toolbar; consolidation/menu access noted above |

### FEM native toolbar differences

No native command addition/removal in the compared toolbar definitions. Plus changes placement and presentation.

### Spreadsheet native toolbar differences

No native command addition/removal in the compared toolbar definitions. Plus changes placement and presentation.

### Material native toolbar differences

No native command addition/removal in the compared toolbar definitions. Plus changes placement and presentation.

### MeshPart native toolbar differences

No native command addition/removal in the compared toolbar definitions. Plus changes placement and presentation.

### Points native toolbar differences

No native command addition/removal in the compared toolbar definitions. Plus changes placement and presentation.

### Robot native toolbar differences

No native command addition/removal in the compared toolbar definitions. Plus changes placement and presentation.

### ReverseEngineering native toolbar differences

No native command addition/removal in the compared toolbar definitions. Plus changes placement and presentation.

### Inspection native toolbar differences

No native command addition/removal in the compared toolbar definitions. Plus changes placement and presentation.

### BIM native toolbar differences

No native command addition/removal in the compared toolbar definitions. Plus changes placement and presentation.

### OpenSCAD native toolbar differences

No native command addition/removal in the compared toolbar definitions. Plus changes placement and presentation.

### Test Framework native toolbar differences

No native command addition/removal in the compared toolbar definitions. Plus changes placement and presentation.

## Maintenance

This reference owns command placement; the UI specification owns shared behavior/sizing. The owner's outline is incomplete: group membership and sizes remain reviewable. Refresh native metadata with [ExportToolbarReference.FCMacro](../../../tools/ExportToolbarReference.FCMacro), then `python tools/GenerateToolbarReference.py <inventory.json> <recorded-upstream-ref>`. Review the generator's target placements when owner decisions change.

Artwork retains its original [license](../../../LICENSE). HTML width/height attributes scale reference icons without changing PNG/SVG assets.

## Complete toolbar button/function catalog

Every Classic/Plus command and native compound-button choice is listed below. Native IDs disambiguate similar captions. Descriptions come from native help/status text or source resources. Dropdown child choices have their own rows. New Component is a registered native Python command with its own ID and function row.

| Icon | Command / choice | Native ID | Function |
| --- | --- | --- | --- |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Add.svg" width="11" height="11" alt="Add Component"> | <a id="button-arch_add"></a>Add Component | `Arch_Add` | Adds the selected components to the active object |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Axis.svg" width="11" height="11" alt="Axis"> | <a id="button-arch_axis"></a>Axis | `Arch_Axis` | Creates a set of axes |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Axis_System.svg" width="11" height="11" alt="Axis System"> | <a id="button-arch_axissystem"></a>Axis System | `Arch_AxisSystem` | Creates an axis system from a set of axes |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Building.svg" width="11" height="11" alt="Building"> | <a id="button-arch_building"></a>Building | `Arch_Building` | Creates a building object |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Component.svg" width="11" height="11" alt="Component"> | <a id="button-arch_component"></a>Component | `Arch_Component` | Creates an undefined architectural component |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_CurtainWall.svg" width="11" height="11" alt="Curtain Wall"> | <a id="button-arch_curtainwall"></a>Curtain Wall | `Arch_CurtainWall` | Creates a curtain wall object from selected line or from scratch |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_CutPlane.svg" width="11" height="11" alt="Cut With Plane"> | <a id="button-arch_cutplane"></a>Cut With Plane | `Arch_CutPlane` | Cuts an object with a plane |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Equipment.svg" width="11" height="11" alt="Equipment"> | <a id="button-arch_equipment"></a>Equipment | `Arch_Equipment` | Creates an equipment from a selected object (Part or Mesh) |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Fence.svg" width="11" height="11" alt="Fence"> | <a id="button-arch_fence"></a>Fence | `Arch_Fence` | Creates a fence object from a selected section, post and path |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Frame.svg" width="11" height="11" alt="Frame"> | <a id="button-arch_frame"></a>Frame | `Arch_Frame` | Creates a frame object from a planar 2D object (the extrusion path(s)) and a profile. Make sure objects are selected in that order. |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Grid.svg" width="11" height="11" alt="Grid"> | <a id="button-arch_grid"></a>Grid | `Arch_Grid` | Creates a customizable grid object |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Floor.svg" width="11" height="11" alt="Level"> | <a id="button-arch_level"></a>Level | `Arch_Level` | Creates a building part object that represents a level |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Panel.svg" width="11" height="11" alt="Panel"> | <a id="button-arch_panel"></a>Panel | `Arch_Panel` | Creates a panel object from scratch or from a selected object (sketch, wire, face or solid) |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Pipe.svg" width="11" height="11" alt="Pipe"> | <a id="button-arch_pipe"></a>Pipe | `Arch_Pipe` | Creates a pipe object from a given wire or line |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_PipeConnector.svg" width="11" height="11" alt="Connector"> | <a id="button-arch_pipeconnector"></a>Connector | `Arch_PipeConnector` | Creates a connector between 2 or 3 selected pipes |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Profile.svg" width="11" height="11" alt="Profile"> | <a id="button-arch_profile"></a>Profile | `Arch_Profile` | Creates a profile |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Rebar.svg" width="11" height="11" alt="Custom Rebar"> | <a id="button-arch_rebar"></a>Custom Rebar | `Arch_Rebar` | Creates a reinforcement bar from the selected face of solid object and/or a sketch |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Reference.svg" width="11" height="11" alt="External Reference"> | <a id="button-arch_reference"></a>External Reference | `Arch_Reference` | Creates an external reference object |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Remove.svg" width="11" height="11" alt="Remove Component"> | <a id="button-arch_remove"></a>Remove Component | `Arch_Remove` | Removes the selected components from their parents, or creates a hole in a component |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Roof.svg" width="11" height="11" alt="Roof"> | <a id="button-arch_roof"></a>Roof | `Arch_Roof` | Creates a roof object from the selected wire. |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Schedule.svg" width="11" height="11" alt="Schedule"> | <a id="button-arch_schedule"></a>Schedule | `Arch_Schedule` | Creates a schedule to collect data from the model |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_SectionPlane.svg" width="11" height="11" alt="Section Plane"> | <a id="button-arch_sectionplane"></a>Section Plane | `Arch_SectionPlane` | Creates a section plane object, including the selected objects |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Site.svg" width="11" height="11" alt="Site"> | <a id="button-arch_site"></a>Site | `Arch_Site` | Creates a site including selected objects |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Space.svg" width="11" height="11" alt="Space"> | <a id="button-arch_space"></a>Space | `Arch_Space` | Creates a space object from selected boundary objects |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Stairs.svg" width="11" height="11" alt="Stairs"> | <a id="button-arch_stairs"></a>Stairs | `Arch_Stairs` | Creates a flight of stairs |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Survey.svg" width="11" height="11" alt="Survey"> | <a id="button-arch_survey"></a>Survey | `Arch_Survey` | Starts survey |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Truss.svg" width="11" height="11" alt="Truss"> | <a id="button-arch_truss"></a>Truss | `Arch_Truss` | Creates a truss object from the selected line or from scratch |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Wall.svg" width="11" height="11" alt="Wall"> | <a id="button-arch_wall"></a>Wall | `Arch_Wall` | Creates a wall object from scratch or from a selected object (wire, face or solid) |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Window.svg" width="11" height="11" alt="Window"> | <a id="button-arch_window"></a>Window | `Arch_Window` | Creates a window object from a selected object (wire, rectangle or sketch) |
| <img src="toolbar-icons/Assembly_CreateAssembly.png" width="11" height="11" alt="New Assembly"> | <a id="button-assembly_createassembly"></a>New Assembly | `Assembly_CreateAssembly` | Creates an assembly object in the current document, or in the current active assembly (if any). Limit of one root assembly per file. |
| <img src="toolbar-icons/Assembly_CreateBom.png" width="11" height="11" alt="Bill of Materials"> | <a id="button-assembly_createbom"></a>Bill of Materials | `Assembly_CreateBom` | Creates a bill of materials of the current assembly. If an assembly is active, it will be a BOM of this assembly. Else it will be a BOM of the whole document. The BOM object is a document object that stores the settings of your BOM. It is also a spreadsheet object so you can easily visualize the BOM. If you do not need the BOM object to be saved as a document object, you can simply export and cancel the task. The columns 'Index', 'Name', 'File Name' and 'Quantity' are automatically generated on recompute. The 'Description' and custom columns are not overwritten. |
| <img src="toolbar-icons/Assembly_CreateJointAngle.png" width="11" height="11" alt="Angle Joint"> | <a id="button-assembly_createjointangle"></a>Angle Joint | `Assembly_CreateJointAngle` | Creates an angle joint that fixes the angle between the Z-axis of the selected coordinate systems |
| <img src="toolbar-icons/Assembly_CreateJointBall.png" width="11" height="11" alt="Ball Joint"> | <a id="button-assembly_createjointball"></a>Ball Joint | `Assembly_CreateJointBall` | Creates a ball joint that connects parts at a point, allowing unrestricted movement as long as the connection points remain in contact |
| <img src="toolbar-icons/Assembly_CreateJointBelt.png" width="11" height="11" alt="Belt Joint"> | <a id="button-assembly_createjointbelt"></a>Belt Joint | `Assembly_CreateJointBelt` | Creates a belt joint that links 2 rotating objects together. They will have the same rotation direction. Select the same coordinate systems as the revolute joints. |
| <img src="toolbar-icons/Assembly_CreateJointCylindrical.png" width="11" height="11" alt="Cylindrical Joint"> | <a id="button-assembly_createjointcylindrical"></a>Cylindrical Joint | `Assembly_CreateJointCylindrical` | Creates a cylindrical joint that allows rotation around and translation along a single axis between assembled parts |
| <img src="toolbar-icons/Assembly_CreateJointDistance.png" width="11" height="11" alt="Distance Joint"> | <a id="button-assembly_createjointdistance"></a>Distance Joint | `Assembly_CreateJointDistance` | Creates a distance joint that fixes the distance between the selected objects Creates one of several different joints based on the selection. For example, a distance of 0 between a plane and a cylinder creates a tangent joint. A distance of 0 between planes will make them co-planar. |
| <img src="toolbar-icons/Assembly_CreateJointFixed.png" width="11" height="11" alt="Fixed Joint"> | <a id="button-assembly_createjointfixed"></a>Fixed Joint | `Assembly_CreateJointFixed` | 1 - If an assembly is active : Creates a joint statically locking two parts together, preventing any movement or rotation 2 - If a part is active: Positions sub-parts by matching selected coordinate systems. The second part selected will move. |
| <img src="toolbar-icons/Assembly_CreateJointGearBelt.png" width="11" height="11" alt="Gears Joint"> | <a id="button-assembly_createjointgearbelt"></a>Gears Joint | `Assembly_CreateJointGearBelt` | Creates a gears joint that links 2 rotating gears together. They will have inverse rotation direction. Select the same coordinate systems as the revolute joints. |
| <img src="toolbar-icons/Assembly_CreateJointGearBelt_1.png" width="11" height="11" alt="Belt Joint"> | â†³ Belt Joint | `Assembly_CreateJointGearBelt` | Creates a belt joint that links 2 rotating objects together. They will have the same rotation direction. Select the same coordinate systems as the revolute joints. |
| <img src="toolbar-icons/Assembly_CreateJointGears.png" width="11" height="11" alt="Gears Joint"> | <a id="button-assembly_createjointgears"></a>Gears Joint | `Assembly_CreateJointGears` | Creates a gears joint that links 2 rotating gears together. They will have inverse rotation direction. Select the same coordinate systems as the revolute joints. |
| <img src="toolbar-icons/Assembly_CreateJointParallel.png" width="11" height="11" alt="Parallel Joint"> | <a id="button-assembly_createjointparallel"></a>Parallel Joint | `Assembly_CreateJointParallel` | Creates a parallel joint that makes the Z-axis of the selected coordinate systems parallel |
| <img src="toolbar-icons/Assembly_CreateJointPerpendicular.png" width="11" height="11" alt="Perpendicular Joint"> | <a id="button-assembly_createjointperpendicular"></a>Perpendicular Joint | `Assembly_CreateJointPerpendicular` | Creates a perpendicular joint that makes the Z-axis of the selected coordinate systems perpendicular |
| <img src="toolbar-icons/Assembly_CreateJointRackPinion.png" width="11" height="11" alt="Rack and Pinion Joint"> | <a id="button-assembly_createjointrackpinion"></a>Rack and Pinion Joint | `Assembly_CreateJointRackPinion` | Creates a rack and pinion joint that links a part with a slider joint to a part with a revolute joint Select the same coordinate systems as the revolute and slider joints. The pitch radius defines the movement ratio between the rack and the pinion. |
| <img src="toolbar-icons/Assembly_CreateJointRevolute.png" width="11" height="11" alt="Revolute Joint"> | <a id="button-assembly_createjointrevolute"></a>Revolute Joint | `Assembly_CreateJointRevolute` | Creates a revolute joint allowing rotation around a single axis between selected parts |
| <img src="toolbar-icons/Assembly_CreateJointRigidGroup.png" width="11" height="11" alt="Create Rigid Group"> | <a id="button-assembly_createjointrigidgroup"></a>Create Rigid Group | `Assembly_CreateJointRigidGroup` | Create a rigid group. Creates a rigid group that permanently locks the selected components together. |
| <img src="toolbar-icons/Assembly_CreateJointScrew.png" width="11" height="11" alt="Screw Joint"> | <a id="button-assembly_createjointscrew"></a>Screw Joint | `Assembly_CreateJointScrew` | Creates a screw joint that links a part with a slider joint to a part with a revolute joint Select the same coordinate systems as the revolute and slider joints. The pitch radius defines the movement ratio between the rotating screw and the sliding part. |
| <img src="toolbar-icons/Assembly_CreateJointSlider.png" width="11" height="11" alt="Slider Joint"> | <a id="button-assembly_createjointslider"></a>Slider Joint | `Assembly_CreateJointSlider` | Creates a slider joint that allows linear movement along a single axis, but restricts rotation between selected parts |
| <img src="toolbar-icons/Assembly_CreateSimulation.png" width="11" height="11" alt="Simulation"> | <a id="button-assembly_createsimulation"></a>Simulation | `Assembly_CreateSimulation` | Creates a new simulation of the current assembly |
| <img src="toolbar-icons/Assembly_CreateSnapshot.png" width="11" height="11" alt="Snapshot"> | <a id="button-assembly_createsnapshot"></a>Snapshot | `Assembly_CreateSnapshot` | Captures the current assembly state (placements and visibility). Double-clicking the Snapshot object restores the assembly to that state. |
| <img src="toolbar-icons/Assembly_CreateView.png" width="11" height="11" alt="Exploded View"> | <a id="button-assembly_createview"></a>Exploded View | `Assembly_CreateView` | Creates an exploded view of the current assembly |
| <img src="toolbar-icons/Assembly_Insert.png" width="11" height="11" alt="Insert Component"> | <a id="button-assembly_insert"></a>Insert Component | `Assembly_Insert` | Inserts a component into the active assembly. This will create dynamic links to parts, bodies, primitives, and assemblies. To insert external components, make sure that the file is open in the current session Insert by left clicking items in the list. Remove by right clicking items in the list. Press shift to add several instances of the component while clicking on the view. |
| <img src="toolbar-icons/Assembly_Insert_1.png" width="11" height="11" alt="Add Component"> | â†³ Add Component | `Assembly_Insert` | Adds a component to the active component or assembly. |
| <img src="toolbar-icons/Assembly_InsertLink.png" width="11" height="11" alt="Insert Component"> | <a id="button-assembly_insertlink"></a>Insert Component | `Assembly_InsertLink` | Inserts a component into the active assembly. This will create dynamic links to parts, bodies, primitives, and assemblies. To insert external components, make sure that the file is open in the current session Insert by left clicking items in the list. Remove by right clicking items in the list. Press shift to add several instances of the component while clicking on the view. |
| <img src="toolbar-icons/Assembly_InsertNewPart.png" width="11" height="11" alt="Add Component"> | <a id="button-assembly_insertnewpart"></a>Add Component | `Assembly_InsertNewPart` | Adds a component to the active component or assembly. |
| <img src="toolbar-icons/Assembly_SolveAssembly.png" width="11" height="11" alt="Solve Assembly"> | <a id="button-assembly_solveassembly"></a>Solve Assembly | `Assembly_SolveAssembly` | Solves the currently active assembly. |
| <img src="toolbar-icons/Assembly_ToggleGrounded.png" width="11" height="11" alt="Toggle Grounded"> | <a id="button-assembly_togglegrounded"></a>Toggle Grounded | `Assembly_ToggleGrounded` | Toggles the grounding of a part. Grounding a part permanently locks its position in the assembly, preventing any movement or rotation. |
| <img src="../../../src/Mod/Draft/Resources/icons/Draft_Arc.svg" width="11" height="11" alt="Arc Tools"> | <a id="button-bim_arctools"></a>Arc Tools | `BIM_ArcTools` | Arc Tools |
| <img src="../../../src/Mod/Draft/Resources/icons/Draft_Array.svg" width="11" height="11" alt="Array Tools"> | <a id="button-bim_arraytools"></a>Array Tools | `BIM_ArrayTools` | Array Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Axis.svg" width="11" height="11" alt="Axis Tools"> | <a id="button-bim_axistools"></a>Axis Tools | `BIM_AxisTools` | Axis Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Beam.svg" width="11" height="11" alt="Beam"> | <a id="button-bim_beam"></a>Beam | `BIM_Beam` | Creates a beam between two points |
| â€” | <a id="button-bim_booleantools"></a>Boolean Tools | `BIM_BooleanTools` | Boolean Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Box.svg" width="11" height="11" alt="Box"> | <a id="button-bim_box"></a>Box | `BIM_Box` | Graphically creates a generic box in the current document |
| <img src="../../../src/Mod/Part/Gui/Resources/icons/create/Part_Shapebuilder.svg" width="11" height="11" alt="Shape Builder"> | <a id="button-bim_builder"></a>Shape Builder | `BIM_Builder` | Advanced utility to create shapes |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Classification.svg" width="11" height="11" alt="Manage Classification"> | <a id="button-bim_classification"></a>Manage Classification | `BIM_Classification` | Manages classification systems and apply classification to objects |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Clone.svg" width="11" height="11" alt="Clone"> | <a id="button-bim_clone"></a>Clone | `BIM_Clone` | Clones selected objects to another location |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Clone.svg" width="11" height="11" alt="Cloning Tools"> | <a id="button-bim_clonetools"></a>Cloning Tools | `BIM_CloneTools` | Cloning Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Column.svg" width="11" height="11" alt="Column"> | <a id="button-bim_column"></a>Column | `BIM_Column` | Creates a column at a specified location |
| <img src="../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Common.svg" width="11" height="11" alt="Intersection"> | <a id="button-bim_common"></a>Intersection | `BIM_Common` | Creates an intersection of two shapes |
| <img src="../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Compound.svg" width="11" height="11" alt="Compound"> | <a id="button-bim_compound"></a>Compound | `BIM_Compound` | Creates a compound of several shapes |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Copy.svg" width="11" height="11" alt="Copy"> | <a id="button-bim_copy"></a>Copy | `BIM_Copy` | Copies selected objects to another location |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Covering.svg" width="11" height="11" alt="Covering"> | <a id="button-bim_covering"></a>Covering | `BIM_Covering` | Creates a covering (floor finish, cladding) on a selected face |
| â€” | <a id="button-bim_create2dviews"></a>Create 2D Views | `BIM_Create2DViews` | Create 2D Views |
| <img src="../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Cut.svg" width="11" height="11" alt="Difference"> | <a id="button-bim_cut"></a>Difference | `BIM_Cut` | Creates a difference between two shapes |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_DimensionAligned.svg" width="11" height="11" alt="Aligned Dimension"> | <a id="button-bim_dimensionaligned"></a>Aligned Dimension | `BIM_DimensionAligned` | Creates an aligned dimension |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_DimensionHorizontal.svg" width="11" height="11" alt="Horizontal Dimension"> | <a id="button-bim_dimensionhorizontal"></a>Horizontal Dimension | `BIM_DimensionHorizontal` | Creates an horizontal dimension |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_DimensionVertical.svg" width="11" height="11" alt="Vertical Dimension"> | <a id="button-bim_dimensionvertical"></a>Vertical Dimension | `BIM_DimensionVertical` | Creates a vertical dimension |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Door.svg" width="11" height="11" alt="Door"> | <a id="button-bim_door"></a>Door | `BIM_Door` | Places a door at a given location |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_ArchView.svg" width="11" height="11" alt="2D Drawing"> | <a id="button-bim_drawingview"></a>2D Drawing | `BIM_DrawingView` | Creates a drawing container to contain elements of a 2D view |
| <img src="../../../src/Mod/Part/Gui/Resources/icons/tools/Part_Extrude.svg" width="11" height="11" alt="Extrude"> | <a id="button-bim_extrude"></a>Extrude | `BIM_Extrude` | Extrudes a selected 2D shape |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_ExtrudeFace.svg" width="11" height="11" alt="Extrude Face"> | <a id="button-bim_extrudeface"></a>Extrude Face | `BIM_ExtrudeFace` | Extrudes a selected face into a solid |
| <img src="../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Fuse.svg" width="11" height="11" alt="Union"> | <a id="button-bim_fuse"></a>Union | `BIM_Fuse` | Creates a union of several shapes |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Box.svg" width="11" height="11" alt="Generic 3D Tools"> | <a id="button-bim_generictools"></a>Generic 3D Tools | `BIM_GenericTools` | Generic 3D Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_IfcElements.svg" width="11" height="11" alt="Manage IFC Elements"> | <a id="button-bim_ifcelements"></a>Manage IFC Elements | `BIM_IfcElements` | Manages how the different elements of the BIM project will be exported to IFC |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_IfcElements.svg" width="11" height="11" alt="IFC Management"> | <a id="button-bim_ifcmanagetools"></a>IFC Management | `BIM_IfcManageTools` | IFC Management |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_IfcProperties.svg" width="11" height="11" alt="Manage IFC Properties"> | <a id="button-bim_ifcproperties"></a>Manage IFC Properties | `BIM_IfcProperties` | Manages the different IFC properties of the BIM objects |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_IfcQuantities.svg" width="11" height="11" alt="Manage IFC Quantities"> | <a id="button-bim_ifcquantities"></a>Manage IFC Quantities | `BIM_IfcQuantities` | Manages how the quantities of different elements of the BIM project will be exported to IFC |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Layers.svg" width="11" height="11" alt="Manage Layers"> | <a id="button-bim_layers"></a>Manage Layers | `BIM_Layers` | Sets/modifies the different layers of your BIM project |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Leader.svg" width="11" height="11" alt="Leader"> | <a id="button-bim_leader"></a>Leader | `BIM_Leader` | Creates a polyline with an arrow at its endpoint |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Library.svg" width="11" height="11" alt="Objects Library"> | <a id="button-bim_library"></a>Objects Library | `BIM_Library` | Opens the objects library |
| <img src="../../../src/Gui/Icons/Link.svg" width="11" height="11" alt="Make Link"> | <a id="button-bim_linkmake"></a>Make Link | `BIM_LinkMake` | Creates a Link to the selected object and immediately enables moving it |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Material.svg" width="11" height="11" alt="Material"> | <a id="button-bim_material"></a>Material | `BIM_Material` | Sets or creates a material for selected objects |
| <img src="../../../src/Mod/Part/Gui/Resources/icons/tools/Part_Offset2D.svg" width="11" height="11" alt="2D Offset"> | <a id="button-bim_offset2d"></a>2D Offset | `BIM_Offset2D` | Utility to offset planar shapes |
| â€” | <a id="button-bim_offsettools"></a>Offset Tools | `BIM_OffsetTools` | Offset Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Preflight.svg" width="11" height="11" alt="Preflight Checks"> | <a id="button-bim_preflight"></a>Preflight Checks | `BIM_Preflight` | Checks several characteristics of this model before exporting to IFC |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_ProjectManager.svg" width="11" height="11" alt="Setup Project"> | <a id="button-bim_projectmanager"></a>Setup Project | `BIM_ProjectManager` | Creates or manages a BIM project |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Report.svg" width="11" height="11" alt="Report"> | <a id="button-bim_report"></a>Report | `BIM_Report` | Create a new BIM Report to query model data with SQL |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Report.svg" width="11" height="11" alt="Report Tools"> | <a id="button-bim_reporttools"></a>Report Tools | `BIM_ReportTools` | Report Tools |
| <img src="../../../src/Gui/Icons/preferences-system.svg" width="11" height="11" alt="BIM Setup"> | <a id="button-bim_setup"></a>BIM Setup | `BIM_Setup` | Sets common FreeCAD preferences for a BIM workflow |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_View_Cut.svg" width="11" height="11" alt="Section Cut"> | <a id="button-bim_shape2dcut"></a>Section Cut | `BIM_Shape2DCut` | Creates a 2D projection of only the intersecting faces of the selected objects on the XY-plane. |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_BuildingPart_Tree.svg" width="11" height="11" alt="Section View"> | <a id="button-bim_shape2dview"></a>Section View | `BIM_Shape2DView` | Creates a 2D projection of the selected objects on the XY-plane. The initial projection direction is the opposite of the current active view direction. |
| <img src="../../../src/Mod/BIM/Resources/icons/Tree_Part.svg" width="11" height="11" alt="Simple Copy"> | <a id="button-bim_simplecopy"></a>Simple Copy | `BIM_SimpleCopy` | Creates a simple non-parametric copy |
| <img src="../../../src/Mod/BIM/Resources/icons/Sketch.svg" width="11" height="11" alt="New Sketch"> | <a id="button-bim_sketch"></a>New Sketch | `BIM_Sketch` | Creates a new sketch in the current working plane |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Slab.svg" width="11" height="11" alt="Slab"> | <a id="button-bim_slab"></a>Slab | `BIM_Slab` | Creates a slab from a planar shape |
| <img src="../../../src/Mod/Draft/Resources/icons/Draft_BSpline.svg" width="11" height="11" alt="Spline Tools"> | <a id="button-bim_splinetools"></a>Spline Tools | `BIM_SplineTools` | Spline Tools |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_PageDefault.svg" width="11" height="11" alt="New Page"> | <a id="button-bim_tdpage"></a>New Page | `BIM_TDPage` | Creates a new TechDraw page from a template |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_InsertView.svg" width="11" height="11" alt="New View"> | <a id="button-bim_tdview"></a>New View | `BIM_TDView` | Inserts a drawing view on a page. To choose where to insert the view when multiple pages are available, select both the view and the page before executing the command. |
| <img src="../../../src/Mod/Draft/Resources/icons/Draft_Text.svg" width="11" height="11" alt="Text"> | <a id="button-bim_text"></a>Text | `BIM_Text` | Create a text in the current 3D view or TechDraw page |
| <img src="../../../src/Mod/Draft/Resources/icons/Draft_Trimex.svg" width="11" height="11" alt="Trimex"> | <a id="button-bim_trimex"></a>Trimex | `BIM_Trimex` | Trims or extends the selected object |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Unclone.svg" width="11" height="11" alt="Unclone"> | <a id="button-bim_unclone"></a>Unclone | `BIM_Unclone` | Creates a selected clone object independent from its original |
| <img src="../../../src/Mod/BIM/Resources/icons/BIM_Windows.svg" width="11" height="11" alt="Manage Doors and Windows"> | <a id="button-bim_windows"></a>Manage Doors and Windows | `BIM_Windows` | Manages the different doors and windows of the BIM project |
| <img src="toolbar-icons/CAM_Adaptive.png" width="11" height="11" alt="Adaptive"> | <a id="button-cam_adaptive"></a>Adaptive | `CAM_Adaptive` | Adaptive clearing and profiling |
| <img src="toolbar-icons/CAM_Array.png" width="11" height="11" alt="Array"> | <a id="button-cam_array"></a>Array | `CAM_Array` | Creates an array from selected toolpaths |
| <img src="toolbar-icons/CAM_DressupTools.png" width="11" height="11" alt="Array"> | <a id="button-cam_dressuptools"></a>Array | `CAM_DressupTools` | Creates an array from a selected toolpath |
| <img src="toolbar-icons/CAM_DressupTools_1.png" width="11" height="11" alt="Axis Map"> | â†³ Axis Map | `CAM_DressupTools` | Remaps one axis to another |
| <img src="toolbar-icons/CAM_DressupTools_2.png" width="11" height="11" alt="Boundary"> | â†³ Boundary | `CAM_DressupTools` | Creates a boundary dress-up from a selected toolpath |
| <img src="toolbar-icons/CAM_DressupTools_3.png" width="11" height="11" alt="Boundary2"> | â†³ Boundary2 | `CAM_DressupTools` | Creates a boundary dress-up from a selected toolpath |
| <img src="toolbar-icons/CAM_DressupTools_4.png" width="11" height="11" alt="Dogbone"> | â†³ Dogbone | `CAM_DressupTools` | Creates a dogbone dress-up object from a selected toolpath |
| <img src="toolbar-icons/CAM_DressupTools_5.png" width="11" height="11" alt="Drag Knife"> | â†³ Drag Knife | `CAM_DressupTools` | Modifies a toolpath to add dragknife corner actions |
| <img src="toolbar-icons/CAM_DressupTools_6.png" width="11" height="11" alt="Lead In/Out"> | â†³ Lead In/Out | `CAM_DressupTools` | Creates entry and exit motions for a selected path |
| <img src="toolbar-icons/CAM_DressupTools_7.png" width="11" height="11" alt="Mirror"> | â†³ Mirror | `CAM_DressupTools` | Creates mirror of a selected path |
| <img src="toolbar-icons/CAM_DressupTools_8.png" width="11" height="11" alt="Plunge Milling"> | â†³ Plunge Milling | `CAM_DressupTools` | Creates plunge milling for a selected path |
| <img src="toolbar-icons/CAM_DressupTools_9.png" width="11" height="11" alt="Ramp Entry"> | â†³ Ramp Entry | `CAM_DressupTools` | Creates a ramp entry dress-up object from a selected toolpath |
| <img src="toolbar-icons/CAM_DressupTools_10.png" width="11" height="11" alt="Tag"> | â†³ Tag | `CAM_DressupTools` | Creates a tag dress-up object from a selected toolpath |
| <img src="toolbar-icons/CAM_DressupTools_11.png" width="11" height="11" alt="Z Depth Correction"> | â†³ Z Depth Correction | `CAM_DressupTools` | Corrects Z depth using a probe map |
| <img src="toolbar-icons/CAM_DrillingTools.png" width="11" height="11" alt="Drilling"> | <a id="button-cam_drillingtools"></a>Drilling | `CAM_DrillingTools` | Creates a Drilling toolpath from the features of a base object |
| <img src="toolbar-icons/CAM_DrillingTools_1.png" width="11" height="11" alt="Thread Milling"> | â†³ Thread Milling | `CAM_DrillingTools` | Creates a Thread Milling toolpath from features of a base object |
| <img src="toolbar-icons/CAM_EngraveTools.png" width="11" height="11" alt="Engrave"> | <a id="button-cam_engravetools"></a>Engrave | `CAM_EngraveTools` | Creates an Engraving toolpath around a Draft ShapeString |
| <img src="toolbar-icons/CAM_EngraveTools_1.png" width="11" height="11" alt="Deburr"> | â†³ Deburr | `CAM_EngraveTools` | Creates a Deburr toolpath along Edges or around Faces |
| <img src="toolbar-icons/CAM_EngraveTools_2.png" width="11" height="11" alt="Vcarve"> | â†³ Vcarve | `CAM_EngraveTools` | Creates a medial line engraving toolpath |
| <img src="toolbar-icons/CAM_Helix.png" width="11" height="11" alt="Helix"> | <a id="button-cam_helix"></a>Helix | `CAM_Helix` | Creates a Helical toolpath from the features of a base object |
| <img src="../../../src/Gui/Icons/preferences-general.svg" width="11" height="11" alt="Holding Tab"> | <a id="button-cam_holdingtab"></a>Holding Tab | `CAM_HoldingTab` | Creates a stock bridge preserved by Parallel and Waterline paths |
| <img src="toolbar-icons/CAM_IndexedSetup.png" width="11" height="11" alt="Indexed Setup"> | <a id="button-cam_indexedsetup"></a>Indexed Setup | `CAM_IndexedSetup` | Creates another manually indexed side of a Job, including its stock and tabs |
| <img src="toolbar-icons/CAM_Inspect.png" width="11" height="11" alt="Inspect Toolpath"> | <a id="button-cam_inspect"></a>Inspect Toolpath | `CAM_Inspect` | Inspects the contents of a toolpath object |
| <img src="toolbar-icons/CAM_Job.png" width="11" height="11" alt="New Job"> | <a id="button-cam_job"></a>New Job | `CAM_Job` | Creates a CAM job |
| <img src="toolbar-icons/CAM_MeshPreparation.png" width="11" height="11" alt="Review CAM mesh..."> | <a id="button-cam_meshpreparation"></a>Review CAM mesh... | `CAM_MeshPreparation` | Inspect an imported mesh and optionally create an independent reversed-normal copy |
| <img src="toolbar-icons/CAM_MillFacing.png" width="11" height="11" alt="Mill Facing"> | <a id="button-cam_millfacing"></a>Mill Facing | `CAM_MillFacing` | Create a Mill Facing Operation to machine the top surface of stock |
| <img src="toolbar-icons/CAM_OpActiveToggle.png" width="11" height="11" alt="Toggle Operation"> | <a id="button-cam_opactivetoggle"></a>Toggle Operation | `CAM_OpActiveToggle` | Toggles the active state of the operation |
| <img src="toolbar-icons/CAM_OperationCopy.png" width="11" height="11" alt="Copy Operation"> | <a id="button-cam_operationcopy"></a>Copy Operation | `CAM_OperationCopy` | Copies the operation in the job |
| <img src="toolbar-icons/CAM_PlanarSurface.png" width="11" height="11" alt="Parallel / Waterline"> | <a id="button-cam_planarsurface"></a>Parallel / Waterline | `CAM_PlanarSurface` | Machines an STL or CAD model with Parallel or Waterline paths |
| <img src="toolbar-icons/CAM_Pocket_Shape.png" width="11" height="11" alt="Pocket Shape"> | <a id="button-cam_pocket_shape"></a>Pocket Shape | `CAM_Pocket_Shape` | Creates a pocket toolpath from a face or faces |
| <img src="toolbar-icons/CAM_PostTools.png" width="11" height="11" alt="Post Process"> | <a id="button-cam_posttools"></a>Post Process | `CAM_PostTools` | Post Processes the selected Job |
| <img src="toolbar-icons/CAM_PostTools_1.png" width="11" height="11" alt="Post Process Selected"> | â†³ Post Process Selected | `CAM_PostTools` | Post Processes the selected operations |
| <img src="toolbar-icons/CAM_Profile.png" width="11" height="11" alt="Profile"> | <a id="button-cam_profile"></a>Profile | `CAM_Profile` | Profile entire model, selected face(s) or selected edge(s) |
| <img src="toolbar-icons/CAM_Sanity.png" width="11" height="11" alt="Sanity Check"> | <a id="button-cam_sanity"></a>Sanity Check | `CAM_Sanity` | Checks the CAM job for common errors |
| <img src="toolbar-icons/CAM_SelectLoop.png" width="11" height="11" alt="Finish Selecting Loop"> | <a id="button-cam_selectloop"></a>Finish Selecting Loop | `CAM_SelectLoop` | Completes the selection of edges or faces that forms a loop. Works in described sequence, but can be forced by modifier key. Face selection: Vertical face: searching loops faces which forms the walls or vertical faces with same center height (SHIFT). Horizontal face: searching inner edges of the face (CTRL), outer edges of the face (CTRL + ALT) or horizontal faces at the same height (SHIFT). Otherwise select all edges of the face (ALT). Edge selection: One edge: searching loop edges in horizontal plane. Two edges: searching loop edges in wires of the shape or tangent edges (CTRL). Otherwise searching horizontal wires which contain selected edges (ALT). Without sub selection: Select all edges, faces (ALT) or vertexes (CTRL) of the model. |
| <img src="toolbar-icons/CAM_SimTools.png" width="11" height="11" alt="CAM Simulator"> | <a id="button-cam_simtools"></a>CAM Simulator | `CAM_SimTools` | Simulates G-code on stock |
| <img src="toolbar-icons/CAM_SimTools_1.png" width="11" height="11" alt="Legacy CAM Simulator"> | â†³ Legacy CAM Simulator | `CAM_SimTools` | Simulates G-code on stock |
| <img src="toolbar-icons/CAM_SimpleCopy.png" width="11" height="11" alt="Simple Copy"> | <a id="button-cam_simplecopy"></a>Simple Copy | `CAM_SimpleCopy` | Creates a non-parametric copy of another toolpath Several operations can be used with identical tool controller and coolant mode |
| <img src="toolbar-icons/CAM_Slot.png" width="11" height="11" alt="Slot"> | <a id="button-cam_slot"></a>Slot | `CAM_Slot` | Create a single horizontal slot between two points. Points can be specified through selected geometry or custom points. Allowed selection only from one model: - two vertexes, - one or two edges, - one horizontal or vertical face, - one or two vertical faces. |
| <img src="toolbar-icons/CAM_ToolBitDock.png" width="11" height="11" alt="Add Toolbitâ€¦"> | <a id="button-cam_toolbitdock"></a>Add Toolbitâ€¦ | `CAM_ToolBitDock` | Opens the toolbit selection dialog |
| <img src="toolbar-icons/CAM_Workplane.png" width="11" height="11" alt="Work Plane"> | <a id="button-cam_workplane"></a>Work Plane | `CAM_Workplane` | Create a named work plane on the Job, from a selected planar face or at the Job origin. Operations can share one work plane. |
| <img src="toolbar-icons/Draft_AddConstruction.png" width="11" height="11" alt="Add to Construction Group"> | <a id="button-draft_addconstruction"></a>Add to Construction Group | `Draft_AddConstruction` | Adds the selected objects to the construction group, and changes their appearance to the construction style. The construction group is created if it does not exist. |
| <img src="toolbar-icons/Draft_AddNamedGroup.png" width="11" height="11" alt="New Named Group"> | <a id="button-draft_addnamedgroup"></a>New Named Group | `Draft_AddNamedGroup` | Adds a group with a given name |
| <img src="toolbar-icons/Draft_AddToGroup.png" width="11" height="11" alt="Add to Group"> | <a id="button-draft_addtogroup"></a>Add to Group | `Draft_AddToGroup` | Adds selected objects to a group, or removes them from any group |
| <img src="toolbar-icons/Draft_AddToLayer.png" width="11" height="11" alt="Add to Layer"> | <a id="button-draft_addtolayer"></a>Add to Layer | `Draft_AddToLayer` | Adds selected objects to a layer, or removes them from any layer |
| <img src="toolbar-icons/Draft_AnnotationStyleEditor.png" width="11" height="11" alt="Annotation Styles"> | <a id="button-draft_annotationstyleeditor"></a>Annotation Styles | `Draft_AnnotationStyleEditor` | Opens an editor to manage or create annotation styles |
| <img src="toolbar-icons/Draft_Arc.png" width="11" height="11" alt="Arc"> | <a id="button-draft_arc"></a>Arc | `Draft_Arc` | Creates a circular arc from a center point and a radius |
| <img src="toolbar-icons/Draft_ArcTools.png" width="11" height="11" alt="Arc"> | <a id="button-draft_arctools"></a>Arc | `Draft_ArcTools` | Creates a circular arc from a center point and a radius |
| <img src="toolbar-icons/Draft_ArcTools_1.png" width="11" height="11" alt="Arc From 3 Points"> | â†³ Arc From 3 Points | `Draft_ArcTools` | Creates a circular arc from 3 points |
| <img src="toolbar-icons/Draft_Arc_3Points.png" width="11" height="11" alt="Arc From 3 Points"> | <a id="button-draft_arc_3points"></a>Arc From 3 Points | `Draft_Arc_3Points` | Creates a circular arc from 3 points |
| <img src="toolbar-icons/Draft_ArrayTools.png" width="11" height="11" alt="Array"> | <a id="button-draft_arraytools"></a>Array | `Draft_ArrayTools` | Creates copies of the selected object in an orthogonal pattern |
| <img src="toolbar-icons/Draft_ArrayTools_1.png" width="11" height="11" alt="Polar Array"> | â†³ Polar Array | `Draft_ArrayTools` | Creates copies of the selected object in a polar pattern |
| <img src="toolbar-icons/Draft_ArrayTools_2.png" width="11" height="11" alt="Circular Array"> | â†³ Circular Array | `Draft_ArrayTools` | Creates copies of the selected object in a radial pattern with 1 or more circular layers |
| <img src="toolbar-icons/Draft_ArrayTools_3.png" width="11" height="11" alt="Path Array"> | â†³ Path Array | `Draft_ArrayTools` | Creates copies of the selected object along a selected path |
| <img src="toolbar-icons/Draft_ArrayTools_4.png" width="11" height="11" alt="Path Link Array"> | â†³ Path Link Array | `Draft_ArrayTools` | Creates linked copies of the selected object along a selected path |
| <img src="toolbar-icons/Draft_ArrayTools_5.png" width="11" height="11" alt="Point Array"> | â†³ Point Array | `Draft_ArrayTools` | Creates copies of the selected object at the points of a point object |
| <img src="toolbar-icons/Draft_ArrayTools_6.png" width="11" height="11" alt="Point Link Array"> | â†³ Point Link Array | `Draft_ArrayTools` | Creates linked copies of the selected object at the points of a point object |
| <img src="toolbar-icons/Draft_ArrayTools_7.png" width="11" height="11" alt="Twisted Path Array"> | â†³ Twisted Path Array | `Draft_ArrayTools` | Creates twisted copies of the selected object along a selected path |
| <img src="toolbar-icons/Draft_ArrayTools_8.png" width="11" height="11" alt="Twisted Path Link Array"> | â†³ Twisted Path Link Array | `Draft_ArrayTools` | Creates twisted linked copies of the selected object along a selected path |
| <img src="toolbar-icons/Draft_BSpline.png" width="11" height="11" alt="B-Spline"> | <a id="button-draft_bspline"></a>B-Spline | `Draft_BSpline` | Creates a multiple-point B-spline |
| <img src="toolbar-icons/Draft_BezCurve.png" width="11" height="11" alt="BÃ©zier Curve"> | <a id="button-draft_bezcurve"></a>BÃ©zier Curve | `Draft_BezCurve` | Creates an n-degree BÃ©zier curve. The more points, the higher the degree. |
| <img src="toolbar-icons/Draft_BezierTools.png" width="11" height="11" alt="Cubic BÃ©zier Curve"> | <a id="button-draft_beziertools"></a>Cubic BÃ©zier Curve | `Draft_BezierTools` | Creates a BÃ©zier curve made of 2nd degree (quadratic) and 3rd degree (cubic) segments. Clicking and dragging allows to define segments. Control points and properties of each knot can be edited after creation. |
| <img src="toolbar-icons/Draft_BezierTools_1.png" width="11" height="11" alt="BÃ©zier Curve"> | â†³ BÃ©zier Curve | `Draft_BezierTools` | Creates an n-degree BÃ©zier curve. The more points, the higher the degree. |
| <img src="toolbar-icons/Draft_Circle.png" width="11" height="11" alt="Circle"> | <a id="button-draft_circle"></a>Circle | `Draft_Circle` | Creates a circle (full circular arc) |
| <img src="toolbar-icons/Draft_CircularArray.png" width="11" height="11" alt="Circular Array"> | <a id="button-draft_circulararray"></a>Circular Array | `Draft_CircularArray` | Creates copies of the selected object in a radial pattern with 1 or more circular layers |
| <img src="toolbar-icons/Draft_Clone.png" width="11" height="11" alt="Clone"> | <a id="button-draft_clone"></a>Clone | `Draft_Clone` | Creates a clone of the selected objects |
| <img src="toolbar-icons/Draft_CubicBezCurve.png" width="11" height="11" alt="Cubic BÃ©zier Curve"> | <a id="button-draft_cubicbezcurve"></a>Cubic BÃ©zier Curve | `Draft_CubicBezCurve` | Creates a BÃ©zier curve made of 2nd degree (quadratic) and 3rd degree (cubic) segments. Clicking and dragging allows to define segments. Control points and properties of each knot can be edited after creation. |
| <img src="toolbar-icons/Draft_Dimension.png" width="11" height="11" alt="Dimension"> | <a id="button-draft_dimension"></a>Dimension | `Draft_Dimension` | Creates a linear dimension for a straight edge, a circular edge, or 2 picked points, or an angular dimension for 2 straight edges |
| <img src="toolbar-icons/Draft_Downgrade.png" width="11" height="11" alt="Downgrade"> | <a id="button-draft_downgrade"></a>Downgrade | `Draft_Downgrade` | Downgrades the selected objects into simpler shapes. The result of the operation depends on the types of objects, which may be downgraded several times in a row. For example, a 3D solid is deconstructed into separate faces, wires, and then edges. Faces can also be subtracted. |
| <img src="toolbar-icons/Draft_Draft2Sketch.png" width="11" height="11" alt="Draft to Sketch"> | <a id="button-draft_draft2sketch"></a>Draft to Sketch | `Draft_Draft2Sketch` | Converts bidirectionally between Draft objects and sketches. Multiple selected Draft objects are converted into a single sketch. However, a single sketch with disconnected traces is converted into several individual Draft objects. |
| <img src="toolbar-icons/Draft_Edit.png" width="11" height="11" alt="Edit"> | <a id="button-draft_edit"></a>Edit | `Draft_Edit` | Edits the active object |
| <img src="toolbar-icons/Draft_Ellipse.png" width="11" height="11" alt="Ellipse"> | <a id="button-draft_ellipse"></a>Ellipse | `Draft_Ellipse` | Creates an ellipse |
| <img src="toolbar-icons/Draft_Facebinder.png" width="11" height="11" alt="Facebinder"> | <a id="button-draft_facebinder"></a>Facebinder | `Draft_Facebinder` | Creates a facebinder from the selected faces |
| <img src="toolbar-icons/Draft_Fillet.png" width="11" height="11" alt="Fillet"> | <a id="button-draft_fillet"></a>Fillet | `Draft_Fillet` | Creates a fillet between 2 selected edges |
| <img src="toolbar-icons/Draft_FlipDimension.png" width="11" height="11" alt="Flip Dimension"> | <a id="button-draft_flipdimension"></a>Flip Dimension | `Draft_FlipDimension` | Flips the normal direction of the selected dimensions (linear, radial, angular). If other objects are selected they are ignored. |
| <img src="toolbar-icons/Draft_Hatch.png" width="11" height="11" alt="Hatch"> | <a id="button-draft_hatch"></a>Hatch | `Draft_Hatch` | Creates hatches on the faces of a selected object |
| <img src="toolbar-icons/Draft_Join.png" width="11" height="11" alt="Join"> | <a id="button-draft_join"></a>Join | `Draft_Join` | Joins the selected lines or polylines into a single object. The lines must share a common point at the start or at the end. |
| <img src="toolbar-icons/Draft_Label.png" width="11" height="11" alt="Label"> | <a id="button-draft_label"></a>Label | `Draft_Label` | Creates a label, optionally attached to a selected object or subelement |
| <img src="toolbar-icons/Draft_LayerManager.png" width="11" height="11" alt="Manage Layers"> | <a id="button-draft_layermanager"></a>Manage Layers | `Draft_LayerManager` | Allows to modify the layers |
| <img src="toolbar-icons/Draft_Line.png" width="11" height="11" alt="Line"> | <a id="button-draft_line"></a>Line | `Draft_Line` | Creates a 2-point line |
| <img src="toolbar-icons/Draft_Mirror.png" width="11" height="11" alt="Mirror"> | <a id="button-draft_mirror"></a>Mirror | `Draft_Mirror` | Mirrors the selected objects along a line defined by 2 points |
| <img src="toolbar-icons/Draft_Move.png" width="11" height="11" alt="Move"> | <a id="button-draft_move"></a>Move | `Draft_Move` | Moves the selected objects. If the "Copy" option is active, it creates displaced copies. |
| <img src="toolbar-icons/Draft_Offset.png" width="11" height="11" alt="Offset"> | <a id="button-draft_offset"></a>Offset | `Draft_Offset` | Offsets the selected object. It can also create an offset copy of the original object. |
| <img src="toolbar-icons/Draft_OrthoArray.png" width="11" height="11" alt="Array"> | <a id="button-draft_orthoarray"></a>Array | `Draft_OrthoArray` | Creates copies of the selected object in an orthogonal pattern |
| <img src="toolbar-icons/Draft_PathArray.png" width="11" height="11" alt="Path Array"> | <a id="button-draft_patharray"></a>Path Array | `Draft_PathArray` | Creates copies of the selected object along a selected path |
| <img src="toolbar-icons/Draft_PathLinkArray.png" width="11" height="11" alt="Path Link Array"> | <a id="button-draft_pathlinkarray"></a>Path Link Array | `Draft_PathLinkArray` | Creates linked copies of the selected object along a selected path |
| <img src="toolbar-icons/Draft_PathTwistedArray.png" width="11" height="11" alt="Twisted Path Array"> | <a id="button-draft_pathtwistedarray"></a>Twisted Path Array | `Draft_PathTwistedArray` | Creates twisted copies of the selected object along a selected path |
| <img src="toolbar-icons/Draft_PathTwistedLinkArray.png" width="11" height="11" alt="Twisted Path Link Array"> | <a id="button-draft_pathtwistedlinkarray"></a>Twisted Path Link Array | `Draft_PathTwistedLinkArray` | Creates twisted linked copies of the selected object along a selected path |
| <img src="toolbar-icons/Draft_Point.png" width="11" height="11" alt="Point"> | <a id="button-draft_point"></a>Point | `Draft_Point` | Creates a point |
| <img src="toolbar-icons/Draft_PointArray.png" width="11" height="11" alt="Point Array"> | <a id="button-draft_pointarray"></a>Point Array | `Draft_PointArray` | Creates copies of the selected object at the points of a point object |
| <img src="toolbar-icons/Draft_PointLinkArray.png" width="11" height="11" alt="Point Link Array"> | <a id="button-draft_pointlinkarray"></a>Point Link Array | `Draft_PointLinkArray` | Creates linked copies of the selected object at the points of a point object |
| <img src="toolbar-icons/Draft_PolarArray.png" width="11" height="11" alt="Polar Array"> | <a id="button-draft_polararray"></a>Polar Array | `Draft_PolarArray` | Creates copies of the selected object in a polar pattern |
| <img src="toolbar-icons/Draft_Polygon.png" width="11" height="11" alt="Polygon"> | <a id="button-draft_polygon"></a>Polygon | `Draft_Polygon` | Creates a regular polygon (triangle, square, pentagonâ€¦) |
| <img src="toolbar-icons/Draft_Rectangle.png" width="11" height="11" alt="Rectangle"> | <a id="button-draft_rectangle"></a>Rectangle | `Draft_Rectangle` | Creates a 2-point rectangle |
| <img src="toolbar-icons/Draft_Rotate.png" width="11" height="11" alt="Rotate"> | <a id="button-draft_rotate"></a>Rotate | `Draft_Rotate` | Rotates the selected objects. If the "Copy" option is active, it will create rotated copies. |
| <img src="toolbar-icons/Draft_Scale.png" width="11" height="11" alt="Scale"> | <a id="button-draft_scale"></a>Scale | `Draft_Scale` | Scales the selected objects from a base point |
| <img src="toolbar-icons/Draft_SelectGroup.png" width="11" height="11" alt="Select Group"> | <a id="button-draft_selectgroup"></a>Select Group | `Draft_SelectGroup` | Selects the contents of selected groups. For selected non-group objects, the contents of the group they are in are selected. |
| <img src="toolbar-icons/Draft_Shape2DView.png" width="11" height="11" alt="Shape 2D View"> | <a id="button-draft_shape2dview"></a>Shape 2D View | `Draft_Shape2DView` | Creates a 2D projection of the selected objects on the XY-plane. The initial projection direction is the opposite of the current active view direction. |
| <img src="toolbar-icons/Draft_ShapeString.png" width="11" height="11" alt="Shape From Text"> | <a id="button-draft_shapestring"></a>Shape From Text | `Draft_ShapeString` | Creates a shape from a text string and a specified font |
| <img src="toolbar-icons/Draft_Slope.png" width="11" height="11" alt="Set Slope"> | <a id="button-draft_slope"></a>Set Slope | `Draft_Slope` | Sets the slope of the selected line by changing the value of the Z value of one of its points. If a polyline is selected, it will apply the slope transformation to each of its segments. The slope will always change the Z value, therefore this command only works well for straight Draft lines that are drawn on the XY-plane. |
| <img src="toolbar-icons/Draft_Snap_Angle.png" width="11" height="11" alt="Snap Angle"> | <a id="button-draft_snap_angle"></a>Snap Angle | `Draft_Snap_Angle` | Snaps to the special cardinal points on circular edges, at multiples of 30Â° and 45Â° |
| <img src="toolbar-icons/Draft_Snap_Center.png" width="11" height="11" alt="Snap Center"> | <a id="button-draft_snap_center"></a>Snap Center | `Draft_Snap_Center` | Snaps to the center point of faces and circular edges, and to the placement point of working plane proxies and building parts |
| <img src="toolbar-icons/Draft_Snap_Dimensions.png" width="11" height="11" alt="Snap Dimensions"> | <a id="button-draft_snap_dimensions"></a>Snap Dimensions | `Draft_Snap_Dimensions` | Shows temporary X and Y dimensions |
| <img src="toolbar-icons/Draft_Snap_Endpoint.png" width="11" height="11" alt="Snap Endpoint"> | <a id="button-draft_snap_endpoint"></a>Snap Endpoint | `Draft_Snap_Endpoint` | Snaps to the endpoints of edges |
| <img src="toolbar-icons/Draft_Snap_Extension.png" width="11" height="11" alt="Snap Extension"> | <a id="button-draft_snap_extension"></a>Snap Extension | `Draft_Snap_Extension` | Snaps to an imaginary line that extends beyond the endpoints of straight edges |
| <img src="toolbar-icons/Draft_Snap_Grid.png" width="11" height="11" alt="Snap Grid"> | <a id="button-draft_snap_grid"></a>Snap Grid | `Draft_Snap_Grid` | Snaps to the intersections of grid lines |
| <img src="toolbar-icons/Draft_Snap_Intersection.png" width="11" height="11" alt="Snap Intersection"> | <a id="button-draft_snap_intersection"></a>Snap Intersection | `Draft_Snap_Intersection` | Snaps to the intersection of 2 edges, and the intersection of a face and an edge |
| <img src="toolbar-icons/Draft_Snap_Lock.png" width="11" height="11" alt="Snap Lock"> | <a id="button-draft_snap_lock"></a>Snap Lock | `Draft_Snap_Lock` | Enables or disables snapping globally |
| <img src="toolbar-icons/Draft_Snap_Midpoint.png" width="11" height="11" alt="Snap Midpoint"> | <a id="button-draft_snap_midpoint"></a>Snap Midpoint | `Draft_Snap_Midpoint` | Snaps to the midpoint of edges |
| <img src="toolbar-icons/Draft_Snap_Near.png" width="11" height="11" alt="Snap Near"> | <a id="button-draft_snap_near"></a>Snap Near | `Draft_Snap_Near` | Snaps to the nearest point on faces and edges |
| <img src="toolbar-icons/Draft_Snap_Ortho.png" width="11" height="11" alt="Snap Ortho"> | <a id="button-draft_snap_ortho"></a>Snap Ortho | `Draft_Snap_Ortho` | Snaps to imaginary lines that cross the previous point at multiples of 45Â° |
| <img src="toolbar-icons/Draft_Snap_Parallel.png" width="11" height="11" alt="Snap Parallel"> | <a id="button-draft_snap_parallel"></a>Snap Parallel | `Draft_Snap_Parallel` | Snaps to an imaginary line parallel to straight edges |
| <img src="toolbar-icons/Draft_Snap_Perpendicular.png" width="11" height="11" alt="Snap Perpendicular"> | <a id="button-draft_snap_perpendicular"></a>Snap Perpendicular | `Draft_Snap_Perpendicular` | Snaps to the perpendicular points on faces and edges |
| <img src="toolbar-icons/Draft_Snap_Special.png" width="11" height="11" alt="Snap Special"> | <a id="button-draft_snap_special"></a>Snap Special | `Draft_Snap_Special` | Snaps to special points defined by the object |
| <img src="toolbar-icons/Draft_Snap_WorkingPlane.png" width="11" height="11" alt="Snap Working Plane"> | <a id="button-draft_snap_workingplane"></a>Snap Working Plane | `Draft_Snap_WorkingPlane` | Projects snap points onto the current working plane |
| <img src="toolbar-icons/Draft_Split.png" width="11" height="11" alt="Split"> | <a id="button-draft_split"></a>Split | `Draft_Split` | Splits the selected line or polyline at a specified point |
| <img src="toolbar-icons/Draft_Stretch.png" width="11" height="11" alt="Stretch"> | <a id="button-draft_stretch"></a>Stretch | `Draft_Stretch` | Stretches the selected objects |
| <img src="toolbar-icons/Draft_SubelementHighlight.png" width="11" height="11" alt="Highlight Subelements"> | <a id="button-draft_subelementhighlight"></a>Highlight Subelements | `Draft_SubelementHighlight` | Highlights the subelements of the selected objects, to be able to move, rotate, and scale them |
| <img src="toolbar-icons/Draft_Text.png" width="11" height="11" alt="Text"> | <a id="button-draft_text"></a>Text | `Draft_Text` | Creates a multi-line annotation |
| <img src="toolbar-icons/Draft_ToggleDisplayMode.png" width="11" height="11" alt="Toggle Wireframe"> | <a id="button-draft_toggledisplaymode"></a>Toggle Wireframe | `Draft_ToggleDisplayMode` | Switches the view style of the selected objects from Flat Lines to Wireframe and back |
| <img src="toolbar-icons/Draft_ToggleGrid.png" width="11" height="11" alt="Toggle Grid"> | <a id="button-draft_togglegrid"></a>Toggle Grid | `Draft_ToggleGrid` | Toggles the visibility of the Draft grid |
| <img src="toolbar-icons/Draft_Trimex.png" width="11" height="11" alt="Trimex"> | <a id="button-draft_trimex"></a>Trimex | `Draft_Trimex` | Trims or extends the selected object |
| <img src="toolbar-icons/Draft_UpdateShape2DView.png" width="11" height="11" alt="Force 2D View Update"> | <a id="button-draft_updateshape2dview"></a>Force 2D View Update | `Draft_UpdateShape2DView` | Forces an update of the selected 2D Views or all 2D Views in the document. The 'Auto Update' property of the views is ignored. |
| <img src="toolbar-icons/Draft_Upgrade.png" width="11" height="11" alt="Upgrade"> | <a id="button-draft_upgrade"></a>Upgrade | `Draft_Upgrade` | Upgrades the selected objects into more complex shapes. The result of the operation depends on the types of objects, which may be able to be upgraded several times in a row. For example, it can join the selected objects into one, convert simple edges into parametric polylines, convert closed edges into filled faces and parametric polygons, and merge faces into a single face. |
| <img src="toolbar-icons/Draft_Wire.png" width="11" height="11" alt="Polyline"> | <a id="button-draft_wire"></a>Polyline | `Draft_Wire` | Creates a polyline |
| <img src="toolbar-icons/Draft_WireToBSpline.png" width="11" height="11" alt="Convert Wire/B-Spline"> | <a id="button-draft_wiretobspline"></a>Convert Wire/B-Spline | `Draft_WireToBSpline` | Converts the selected polyline to a B-spline, or the selected B-spline to a polyline |
| <img src="toolbar-icons/Draft_WorkingPlaneProxy.png" width="11" height="11" alt="Working Plane Proxy"> | <a id="button-draft_workingplaneproxy"></a>Working Plane Proxy | `Draft_WorkingPlaneProxy` | Creates a proxy object from the current working plane that allows to restore the camera position and visibility of objects |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_Analysis.svg" width="11" height="11" alt="New Analysis"> | <a id="button-fem_analysis"></a>New Analysis | `FEM_Analysis` | Creates an analysis container with default solver |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ClippingPlaneAdd.svg" width="11" height="11" alt="Clipping Plane on Face"> | <a id="button-fem_clippingplaneadd"></a>Clipping Plane on Face | `FEM_ClippingPlaneAdd` | Adds a clipping plane on a selected face |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ClippingPlaneRemoveAll.svg" width="11" height="11" alt="Remove All Clipping Planes"> | <a id="button-fem_clippingplaneremoveall"></a>Remove All Clipping Planes | `FEM_ClippingPlaneRemoveAll` | Removes all clipping planes |
| â€” | <a id="button-fem_compemconstraints"></a>Electromagnetic Boundary Conditions | `FEM_CompEmConstraints` | Electromagnetic boundary conditions |
| â€” | <a id="button-fem_compemequations"></a>Electromagnetic Equations | `FEM_CompEmEquations` | Electromagnetic equations for the Elmer solver |
| â€” | <a id="button-fem_compmechequations"></a>Mechanical Equations | `FEM_CompMechEquations` | Mechanical equations for the Elmer solver |
| â€” | <a id="button-fem_compsolvers"></a>Solvers | `FEM_CompSolvers` | Creates a FEM solver |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintBodyHeatSource.svg" width="11" height="11" alt="Body Heat Source"> | <a id="button-fem_constraintbodyheatsource"></a>Body Heat Source | `FEM_ConstraintBodyHeatSource` | Creates a body heat source |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintCentrif.svg" width="11" height="11" alt="Centrifugal Load"> | <a id="button-fem_constraintcentrif"></a>Centrifugal Load | `FEM_ConstraintCentrif` | Creates a centrifugal load |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintContact.svg" width="11" height="11" alt="Contact Constraint"> | <a id="button-fem_constraintcontact"></a>Contact Constraint | `FEM_ConstraintContact` | Creates a contact constraint between faces |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintCurrentDensity.svg" width="11" height="11" alt="Current Density Boundary Condition"> | <a id="button-fem_constraintcurrentdensity"></a>Current Density Boundary Condition | `FEM_ConstraintCurrentDensity` | Creates a current density boundary condition |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintDisplacement.svg" width="11" height="11" alt="Displacement Boundary Condition"> | <a id="button-fem_constraintdisplacement"></a>Displacement Boundary Condition | `FEM_ConstraintDisplacement` | Creates a displacement boundary condition for a geometric entity |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintElectricChargeDensity.svg" width="11" height="11" alt="Electric Charge Density"> | <a id="button-fem_constraintelectricchargedensity"></a>Electric Charge Density | `FEM_ConstraintElectricChargeDensity` | Creates an electric charge density |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintElectromagnetic.svg" width="11" height="11" alt="Electromagnetic Boundary Condition"> | <a id="button-fem_constraintelectromagnetic"></a>Electromagnetic Boundary Condition | `FEM_ConstraintElectromagnetic` | Creates an electromagnetic boundary condition |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintFixed.svg" width="11" height="11" alt="Fixed Boundary Condition"> | <a id="button-fem_constraintfixed"></a>Fixed Boundary Condition | `FEM_ConstraintFixed` | Creates a fixed boundary condition for a geometric entity |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintFlowVelocity.svg" width="11" height="11" alt="Flow Velocity Boundary Condition"> | <a id="button-fem_constraintflowvelocity"></a>Flow Velocity Boundary Condition | `FEM_ConstraintFlowVelocity` | Creates a flow velocity boundary condition |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintForce.svg" width="11" height="11" alt="Force Load"> | <a id="button-fem_constraintforce"></a>Force Load | `FEM_ConstraintForce` | Creates a force load applied to a geometric entity |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintHeatflux.svg" width="11" height="11" alt="Heat Flux Load"> | <a id="button-fem_constraintheatflux"></a>Heat Flux Load | `FEM_ConstraintHeatflux` | Creates a heat flux load acting on a face |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialFlowVelocity.svg" width="11" height="11" alt="Initial Flow Velocity Condition"> | <a id="button-fem_constraintinitialflowvelocity"></a>Initial Flow Velocity Condition | `FEM_ConstraintInitialFlowVelocity` | Creates an initial flow velocity condition |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialPressure.svg" width="11" height="11" alt="Initial Pressure Condition"> | <a id="button-fem_constraintinitialpressure"></a>Initial Pressure Condition | `FEM_ConstraintInitialPressure` | Creates an initial pressure condition |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialTemperature.svg" width="11" height="11" alt="Initial Temperature"> | <a id="button-fem_constraintinitialtemperature"></a>Initial Temperature | `FEM_ConstraintInitialTemperature` | Creates an initial temperature acting on a body |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintMagnetization.svg" width="11" height="11" alt="Magnetization Boundary Condition"> | <a id="button-fem_constraintmagnetization"></a>Magnetization Boundary Condition | `FEM_ConstraintMagnetization` | Creates a magnetization boundary condition |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintPlaneRotation.svg" width="11" height="11" alt="Plane Multi-Point Constraint"> | <a id="button-fem_constraintplanerotation"></a>Plane Multi-Point Constraint | `FEM_ConstraintPlaneRotation` | Creates a plane multi-point constraint for a face |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintPressure.svg" width="11" height="11" alt="Pressure Load"> | <a id="button-fem_constraintpressure"></a>Pressure Load | `FEM_ConstraintPressure` | Creates a pressure load acting on a face |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintRigidBody.svg" width="11" height="11" alt="Rigid Body Constraint"> | <a id="button-fem_constraintrigidbody"></a>Rigid Body Constraint | `FEM_ConstraintRigidBody` | Creates a rigid body constraint for a geometric entity |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSectionPrint.svg" width="11" height="11" alt="Section Print Feature"> | <a id="button-fem_constraintsectionprint"></a>Section Print Feature | `FEM_ConstraintSectionPrint` | Creates a section print feature |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSelfWeight.svg" width="11" height="11" alt="Gravity Load"> | <a id="button-fem_constraintselfweight"></a>Gravity Load | `FEM_ConstraintSelfWeight` | Creates a gravity load |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSpring.svg" width="11" height="11" alt="Spring Boundary Condition"> | <a id="button-fem_constraintspring"></a>Spring Boundary Condition | `FEM_ConstraintSpring` | Creates a spring boundary condition on a face |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTemperature.svg" width="11" height="11" alt="Temperature Boundary Condition"> | <a id="button-fem_constrainttemperature"></a>Temperature Boundary Condition | `FEM_ConstraintTemperature` | Creates a temperature/concentrated heat flux load acting on a face |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTie.svg" width="11" height="11" alt="Tie Constraint"> | <a id="button-fem_constrainttie"></a>Tie Constraint | `FEM_ConstraintTie` | Creates a tie constraint |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTransform.svg" width="11" height="11" alt="Local Coordinate System"> | <a id="button-fem_constrainttransform"></a>Local Coordinate System | `FEM_ConstraintTransform` | Creates a local coordinate system on a face |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementFluid1D.svg" width="11" height="11" alt="Fluid Section for 1D Flow"> | <a id="button-fem_elementfluid1d"></a>Fluid Section for 1D Flow | `FEM_ElementFluid1D` | Creates a fluid section for 1D flow |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementGeometry1D.svg" width="11" height="11" alt="Beam Cross Section"> | <a id="button-fem_elementgeometry1d"></a>Beam Cross Section | `FEM_ElementGeometry1D` | Creates a beam cross section |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementGeometry2D.svg" width="11" height="11" alt="Shell Plate Thickness"> | <a id="button-fem_elementgeometry2d"></a>Shell Plate Thickness | `FEM_ElementGeometry2D` | Creates a shell plate thickness |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementRotation1D.svg" width="11" height="11" alt="Beam Rotation"> | <a id="button-fem_elementrotation1d"></a>Beam Rotation | `FEM_ElementRotation1D` | Creates a beam rotation |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationDeformation.svg" width="11" height="11" alt="Deformation Equation"> | <a id="button-fem_equationdeformation"></a>Deformation Equation | `FEM_EquationDeformation` | Creates an equation for deformation (nonlinear elasticity) |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationElasticity.svg" width="11" height="11" alt="Elasticity Equation"> | <a id="button-fem_equationelasticity"></a>Elasticity Equation | `FEM_EquationElasticity` | Creates an equation for elasticity (stress) |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationElectricforce.svg" width="11" height="11" alt="Electricforce Equation"> | <a id="button-fem_equationelectricforce"></a>Electricforce Equation | `FEM_EquationElectricforce` | Creates an equation for electric forces |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationElectrostatic.svg" width="11" height="11" alt="Electrostatic Equation"> | <a id="button-fem_equationelectrostatic"></a>Electrostatic Equation | `FEM_EquationElectrostatic` | Creates an equation for electrostatic |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationFlow.svg" width="11" height="11" alt="Flow Equation"> | <a id="button-fem_equationflow"></a>Flow Equation | `FEM_EquationFlow` | Creates an equation for flow |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationFlux.svg" width="11" height="11" alt="Flux Equation"> | <a id="button-fem_equationflux"></a>Flux Equation | `FEM_EquationFlux` | Creates an equation for flux |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationHeat.svg" width="11" height="11" alt="Heat Equation"> | <a id="button-fem_equationheat"></a>Heat Equation | `FEM_EquationHeat` | Creates an equation for heat |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationMagnetodynamic.svg" width="11" height="11" alt="Magnetodynamic Equation"> | <a id="button-fem_equationmagnetodynamic"></a>Magnetodynamic Equation | `FEM_EquationMagnetodynamic` | Creates an equation for magnetodynamic forces |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationMagnetodynamic2D.svg" width="11" height="11" alt="Magnetodynamic 2D Equation"> | <a id="button-fem_equationmagnetodynamic2d"></a>Magnetodynamic 2D Equation | `FEM_EquationMagnetodynamic2D` | Creates an equation for 2D magnetodynamic forces |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationStaticCurrent.svg" width="11" height="11" alt="Static Current Equation"> | <a id="button-fem_equationstaticcurrent"></a>Static Current Equation | `FEM_EquationStaticCurrent` | Creates an equation for static current |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FemWorkbench.svg" width="11" height="11" alt="FEM Examples"> | <a id="button-fem_examples"></a>FEM Examples | `FEM_Examples` | Opens the FEM examples |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_FEMMesh2Mesh.svg" width="11" height="11" alt="FEM Mesh to Mesh"> | <a id="button-fem_femmesh2mesh"></a>FEM Mesh to Mesh | `FEM_FEMMesh2Mesh` | Converts the surface of a FEM mesh to a mesh |
| <img src="../../../src/Mod/BIM/Resources/icons/Arch_Material_Group.svg" width="11" height="11" alt="Material Editor"> | <a id="button-fem_materialeditor"></a>Material Editor | `FEM_MaterialEditor` | Opens the FreeCAD material editor |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialFluid.svg" width="11" height="11" alt="Fluid Material"> | <a id="button-fem_materialfluid"></a>Fluid Material | `FEM_MaterialFluid` | Creates a fluid material |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialMechanicalNonlinear.svg" width="11" height="11" alt="Non-Linear Mechanical Material"> | <a id="button-fem_materialmechanicalnonlinear"></a>Non-Linear Mechanical Material | `FEM_MaterialMechanicalNonlinear` | Add non-linear mechanical properties to material |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialReinforced.svg" width="11" height="11" alt="Reinforced Material (Concrete)"> | <a id="button-fem_materialreinforced"></a>Reinforced Material (Concrete) | `FEM_MaterialReinforced` | Creates a material for reinforced matrix material such as concrete |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialSolid.svg" width="11" height="11" alt="Solid Material"> | <a id="button-fem_materialsolid"></a>Solid Material | `FEM_MaterialSolid` | Creates a solid material |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshAdvanced.svg" width="11" height="11" alt="Advanced Refinement Types"> | <a id="button-fem_meshadvanced"></a>Advanced Refinement Types | `FEM_MeshAdvanced` | Allows to define the mesh size by various advanced means |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshBoundaryLayer.svg" width="11" height="11" alt="2D Boundary Layer"> | <a id="button-fem_meshboundarylayer"></a>2D Boundary Layer | `FEM_MeshBoundaryLayer` | Adds a structured layer of mesh elements on 2D model boundaries |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshDistance.svg" width="11" height="11" alt="Distance-Based Refinement"> | <a id="button-fem_meshdistance"></a>Distance-Based Refinement | `FEM_MeshDistance` | Sets mesh size based on the distance to vertices, edges, and faces |
| â€” | <a id="button-fem_meshgmshrefinement"></a>GMSH Refinements | `FEM_MeshGMSHRefinement` | Mesh refinements for the GMSH mesh generation |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshGmshFromShape.svg" width="11" height="11" alt="Mesh From Shape by Gmsh"> | <a id="button-fem_meshgmshfromshape"></a>Mesh From Shape by Gmsh | `FEM_MeshGmshFromShape` | Creates a FEM mesh from a shape by Gmsh mesher |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshGroup.svg" width="11" height="11" alt="Mesh Group"> | <a id="button-fem_meshgroup"></a>Mesh Group | `FEM_MeshGroup` | Creates a mesh group |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshManipulate.svg" width="11" height="11" alt="Manipulate Refinement"> | <a id="button-fem_meshmanipulate"></a>Manipulate Refinement | `FEM_MeshManipulate` | Allows to manipulate the output of a refinement in various ways |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshNetgenFromShape.svg" width="11" height="11" alt="Mesh From Shape by Netgen"> | <a id="button-fem_meshnetgenfromshape"></a>Mesh From Shape by Netgen | `FEM_MeshNetgenFromShape` | Creates a FEM mesh from a solid or face shape by Netgen internal mesher |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshRegion.svg" width="11" height="11" alt="Mesh Refinement"> | <a id="button-fem_meshregion"></a>Mesh Refinement | `FEM_MeshRegion` | Creates a FEM mesh refinement |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshShape.svg" width="11" height="11" alt="Shape-Based Refinement"> | <a id="button-fem_meshshape"></a>Shape-Based Refinement | `FEM_MeshShape` | Sets mesh size within and outside of a geometric shape (box, sphere, cylinder) |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshTransfiniteCurve.svg" width="11" height="11" alt="Structured Transfinite Curve"> | <a id="button-fem_meshtransfinitecurve"></a>Structured Transfinite Curve | `FEM_MeshTransfiniteCurve` | Creates a fixed number of nodes on an edge with a structured algorithm |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshTransfiniteSurface.svg" width="11" height="11" alt="Structured Transfinite Surface"> | <a id="button-fem_meshtransfinitesurface"></a>Structured Transfinite Surface | `FEM_MeshTransfiniteSurface` | Creates a structured mesh on a face |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshTransfiniteVolume.svg" width="11" height="11" alt="Structured Transfinite Volume"> | <a id="button-fem_meshtransfinitevolume"></a>Structured Transfinite Volume | `FEM_MeshTransfiniteVolume` | Creates a structured mesh in a 4- or 5-sided volume bounded by transfinite surfaces |
| <img src="../../../src/Gui/Icons/view-refresh.svg" width="11" height="11" alt="Apply Changes to Pipeline"> | <a id="button-fem_postapplychanges"></a>Apply Changes to Pipeline | `FEM_PostApplyChanges` | Applies changes to parameters directly and not on recompute only |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostBranchFilter.svg" width="11" height="11" alt="Pipeline Branch"> | <a id="button-fem_postbranchfilter"></a>Pipeline Branch | `FEM_PostBranchFilter` | Branches the pipeline into a new path |
| â€” | <a id="button-fem_postcreatefunctions"></a>Filter Functions | `FEM_PostCreateFunctions` | Functions for use in postprocessing filter |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterCalculator.svg" width="11" height="11" alt="Calculator Filter"> | <a id="button-fem_postfiltercalculator"></a>Calculator Filter | `FEM_PostFilterCalculator` | Creates a new field from current data |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterClipRegion.svg" width="11" height="11" alt="Region Clip Filter"> | <a id="button-fem_postfilterclipregion"></a>Region Clip Filter | `FEM_PostFilterClipRegion` | Defines a clip filter which uses functions to define the clipped region |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterClipScalar.svg" width="11" height="11" alt="Scalar Clip Filter"> | <a id="button-fem_postfilterclipscalar"></a>Scalar Clip Filter | `FEM_PostFilterClipScalar` | Defines a clip filter which clips a field with a scalar value |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterContours.svg" width="11" height="11" alt="Contours Filter"> | <a id="button-fem_postfiltercontours"></a>Contours Filter | `FEM_PostFilterContours` | Defines a contours filter that displays iso contours |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterCutFunction.svg" width="11" height="11" alt="Function Cut Filter"> | <a id="button-fem_postfiltercutfunction"></a>Function Cut Filter | `FEM_PostFilterCutFunction` | Cuts the data along an implicit function |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterDataAlongLine.svg" width="11" height="11" alt="Line Clip Filter"> | <a id="button-fem_postfilterdataalongline"></a>Line Clip Filter | `FEM_PostFilterDataAlongLine` | Defines a clip filter which clips a field along a line |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterDataAtPoint.svg" width="11" height="11" alt="Data at Point Clip Filter"> | <a id="button-fem_postfilterdataatpoint"></a>Data at Point Clip Filter | `FEM_PostFilterDataAtPoint` | Defines a clip filter which clips a field data at point |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterGlyph.svg" width="11" height="11" alt="Glyph Filter"> | <a id="button-fem_postfilterglyph"></a>Glyph Filter | `FEM_PostFilterGlyph` | Adds a post-processing filter that adds glyphs to the mesh vertices for vertex data visualization |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterLinearizedStresses.svg" width="11" height="11" alt="Stress Linearization Plot"> | <a id="button-fem_postfilterlinearizedstresses"></a>Stress Linearization Plot | `FEM_PostFilterLinearizedStresses` | Defines a stress linearization plot |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterWarp.svg" width="11" height="11" alt="Warp Filter"> | <a id="button-fem_postfilterwarp"></a>Warp Filter | `FEM_PostFilterWarp` | Warps the geometry along a vector field by a certain factor |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostPipelineFromResult.svg" width="11" height="11" alt="Post Pipeline From Result"> | <a id="button-fem_postpipelinefromresult"></a>Post Pipeline From Result | `FEM_PostPipelineFromResult` | Creates a post processing pipeline from a result object |
| â€” | <a id="button-fem_postvisualization"></a>Data Visualizations | `FEM_PostVisualization` | Different visualizations to show post processing data in |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ResultShow.svg" width="11" height="11" alt="Show Result"> | <a id="button-fem_resultshow"></a>Show Result | `FEM_ResultShow` | Shows and visualizes the selected result data |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_ResultsPurge.svg" width="11" height="11" alt="Purge Results"> | <a id="button-fem_resultspurge"></a>Purge Results | `FEM_ResultsPurge` | Purges all results from the active analysis |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverStandard.svg" width="11" height="11" alt="Solver CalculiX"> | <a id="button-fem_solvercalculix"></a>Solver CalculiX | `FEM_SolverCalculiX` | Creates a FEM solver CalculiX |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverControl.svg" width="11" height="11" alt="Solver Job Control"> | <a id="button-fem_solvercontrol"></a>Solver Job Control | `FEM_SolverControl` | Changes solver attributes and runs the calculations for the selected solver |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverElmer.svg" width="11" height="11" alt="Solver Elmer"> | <a id="button-fem_solverelmer"></a>Solver Elmer | `FEM_SolverElmer` | Creates a FEM solver Elmer |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverMystran.svg" width="11" height="11" alt="Solver Mystran"> | <a id="button-fem_solvermystran"></a>Solver Mystran | `FEM_SolverMystran` | Creates a FEM solver Mystran |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverRun.svg" width="11" height="11" alt="Run Solver"> | <a id="button-fem_solverrun"></a>Run Solver | `FEM_SolverRun` | Runs the calculations for the selected solver |
| <img src="../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverZ88.svg" width="11" height="11" alt="Solver Z88"> | <a id="button-fem_solverz88"></a>Solver Z88 | `FEM_SolverZ88` | Creates a FEM solver Z88 |
| <img src="../../../src/Mod/Inspection/Gui/Resources/icons/inspect_pipette.svg" width="11" height="11" alt="Inspectionâ€¦"> | <a id="button-inspection_inspectelement"></a>Inspectionâ€¦ | `Inspection_InspectElement` | Inspects distance information |
| <img src="../../../src/Mod/Inspection/Gui/Resources/icons/InspectionWorkbench.svg" width="11" height="11" alt="Visual Inspection"> | <a id="button-inspection_visualinspection"></a>Visual Inspection | `Inspection_VisualInspection` | Inspects the objects visually |
| <img src="toolbar-icons/Material_Edit.png" width="11" height="11" alt="Edit"> | <a id="button-material_edit"></a>Edit | `Material_Edit` | Edits material properties |
| <img src="../../../src/Gui/Icons/preferences-general.svg" width="11" height="11" alt="Mesh From Shape"> | <a id="button-meshpart_mesher"></a>Mesh From Shape | `MeshPart_Mesher` | Tessellate shape |
| <img src="toolbar-icons/Mesh_AddFacet.png" width="11" height="11" alt="Add Triangle"> | <a id="button-mesh_addfacet"></a>Add Triangle | `Mesh_AddFacet` | Adds a triangle manually to a mesh |
| <img src="toolbar-icons/Mesh_BoundingBox.png" width="11" height="11" alt="Bounding Box Info"> | <a id="button-mesh_boundingbox"></a>Bounding Box Info | `Mesh_BoundingBox` | Shows the bounding box coordinates of the selected mesh |
| <img src="toolbar-icons/Mesh_BuildRegularSolid.png" width="11" height="11" alt="Regular Solid"> | <a id="button-mesh_buildregularsolid"></a>Regular Solid | `Mesh_BuildRegularSolid` | Builds a regular solid |
| <img src="toolbar-icons/Mesh_CrossSections.png" width="11" height="11" alt="Cross-Sections"> | <a id="button-mesh_crosssections"></a>Cross-Sections | `Mesh_CrossSections` | Creates cross-sections of the mesh |
| <img src="toolbar-icons/Mesh_CurvatureInfo.png" width="11" height="11" alt="Curvature Info"> | <a id="button-mesh_curvatureinfo"></a>Curvature Info | `Mesh_CurvatureInfo` | Displays information about the curvature |
| <img src="toolbar-icons/Mesh_Decimating.png" width="11" height="11" alt="Decimate"> | <a id="button-mesh_decimating"></a>Decimate | `Mesh_Decimating` | Decimates a mesh |
| <img src="toolbar-icons/Mesh_Difference.png" width="11" height="11" alt="Difference"> | <a id="button-mesh_difference"></a>Difference | `Mesh_Difference` | Creates a boolean difference of the selected meshes |
| <img src="toolbar-icons/Mesh_EvaluateFacet.png" width="11" height="11" alt="Face Info"> | <a id="button-mesh_evaluatefacet"></a>Face Info | `Mesh_EvaluateFacet` | Displays information about the selected faces |
| <img src="toolbar-icons/Mesh_EvaluateSolid.png" width="11" height="11" alt="Evaluate Solid"> | <a id="button-mesh_evaluatesolid"></a>Evaluate Solid | `Mesh_EvaluateSolid` | Checks whether the mesh is a solid |
| <img src="toolbar-icons/Mesh_Evaluation.png" width="11" height="11" alt="Evaluate and Repair"> | <a id="button-mesh_evaluation"></a>Evaluate and Repair | `Mesh_Evaluation` | Opens a dialog to analyze and repair a mesh |
| <img src="toolbar-icons/Mesh_Export.png" width="11" height="11" alt="Export Meshâ€¦"> | <a id="button-mesh_export"></a>Export Meshâ€¦ | `Mesh_Export` | Exports a mesh to a file |
| <img src="toolbar-icons/Mesh_FillInteractiveHole.png" width="11" height="11" alt="Close Hole"> | <a id="button-mesh_fillinteractivehole"></a>Close Hole | `Mesh_FillInteractiveHole` | Closes a hole interactively in the mesh |
| <img src="toolbar-icons/Mesh_FillupHoles.png" width="11" height="11" alt="Fill Holes"> | <a id="button-mesh_fillupholes"></a>Fill Holes | `Mesh_FillupHoles` | Fills holes in the mesh |
| <img src="toolbar-icons/Mesh_FlipNormals.png" width="11" height="11" alt="Flip Normals"> | <a id="button-mesh_flipnormals"></a>Flip Normals | `Mesh_FlipNormals` | Flips the normals of the selected mesh |
| <img src="toolbar-icons/Mesh_FromPartShape.png" width="11" height="11" alt="Mesh From Shape"> | <a id="button-mesh_frompartshape"></a>Mesh From Shape | `Mesh_FromPartShape` | Tessellates the selected shape to a mesh |
| <img src="toolbar-icons/Mesh_HarmonizeNormals.png" width="11" height="11" alt="Harmonize Normals"> | <a id="button-mesh_harmonizenormals"></a>Harmonize Normals | `Mesh_HarmonizeNormals` | Harmonizes the normals of the mesh |
| <img src="toolbar-icons/Mesh_Import.png" width="11" height="11" alt="Import Meshâ€¦"> | <a id="button-mesh_import"></a>Import Meshâ€¦ | `Mesh_Import` | Imports a mesh from a file |
| <img src="toolbar-icons/Mesh_Intersection.png" width="11" height="11" alt="Intersection"> | <a id="button-mesh_intersection"></a>Intersection | `Mesh_Intersection` | Creates a boolean intersection from the selected meshes |
| <img src="toolbar-icons/Mesh_Merge.png" width="11" height="11" alt="Merge"> | <a id="button-mesh_merge"></a>Merge | `Mesh_Merge` | Merges selected meshes into one |
| <img src="toolbar-icons/Mesh_PolyCut.png" width="11" height="11" alt="Cut"> | <a id="button-mesh_polycut"></a>Cut | `Mesh_PolyCut` | Cuts the mesh with a selected polygon |
| <img src="toolbar-icons/Mesh_PolyTrim.png" width="11" height="11" alt="Trim"> | <a id="button-mesh_polytrim"></a>Trim | `Mesh_PolyTrim` | Trims a mesh with a picked polygon |
| <img src="toolbar-icons/Mesh_RemeshGmsh.png" width="11" height="11" alt="Refinement"> | <a id="button-mesh_remeshgmsh"></a>Refinement | `Mesh_RemeshGmsh` | Refines an existing mesh |
| <img src="toolbar-icons/Mesh_RemoveComponents.png" width="11" height="11" alt="Remove Components"> | <a id="button-mesh_removecomponents"></a>Remove Components | `Mesh_RemoveComponents` | Removes topologically independent components from the mesh |
| <img src="toolbar-icons/Mesh_Scale.png" width="11" height="11" alt="Scale"> | <a id="button-mesh_scale"></a>Scale | `Mesh_Scale` | Scales the selected mesh objects |
| <img src="toolbar-icons/Mesh_SectionByPlane.png" width="11" height="11" alt="Section From Plane"> | <a id="button-mesh_sectionbyplane"></a>Section From Plane | `Mesh_SectionByPlane` | Sections the mesh with the selected plane |
| <img src="toolbar-icons/Mesh_Segmentation.png" width="11" height="11" alt="Segmentation"> | <a id="button-mesh_segmentation"></a>Segmentation | `Mesh_Segmentation` | Creates new mesh segments from the mesh |
| <img src="toolbar-icons/Mesh_SegmentationBestFit.png" width="11" height="11" alt="Segmentation From Best-Fit Surfaces"> | <a id="button-mesh_segmentationbestfit"></a>Segmentation From Best-Fit Surfaces | `Mesh_SegmentationBestFit` | Creates new mesh segments from the best-fit surfaces |
| <img src="toolbar-icons/Mesh_Smoothing.png" width="11" height="11" alt="Smooth"> | <a id="button-mesh_smoothing"></a>Smooth | `Mesh_Smoothing` | Smoothes the selected meshes |
| <img src="toolbar-icons/Mesh_SplitComponents.png" width="11" height="11" alt="Split by Components"> | <a id="button-mesh_splitcomponents"></a>Split by Components | `Mesh_SplitComponents` | Splits the selected mesh into its components |
| <img src="toolbar-icons/Mesh_TrimByPlane.png" width="11" height="11" alt="Trim With Plane"> | <a id="button-mesh_trimbyplane"></a>Trim With Plane | `Mesh_TrimByPlane` | Trims a mesh by removing faces on one side of a selected plane |
| <img src="toolbar-icons/Mesh_Union.png" width="11" height="11" alt="Union"> | <a id="button-mesh_union"></a>Union | `Mesh_Union` | Unifies the selected meshes |
| <img src="toolbar-icons/Mesh_VertexCurvature.png" width="11" height="11" alt="Curvature Plot"> | <a id="button-mesh_vertexcurvature"></a>Curvature Plot | `Mesh_VertexCurvature` | Calculates the curvature of the vertices of a mesh |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_AddOpenSCADElement.svg" width="11" height="11" alt="Add OpenSCAD Element"> | <a id="button-openscad_addopenscadelement"></a>Add OpenSCAD Element | `OpenSCAD_AddOpenSCADElement` | Adds an OpenSCAD element based on entered OpenSCAD code using the OpenSCAD binary |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Explode_Group.svg" width="11" height="11" alt="Explode Group"> | <a id="button-openscad_explodegroup"></a>Explode Group | `OpenSCAD_ExplodeGroup` | Explodes a fusion or compound and applies random colors |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Hull.svg" width="11" height="11" alt="Hull"> | <a id="button-openscad_hull"></a>Hull | `OpenSCAD_Hull` | Creates a hull |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_IncreaseToleranceFeature.svg" width="11" height="11" alt="Increase Tolerance Feature"> | <a id="button-openscad_increasetolerancefeature"></a>Increase Tolerance Feature | `OpenSCAD_IncreaseToleranceFeature` | Creates a feature to increase the tolerance |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_MeshBooleans.svg" width="11" height="11" alt="Mesh Boolean"> | <a id="button-openscad_meshboolean"></a>Mesh Boolean | `OpenSCAD_MeshBoolean` | Performs a boolean operation using the OpenSCAD binary |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Minkowski.svg" width="11" height="11" alt="Minkowski Sum"> | <a id="button-openscad_minkowski"></a>Minkowski Sum | `OpenSCAD_Minkowski` | Creates a Minkowski sum |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_RefineShapeFeature.svg" width="11" height="11" alt="Refine Shape Feature"> | <a id="button-openscad_refineshapefeature"></a>Refine Shape Feature | `OpenSCAD_RefineShapeFeature` | Creates a refined shape |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_RemoveSubtree.svg" width="11" height="11" alt="Remove Objects and Children"> | <a id="button-openscad_removesubtree"></a>Remove Objects and Children | `OpenSCAD_RemoveSubtree` | Removes the selected objects and all children that are not referenced by other objects |
| <img src="../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_ReplaceObject.svg" width="11" height="11" alt="Replace Object"> | <a id="button-openscad_replaceobject"></a>Replace Object | `OpenSCAD_ReplaceObject` | Replaces an object in the Tree View |
| <img src="toolbar-icons/PartDesign_AddReferenceObject.png" width="11" height="11" alt="Add Reference Object"> | <a id="button-partdesign_addreferenceobject"></a>Add Reference Object | `PartDesign_AddReferenceObject` | Reference evaluated geometry from a direct child of the active component |
| <img src="toolbar-icons/PartDesign_AdditiveHelix.png" width="11" height="11" alt="Additive Helix"> | <a id="button-partdesign_additivehelix"></a>Additive Helix | `PartDesign_AdditiveHelix` | Sweeps the selected sketch or profile along a helix and adds it to the body |
| <img src="toolbar-icons/PartDesign_AdditiveLoft.png" width="11" height="11" alt="Additive Loft"> | <a id="button-partdesign_additiveloft"></a>Additive Loft | `PartDesign_AdditiveLoft` | Lofts the selected sketch or profile through one or more sections and adds it to the body |
| <img src="toolbar-icons/PartDesign_AdditivePipe.png" width="11" height="11" alt="Additive Pipe"> | <a id="button-partdesign_additivepipe"></a>Additive Pipe | `PartDesign_AdditivePipe` | Sweeps the selected sketch or profile along a path and adds it to the body |
| <img src="toolbar-icons/PartDesign_Body.png" width="11" height="11" alt="New Body"> | <a id="button-partdesign_body"></a>New Body | `PartDesign_Body` | Creates a new body and activates it |
| <img src="toolbar-icons/PartDesign_Boolean.png" width="11" height="11" alt="Boolean Operation"> | <a id="button-partdesign_boolean"></a>Boolean Operation | `PartDesign_Boolean` | Applies boolean operations with the selected objects and the active body |
| <img src="toolbar-icons/PartDesign_Chamfer.png" width="11" height="11" alt="Chamfer"> | <a id="button-partdesign_chamfer"></a>Chamfer | `PartDesign_Chamfer` | Applies a chamfer to the selected edges or faces |
| <img src="toolbar-icons/PartDesign_CircularPattern.png" width="11" height="11" alt="Circular Pattern"> | <a id="button-partdesign_circularpattern"></a>Circular Pattern | `PartDesign_CircularPattern` | Duplicates the selected features or the active body in concentric circular patterns |
| <img src="toolbar-icons/PartDesign_Clone.png" width="11" height="11" alt="Clone"> | <a id="button-partdesign_clone"></a>Clone | `PartDesign_Clone` | Copies a solid object parametrically as the base feature of a new body |
| <img src="toolbar-icons/PartDesign_CompPrimitiveAdditive.png" width="11" height="11" alt="Additive Box"> | <a id="button-partdesign_compprimitiveadditive"></a>Additive Box | `PartDesign_CompPrimitiveAdditive` | Creates an additive box by its width, height, and length |
| <img src="toolbar-icons/PartDesign_CompPrimitiveAdditive_1.png" width="11" height="11" alt="Additive Cylinder"> | â†³ Additive Cylinder | `PartDesign_CompPrimitiveAdditive` | Creates an additive cylinder by its radius, height, and angle |
| <img src="toolbar-icons/PartDesign_CompPrimitiveAdditive_2.png" width="11" height="11" alt="Additive Sphere"> | â†³ Additive Sphere | `PartDesign_CompPrimitiveAdditive` | Creates an additive sphere by its radius and various angles |
| <img src="toolbar-icons/PartDesign_CompPrimitiveAdditive_3.png" width="11" height="11" alt="Additive Cone"> | â†³ Additive Cone | `PartDesign_CompPrimitiveAdditive` | Creates an additive cone |
| <img src="toolbar-icons/PartDesign_CompPrimitiveAdditive_4.png" width="11" height="11" alt="Additive Ellipsoid"> | â†³ Additive Ellipsoid | `PartDesign_CompPrimitiveAdditive` | Creates an additive ellipsoid |
| <img src="toolbar-icons/PartDesign_CompPrimitiveAdditive_5.png" width="11" height="11" alt="Additive Torus"> | â†³ Additive Torus | `PartDesign_CompPrimitiveAdditive` | Creates an additive torus |
| <img src="toolbar-icons/PartDesign_CompPrimitiveAdditive_6.png" width="11" height="11" alt="Additive Prism"> | â†³ Additive Prism | `PartDesign_CompPrimitiveAdditive` | Creates an additive prism |
| <img src="toolbar-icons/PartDesign_CompPrimitiveAdditive_7.png" width="11" height="11" alt="Additive Wedge"> | â†³ Additive Wedge | `PartDesign_CompPrimitiveAdditive` | Creates an additive wedge |
| <img src="toolbar-icons/PartDesign_CompPrimitiveSubtractive.png" width="11" height="11" alt="Subtractive Box"> | <a id="button-partdesign_compprimitivesubtractive"></a>Subtractive Box | `PartDesign_CompPrimitiveSubtractive` | Creates a subtractive box by its width, height and length |
| <img src="toolbar-icons/PartDesign_CompPrimitiveSubtractive_1.png" width="11" height="11" alt="Subtractive Cylinder"> | â†³ Subtractive Cylinder | `PartDesign_CompPrimitiveSubtractive` | Creates a subtractive cylinder by its radius, height and angle |
| <img src="toolbar-icons/PartDesign_CompPrimitiveSubtractive_2.png" width="11" height="11" alt="Subtractive Sphere"> | â†³ Subtractive Sphere | `PartDesign_CompPrimitiveSubtractive` | Creates a subtractive sphere by its radius and various angles |
| <img src="toolbar-icons/PartDesign_CompPrimitiveSubtractive_3.png" width="11" height="11" alt="Subtractive Cone"> | â†³ Subtractive Cone | `PartDesign_CompPrimitiveSubtractive` | Creates a subtractive cone |
| <img src="toolbar-icons/PartDesign_CompPrimitiveSubtractive_4.png" width="11" height="11" alt="Subtractive Ellipsoid"> | â†³ Subtractive Ellipsoid | `PartDesign_CompPrimitiveSubtractive` | Creates a subtractive ellipsoid |
| <img src="toolbar-icons/PartDesign_CompPrimitiveSubtractive_5.png" width="11" height="11" alt="Subtractive Torus"> | â†³ Subtractive Torus | `PartDesign_CompPrimitiveSubtractive` | Creates a subtractive torus |
| <img src="toolbar-icons/PartDesign_CompPrimitiveSubtractive_6.png" width="11" height="11" alt="Subtractive Prism"> | â†³ Subtractive Prism | `PartDesign_CompPrimitiveSubtractive` | Creates a subtractive prism |
| <img src="toolbar-icons/PartDesign_CompPrimitiveSubtractive_7.png" width="11" height="11" alt="Subtractive Wedge"> | â†³ Subtractive Wedge | `PartDesign_CompPrimitiveSubtractive` | Creates a subtractive wedge |
| <img src="toolbar-icons/PartDesign_CompSketches.png" width="11" height="11" alt="New Sketch"> | <a id="button-partdesign_compsketches"></a>New Sketch | `PartDesign_CompSketches` | Creates a new sketch |
| <img src="toolbar-icons/PartDesign_CompSketches_1.png" width="11" height="11" alt="Attach Sketch"> | â†³ Attach Sketch | `PartDesign_CompSketches` | Attaches a sketch to the selected geometry element |
| <img src="toolbar-icons/PartDesign_CompSketches_2.png" width="11" height="11" alt="Edit Sketch"> | â†³ Edit Sketch | `PartDesign_CompSketches` | Opens the selected sketch for editing |
| <img src="toolbar-icons/PartDesign_Defeaturing.png" width="11" height="11" alt="Defeaturing"> | <a id="button-partdesign_defeaturing"></a>Defeaturing | `PartDesign_Defeaturing` | Removes selected faces from a solid |
| <img src="toolbar-icons/PartDesign_Draft.png" width="11" height="11" alt="Draft"> | <a id="button-partdesign_draft"></a>Draft | `PartDesign_Draft` | Applies a draft to the selected faces |
| <img src="toolbar-icons/PartDesign_Extrude.png" width="11" height="11" alt="Extrude"> | <a id="button-partdesign_extrude"></a>Extrude | `PartDesign_Extrude` | Extrudes a profile with Add or Subtract selected in the task panel |
| <img src="toolbar-icons/PartDesign_Fillet.png" width="11" height="11" alt="Fillet"> | <a id="button-partdesign_fillet"></a>Fillet | `PartDesign_Fillet` | Applies a fillet to the selected edges or faces |
| <img src="toolbar-icons/PartDesign_Groove.png" width="11" height="11" alt="Groove"> | <a id="button-partdesign_groove"></a>Groove | `PartDesign_Groove` | Revolves the sketch or profile around a line or axis and removes it from the body |
| <img src="toolbar-icons/PartDesign_Hole.png" width="11" height="11" alt="Hole"> | <a id="button-partdesign_hole"></a>Hole | `PartDesign_Hole` | Creates holes in the active body at the center points of circles or arcs of the selected sketch or profile |
| <img src="toolbar-icons/PartDesign_LinearPattern.png" width="11" height="11" alt="Linear Pattern"> | <a id="button-partdesign_linearpattern"></a>Linear Pattern | `PartDesign_LinearPattern` | Duplicates the selected features or the active body in a linear pattern |
| <img src="toolbar-icons/PartDesign_Mirrored.png" width="11" height="11" alt="Mirror"> | <a id="button-partdesign_mirrored"></a>Mirror | `PartDesign_Mirrored` | Mirrors the selected features or active body |
| <img src="toolbar-icons/PartDesign_MultiTransform.png" width="11" height="11" alt="Multi-Transform"> | <a id="button-partdesign_multitransform"></a>Multi-Transform | `PartDesign_MultiTransform` | Applies multiple transformations to the selected features or active body |
| <img src="toolbar-icons/PartDesign_NewSketch.png" width="11" height="11" alt="New Sketch"> | <a id="button-partdesign_newsketch"></a>New Sketch | `PartDesign_NewSketch` | Creates a new sketch |
| <img src="toolbar-icons/PartDesign_Pad.png" width="11" height="11" alt="Pad"> | <a id="button-partdesign_pad"></a>Pad | `PartDesign_Pad` | Extrudes a sketch or profile selected before or within the task panel and adds it to the body |
| <img src="toolbar-icons/PartDesign_PathPattern.png" width="11" height="11" alt="Path Pattern"> | <a id="button-partdesign_pathpattern"></a>Path Pattern | `PartDesign_PathPattern` | Duplicates the selected features or the active body along a path |
| <img src="toolbar-icons/PartDesign_Pattern.png" width="11" height="11" alt="Pattern"> | <a id="button-partdesign_pattern"></a>Pattern | `PartDesign_Pattern` | Creates a linear or circular pattern; select the type and features in the task pane |
| <img src="toolbar-icons/PartDesign_Pocket.png" width="11" height="11" alt="Pocket"> | <a id="button-partdesign_pocket"></a>Pocket | `PartDesign_Pocket` | Extrudes the selected sketch or profile and removes it from the body |
| <img src="toolbar-icons/PartDesign_PointPattern.png" width="11" height="11" alt="Point Pattern"> | <a id="button-partdesign_pointpattern"></a>Point Pattern | `PartDesign_PointPattern` | Duplicates the selected features or the active body at points from a shape |
| <img src="toolbar-icons/PartDesign_PolarPattern.png" width="11" height="11" alt="Polar Pattern"> | <a id="button-partdesign_polarpattern"></a>Polar Pattern | `PartDesign_PolarPattern` | Duplicates the selected features or the active body in a circular pattern |
| <img src="toolbar-icons/PartDesign_Revolution.png" width="11" height="11" alt="Revolve"> | <a id="button-partdesign_revolution"></a>Revolve | `PartDesign_Revolution` | Revolves the selected sketch or profile around a line or axis and adds it to the body |
| <img src="toolbar-icons/PartDesign_SubShapeBinder.png" width="11" height="11" alt="Sub-Shape Binder"> | <a id="button-partdesign_subshapebinder"></a>Sub-Shape Binder | `PartDesign_SubShapeBinder` | Creates a reference to geometry from one or more objects, allowing it to be used inside or outside a body. It tracks relative placements, supports multiple geometry types (solids, faces, edges, vertices), and can work with objects in the same or external documents. |
| <img src="toolbar-icons/PartDesign_SubtractiveHelix.png" width="11" height="11" alt="Subtractive Helix"> | <a id="button-partdesign_subtractivehelix"></a>Subtractive Helix | `PartDesign_SubtractiveHelix` | Sweeps the selected sketch or profile along a helix and removes it from the body |
| <img src="toolbar-icons/PartDesign_SubtractiveLoft.png" width="11" height="11" alt="Subtractive Loft"> | <a id="button-partdesign_subtractiveloft"></a>Subtractive Loft | `PartDesign_SubtractiveLoft` | Lofts the selected sketch or profile through one or more sections and removes it from the body |
| <img src="toolbar-icons/PartDesign_SubtractivePipe.png" width="11" height="11" alt="Subtractive Pipe"> | <a id="button-partdesign_subtractivepipe"></a>Subtractive Pipe | `PartDesign_SubtractivePipe` | Sweeps the selected sketch or profile along a path and removes it from the body |
| <img src="toolbar-icons/PartDesign_Thickness.png" width="11" height="11" alt="Thickness"> | <a id="button-partdesign_thickness"></a>Thickness | `PartDesign_Thickness` | Applies thickness and removes the selected faces |
| <img src="toolbar-icons/Part_Boolean.png" width="11" height="11" alt="Boolean Operation"> | <a id="button-part_boolean"></a>Boolean Operation | `Part_Boolean` | Applies a boolean operation with the selected shapes |
| <img src="toolbar-icons/Part_BooleanFragments.png" width="11" height="11" alt="Boolean Fragments"> | <a id="button-part_booleanfragments"></a>Boolean Fragments | `Part_BooleanFragments` | Creates a boolean union which is sliced at the intersections of the selected shapes |
| <img src="toolbar-icons/Part_Box.png" width="11" height="11" alt="Cube"> | <a id="button-part_box"></a>Cube | `Part_Box` | Creates a solid cube |
| <img src="toolbar-icons/Part_Builder.png" width="11" height="11" alt="Shape Builder"> | <a id="button-part_builder"></a>Shape Builder | `Part_Builder` | Advanced utility to create shapes |
| <img src="toolbar-icons/Part_Chamfer.png" width="11" height="11" alt="Chamfer"> | <a id="button-part_chamfer"></a>Chamfer | `Part_Chamfer` | Chamfers the selected edges of a shape |
| <img src="toolbar-icons/Part_CheckGeometry.png" width="11" height="11" alt="Check Geometry"> | <a id="button-part_checkgeometry"></a>Check Geometry | `Part_CheckGeometry` | Analyzes the selected shapes for errors |
| <img src="toolbar-icons/Part_ColorPerFace.png" width="11" height="11" alt="Appearance per Face"> | <a id="button-part_colorperface"></a>Appearance per Face | `Part_ColorPerFace` | Sets the appearance of individual faces of the selected object |
| <img src="toolbar-icons/Part_Common.png" width="11" height="11" alt="Intersection"> | <a id="button-part_common"></a>Intersection | `Part_Common` | Intersects the selected shapes |
| <img src="toolbar-icons/Part_CompCompoundTools.png" width="11" height="11" alt="Compound"> | <a id="button-part_compcompoundtools"></a>Compound | `Part_CompCompoundTools` | Compounds the selected shapes |
| <img src="toolbar-icons/Part_CompCompoundTools_1.png" width="11" height="11" alt="Explode Compound"> | â†³ Explode Compound | `Part_CompCompoundTools` | Splits up a compound of shapes into separate objects, creating a compound filter for each shape |
| <img src="toolbar-icons/Part_CompCompoundTools_2.png" width="11" height="11" alt="Compound Filter"> | â†³ Compound Filter | `Part_CompCompoundTools` | Filters out objects from the selected compound by characteristics like volume, area, or length, or by choosing specific items. If a second object is selected, it will be used as reference, for example, for collision or distance filtering. |
| <img src="toolbar-icons/Part_CompJoinFeatures.png" width="11" height="11" alt="Connect Shapes"> | <a id="button-part_compjoinfeatures"></a>Connect Shapes | `Part_CompJoinFeatures` | Fuses shapes, taking care to preserve voids |
| <img src="toolbar-icons/Part_CompJoinFeatures_1.png" width="11" height="11" alt="Embed Shapes"> | â†³ Embed Shapes | `Part_CompJoinFeatures` | Fuses one shape into another, taking care to preserve voids |
| <img src="toolbar-icons/Part_CompJoinFeatures_2.png" width="11" height="11" alt="Cutout Shape"> | â†³ Cutout Shape | `Part_CompJoinFeatures` | Creates a cutout in the selected shape to fit another shape |
| <img src="toolbar-icons/Part_CompOffset.png" width="11" height="11" alt="3D Offset"> | <a id="button-part_compoffset"></a>3D Offset | `Part_CompOffset` | Offsets shapes in 3D |
| <img src="toolbar-icons/Part_CompOffset_1.png" width="11" height="11" alt="2D Offset"> | â†³ 2D Offset | `Part_CompOffset` | Offsets planar shapes in 2D |
| <img src="toolbar-icons/Part_CompSplitFeatures.png" width="11" height="11" alt="Boolean Fragments"> | <a id="button-part_compsplitfeatures"></a>Boolean Fragments | `Part_CompSplitFeatures` | Creates a boolean union which is sliced at the intersections of the selected shapes |
| <img src="toolbar-icons/Part_CompSplitFeatures_1.png" width="11" height="11" alt="Slice Apart"> | â†³ Slice Apart | `Part_CompSplitFeatures` | Slices the selected object by other objects, and splits it apart, creating a compound filter for each slide |
| <img src="toolbar-icons/Part_CompSplitFeatures_2.png" width="11" height="11" alt="Slice to Compound"> | â†³ Slice to Compound | `Part_CompSplitFeatures` | Slices the selected object by using other objects as cutting tools and storing the results in one compound |
| <img src="toolbar-icons/Part_CompSplitFeatures_3.png" width="11" height="11" alt="Boolean XOR"> | â†³ Boolean XOR | `Part_CompSplitFeatures` | Performs an 'exclusive OR' boolean operation with two or more selected objects, or with the shapes inside a compound. Overlapping volumes of the shapes will be removed. |
| <img src="toolbar-icons/Part_Compound.png" width="11" height="11" alt="Compound"> | <a id="button-part_compound"></a>Compound | `Part_Compound` | Compounds the selected shapes |
| <img src="toolbar-icons/Part_CompoundFilter.png" width="11" height="11" alt="Compound Filter"> | <a id="button-part_compoundfilter"></a>Compound Filter | `Part_CompoundFilter` | Filters out objects from the selected compound by characteristics like volume, area, or length, or by choosing specific items. If a second object is selected, it will be used as reference, for example, for collision or distance filtering. |
| <img src="toolbar-icons/Part_Cone.png" width="11" height="11" alt="Cone"> | <a id="button-part_cone"></a>Cone | `Part_Cone` | Creates a solid cone |
| <img src="toolbar-icons/Part_CoordinateSystem.png" width="11" height="11" alt="Coordinate System"> | <a id="button-part_coordinatesystem"></a>Coordinate System | `Part_CoordinateSystem` | Creates a coordinate system that can be attached to other objects |
| <img src="toolbar-icons/Part_CrossSections.png" width="11" height="11" alt="Cross-Sections"> | <a id="button-part_crosssections"></a>Cross-Sections | `Part_CrossSections` | Creates cross-sections |
| <img src="toolbar-icons/Part_Cut.png" width="11" height="11" alt="Cut"> | <a id="button-part_cut"></a>Cut | `Part_Cut` | Cuts 2 selected shapes |
| <img src="toolbar-icons/Part_Cylinder.png" width="11" height="11" alt="Cylinder"> | <a id="button-part_cylinder"></a>Cylinder | `Part_Cylinder` | Creates a solid cylinder |
| <img src="toolbar-icons/Part_DatumLine.png" width="11" height="11" alt="Datum Line"> | <a id="button-part_datumline"></a>Datum Line | `Part_DatumLine` | Creates a datum line that can be attached to other objects |
| <img src="toolbar-icons/Part_DatumPlane.png" width="11" height="11" alt="Datum Plane"> | <a id="button-part_datumplane"></a>Datum Plane | `Part_DatumPlane` | Creates a datum plane that can be attached to other objects |
| <img src="toolbar-icons/Part_DatumPoint.png" width="11" height="11" alt="Datum Point"> | <a id="button-part_datumpoint"></a>Datum Point | `Part_DatumPoint` | Creates a datum point that can be attached to other objects |
| <img src="toolbar-icons/Part_Datums.png" width="11" height="11" alt="Coordinate System"> | <a id="button-part_datums"></a>Coordinate System | `Part_Datums` | Creates a coordinate system that can be attached to other objects |
| <img src="toolbar-icons/Part_Datums_1.png" width="11" height="11" alt="Datum Plane"> | â†³ Datum Plane | `Part_Datums` | Creates a datum plane that can be attached to other objects |
| <img src="toolbar-icons/Part_Datums_2.png" width="11" height="11" alt="Datum Line"> | â†³ Datum Line | `Part_Datums` | Creates a datum line that can be attached to other objects |
| <img src="toolbar-icons/Part_Datums_3.png" width="11" height="11" alt="Datum Point"> | â†³ Datum Point | `Part_Datums` | Creates a datum point that can be attached to other objects |
| <img src="toolbar-icons/Part_Defeaturing.png" width="11" height="11" alt="Defeaturing"> | <a id="button-part_defeaturing"></a>Defeaturing | `Part_Defeaturing` | Removes the selected features from a shape |
| <img src="toolbar-icons/Part_ExplodeCompound.png" width="11" height="11" alt="Explode Compound"> | <a id="button-part_explodecompound"></a>Explode Compound | `Part_ExplodeCompound` | Splits up a compound of shapes into separate objects, creating a compound filter for each shape |
| <img src="toolbar-icons/Part_Extrude.png" width="11" height="11" alt="Extrude"> | <a id="button-part_extrude"></a>Extrude | `Part_Extrude` | Extrudes the selected sketch or profile |
| <img src="toolbar-icons/Part_Fillet.png" width="11" height="11" alt="Fillet"> | <a id="button-part_fillet"></a>Fillet | `Part_Fillet` | Fillets the selected edges of a shape |
| <img src="toolbar-icons/Part_Fuse.png" width="11" height="11" alt="Union"> | <a id="button-part_fuse"></a>Union | `Part_Fuse` | Unites the selected shapes |
| <img src="toolbar-icons/Part_IsoclineCurve.png" width="11" height="11" alt="Isocline Curve"> | <a id="button-part_isoclinecurve"></a>Isocline Curve | `Part_IsoclineCurve` | Create associative draft-angle curves on selected faces |
| <img src="toolbar-icons/Part_JoinConnect.png" width="11" height="11" alt="Connect Shapes"> | <a id="button-part_joinconnect"></a>Connect Shapes | `Part_JoinConnect` | Fuses shapes, taking care to preserve voids |
| <img src="toolbar-icons/Part_JoinCutout.png" width="11" height="11" alt="Cutout Shape"> | <a id="button-part_joincutout"></a>Cutout Shape | `Part_JoinCutout` | Creates a cutout in the selected shape to fit another shape |
| <img src="toolbar-icons/Part_JoinEmbed.png" width="11" height="11" alt="Embed Shapes"> | <a id="button-part_joinembed"></a>Embed Shapes | `Part_JoinEmbed` | Fuses one shape into another, taking care to preserve voids |
| <img src="toolbar-icons/Part_LinkArrays.png" width="11" height="11" alt="Circular Link Array"> | <a id="button-part_linkarrays"></a>Circular Link Array | `Part_LinkArrays` | Creates a concentric circular array of linked objects |
| <img src="toolbar-icons/Part_LinkArrays_1.png" width="11" height="11" alt="Linear Link Array"> | â†³ Linear Link Array | `Part_LinkArrays` | Creates a linear array of linked objects |
| <img src="toolbar-icons/Part_LinkArrays_2.png" width="11" height="11" alt="Path Link Array"> | â†³ Path Link Array | `Part_LinkArrays` | Creates an array of linked objects along a path |
| <img src="toolbar-icons/Part_LinkArrays_3.png" width="11" height="11" alt="Point Link Array"> | â†³ Point Link Array | `Part_LinkArrays` | Creates an array of linked objects at each point of a sketch or shape |
| <img src="toolbar-icons/Part_LinkArrays_4.png" width="11" height="11" alt="Polar Link Array"> | â†³ Polar Link Array | `Part_LinkArrays` | Creates a polar array of linked objects |
| <img src="toolbar-icons/Part_Loft.png" width="11" height="11" alt="Loft"> | <a id="button-part_loft"></a>Loft | `Part_Loft` | Lofts the selected profiles |
| <img src="toolbar-icons/Part_MakeFace.png" width="11" height="11" alt="Face From Wires"> | <a id="button-part_makeface"></a>Face From Wires | `Part_MakeFace` | Creates a face from the selected wires (e.g. from a sketch) |
| <img src="toolbar-icons/Part_Mirror.png" width="11" height="11" alt="Mirror"> | <a id="button-part_mirror"></a>Mirror | `Part_Mirror` | Mirrors the selected shape |
| <img src="toolbar-icons/Part_Offset.png" width="11" height="11" alt="3D Offset"> | <a id="button-part_offset"></a>3D Offset | `Part_Offset` | Offsets shapes in 3D |
| <img src="toolbar-icons/Part_Offset2D.png" width="11" height="11" alt="2D Offset"> | <a id="button-part_offset2d"></a>2D Offset | `Part_Offset2D` | Offsets planar shapes in 2D |
| <img src="toolbar-icons/Part_Primitives.png" width="11" height="11" alt="Primitive"> | <a id="button-part_primitives"></a>Primitive | `Part_Primitives` | Creates solid geometric primitives parametrically |
| <img src="toolbar-icons/Part_ProjectionOnSurface.png" width="11" height="11" alt="Project on Surface"> | <a id="button-part_projectiononsurface"></a>Project on Surface | `Part_ProjectionOnSurface` | Projects edges, wires, or faces of one shape onto a face of another shape. The camera view determines the direction of the projection. |
| <img src="toolbar-icons/Part_Revolve.png" width="11" height="11" alt="Revolve"> | <a id="button-part_revolve"></a>Revolve | `Part_Revolve` | Revolves the selected shape |
| <img src="toolbar-icons/Part_RuledSurface.png" width="11" height="11" alt="Ruled Surface"> | <a id="button-part_ruledsurface"></a>Ruled Surface | `Part_RuledSurface` | Creates a ruled surface between 2 selected wires |
| <img src="toolbar-icons/Part_Scale.png" width="11" height="11" alt="Scale"> | <a id="button-part_scale"></a>Scale | `Part_Scale` | Scales the selected shape |
| <img src="toolbar-icons/Part_Section.png" width="11" height="11" alt="Section"> | <a id="button-part_section"></a>Section | `Part_Section` | Sections 2 selected shapes |
| <img src="toolbar-icons/Part_SelectFilter.png" width="11" height="11" alt="Vertex Selection"> | <a id="button-part_selectfilter"></a>Vertex Selection | `Part_SelectFilter` | Only allows the selection of vertices |
| <img src="toolbar-icons/Part_SelectFilter_1.png" width="11" height="11" alt="Edge Selection"> | â†³ Edge Selection | `Part_SelectFilter` | Only allows the selection of edges |
| <img src="toolbar-icons/Part_SelectFilter_2.png" width="11" height="11" alt="Face Selection"> | â†³ Face Selection | `Part_SelectFilter` | Only allows the selection of faces |
| <img src="toolbar-icons/Part_SelectFilter_3.png" width="11" height="11" alt="No Selection Filters"> | â†³ No Selection Filters | `Part_SelectFilter` | Clears all selection filters |
| <img src="toolbar-icons/Part_Slice.png" width="11" height="11" alt="Slice to Compound"> | <a id="button-part_slice"></a>Slice to Compound | `Part_Slice` | Slices the selected object by using other objects as cutting tools and storing the results in one compound |
| <img src="toolbar-icons/Part_SliceApart.png" width="11" height="11" alt="Slice Apart"> | <a id="button-part_sliceapart"></a>Slice Apart | `Part_SliceApart` | Slices the selected object by other objects, and splits it apart, creating a compound filter for each slide |
| <img src="toolbar-icons/Part_Sphere.png" width="11" height="11" alt="Sphere"> | <a id="button-part_sphere"></a>Sphere | `Part_Sphere` | Creates a solid sphere |
| <img src="toolbar-icons/Part_Sweep.png" width="11" height="11" alt="Sweep"> | <a id="button-part_sweep"></a>Sweep | `Part_Sweep` | Sweeps profiles along a wire |
| <img src="toolbar-icons/Part_Thickness.png" width="11" height="11" alt="Thickness"> | <a id="button-part_thickness"></a>Thickness | `Part_Thickness` | Removes the selected faces and offsets the remaining shape outward to add thickness |
| <img src="toolbar-icons/Part_Torus.png" width="11" height="11" alt="Torus"> | <a id="button-part_torus"></a>Torus | `Part_Torus` | Creates a solid torus |
| <img src="toolbar-icons/Part_TrimBody.png" width="11" height="11" alt="Trim Body"> | <a id="button-part_trimbody"></a>Trim Body | `Part_TrimBody` | Trim a solid or sheet with a plane, face, or sheet and choose the side to keep |
| <img src="toolbar-icons/Part_Tube.png" width="11" height="11" alt="Tube"> | <a id="button-part_tube"></a>Tube | `Part_Tube` | Creates a tube |
| <img src="toolbar-icons/Part_XOR.png" width="11" height="11" alt="Boolean XOR"> | <a id="button-part_xor"></a>Boolean XOR | `Part_XOR` | Performs an 'exclusive OR' boolean operation with two or more selected objects, or with the shapes inside a compound. Overlapping volumes of the shapes will be removed. |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Convert.svg" width="11" height="11" alt="Convert to Points"> | <a id="button-points_convert"></a>Convert to Points | `Points_Convert` | Converts to points |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Export_Point_cloud.svg" width="11" height="11" alt="Export Pointsâ€¦"> | <a id="button-points_export"></a>Export Pointsâ€¦ | `Points_Export` | Exports a point cloud |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Import_Point_cloud.svg" width="11" height="11" alt="Import Pointsâ€¦"> | <a id="button-points_import"></a>Import Pointsâ€¦ | `Points_Import` | Imports a point cloud |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Merge.svg" width="11" height="11" alt="Merge Point Clouds"> | <a id="button-points_merge"></a>Merge Point Clouds | `Points_Merge` | Merges several point clouds into one |
| <img src="../../../src/Gui/Icons/PolygonPick.svg" width="11" height="11" alt="Cut Point Cloud"> | <a id="button-points_polycut"></a>Cut Point Cloud | `Points_PolyCut` | Cuts a point cloud with a selected polygon |
| <img src="../../../src/Mod/Points/Gui/Resources/icons/Points_Structure.svg" width="11" height="11" alt="Structured Point Cloud"> | <a id="button-points_structure"></a>Structured Point Cloud | `Points_Structure` | Converts points to a structured point cloud |
| <img src="../../../src/Mod/ReverseEngineering/Gui/Resources/icons/actions/FitSurface.svg" width="11" height="11" alt="Approximate B-Spline Surfaceâ€¦"> | <a id="button-reen_approxsurface"></a>Approximate B-Spline Surfaceâ€¦ | `Reen_ApproxSurface` | Approximates a B-spline surface |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_CreateRobot.svg" width="11" height="11" alt="Place Robot"> | <a id="button-robot_create"></a>Place Robot | `Robot_Create` | Places a robot in the scene |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_CreateTrajectory.svg" width="11" height="11" alt="Trajectory"> | <a id="button-robot_createtrajectory"></a>Trajectory | `Robot_CreateTrajectory` | Creates a new empty trajectory |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_Edge2Trac.svg" width="11" height="11" alt="Edge to Trajectory"> | <a id="button-robot_edge2trac"></a>Edge to Trajectory | `Robot_Edge2Trac` | Generates a trajectory from the selected edges |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_InsertWaypoint.svg" width="11" height="11" alt="Insert in Trajectory"> | <a id="button-robot_insertwaypoint"></a>Insert in Trajectory | `Robot_InsertWaypoint` | Inserts the robot tool location into the trajectory |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_InsertWaypointPre.svg" width="11" height="11" alt="Insert in Trajectory"> | <a id="button-robot_insertwaypointpreselect"></a>Insert in Trajectory | `Robot_InsertWaypointPreselect` | Inserts the preselection position into the trajectory (W) |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_RestoreHomePos.svg" width="11" height="11" alt="Move to Home"> | <a id="button-robot_restorehomepos"></a>Move to Home | `Robot_RestoreHomePos` | Moves to the home position |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_SetHomePos.svg" width="11" height="11" alt="Set Home Position"> | <a id="button-robot_sethomepos"></a>Set Home Position | `Robot_SetHomePos` | Sets the home position |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_Simulate.svg" width="11" height="11" alt="Simulate Trajectory"> | <a id="button-robot_simulate"></a>Simulate Trajectory | `Robot_Simulate` | Simulates robot movement along a selected trajectory |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_TrajectoryCompound.svg" width="11" height="11" alt="Trajectory Compound"> | <a id="button-robot_trajectorycompound"></a>Trajectory Compound | `Robot_TrajectoryCompound` | Groups and connects multiple trajectories into one |
| <img src="../../../src/Mod/Robot/Gui/Resources/icons/Robot_TrajectoryDressUp.svg" width="11" height="11" alt="Dress-Up Trajectory"> | <a id="button-robot_trajectorydressup"></a>Dress-Up Trajectory | `Robot_TrajectoryDressUp` | Creates a dress-up object that overrides aspects of a trajectory |
| <img src="toolbar-icons/Sketcher_ArcOverlay.png" width="11" height="11" alt="Toggle Circular Helper for Arcs"> | <a id="button-sketcher_arcoverlay"></a>Toggle Circular Helper for Arcs | `Sketcher_ArcOverlay` | Toggles the visibility of the circular helpers for all arcs |
| <img src="toolbar-icons/Sketcher_BSplineConvertToNURBS.png" width="11" height="11" alt="Geometry to B-Spline"> | <a id="button-sketcher_bsplineconverttonurbs"></a>Geometry to B-Spline | `Sketcher_BSplineConvertToNURBS` | Converts the selected geometry to B-splines |
| <img src="toolbar-icons/Sketcher_BSplineDecreaseDegree.png" width="11" height="11" alt="Decrease B-Spline Degree"> | <a id="button-sketcher_bsplinedecreasedegree"></a>Decrease B-Spline Degree | `Sketcher_BSplineDecreaseDegree` | Decreases the degree of the B-spline |
| <img src="toolbar-icons/Sketcher_BSplineIncreaseDegree.png" width="11" height="11" alt="Increase B-Spline Degree"> | <a id="button-sketcher_bsplineincreasedegree"></a>Increase B-Spline Degree | `Sketcher_BSplineIncreaseDegree` | Increases the degree of the B-spline |
| <img src="toolbar-icons/Sketcher_BSplineInsertKnot.png" width="11" height="11" alt="Insert Knot"> | <a id="button-sketcher_bsplineinsertknot"></a>Insert Knot | `Sketcher_BSplineInsertKnot` | Inserts a knot at a given parameter. If a knot already exists at that parameter, its multiplicity is increased by 1. |
| <img src="toolbar-icons/Sketcher_CarbonCopy.png" width="11" height="11" alt="Carbon Copy"> | <a id="button-sketcher_carboncopy"></a>Carbon Copy | `Sketcher_CarbonCopy` | Copies the geometry of another sketch |
| <img src="toolbar-icons/Sketcher_CompBSplineShowHideGeometryInformation.png" width="11" height="11" alt="Toggle B-Spline Degree"> | <a id="button-sketcher_compbsplineshowhidegeometryinformation"></a>Toggle B-Spline Degree | `Sketcher_CompBSplineShowHideGeometryInformation` | Toggles the visibility of the degree for all B-splines |
| <img src="toolbar-icons/Sketcher_CompBSplineShowHideGeometryInformation_1.png" width="11" height="11" alt="Toggle B-Spline Control Polygon"> | â†³ Toggle B-Spline Control Polygon | `Sketcher_CompBSplineShowHideGeometryInformation` | Toggles the visibility of the control polygons for all B-splines |
| <img src="toolbar-icons/Sketcher_CompBSplineShowHideGeometryInformation_2.png" width="11" height="11" alt="Toggle B-Spline Curvature Comb"> | â†³ Toggle B-Spline Curvature Comb | `Sketcher_CompBSplineShowHideGeometryInformation` | Toggles the visibility of the curvature comb for all B-splines |
| <img src="toolbar-icons/Sketcher_CompBSplineShowHideGeometryInformation_3.png" width="11" height="11" alt="Toggle B-Spline Knot Multiplicity"> | â†³ Toggle B-Spline Knot Multiplicity | `Sketcher_CompBSplineShowHideGeometryInformation` | Toggles the visibility of the knot multiplicity for all B-splines |
| <img src="toolbar-icons/Sketcher_CompBSplineShowHideGeometryInformation_4.png" width="11" height="11" alt="Toggle B-Spline Control Point Weight"> | â†³ Toggle B-Spline Control Point Weight | `Sketcher_CompBSplineShowHideGeometryInformation` | Toggles the visibility of the control point weight for all B-splines |
| <img src="toolbar-icons/Sketcher_CompConstrainRadDia.png" width="11" height="11" alt="Constrain radius"> | <a id="button-sketcher_compconstrainraddia"></a>Constrain radius | `Sketcher_CompConstrainRadDia` | Fix the radius of an arc or a circle |
| <img src="toolbar-icons/Sketcher_CompConstrainRadDia_1.png" width="11" height="11" alt="Constrain diameter"> | â†³ Constrain diameter | `Sketcher_CompConstrainRadDia` | Fix the diameter of a circle or an arc |
| <img src="toolbar-icons/Sketcher_CompConstrainRadDia_2.png" width="11" height="11" alt="Constrain auto radius/diameter"> | â†³ Constrain auto radius/diameter | `Sketcher_CompConstrainRadDia` | Fix the radius/diameter of an arc or a circle |
| <img src="toolbar-icons/Sketcher_CompCreateArc.png" width="11" height="11" alt="Arc From Center"> | <a id="button-sketcher_compcreatearc"></a>Arc From Center | `Sketcher_CompCreateArc` | Creates an arc defined by a center point and an end point |
| <img src="toolbar-icons/Sketcher_CompCreateArc_1.png" width="11" height="11" alt="Arc From 3 Points"> | â†³ Arc From 3 Points | `Sketcher_CompCreateArc` | Creates an arc defined by 2 end points and 1 point on the arc |
| <img src="toolbar-icons/Sketcher_CompCreateArc_2.png" width="11" height="11" alt="Elliptical Arc"> | â†³ Elliptical Arc | `Sketcher_CompCreateArc` | Creates an elliptical arc |
| <img src="toolbar-icons/Sketcher_CompCreateArc_3.png" width="11" height="11" alt="Hyperbolic Arc"> | â†³ Hyperbolic Arc | `Sketcher_CompCreateArc` | Creates a hyperbolic arc |
| <img src="toolbar-icons/Sketcher_CompCreateArc_4.png" width="11" height="11" alt="Parabolic Arc"> | â†³ Parabolic Arc | `Sketcher_CompCreateArc` | Creates a parabolic arc |
| <img src="toolbar-icons/Sketcher_CompCreateBSpline.png" width="11" height="11" alt="B-Spline"> | <a id="button-sketcher_compcreatebspline"></a>B-Spline | `Sketcher_CompCreateBSpline` | Creates a B-spline curve defined by control points |
| <img src="toolbar-icons/Sketcher_CompCreateBSpline_1.png" width="11" height="11" alt="Periodic B-Spline"> | â†³ Periodic B-Spline | `Sketcher_CompCreateBSpline` | Creates a periodic B-spline curve defined by control points |
| <img src="toolbar-icons/Sketcher_CompCreateBSpline_2.png" width="11" height="11" alt="B-Spline From Knots"> | â†³ B-Spline From Knots | `Sketcher_CompCreateBSpline` | Creates a B-spline from knots, i.e. from interpolation |
| <img src="toolbar-icons/Sketcher_CompCreateBSpline_3.png" width="11" height="11" alt="Periodic B-Spline From Knots"> | â†³ Periodic B-Spline From Knots | `Sketcher_CompCreateBSpline` | Creates a periodic B-spline defined by knots using interpolation |
| <img src="toolbar-icons/Sketcher_CompCreateConic.png" width="11" height="11" alt="Circle From Center"> | <a id="button-sketcher_compcreateconic"></a>Circle From Center | `Sketcher_CompCreateConic` | Creates a circle from a center and rim point |
| <img src="toolbar-icons/Sketcher_CompCreateConic_1.png" width="11" height="11" alt="Circle From 3 Points"> | â†³ Circle From 3 Points | `Sketcher_CompCreateConic` | Creates a circle from 3 perimeter points |
| <img src="toolbar-icons/Sketcher_CompCreateConic_2.png" width="11" height="11" alt="Ellipse From Center"> | â†³ Ellipse From Center | `Sketcher_CompCreateConic` | Creates an ellipse from a center and rim point |
| <img src="toolbar-icons/Sketcher_CompCreateConic_3.png" width="11" height="11" alt="Ellipse From 3 Points"> | â†³ Ellipse From 3 Points | `Sketcher_CompCreateConic` | Creates an ellipse from 3 points on its perimeter |
| <img src="toolbar-icons/Sketcher_CompCreateFillets.png" width="11" height="11" alt="Fillet"> | <a id="button-sketcher_compcreatefillets"></a>Fillet | `Sketcher_CompCreateFillets` | Creates a fillet between 2 selected curves or at coincident points |
| <img src="toolbar-icons/Sketcher_CompCreateFillets_1.png" width="11" height="11" alt="Chamfer"> | â†³ Chamfer | `Sketcher_CompCreateFillets` | Creates a chamfer between 2 selected curves or at coincident points |
| <img src="toolbar-icons/Sketcher_CompCreateRectangles.png" width="11" height="11" alt="Rectangle"> | <a id="button-sketcher_compcreaterectangles"></a>Rectangle | `Sketcher_CompCreateRectangles` | Creates a rectangle from 2 corner points |
| <img src="toolbar-icons/Sketcher_CompCreateRectangles_1.png" width="11" height="11" alt="Centered Rectangle"> | â†³ Centered Rectangle | `Sketcher_CompCreateRectangles` | Creates a centered rectangle from a center and a corner point |
| <img src="toolbar-icons/Sketcher_CompCreateRectangles_2.png" width="11" height="11" alt="Rounded Rectangle"> | â†³ Rounded Rectangle | `Sketcher_CompCreateRectangles` | Creates a rounded rectangle from 2 corner points |
| <img src="toolbar-icons/Sketcher_CompCreateRegularPolygon.png" width="11" height="11" alt="Triangle"> | <a id="button-sketcher_compcreateregularpolygon"></a>Triangle | `Sketcher_CompCreateRegularPolygon` | Creates an equilateral triangle from a center and corner point |
| <img src="toolbar-icons/Sketcher_CompCreateRegularPolygon_1.png" width="11" height="11" alt="Square"> | â†³ Square | `Sketcher_CompCreateRegularPolygon` | Creates a square from a center and corner point |
| <img src="toolbar-icons/Sketcher_CompCreateRegularPolygon_2.png" width="11" height="11" alt="Pentagon"> | â†³ Pentagon | `Sketcher_CompCreateRegularPolygon` | Creates a pentagon from a center and corner point |
| <img src="toolbar-icons/Sketcher_CompCreateRegularPolygon_3.png" width="11" height="11" alt="Hexagon"> | â†³ Hexagon | `Sketcher_CompCreateRegularPolygon` | Creates a hexagon from a center and corner point |
| <img src="toolbar-icons/Sketcher_CompCreateRegularPolygon_4.png" width="11" height="11" alt="Heptagon"> | â†³ Heptagon | `Sketcher_CompCreateRegularPolygon` | Creates a heptagon from a center and corner point |
| <img src="toolbar-icons/Sketcher_CompCreateRegularPolygon_5.png" width="11" height="11" alt="Octagon"> | â†³ Octagon | `Sketcher_CompCreateRegularPolygon` | Creates an octagon from a center and corner point |
| <img src="toolbar-icons/Sketcher_CompCreateRegularPolygon_6.png" width="11" height="11" alt="Polygon"> | â†³ Polygon | `Sketcher_CompCreateRegularPolygon` | Creates a regular polygon from a center and corner point |
| <img src="toolbar-icons/Sketcher_CompCurveEdition.png" width="11" height="11" alt="Trim Edge"> | <a id="button-sketcher_compcurveedition"></a>Trim Edge | `Sketcher_CompCurveEdition` | Trims an edge with respect to the selected position |
| <img src="toolbar-icons/Sketcher_CompCurveEdition_1.png" width="11" height="11" alt="Split Edge"> | â†³ Split Edge | `Sketcher_CompCurveEdition` | Splits an edge into 2 segments while preserving constraints |
| <img src="toolbar-icons/Sketcher_CompCurveEdition_2.png" width="11" height="11" alt="Extend Edge"> | â†³ Extend Edge | `Sketcher_CompCurveEdition` | Extends an edge with respect to the selected position |
| <img src="toolbar-icons/Sketcher_CompDimensionTools.png" width="11" height="11" alt="Dimension"> | <a id="button-sketcher_compdimensiontools"></a>Dimension | `Sketcher_CompDimensionTools` | Constrains contextually based on the selection. The type can be changed with the M key. |
| <img src="toolbar-icons/Sketcher_CompDimensionTools_2.png" width="11" height="11" alt="Horizontal Dimension"> | â†³ Horizontal Dimension | `Sketcher_CompDimensionTools` | Constrains the horizontal distance between two points, or from a point to the origin if only one is selected |
| <img src="toolbar-icons/Sketcher_CompDimensionTools_3.png" width="11" height="11" alt="Vertical Dimension"> | â†³ Vertical Dimension | `Sketcher_CompDimensionTools` | Constrains the vertical distance between two points, or from a point to the origin if only one is selected |
| <img src="toolbar-icons/Sketcher_CompDimensionTools_4.png" width="11" height="11" alt="Distance Dimension"> | â†³ Distance Dimension | `Sketcher_CompDimensionTools` | Constrains the vertical distance between two points, or from a point to the origin if one is selected |
| <img src="toolbar-icons/Sketcher_CompDimensionTools_5.png" width="11" height="11" alt="Radius/Diameter Dimension"> | â†³ Radius/Diameter Dimension | `Sketcher_CompDimensionTools` | Constrains the radius of the selected arc or the diameter of the selected circle |
| <img src="toolbar-icons/Sketcher_CompDimensionTools_6.png" width="11" height="11" alt="Radius Dimension"> | â†³ Radius Dimension | `Sketcher_CompDimensionTools` | Constrains the radius of the selected circle or arc |
| <img src="toolbar-icons/Sketcher_CompDimensionTools_7.png" width="11" height="11" alt="Diameter Dimension"> | â†³ Diameter Dimension | `Sketcher_CompDimensionTools` | Constrains the diameter of the selected circle or arc |
| <img src="toolbar-icons/Sketcher_CompDimensionTools_8.png" width="11" height="11" alt="Angle Dimension"> | â†³ Angle Dimension | `Sketcher_CompDimensionTools` | Constrains the angle between two straight lines or between one line and the X-axis of the sketch if only one is selected |
| <img src="toolbar-icons/Sketcher_CompDimensionTools_9.png" width="11" height="11" alt="Lock Position"> | â†³ Lock Position | `Sketcher_CompDimensionTools` | Constrains the selected vertices by adding horizontal and vertical distance constraints |
| <img src="toolbar-icons/Sketcher_CompExternal.png" width="11" height="11" alt="External Projection"> | <a id="button-sketcher_compexternal"></a>External Projection | `Sketcher_CompExternal` | Creates the projection of external geometry in the sketch plane |
| <img src="toolbar-icons/Sketcher_CompExternal_1.png" width="11" height="11" alt="External Intersection"> | â†³ External Intersection | `Sketcher_CompExternal` | Creates the intersection of external geometry with the sketch plane |
| <img src="toolbar-icons/Sketcher_CompHorVer.png" width="11" height="11" alt="Horizontal Constraint"> | <a id="button-sketcher_comphorver"></a>Horizontal Constraint | `Sketcher_CompHorVer` | Constrains the selected elements horizontally |
| <img src="toolbar-icons/Sketcher_CompHorVer_1.png" width="11" height="11" alt="Vertical Constraint"> | â†³ Vertical Constraint | `Sketcher_CompHorVer` | Constrains the selected elements vertically |
| <img src="toolbar-icons/Sketcher_CompLine.png" width="11" height="11" alt="Polyline"> | <a id="button-sketcher_compline"></a>Polyline | `Sketcher_CompLine` | Creates a polyline in the sketch. M key cycles through segment modes. |
| <img src="toolbar-icons/Sketcher_CompLine_1.png" width="11" height="11" alt="Line"> | â†³ Line | `Sketcher_CompLine` | Creates a line |
| <img src="toolbar-icons/Sketcher_CompModifyKnotMultiplicity.png" width="11" height="11" alt="Increase knot multiplicity"> | <a id="button-sketcher_compmodifyknotmultiplicity"></a>Increase knot multiplicity | `Sketcher_CompModifyKnotMultiplicity` | Increases the multiplicity of the selected knot of a B-spline |
| <img src="toolbar-icons/Sketcher_CompModifyKnotMultiplicity_1.png" width="11" height="11" alt="Decrease knot multiplicity"> | â†³ Decrease knot multiplicity | `Sketcher_CompModifyKnotMultiplicity` | Decreases the multiplicity of the selected knot of a B-spline |
| <img src="toolbar-icons/Sketcher_CompSlot.png" width="11" height="11" alt="Slot"> | <a id="button-sketcher_compslot"></a>Slot | `Sketcher_CompSlot` | Creates a slot |
| <img src="toolbar-icons/Sketcher_CompSlot_1.png" width="11" height="11" alt="Arc Slot"> | â†³ Arc Slot | `Sketcher_CompSlot` | Creates an arc slot |
| <img src="toolbar-icons/Sketcher_CompToggleConstraints.png" width="11" height="11" alt="Toggle Driving/Reference Constraints"> | <a id="button-sketcher_comptoggleconstraints"></a>Toggle Driving/Reference Constraints | `Sketcher_CompToggleConstraints` | Toggles between driving and reference mode of the selected constraints and commands |
| <img src="toolbar-icons/Sketcher_CompToggleConstraints_1.png" width="11" height="11" alt="Toggle Constraints"> | â†³ Toggle Constraints | `Sketcher_CompToggleConstraints` | Toggles the state of the selected constraints |
| <img src="toolbar-icons/Sketcher_ConstrainAngle.png" width="11" height="11" alt="Angle Dimension"> | <a id="button-sketcher_constrainangle"></a>Angle Dimension | `Sketcher_ConstrainAngle` | Constrains the angle between two straight lines or between one line and the X-axis of the sketch if only one is selected |
| <img src="toolbar-icons/Sketcher_ConstrainBlock.png" width="11" height="11" alt="Block Constraint"> | <a id="button-sketcher_constrainblock"></a>Block Constraint | `Sketcher_ConstrainBlock` | Constrains the selected edges as fixed |
| <img src="toolbar-icons/Sketcher_ConstrainCoincidentUnified.png" width="11" height="11" alt="Coincident Constraint"> | <a id="button-sketcher_constraincoincidentunified"></a>Coincident Constraint | `Sketcher_ConstrainCoincidentUnified` | Constrains the selected elements to be coincident |
| <img src="toolbar-icons/Sketcher_ConstrainDiameter.png" width="11" height="11" alt="Diameter Dimension"> | <a id="button-sketcher_constraindiameter"></a>Diameter Dimension | `Sketcher_ConstrainDiameter` | Constrains the diameter of the selected circle or arc |
| <img src="toolbar-icons/Sketcher_ConstrainDistance.png" width="11" height="11" alt="Distance Dimension"> | <a id="button-sketcher_constraindistance"></a>Distance Dimension | `Sketcher_ConstrainDistance` | Constrains the vertical distance between two points, or from a point to the origin if one is selected |
| <img src="toolbar-icons/Sketcher_ConstrainDistanceX.png" width="11" height="11" alt="Horizontal Dimension"> | <a id="button-sketcher_constraindistancex"></a>Horizontal Dimension | `Sketcher_ConstrainDistanceX` | Constrains the horizontal distance between two points, or from a point to the origin if only one is selected |
| <img src="toolbar-icons/Sketcher_ConstrainDistanceY.png" width="11" height="11" alt="Vertical Dimension"> | <a id="button-sketcher_constraindistancey"></a>Vertical Dimension | `Sketcher_ConstrainDistanceY` | Constrains the vertical distance between two points, or from a point to the origin if only one is selected |
| <img src="toolbar-icons/Sketcher_ConstrainEqual.png" width="11" height="11" alt="Equal Constraint"> | <a id="button-sketcher_constrainequal"></a>Equal Constraint | `Sketcher_ConstrainEqual` | Constrains the selected edges or circles to be equal |
| <img src="toolbar-icons/Sketcher_ConstrainGroup.png" width="11" height="11" alt="Group Constraint (Development preview)"> | <a id="button-sketcher_constraingroup"></a>Group Constraint (Development preview) | `Sketcher_ConstrainGroup` | Constrains the selected geometries together as a single entity.The position and size of the grouped geometries can be defined by constraining the construction line that is generated.Constraints applied to grouped edges are ignored as long as the Group constraint is here. |
| <img src="toolbar-icons/Sketcher_ConstrainLock.png" width="11" height="11" alt="Lock Position"> | <a id="button-sketcher_constrainlock"></a>Lock Position | `Sketcher_ConstrainLock` | Constrains the selected vertices by adding horizontal and vertical distance constraints |
| <img src="toolbar-icons/Sketcher_ConstrainParallel.png" width="11" height="11" alt="Parallel Constraint"> | <a id="button-sketcher_constrainparallel"></a>Parallel Constraint | `Sketcher_ConstrainParallel` | Constrains the selected lines to be parallel |
| <img src="toolbar-icons/Sketcher_ConstrainPerpendicular.png" width="11" height="11" alt="Perpendicular Constraint"> | <a id="button-sketcher_constrainperpendicular"></a>Perpendicular Constraint | `Sketcher_ConstrainPerpendicular` | Constrains the selected lines to be perpendicular |
| <img src="toolbar-icons/Sketcher_ConstrainRadiam.png" width="11" height="11" alt="Radius/Diameter Dimension"> | <a id="button-sketcher_constrainradiam"></a>Radius/Diameter Dimension | `Sketcher_ConstrainRadiam` | Constrains the radius of the selected arc or the diameter of the selected circle |
| <img src="toolbar-icons/Sketcher_ConstrainRadius.png" width="11" height="11" alt="Radius Dimension"> | <a id="button-sketcher_constrainradius"></a>Radius Dimension | `Sketcher_ConstrainRadius` | Constrains the radius of the selected circle or arc |
| <img src="toolbar-icons/Sketcher_ConstrainSnellsLaw.png" width="11" height="11" alt="Refraction Constraint"> | <a id="button-sketcher_constrainsnellslaw"></a>Refraction Constraint | `Sketcher_ConstrainSnellsLaw` | Constrains the selected elements based on the refraction law (Snell's Law) |
| <img src="toolbar-icons/Sketcher_ConstrainSymmetric.png" width="11" height="11" alt="Symmetric Constraint"> | <a id="button-sketcher_constrainsymmetric"></a>Symmetric Constraint | `Sketcher_ConstrainSymmetric` | Constrains the selected elements to be symmetric |
| <img src="toolbar-icons/Sketcher_ConstrainTangent.png" width="11" height="11" alt="Tangent/Collinear Constraint"> | <a id="button-sketcher_constraintangent"></a>Tangent/Collinear Constraint | `Sketcher_ConstrainTangent` | Constrains the selected elements to be tangent or collinear |
| <img src="toolbar-icons/Sketcher_CreatePoint.png" width="11" height="11" alt="Point"> | <a id="button-sketcher_createpoint"></a>Point | `Sketcher_CreatePoint` | Creates a point |
| <img src="toolbar-icons/Sketcher_CreateText.png" width="11" height="11" alt="Text (Experimental)"> | <a id="button-sketcher_createtext"></a>Text (Experimental) | `Sketcher_CreateText` | Creates text geometries controlled by a Text constraint. To Edit: Double-click the Text constraint to change the text content and font. To Position/Size: Apply constraints to the group's construction line. Note: While the Text constraint is active, any constraints applied directly to the text geometries will be ignored. |
| <img src="toolbar-icons/Sketcher_Dimension.png" width="11" height="11" alt="Dimension"> | <a id="button-sketcher_dimension"></a>Dimension | `Sketcher_Dimension` | Constrains contextually based on the selection. The type can be changed with the M key. |
| <img src="toolbar-icons/Sketcher_EditSketch.png" width="11" height="11" alt="Edit Sketch"> | <a id="button-sketcher_editsketch"></a>Edit Sketch | `Sketcher_EditSketch` | Opens the selected sketch for editing |
| <img src="toolbar-icons/Sketcher_JoinCurves.png" width="11" height="11" alt="Join Curves"> | <a id="button-sketcher_joincurves"></a>Join Curves | `Sketcher_JoinCurves` | Joins 2 curves at selected end points |
| <img src="toolbar-icons/Sketcher_LeaveSketch.png" width="11" height="11" alt="Leave Sketch"> | <a id="button-sketcher_leavesketch"></a>Leave Sketch | `Sketcher_LeaveSketch` | Finishes editing the active sketch. Press Escape to exit. |
| <img src="toolbar-icons/Sketcher_MapSketch.png" width="11" height="11" alt="Attach Sketch"> | <a id="button-sketcher_mapsketch"></a>Attach Sketch | `Sketcher_MapSketch` | Attaches a sketch to the selected geometry element |
| <img src="toolbar-icons/Sketcher_MergeSketches.png" width="11" height="11" alt="Merge Sketches"> | <a id="button-sketcher_mergesketches"></a>Merge Sketches | `Sketcher_MergeSketches` | Creates a new sketch by merging at least 2 selected sketches |
| <img src="toolbar-icons/Sketcher_MirrorSketch.png" width="11" height="11" alt="Mirror Sketch"> | <a id="button-sketcher_mirrorsketch"></a>Mirror Sketch | `Sketcher_MirrorSketch` | Creates a new mirrored sketch for each selected sketch by using the X or Y axes, or the origin point, as mirroring reference |
| <img src="toolbar-icons/Sketcher_NewSketch.png" width="11" height="11" alt="New Sketch"> | <a id="button-sketcher_newsketch"></a>New Sketch | `Sketcher_NewSketch` | Creates a new sketch |
| <img src="toolbar-icons/Sketcher_Offset.png" width="11" height="11" alt="Offset"> | <a id="button-sketcher_offset"></a>Offset | `Sketcher_Offset` | Adds an equidistant closed contour around selected geometry: positive values offset outward, negative values inward |
| <img src="toolbar-icons/Sketcher_RemoveAxesAlignment.png" width="11" height="11" alt="Remove Axes Alignment"> | <a id="button-sketcher_removeaxesalignment"></a>Remove Axes Alignment | `Sketcher_RemoveAxesAlignment` | Modifies the constraints to remove axes alignment while trying to preserve the constraint relationship of the selection |
| <img src="toolbar-icons/Sketcher_ReorientSketch.png" width="11" height="11" alt="Reorient Sketch"> | <a id="button-sketcher_reorientsketch"></a>Reorient Sketch | `Sketcher_ReorientSketch` | Places the selected sketch on one of the global coordinate planes. This will clear the AttachmentSupport property. |
| <img src="toolbar-icons/Sketcher_RestoreInternalAlignmentGeometry.png" width="11" height="11" alt="Toggle Internal Geometry"> | <a id="button-sketcher_restoreinternalalignmentgeometry"></a>Toggle Internal Geometry | `Sketcher_RestoreInternalAlignmentGeometry` | Toggles the visibility of all internal geometry |
| <img src="toolbar-icons/Sketcher_Rotate.png" width="11" height="11" alt="Rotate / Polar Transform"> | <a id="button-sketcher_rotate"></a>Rotate / Polar Transform | `Sketcher_Rotate` | Rotates the selected geometry by creating 'n' total elements, enabling circular pattern creation |
| <img src="toolbar-icons/Sketcher_Scale.png" width="11" height="11" alt="Scale"> | <a id="button-sketcher_scale"></a>Scale | `Sketcher_Scale` | Scales the selected geometries |
| <img src="toolbar-icons/Sketcher_SelectConstraints.png" width="11" height="11" alt="Select Associated Constraints"> | <a id="button-sketcher_selectconstraints"></a>Select Associated Constraints | `Sketcher_SelectConstraints` | Selects the constraints associated with the selected geometrical elements |
| <img src="toolbar-icons/Sketcher_SelectElementsAssociatedWithConstraints.png" width="11" height="11" alt="Select Associated Geometry"> | <a id="button-sketcher_selectelementsassociatedwithconstraints"></a>Select Associated Geometry | `Sketcher_SelectElementsAssociatedWithConstraints` | Selects the geometrical elements associated with the selected constraints |
| <img src="toolbar-icons/Sketcher_SwitchVirtualSpace.png" width="11" height="11" alt="Switch Virtual Space"> | <a id="button-sketcher_switchvirtualspace"></a>Switch Virtual Space | `Sketcher_SwitchVirtualSpace` | Switches the selected constraints or the view to the other virtual space |
| <img src="toolbar-icons/Sketcher_Symmetry.png" width="11" height="11" alt="Mirror"> | <a id="button-sketcher_symmetry"></a>Mirror | `Sketcher_Symmetry` | Creates a mirrored copy of the selected geometry |
| <img src="toolbar-icons/Sketcher_ToggleConstruction.png" width="11" height="11" alt="Toggle Construction Geometry"> | <a id="button-sketcher_toggleconstruction"></a>Toggle Construction Geometry | `Sketcher_ToggleConstruction` | Toggles between defining geometry and construction geometry modes |
| <img src="toolbar-icons/Sketcher_Translate.png" width="11" height="11" alt="Move / Array Transform"> | <a id="button-sketcher_translate"></a>Move / Array Transform | `Sketcher_Translate` | Translates the selected geometries and enables the creation of 'i' * 'j' total elements |
| <img src="toolbar-icons/Sketcher_ValidateSketch.png" width="11" height="11" alt="Validate Sketch"> | <a id="button-sketcher_validatesketch"></a>Validate Sketch | `Sketcher_ValidateSketch` | Validates a sketch by checking for missing coincidences, invalid constraints, and degenerate geometry |
| <img src="toolbar-icons/Sketcher_ViewSection.png" width="11" height="11" alt="Toggle Section View"> | <a id="button-sketcher_viewsection"></a>Toggle Section View | `Sketcher_ViewSection` | Toggles between section view and full view |
| <img src="toolbar-icons/Sketcher_ViewSketch.png" width="11" height="11" alt="Align View to Sketch"> | <a id="button-sketcher_viewsketch"></a>Align View to Sketch | `Sketcher_ViewSketch` | Aligns the camera orientation perpendicular to the active sketch plane |
| <img src="toolbar-icons/Spreadsheet_AlignBottom.png" width="11" height="11" alt="Align Bottom"> | <a id="button-spreadsheet_alignbottom"></a>Align Bottom | `Spreadsheet_AlignBottom` | Aligns cell contents to the bottom |
| <img src="toolbar-icons/Spreadsheet_AlignCenter.png" width="11" height="11" alt="Align Horizontal Center"> | <a id="button-spreadsheet_aligncenter"></a>Align Horizontal Center | `Spreadsheet_AlignCenter` | Aligns cell contents to the horizontal center |
| <img src="toolbar-icons/Spreadsheet_AlignLeft.png" width="11" height="11" alt="Align Left"> | <a id="button-spreadsheet_alignleft"></a>Align Left | `Spreadsheet_AlignLeft` | Aligns cell contents to the left |
| <img src="toolbar-icons/Spreadsheet_AlignRight.png" width="11" height="11" alt="Align Right"> | <a id="button-spreadsheet_alignright"></a>Align Right | `Spreadsheet_AlignRight` | Aligns cell contents to the right |
| <img src="toolbar-icons/Spreadsheet_AlignTop.png" width="11" height="11" alt="Align Top"> | <a id="button-spreadsheet_aligntop"></a>Align Top | `Spreadsheet_AlignTop` | Aligns cell contents to the top |
| <img src="toolbar-icons/Spreadsheet_AlignVCenter.png" width="11" height="11" alt="Align Vertical Center"> | <a id="button-spreadsheet_alignvcenter"></a>Align Vertical Center | `Spreadsheet_AlignVCenter` | Aligns cell contents to the vertical center |
| <img src="toolbar-icons/Spreadsheet_CreateSheet.png" width="11" height="11" alt="New Spreadsheet"> | <a id="button-spreadsheet_createsheet"></a>New Spreadsheet | `Spreadsheet_CreateSheet` | Creates a new spreadsheet |
| <img src="toolbar-icons/Spreadsheet_Export.png" width="11" height="11" alt="Export Spreadsheet"> | <a id="button-spreadsheet_export"></a>Export Spreadsheet | `Spreadsheet_Export` | Exports the spreadsheet to a CSV file |
| <img src="toolbar-icons/Spreadsheet_Import.png" width="11" height="11" alt="Import Spreadsheet"> | <a id="button-spreadsheet_import"></a>Import Spreadsheet | `Spreadsheet_Import` | Imports a CSV file into a new spreadsheet |
| <img src="toolbar-icons/Spreadsheet_MergeCells.png" width="11" height="11" alt="Merge Cells"> | <a id="button-spreadsheet_mergecells"></a>Merge Cells | `Spreadsheet_MergeCells` | Merges the selected cells |
| <img src="toolbar-icons/Spreadsheet_SetAlias.png" width="11" height="11" alt="Set Alias"> | <a id="button-spreadsheet_setalias"></a>Set Alias | `Spreadsheet_SetAlias` | Sets an alias for the selected cell |
| <img src="toolbar-icons/Spreadsheet_SplitCell.png" width="11" height="11" alt="Split Cell"> | <a id="button-spreadsheet_splitcell"></a>Split Cell | `Spreadsheet_SplitCell` | Splits a previously merged cell |
| <img src="toolbar-icons/Spreadsheet_StyleBold.png" width="11" height="11" alt="Bold Text"> | <a id="button-spreadsheet_stylebold"></a>Bold Text | `Spreadsheet_StyleBold` | Sets the text in the selected cells bold |
| <img src="toolbar-icons/Spreadsheet_StyleItalic.png" width="11" height="11" alt="Italic Text"> | <a id="button-spreadsheet_styleitalic"></a>Italic Text | `Spreadsheet_StyleItalic` | Sets the text in the selected cells italic |
| <img src="toolbar-icons/Spreadsheet_StyleUnderline.png" width="11" height="11" alt="Underline Text"> | <a id="button-spreadsheet_styleunderline"></a>Underline Text | `Spreadsheet_StyleUnderline` | Underlines the text in the selected cells |
| <img src="toolbar-icons/Std_AlignToSelection.png" width="11" height="11" alt="Align to Selection"> | <a id="button-std_aligntoselection"></a>Align to Selection | `Std_AlignToSelection` | Aligns the camera view to the selected elements in the 3D view |
| <img src="../../../src/Gui/Icons/zoom-in.svg" width="11" height="11" alt="Command search..."> | <a id="button-std_commandsearch"></a>Command search... | `Std_CommandSearch` | Find commands by name, familiar alias or shortcut |
| <img src="toolbar-icons/Std_ComponentStructure.png" width="11" height="11" alt="Components"> | <a id="button-std_componentstructure"></a>Components | `Std_ComponentStructure` | Show Models, Part Tree and History |
| <img src="toolbar-icons/Std_Copy.png" width="11" height="11" alt="Copy"> | <a id="button-std_copy"></a>Copy | `Std_Copy` | Copies the selection to the clipboard |
| <img src="toolbar-icons/Std_Cut.png" width="11" height="11" alt="Cut"> | <a id="button-std_cut"></a>Cut | `Std_Cut` | Removes the selection and copies it to the clipboard |
| <img src="toolbar-icons/Std_Delete.png" width="11" height="11" alt="Delete"> | <a id="button-std_delete"></a>Delete | `Std_Delete` | Deletes the selected objects |
| <img src="toolbar-icons/Std_DlgMacroExecute.png" width="11" height="11" alt="Macros"> | <a id="button-std_dlgmacroexecute"></a>Macros | `Std_DlgMacroExecute` | Opens a dialog to execute a recorded macro |
| <img src="toolbar-icons/Std_DlgMacroExecuteDirect.png" width="11" height="11" alt="Execute Macro"> | <a id="button-std_dlgmacroexecutedirect"></a>Execute Macro | `Std_DlgMacroExecuteDirect` | Executes the macro in the editor |
| <img src="toolbar-icons/Std_DlgMacroRecord.png" width="11" height="11" alt="Record Macro"> | <a id="button-std_dlgmacrorecord"></a>Record Macro | `Std_DlgMacroRecord` | Opens a dialog to record a macro |
| <img src="toolbar-icons/Std_DlgPreferences.png" width="11" height="11" alt="Preferences"> | <a id="button-std_dlgpreferences"></a>Preferences | `Std_DlgPreferences` | Opens a dialog to edit the preferences |
| <img src="../../../src/Gui/Icons/Std_ToggleBottomPanels.svg" width="11" height="11" alt="Panels"> | <a id="button-std_dockviewmenu"></a>Panels | `Std_DockViewMenu` | Lists available dock panels |
| <img src="toolbar-icons/Std_DrawStyle.png" width="11" height="11" alt="As Is"> | <a id="button-std_drawstyle"></a>As Is | `Std_DrawStyle` | Normal mode |
| <img src="toolbar-icons/Std_DrawStyle_1.png" width="11" height="11" alt="Points"> | â†³ Points | `Std_DrawStyle` | Points mode |
| <img src="toolbar-icons/Std_DrawStyle_2.png" width="11" height="11" alt="Wireframe"> | â†³ Wireframe | `Std_DrawStyle` | Wireframe mode |
| <img src="toolbar-icons/Std_DrawStyle_3.png" width="11" height="11" alt="Hidden Line"> | â†³ Hidden Line | `Std_DrawStyle` | Hidden line mode |
| <img src="toolbar-icons/Std_DrawStyle_4.png" width="11" height="11" alt="No Shading"> | â†³ No Shading | `Std_DrawStyle` | No shading mode |
| <img src="toolbar-icons/Std_DrawStyle_5.png" width="11" height="11" alt="Shaded"> | â†³ Shaded | `Std_DrawStyle` | Shaded mode |
| <img src="toolbar-icons/Std_DrawStyle_6.png" width="11" height="11" alt="Flat Lines"> | â†³ Flat Lines | `Std_DrawStyle` | Flat lines mode |
| <img src="../../../src/Gui/Icons/view-select.svg" width="11" height="11" alt="Selection filtersâ€¦"> | <a id="button-std_entityselectionfilter"></a>Selection filtersâ€¦ | `Std_EntitySelectionFilter` | Restrict new picks to vertices, edges, faces or whole objects |
| <img src="toolbar-icons/Std_Export.png" width="11" height="11" alt="Exportâ€¦"> | <a id="button-std_export"></a>Exportâ€¦ | `Std_Export` | Exports an object in the active document |
| <img src="toolbar-icons/Std_Group.png" width="11" height="11" alt="New Group"> | <a id="button-std_group"></a>New Group | `Std_Group` | Creates a group, which is a general-purpose container to group objects in the tree view, regardless of their data type. It is a simple folder to organize the objects in a model. |
| <img src="toolbar-icons/Std_Import.png" width="11" height="11" alt="Importâ€¦"> | <a id="button-std_import"></a>Importâ€¦ | `Std_Import` | Imports a file into the active document |
| <img src="toolbar-icons/Std_LinkActions.png" width="11" height="11" alt="Make Link"> | <a id="button-std_linkactions"></a>Make Link | `Std_LinkActions` | A link is an object that references another object, either within the same or in another document. Unlike clones, links reference the original shape directly, making them more memory-efficient, which helps with the creation of complex assemblies. |
| <img src="toolbar-icons/Std_LinkActions_1.png" width="11" height="11" alt="Make Sub-Link"> | â†³ Make Sub-Link | `Std_LinkActions` | Creates a sub-object or sub-element link |
| <img src="toolbar-icons/Std_LinkActions_2.png" width="11" height="11" alt="Replace With Link"> | â†³ Replace With Link | `Std_LinkActions` | Replaces the selected objects with links |
| <img src="toolbar-icons/Std_LinkActions_3.png" width="11" height="11" alt="Unlink"> | â†³ Unlink | `Std_LinkActions` | Unlinks the object by placing it directly in the container |
| <img src="toolbar-icons/Std_LinkActions_4.png" width="11" height="11" alt="Import Links"> | â†³ Import Links | `Std_LinkActions` | Imports selected external links |
| <img src="toolbar-icons/Std_LinkActions_5.png" width="11" height="11" alt="Import All Links"> | â†³ Import All Links | `Std_LinkActions` | Imports all links of the active document |
| <img src="toolbar-icons/Std_MassProperties.png" width="11" height="11" alt="Mass Properties"> | <a id="button-std_massproperties"></a>Mass Properties | `Std_MassProperties` | Calculates mass properties of selected objects |
| <img src="toolbar-icons/Std_Measure.png" width="11" height="11" alt="Measure"> | <a id="button-std_measure"></a>Measure | `Std_Measure` | Measures a feature |
| <img src="toolbar-icons/Std_New.png" width="11" height="11" alt="New Document"> | <a id="button-std_new"></a>New Document | `Std_New` | Creates a new empty document |
| <img src="toolbar-icons/Std_NewComponent.png" width="11" height="11" alt="New Component"> | <a id="button-std_newcomponent"></a>New Component | `Std_NewComponent` | Create an embedded model with no assembly instances and open it for editing |
| <img src="toolbar-icons/Std_Open.png" width="11" height="11" alt="Openâ€¦"> | <a id="button-std_open"></a>Openâ€¦ | `Std_Open` | Opens a document or imports files |
| <img src="toolbar-icons/Std_Part.png" width="11" height="11" alt="Add Component"> | <a id="button-std_part"></a>Add Component | `Std_Part` | Adds a component to the active component. |
| <img src="toolbar-icons/Std_Paste.png" width="11" height="11" alt="Paste"> | <a id="button-std_paste"></a>Paste | `Std_Paste` | Pastes the contents of the clipboard |
| <img src="toolbar-icons/Std_Redo.png" width="11" height="11" alt="Redo"> | <a id="button-std_redo"></a>Redo | `Std_Redo` | Redoes a previously undone action |
| <img src="toolbar-icons/Std_Refresh.png" width="11" height="11" alt="Recompute"> | <a id="button-std_refresh"></a>Recompute | `Std_Refresh` | Recomputes the active document |
| <img src="toolbar-icons/Std_Save.png" width="11" height="11" alt="Save"> | <a id="button-std_save"></a>Save | `Std_Save` | Saves the active document |
| <img src="toolbar-icons/Std_SaveAs.png" width="11" height="11" alt="Save Asâ€¦"> | <a id="button-std_saveas"></a>Save Asâ€¦ | `Std_SaveAs` | Saves the active document under a new file name |
| <img src="../../../src/Gui/Icons/preferences-workbenches.svg" width="11" height="11" alt="Toolbars"> | <a id="button-std_toolbarmenu"></a>Toolbars | `Std_ToolBarMenu` | Toggles this window |
| <img src="toolbar-icons/Std_Undo.png" width="11" height="11" alt="Undo"> | <a id="button-std_undo"></a>Undo | `Std_Undo` | Undoes the previous action |
| <img src="toolbar-icons/Std_VarSet.png" width="11" height="11" alt="Variable Set"> | <a id="button-std_varset"></a>Variable Set | `Std_VarSet` | Creates a variable set, which is an object that maintains a set of properties to be used as variables |
| <img src="toolbar-icons/Std_ViewBottom.png" width="11" height="11" alt="Bottom"> | <a id="button-std_viewbottom"></a>Bottom | `Std_ViewBottom` | Sets the camera to the bottom view |
| <img src="toolbar-icons/Std_ViewFitAll.png" width="11" height="11" alt="Fit All"> | <a id="button-std_viewfitall"></a>Fit All | `Std_ViewFitAll` | Fits all content into the 3D view |
| <img src="toolbar-icons/Std_ViewFitSelection.png" width="11" height="11" alt="Fit Selection"> | <a id="button-std_viewfitselection"></a>Fit Selection | `Std_ViewFitSelection` | Fits the selected content into the 3D view |
| <img src="toolbar-icons/Std_ViewFront.png" width="11" height="11" alt="Front"> | <a id="button-std_viewfront"></a>Front | `Std_ViewFront` | Sets the camera to the front view |
| <img src="toolbar-icons/Std_ViewGroup.png" width="11" height="11" alt="Isometric"> | <a id="button-std_viewgroup"></a>Isometric | `Std_ViewGroup` | Sets the camera to the isometric view |
| <img src="toolbar-icons/Std_ViewGroup_1.png" width="11" height="11" alt="Front"> | â†³ Front | `Std_ViewGroup` | Sets the camera to the front view |
| <img src="toolbar-icons/Std_ViewGroup_2.png" width="11" height="11" alt="Top"> | â†³ Top | `Std_ViewGroup` | Sets the camera to the top view |
| <img src="toolbar-icons/Std_ViewGroup_3.png" width="11" height="11" alt="Right"> | â†³ Right | `Std_ViewGroup` | Sets the camera to the right view |
| <img src="toolbar-icons/Std_ViewGroup_4.png" width="11" height="11" alt="Rear"> | â†³ Rear | `Std_ViewGroup` | Sets the camera to the rear view |
| <img src="toolbar-icons/Std_ViewGroup_5.png" width="11" height="11" alt="Bottom"> | â†³ Bottom | `Std_ViewGroup` | Sets the camera to the bottom view |
| <img src="toolbar-icons/Std_ViewGroup_6.png" width="11" height="11" alt="Left"> | â†³ Left | `Std_ViewGroup` | Sets the camera to the left view |
| <img src="toolbar-icons/Std_ViewIsometric.png" width="11" height="11" alt="Isometric"> | <a id="button-std_viewisometric"></a>Isometric | `Std_ViewIsometric` | Sets the camera to the isometric view |
| <img src="toolbar-icons/Std_ViewLeft.png" width="11" height="11" alt="Left"> | <a id="button-std_viewleft"></a>Left | `Std_ViewLeft` | Sets the camera to the left view |
| <img src="toolbar-icons/Std_ViewRear.png" width="11" height="11" alt="Rear"> | <a id="button-std_viewrear"></a>Rear | `Std_ViewRear` | Sets the camera to the rear view |
| <img src="toolbar-icons/Std_ViewRight.png" width="11" height="11" alt="Right"> | <a id="button-std_viewright"></a>Right | `Std_ViewRight` | Sets the camera to the right view |
| <img src="../../../src/Gui/Icons/info.svg" width="11" height="11" alt="Status Bar"> | <a id="button-std_viewstatusbar"></a>Status Bar | `Std_ViewStatusBar` | Toggles the status bar |
| <img src="toolbar-icons/Std_ViewTop.png" width="11" height="11" alt="Top"> | <a id="button-std_viewtop"></a>Top | `Std_ViewTop` | Sets the camera to the top view |
| <img src="toolbar-icons/Std_WhatsThis.png" width="11" height="11" alt="What&#x27;s This?"> | <a id="button-std_whatsthis"></a>What's This? | `Std_WhatsThis` | Opens the documentation for the selected command |
| <img src="toolbar-icons/Std_Workbench.png" width="11" height="11" alt="Assembly"> | <a id="button-std_workbench"></a>Assembly | `Std_Workbench` | Selects the 'Assembly' workbench |
| <img src="toolbar-icons/Std_Workbench_1.png" width="11" height="11" alt="CAM"> | â†³ CAM | `Std_Workbench` | Selects the 'CAM' workbench |
| <img src="toolbar-icons/Std_Workbench_2.png" width="11" height="11" alt="Draft"> | â†³ Draft | `Std_Workbench` | Selects the 'Draft' workbench |
| <img src="toolbar-icons/Std_Workbench_3.png" width="11" height="11" alt="Material"> | â†³ Material | `Std_Workbench` | Selects the 'Material' workbench |
| <img src="toolbar-icons/Std_Workbench_4.png" width="11" height="11" alt="Mesh"> | â†³ Mesh | `Std_Workbench` | Selects the 'Mesh' workbench |
| <img src="toolbar-icons/Std_Workbench_5.png" width="11" height="11" alt="Part Design"> | â†³ Part Design | `Std_Workbench` | Selects the 'Part Design' workbench |
| <img src="toolbar-icons/Std_Workbench_6.png" width="11" height="11" alt="Part"> | â†³ Part | `Std_Workbench` | Selects the 'Part' workbench |
| <img src="toolbar-icons/Std_Workbench_7.png" width="11" height="11" alt="Sketcher"> | â†³ Sketcher | `Std_Workbench` | Selects the 'Sketcher' workbench |
| <img src="toolbar-icons/Std_Workbench_8.png" width="11" height="11" alt="Spreadsheet"> | â†³ Spreadsheet | `Std_Workbench` | Selects the 'Spreadsheet' workbench |
| <img src="toolbar-icons/Std_Workbench_9.png" width="11" height="11" alt="Surface"> | â†³ Surface | `Std_Workbench` | Selects the 'Surface' workbench |
| <img src="toolbar-icons/Std_Workbench_10.png" width="11" height="11" alt="TechDraw"> | â†³ TechDraw | `Std_Workbench` | Selects the 'TechDraw' workbench |
| <img src="toolbar-icons/Std_Workbench_11.png" width="11" height="11" alt=""> | â†³  | `Std_Workbench` | Select the ' ' workbench |
| <img src="toolbar-icons/Std_Workbench_12.png" width="11" height="11" alt="Test Framework"> | â†³ Test Framework | `Std_Workbench` | Select the 'Test Framework' workbench |
| <img src="toolbar-icons/Surface_BlendCurve.png" width="11" height="11" alt="Blend Curve"> | <a id="button-surface_blendcurve"></a>Blend Curve | `Surface_BlendCurve` | Joins 2 edges with continuity |
| <img src="toolbar-icons/Surface_CurveOnMesh.png" width="11" height="11" alt="Curve on Mesh"> | <a id="button-surface_curveonmesh"></a>Curve on Mesh | `Surface_CurveOnMesh` | Creates an approximated curve on top of a mesh. This command only works with a mesh object. |
| <img src="toolbar-icons/Surface_ExtendFace.png" width="11" height="11" alt="Extend Face"> | <a id="button-surface_extendface"></a>Extend Face | `Surface_ExtendFace` | Extrapolates the selected face or surface at its boundaries with its local U and V parameters |
| <img src="toolbar-icons/Surface_Filling.png" width="11" height="11" alt="Filling"> | <a id="button-surface_filling"></a>Filling | `Surface_Filling` | Creates a surface from a series of selected boundary edges. Additionally, the surface may be constrained by edges and vertices that are not on the boundary. |
| <img src="toolbar-icons/Surface_GeomFillSurface.png" width="11" height="11" alt="Fill Boundary Curves"> | <a id="button-surface_geomfillsurface"></a>Fill Boundary Curves | `Surface_GeomFillSurface` | Creates a surface from 2, 3, or 4 boundary edges |
| <img src="toolbar-icons/Surface_Sections.png" width="11" height="11" alt="Sections"> | <a id="button-surface_sections"></a>Sections | `Surface_Sections` | Creates a surface from a series of sectional edges |
| <img src="toolbar-icons/TechDraw_2PointCosmeticLine.png" width="11" height="11" alt="Cosmetic Line Through 2 Points"> | <a id="button-techdraw_2pointcosmeticline"></a>Cosmetic Line Through 2 Points | `TechDraw_2PointCosmeticLine` | Adds a cosmetic line that passes through 2 selected points |
| <img src="toolbar-icons/TechDraw_3PtAngleDimension.png" width="11" height="11" alt="Angle Dimension From 3 Points"> | <a id="button-techdraw_3ptangledimension"></a>Angle Dimension From 3 Points | `TechDraw_3PtAngleDimension` | Inserts an angle dimension between 3 selected points |
| <img src="toolbar-icons/TechDraw_ActiveView.png" width="11" height="11" alt="Active View"> | <a id="button-techdraw_activeview"></a>Active View | `TechDraw_ActiveView` | Inserts an image of the open 3D view in the current page. If multiple 3D views are open, a selection dialog will be shown. |
| <img src="toolbar-icons/TechDraw_AngleDimension.png" width="11" height="11" alt="Angle Dimension"> | <a id="button-techdraw_angledimension"></a>Angle Dimension | `TechDraw_AngleDimension` | Inserts an angle dimension between two edges |
| <img src="toolbar-icons/TechDraw_AreaDimension.png" width="11" height="11" alt="Area Annotation"> | <a id="button-techdraw_areadimension"></a>Area Annotation | `TechDraw_AreaDimension` | Inserts an annotation showing the area of a selected face |
| <img src="toolbar-icons/TechDraw_AxoLengthDimension.png" width="11" height="11" alt="Axonometric Length Dimension"> | <a id="button-techdraw_axolengthdimension"></a>Axonometric Length Dimension | `TechDraw_AxoLengthDimension` | Creates a length dimension in with axonometric view, using selected edges or vertex pairs to define direction and measurement |
| <img src="toolbar-icons/TechDraw_Balloon.png" width="11" height="11" alt="Balloon Annotation"> | <a id="button-techdraw_balloon"></a>Balloon Annotation | `TechDraw_Balloon` | Inserts a new balloon annotation in the selected view |
| <img src="toolbar-icons/TechDraw_BrokenView.png" width="11" height="11" alt="Broken View"> | <a id="button-techdraw_brokenview"></a>Broken View | `TechDraw_BrokenView` | Inserts a new broken view for the selected objects or base view and break definition objects |
| <img src="toolbar-icons/TechDraw_CenterLineGroup.png" width="11" height="11" alt="Centerline on Face"> | <a id="button-techdraw_centerlinegroup"></a>Centerline on Face | `TechDraw_CenterLineGroup` | Adds a centerline to selected faces |
| <img src="toolbar-icons/TechDraw_CenterLineGroup_1.png" width="11" height="11" alt="Centerline Between 2 Lines"> | â†³ Centerline Between 2 Lines | `TechDraw_CenterLineGroup` | Adds a centerline between 2 selected lines |
| <img src="toolbar-icons/TechDraw_CenterLineGroup_2.png" width="11" height="11" alt="Centerline Between 2 Points"> | â†³ Centerline Between 2 Points | `TechDraw_CenterLineGroup` | Adds a centerline between 2 selected points |
| <img src="toolbar-icons/TechDraw_ClipGroup.png" width="11" height="11" alt="Clip Group"> | <a id="button-techdraw_clipgroup"></a>Clip Group | `TechDraw_ClipGroup` | Inserts a new clip group for the selected view |
| <img src="toolbar-icons/TechDraw_CommandAddOffsetVertex.png" width="11" height="11" alt="Offset Vertex"> | <a id="button-techdraw_commandaddoffsetvertex"></a>Offset Vertex | `TechDraw_CommandAddOffsetVertex` | Creates an offset from one selected vertex |
| <img src="toolbar-icons/TechDraw_CommandVertexCreationGroup.png" width="11" height="11" alt="Cosmetic Intersection Vertices"> | <a id="button-techdraw_commandvertexcreationgroup"></a>Cosmetic Intersection Vertices | `TechDraw_CommandVertexCreationGroup` | Cosmetic Intersection Vertices |
| <img src="toolbar-icons/TechDraw_CommandVertexCreationGroup_1.png" width="11" height="11" alt="Offset Vertex"> | â†³ Offset Vertex | `TechDraw_CommandVertexCreationGroup` | Creates an offset from one selected vertex |
| <img src="toolbar-icons/TechDraw_CompDimensionTools.png" width="11" height="11" alt="Dimension"> | <a id="button-techdraw_compdimensiontools"></a>Dimension | `TechDraw_CompDimensionTools` | Inserts new contextual dimensions to the selection. Depending on your selection you might have several dimensions available. You can cycle through them using the M key. Left clicking on empty space will validate the current dimension. Right clicking or pressing Esc will cancel. |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_2.png" width="11" height="11" alt="Length Dimension"> | â†³ Length Dimension | `TechDraw_CompDimensionTools` | Inserts a length dimension of an edge or distance between two points |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_3.png" width="11" height="11" alt="Horizontal Length Dimension"> | â†³ Horizontal Length Dimension | `TechDraw_CompDimensionTools` | Inserts a horizontal length dimension of an edge or distance between two points |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_4.png" width="11" height="11" alt="Vertical Length Dimension"> | â†³ Vertical Length Dimension | `TechDraw_CompDimensionTools` | Inserts a vertical length dimension of an edge or distance between two points |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_5.png" width="11" height="11" alt="Radius Dimension"> | â†³ Radius Dimension | `TechDraw_CompDimensionTools` | Inserts a radius dimension of a circular edge or arc |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_6.png" width="11" height="11" alt="Diameter Dimension"> | â†³ Diameter Dimension | `TechDraw_CompDimensionTools` | Inserts a diameter dimension of a circular edge or arc |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_7.png" width="11" height="11" alt="Angle Dimension"> | â†³ Angle Dimension | `TechDraw_CompDimensionTools` | Inserts an angle dimension between two edges |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_8.png" width="11" height="11" alt="Angle Dimension From 3 Points"> | â†³ Angle Dimension From 3 Points | `TechDraw_CompDimensionTools` | Inserts an angle dimension between 3 selected points |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_9.png" width="11" height="11" alt="Area Annotation"> | â†³ Area Annotation | `TechDraw_CompDimensionTools` | Inserts an annotation showing the area of a selected face |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_10.png" width="11" height="11" alt="Arc Length Dimension"> | â†³ Arc Length Dimension | `TechDraw_CompDimensionTools` | Arc Length Dimension |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_12.png" width="11" height="11" alt="Horizontal Extent Dimension"> | â†³ Horizontal Extent Dimension | `TechDraw_CompDimensionTools` | Inserts a dimension showing the horizontal extent (overall length) of an object or feature |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_13.png" width="11" height="11" alt="Vertical Extent Dimension"> | â†³ Vertical Extent Dimension | `TechDraw_CompDimensionTools` | Inserts a dimension showing the vertical extent (overall length) of an object or feature |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_15.png" width="11" height="11" alt="Horizontal Chain Dimension"> | â†³ Horizontal Chain Dimension | `TechDraw_CompDimensionTools` | Horizontal Chain Dimension |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_16.png" width="11" height="11" alt="Vertical Chain Dimension"> | â†³ Vertical Chain Dimension | `TechDraw_CompDimensionTools` | Vertical Chain Dimension |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_17.png" width="11" height="11" alt="Oblique Chain Dimension"> | â†³ Oblique Chain Dimension | `TechDraw_CompDimensionTools` | Oblique Chain Dimension |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_19.png" width="11" height="11" alt="Horizontal Coordinate Dimension"> | â†³ Horizontal Coordinate Dimension | `TechDraw_CompDimensionTools` | Horizontal Coordinate Dimension |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_20.png" width="11" height="11" alt="Vertical Coordinate Dimension"> | â†³ Vertical Coordinate Dimension | `TechDraw_CompDimensionTools` | Vertical Coordinate Dimension |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_21.png" width="11" height="11" alt="Oblique Coordinate Dimension"> | â†³ Oblique Coordinate Dimension | `TechDraw_CompDimensionTools` | Oblique Coordinate Dimension |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_23.png" width="11" height="11" alt="Horizontal Chamfer Dimension"> | â†³ Horizontal Chamfer Dimension | `TechDraw_CompDimensionTools` | Horizontal Chamfer Dimension |
| <img src="toolbar-icons/TechDraw_CompDimensionTools_24.png" width="11" height="11" alt="Vertical Chamfer Dimension"> | â†³ Vertical Chamfer Dimension | `TechDraw_CompDimensionTools` | Vertical Chamfer Dimension |
| <img src="toolbar-icons/TechDraw_CosmeticVertexGroup.png" width="11" height="11" alt="Cosmetic Vertex"> | <a id="button-techdraw_cosmeticvertexgroup"></a>Cosmetic Vertex | `TechDraw_CosmeticVertexGroup` | Inserts a cosmetic vertex into a view |
| <img src="toolbar-icons/TechDraw_CosmeticVertexGroup_1.png" width="11" height="11" alt="Midpoint Vertices"> | â†³ Midpoint Vertices | `TechDraw_CosmeticVertexGroup` | Inserts cosmetic vertices at the midpoint of the selected edges |
| <img src="toolbar-icons/TechDraw_CosmeticVertexGroup_2.png" width="11" height="11" alt="Quadrant Vertices"> | â†³ Quadrant Vertices | `TechDraw_CosmeticVertexGroup` | Inserts cosmetic vertices at the quadrant points of the selected circles |
| <img src="toolbar-icons/TechDraw_DecorateLine.png" width="11" height="11" alt="Edit Line Appearance"> | <a id="button-techdraw_decorateline"></a>Edit Line Appearance | `TechDraw_DecorateLine` | Opens the 'Line decoration' dialog to edit the selected lines |
| <img src="toolbar-icons/TechDraw_DetailView.png" width="11" height="11" alt="Detail View"> | <a id="button-techdraw_detailview"></a>Detail View | `TechDraw_DetailView` | Inserts a new detail view based on the selected view in the current page |
| <img src="toolbar-icons/TechDraw_DiameterDimension.png" width="11" height="11" alt="Diameter Dimension"> | <a id="button-techdraw_diameterdimension"></a>Diameter Dimension | `TechDraw_DiameterDimension` | Inserts a diameter dimension of a circular edge or arc |
| <img src="toolbar-icons/TechDraw_Dimension.png" width="11" height="11" alt="Dimension"> | <a id="button-techdraw_dimension"></a>Dimension | `TechDraw_Dimension` | Inserts new contextual dimensions to the selection. Depending on your selection you might have several dimensions available. You can cycle through them using the M key. Left clicking on empty space will validate the current dimension. Right clicking or pressing Esc will cancel. |
| <img src="toolbar-icons/TechDraw_DimensionRepair.png" width="11" height="11" alt="Repair Dimension References"> | <a id="button-techdraw_dimensionrepair"></a>Repair Dimension References | `TechDraw_DimensionRepair` | Repairs broken or incorrect dimension references |
| <img src="toolbar-icons/TechDraw_DraftView.png" width="11" height="11" alt="Draft View"> | <a id="button-techdraw_draftview"></a>Draft View | `TechDraw_DraftView` | Inserts a view of a Draft object |
| <img src="toolbar-icons/TechDraw_ExportPageDXF.png" width="11" height="11" alt="Export Page as DXF"> | <a id="button-techdraw_exportpagedxf"></a>Export Page as DXF | `TechDraw_ExportPageDXF` | Exports the current page as a DXF |
| <img src="toolbar-icons/TechDraw_ExportPageSVG.png" width="11" height="11" alt="Export Page as SVG"> | <a id="button-techdraw_exportpagesvg"></a>Export Page as SVG | `TechDraw_ExportPageSVG` | Exports the current page as an SVG |
| <img src="toolbar-icons/TechDraw_ExtensionArcLengthAnnotation.png" width="11" height="11" alt="Arc Length Annotation"> | <a id="button-techdraw_extensionarclengthannotation"></a>Arc Length Annotation | `TechDraw_ExtensionArcLengthAnnotation` | Inserts an annotation with the calculated arc length of the selected edges |
| <img src="toolbar-icons/TechDraw_ExtensionAreaAnnotation.png" width="11" height="11" alt="Area Annotation"> | <a id="button-techdraw_extensionareaannotation"></a>Area Annotation | `TechDraw_ExtensionAreaAnnotation` | Calculates the area of multiple selected faces |
| <img src="toolbar-icons/TechDraw_ExtensionChamferDimensionGroup.png" width="11" height="11" alt="Horizontal Chamfer Dimension"> | <a id="button-techdraw_extensionchamferdimensiongroup"></a>Horizontal Chamfer Dimension | `TechDraw_ExtensionChamferDimensionGroup` | Horizontal Chamfer Dimension |
| <img src="toolbar-icons/TechDraw_ExtensionChamferDimensionGroup_1.png" width="11" height="11" alt="Vertical Chamfer Dimension"> | â†³ Vertical Chamfer Dimension | `TechDraw_ExtensionChamferDimensionGroup` | Vertical Chamfer Dimension |
| <img src="toolbar-icons/TechDraw_ExtensionChangeLineAttributes.png" width="11" height="11" alt="Change Line Attributes"> | <a id="button-techdraw_extensionchangelineattributes"></a>Change Line Attributes | `TechDraw_ExtensionChangeLineAttributes` | Change Line Attributes |
| <img src="toolbar-icons/TechDraw_ExtensionCircleCenterLinesGroup.png" width="11" height="11" alt="Circle Centerlines"> | <a id="button-techdraw_extensioncirclecenterlinesgroup"></a>Circle Centerlines | `TechDraw_ExtensionCircleCenterLinesGroup` | Circle Centerlines |
| <img src="toolbar-icons/TechDraw_ExtensionCircleCenterLinesGroup_1.png" width="11" height="11" alt="Bolt Circle Centerlines"> | â†³ Bolt Circle Centerlines | `TechDraw_ExtensionCircleCenterLinesGroup` | Bolt Circle Centerlines |
| <img src="toolbar-icons/TechDraw_ExtensionCreateChainDimensionGroup.png" width="11" height="11" alt="Horizontal Chain Dimension"> | <a id="button-techdraw_extensioncreatechaindimensiongroup"></a>Horizontal Chain Dimension | `TechDraw_ExtensionCreateChainDimensionGroup` | Horizontal Chain Dimension |
| <img src="toolbar-icons/TechDraw_ExtensionCreateChainDimensionGroup_1.png" width="11" height="11" alt="Vertical Chain Dimension"> | â†³ Vertical Chain Dimension | `TechDraw_ExtensionCreateChainDimensionGroup` | Vertical Chain Dimension |
| <img src="toolbar-icons/TechDraw_ExtensionCreateChainDimensionGroup_2.png" width="11" height="11" alt="Oblique Chain Dimension"> | â†³ Oblique Chain Dimension | `TechDraw_ExtensionCreateChainDimensionGroup` | Oblique Chain Dimension |
| <img src="toolbar-icons/TechDraw_ExtensionCreateCoordDimensionGroup.png" width="11" height="11" alt="Horizontal Coordinate Dimension"> | <a id="button-techdraw_extensioncreatecoorddimensiongroup"></a>Horizontal Coordinate Dimension | `TechDraw_ExtensionCreateCoordDimensionGroup` | Horizontal Coordinate Dimension |
| <img src="toolbar-icons/TechDraw_ExtensionCreateCoordDimensionGroup_1.png" width="11" height="11" alt="Vertical Coordinate Dimension"> | â†³ Vertical Coordinate Dimension | `TechDraw_ExtensionCreateCoordDimensionGroup` | Vertical Coordinate Dimension |
| <img src="toolbar-icons/TechDraw_ExtensionCreateCoordDimensionGroup_2.png" width="11" height="11" alt="Oblique Coordinate Dimension"> | â†³ Oblique Coordinate Dimension | `TechDraw_ExtensionCreateCoordDimensionGroup` | Oblique Coordinate Dimension |
| <img src="toolbar-icons/TechDraw_ExtensionCreateLengthArc.png" width="11" height="11" alt="Arc Length Dimension"> | <a id="button-techdraw_extensioncreatelengtharc"></a>Arc Length Dimension | `TechDraw_ExtensionCreateLengthArc` | Arc Length Dimension |
| <img src="toolbar-icons/TechDraw_ExtensionCustomizeFormat.png" width="11" height="11" alt="Customize Format Label"> | <a id="button-techdraw_extensioncustomizeformat"></a>Customize Format Label | `TechDraw_ExtensionCustomizeFormat` | Customizes the format label of a selected dimension or balloon |
| <img src="toolbar-icons/TechDraw_ExtensionDrawCirclesGroup.png" width="11" height="11" alt="Cosmetic 1 Point Circle"> | <a id="button-techdraw_extensiondrawcirclesgroup"></a>Cosmetic 1 Point Circle | `TechDraw_ExtensionDrawCirclesGroup` | Cosmetic 1 Point Circle |
| <img src="toolbar-icons/TechDraw_ExtensionDrawCirclesGroup_1.png" width="11" height="11" alt="Cosmetic 2 Point Circle"> | â†³ Cosmetic 2 Point Circle | `TechDraw_ExtensionDrawCirclesGroup` | Cosmetic 2 Point Circle |
| <img src="toolbar-icons/TechDraw_ExtensionDrawCirclesGroup_2.png" width="11" height="11" alt="Cosmetic 3 Point Circle"> | â†³ Cosmetic 3 Point Circle | `TechDraw_ExtensionDrawCirclesGroup` | Cosmetic 3 Point Circle |
| <img src="toolbar-icons/TechDraw_ExtensionDrawCirclesGroup_3.png" width="11" height="11" alt="Cosmetic Arc"> | â†³ Cosmetic Arc | `TechDraw_ExtensionDrawCirclesGroup` | Cosmetic Arc |
| <img src="toolbar-icons/TechDraw_ExtensionExtendShortenLineGroup.png" width="11" height="11" alt="Extend Line"> | <a id="button-techdraw_extensionextendshortenlinegroup"></a>Extend Line | `TechDraw_ExtensionExtendShortenLineGroup` | Extend Line |
| <img src="toolbar-icons/TechDraw_ExtensionExtendShortenLineGroup_1.png" width="11" height="11" alt="Shorten Line"> | â†³ Shorten Line | `TechDraw_ExtensionExtendShortenLineGroup` | Shorten Line |
| <img src="toolbar-icons/TechDraw_ExtensionIncreaseDecreaseGroup.png" width="11" height="11" alt="Increase Decimal Places"> | <a id="button-techdraw_extensionincreasedecreasegroup"></a>Increase Decimal Places | `TechDraw_ExtensionIncreaseDecreaseGroup` | Increase Decimal Places |
| <img src="toolbar-icons/TechDraw_ExtensionIncreaseDecreaseGroup_1.png" width="11" height="11" alt="Decrease Decimal Places"> | â†³ Decrease Decimal Places | `TechDraw_ExtensionIncreaseDecreaseGroup` | Decrease Decimal Places |
| <img src="toolbar-icons/TechDraw_ExtensionInsertPrefixGroup.png" width="11" height="11" alt="Insert &#x27;âŒ€&#x27; Prefix"> | <a id="button-techdraw_extensioninsertprefixgroup"></a>Insert 'âŒ€' Prefix | `TechDraw_ExtensionInsertPrefixGroup` | Insert 'âŒ€' Prefix |
| <img src="toolbar-icons/TechDraw_ExtensionInsertPrefixGroup_1.png" width="11" height="11" alt="Insert &#x27;â–¡&#x27; Prefix"> | â†³ Insert 'â–¡' Prefix | `TechDraw_ExtensionInsertPrefixGroup` | Insert 'â–¡' Prefix |
| <img src="toolbar-icons/TechDraw_ExtensionInsertPrefixGroup_2.png" width="11" height="11" alt="Insert &#x27;nÃ—&#x27; Prefix"> | â†³ Insert 'nÃ—' Prefix | `TechDraw_ExtensionInsertPrefixGroup` | Insert 'nÃ—' Prefix |
| <img src="toolbar-icons/TechDraw_ExtensionInsertPrefixGroup_3.png" width="11" height="11" alt="Remove Prefix"> | â†³ Remove Prefix | `TechDraw_ExtensionInsertPrefixGroup` | Remove Prefix |
| <img src="toolbar-icons/TechDraw_ExtensionLinePPGroup.png" width="11" height="11" alt="Cosmetic Parallel Line"> | <a id="button-techdraw_extensionlineppgroup"></a>Cosmetic Parallel Line | `TechDraw_ExtensionLinePPGroup` | Cosmetic Parallel Line |
| <img src="toolbar-icons/TechDraw_ExtensionLinePPGroup_1.png" width="11" height="11" alt="Cosmetic Perpendicular Line"> | â†³ Cosmetic Perpendicular Line | `TechDraw_ExtensionLinePPGroup` | Cosmetic Perpendicular Line |
| <img src="toolbar-icons/TechDraw_ExtensionLockUnlockView.png" width="11" height="11" alt="Toggle View Lock"> | <a id="button-techdraw_extensionlockunlockview"></a>Toggle View Lock | `TechDraw_ExtensionLockUnlockView` | Toggle View Lock |
| <img src="toolbar-icons/TechDraw_ExtensionPositionSectionView.png" width="11" height="11" alt="Position Section View"> | <a id="button-techdraw_extensionpositionsectionview"></a>Position Section View | `TechDraw_ExtensionPositionSectionView` | Aligns the selected section view with its source view orthogonally or the selected edge in the section view to the selected vertex in the base view |
| <img src="toolbar-icons/TechDraw_ExtensionSelectLineAttributes.png" width="11" height="11" alt="Select Line Attributes, Cascade Spacing and Delta Distance"> | <a id="button-techdraw_extensionselectlineattributes"></a>Select Line Attributes, Cascade Spacing and Delta Distance | `TechDraw_ExtensionSelectLineAttributes` | Select Line Attributes, Cascade Spacing and Delta Distance |
| <img src="toolbar-icons/TechDraw_ExtensionThreadsGroup.png" width="11" height="11" alt="Cosmetic Thread Hole Side View"> | <a id="button-techdraw_extensionthreadsgroup"></a>Cosmetic Thread Hole Side View | `TechDraw_ExtensionThreadsGroup` | Cosmetic Thread Hole Side View |
| <img src="toolbar-icons/TechDraw_ExtensionThreadsGroup_1.png" width="11" height="11" alt="Cosmetic Thread Hole Bottom View"> | â†³ Cosmetic Thread Hole Bottom View | `TechDraw_ExtensionThreadsGroup` | Cosmetic Thread Hole Bottom View |
| <img src="toolbar-icons/TechDraw_ExtensionThreadsGroup_2.png" width="11" height="11" alt="Cosmetic Thread Bolt Side View"> | â†³ Cosmetic Thread Bolt Side View | `TechDraw_ExtensionThreadsGroup` | Cosmetic Thread Bolt Side View |
| <img src="toolbar-icons/TechDraw_ExtensionThreadsGroup_3.png" width="11" height="11" alt="Cosmetic Thread Bolt Bottom View"> | â†³ Cosmetic Thread Bolt Bottom View | `TechDraw_ExtensionThreadsGroup` | Cosmetic Thread Bolt Bottom View |
| <img src="toolbar-icons/TechDraw_ExtensionVertexAtIntersection.png" width="11" height="11" alt="Cosmetic Intersection Vertices"> | <a id="button-techdraw_extensionvertexatintersection"></a>Cosmetic Intersection Vertices | `TechDraw_ExtensionVertexAtIntersection` | Cosmetic Intersection Vertices |
| <img src="toolbar-icons/TechDraw_ExtentGroup.png" width="11" height="11" alt="Horizontal extent"> | <a id="button-techdraw_extentgroup"></a>Horizontal extent | `TechDraw_ExtentGroup` | Insert horizontal extent dimension |
| <img src="toolbar-icons/TechDraw_ExtentGroup_1.png" width="11" height="11" alt="Vertical extent"> | â†³ Vertical extent | `TechDraw_ExtentGroup` | Insert vertical extent dimension |
| <img src="toolbar-icons/TechDraw_FillTemplateFields.png" width="11" height="11" alt="Update Template Fields"> | <a id="button-techdraw_filltemplatefields"></a>Update Template Fields | `TechDraw_FillTemplateFields` | Uses document info to populate the template fields |
| <img src="toolbar-icons/TechDraw_GeometricHatch.png" width="11" height="11" alt="Geometric Hatch"> | <a id="button-techdraw_geometrichatch"></a>Geometric Hatch | `TechDraw_GeometricHatch` | Applies a geometric hatch pattern to the selected faces |
| <img src="toolbar-icons/TechDraw_Hatch.png" width="11" height="11" alt="Image Hatch"> | <a id="button-techdraw_hatch"></a>Image Hatch | `TechDraw_Hatch` | Applies a hatch pattern to the selected faces using an image file |
| <img src="toolbar-icons/TechDraw_HoleShaftFit.png" width="11" height="11" alt="Hole/Shaft Fit"> | <a id="button-techdraw_holeshaftfit"></a>Hole/Shaft Fit | `TechDraw_HoleShaftFit` | Adds a hole or shaft fit to a selected length or diameter dimension |
| <img src="toolbar-icons/TechDraw_HorizontalDimension.png" width="11" height="11" alt="Horizontal Length Dimension"> | <a id="button-techdraw_horizontaldimension"></a>Horizontal Length Dimension | `TechDraw_HorizontalDimension` | Inserts a horizontal length dimension of an edge or distance between two points |
| <img src="toolbar-icons/TechDraw_LeaderLine.png" width="11" height="11" alt="Leader Line"> | <a id="button-techdraw_leaderline"></a>Leader Line | `TechDraw_LeaderLine` | Adds a leader line |
| <img src="toolbar-icons/TechDraw_LengthDimension.png" width="11" height="11" alt="Length Dimension"> | <a id="button-techdraw_lengthdimension"></a>Length Dimension | `TechDraw_LengthDimension` | Inserts a length dimension of an edge or distance between two points |
| <img src="toolbar-icons/TechDraw_PageDefault.png" width="11" height="11" alt="New Page"> | <a id="button-techdraw_pagedefault"></a>New Page | `TechDraw_PageDefault` | Creates a new page with the default template |
| <img src="toolbar-icons/TechDraw_PageTemplate.png" width="11" height="11" alt="New Page From Template"> | <a id="button-techdraw_pagetemplate"></a>New Page From Template | `TechDraw_PageTemplate` | Creates a new page from a custom template |
| <img src="toolbar-icons/TechDraw_PrintAll.png" width="11" height="11" alt="Print All Pages"> | <a id="button-techdraw_printall"></a>Print All Pages | `TechDraw_PrintAll` | Prints all pages with the print dialog |
| <img src="toolbar-icons/TechDraw_RadiusDimension.png" width="11" height="11" alt="Radius Dimension"> | <a id="button-techdraw_radiusdimension"></a>Radius Dimension | `TechDraw_RadiusDimension` | Inserts a radius dimension of a circular edge or arc |
| <img src="toolbar-icons/TechDraw_RedrawPage.png" width="11" height="11" alt="Redraw Page"> | <a id="button-techdraw_redrawpage"></a>Redraw Page | `TechDraw_RedrawPage` | Redraws the current page |
| <img src="toolbar-icons/TechDraw_RichTextAnnotation.png" width="11" height="11" alt="Rich Text Annotation"> | <a id="button-techdraw_richtextannotation"></a>Rich Text Annotation | `TechDraw_RichTextAnnotation` | Inserts a rich text annotation in the current page |
| <img src="toolbar-icons/TechDraw_SectionGroup.png" width="11" height="11" alt="Section View"> | <a id="button-techdraw_sectiongroup"></a>Section View | `TechDraw_SectionGroup` | Inserts a simple section view |
| <img src="toolbar-icons/TechDraw_SectionGroup_1.png" width="11" height="11" alt="Complex Section View"> | â†³ Complex Section View | `TechDraw_SectionGroup` | Inserts a complex section view |
| <img src="toolbar-icons/TechDraw_ShowAll.png" width="11" height="11" alt="Toggle Edge Visibility"> | <a id="button-techdraw_showall"></a>Toggle Edge Visibility | `TechDraw_ShowAll` | Toggles the visibility of the selected edges |
| <img src="toolbar-icons/TechDraw_SpreadsheetView.png" width="11" height="11" alt="Spreadsheet View"> | <a id="button-techdraw_spreadsheetview"></a>Spreadsheet View | `TechDraw_SpreadsheetView` | Inserts a view of a spreadsheet in the current page |
| <img src="toolbar-icons/TechDraw_StackGroup.png" width="11" height="11" alt="Stack Top"> | <a id="button-techdraw_stackgroup"></a>Stack Top | `TechDraw_StackGroup` | Moves the view to the top of the stack |
| <img src="toolbar-icons/TechDraw_StackGroup_1.png" width="11" height="11" alt="Stack Bottom"> | â†³ Stack Bottom | `TechDraw_StackGroup` | Moves the view to the bottom of the stack |
| <img src="toolbar-icons/TechDraw_StackGroup_2.png" width="11" height="11" alt="Stack Up"> | â†³ Stack Up | `TechDraw_StackGroup` | Moves the view up one level |
| <img src="toolbar-icons/TechDraw_StackGroup_3.png" width="11" height="11" alt="Stack Down"> | â†³ Stack Down | `TechDraw_StackGroup` | Moves the view down one level |
| <img src="toolbar-icons/TechDraw_SurfaceFinishSymbols.png" width="11" height="11" alt="Surface Finish Symbol"> | <a id="button-techdraw_surfacefinishsymbols"></a>Surface Finish Symbol | `TechDraw_SurfaceFinishSymbols` | Adds a surface finish symbol in the selected view |
| <img src="toolbar-icons/TechDraw_ToggleFrame.png" width="11" height="11" alt="Toggle View Frames"> | <a id="button-techdraw_toggleframe"></a>Toggle View Frames | `TechDraw_ToggleFrame` | Toggles visibility of view frames and vertices |
| <img src="toolbar-icons/TechDraw_VerticalDimension.png" width="11" height="11" alt="Vertical Length Dimension"> | <a id="button-techdraw_verticaldimension"></a>Vertical Length Dimension | `TechDraw_VerticalDimension` | Inserts a vertical length dimension of an edge or distance between two points |
| <img src="toolbar-icons/TechDraw_View.png" width="11" height="11" alt="New View"> | <a id="button-techdraw_view"></a>New View | `TechDraw_View` | Inserts a new view into the current page based on the selected object in the tree view or 3D view. If no object is selected, a file browser opens to select an SVG or image file. |
| <img src="toolbar-icons/TechDraw_WeldSymbol.png" width="11" height="11" alt="Weld Symbol"> | <a id="button-techdraw_weldsymbol"></a>Weld Symbol | `TechDraw_WeldSymbol` | Adds welding information to the selected leader line |
| <img src="../../../src/Gui/Icons/preferences-general.svg" width="11" height="11" alt="Self-test..."> | <a id="button-test_test"></a>Self-test... | `Test_Test` | Runs a self-test to check if the application works properly |
| <img src="toolbar-icons/Test_TestAll.png" width="11" height="11" alt="Test all"> | <a id="button-test_testall"></a>Test all | `Test_TestAll` | Runs all tests at once (can take very long!) |
| <img src="toolbar-icons/Test_TestBase.png" width="11" height="11" alt="Test base"> | <a id="button-test_testbase"></a>Test base | `Test_TestBase` | Test the basic functions of FreeCAD |
| <img src="toolbar-icons/Test_TestDoc.png" width="11" height="11" alt="Test Document"> | <a id="button-test_testdoc"></a>Test Document | `Test_TestDoc` | Test the document (creation, save, load and destruction) |
