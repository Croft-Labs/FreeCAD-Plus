# FreeCAD Plus toolbar governance and visual reference

## Authority and maintenance

This is the governing command-placement reference for Classic versus Plus toolbars. The [UI specification](../../UI_UX_SPEC.md#toolbar-ui-styles) owns shared interaction and sizing rules. Change this reference whenever a toolbar command, section, dropdown or caption changes; preserve command IDs and native action behavior. Do not silently remove a function when consolidating buttons.

Common actions use large buttons (**L**); secondary actions use small icons (**S**) in three rows; related/rare variants use dropdowns (**▼**). Icons below identify commands; these Markdown tables show membership and order, not exact ribbon pixel layout. Plus and Classic are mutually exclusive. Default UI is Plus; explicit saved Classic choices remain valid.

Snapshot: 2026-10-02. Fork source `d32c3542384c`; recorded upstream FreeCAD/main `b9609745048b`. Upstream means that local source snapshot, not a claim that the remote has no later commits. Native action metadata/icons were read from the fork executable at application source `52495b0cb2bd`; Plus grouping/projection was read from current source. Pending source ribbon changes are not yet incorporated in the owner's 10/2 build. Runtime export is an inventory check, not functional acceptance of every command.

For every toolbar change, review placement, native command identity, retained functionality, icon/caption, large/small/dropdown priority, enabled/checked states and accessibility. Record new implementations and build/acceptance status in the existing roadmap/WORK_STATE, rather than treating this catalog as a release record.

Classic tables list upstream definitions, including context-dependent/edit-only groups. They do not claim all groups are visible simultaneously. Compound toolbar buttons keep native choices; the final catalog expands those choices. Separators are shown as dots.

To refresh: run [ExportToolbarReference.FCMacro](../../../tools/ExportToolbarReference.FCMacro) with isolated preferences against this fork, then `python tools/GenerateToolbarReference.py <inventory.json> <recorded-upstream-ref>`. Review upstream-specific differences and source-only entries before accepting generated changes. PNG icons are native action renders of the existing FreeCAD artwork; original licensing remains in [LICENSE](../../../LICENSE) and the corresponding source resource folders.

## Navigation

- [Shared desktop toolbars](#shared-desktop-toolbars)
- [Part Design](#workbench-partdesignworkbench)
- [Part](#workbench-partworkbench)
- [Sketcher](#workbench-sketcherworkbench)
- [Surface](#workbench-surfaceworkbench)
- [Mesh](#workbench-meshworkbench)
- [Draft](#workbench-draftworkbench)
- [Assembly](#workbench-assemblyworkbench)
- [CAM](#workbench-camworkbench)
- [TechDraw](#workbench-techdrawworkbench)
- [FEM](#workbench-femworkbench)
- [Spreadsheet](#workbench-spreadsheetworkbench)
- [Material](#workbench-materialworkbench)
- [MeshPart](#workbench-meshpartworkbench)
- [Points](#workbench-pointsworkbench)
- [Robot](#workbench-robotworkbench)
- [ReverseEngineering](#workbench-reverseengineeringworkbench)
- [Inspection](#workbench-inspectionworkbench)
- [BIM](#workbench-bimworkbench)
- [OpenSCAD](#workbench-openscadworkbench)
- [Test Framework](#workbench-testworkbench)
- [Complete button/function catalog](#complete-toolbar-buttonfunction-catalog)

## Shared desktop toolbars

### Classic upstream groups

The shared list includes Part's upstream toolbar manipulator additions: Datums in Structure and the native selection filter in View, once PartGui is loaded. The Classic Workbench control is a selector, not an Assembly operation button.

| Section / toolbar group | Buttons in display order |
| --- | --- |
| File | ![New Document](toolbar-icons/Std_New.png) [New Document](#button-std_new); ![Open…](toolbar-icons/Std_Open.png) [Open…](#button-std_open); ![Save](toolbar-icons/Std_Save.png) [Save](#button-std_save) |
| Edit | ![Undo](toolbar-icons/Std_Undo.png) [Undo](#button-std_undo); ![Redo](toolbar-icons/Std_Redo.png) [Redo](#button-std_redo);  · ; ![Recompute](toolbar-icons/Std_Refresh.png) [Recompute](#button-std_refresh) |
| Clipboard | ![Cut](toolbar-icons/Std_Cut.png) [Cut](#button-std_cut); ![Copy](toolbar-icons/Std_Copy.png) [Copy](#button-std_copy); ![Paste](toolbar-icons/Std_Paste.png) [Paste](#button-std_paste) |
| Workbench | ![Assembly](toolbar-icons/Std_Workbench.png) [Assembly](#button-std_workbench) |
| Macro | ![Record Macro](toolbar-icons/Std_DlgMacroRecord.png) [Record Macro](#button-std_dlgmacrorecord); ![Macros](toolbar-icons/Std_DlgMacroExecute.png) [Macros](#button-std_dlgmacroexecute); ![Execute Macro](toolbar-icons/Std_DlgMacroExecuteDirect.png) [Execute Macro](#button-std_dlgmacroexecutedirect) |
| View | ![Fit All](toolbar-icons/Std_ViewFitAll.png) [Fit All](#button-std_viewfitall); ![Fit Selection](toolbar-icons/Std_ViewFitSelection.png) [Fit Selection](#button-std_viewfitselection); ![Isometric](toolbar-icons/Std_ViewGroup.png) [Isometric](#button-std_viewgroup); ![Align to Selection](toolbar-icons/Std_AlignToSelection.png) [Align to Selection](#button-std_aligntoselection);  · ; ![As Is](toolbar-icons/Std_DrawStyle.png) [As Is](#button-std_drawstyle); ![Vertex Selection](toolbar-icons/Part_SelectFilter.png) [Vertex Selection](#button-part_selectfilter);  · ; ![Measure](toolbar-icons/Std_Measure.png) [Measure](#button-std_measure); ![Mass Properties](toolbar-icons/Std_MassProperties.png) [Mass Properties](#button-std_massproperties) |
| Individual Views | ![Isometric](toolbar-icons/Std_ViewIsometric.png) [Isometric](#button-std_viewisometric); ![Front](toolbar-icons/Std_ViewFront.png) [Front](#button-std_viewfront); ![Top](toolbar-icons/Std_ViewTop.png) [Top](#button-std_viewtop); ![Right](toolbar-icons/Std_ViewRight.png) [Right](#button-std_viewright); ![Rear](toolbar-icons/Std_ViewRear.png) [Rear](#button-std_viewrear); ![Bottom](toolbar-icons/Std_ViewBottom.png) [Bottom](#button-std_viewbottom); ![Left](toolbar-icons/Std_ViewLeft.png) [Left](#button-std_viewleft) |
| Structure | ![Add Component](toolbar-icons/Std_Part.png) [New Part](#button-std_part); ![Coordinate System](toolbar-icons/Part_Datums.png) [Coordinate System](#button-part_datums); ![New Group](toolbar-icons/Std_Group.png) [New Group](#button-std_group); ![Make Link](toolbar-icons/Std_LinkActions.png) [Make Link](#button-std_linkactions); ![Variable Set](toolbar-icons/Std_VarSet.png) [Variable Set](#button-std_varset) |
| Help | ![What's This?](toolbar-icons/Std_WhatsThis.png) [What's This?](#button-std_whatsthis) |

### Changes in Plus

- The Workbench selector is replaced visually by the mode dropdown (Design, Draft, CAM, etc.).
- File adds Save As, Import and Export; New uses the document icon and caption **New File**, with the component-document workflow. Native command identity remains `Std_New`.
- Edit adds Delete and Preferences. Clipboard remains its native section.
- Home Structure uses Components, Add part, Group, Link Actions and Add Reference Object. The audit correction restores native Datums as one dropdown and Variable Set as a small button. Coordinate System/Datum Plane creation is also exposed through the idle component Tasks pane.
- View and Individual Views move to the View tab; Display adds selection filters, toolbar menu, dock menu and status-bar toggle.
- Help and Macro each use one compact dropdown; record, macro manager and direct execution retain native states. The audit correction restores Macro ribbon access.
- Iconless native actions get a ribbon-only icon from existing artwork. Their native QAction icons, states and menu identities remain unchanged. Native compound-menu separators are omitted from button-choice lists.
- Home common Tools adds Command Search, Measure and Mass Properties in Design. Workbenches retain their native menu/shortcut commands even where the ribbon omits a toolbar button.

### Plus shared sections

| Section / toolbar group | Buttons in display order |
| --- | --- |
| File | ![New Document](toolbar-icons/Std_New.png) [New File](#button-std_new) **L**; ![Open…](toolbar-icons/Std_Open.png) [Open…](#button-std_open) **L**; ![Save](toolbar-icons/Std_Save.png) [Save](#button-std_save) **L**; ![Save As…](toolbar-icons/Std_SaveAs.png) [Save As…](#button-std_saveas) **S**; ![Import…](toolbar-icons/Std_Import.png) [Import…](#button-std_import) **S**; ![Export…](toolbar-icons/Std_Export.png) [Export…](#button-std_export) **S** |
| Edit | ![Undo](toolbar-icons/Std_Undo.png) [Undo](#button-std_undo) **S**; ![Redo](toolbar-icons/Std_Redo.png) [Redo](#button-std_redo) **S**; ![Delete](toolbar-icons/Std_Delete.png) [Delete](#button-std_delete) **S**; ![Recompute](toolbar-icons/Std_Refresh.png) [Recompute](#button-std_refresh) **S**; ![Preferences](toolbar-icons/Std_DlgPreferences.png) [Preferences](#button-std_dlgpreferences) **S** |
| Clipboard | ![Cut](toolbar-icons/Std_Cut.png) [Cut](#button-std_cut) **S**; ![Copy](toolbar-icons/Std_Copy.png) [Copy](#button-std_copy) **S**; ![Paste](toolbar-icons/Std_Paste.png) [Paste](#button-std_paste) **S** |
| Structure | ![Components](toolbar-icons/Std_ComponentStructure.png) [Components](#button-std_componentstructure) **S**; ![Add Component](toolbar-icons/Std_Part.png) [Add part](#button-std_part) **L**; ![Coordinate System](toolbar-icons/Part_Datums.png) [Coordinate System](#button-part_datums) **S** **▼**; ![New Group](toolbar-icons/Std_Group.png) [New Group](#button-std_group) **S**; ![Make Link](toolbar-icons/Std_LinkActions.png) [Make Link](#button-std_linkactions) **S** **▼**; ![Variable Set](toolbar-icons/Std_VarSet.png) [Variable Set](#button-std_varset) **S**; ![Add Reference Object](toolbar-icons/PartDesign_AddReferenceObject.png) [Add Reference Object](#button-partdesign_addreferenceobject) **S** |
| Sketch | ![New Sketch](toolbar-icons/PartDesign_NewSketch.png) [New Sketch](#button-partdesign_newsketch) **L**; ![Attach Sketch](toolbar-icons/Sketcher_MapSketch.png) [Attach Sketch](#button-sketcher_mapsketch) **S**; ![Edit Sketch](toolbar-icons/Sketcher_EditSketch.png) [Edit Sketch](#button-sketcher_editsketch) **L**; ![Validate Sketch](toolbar-icons/Sketcher_ValidateSketch.png) [Validate Sketch](#button-sketcher_validatesketch) **S** |
| Tools | ![Command search...](../../../src/Gui/Icons/zoom-in.svg) [Command search...](#button-std_commandsearch) **S**; ![Measure](toolbar-icons/Std_Measure.png) [Measure](#button-std_measure) **S**; ![Mass Properties](toolbar-icons/Std_MassProperties.png) [Mass Properties](#button-std_massproperties) **S** |
| Help | Help dropdown → ![What's This?](toolbar-icons/Std_WhatsThis.png) [What's This?](#button-std_whatsthis) |
| Macro | Macro dropdown → ![Record Macro](toolbar-icons/Std_DlgMacroRecord.png) [Record Macro](#button-std_dlgmacrorecord); ![Macros](toolbar-icons/Std_DlgMacroExecute.png) [Macros](#button-std_dlgmacroexecute); ![Execute Macro](toolbar-icons/Std_DlgMacroExecuteDirect.png) [Execute Macro](#button-std_dlgmacroexecutedirect) |

**View tab** (shared projection of each active workbench's native View / Individual Views groups):

| Section / toolbar group | Buttons in display order |
| --- | --- |
| View | ![Fit All](toolbar-icons/Std_ViewFitAll.png) [Fit All](#button-std_viewfitall) **L**; ![Fit Selection](toolbar-icons/Std_ViewFitSelection.png) [Fit Selection](#button-std_viewfitselection) **S**; ![Isometric](toolbar-icons/Std_ViewGroup.png) [Isometric](#button-std_viewgroup) **S** **▼**; ![Align to Selection](toolbar-icons/Std_AlignToSelection.png) [Align to Selection](#button-std_aligntoselection) **S**; ![As Is](toolbar-icons/Std_DrawStyle.png) [As Is](#button-std_drawstyle) **S** **▼**; ![Vertex Selection](toolbar-icons/Part_SelectFilter.png) [Vertex Selection](#button-part_selectfilter) **S** **▼**; ![Measure](toolbar-icons/Std_Measure.png) [Measure](#button-std_measure) **S**; ![Mass Properties](toolbar-icons/Std_MassProperties.png) [Mass Properties](#button-std_massproperties) **S** |
| Individual Views | ![Isometric](toolbar-icons/Std_ViewIsometric.png) [Isometric](#button-std_viewisometric) **S**; ![Front](toolbar-icons/Std_ViewFront.png) [Front](#button-std_viewfront) **S**; ![Top](toolbar-icons/Std_ViewTop.png) [Top](#button-std_viewtop) **S**; ![Right](toolbar-icons/Std_ViewRight.png) [Right](#button-std_viewright) **S**; ![Rear](toolbar-icons/Std_ViewRear.png) [Rear](#button-std_viewrear) **S**; ![Bottom](toolbar-icons/Std_ViewBottom.png) [Bottom](#button-std_viewbottom) **S**; ![Left](toolbar-icons/Std_ViewLeft.png) [Left](#button-std_viewleft) **S** |
| Display | ![Selection filters…](../../../src/Gui/Icons/view-select.svg) [Selection filters…](#button-std_entityselectionfilter) **S**; ![Toolbars](../../../src/Gui/Icons/preferences-workbenches.svg) [Toolbars](#button-std_toolbarmenu) **S**; ![Panels](../../../src/Gui/Icons/Std_ToggleBottomPanels.svg) [Panels](#button-std_dockviewmenu) **S**; ![Status Bar](../../../src/Gui/Icons/info.svg) [Status Bar](#button-std_viewstatusbar) **S** |

## Workbench comparisons

Design tabs are **Home → Modeling → Surface → Sketch → Mesh → View**. Part Design supplies Home/Modeling; Surface, Sketcher and Mesh supply their namesake tabs. Other registered modes use **Home → Tools → View**. Part is a separate mode with its native operation groups under Tools; it is not a separate Design tab.

<a id="workbench-partdesignworkbench"></a>
### Part Design (`PartDesignWorkbench`)

Definition: [`src/Mod/PartDesign/Gui/Workbench.cpp`](../../../src/Mod/PartDesign/Gui/Workbench.cpp). Shared Classic groups are listed once above.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Part Design Helper Features | ![New Body](toolbar-icons/PartDesign_Body.png) [New Body](#button-partdesign_body); ![New Sketch](toolbar-icons/PartDesign_CompSketches.png) [New Sketch](#button-partdesign_compsketches); ![Validate Sketch](toolbar-icons/Sketcher_ValidateSketch.png) [Validate Sketch](#button-sketcher_validatesketch); ![Check Geometry](toolbar-icons/Part_CheckGeometry.png) [Check Geometry](#button-part_checkgeometry); ![Sub-Shape Binder](toolbar-icons/PartDesign_SubShapeBinder.png) [Sub-Shape Binder](#button-partdesign_subshapebinder); ![Clone](toolbar-icons/PartDesign_Clone.png) [Clone](#button-partdesign_clone) |
| Part Design Modeling Features | ![Pad](toolbar-icons/PartDesign_Pad.png) [Pad](#button-partdesign_pad); ![Revolve](toolbar-icons/PartDesign_Revolution.png) [Revolve](#button-partdesign_revolution); ![Additive Loft](toolbar-icons/PartDesign_AdditiveLoft.png) [Additive Loft](#button-partdesign_additiveloft); ![Additive Pipe](toolbar-icons/PartDesign_AdditivePipe.png) [Additive Pipe](#button-partdesign_additivepipe); ![Additive Helix](toolbar-icons/PartDesign_AdditiveHelix.png) [Additive Helix](#button-partdesign_additivehelix); ![Additive Box](toolbar-icons/PartDesign_CompPrimitiveAdditive.png) [Additive Box](#button-partdesign_compprimitiveadditive);  · ; ![Pocket](toolbar-icons/PartDesign_Pocket.png) [Pocket](#button-partdesign_pocket); ![Hole](toolbar-icons/PartDesign_Hole.png) [Hole](#button-partdesign_hole); ![Groove](toolbar-icons/PartDesign_Groove.png) [Groove](#button-partdesign_groove); ![Subtractive Loft](toolbar-icons/PartDesign_SubtractiveLoft.png) [Subtractive Loft](#button-partdesign_subtractiveloft); ![Subtractive Pipe](toolbar-icons/PartDesign_SubtractivePipe.png) [Subtractive Pipe](#button-partdesign_subtractivepipe); ![Subtractive Helix](toolbar-icons/PartDesign_SubtractiveHelix.png) [Subtractive Helix](#button-partdesign_subtractivehelix); ![Subtractive Box](toolbar-icons/PartDesign_CompPrimitiveSubtractive.png) [Subtractive Box](#button-partdesign_compprimitivesubtractive);  · ; ![Boolean Operation](toolbar-icons/PartDesign_Boolean.png) [Boolean Operation](#button-partdesign_boolean) |
| Part Design Dress-Up Features | ![Fillet](toolbar-icons/PartDesign_Fillet.png) [Fillet](#button-partdesign_fillet); ![Chamfer](toolbar-icons/PartDesign_Chamfer.png) [Chamfer](#button-partdesign_chamfer); ![Draft](toolbar-icons/PartDesign_Draft.png) [Draft](#button-partdesign_draft); ![Thickness](toolbar-icons/PartDesign_Thickness.png) [Thickness](#button-partdesign_thickness); ![Defeaturing](toolbar-icons/PartDesign_Defeaturing.png) [Defeaturing](#button-partdesign_defeaturing) |
| Part Design Transformation Features | ![Mirror](toolbar-icons/PartDesign_Mirrored.png) [Mirror](#button-partdesign_mirrored); ![Linear Pattern](toolbar-icons/PartDesign_LinearPattern.png) [Linear Pattern](#button-partdesign_linearpattern); ![Polar Pattern](toolbar-icons/PartDesign_PolarPattern.png) [Polar Pattern](#button-partdesign_polarpattern); ![Circular Pattern](../../../src/Mod/PartDesign/Gui/Resources/icons/PartDesign_CircularPattern.svg) [Circular Pattern](#button-partdesign_circularpattern); ![Path Pattern](../../../src/Mod/PartDesign/Gui/Resources/icons/PartDesign_PathPattern.svg) [Path Pattern](#button-partdesign_pathpattern); ![Point Pattern](../../../src/Mod/PartDesign/Gui/Resources/icons/PartDesign_PointPattern.svg) [Point Pattern](#button-partdesign_pointpattern); ![Multi-Transform](toolbar-icons/PartDesign_MultiTransform.png) [Multi-Transform](#button-partdesign_multitransform) |

#### Changes made / buttons consolidated or omitted

- ![Pad](toolbar-icons/PartDesign_Pad.png) [Pad](#button-partdesign_pad) + ![Pocket](toolbar-icons/PartDesign_Pocket.png) [Pocket](#button-partdesign_pocket) → ![Extrude](toolbar-icons/PartDesign_Extrude.png) [Extrude](#button-partdesign_extrude). Add/Subtract is selected in the task pane; the component workflow also supports separate background solid results.
- ![Linear Pattern](toolbar-icons/PartDesign_LinearPattern.png) [Linear Pattern](#button-partdesign_linearpattern), ![Polar Pattern](toolbar-icons/PartDesign_PolarPattern.png) [Polar Pattern](#button-partdesign_polarpattern), ![Circular Pattern](../../../src/Mod/PartDesign/Gui/Resources/icons/PartDesign_CircularPattern.svg) [Circular Pattern](#button-partdesign_circularpattern), ![Path Pattern](../../../src/Mod/PartDesign/Gui/Resources/icons/PartDesign_PathPattern.svg) [Path Pattern](#button-partdesign_pathpattern), ![Point Pattern](../../../src/Mod/PartDesign/Gui/Resources/icons/PartDesign_PointPattern.svg) [Point Pattern](#button-partdesign_pointpattern) share ![Pattern](toolbar-icons/PartDesign_Pattern.png) [Pattern](#button-partdesign_pattern) as the primary ribbon entry. The unified task offers linear/circular patterns; the dropdown adds native concentric Circular, Path and Point tasks. The audit correction restores their upstream commands and view providers in source, without changing geometry. Those three bindings remain pending native rebuild/GUI validation in the inspected executable. Classic exposes their individual native buttons; Mirrored and MultiTransform remain separate buttons.
- Additive/Subtractive Loft, Pipe and Helix each share one dropdown. Both variants remain selectable.
- Added to native toolbar definitions: ![Add Reference Object](toolbar-icons/PartDesign_AddReferenceObject.png) [Add Reference Object](#button-partdesign_addreferenceobject); ![Extrude](toolbar-icons/PartDesign_Extrude.png) [Extrude](#button-partdesign_extrude); ![Pattern](toolbar-icons/PartDesign_Pattern.png) [Pattern](#button-partdesign_pattern); ![Isocline Curve](toolbar-icons/Part_IsoclineCurve.png) [Isocline Curve](#button-part_isoclinecurve); ![Trim Body](toolbar-icons/Part_TrimBody.png) [Trim Body](#button-part_trimbody).

#### Plus UI tabs and sections

**Home:** shared sections above.

**Design → Modeling**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Part Design Modeling Features | ![Extrude](toolbar-icons/PartDesign_Extrude.png) [Extrude](#button-partdesign_extrude) **L**; ![Add Reference Object](toolbar-icons/PartDesign_AddReferenceObject.png) [Add Reference Object](#button-partdesign_addreferenceobject) **S**; ![Revolve](toolbar-icons/PartDesign_Revolution.png) [Revolve](#button-partdesign_revolution) **L**; ![Additive Loft](toolbar-icons/PartDesign_AdditiveLoft.png) [Additive Loft](#button-partdesign_additiveloft) **S** **▼** {![Additive Loft](toolbar-icons/PartDesign_AdditiveLoft.png) [Additive Loft](#button-partdesign_additiveloft); ![Subtractive Loft](toolbar-icons/PartDesign_SubtractiveLoft.png) [Subtractive Loft](#button-partdesign_subtractiveloft)}; ![Additive Pipe](toolbar-icons/PartDesign_AdditivePipe.png) [Additive Pipe](#button-partdesign_additivepipe) **S** **▼** {![Additive Pipe](toolbar-icons/PartDesign_AdditivePipe.png) [Additive Pipe](#button-partdesign_additivepipe); ![Subtractive Pipe](toolbar-icons/PartDesign_SubtractivePipe.png) [Subtractive Pipe](#button-partdesign_subtractivepipe)}; ![Additive Helix](toolbar-icons/PartDesign_AdditiveHelix.png) [Additive Helix](#button-partdesign_additivehelix) **S** **▼** {![Additive Helix](toolbar-icons/PartDesign_AdditiveHelix.png) [Additive Helix](#button-partdesign_additivehelix); ![Subtractive Helix](toolbar-icons/PartDesign_SubtractiveHelix.png) [Subtractive Helix](#button-partdesign_subtractivehelix)}; ![Additive Box](toolbar-icons/PartDesign_CompPrimitiveAdditive.png) [Additive Box](#button-partdesign_compprimitiveadditive) **S** **▼**; ![Hole](toolbar-icons/PartDesign_Hole.png) [Hole](#button-partdesign_hole) **S**; ![Groove](toolbar-icons/PartDesign_Groove.png) [Groove](#button-partdesign_groove) **S**; ![Subtractive Box](toolbar-icons/PartDesign_CompPrimitiveSubtractive.png) [Subtractive Box](#button-partdesign_compprimitivesubtractive) **S** **▼**; ![Boolean Operation](toolbar-icons/PartDesign_Boolean.png) [Boolean Operation](#button-partdesign_boolean) **S**; ![Isocline Curve](toolbar-icons/Part_IsoclineCurve.png) [Isocline Curve](#button-part_isoclinecurve) **S**; ![Trim Body](toolbar-icons/Part_TrimBody.png) [Trim Body](#button-part_trimbody) **S** |
| Part Design Transformation Features | ![Mirror](toolbar-icons/PartDesign_Mirrored.png) [Mirror](#button-partdesign_mirrored) **S**; ![Pattern](toolbar-icons/PartDesign_Pattern.png) [Pattern](#button-partdesign_pattern) **L** **▼** {![Pattern](toolbar-icons/PartDesign_Pattern.png) [Pattern](#button-partdesign_pattern); ![Circular Pattern](../../../src/Mod/PartDesign/Gui/Resources/icons/PartDesign_CircularPattern.svg) [Circular Pattern](#button-partdesign_circularpattern); ![Path Pattern](../../../src/Mod/PartDesign/Gui/Resources/icons/PartDesign_PathPattern.svg) [Path Pattern](#button-partdesign_pathpattern); ![Point Pattern](../../../src/Mod/PartDesign/Gui/Resources/icons/PartDesign_PointPattern.svg) [Point Pattern](#button-partdesign_pointpattern)}; ![Multi-Transform](toolbar-icons/PartDesign_MultiTransform.png) [Multi-Transform](#button-partdesign_multitransform) **S** |
| Part Design Dress-Up Features | ![Fillet](toolbar-icons/PartDesign_Fillet.png) [Fillet](#button-partdesign_fillet) **L**; ![Chamfer](toolbar-icons/PartDesign_Chamfer.png) [Chamfer](#button-partdesign_chamfer) **S**; ![Draft](toolbar-icons/PartDesign_Draft.png) [Draft](#button-partdesign_draft) **S**; ![Thickness](toolbar-icons/PartDesign_Thickness.png) [Thickness](#button-partdesign_thickness) **S**; ![Defeaturing](toolbar-icons/PartDesign_Defeaturing.png) [Defeaturing](#button-partdesign_defeaturing) **S** |
| Part Design Helper Features | ![New Body](toolbar-icons/PartDesign_Body.png) [New Body](#button-partdesign_body) **S**; ![New Sketch](toolbar-icons/PartDesign_CompSketches.png) [New Sketch](#button-partdesign_compsketches) **S** **▼**; ![Validate Sketch](toolbar-icons/Sketcher_ValidateSketch.png) [Validate Sketch](#button-sketcher_validatesketch) **S**; ![Check Geometry](toolbar-icons/Part_CheckGeometry.png) [Check Geometry](#button-part_checkgeometry) **S**; ![Sub-Shape Binder](toolbar-icons/PartDesign_SubShapeBinder.png) [Sub-Shape Binder](#button-partdesign_subshapebinder) **S**; ![Clone](toolbar-icons/PartDesign_Clone.png) [Clone](#button-partdesign_clone) **S** |

**View:** shared sections above.

<a id="workbench-partworkbench"></a>
### Part (`PartWorkbench`)

Definition: [`src/Mod/Part/Gui/Workbench.cpp`](../../../src/Mod/Part/Gui/Workbench.cpp). Shared Classic groups are listed once above.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Solids | ![Cube](toolbar-icons/Part_Box.png) [Cube](#button-part_box); ![Cylinder](toolbar-icons/Part_Cylinder.png) [Cylinder](#button-part_cylinder); ![Sphere](toolbar-icons/Part_Sphere.png) [Sphere](#button-part_sphere); ![Cone](toolbar-icons/Part_Cone.png) [Cone](#button-part_cone); ![Torus](toolbar-icons/Part_Torus.png) [Torus](#button-part_torus); ![Tube](toolbar-icons/Part_Tube.png) [Tube](#button-part_tube); ![Primitive](toolbar-icons/Part_Primitives.png) [Primitive](#button-part_primitives); ![Shape Builder](toolbar-icons/Part_Builder.png) [Shape Builder](#button-part_builder) |
| Part Tools | ![New Sketch](toolbar-icons/Sketcher_NewSketch.png) [New Sketch](#button-sketcher_newsketch); ![Extrude](toolbar-icons/Part_Extrude.png) [Extrude](#button-part_extrude); ![Revolve](toolbar-icons/Part_Revolve.png) [Revolve](#button-part_revolve); ![Mirror](toolbar-icons/Part_Mirror.png) [Mirror](#button-part_mirror); ![Scale](toolbar-icons/Part_Scale.png) [Scale](#button-part_scale); ![Fillet](toolbar-icons/Part_Fillet.png) [Fillet](#button-part_fillet); ![Chamfer](toolbar-icons/Part_Chamfer.png) [Chamfer](#button-part_chamfer); ![Face From Wires](toolbar-icons/Part_MakeFace.png) [Face From Wires](#button-part_makeface); ![Ruled Surface](toolbar-icons/Part_RuledSurface.png) [Ruled Surface](#button-part_ruledsurface); ![Loft](toolbar-icons/Part_Loft.png) [Loft](#button-part_loft); ![Sweep](toolbar-icons/Part_Sweep.png) [Sweep](#button-part_sweep); ![Section](toolbar-icons/Part_Section.png) [Section](#button-part_section); ![Cross-Sections](toolbar-icons/Part_CrossSections.png) [Cross-Sections](#button-part_crosssections); ![3D Offset](toolbar-icons/Part_CompOffset.png) [3D Offset](#button-part_compoffset); ![Thickness](toolbar-icons/Part_Thickness.png) [Thickness](#button-part_thickness); ![Project on Surface](toolbar-icons/Part_ProjectionOnSurface.png) [Project on Surface](#button-part_projectiononsurface); ![Appearance per Face](toolbar-icons/Part_ColorPerFace.png) [Appearance per Face](#button-part_colorperface) |
| Boolean Tools | ![Compound](toolbar-icons/Part_CompCompoundTools.png) [Compound](#button-part_compcompoundtools); ![Boolean Operation](toolbar-icons/Part_Boolean.png) [Boolean Operation](#button-part_boolean); ![Cut](toolbar-icons/Part_Cut.png) [Cut](#button-part_cut); ![Union](toolbar-icons/Part_Fuse.png) [Union](#button-part_fuse); ![Intersection](toolbar-icons/Part_Common.png) [Intersection](#button-part_common); ![Connect Shapes](toolbar-icons/Part_CompJoinFeatures.png) [Connect Shapes](#button-part_compjoinfeatures); ![Boolean Fragments](toolbar-icons/Part_CompSplitFeatures.png) [Boolean Fragments](#button-part_compsplitfeatures); ![Check Geometry](toolbar-icons/Part_CheckGeometry.png) [Check Geometry](#button-part_checkgeometry); ![Defeaturing](toolbar-icons/Part_Defeaturing.png) [Defeaturing](#button-part_defeaturing) |

#### Changes made / buttons consolidated or omitted

- Added to native toolbar definitions: ![Add Reference Object](toolbar-icons/PartDesign_AddReferenceObject.png) [Add Reference Object](#button-partdesign_addreferenceobject); ![Isocline Curve](toolbar-icons/Part_IsoclineCurve.png) [Isocline Curve](#button-part_isoclinecurve); ![Trim Body](toolbar-icons/Part_TrimBody.png) [Trim Body](#button-part_trimbody).

#### Plus UI tabs and sections

**Home:** shared sections above; Home excludes the Design-only Sketch and Tools sections.

**Part → Tools**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Solids | ![Cube](toolbar-icons/Part_Box.png) [Cube](#button-part_box) **S**; ![Cylinder](toolbar-icons/Part_Cylinder.png) [Cylinder](#button-part_cylinder) **S**; ![Sphere](toolbar-icons/Part_Sphere.png) [Sphere](#button-part_sphere) **S**; ![Cone](toolbar-icons/Part_Cone.png) [Cone](#button-part_cone) **S**; ![Torus](toolbar-icons/Part_Torus.png) [Torus](#button-part_torus) **S**; ![Tube](toolbar-icons/Part_Tube.png) [Tube](#button-part_tube) **S**; ![Primitive](toolbar-icons/Part_Primitives.png) [Primitive](#button-part_primitives) **S**; ![Shape Builder](toolbar-icons/Part_Builder.png) [Shape Builder](#button-part_builder) **S** |
| Part Tools | ![New Sketch](toolbar-icons/Sketcher_NewSketch.png) [New Sketch](#button-sketcher_newsketch) **L**; ![Extrude](toolbar-icons/Part_Extrude.png) [Extrude](#button-part_extrude) **S**; ![Add Reference Object](toolbar-icons/PartDesign_AddReferenceObject.png) [Add Reference Object](#button-partdesign_addreferenceobject) **S**; ![Revolve](toolbar-icons/Part_Revolve.png) [Revolve](#button-part_revolve) **S**; ![Mirror](toolbar-icons/Part_Mirror.png) [Mirror](#button-part_mirror) **S**; ![Scale](toolbar-icons/Part_Scale.png) [Scale](#button-part_scale) **S**; ![Fillet](toolbar-icons/Part_Fillet.png) [Fillet](#button-part_fillet) **S**; ![Chamfer](toolbar-icons/Part_Chamfer.png) [Chamfer](#button-part_chamfer) **S**; ![Face From Wires](toolbar-icons/Part_MakeFace.png) [Face From Wires](#button-part_makeface) **S**; ![Ruled Surface](toolbar-icons/Part_RuledSurface.png) [Ruled Surface](#button-part_ruledsurface) **S**; ![Loft](toolbar-icons/Part_Loft.png) [Loft](#button-part_loft) **S**; ![Sweep](toolbar-icons/Part_Sweep.png) [Sweep](#button-part_sweep) **S**; ![Section](toolbar-icons/Part_Section.png) [Section](#button-part_section) **S**; ![Cross-Sections](toolbar-icons/Part_CrossSections.png) [Cross-Sections](#button-part_crosssections) **S**; ![3D Offset](toolbar-icons/Part_CompOffset.png) [3D Offset](#button-part_compoffset) **S** **▼**; ![Thickness](toolbar-icons/Part_Thickness.png) [Thickness](#button-part_thickness) **S**; ![Project on Surface](toolbar-icons/Part_ProjectionOnSurface.png) [Project on Surface](#button-part_projectiononsurface) **S**; ![Isocline Curve](toolbar-icons/Part_IsoclineCurve.png) [Isocline Curve](#button-part_isoclinecurve) **S**; ![Appearance per Face](toolbar-icons/Part_ColorPerFace.png) [Appearance per Face](#button-part_colorperface) **S** |
| Boolean Tools | ![Compound](toolbar-icons/Part_CompCompoundTools.png) [Compound](#button-part_compcompoundtools) **S** **▼**; ![Boolean Operation](toolbar-icons/Part_Boolean.png) [Boolean Operation](#button-part_boolean) **S**; ![Cut](toolbar-icons/Part_Cut.png) [Cut](#button-part_cut) **S**; ![Union](toolbar-icons/Part_Fuse.png) [Union](#button-part_fuse) **S**; ![Intersection](toolbar-icons/Part_Common.png) [Intersection](#button-part_common) **S**; ![Trim Body](toolbar-icons/Part_TrimBody.png) [Trim Body](#button-part_trimbody) **S**; ![Connect Shapes](toolbar-icons/Part_CompJoinFeatures.png) [Connect Shapes](#button-part_compjoinfeatures) **S** **▼**; ![Boolean Fragments](toolbar-icons/Part_CompSplitFeatures.png) [Boolean Fragments](#button-part_compsplitfeatures) **S** **▼**; ![Check Geometry](toolbar-icons/Part_CheckGeometry.png) [Check Geometry](#button-part_checkgeometry) **S**; ![Defeaturing](toolbar-icons/Part_Defeaturing.png) [Defeaturing](#button-part_defeaturing) **S** |

**View:** shared sections above.

<a id="workbench-sketcherworkbench"></a>
### Sketcher (`SketcherWorkbench`)

Definition: [`src/Mod/Sketcher/Gui/Workbench.cpp`](../../../src/Mod/Sketcher/Gui/Workbench.cpp). Shared Classic groups are listed once above.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Sketcher | ![New Sketch](toolbar-icons/Sketcher_NewSketch.png) [New Sketch](#button-sketcher_newsketch); ![Edit Sketch](toolbar-icons/Sketcher_EditSketch.png) [Edit Sketch](#button-sketcher_editsketch); ![Attach Sketch](toolbar-icons/Sketcher_MapSketch.png) [Attach Sketch](#button-sketcher_mapsketch); ![Reorient Sketch](toolbar-icons/Sketcher_ReorientSketch.png) [Reorient Sketch](#button-sketcher_reorientsketch); ![Validate Sketch](toolbar-icons/Sketcher_ValidateSketch.png) [Validate Sketch](#button-sketcher_validatesketch); ![Merge Sketches](toolbar-icons/Sketcher_MergeSketches.png) [Merge Sketches](#button-sketcher_mergesketches); ![Mirror Sketch](toolbar-icons/Sketcher_MirrorSketch.png) [Mirror Sketch](#button-sketcher_mirrorsketch) |
| Edit Mode | ![Leave Sketch](toolbar-icons/Sketcher_LeaveSketch.png) [Leave Sketch](#button-sketcher_leavesketch); ![Align View to Sketch](toolbar-icons/Sketcher_ViewSketch.png) [Align View to Sketch](#button-sketcher_viewsketch); ![Toggle Section View](toolbar-icons/Sketcher_ViewSection.png) [Toggle Section View](#button-sketcher_viewsection) |
| Geometries | ![Point](toolbar-icons/Sketcher_CreatePoint.png) [Point](#button-sketcher_createpoint); ![Polyline](toolbar-icons/Sketcher_CompLine.png) [Polyline](#button-sketcher_compline); ![Arc From Center](toolbar-icons/Sketcher_CompCreateArc.png) [Arc From Center](#button-sketcher_compcreatearc); ![Circle From Center](toolbar-icons/Sketcher_CompCreateConic.png) [Circle From Center](#button-sketcher_compcreateconic); ![Rectangle](toolbar-icons/Sketcher_CompCreateRectangles.png) [Rectangle](#button-sketcher_compcreaterectangles); ![Triangle](toolbar-icons/Sketcher_CompCreateRegularPolygon.png) [Triangle](#button-sketcher_compcreateregularpolygon); ![Slot](toolbar-icons/Sketcher_CompSlot.png) [Slot](#button-sketcher_compslot); ![B-Spline](toolbar-icons/Sketcher_CompCreateBSpline.png) [B-Spline](#button-sketcher_compcreatebspline); ![Text (Experimental)](toolbar-icons/Sketcher_CreateText.png) [Text (Experimental)](#button-sketcher_createtext);  · ; ![Toggle Construction Geometry](toolbar-icons/Sketcher_ToggleConstruction.png) [Toggle Construction Geometry](#button-sketcher_toggleconstruction) |
| Constraints | ![Dimension](toolbar-icons/Sketcher_CompDimensionTools.png) [Dimension](#button-sketcher_compdimensiontools);  · ; ![Coincident Constraint](toolbar-icons/Sketcher_ConstrainCoincidentUnified.png) [Coincident Constraint](#button-sketcher_constraincoincidentunified); ![Horizontal Constraint](toolbar-icons/Sketcher_CompHorVer.png) [Horizontal Constraint](#button-sketcher_comphorver); ![Parallel Constraint](toolbar-icons/Sketcher_ConstrainParallel.png) [Parallel Constraint](#button-sketcher_constrainparallel); ![Perpendicular Constraint](toolbar-icons/Sketcher_ConstrainPerpendicular.png) [Perpendicular Constraint](#button-sketcher_constrainperpendicular); ![Tangent/Collinear Constraint](toolbar-icons/Sketcher_ConstrainTangent.png) [Tangent/Collinear Constraint](#button-sketcher_constraintangent); ![Equal Constraint](toolbar-icons/Sketcher_ConstrainEqual.png) [Equal Constraint](#button-sketcher_constrainequal); ![Symmetric Constraint](toolbar-icons/Sketcher_ConstrainSymmetric.png) [Symmetric Constraint](#button-sketcher_constrainsymmetric); ![Block Constraint](toolbar-icons/Sketcher_ConstrainBlock.png) [Block Constraint](#button-sketcher_constrainblock); ![Group Constraint (Development preview)](toolbar-icons/Sketcher_ConstrainGroup.png) [Group Constraint (Development preview)](#button-sketcher_constraingroup);  · ; ![Toggle Driving/Reference Constraints](toolbar-icons/Sketcher_CompToggleConstraints.png) [Toggle Driving/Reference Constraints](#button-sketcher_comptoggleconstraints) |
| Sketcher Tools | ![Fillet](toolbar-icons/Sketcher_CompCreateFillets.png) [Fillet](#button-sketcher_compcreatefillets); ![Trim Edge](toolbar-icons/Sketcher_CompCurveEdition.png) [Trim Edge](#button-sketcher_compcurveedition); ![External Projection](toolbar-icons/Sketcher_CompExternal.png) [External Projection](#button-sketcher_compexternal); ![Carbon Copy](toolbar-icons/Sketcher_CarbonCopy.png) [Carbon Copy](#button-sketcher_carboncopy);  · ; ![Move / Array Transform](toolbar-icons/Sketcher_Translate.png) [Move / Array Transform](#button-sketcher_translate); ![Rotate / Polar Transform](toolbar-icons/Sketcher_Rotate.png) [Rotate / Polar Transform](#button-sketcher_rotate); ![Scale](toolbar-icons/Sketcher_Scale.png) [Scale](#button-sketcher_scale); ![Offset](toolbar-icons/Sketcher_Offset.png) [Offset](#button-sketcher_offset); ![Mirror](toolbar-icons/Sketcher_Symmetry.png) [Mirror](#button-sketcher_symmetry); ![Remove Axes Alignment](toolbar-icons/Sketcher_RemoveAxesAlignment.png) [Remove Axes Alignment](#button-sketcher_removeaxesalignment) |
| B-Spline Tools | ![Geometry to B-Spline](toolbar-icons/Sketcher_BSplineConvertToNURBS.png) [Geometry to B-Spline](#button-sketcher_bsplineconverttonurbs); ![Increase B-Spline Degree](toolbar-icons/Sketcher_BSplineIncreaseDegree.png) [Increase B-Spline Degree](#button-sketcher_bsplineincreasedegree); ![Decrease B-Spline Degree](toolbar-icons/Sketcher_BSplineDecreaseDegree.png) [Decrease B-Spline Degree](#button-sketcher_bsplinedecreasedegree); ![Increase knot multiplicity](toolbar-icons/Sketcher_CompModifyKnotMultiplicity.png) [Increase knot multiplicity](#button-sketcher_compmodifyknotmultiplicity); ![Insert Knot](toolbar-icons/Sketcher_BSplineInsertKnot.png) [Insert Knot](#button-sketcher_bsplineinsertknot); ![Join Curves](toolbar-icons/Sketcher_JoinCurves.png) [Join Curves](#button-sketcher_joincurves) |
| Visual Helpers | ![Select Associated Constraints](toolbar-icons/Sketcher_SelectConstraints.png) [Select Associated Constraints](#button-sketcher_selectconstraints); ![Select Associated Geometry](toolbar-icons/Sketcher_SelectElementsAssociatedWithConstraints.png) [Select Associated Geometry](#button-sketcher_selectelementsassociatedwithconstraints);  · ; ![Toggle Circular Helper for Arcs](toolbar-icons/Sketcher_ArcOverlay.png) [Toggle Circular Helper for Arcs](#button-sketcher_arcoverlay); ![Toggle B-Spline Degree](toolbar-icons/Sketcher_CompBSplineShowHideGeometryInformation.png) [Toggle B-Spline Degree](#button-sketcher_compbsplineshowhidegeometryinformation); ![Toggle Internal Geometry](toolbar-icons/Sketcher_RestoreInternalAlignmentGeometry.png) [Toggle Internal Geometry](#button-sketcher_restoreinternalalignmentgeometry); ![Switch Virtual Space](toolbar-icons/Sketcher_SwitchVirtualSpace.png) [Switch Virtual Space](#button-sketcher_switchvirtualspace) |

#### Changes made / buttons consolidated or omitted

- Dimension buttons are consolidated under large Auto Dimension, with vertical, horizontal, angle, radius, diameter, distance, radius/diameter, lock and Snell's-law choices. Native geometry/B-spline/constraint compound dropdowns remain native.
- Sketch support review, reusable copy and constraint-repair review are menu additions, not new buttons in the upstream Sketcher toolbar groups.
- No workbench-specific toolbar command removal found in the compared definitions; Plus changes presentation/routing and applies the shared Home/View rules above.

#### Plus UI tabs and sections

**Design → Sketch**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Sketcher | ![New Sketch](toolbar-icons/Sketcher_NewSketch.png) [New Sketch](#button-sketcher_newsketch) **L**; ![Edit Sketch](toolbar-icons/Sketcher_EditSketch.png) [Edit Sketch](#button-sketcher_editsketch) **L**; ![Attach Sketch](toolbar-icons/Sketcher_MapSketch.png) [Attach Sketch](#button-sketcher_mapsketch) **S**; ![Reorient Sketch](toolbar-icons/Sketcher_ReorientSketch.png) [Reorient Sketch](#button-sketcher_reorientsketch) **S**; ![Validate Sketch](toolbar-icons/Sketcher_ValidateSketch.png) [Validate Sketch](#button-sketcher_validatesketch) **S**; ![Merge Sketches](toolbar-icons/Sketcher_MergeSketches.png) [Merge Sketches](#button-sketcher_mergesketches) **S**; ![Mirror Sketch](toolbar-icons/Sketcher_MirrorSketch.png) [Mirror Sketch](#button-sketcher_mirrorsketch) **S** |
| Edit Mode | ![Leave Sketch](toolbar-icons/Sketcher_LeaveSketch.png) [Leave Sketch](#button-sketcher_leavesketch) **S**; ![Align View to Sketch](toolbar-icons/Sketcher_ViewSketch.png) [Align View to Sketch](#button-sketcher_viewsketch) **S**; ![Toggle Section View](toolbar-icons/Sketcher_ViewSection.png) [Toggle Section View](#button-sketcher_viewsection) **S** |
| Geometries | ![Point](toolbar-icons/Sketcher_CreatePoint.png) [Point](#button-sketcher_createpoint) **S**; ![Polyline](toolbar-icons/Sketcher_CompLine.png) [Polyline](#button-sketcher_compline) **L** **▼**; ![Arc From Center](toolbar-icons/Sketcher_CompCreateArc.png) [Arc From Center](#button-sketcher_compcreatearc) **S** **▼**; ![Circle From Center](toolbar-icons/Sketcher_CompCreateConic.png) [Circle From Center](#button-sketcher_compcreateconic) **S** **▼**; ![Rectangle](toolbar-icons/Sketcher_CompCreateRectangles.png) [Rectangle](#button-sketcher_compcreaterectangles) **L** **▼**; ![Triangle](toolbar-icons/Sketcher_CompCreateRegularPolygon.png) [Triangle](#button-sketcher_compcreateregularpolygon) **S** **▼**; ![Slot](toolbar-icons/Sketcher_CompSlot.png) [Slot](#button-sketcher_compslot) **S** **▼**; ![B-Spline](toolbar-icons/Sketcher_CompCreateBSpline.png) [B-Spline](#button-sketcher_compcreatebspline) **S** **▼**; ![Text (Experimental)](toolbar-icons/Sketcher_CreateText.png) [Text (Experimental)](#button-sketcher_createtext) **S**; ![Toggle Construction Geometry](toolbar-icons/Sketcher_ToggleConstruction.png) [Toggle Construction Geometry](#button-sketcher_toggleconstruction) **S** |
| Constraints | ![Dimension](toolbar-icons/Sketcher_Dimension.png) [Auto Dimension](#button-sketcher_dimension) **L** **▼** {![Dimension](toolbar-icons/Sketcher_Dimension.png) [Auto Dimension](#button-sketcher_dimension); ![Vertical Dimension](toolbar-icons/Sketcher_ConstrainDistanceY.png) [Vertical Dimension](#button-sketcher_constraindistancey); ![Horizontal Dimension](toolbar-icons/Sketcher_ConstrainDistanceX.png) [Horizontal Dimension](#button-sketcher_constraindistancex); ![Angle Dimension](toolbar-icons/Sketcher_ConstrainAngle.png) [Angle Dimension](#button-sketcher_constrainangle); ![Radius Dimension](toolbar-icons/Sketcher_ConstrainRadius.png) [Radius Dimension](#button-sketcher_constrainradius); ![Diameter Dimension](toolbar-icons/Sketcher_ConstrainDiameter.png) [Diameter Dimension](#button-sketcher_constraindiameter); ![Distance Dimension](toolbar-icons/Sketcher_ConstrainDistance.png) [Distance Dimension](#button-sketcher_constraindistance); ![Radius/Diameter Dimension](toolbar-icons/Sketcher_ConstrainRadiam.png) [Radius/Diameter Dimension](#button-sketcher_constrainradiam); ![Lock Position](toolbar-icons/Sketcher_ConstrainLock.png) [Lock Position](#button-sketcher_constrainlock); ![Refraction Constraint](toolbar-icons/Sketcher_ConstrainSnellsLaw.png) [Refraction Constraint](#button-sketcher_constrainsnellslaw)}; ![Coincident Constraint](toolbar-icons/Sketcher_ConstrainCoincidentUnified.png) [Coincident Constraint](#button-sketcher_constraincoincidentunified) **S**; ![Horizontal Constraint](toolbar-icons/Sketcher_CompHorVer.png) [Horizontal Constraint](#button-sketcher_comphorver) **S** **▼**; ![Parallel Constraint](toolbar-icons/Sketcher_ConstrainParallel.png) [Parallel Constraint](#button-sketcher_constrainparallel) **S**; ![Perpendicular Constraint](toolbar-icons/Sketcher_ConstrainPerpendicular.png) [Perpendicular Constraint](#button-sketcher_constrainperpendicular) **S**; ![Tangent/Collinear Constraint](toolbar-icons/Sketcher_ConstrainTangent.png) [Tangent/Collinear Constraint](#button-sketcher_constraintangent) **S**; ![Equal Constraint](toolbar-icons/Sketcher_ConstrainEqual.png) [Equal Constraint](#button-sketcher_constrainequal) **S**; ![Symmetric Constraint](toolbar-icons/Sketcher_ConstrainSymmetric.png) [Symmetric Constraint](#button-sketcher_constrainsymmetric) **S**; ![Block Constraint](toolbar-icons/Sketcher_ConstrainBlock.png) [Block Constraint](#button-sketcher_constrainblock) **S**; ![Group Constraint (Development preview)](toolbar-icons/Sketcher_ConstrainGroup.png) [Group Constraint (Development preview)](#button-sketcher_constraingroup) **S**; ![Toggle Driving/Reference Constraints](toolbar-icons/Sketcher_CompToggleConstraints.png) [Toggle Driving/Reference Constraints](#button-sketcher_comptoggleconstraints) **S** **▼** |
| Sketcher Tools | ![Fillet](toolbar-icons/Sketcher_CompCreateFillets.png) [Fillet](#button-sketcher_compcreatefillets) **S** **▼**; ![Trim Edge](toolbar-icons/Sketcher_CompCurveEdition.png) [Trim Edge](#button-sketcher_compcurveedition) **S** **▼**; ![External Projection](toolbar-icons/Sketcher_CompExternal.png) [External Projection](#button-sketcher_compexternal) **S** **▼**; ![Carbon Copy](toolbar-icons/Sketcher_CarbonCopy.png) [Carbon Copy](#button-sketcher_carboncopy) **S**; ![Move / Array Transform](toolbar-icons/Sketcher_Translate.png) [Move / Array Transform](#button-sketcher_translate) **S**; ![Rotate / Polar Transform](toolbar-icons/Sketcher_Rotate.png) [Rotate / Polar Transform](#button-sketcher_rotate) **S**; ![Scale](toolbar-icons/Sketcher_Scale.png) [Scale](#button-sketcher_scale) **S**; ![Offset](toolbar-icons/Sketcher_Offset.png) [Offset](#button-sketcher_offset) **S**; ![Mirror](toolbar-icons/Sketcher_Symmetry.png) [Mirror](#button-sketcher_symmetry) **S**; ![Remove Axes Alignment](toolbar-icons/Sketcher_RemoveAxesAlignment.png) [Remove Axes Alignment](#button-sketcher_removeaxesalignment) **S** |
| B-Spline Tools | ![Geometry to B-Spline](toolbar-icons/Sketcher_BSplineConvertToNURBS.png) [Geometry to B-Spline](#button-sketcher_bsplineconverttonurbs) **S**; ![Increase B-Spline Degree](toolbar-icons/Sketcher_BSplineIncreaseDegree.png) [Increase B-Spline Degree](#button-sketcher_bsplineincreasedegree) **S**; ![Decrease B-Spline Degree](toolbar-icons/Sketcher_BSplineDecreaseDegree.png) [Decrease B-Spline Degree](#button-sketcher_bsplinedecreasedegree) **S**; ![Increase knot multiplicity](toolbar-icons/Sketcher_CompModifyKnotMultiplicity.png) [Increase knot multiplicity](#button-sketcher_compmodifyknotmultiplicity) **S** **▼**; ![Insert Knot](toolbar-icons/Sketcher_BSplineInsertKnot.png) [Insert Knot](#button-sketcher_bsplineinsertknot) **S**; ![Join Curves](toolbar-icons/Sketcher_JoinCurves.png) [Join Curves](#button-sketcher_joincurves) **S** |
| Visual Helpers | ![Select Associated Constraints](toolbar-icons/Sketcher_SelectConstraints.png) [Select Associated Constraints](#button-sketcher_selectconstraints) **S**; ![Select Associated Geometry](toolbar-icons/Sketcher_SelectElementsAssociatedWithConstraints.png) [Select Associated Geometry](#button-sketcher_selectelementsassociatedwithconstraints) **S**; ![Toggle Circular Helper for Arcs](toolbar-icons/Sketcher_ArcOverlay.png) [Toggle Circular Helper for Arcs](#button-sketcher_arcoverlay) **S**; ![Toggle B-Spline Degree](toolbar-icons/Sketcher_CompBSplineShowHideGeometryInformation.png) [Toggle B-Spline Degree](#button-sketcher_compbsplineshowhidegeometryinformation) **S** **▼**; ![Toggle Internal Geometry](toolbar-icons/Sketcher_RestoreInternalAlignmentGeometry.png) [Toggle Internal Geometry](#button-sketcher_restoreinternalalignmentgeometry) **S**; ![Switch Virtual Space](toolbar-icons/Sketcher_SwitchVirtualSpace.png) [Switch Virtual Space](#button-sketcher_switchvirtualspace) **S** |

<a id="workbench-surfaceworkbench"></a>
### Surface (`SurfaceWorkbench`)

Definition: [`src/Mod/Surface/Gui/Workbench.cpp`](../../../src/Mod/Surface/Gui/Workbench.cpp). Shared Classic groups are listed once above.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Surface | ![Filling](toolbar-icons/Surface_Filling.png) [Filling](#button-surface_filling); ![Fill Boundary Curves](toolbar-icons/Surface_GeomFillSurface.png) [Fill Boundary Curves](#button-surface_geomfillsurface); ![Sections](toolbar-icons/Surface_Sections.png) [Sections](#button-surface_sections); ![Extend Face](toolbar-icons/Surface_ExtendFace.png) [Extend Face](#button-surface_extendface); ![Curve on Mesh](toolbar-icons/Surface_CurveOnMesh.png) [Curve on Mesh](#button-surface_curveonmesh); ![Blend Curve](toolbar-icons/Surface_BlendCurve.png) [Blend Curve](#button-surface_blendcurve) |

#### Changes made / buttons consolidated or omitted

- No workbench-specific toolbar command removal found in the compared definitions; Plus changes presentation/routing and applies the shared Home/View rules above.

#### Plus UI tabs and sections

**Design → Surface**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Surface | ![Filling](toolbar-icons/Surface_Filling.png) [Filling](#button-surface_filling) **S**; ![Fill Boundary Curves](toolbar-icons/Surface_GeomFillSurface.png) [Fill Boundary Curves](#button-surface_geomfillsurface) **S**; ![Sections](toolbar-icons/Surface_Sections.png) [Sections](#button-surface_sections) **S**; ![Extend Face](toolbar-icons/Surface_ExtendFace.png) [Extend Face](#button-surface_extendface) **L**; ![Curve on Mesh](toolbar-icons/Surface_CurveOnMesh.png) [Curve on Mesh](#button-surface_curveonmesh) **S**; ![Blend Curve](toolbar-icons/Surface_BlendCurve.png) [Blend Curve](#button-surface_blendcurve) **S** |

<a id="workbench-meshworkbench"></a>
### Mesh (`MeshWorkbench`)

Definition: [`src/Mod/Mesh/Gui/Workbench.cpp`](../../../src/Mod/Mesh/Gui/Workbench.cpp). Shared Classic groups are listed once above.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Mesh Tools | ![Import Mesh…](toolbar-icons/Mesh_Import.png) [Import Mesh…](#button-mesh_import); ![Export Mesh…](toolbar-icons/Mesh_Export.png) [Export Mesh…](#button-mesh_export); ![Mesh From Shape](toolbar-icons/Mesh_FromPartShape.png) [Mesh From Shape](#button-mesh_frompartshape); ![Regular Solid](toolbar-icons/Mesh_BuildRegularSolid.png) [Regular Solid](#button-mesh_buildregularsolid) |
| Mesh Modify | ![Harmonize Normals](toolbar-icons/Mesh_HarmonizeNormals.png) [Harmonize Normals](#button-mesh_harmonizenormals); ![Flip Normals](toolbar-icons/Mesh_FlipNormals.png) [Flip Normals](#button-mesh_flipnormals); ![Fill Holes](toolbar-icons/Mesh_FillupHoles.png) [Fill Holes](#button-mesh_fillupholes); ![Close Hole](toolbar-icons/Mesh_FillInteractiveHole.png) [Close Hole](#button-mesh_fillinteractivehole); ![Add Triangle](toolbar-icons/Mesh_AddFacet.png) [Add Triangle](#button-mesh_addfacet); ![Remove Components](toolbar-icons/Mesh_RemoveComponents.png) [Remove Components](#button-mesh_removecomponents); ![Smooth](toolbar-icons/Mesh_Smoothing.png) [Smooth](#button-mesh_smoothing); ![Refinement](toolbar-icons/Mesh_RemeshGmsh.png) [Refinement](#button-mesh_remeshgmsh); ![Decimate](toolbar-icons/Mesh_Decimating.png) [Decimate](#button-mesh_decimating); ![Scale](toolbar-icons/Mesh_Scale.png) [Scale](#button-mesh_scale) |
| Mesh Boolean | ![Union](toolbar-icons/Mesh_Union.png) [Union](#button-mesh_union); ![Intersection](toolbar-icons/Mesh_Intersection.png) [Intersection](#button-mesh_intersection); ![Difference](toolbar-icons/Mesh_Difference.png) [Difference](#button-mesh_difference) |
| Mesh Cutting | ![Cut](toolbar-icons/Mesh_PolyCut.png) [Cut](#button-mesh_polycut); ![Trim](toolbar-icons/Mesh_PolyTrim.png) [Trim](#button-mesh_polytrim); ![Trim With Plane](toolbar-icons/Mesh_TrimByPlane.png) [Trim With Plane](#button-mesh_trimbyplane); ![Section From Plane](toolbar-icons/Mesh_SectionByPlane.png) [Section From Plane](#button-mesh_sectionbyplane); ![Cross-Sections](toolbar-icons/Mesh_CrossSections.png) [Cross-Sections](#button-mesh_crosssections) |
| Mesh Segmentation | ![Merge](toolbar-icons/Mesh_Merge.png) [Merge](#button-mesh_merge); ![Split by Components](toolbar-icons/Mesh_SplitComponents.png) [Split by Components](#button-mesh_splitcomponents); ![Segmentation](toolbar-icons/Mesh_Segmentation.png) [Segmentation](#button-mesh_segmentation); ![Segmentation From Best-Fit Surfaces](toolbar-icons/Mesh_SegmentationBestFit.png) [Segmentation From Best-Fit Surfaces](#button-mesh_segmentationbestfit) |
| Mesh Analyze | ![Evaluate and Repair](toolbar-icons/Mesh_Evaluation.png) [Evaluate and Repair](#button-mesh_evaluation); ![Face Info](toolbar-icons/Mesh_EvaluateFacet.png) [Face Info](#button-mesh_evaluatefacet); ![Curvature Plot](toolbar-icons/Mesh_VertexCurvature.png) [Curvature Plot](#button-mesh_vertexcurvature); ![Curvature Info](toolbar-icons/Mesh_CurvatureInfo.png) [Curvature Info](#button-mesh_curvatureinfo); ![Evaluate Solid](toolbar-icons/Mesh_EvaluateSolid.png) [Evaluate Solid](#button-mesh_evaluatesolid); ![Bounding Box Info](toolbar-icons/Mesh_BoundingBox.png) [Bounding Box Info](#button-mesh_boundingbox) |

#### Changes made / buttons consolidated or omitted

- No workbench-specific toolbar command removal found in the compared definitions; Plus changes presentation/routing and applies the shared Home/View rules above.

#### Plus UI tabs and sections

**Design → Mesh**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Mesh Tools | ![Import Mesh…](toolbar-icons/Mesh_Import.png) [Import Mesh…](#button-mesh_import) **L**; ![Export Mesh…](toolbar-icons/Mesh_Export.png) [Export Mesh…](#button-mesh_export) **S**; ![Mesh From Shape](toolbar-icons/Mesh_FromPartShape.png) [Mesh From Shape](#button-mesh_frompartshape) **S**; ![Regular Solid](toolbar-icons/Mesh_BuildRegularSolid.png) [Regular Solid](#button-mesh_buildregularsolid) **S** |
| Mesh Modify | ![Harmonize Normals](toolbar-icons/Mesh_HarmonizeNormals.png) [Harmonize Normals](#button-mesh_harmonizenormals) **S**; ![Flip Normals](toolbar-icons/Mesh_FlipNormals.png) [Flip Normals](#button-mesh_flipnormals) **S**; ![Fill Holes](toolbar-icons/Mesh_FillupHoles.png) [Fill Holes](#button-mesh_fillupholes) **S**; ![Close Hole](toolbar-icons/Mesh_FillInteractiveHole.png) [Close Hole](#button-mesh_fillinteractivehole) **S**; ![Add Triangle](toolbar-icons/Mesh_AddFacet.png) [Add Triangle](#button-mesh_addfacet) **S**; ![Remove Components](toolbar-icons/Mesh_RemoveComponents.png) [Remove Components](#button-mesh_removecomponents) **S**; ![Smooth](toolbar-icons/Mesh_Smoothing.png) [Smooth](#button-mesh_smoothing) **S**; ![Refinement](toolbar-icons/Mesh_RemeshGmsh.png) [Refinement](#button-mesh_remeshgmsh) **S**; ![Decimate](toolbar-icons/Mesh_Decimating.png) [Decimate](#button-mesh_decimating) **S**; ![Scale](toolbar-icons/Mesh_Scale.png) [Scale](#button-mesh_scale) **S** |
| Mesh Boolean | ![Union](toolbar-icons/Mesh_Union.png) [Union](#button-mesh_union) **S**; ![Intersection](toolbar-icons/Mesh_Intersection.png) [Intersection](#button-mesh_intersection) **S**; ![Difference](toolbar-icons/Mesh_Difference.png) [Difference](#button-mesh_difference) **S** |
| Mesh Cutting | ![Cut](toolbar-icons/Mesh_PolyCut.png) [Cut](#button-mesh_polycut) **S**; ![Trim](toolbar-icons/Mesh_PolyTrim.png) [Trim](#button-mesh_polytrim) **S**; ![Trim With Plane](toolbar-icons/Mesh_TrimByPlane.png) [Trim With Plane](#button-mesh_trimbyplane) **S**; ![Section From Plane](toolbar-icons/Mesh_SectionByPlane.png) [Section From Plane](#button-mesh_sectionbyplane) **S**; ![Cross-Sections](toolbar-icons/Mesh_CrossSections.png) [Cross-Sections](#button-mesh_crosssections) **S** |
| Mesh Segmentation | ![Merge](toolbar-icons/Mesh_Merge.png) [Merge](#button-mesh_merge) **S**; ![Split by Components](toolbar-icons/Mesh_SplitComponents.png) [Split by Components](#button-mesh_splitcomponents) **S**; ![Segmentation](toolbar-icons/Mesh_Segmentation.png) [Segmentation](#button-mesh_segmentation) **S**; ![Segmentation From Best-Fit Surfaces](toolbar-icons/Mesh_SegmentationBestFit.png) [Segmentation From Best-Fit Surfaces](#button-mesh_segmentationbestfit) **S** |
| Mesh Analyze | ![Evaluate and Repair](toolbar-icons/Mesh_Evaluation.png) [Evaluate and Repair](#button-mesh_evaluation) **S**; ![Face Info](toolbar-icons/Mesh_EvaluateFacet.png) [Face Info](#button-mesh_evaluatefacet) **S**; ![Curvature Plot](toolbar-icons/Mesh_VertexCurvature.png) [Curvature Plot](#button-mesh_vertexcurvature) **S**; ![Curvature Info](toolbar-icons/Mesh_CurvatureInfo.png) [Curvature Info](#button-mesh_curvatureinfo) **S**; ![Evaluate Solid](toolbar-icons/Mesh_EvaluateSolid.png) [Evaluate Solid](#button-mesh_evaluatesolid) **S**; ![Bounding Box Info](toolbar-icons/Mesh_BoundingBox.png) [Bounding Box Info](#button-mesh_boundingbox) **S** |

<a id="workbench-draftworkbench"></a>
### Draft (`DraftWorkbench`)

Definition: [`src/Mod/Draft/InitGui.py`](../../../src/Mod/Draft/InitGui.py). Shared Classic groups are listed once above.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Draft Creation | ![Line](toolbar-icons/Draft_Line.png) [Line](#button-draft_line); ![Polyline](toolbar-icons/Draft_Wire.png) [Polyline](#button-draft_wire); ![Fillet](toolbar-icons/Draft_Fillet.png) [Fillet](#button-draft_fillet); ![Arc](toolbar-icons/Draft_ArcTools.png) [Arc](#button-draft_arctools); ![Circle](toolbar-icons/Draft_Circle.png) [Circle](#button-draft_circle); ![Ellipse](toolbar-icons/Draft_Ellipse.png) [Ellipse](#button-draft_ellipse); ![Rectangle](toolbar-icons/Draft_Rectangle.png) [Rectangle](#button-draft_rectangle); ![Polygon](toolbar-icons/Draft_Polygon.png) [Polygon](#button-draft_polygon); ![B-Spline](toolbar-icons/Draft_BSpline.png) [B-Spline](#button-draft_bspline); ![Cubic Bézier Curve](toolbar-icons/Draft_BezierTools.png) [Cubic Bézier Curve](#button-draft_beziertools); ![Point](toolbar-icons/Draft_Point.png) [Point](#button-draft_point); ![Facebinder](toolbar-icons/Draft_Facebinder.png) [Facebinder](#button-draft_facebinder); ![Shape From Text](toolbar-icons/Draft_ShapeString.png) [Shape From Text](#button-draft_shapestring); ![Hatch](toolbar-icons/Draft_Hatch.png) [Hatch](#button-draft_hatch) |
| Draft Annotation | ![Text](toolbar-icons/Draft_Text.png) [Text](#button-draft_text); ![Dimension](toolbar-icons/Draft_Dimension.png) [Dimension](#button-draft_dimension); ![Label](toolbar-icons/Draft_Label.png) [Label](#button-draft_label); ![Annotation Styles](toolbar-icons/Draft_AnnotationStyleEditor.png) [Annotation Styles](#button-draft_annotationstyleeditor) |
| Draft Modification | ![Move](toolbar-icons/Draft_Move.png) [Move](#button-draft_move); ![Rotate](toolbar-icons/Draft_Rotate.png) [Rotate](#button-draft_rotate); ![Scale](toolbar-icons/Draft_Scale.png) [Scale](#button-draft_scale); ![Mirror](toolbar-icons/Draft_Mirror.png) [Mirror](#button-draft_mirror); ![Offset](toolbar-icons/Draft_Offset.png) [Offset](#button-draft_offset); ![Trimex](toolbar-icons/Draft_Trimex.png) [Trimex](#button-draft_trimex); ![Stretch](toolbar-icons/Draft_Stretch.png) [Stretch](#button-draft_stretch);  · ; ![Clone](toolbar-icons/Draft_Clone.png) [Clone](#button-draft_clone); ![Array](toolbar-icons/Draft_ArrayTools.png) [Array](#button-draft_arraytools);  · ; ![Edit](toolbar-icons/Draft_Edit.png) [Edit](#button-draft_edit); ![Highlight Subelements](toolbar-icons/Draft_SubelementHighlight.png) [Highlight Subelements](#button-draft_subelementhighlight);  · ; ![Join](toolbar-icons/Draft_Join.png) [Join](#button-draft_join); ![Split](toolbar-icons/Draft_Split.png) [Split](#button-draft_split); ![Upgrade](toolbar-icons/Draft_Upgrade.png) [Upgrade](#button-draft_upgrade); ![Downgrade](toolbar-icons/Draft_Downgrade.png) [Downgrade](#button-draft_downgrade);  · ; ![Convert Wire/B-Spline](toolbar-icons/Draft_WireToBSpline.png) [Convert Wire/B-Spline](#button-draft_wiretobspline); ![Draft to Sketch](toolbar-icons/Draft_Draft2Sketch.png) [Draft to Sketch](#button-draft_draft2sketch); ![Set Slope](toolbar-icons/Draft_Slope.png) [Set Slope](#button-draft_slope); ![Flip Dimension](toolbar-icons/Draft_FlipDimension.png) [Flip Dimension](#button-draft_flipdimension);  · ; ![Shape 2D View](toolbar-icons/Draft_Shape2DView.png) [Shape 2D View](#button-draft_shape2dview) |
| Draft Utility | ![Manage Layers](toolbar-icons/Draft_LayerManager.png) [Manage Layers](#button-draft_layermanager); ![New Named Group](toolbar-icons/Draft_AddNamedGroup.png) [New Named Group](#button-draft_addnamedgroup); ![Select Group](toolbar-icons/Draft_SelectGroup.png) [Select Group](#button-draft_selectgroup); ![Add to Layer](toolbar-icons/Draft_AddToLayer.png) [Add to Layer](#button-draft_addtolayer); ![Add to Group](toolbar-icons/Draft_AddToGroup.png) [Add to Group](#button-draft_addtogroup); ![Add to Construction Group](toolbar-icons/Draft_AddConstruction.png) [Add to Construction Group](#button-draft_addconstruction); ![Toggle Wireframe](toolbar-icons/Draft_ToggleDisplayMode.png) [Toggle Wireframe](#button-draft_toggledisplaymode); ![Working Plane Proxy](toolbar-icons/Draft_WorkingPlaneProxy.png) [Working Plane Proxy](#button-draft_workingplaneproxy) |
| Draft Snap | ![Snap Lock](toolbar-icons/Draft_Snap_Lock.png) [Snap Lock](#button-draft_snap_lock); ![Snap Endpoint](toolbar-icons/Draft_Snap_Endpoint.png) [Snap Endpoint](#button-draft_snap_endpoint); ![Snap Midpoint](toolbar-icons/Draft_Snap_Midpoint.png) [Snap Midpoint](#button-draft_snap_midpoint); ![Snap Center](toolbar-icons/Draft_Snap_Center.png) [Snap Center](#button-draft_snap_center); ![Snap Angle](toolbar-icons/Draft_Snap_Angle.png) [Snap Angle](#button-draft_snap_angle); ![Snap Intersection](toolbar-icons/Draft_Snap_Intersection.png) [Snap Intersection](#button-draft_snap_intersection); ![Snap Perpendicular](toolbar-icons/Draft_Snap_Perpendicular.png) [Snap Perpendicular](#button-draft_snap_perpendicular); ![Snap Extension](toolbar-icons/Draft_Snap_Extension.png) [Snap Extension](#button-draft_snap_extension); ![Snap Parallel](toolbar-icons/Draft_Snap_Parallel.png) [Snap Parallel](#button-draft_snap_parallel); ![Snap Special](toolbar-icons/Draft_Snap_Special.png) [Snap Special](#button-draft_snap_special); ![Snap Near](toolbar-icons/Draft_Snap_Near.png) [Snap Near](#button-draft_snap_near); ![Snap Ortho](toolbar-icons/Draft_Snap_Ortho.png) [Snap Ortho](#button-draft_snap_ortho); ![Snap Grid](toolbar-icons/Draft_Snap_Grid.png) [Snap Grid](#button-draft_snap_grid); ![Snap Working Plane](toolbar-icons/Draft_Snap_WorkingPlane.png) [Snap Working Plane](#button-draft_snap_workingplane); ![Snap Dimensions](toolbar-icons/Draft_Snap_Dimensions.png) [Snap Dimensions](#button-draft_snap_dimensions);  · ; ![Toggle Grid](toolbar-icons/Draft_ToggleGrid.png) [Toggle Grid](#button-draft_togglegrid) |

#### Changes made / buttons consolidated or omitted

- No workbench-specific toolbar command removal found in the compared definitions; Plus changes presentation/routing and applies the shared Home/View rules above.

#### Plus UI tabs and sections

**Home:** shared sections above; Home excludes the Design-only Sketch and Tools sections.

**Draft → Tools**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Draft Creation | ![Line](toolbar-icons/Draft_Line.png) [Line](#button-draft_line) **L**; ![Polyline](toolbar-icons/Draft_Wire.png) [Polyline](#button-draft_wire) **L**; ![Fillet](toolbar-icons/Draft_Fillet.png) [Fillet](#button-draft_fillet) **S**; ![Arc](toolbar-icons/Draft_ArcTools.png) [Arc](#button-draft_arctools) **S** **▼**; ![Circle](toolbar-icons/Draft_Circle.png) [Circle](#button-draft_circle) **S**; ![Ellipse](toolbar-icons/Draft_Ellipse.png) [Ellipse](#button-draft_ellipse) **S**; ![Rectangle](toolbar-icons/Draft_Rectangle.png) [Rectangle](#button-draft_rectangle) **S**; ![Polygon](toolbar-icons/Draft_Polygon.png) [Polygon](#button-draft_polygon) **S**; ![B-Spline](toolbar-icons/Draft_BSpline.png) [B-Spline](#button-draft_bspline) **S**; ![Cubic Bézier Curve](toolbar-icons/Draft_BezierTools.png) [Cubic Bézier Curve](#button-draft_beziertools) **S** **▼**; ![Point](toolbar-icons/Draft_Point.png) [Point](#button-draft_point) **S**; ![Facebinder](toolbar-icons/Draft_Facebinder.png) [Facebinder](#button-draft_facebinder) **S**; ![Shape From Text](toolbar-icons/Draft_ShapeString.png) [Shape From Text](#button-draft_shapestring) **S**; ![Hatch](toolbar-icons/Draft_Hatch.png) [Hatch](#button-draft_hatch) **S** |
| Draft Annotation | ![Text](toolbar-icons/Draft_Text.png) [Text](#button-draft_text) **S**; ![Dimension](toolbar-icons/Draft_Dimension.png) [Dimension](#button-draft_dimension) **S**; ![Label](toolbar-icons/Draft_Label.png) [Label](#button-draft_label) **S**; ![Annotation Styles](toolbar-icons/Draft_AnnotationStyleEditor.png) [Annotation Styles](#button-draft_annotationstyleeditor) **S** |
| Draft Modification | ![Move](toolbar-icons/Draft_Move.png) [Move](#button-draft_move) **S**; ![Rotate](toolbar-icons/Draft_Rotate.png) [Rotate](#button-draft_rotate) **S**; ![Scale](toolbar-icons/Draft_Scale.png) [Scale](#button-draft_scale) **S**; ![Mirror](toolbar-icons/Draft_Mirror.png) [Mirror](#button-draft_mirror) **S**; ![Offset](toolbar-icons/Draft_Offset.png) [Offset](#button-draft_offset) **S**; ![Trimex](toolbar-icons/Draft_Trimex.png) [Trimex](#button-draft_trimex) **S**; ![Stretch](toolbar-icons/Draft_Stretch.png) [Stretch](#button-draft_stretch) **S**; ![Clone](toolbar-icons/Draft_Clone.png) [Clone](#button-draft_clone) **S**; ![Array](toolbar-icons/Draft_ArrayTools.png) [Array](#button-draft_arraytools) **S** **▼**; ![Edit](toolbar-icons/Draft_Edit.png) [Edit](#button-draft_edit) **S**; ![Highlight Subelements](toolbar-icons/Draft_SubelementHighlight.png) [Highlight Subelements](#button-draft_subelementhighlight) **S**; ![Join](toolbar-icons/Draft_Join.png) [Join](#button-draft_join) **S**; ![Split](toolbar-icons/Draft_Split.png) [Split](#button-draft_split) **S**; ![Upgrade](toolbar-icons/Draft_Upgrade.png) [Upgrade](#button-draft_upgrade) **S**; ![Downgrade](toolbar-icons/Draft_Downgrade.png) [Downgrade](#button-draft_downgrade) **S**; ![Convert Wire/B-Spline](toolbar-icons/Draft_WireToBSpline.png) [Convert Wire/B-Spline](#button-draft_wiretobspline) **S**; ![Draft to Sketch](toolbar-icons/Draft_Draft2Sketch.png) [Draft to Sketch](#button-draft_draft2sketch) **S**; ![Set Slope](toolbar-icons/Draft_Slope.png) [Set Slope](#button-draft_slope) **S**; ![Flip Dimension](toolbar-icons/Draft_FlipDimension.png) [Flip Dimension](#button-draft_flipdimension) **S**; ![Shape 2D View](toolbar-icons/Draft_Shape2DView.png) [Shape 2D View](#button-draft_shape2dview) **S** |
| Draft Utility | ![Manage Layers](toolbar-icons/Draft_LayerManager.png) [Manage Layers](#button-draft_layermanager) **S**; ![New Named Group](toolbar-icons/Draft_AddNamedGroup.png) [New Named Group](#button-draft_addnamedgroup) **S**; ![Select Group](toolbar-icons/Draft_SelectGroup.png) [Select Group](#button-draft_selectgroup) **S**; ![Add to Layer](toolbar-icons/Draft_AddToLayer.png) [Add to Layer](#button-draft_addtolayer) **S**; ![Add to Group](toolbar-icons/Draft_AddToGroup.png) [Add to Group](#button-draft_addtogroup) **S**; ![Add to Construction Group](toolbar-icons/Draft_AddConstruction.png) [Add to Construction Group](#button-draft_addconstruction) **S**; ![Toggle Wireframe](toolbar-icons/Draft_ToggleDisplayMode.png) [Toggle Wireframe](#button-draft_toggledisplaymode) **S**; ![Working Plane Proxy](toolbar-icons/Draft_WorkingPlaneProxy.png) [Working Plane Proxy](#button-draft_workingplaneproxy) **S** |
| Draft Snap | ![Snap Lock](toolbar-icons/Draft_Snap_Lock.png) [Snap Lock](#button-draft_snap_lock) **S**; ![Snap Endpoint](toolbar-icons/Draft_Snap_Endpoint.png) [Snap Endpoint](#button-draft_snap_endpoint) **S**; ![Snap Midpoint](toolbar-icons/Draft_Snap_Midpoint.png) [Snap Midpoint](#button-draft_snap_midpoint) **S**; ![Snap Center](toolbar-icons/Draft_Snap_Center.png) [Snap Center](#button-draft_snap_center) **S**; ![Snap Angle](toolbar-icons/Draft_Snap_Angle.png) [Snap Angle](#button-draft_snap_angle) **S**; ![Snap Intersection](toolbar-icons/Draft_Snap_Intersection.png) [Snap Intersection](#button-draft_snap_intersection) **S**; ![Snap Perpendicular](toolbar-icons/Draft_Snap_Perpendicular.png) [Snap Perpendicular](#button-draft_snap_perpendicular) **S**; ![Snap Extension](toolbar-icons/Draft_Snap_Extension.png) [Snap Extension](#button-draft_snap_extension) **S**; ![Snap Parallel](toolbar-icons/Draft_Snap_Parallel.png) [Snap Parallel](#button-draft_snap_parallel) **S**; ![Snap Special](toolbar-icons/Draft_Snap_Special.png) [Snap Special](#button-draft_snap_special) **S**; ![Snap Near](toolbar-icons/Draft_Snap_Near.png) [Snap Near](#button-draft_snap_near) **S**; ![Snap Ortho](toolbar-icons/Draft_Snap_Ortho.png) [Snap Ortho](#button-draft_snap_ortho) **S**; ![Snap Grid](toolbar-icons/Draft_Snap_Grid.png) [Snap Grid](#button-draft_snap_grid) **S**; ![Snap Working Plane](toolbar-icons/Draft_Snap_WorkingPlane.png) [Snap Working Plane](#button-draft_snap_workingplane) **S**; ![Snap Dimensions](toolbar-icons/Draft_Snap_Dimensions.png) [Snap Dimensions](#button-draft_snap_dimensions) **S**; ![Toggle Grid](toolbar-icons/Draft_ToggleGrid.png) [Toggle Grid](#button-draft_togglegrid) **S** |

**View:** shared sections above.

<a id="workbench-assemblyworkbench"></a>
### Assembly (`AssemblyWorkbench`)

Definition: [`src/Mod/Assembly/InitGui.py`](../../../src/Mod/Assembly/InitGui.py). Shared Classic groups are listed once above.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Assembly | ![New Assembly](toolbar-icons/Assembly_CreateAssembly.png) [New Assembly](#button-assembly_createassembly); ![Insert Component](toolbar-icons/Assembly_Insert.png) [Insert Component](#button-assembly_insert); ![Circular Link Array](toolbar-icons/Part_LinkArrays.png) [Circular Link Array](#button-part_linkarrays); ![Solve Assembly](toolbar-icons/Assembly_SolveAssembly.png) [Solve Assembly](#button-assembly_solveassembly); ![Exploded View](toolbar-icons/Assembly_CreateView.png) [Exploded View](#button-assembly_createview); ![Snapshot](toolbar-icons/Assembly_CreateSnapshot.png) [Snapshot](#button-assembly_createsnapshot); ![Simulation](toolbar-icons/Assembly_CreateSimulation.png) [Simulation](#button-assembly_createsimulation); ![Bill of Materials](toolbar-icons/Assembly_CreateBom.png) [Bill of Materials](#button-assembly_createbom) |
| Assembly Joints | ![Toggle Grounded](toolbar-icons/Assembly_ToggleGrounded.png) [Toggle Grounded](#button-assembly_togglegrounded); ![Create Rigid Group](toolbar-icons/Assembly_CreateJointRigidGroup.png) [Create Rigid Group](#button-assembly_createjointrigidgroup);  · ; ![Fixed Joint](toolbar-icons/Assembly_CreateJointFixed.png) [Fixed Joint](#button-assembly_createjointfixed); ![Revolute Joint](toolbar-icons/Assembly_CreateJointRevolute.png) [Revolute Joint](#button-assembly_createjointrevolute); ![Cylindrical Joint](toolbar-icons/Assembly_CreateJointCylindrical.png) [Cylindrical Joint](#button-assembly_createjointcylindrical); ![Slider Joint](toolbar-icons/Assembly_CreateJointSlider.png) [Slider Joint](#button-assembly_createjointslider); ![Ball Joint](toolbar-icons/Assembly_CreateJointBall.png) [Ball Joint](#button-assembly_createjointball);  · ; ![Distance Joint](toolbar-icons/Assembly_CreateJointDistance.png) [Distance Joint](#button-assembly_createjointdistance); ![Parallel Joint](toolbar-icons/Assembly_CreateJointParallel.png) [Parallel Joint](#button-assembly_createjointparallel); ![Perpendicular Joint](toolbar-icons/Assembly_CreateJointPerpendicular.png) [Perpendicular Joint](#button-assembly_createjointperpendicular); ![Angle Joint](toolbar-icons/Assembly_CreateJointAngle.png) [Angle Joint](#button-assembly_createjointangle);  · ; ![Rack and Pinion Joint](toolbar-icons/Assembly_CreateJointRackPinion.png) [Rack and Pinion Joint](#button-assembly_createjointrackpinion); ![Screw Joint](toolbar-icons/Assembly_CreateJointScrew.png) [Screw Joint](#button-assembly_createjointscrew); ![Gears Joint](toolbar-icons/Assembly_CreateJointGearBelt.png) [Gears Joint](#button-assembly_createjointgearbelt) |

#### Changes made / buttons consolidated or omitted

- No workbench-specific toolbar command removal found in the compared definitions; Plus changes presentation/routing and applies the shared Home/View rules above.

#### Plus UI tabs and sections

**Home:** shared sections above; Home excludes the Design-only Sketch and Tools sections.

**Assembly → Tools**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Assembly | ![New Assembly](toolbar-icons/Assembly_CreateAssembly.png) [New Assembly](#button-assembly_createassembly) **S**; ![Insert Component](toolbar-icons/Assembly_Insert.png) [Insert Component](#button-assembly_insert) **S** **▼**; ![Circular Link Array](toolbar-icons/Part_LinkArrays.png) [Circular Link Array](#button-part_linkarrays) **S** **▼**; ![Solve Assembly](toolbar-icons/Assembly_SolveAssembly.png) [Solve Assembly](#button-assembly_solveassembly) **S**; ![Exploded View](toolbar-icons/Assembly_CreateView.png) [Exploded View](#button-assembly_createview) **S**; ![Snapshot](toolbar-icons/Assembly_CreateSnapshot.png) [Snapshot](#button-assembly_createsnapshot) **S**; ![Simulation](toolbar-icons/Assembly_CreateSimulation.png) [Simulation](#button-assembly_createsimulation) **S**; ![Bill of Materials](toolbar-icons/Assembly_CreateBom.png) [Bill of Materials](#button-assembly_createbom) **S** |
| Assembly Joints | ![Toggle Grounded](toolbar-icons/Assembly_ToggleGrounded.png) [Toggle Grounded](#button-assembly_togglegrounded) **S**; ![Create Rigid Group](toolbar-icons/Assembly_CreateJointRigidGroup.png) [Create Rigid Group](#button-assembly_createjointrigidgroup) **S**; ![Fixed Joint](toolbar-icons/Assembly_CreateJointFixed.png) [Fixed Joint](#button-assembly_createjointfixed) **S**; ![Revolute Joint](toolbar-icons/Assembly_CreateJointRevolute.png) [Revolute Joint](#button-assembly_createjointrevolute) **S**; ![Cylindrical Joint](toolbar-icons/Assembly_CreateJointCylindrical.png) [Cylindrical Joint](#button-assembly_createjointcylindrical) **S**; ![Slider Joint](toolbar-icons/Assembly_CreateJointSlider.png) [Slider Joint](#button-assembly_createjointslider) **S**; ![Ball Joint](toolbar-icons/Assembly_CreateJointBall.png) [Ball Joint](#button-assembly_createjointball) **S**; ![Distance Joint](toolbar-icons/Assembly_CreateJointDistance.png) [Distance Joint](#button-assembly_createjointdistance) **S**; ![Parallel Joint](toolbar-icons/Assembly_CreateJointParallel.png) [Parallel Joint](#button-assembly_createjointparallel) **S**; ![Perpendicular Joint](toolbar-icons/Assembly_CreateJointPerpendicular.png) [Perpendicular Joint](#button-assembly_createjointperpendicular) **S**; ![Angle Joint](toolbar-icons/Assembly_CreateJointAngle.png) [Angle Joint](#button-assembly_createjointangle) **S**; ![Rack and Pinion Joint](toolbar-icons/Assembly_CreateJointRackPinion.png) [Rack and Pinion Joint](#button-assembly_createjointrackpinion) **S**; ![Screw Joint](toolbar-icons/Assembly_CreateJointScrew.png) [Screw Joint](#button-assembly_createjointscrew) **S**; ![Gears Joint](toolbar-icons/Assembly_CreateJointGearBelt.png) [Gears Joint](#button-assembly_createjointgearbelt) **S** **▼** |

**View:** shared sections above.

<a id="workbench-camworkbench"></a>
### CAM (`CAMWorkbench`)

Definition: [`src/Mod/CAM/InitGui.py`](../../../src/Mod/CAM/InitGui.py). Shared Classic groups are listed once above.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Project Setup | ![New Job](toolbar-icons/CAM_Job.png) [New Job](#button-cam_job); ![Work Plane](toolbar-icons/CAM_Workplane.png) [Work Plane](#button-cam_workplane); ![Sanity Check](toolbar-icons/CAM_Sanity.png) [Sanity Check](#button-cam_sanity); ![Post Process](toolbar-icons/CAM_PostTools.png) [Post Process](#button-cam_posttools) |
| Tool Commands | ![CAM Simulator](toolbar-icons/CAM_SimTools.png) [CAM Simulator](#button-cam_simtools); ![Inspect Toolpath](toolbar-icons/CAM_Inspect.png) [Inspect Toolpath](#button-cam_inspect); ![Finish Selecting Loop](toolbar-icons/CAM_SelectLoop.png) [Finish Selecting Loop](#button-cam_selectloop); ![Toggle Operation](toolbar-icons/CAM_OpActiveToggle.png) [Toggle Operation](#button-cam_opactivetoggle); ![Add Toolbit…](toolbar-icons/CAM_ToolBitDock.png) [Add Toolbit…](#button-cam_toolbitdock) |
| New Operations | ![Profile](toolbar-icons/CAM_Profile.png) [Profile](#button-cam_profile); ![Pocket Shape](toolbar-icons/CAM_Pocket_Shape.png) [Pocket Shape](#button-cam_pocket_shape); ![Mill Facing](toolbar-icons/CAM_MillFacing.png) [Mill Facing](#button-cam_millfacing); ![Helix](toolbar-icons/CAM_Helix.png) [Helix](#button-cam_helix); ![Adaptive](toolbar-icons/CAM_Adaptive.png) [Adaptive](#button-cam_adaptive); ![Slot](toolbar-icons/CAM_Slot.png) [Slot](#button-cam_slot); ![Drilling](toolbar-icons/CAM_DrillingTools.png) [Drilling](#button-cam_drillingtools); ![Engrave](toolbar-icons/CAM_EngraveTools.png) [Engrave](#button-cam_engravetools) |
| Path Modification | ![Copy Operation](toolbar-icons/CAM_OperationCopy.png) [Copy Operation](#button-cam_operationcopy); ![Array](toolbar-icons/CAM_Array.png) [Array](#button-cam_array); ![Simple Copy](toolbar-icons/CAM_SimpleCopy.png) [Simple Copy](#button-cam_simplecopy); ![Array](toolbar-icons/CAM_DressupTools.png) [Array](#button-cam_dressuptools) |

#### Changes made / buttons consolidated or omitted

- Project Setup adds Mesh Preparation, Holding Tabs and Indexed Setup.
- New Operations exposes Parallel / Waterline (`CAM_PlanarSurface`) with OpenCAMLib. Stock upstream makes advanced 3D operations conditional; grouping can change when the advanced setting is enabled.
- Added to native toolbar definitions: ![Holding Tab](../../../src/Gui/Icons/preferences-general.svg) [Holding Tab](#button-cam_holdingtab); ![Indexed Setup](toolbar-icons/CAM_IndexedSetup.png) [Indexed Setup](#button-cam_indexedsetup); ![Review CAM mesh...](toolbar-icons/CAM_MeshPreparation.png) [Review CAM mesh...](#button-cam_meshpreparation); ![Parallel / Waterline](toolbar-icons/CAM_PlanarSurface.png) [Parallel / Waterline](#button-cam_planarsurface).

#### Plus UI tabs and sections

**Home:** shared sections above; Home excludes the Design-only Sketch and Tools sections.

**CAM → Tools**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Project Setup | ![New Job](toolbar-icons/CAM_Job.png) [New Job](#button-cam_job) **L**; ![Review CAM mesh...](toolbar-icons/CAM_MeshPreparation.png) [Review CAM mesh...](#button-cam_meshpreparation) **S**; ![Work Plane](toolbar-icons/CAM_Workplane.png) [Work Plane](#button-cam_workplane) **S**; ![Holding Tab](../../../src/Gui/Icons/preferences-general.svg) [Holding Tab](#button-cam_holdingtab) **S**; ![Indexed Setup](toolbar-icons/CAM_IndexedSetup.png) [Indexed Setup](#button-cam_indexedsetup) **S**; ![Sanity Check](toolbar-icons/CAM_Sanity.png) [Sanity Check](#button-cam_sanity) **S**; ![Post Process](toolbar-icons/CAM_PostTools.png) [Post Process](#button-cam_posttools) **S** **▼** |
| Tool Commands | ![CAM Simulator](toolbar-icons/CAM_SimTools.png) [CAM Simulator](#button-cam_simtools) **S** **▼**; ![Inspect Toolpath](toolbar-icons/CAM_Inspect.png) [Inspect Toolpath](#button-cam_inspect) **S**; ![Finish Selecting Loop](toolbar-icons/CAM_SelectLoop.png) [Finish Selecting Loop](#button-cam_selectloop) **S**; ![Toggle Operation](toolbar-icons/CAM_OpActiveToggle.png) [Toggle Operation](#button-cam_opactivetoggle) **S**; ![Add Toolbit…](toolbar-icons/CAM_ToolBitDock.png) [Add Toolbit…](#button-cam_toolbitdock) **S** |
| New Operations | ![Profile](toolbar-icons/CAM_Profile.png) [Profile](#button-cam_profile) **S**; ![Pocket Shape](toolbar-icons/CAM_Pocket_Shape.png) [Pocket Shape](#button-cam_pocket_shape) **S**; ![Mill Facing](toolbar-icons/CAM_MillFacing.png) [Mill Facing](#button-cam_millfacing) **S**; ![Helix](toolbar-icons/CAM_Helix.png) [Helix](#button-cam_helix) **S**; ![Adaptive](toolbar-icons/CAM_Adaptive.png) [Adaptive](#button-cam_adaptive) **S**; ![Slot](toolbar-icons/CAM_Slot.png) [Slot](#button-cam_slot) **S**; ![Drilling](toolbar-icons/CAM_DrillingTools.png) [Drilling](#button-cam_drillingtools) **S** **▼**; ![Engrave](toolbar-icons/CAM_EngraveTools.png) [Engrave](#button-cam_engravetools) **S** **▼**; ![Parallel / Waterline](toolbar-icons/CAM_PlanarSurface.png) [Parallel / Waterline](#button-cam_planarsurface) **S** |
| Path Modification | ![Copy Operation](toolbar-icons/CAM_OperationCopy.png) [Copy Operation](#button-cam_operationcopy) **S**; ![Array](toolbar-icons/CAM_Array.png) [Array](#button-cam_array) **S**; ![Simple Copy](toolbar-icons/CAM_SimpleCopy.png) [Simple Copy](#button-cam_simplecopy) **S**; ![Array](toolbar-icons/CAM_DressupTools.png) [Array](#button-cam_dressuptools) **S** **▼** |

**View:** shared sections above.

<a id="workbench-techdrawworkbench"></a>
### TechDraw (`TechDrawWorkbench`)

Definition: [`src/Mod/TechDraw/Gui/Workbench.cpp`](../../../src/Mod/TechDraw/Gui/Workbench.cpp). Shared Classic groups are listed once above.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| TechDraw Pages | ![New Page](toolbar-icons/TechDraw_PageDefault.png) [New Page](#button-techdraw_pagedefault); ![New Page From Template](toolbar-icons/TechDraw_PageTemplate.png) [New Page From Template](#button-techdraw_pagetemplate); ![Update Template Fields](toolbar-icons/TechDraw_FillTemplateFields.png) [Update Template Fields](#button-techdraw_filltemplatefields); ![Redraw Page](toolbar-icons/TechDraw_RedrawPage.png) [Redraw Page](#button-techdraw_redrawpage); ![Print All Pages](toolbar-icons/TechDraw_PrintAll.png) [Print All Pages](#button-techdraw_printall) |
| TechDraw Views | ![New View](toolbar-icons/TechDraw_View.png) [New View](#button-techdraw_view); ![Broken View](toolbar-icons/TechDraw_BrokenView.png) [Broken View](#button-techdraw_brokenview); ![Active View](toolbar-icons/TechDraw_ActiveView.png) [Active View](#button-techdraw_activeview); ![Section View](toolbar-icons/TechDraw_SectionGroup.png) [Section View](#button-techdraw_sectiongroup); ![Detail View](toolbar-icons/TechDraw_DetailView.png) [Detail View](#button-techdraw_detailview); ![Draft View](toolbar-icons/TechDraw_DraftView.png) [Draft View](#button-techdraw_draftview); ![Spreadsheet View](toolbar-icons/TechDraw_SpreadsheetView.png) [Spreadsheet View](#button-techdraw_spreadsheetview); ![Clip Group](toolbar-icons/TechDraw_ClipGroup.png) [Clip Group](#button-techdraw_clipgroup) |
| TechDraw Stacking | ![Stack Top](toolbar-icons/TechDraw_StackGroup.png) [Stack Top](#button-techdraw_stackgroup) |
| TechDraw Dimensions | ![Dimension](toolbar-icons/TechDraw_Dimension.png) [Dimension](#button-techdraw_dimension); ![Dimension](toolbar-icons/TechDraw_CompDimensionTools.png) [Dimension](#button-techdraw_compdimensiontools); ![Length Dimension](toolbar-icons/TechDraw_LengthDimension.png) [Length Dimension](#button-techdraw_lengthdimension); ![Horizontal Length Dimension](toolbar-icons/TechDraw_HorizontalDimension.png) [Horizontal Length Dimension](#button-techdraw_horizontaldimension); ![Vertical Length Dimension](toolbar-icons/TechDraw_VerticalDimension.png) [Vertical Length Dimension](#button-techdraw_verticaldimension); ![Radius Dimension](toolbar-icons/TechDraw_RadiusDimension.png) [Radius Dimension](#button-techdraw_radiusdimension); ![Diameter Dimension](toolbar-icons/TechDraw_DiameterDimension.png) [Diameter Dimension](#button-techdraw_diameterdimension); ![Angle Dimension](toolbar-icons/TechDraw_AngleDimension.png) [Angle Dimension](#button-techdraw_angledimension); ![Angle Dimension From 3 Points](toolbar-icons/TechDraw_3PtAngleDimension.png) [Angle Dimension From 3 Points](#button-techdraw_3ptangledimension); ![Area Annotation](toolbar-icons/TechDraw_AreaDimension.png) [Area Annotation](#button-techdraw_areadimension); ![Horizontal extent](toolbar-icons/TechDraw_ExtentGroup.png) [Horizontal extent](#button-techdraw_extentgroup); ![Balloon Annotation](toolbar-icons/TechDraw_Balloon.png) [Balloon Annotation](#button-techdraw_balloon); ![Axonometric Length Dimension](toolbar-icons/TechDraw_AxoLengthDimension.png) [Axonometric Length Dimension](#button-techdraw_axolengthdimension); ![Repair Dimension References](toolbar-icons/TechDraw_DimensionRepair.png) [Repair Dimension References](#button-techdraw_dimensionrepair) |
| TechDraw Attributes | ![Select Line Attributes, Cascade Spacing and Delta Distance](toolbar-icons/TechDraw_ExtensionSelectLineAttributes.png) [Select Line Attributes, Cascade Spacing and Delta Distance](#button-techdraw_extensionselectlineattributes); ![Change Line Attributes](toolbar-icons/TechDraw_ExtensionChangeLineAttributes.png) [Change Line Attributes](#button-techdraw_extensionchangelineattributes); ![Extend Line](toolbar-icons/TechDraw_ExtensionExtendShortenLineGroup.png) [Extend Line](#button-techdraw_extensionextendshortenlinegroup); ![Toggle View Lock](toolbar-icons/TechDraw_ExtensionLockUnlockView.png) [Toggle View Lock](#button-techdraw_extensionlockunlockview); ![Position Section View](toolbar-icons/TechDraw_ExtensionPositionSectionView.png) [Position Section View](#button-techdraw_extensionpositionsectionview); ![Area Annotation](toolbar-icons/TechDraw_ExtensionAreaAnnotation.png) [Area Annotation](#button-techdraw_extensionareaannotation); ![Arc Length Annotation](toolbar-icons/TechDraw_ExtensionArcLengthAnnotation.png) [Arc Length Annotation](#button-techdraw_extensionarclengthannotation); ![Customize Format Label](toolbar-icons/TechDraw_ExtensionCustomizeFormat.png) [Customize Format Label](#button-techdraw_extensioncustomizeformat) |
| TechDraw Centerlines | ![Circle Centerlines](toolbar-icons/TechDraw_ExtensionCircleCenterLinesGroup.png) [Circle Centerlines](#button-techdraw_extensioncirclecenterlinesgroup); ![Cosmetic Thread Hole Side View](toolbar-icons/TechDraw_ExtensionThreadsGroup.png) [Cosmetic Thread Hole Side View](#button-techdraw_extensionthreadsgroup); ![Cosmetic Intersection Vertices](toolbar-icons/TechDraw_CommandVertexCreationGroup.png) [Cosmetic Intersection Vertices](#button-techdraw_commandvertexcreationgroup); ![Cosmetic 1 Point Circle](toolbar-icons/TechDraw_ExtensionDrawCirclesGroup.png) [Cosmetic 1 Point Circle](#button-techdraw_extensiondrawcirclesgroup); ![Cosmetic Parallel Line](toolbar-icons/TechDraw_ExtensionLinePPGroup.png) [Cosmetic Parallel Line](#button-techdraw_extensionlineppgroup) |
| TechDraw Extend Dimensions | ![Horizontal Chain Dimension](toolbar-icons/TechDraw_ExtensionCreateChainDimensionGroup.png) [Horizontal Chain Dimension](#button-techdraw_extensioncreatechaindimensiongroup); ![Horizontal Coordinate Dimension](toolbar-icons/TechDraw_ExtensionCreateCoordDimensionGroup.png) [Horizontal Coordinate Dimension](#button-techdraw_extensioncreatecoorddimensiongroup); ![Horizontal Chamfer Dimension](toolbar-icons/TechDraw_ExtensionChamferDimensionGroup.png) [Horizontal Chamfer Dimension](#button-techdraw_extensionchamferdimensiongroup); ![Arc Length Dimension](toolbar-icons/TechDraw_ExtensionCreateLengthArc.png) [Arc Length Dimension](#button-techdraw_extensioncreatelengtharc); ![Insert '⌀' Prefix](toolbar-icons/TechDraw_ExtensionInsertPrefixGroup.png) [Insert '⌀' Prefix](#button-techdraw_extensioninsertprefixgroup); ![Increase Decimal Places](toolbar-icons/TechDraw_ExtensionIncreaseDecreaseGroup.png) [Increase Decimal Places](#button-techdraw_extensionincreasedecreasegroup) |
| TechDraw File Access | ![Export Page as SVG](toolbar-icons/TechDraw_ExportPageSVG.png) [Export Page as SVG](#button-techdraw_exportpagesvg); ![Export Page as DXF](toolbar-icons/TechDraw_ExportPageDXF.png) [Export Page as DXF](#button-techdraw_exportpagedxf) |
| TechDraw Decoration | ![Toggle View Frames](toolbar-icons/TechDraw_ToggleFrame.png) [Toggle View Frames](#button-techdraw_toggleframe); ![Image Hatch](toolbar-icons/TechDraw_Hatch.png) [Image Hatch](#button-techdraw_hatch); ![Geometric Hatch](toolbar-icons/TechDraw_GeometricHatch.png) [Geometric Hatch](#button-techdraw_geometrichatch) |
| TechDraw Annotation | ![Rich Text Annotation](toolbar-icons/TechDraw_RichTextAnnotation.png) [Rich Text Annotation](#button-techdraw_richtextannotation); ![Leader Line](toolbar-icons/TechDraw_LeaderLine.png) [Leader Line](#button-techdraw_leaderline); ![Cosmetic Vertex](toolbar-icons/TechDraw_CosmeticVertexGroup.png) [Cosmetic Vertex](#button-techdraw_cosmeticvertexgroup); ![Centerline on Face](toolbar-icons/TechDraw_CenterLineGroup.png) [Centerline on Face](#button-techdraw_centerlinegroup); ![Cosmetic Line Through 2 Points](toolbar-icons/TechDraw_2PointCosmeticLine.png) [Cosmetic Line Through 2 Points](#button-techdraw_2pointcosmeticline); ![Edit Line Appearance](toolbar-icons/TechDraw_DecorateLine.png) [Edit Line Appearance](#button-techdraw_decorateline); ![Toggle Edge Visibility](toolbar-icons/TechDraw_ShowAll.png) [Toggle Edge Visibility](#button-techdraw_showall); ![Weld Symbol](toolbar-icons/TechDraw_WeldSymbol.png) [Weld Symbol](#button-techdraw_weldsymbol); ![Surface Finish Symbol](toolbar-icons/TechDraw_SurfaceFinishSymbols.png) [Surface Finish Symbol](#button-techdraw_surfacefinishsymbols); ![Hole/Shaft Fit](toolbar-icons/TechDraw_HoleShaftFit.png) [Hole/Shaft Fit](#button-techdraw_holeshaftfit) |

#### Changes made / buttons consolidated or omitted

- Removed from native toolbar definitions: ![Angle Dimension From 3 Points](toolbar-icons/TechDraw_3PtAngleDimension.png) [Angle Dimension From 3 Points](#button-techdraw_3ptangledimension); ![Angle Dimension](toolbar-icons/TechDraw_AngleDimension.png) [Angle Dimension](#button-techdraw_angledimension); ![Area Annotation](toolbar-icons/TechDraw_AreaDimension.png) [Area Annotation](#button-techdraw_areadimension); ![Diameter Dimension](toolbar-icons/TechDraw_DiameterDimension.png) [Diameter Dimension](#button-techdraw_diameterdimension); ![Dimension](toolbar-icons/TechDraw_Dimension.png) [Dimension](#button-techdraw_dimension); ![Arc Length Annotation](toolbar-icons/TechDraw_ExtensionArcLengthAnnotation.png) [Arc Length Annotation](#button-techdraw_extensionarclengthannotation); ![Area Annotation](toolbar-icons/TechDraw_ExtensionAreaAnnotation.png) [Area Annotation](#button-techdraw_extensionareaannotation); ![Horizontal Chamfer Dimension](toolbar-icons/TechDraw_ExtensionChamferDimensionGroup.png) [Horizontal Chamfer Dimension](#button-techdraw_extensionchamferdimensiongroup); ![Horizontal Chain Dimension](toolbar-icons/TechDraw_ExtensionCreateChainDimensionGroup.png) [Horizontal Chain Dimension](#button-techdraw_extensioncreatechaindimensiongroup); ![Horizontal Coordinate Dimension](toolbar-icons/TechDraw_ExtensionCreateCoordDimensionGroup.png) [Horizontal Coordinate Dimension](#button-techdraw_extensioncreatecoorddimensiongroup); ![Arc Length Dimension](toolbar-icons/TechDraw_ExtensionCreateLengthArc.png) [Arc Length Dimension](#button-techdraw_extensioncreatelengtharc); ![Horizontal extent](toolbar-icons/TechDraw_ExtentGroup.png) [Horizontal extent](#button-techdraw_extentgroup); ![Horizontal Length Dimension](toolbar-icons/TechDraw_HorizontalDimension.png) [Horizontal Length Dimension](#button-techdraw_horizontaldimension); ![Length Dimension](toolbar-icons/TechDraw_LengthDimension.png) [Length Dimension](#button-techdraw_lengthdimension); ![Radius Dimension](toolbar-icons/TechDraw_RadiusDimension.png) [Radius Dimension](#button-techdraw_radiusdimension); ![Vertical Length Dimension](toolbar-icons/TechDraw_VerticalDimension.png) [Vertical Length Dimension](#button-techdraw_verticaldimension).

#### Plus UI tabs and sections

**Home:** shared sections above; Home excludes the Design-only Sketch and Tools sections.

**TechDraw → Tools**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| TechDraw Pages | ![New Page](toolbar-icons/TechDraw_PageDefault.png) [New Page](#button-techdraw_pagedefault) **L**; ![New Page From Template](toolbar-icons/TechDraw_PageTemplate.png) [New Page From Template](#button-techdraw_pagetemplate) **S**; ![Update Template Fields](toolbar-icons/TechDraw_FillTemplateFields.png) [Update Template Fields](#button-techdraw_filltemplatefields) **S**; ![Redraw Page](toolbar-icons/TechDraw_RedrawPage.png) [Redraw Page](#button-techdraw_redrawpage) **S**; ![Print All Pages](toolbar-icons/TechDraw_PrintAll.png) [Print All Pages](#button-techdraw_printall) **S** |
| TechDraw Views | ![New View](toolbar-icons/TechDraw_View.png) [New View](#button-techdraw_view) **S**; ![Broken View](toolbar-icons/TechDraw_BrokenView.png) [Broken View](#button-techdraw_brokenview) **S**; ![Active View](toolbar-icons/TechDraw_ActiveView.png) [Active View](#button-techdraw_activeview) **S**; ![Section View](toolbar-icons/TechDraw_SectionGroup.png) [Section View](#button-techdraw_sectiongroup) **S** **▼**; ![Detail View](toolbar-icons/TechDraw_DetailView.png) [Detail View](#button-techdraw_detailview) **S**; ![Draft View](toolbar-icons/TechDraw_DraftView.png) [Draft View](#button-techdraw_draftview) **S**; ![Spreadsheet View](toolbar-icons/TechDraw_SpreadsheetView.png) [Spreadsheet View](#button-techdraw_spreadsheetview) **S**; ![Clip Group](toolbar-icons/TechDraw_ClipGroup.png) [Clip Group](#button-techdraw_clipgroup) **S** |
| TechDraw Stacking | ![Stack Top](toolbar-icons/TechDraw_StackGroup.png) [Stack Top](#button-techdraw_stackgroup) **S** **▼** |
| TechDraw Dimensions | ![Dimension](toolbar-icons/TechDraw_CompDimensionTools.png) [Dimension](#button-techdraw_compdimensiontools) **S** **▼**; ![Balloon Annotation](toolbar-icons/TechDraw_Balloon.png) [Balloon Annotation](#button-techdraw_balloon) **S**; ![Axonometric Length Dimension](toolbar-icons/TechDraw_AxoLengthDimension.png) [Axonometric Length Dimension](#button-techdraw_axolengthdimension) **S**; ![Repair Dimension References](toolbar-icons/TechDraw_DimensionRepair.png) [Repair Dimension References](#button-techdraw_dimensionrepair) **S** |
| TechDraw Attributes | ![Select Line Attributes, Cascade Spacing and Delta Distance](toolbar-icons/TechDraw_ExtensionSelectLineAttributes.png) [Select Line Attributes, Cascade Spacing and Delta Distance](#button-techdraw_extensionselectlineattributes) **S**; ![Change Line Attributes](toolbar-icons/TechDraw_ExtensionChangeLineAttributes.png) [Change Line Attributes](#button-techdraw_extensionchangelineattributes) **S**; ![Extend Line](toolbar-icons/TechDraw_ExtensionExtendShortenLineGroup.png) [Extend Line](#button-techdraw_extensionextendshortenlinegroup) **S** **▼**; ![Toggle View Lock](toolbar-icons/TechDraw_ExtensionLockUnlockView.png) [Toggle View Lock](#button-techdraw_extensionlockunlockview) **S**; ![Position Section View](toolbar-icons/TechDraw_ExtensionPositionSectionView.png) [Position Section View](#button-techdraw_extensionpositionsectionview) **S**; ![Customize Format Label](toolbar-icons/TechDraw_ExtensionCustomizeFormat.png) [Customize Format Label](#button-techdraw_extensioncustomizeformat) **S** |
| TechDraw Centerlines | ![Circle Centerlines](toolbar-icons/TechDraw_ExtensionCircleCenterLinesGroup.png) [Circle Centerlines](#button-techdraw_extensioncirclecenterlinesgroup) **S** **▼**; ![Cosmetic Thread Hole Side View](toolbar-icons/TechDraw_ExtensionThreadsGroup.png) [Cosmetic Thread Hole Side View](#button-techdraw_extensionthreadsgroup) **S** **▼**; ![Cosmetic Intersection Vertices](toolbar-icons/TechDraw_CommandVertexCreationGroup.png) [Cosmetic Intersection Vertices](#button-techdraw_commandvertexcreationgroup) **S** **▼**; ![Cosmetic 1 Point Circle](toolbar-icons/TechDraw_ExtensionDrawCirclesGroup.png) [Cosmetic 1 Point Circle](#button-techdraw_extensiondrawcirclesgroup) **S** **▼**; ![Cosmetic Parallel Line](toolbar-icons/TechDraw_ExtensionLinePPGroup.png) [Cosmetic Parallel Line](#button-techdraw_extensionlineppgroup) **S** **▼** |
| TechDraw Extend Dimensions | ![Insert '⌀' Prefix](toolbar-icons/TechDraw_ExtensionInsertPrefixGroup.png) [Insert '⌀' Prefix](#button-techdraw_extensioninsertprefixgroup) **S** **▼**; ![Increase Decimal Places](toolbar-icons/TechDraw_ExtensionIncreaseDecreaseGroup.png) [Increase Decimal Places](#button-techdraw_extensionincreasedecreasegroup) **S** **▼** |
| TechDraw File Access | ![Export Page as SVG](toolbar-icons/TechDraw_ExportPageSVG.png) [Export Page as SVG](#button-techdraw_exportpagesvg) **S**; ![Export Page as DXF](toolbar-icons/TechDraw_ExportPageDXF.png) [Export Page as DXF](#button-techdraw_exportpagedxf) **S** |
| TechDraw Decoration | ![Toggle View Frames](toolbar-icons/TechDraw_ToggleFrame.png) [Toggle View Frames](#button-techdraw_toggleframe) **S**; ![Image Hatch](toolbar-icons/TechDraw_Hatch.png) [Image Hatch](#button-techdraw_hatch) **S**; ![Geometric Hatch](toolbar-icons/TechDraw_GeometricHatch.png) [Geometric Hatch](#button-techdraw_geometrichatch) **S** |
| TechDraw Annotation | ![Rich Text Annotation](toolbar-icons/TechDraw_RichTextAnnotation.png) [Rich Text Annotation](#button-techdraw_richtextannotation) **S**; ![Leader Line](toolbar-icons/TechDraw_LeaderLine.png) [Leader Line](#button-techdraw_leaderline) **S**; ![Cosmetic Vertex](toolbar-icons/TechDraw_CosmeticVertexGroup.png) [Cosmetic Vertex](#button-techdraw_cosmeticvertexgroup) **S** **▼**; ![Centerline on Face](toolbar-icons/TechDraw_CenterLineGroup.png) [Centerline on Face](#button-techdraw_centerlinegroup) **S** **▼**; ![Cosmetic Line Through 2 Points](toolbar-icons/TechDraw_2PointCosmeticLine.png) [Cosmetic Line Through 2 Points](#button-techdraw_2pointcosmeticline) **S**; ![Edit Line Appearance](toolbar-icons/TechDraw_DecorateLine.png) [Edit Line Appearance](#button-techdraw_decorateline) **S**; ![Toggle Edge Visibility](toolbar-icons/TechDraw_ShowAll.png) [Toggle Edge Visibility](#button-techdraw_showall) **S**; ![Weld Symbol](toolbar-icons/TechDraw_WeldSymbol.png) [Weld Symbol](#button-techdraw_weldsymbol) **S**; ![Surface Finish Symbol](toolbar-icons/TechDraw_SurfaceFinishSymbols.png) [Surface Finish Symbol](#button-techdraw_surfacefinishsymbols) **S**; ![Hole/Shaft Fit](toolbar-icons/TechDraw_HoleShaftFit.png) [Hole/Shaft Fit](#button-techdraw_holeshaftfit) **S** |

**View:** shared sections above.

<a id="workbench-femworkbench"></a>
### FEM (`FemWorkbench`)

Definition: [`src/Mod/Fem/Gui/Workbench.cpp`](../../../src/Mod/Fem/Gui/Workbench.cpp). Shared Classic groups are listed once above.

**Source-only / not packaged in the inspected build.** These toolbar definitions exist in source. When the workbench is installed and registered, its Plus mode uses shared Home/View and these native groups in Tools. No executable/icon-menu acceptance is claimed for this workbench.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Model | ![New Analysis](../../../src/Mod/Fem/Gui/Resources/icons/FEM_Analysis.svg) [New Analysis](#button-fem_analysis);  · ; ![Solid Material](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialSolid.svg) [Solid Material](#button-fem_materialsolid); ![Fluid Material](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialFluid.svg) [Fluid Material](#button-fem_materialfluid); ![Non-Linear Mechanical Material](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialMechanicalNonlinear.svg) [Non-Linear Mechanical Material](#button-fem_materialmechanicalnonlinear); ![Reinforced Material (Concrete)](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialReinforced.svg) [Reinforced Material (Concrete)](#button-fem_materialreinforced); ![Material Editor](../../../src/Mod/BIM/Resources/icons/Arch_Material_Group.svg) [Material Editor](#button-fem_materialeditor);  · ; ![Beam Cross Section](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementGeometry1D.svg) [Beam Cross Section](#button-fem_elementgeometry1d); ![Beam Rotation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementRotation1D.svg) [Beam Rotation](#button-fem_elementrotation1d); ![Shell Plate Thickness](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementGeometry2D.svg) [Shell Plate Thickness](#button-fem_elementgeometry2d); ![Fluid Section for 1D Flow](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementFluid1D.svg) [Fluid Section for 1D Flow](#button-fem_elementfluid1d) |
| Electromagnetic Boundary Conditions | — [Electromagnetic Boundary Conditions](#button-fem_compemconstraints) |
| Fluid Boundary Conditions | ![Initial Flow Velocity Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialFlowVelocity.svg) [Initial Flow Velocity Condition](#button-fem_constraintinitialflowvelocity); ![Initial Pressure Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialPressure.svg) [Initial Pressure Condition](#button-fem_constraintinitialpressure);  · ; ![Flow Velocity Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintFlowVelocity.svg) [Flow Velocity Boundary Condition](#button-fem_constraintflowvelocity) |
| Geometrical Analysis Features | ![Plane Multi-Point Constraint](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintPlaneRotation.svg) [Plane Multi-Point Constraint](#button-fem_constraintplanerotation); ![Section Print Feature](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSectionPrint.svg) [Section Print Feature](#button-fem_constraintsectionprint); ![Local Coordinate System](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTransform.svg) [Local Coordinate System](#button-fem_constrainttransform) |
| Mechanical Boundary Conditions and Loads | ![Fixed Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintFixed.svg) [Fixed Boundary Condition](#button-fem_constraintfixed); ![Rigid Body Constraint](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintRigidBody.svg) [Rigid Body Constraint](#button-fem_constraintrigidbody); ![Displacement Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintDisplacement.svg) [Displacement Boundary Condition](#button-fem_constraintdisplacement); ![Contact Constraint](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintContact.svg) [Contact Constraint](#button-fem_constraintcontact); ![Tie Constraint](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTie.svg) [Tie Constraint](#button-fem_constrainttie); ![Spring Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSpring.svg) [Spring Boundary Condition](#button-fem_constraintspring);  · ; ![Force Load](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintForce.svg) [Force Load](#button-fem_constraintforce); ![Pressure Load](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintPressure.svg) [Pressure Load](#button-fem_constraintpressure); ![Centrifugal Load](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintCentrif.svg) [Centrifugal Load](#button-fem_constraintcentrif); ![Gravity Load](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSelfWeight.svg) [Gravity Load](#button-fem_constraintselfweight) |
| Thermal Boundary Conditions and Loads | ![Initial Temperature](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialTemperature.svg) [Initial Temperature](#button-fem_constraintinitialtemperature);  · ; ![Heat Flux Load](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintHeatflux.svg) [Heat Flux Load](#button-fem_constraintheatflux); ![Temperature Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTemperature.svg) [Temperature Boundary Condition](#button-fem_constrainttemperature); ![Body Heat Source](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintBodyHeatSource.svg) [Body Heat Source](#button-fem_constraintbodyheatsource) |
| Mesh | ![Mesh From Shape by Netgen](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshNetgenFromShape.svg) [Mesh From Shape by Netgen](#button-fem_meshnetgenfromshape); ![Mesh From Shape by Gmsh](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshGmshFromShape.svg) [Mesh From Shape by Gmsh](#button-fem_meshgmshfromshape);  · ; ![Mesh Refinement](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshRegion.svg) [Mesh Refinement](#button-fem_meshregion); ![Mesh Group](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshGroup.svg) [Mesh Group](#button-fem_meshgroup); — [GMSH Refinements](#button-fem_meshgmshrefinement);  · ; ![FEM Mesh to Mesh](../../../src/Mod/Fem/Gui/Resources/icons/FEM_FEMMesh2Mesh.svg) [FEM Mesh to Mesh](#button-fem_femmesh2mesh) |
| Solve | — [Solvers](#button-fem_compsolvers);  · ; — [Mechanical Equations](#button-fem_compmechequations); — [Electromagnetic Equations](#button-fem_compemequations); ![Flow Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationFlow.svg) [Flow Equation](#button-fem_equationflow); ![Flux Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationFlux.svg) [Flux Equation](#button-fem_equationflux); ![Heat Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationHeat.svg) [Heat Equation](#button-fem_equationheat);  · ; ![Solver Job Control](../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverControl.svg) [Solver Job Control](#button-fem_solvercontrol); ![Run Solver](../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverRun.svg) [Run Solver](#button-fem_solverrun) |
| Results | ![Purge Results](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ResultsPurge.svg) [Purge Results](#button-fem_resultspurge); ![Show Result](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ResultShow.svg) [Show Result](#button-fem_resultshow);  · ; ![Apply Changes to Pipeline](../../../src/Gui/Icons/view-refresh.svg) [Apply Changes to Pipeline](#button-fem_postapplychanges); ![Post Pipeline From Result](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostPipelineFromResult.svg) [Post Pipeline From Result](#button-fem_postpipelinefromresult); ![Pipeline Branch](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostBranchFilter.svg) [Pipeline Branch](#button-fem_postbranchfilter);  · ; ![Warp Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterWarp.svg) [Warp Filter](#button-fem_postfilterwarp); ![Scalar Clip Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterClipScalar.svg) [Scalar Clip Filter](#button-fem_postfilterclipscalar); ![Function Cut Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterCutFunction.svg) [Function Cut Filter](#button-fem_postfiltercutfunction); ![Region Clip Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterClipRegion.svg) [Region Clip Filter](#button-fem_postfilterclipregion); ![Contours Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterContours.svg) [Contours Filter](#button-fem_postfiltercontours); ![Glyph Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterGlyph.svg) [Glyph Filter](#button-fem_postfilterglyph); ![Line Clip Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterDataAlongLine.svg) [Line Clip Filter](#button-fem_postfilterdataalongline); ![Stress Linearization Plot](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterLinearizedStresses.svg) [Stress Linearization Plot](#button-fem_postfilterlinearizedstresses); ![Data at Point Clip Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterDataAtPoint.svg) [Data at Point Clip Filter](#button-fem_postfilterdataatpoint); ![Calculator Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterCalculator.svg) [Calculator Filter](#button-fem_postfiltercalculator);  · ; — [Filter Functions](#button-fem_postcreatefunctions); — [Data Visualizations](#button-fem_postvisualization) |
| Utilities | ![Clipping Plane on Face](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ClippingPlaneAdd.svg) [Clipping Plane on Face](#button-fem_clippingplaneadd); ![Remove All Clipping Planes](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ClippingPlaneRemoveAll.svg) [Remove All Clipping Planes](#button-fem_clippingplaneremoveall); ![FEM Examples](../../../src/Mod/Fem/Gui/Resources/icons/FemWorkbench.svg) [FEM Examples](#button-fem_examples) |

#### Changes made / buttons consolidated or omitted

- No workbench-specific toolbar command removal found in the compared definitions; Plus changes presentation/routing and applies the shared Home/View rules above.

#### Plus UI tabs and sections

**FEM → Tools**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Model | ![New Analysis](../../../src/Mod/Fem/Gui/Resources/icons/FEM_Analysis.svg) [New Analysis](#button-fem_analysis) **S**; ![Solid Material](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialSolid.svg) [Solid Material](#button-fem_materialsolid) **S**; ![Fluid Material](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialFluid.svg) [Fluid Material](#button-fem_materialfluid) **S**; ![Non-Linear Mechanical Material](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialMechanicalNonlinear.svg) [Non-Linear Mechanical Material](#button-fem_materialmechanicalnonlinear) **S**; ![Reinforced Material (Concrete)](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialReinforced.svg) [Reinforced Material (Concrete)](#button-fem_materialreinforced) **S**; ![Material Editor](../../../src/Mod/BIM/Resources/icons/Arch_Material_Group.svg) [Material Editor](#button-fem_materialeditor) **S**; ![Beam Cross Section](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementGeometry1D.svg) [Beam Cross Section](#button-fem_elementgeometry1d) **S**; ![Beam Rotation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementRotation1D.svg) [Beam Rotation](#button-fem_elementrotation1d) **S**; ![Shell Plate Thickness](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementGeometry2D.svg) [Shell Plate Thickness](#button-fem_elementgeometry2d) **S**; ![Fluid Section for 1D Flow](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementFluid1D.svg) [Fluid Section for 1D Flow](#button-fem_elementfluid1d) **S** |
| Electromagnetic Boundary Conditions | — [Electromagnetic Boundary Conditions](#button-fem_compemconstraints) **S** |
| Fluid Boundary Conditions | ![Initial Flow Velocity Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialFlowVelocity.svg) [Initial Flow Velocity Condition](#button-fem_constraintinitialflowvelocity) **S**; ![Initial Pressure Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialPressure.svg) [Initial Pressure Condition](#button-fem_constraintinitialpressure) **S**; ![Flow Velocity Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintFlowVelocity.svg) [Flow Velocity Boundary Condition](#button-fem_constraintflowvelocity) **S** |
| Geometrical Analysis Features | ![Plane Multi-Point Constraint](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintPlaneRotation.svg) [Plane Multi-Point Constraint](#button-fem_constraintplanerotation) **S**; ![Section Print Feature](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSectionPrint.svg) [Section Print Feature](#button-fem_constraintsectionprint) **S**; ![Local Coordinate System](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTransform.svg) [Local Coordinate System](#button-fem_constrainttransform) **S** |
| Mechanical Boundary Conditions and Loads | ![Fixed Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintFixed.svg) [Fixed Boundary Condition](#button-fem_constraintfixed) **S**; ![Rigid Body Constraint](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintRigidBody.svg) [Rigid Body Constraint](#button-fem_constraintrigidbody) **S**; ![Displacement Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintDisplacement.svg) [Displacement Boundary Condition](#button-fem_constraintdisplacement) **S**; ![Contact Constraint](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintContact.svg) [Contact Constraint](#button-fem_constraintcontact) **S**; ![Tie Constraint](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTie.svg) [Tie Constraint](#button-fem_constrainttie) **S**; ![Spring Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSpring.svg) [Spring Boundary Condition](#button-fem_constraintspring) **S**; ![Force Load](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintForce.svg) [Force Load](#button-fem_constraintforce) **S**; ![Pressure Load](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintPressure.svg) [Pressure Load](#button-fem_constraintpressure) **S**; ![Centrifugal Load](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintCentrif.svg) [Centrifugal Load](#button-fem_constraintcentrif) **S**; ![Gravity Load](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSelfWeight.svg) [Gravity Load](#button-fem_constraintselfweight) **S** |
| Thermal Boundary Conditions and Loads | ![Initial Temperature](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialTemperature.svg) [Initial Temperature](#button-fem_constraintinitialtemperature) **S**; ![Heat Flux Load](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintHeatflux.svg) [Heat Flux Load](#button-fem_constraintheatflux) **S**; ![Temperature Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTemperature.svg) [Temperature Boundary Condition](#button-fem_constrainttemperature) **S**; ![Body Heat Source](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintBodyHeatSource.svg) [Body Heat Source](#button-fem_constraintbodyheatsource) **S** |
| Mesh | ![Mesh From Shape by Netgen](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshNetgenFromShape.svg) [Mesh From Shape by Netgen](#button-fem_meshnetgenfromshape) **S**; ![Mesh From Shape by Gmsh](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshGmshFromShape.svg) [Mesh From Shape by Gmsh](#button-fem_meshgmshfromshape) **S**; ![Mesh Refinement](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshRegion.svg) [Mesh Refinement](#button-fem_meshregion) **S**; ![Mesh Group](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshGroup.svg) [Mesh Group](#button-fem_meshgroup) **S**; — [GMSH Refinements](#button-fem_meshgmshrefinement) **S**; ![FEM Mesh to Mesh](../../../src/Mod/Fem/Gui/Resources/icons/FEM_FEMMesh2Mesh.svg) [FEM Mesh to Mesh](#button-fem_femmesh2mesh) **S** |
| Solve | — [Solvers](#button-fem_compsolvers) **S**; — [Mechanical Equations](#button-fem_compmechequations) **S**; — [Electromagnetic Equations](#button-fem_compemequations) **S**; ![Flow Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationFlow.svg) [Flow Equation](#button-fem_equationflow) **S**; ![Flux Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationFlux.svg) [Flux Equation](#button-fem_equationflux) **S**; ![Heat Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationHeat.svg) [Heat Equation](#button-fem_equationheat) **S**; ![Solver Job Control](../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverControl.svg) [Solver Job Control](#button-fem_solvercontrol) **S**; ![Run Solver](../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverRun.svg) [Run Solver](#button-fem_solverrun) **S** |
| Results | ![Purge Results](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ResultsPurge.svg) [Purge Results](#button-fem_resultspurge) **S**; ![Show Result](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ResultShow.svg) [Show Result](#button-fem_resultshow) **S**; ![Apply Changes to Pipeline](../../../src/Gui/Icons/view-refresh.svg) [Apply Changes to Pipeline](#button-fem_postapplychanges) **S**; ![Post Pipeline From Result](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostPipelineFromResult.svg) [Post Pipeline From Result](#button-fem_postpipelinefromresult) **S**; ![Pipeline Branch](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostBranchFilter.svg) [Pipeline Branch](#button-fem_postbranchfilter) **S**; ![Warp Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterWarp.svg) [Warp Filter](#button-fem_postfilterwarp) **S**; ![Scalar Clip Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterClipScalar.svg) [Scalar Clip Filter](#button-fem_postfilterclipscalar) **S**; ![Function Cut Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterCutFunction.svg) [Function Cut Filter](#button-fem_postfiltercutfunction) **S**; ![Region Clip Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterClipRegion.svg) [Region Clip Filter](#button-fem_postfilterclipregion) **S**; ![Contours Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterContours.svg) [Contours Filter](#button-fem_postfiltercontours) **S**; ![Glyph Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterGlyph.svg) [Glyph Filter](#button-fem_postfilterglyph) **S**; ![Line Clip Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterDataAlongLine.svg) [Line Clip Filter](#button-fem_postfilterdataalongline) **S**; ![Stress Linearization Plot](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterLinearizedStresses.svg) [Stress Linearization Plot](#button-fem_postfilterlinearizedstresses) **S**; ![Data at Point Clip Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterDataAtPoint.svg) [Data at Point Clip Filter](#button-fem_postfilterdataatpoint) **S**; ![Calculator Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterCalculator.svg) [Calculator Filter](#button-fem_postfiltercalculator) **S**; — [Filter Functions](#button-fem_postcreatefunctions) **S**; — [Data Visualizations](#button-fem_postvisualization) **S** |
| Utilities | ![Clipping Plane on Face](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ClippingPlaneAdd.svg) [Clipping Plane on Face](#button-fem_clippingplaneadd) **S**; ![Remove All Clipping Planes](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ClippingPlaneRemoveAll.svg) [Remove All Clipping Planes](#button-fem_clippingplaneremoveall) **S**; ![FEM Examples](../../../src/Mod/Fem/Gui/Resources/icons/FemWorkbench.svg) [FEM Examples](#button-fem_examples) **S** |

<a id="workbench-spreadsheetworkbench"></a>
### Spreadsheet (`SpreadsheetWorkbench`)

Definition: [`src/Mod/Spreadsheet/Gui/Workbench.cpp`](../../../src/Mod/Spreadsheet/Gui/Workbench.cpp). Shared Classic groups are listed once above.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Spreadsheet | ![New Spreadsheet](toolbar-icons/Spreadsheet_CreateSheet.png) [New Spreadsheet](#button-spreadsheet_createsheet);  · ; ![Import Spreadsheet](toolbar-icons/Spreadsheet_Import.png) [Import Spreadsheet](#button-spreadsheet_import); ![Export Spreadsheet](toolbar-icons/Spreadsheet_Export.png) [Export Spreadsheet](#button-spreadsheet_export);  · ; ![Merge Cells](toolbar-icons/Spreadsheet_MergeCells.png) [Merge Cells](#button-spreadsheet_mergecells); ![Split Cell](toolbar-icons/Spreadsheet_SplitCell.png) [Split Cell](#button-spreadsheet_splitcell);  · ; ![Align Left](toolbar-icons/Spreadsheet_AlignLeft.png) [Align Left](#button-spreadsheet_alignleft); ![Align Horizontal Center](toolbar-icons/Spreadsheet_AlignCenter.png) [Align Horizontal Center](#button-spreadsheet_aligncenter); ![Align Right](toolbar-icons/Spreadsheet_AlignRight.png) [Align Right](#button-spreadsheet_alignright); ![Align Top](toolbar-icons/Spreadsheet_AlignTop.png) [Align Top](#button-spreadsheet_aligntop); ![Align Vertical Center](toolbar-icons/Spreadsheet_AlignVCenter.png) [Align Vertical Center](#button-spreadsheet_alignvcenter); ![Align Bottom](toolbar-icons/Spreadsheet_AlignBottom.png) [Align Bottom](#button-spreadsheet_alignbottom);  · ; ![Bold Text](toolbar-icons/Spreadsheet_StyleBold.png) [Bold Text](#button-spreadsheet_stylebold); ![Italic Text](toolbar-icons/Spreadsheet_StyleItalic.png) [Italic Text](#button-spreadsheet_styleitalic); ![Underline Text](toolbar-icons/Spreadsheet_StyleUnderline.png) [Underline Text](#button-spreadsheet_styleunderline);  · ; ![Set Alias](toolbar-icons/Spreadsheet_SetAlias.png) [Set Alias](#button-spreadsheet_setalias);  ·  |

#### Changes made / buttons consolidated or omitted

- No workbench-specific toolbar command removal found in the compared definitions; Plus changes presentation/routing and applies the shared Home/View rules above.

#### Plus UI tabs and sections

**Home:** shared sections above; Home excludes the Design-only Sketch and Tools sections.

**Spreadsheet → Tools**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Spreadsheet | ![New Spreadsheet](toolbar-icons/Spreadsheet_CreateSheet.png) [New Spreadsheet](#button-spreadsheet_createsheet) **S**; ![Import Spreadsheet](toolbar-icons/Spreadsheet_Import.png) [Import Spreadsheet](#button-spreadsheet_import) **S**; ![Export Spreadsheet](toolbar-icons/Spreadsheet_Export.png) [Export Spreadsheet](#button-spreadsheet_export) **S**; ![Merge Cells](toolbar-icons/Spreadsheet_MergeCells.png) [Merge Cells](#button-spreadsheet_mergecells) **S**; ![Split Cell](toolbar-icons/Spreadsheet_SplitCell.png) [Split Cell](#button-spreadsheet_splitcell) **S**; ![Align Left](toolbar-icons/Spreadsheet_AlignLeft.png) [Align Left](#button-spreadsheet_alignleft) **S**; ![Align Horizontal Center](toolbar-icons/Spreadsheet_AlignCenter.png) [Align Horizontal Center](#button-spreadsheet_aligncenter) **S**; ![Align Right](toolbar-icons/Spreadsheet_AlignRight.png) [Align Right](#button-spreadsheet_alignright) **S**; ![Align Top](toolbar-icons/Spreadsheet_AlignTop.png) [Align Top](#button-spreadsheet_aligntop) **S**; ![Align Vertical Center](toolbar-icons/Spreadsheet_AlignVCenter.png) [Align Vertical Center](#button-spreadsheet_alignvcenter) **S**; ![Align Bottom](toolbar-icons/Spreadsheet_AlignBottom.png) [Align Bottom](#button-spreadsheet_alignbottom) **S**; ![Bold Text](toolbar-icons/Spreadsheet_StyleBold.png) [Bold Text](#button-spreadsheet_stylebold) **S**; ![Italic Text](toolbar-icons/Spreadsheet_StyleItalic.png) [Italic Text](#button-spreadsheet_styleitalic) **S**; ![Underline Text](toolbar-icons/Spreadsheet_StyleUnderline.png) [Underline Text](#button-spreadsheet_styleunderline) **S**; ![Set Alias](toolbar-icons/Spreadsheet_SetAlias.png) [Set Alias](#button-spreadsheet_setalias) **S** |

**View:** shared sections above.

<a id="workbench-materialworkbench"></a>
### Material (`MaterialWorkbench`)

Definition: [`src/Mod/Material/Gui/Workbench.cpp`](../../../src/Mod/Material/Gui/Workbench.cpp). Shared Classic groups are listed once above.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Material | ![Edit](toolbar-icons/Material_Edit.png) [Edit](#button-material_edit) |

#### Changes made / buttons consolidated or omitted

- No workbench-specific toolbar command removal found in the compared definitions; Plus changes presentation/routing and applies the shared Home/View rules above.

#### Plus UI tabs and sections

**Home:** shared sections above; Home excludes the Design-only Sketch and Tools sections.

**Material → Tools**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Material | ![Edit](toolbar-icons/Material_Edit.png) [Edit](#button-material_edit) **S** |

**View:** shared sections above.

<a id="workbench-meshpartworkbench"></a>
### MeshPart (`MeshPartWorkbench`)

Definition: [`src/Mod/MeshPart/Gui/Workbench.cpp`](../../../src/Mod/MeshPart/Gui/Workbench.cpp). Shared Classic groups are listed once above.

**Source-only / not packaged in the inspected build.** These toolbar definitions exist in source. When the workbench is installed and registered, its Plus mode uses shared Home/View and these native groups in Tools. No executable/icon-menu acceptance is claimed for this workbench.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| MeshPart | ![Mesh From Shape](../../../src/Gui/Icons/preferences-general.svg) [Mesh From Shape](#button-meshpart_mesher) |

#### Changes made / buttons consolidated or omitted

- No workbench-specific toolbar command removal found in the compared definitions; Plus changes presentation/routing and applies the shared Home/View rules above.

#### Plus UI tabs and sections

**MeshPart → Tools**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| MeshPart | ![Mesh From Shape](../../../src/Gui/Icons/preferences-general.svg) [Mesh From Shape](#button-meshpart_mesher) **S** |

<a id="workbench-pointsworkbench"></a>
### Points (`PointsWorkbench`)

Definition: [`src/Mod/Points/Gui/Workbench.cpp`](../../../src/Mod/Points/Gui/Workbench.cpp). Shared Classic groups are listed once above.

**Source-only / not packaged in the inspected build.** These toolbar definitions exist in source. When the workbench is installed and registered, its Plus mode uses shared Home/View and these native groups in Tools. No executable/icon-menu acceptance is claimed for this workbench.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Points Tools | ![Import Points…](../../../src/Mod/Points/Gui/Resources/icons/Points_Import_Point_cloud.svg) [Import Points…](#button-points_import); ![Export Points…](../../../src/Mod/Points/Gui/Resources/icons/Points_Export_Point_cloud.svg) [Export Points…](#button-points_export);  · ; ![Convert to Points](../../../src/Mod/Points/Gui/Resources/icons/Points_Convert.svg) [Convert to Points](#button-points_convert); ![Structured Point Cloud](../../../src/Mod/Points/Gui/Resources/icons/Points_Structure.svg) [Structured Point Cloud](#button-points_structure); ![Merge Point Clouds](../../../src/Mod/Points/Gui/Resources/icons/Points_Merge.svg) [Merge Point Clouds](#button-points_merge); ![Cut Point Cloud](../../../src/Gui/Icons/PolygonPick.svg) [Cut Point Cloud](#button-points_polycut) |

#### Changes made / buttons consolidated or omitted

- No workbench-specific toolbar command removal found in the compared definitions; Plus changes presentation/routing and applies the shared Home/View rules above.

#### Plus UI tabs and sections

**Points → Tools**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Points Tools | ![Import Points…](../../../src/Mod/Points/Gui/Resources/icons/Points_Import_Point_cloud.svg) [Import Points…](#button-points_import) **S**; ![Export Points…](../../../src/Mod/Points/Gui/Resources/icons/Points_Export_Point_cloud.svg) [Export Points…](#button-points_export) **S**; ![Convert to Points](../../../src/Mod/Points/Gui/Resources/icons/Points_Convert.svg) [Convert to Points](#button-points_convert) **S**; ![Structured Point Cloud](../../../src/Mod/Points/Gui/Resources/icons/Points_Structure.svg) [Structured Point Cloud](#button-points_structure) **S**; ![Merge Point Clouds](../../../src/Mod/Points/Gui/Resources/icons/Points_Merge.svg) [Merge Point Clouds](#button-points_merge) **S**; ![Cut Point Cloud](../../../src/Gui/Icons/PolygonPick.svg) [Cut Point Cloud](#button-points_polycut) **S** |

<a id="workbench-robotworkbench"></a>
### Robot (`RobotWorkbench`)

Definition: [`src/Mod/Robot/Gui/Workbench.cpp`](../../../src/Mod/Robot/Gui/Workbench.cpp). Shared Classic groups are listed once above.

**Source-only / not packaged in the inspected build.** These toolbar definitions exist in source. When the workbench is installed and registered, its Plus mode uses shared Home/View and these native groups in Tools. No executable/icon-menu acceptance is claimed for this workbench.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Robot | ![Place Robot](../../../src/Mod/Robot/Gui/Resources/icons/Robot_CreateRobot.svg) [Place Robot](#button-robot_create);  · ; ![Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_CreateTrajectory.svg) [Trajectory](#button-robot_createtrajectory); ![Insert in Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_InsertWaypoint.svg) [Insert in Trajectory](#button-robot_insertwaypoint); ![Insert in Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_InsertWaypointPre.svg) [Insert in Trajectory](#button-robot_insertwaypointpreselect);  · ; ![Edge to Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_Edge2Trac.svg) [Edge to Trajectory](#button-robot_edge2trac); ![Dress-Up Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_TrajectoryDressUp.svg) [Dress-Up Trajectory](#button-robot_trajectorydressup); ![Trajectory Compound](../../../src/Mod/Robot/Gui/Resources/icons/Robot_TrajectoryCompound.svg) [Trajectory Compound](#button-robot_trajectorycompound);  · ; ![Set Home Position](../../../src/Mod/Robot/Gui/Resources/icons/Robot_SetHomePos.svg) [Set Home Position](#button-robot_sethomepos); ![Move to Home](../../../src/Mod/Robot/Gui/Resources/icons/Robot_RestoreHomePos.svg) [Move to Home](#button-robot_restorehomepos);  · ; ![Simulate Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_Simulate.svg) [Simulate Trajectory](#button-robot_simulate) |

#### Changes made / buttons consolidated or omitted

- No workbench-specific toolbar command removal found in the compared definitions; Plus changes presentation/routing and applies the shared Home/View rules above.

#### Plus UI tabs and sections

**Robot → Tools**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Robot | ![Place Robot](../../../src/Mod/Robot/Gui/Resources/icons/Robot_CreateRobot.svg) [Place Robot](#button-robot_create) **S**; ![Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_CreateTrajectory.svg) [Trajectory](#button-robot_createtrajectory) **S**; ![Insert in Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_InsertWaypoint.svg) [Insert in Trajectory](#button-robot_insertwaypoint) **S**; ![Insert in Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_InsertWaypointPre.svg) [Insert in Trajectory](#button-robot_insertwaypointpreselect) **S**; ![Edge to Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_Edge2Trac.svg) [Edge to Trajectory](#button-robot_edge2trac) **S**; ![Dress-Up Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_TrajectoryDressUp.svg) [Dress-Up Trajectory](#button-robot_trajectorydressup) **S**; ![Trajectory Compound](../../../src/Mod/Robot/Gui/Resources/icons/Robot_TrajectoryCompound.svg) [Trajectory Compound](#button-robot_trajectorycompound) **S**; ![Set Home Position](../../../src/Mod/Robot/Gui/Resources/icons/Robot_SetHomePos.svg) [Set Home Position](#button-robot_sethomepos) **S**; ![Move to Home](../../../src/Mod/Robot/Gui/Resources/icons/Robot_RestoreHomePos.svg) [Move to Home](#button-robot_restorehomepos) **S**; ![Simulate Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_Simulate.svg) [Simulate Trajectory](#button-robot_simulate) **S** |

<a id="workbench-reverseengineeringworkbench"></a>
### ReverseEngineering (`ReverseEngineeringWorkbench`)

Definition: [`src/Mod/ReverseEngineering/Gui/Workbench.cpp`](../../../src/Mod/ReverseEngineering/Gui/Workbench.cpp). Shared Classic groups are listed once above.

**Source-only / not packaged in the inspected build.** These toolbar definitions exist in source. When the workbench is installed and registered, its Plus mode uses shared Home/View and these native groups in Tools. No executable/icon-menu acceptance is claimed for this workbench.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Reverse Engineering | ![Approximate B-Spline Surface…](../../../src/Mod/ReverseEngineering/Gui/Resources/icons/actions/FitSurface.svg) [Approximate B-Spline Surface…](#button-reen_approxsurface) |

#### Changes made / buttons consolidated or omitted

- No workbench-specific toolbar command removal found in the compared definitions; Plus changes presentation/routing and applies the shared Home/View rules above.

#### Plus UI tabs and sections

**ReverseEngineering → Tools**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Reverse Engineering | ![Approximate B-Spline Surface…](../../../src/Mod/ReverseEngineering/Gui/Resources/icons/actions/FitSurface.svg) [Approximate B-Spline Surface…](#button-reen_approxsurface) **S** |

<a id="workbench-inspectionworkbench"></a>
### Inspection (`InspectionWorkbench`)

Definition: [`src/Mod/Inspection/Gui/Workbench.cpp`](../../../src/Mod/Inspection/Gui/Workbench.cpp). Shared Classic groups are listed once above.

**Source-only / not packaged in the inspected build.** These toolbar definitions exist in source. When the workbench is installed and registered, its Plus mode uses shared Home/View and these native groups in Tools. No executable/icon-menu acceptance is claimed for this workbench.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Inspection | ![Visual Inspection](../../../src/Mod/Inspection/Gui/Resources/icons/InspectionWorkbench.svg) [Visual Inspection](#button-inspection_visualinspection); ![Inspection…](../../../src/Mod/Inspection/Gui/Resources/icons/inspect_pipette.svg) [Inspection…](#button-inspection_inspectelement) |

#### Changes made / buttons consolidated or omitted

- No workbench-specific toolbar command removal found in the compared definitions; Plus changes presentation/routing and applies the shared Home/View rules above.

#### Plus UI tabs and sections

**Inspection → Tools**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Inspection | ![Visual Inspection](../../../src/Mod/Inspection/Gui/Resources/icons/InspectionWorkbench.svg) [Visual Inspection](#button-inspection_visualinspection) **S**; ![Inspection…](../../../src/Mod/Inspection/Gui/Resources/icons/inspect_pipette.svg) [Inspection…](#button-inspection_inspectelement) **S** |

<a id="workbench-bimworkbench"></a>
### BIM (`BIMWorkbench`)

Definition: [`src/Mod/BIM/InitGui.py`](../../../src/Mod/BIM/InitGui.py). Shared Classic groups are listed once above.

**Source-only / not packaged in the inspected build.** These toolbar definitions exist in source. When the workbench is installed and registered, its Plus mode uses shared Home/View and these native groups in Tools. No executable/icon-menu acceptance is claimed for this workbench.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Drafting Tools | ![New Sketch](../../../src/Mod/BIM/Resources/icons/Sketch.svg) [New Sketch](#button-bim_sketch); ![Line](toolbar-icons/Draft_Line.png) [Line](#button-draft_line); ![Polyline](toolbar-icons/Draft_Wire.png) [Polyline](#button-draft_wire); ![Rectangle](toolbar-icons/Draft_Rectangle.png) [Rectangle](#button-draft_rectangle); ![Arc Tools](../../../src/Mod/Draft/Resources/icons/Draft_Arc.svg) [Arc Tools](#button-bim_arctools); ![Circle](toolbar-icons/Draft_Circle.png) [Circle](#button-draft_circle); ![Ellipse](toolbar-icons/Draft_Ellipse.png) [Ellipse](#button-draft_ellipse); ![Polygon](toolbar-icons/Draft_Polygon.png) [Polygon](#button-draft_polygon); ![Spline Tools](../../../src/Mod/Draft/Resources/icons/Draft_BSpline.svg) [Spline Tools](#button-bim_splinetools); ![Point](toolbar-icons/Draft_Point.png) [Point](#button-draft_point); ![Fillet](toolbar-icons/Draft_Fillet.png) [Fillet](#button-draft_fillet) |
| Draft Snap | ![Snap Lock](toolbar-icons/Draft_Snap_Lock.png) [Snap Lock](#button-draft_snap_lock); ![Snap Endpoint](toolbar-icons/Draft_Snap_Endpoint.png) [Snap Endpoint](#button-draft_snap_endpoint); ![Snap Midpoint](toolbar-icons/Draft_Snap_Midpoint.png) [Snap Midpoint](#button-draft_snap_midpoint); ![Snap Center](toolbar-icons/Draft_Snap_Center.png) [Snap Center](#button-draft_snap_center); ![Snap Angle](toolbar-icons/Draft_Snap_Angle.png) [Snap Angle](#button-draft_snap_angle); ![Snap Intersection](toolbar-icons/Draft_Snap_Intersection.png) [Snap Intersection](#button-draft_snap_intersection); ![Snap Perpendicular](toolbar-icons/Draft_Snap_Perpendicular.png) [Snap Perpendicular](#button-draft_snap_perpendicular); ![Snap Extension](toolbar-icons/Draft_Snap_Extension.png) [Snap Extension](#button-draft_snap_extension); ![Snap Parallel](toolbar-icons/Draft_Snap_Parallel.png) [Snap Parallel](#button-draft_snap_parallel); ![Snap Special](toolbar-icons/Draft_Snap_Special.png) [Snap Special](#button-draft_snap_special); ![Snap Near](toolbar-icons/Draft_Snap_Near.png) [Snap Near](#button-draft_snap_near); ![Snap Ortho](toolbar-icons/Draft_Snap_Ortho.png) [Snap Ortho](#button-draft_snap_ortho); ![Snap Grid](toolbar-icons/Draft_Snap_Grid.png) [Snap Grid](#button-draft_snap_grid); ![Snap Working Plane](toolbar-icons/Draft_Snap_WorkingPlane.png) [Snap Working Plane](#button-draft_snap_workingplane); ![Snap Dimensions](toolbar-icons/Draft_Snap_Dimensions.png) [Snap Dimensions](#button-draft_snap_dimensions);  · ; ![Toggle Grid](toolbar-icons/Draft_ToggleGrid.png) [Toggle Grid](#button-draft_togglegrid) |
| 3D/BIM Tools | ![Site](../../../src/Mod/BIM/Resources/icons/Arch_Site.svg) [Site](#button-arch_site); ![Building](../../../src/Mod/BIM/Resources/icons/Arch_Building.svg) [Building](#button-arch_building); ![Level](../../../src/Mod/BIM/Resources/icons/Arch_Floor.svg) [Level](#button-arch_level); ![Space](../../../src/Mod/BIM/Resources/icons/Arch_Space.svg) [Space](#button-arch_space);  · ; ![Wall](../../../src/Mod/BIM/Resources/icons/Arch_Wall.svg) [Wall](#button-arch_wall); ![Curtain Wall](../../../src/Mod/BIM/Resources/icons/Arch_CurtainWall.svg) [Curtain Wall](#button-arch_curtainwall); ![Column](../../../src/Mod/BIM/Resources/icons/BIM_Column.svg) [Column](#button-bim_column); ![Beam](../../../src/Mod/BIM/Resources/icons/BIM_Beam.svg) [Beam](#button-bim_beam); ![Slab](../../../src/Mod/BIM/Resources/icons/BIM_Slab.svg) [Slab](#button-bim_slab); ![Door](../../../src/Mod/BIM/Resources/icons/BIM_Door.svg) [Door](#button-bim_door); ![Window](../../../src/Mod/BIM/Resources/icons/Arch_Window.svg) [Window](#button-arch_window); ![Covering](../../../src/Mod/BIM/Resources/icons/BIM_Covering.svg) [Covering](#button-bim_covering); ![Pipe](../../../src/Mod/BIM/Resources/icons/Arch_Pipe.svg) [Pipe](#button-arch_pipe); ![Connector](../../../src/Mod/BIM/Resources/icons/Arch_PipeConnector.svg) [Connector](#button-arch_pipeconnector); ![Stairs](../../../src/Mod/BIM/Resources/icons/Arch_Stairs.svg) [Stairs](#button-arch_stairs); ![Roof](../../../src/Mod/BIM/Resources/icons/Arch_Roof.svg) [Roof](#button-arch_roof); ![Panel](../../../src/Mod/BIM/Resources/icons/Arch_Panel.svg) [Panel](#button-arch_panel); ![Frame](../../../src/Mod/BIM/Resources/icons/Arch_Frame.svg) [Frame](#button-arch_frame); ![Fence](../../../src/Mod/BIM/Resources/icons/Arch_Fence.svg) [Fence](#button-arch_fence); ![Truss](../../../src/Mod/BIM/Resources/icons/Arch_Truss.svg) [Truss](#button-arch_truss); ![Equipment](../../../src/Mod/BIM/Resources/icons/Arch_Equipment.svg) [Equipment](#button-arch_equipment); ![Custom Rebar](../../../src/Mod/BIM/Resources/icons/Arch_Rebar.svg) [Custom Rebar](#button-arch_rebar); ![Generic 3D Tools](../../../src/Mod/BIM/Resources/icons/BIM_Box.svg) [Generic 3D Tools](#button-bim_generictools) |
| Annotation Tools | ![Aligned Dimension](../../../src/Mod/BIM/Resources/icons/BIM_DimensionAligned.svg) [Aligned Dimension](#button-bim_dimensionaligned); ![Horizontal Dimension](../../../src/Mod/BIM/Resources/icons/BIM_DimensionHorizontal.svg) [Horizontal Dimension](#button-bim_dimensionhorizontal); ![Vertical Dimension](../../../src/Mod/BIM/Resources/icons/BIM_DimensionVertical.svg) [Vertical Dimension](#button-bim_dimensionvertical); ![Text](../../../src/Mod/Draft/Resources/icons/Draft_Text.svg) [Text](#button-bim_text); ![Leader](../../../src/Mod/BIM/Resources/icons/BIM_Leader.svg) [Leader](#button-bim_leader); ![Label](toolbar-icons/Draft_Label.png) [Label](#button-draft_label); ![Hatch](toolbar-icons/Draft_Hatch.png) [Hatch](#button-draft_hatch); ![Axis Tools](../../../src/Mod/BIM/Resources/icons/Arch_Axis.svg) [Axis Tools](#button-bim_axistools); ![Grid](../../../src/Mod/BIM/Resources/icons/Arch_Grid.svg) [Grid](#button-arch_grid); ![Section Plane](../../../src/Mod/BIM/Resources/icons/Arch_SectionPlane.svg) [Section Plane](#button-arch_sectionplane); — [Create 2D Views](#button-bim_create2dviews); ![New Page](../../../src/Mod/BIM/Resources/icons/BIM_PageDefault.svg) [New Page](#button-bim_tdpage); ![New View](../../../src/Mod/BIM/Resources/icons/BIM_InsertView.svg) [New View](#button-bim_tdview) |
| General Tools | ![Move](toolbar-icons/Draft_Move.png) [Move](#button-draft_move); ![Rotate](toolbar-icons/Draft_Rotate.png) [Rotate](#button-draft_rotate); ![Scale](toolbar-icons/Draft_Scale.png) [Scale](#button-draft_scale); ![Mirror](toolbar-icons/Draft_Mirror.png) [Mirror](#button-draft_mirror); ![Cloning Tools](../../../src/Mod/BIM/Resources/icons/BIM_Clone.svg) [Cloning Tools](#button-bim_clonetools); ![Copy](../../../src/Mod/BIM/Resources/icons/BIM_Copy.svg) [Copy](#button-bim_copy); ![Simple Copy](../../../src/Mod/BIM/Resources/icons/Tree_Part.svg) [Simple Copy](#button-bim_simplecopy); ![Compound](../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Compound.svg) [Compound](#button-bim_compound) |
| 2D Tools | — [Offset Tools](#button-bim_offsettools); ![Trimex](../../../src/Mod/Draft/Resources/icons/Draft_Trimex.svg) [Trimex](#button-bim_trimex); ![Join](toolbar-icons/Draft_Join.png) [Join](#button-draft_join); ![Split](toolbar-icons/Draft_Split.png) [Split](#button-draft_split); ![Stretch](toolbar-icons/Draft_Stretch.png) [Stretch](#button-draft_stretch); ![Draft to Sketch](toolbar-icons/Draft_Draft2Sketch.png) [Draft to Sketch](#button-draft_draft2sketch); ![Edit](toolbar-icons/Draft_Edit.png) [Edit](#button-draft_edit) |
| Object Tools | ![Upgrade](toolbar-icons/Draft_Upgrade.png) [Upgrade](#button-draft_upgrade); ![Downgrade](toolbar-icons/Draft_Downgrade.png) [Downgrade](#button-draft_downgrade); ![Add Component](../../../src/Mod/BIM/Resources/icons/Arch_Add.svg) [Add Component](#button-arch_add); ![Remove Component](../../../src/Mod/BIM/Resources/icons/Arch_Remove.svg) [Remove Component](#button-arch_remove) |
| 3D Tools | ![Array Tools](../../../src/Mod/Draft/Resources/icons/Draft_Array.svg) [Array Tools](#button-bim_arraytools); ![Cut With Plane](../../../src/Mod/BIM/Resources/icons/Arch_CutPlane.svg) [Cut With Plane](#button-arch_cutplane); ![Extrude](../../../src/Mod/Part/Gui/Resources/icons/tools/Part_Extrude.svg) [Extrude](#button-bim_extrude); ![Extrude Face](../../../src/Mod/BIM/Resources/icons/BIM_ExtrudeFace.svg) [Extrude Face](#button-bim_extrudeface); — [Boolean Tools](#button-bim_booleantools) |
| Manage Tools | ![BIM Setup](../../../src/Gui/Icons/preferences-system.svg) [BIM Setup](#button-bim_setup); ![Setup Project](../../../src/Mod/BIM/Resources/icons/BIM_ProjectManager.svg) [Setup Project](#button-bim_projectmanager); ![Manage Doors and Windows](../../../src/Mod/BIM/Resources/icons/BIM_Windows.svg) [Manage Doors and Windows](#button-bim_windows); ![IFC Management](../../../src/Mod/BIM/Resources/icons/BIM_IfcElements.svg) [IFC Management](#button-bim_ifcmanagetools); ![Manage Layers](../../../src/Mod/BIM/Resources/icons/BIM_Layers.svg) [Manage Layers](#button-bim_layers); ![Material](../../../src/Mod/BIM/Resources/icons/BIM_Material.svg) [Material](#button-bim_material); ![Report Tools](../../../src/Mod/BIM/Resources/icons/BIM_Report.svg) [Report Tools](#button-bim_reporttools); ![Preflight Checks](../../../src/Mod/BIM/Resources/icons/BIM_Preflight.svg) [Preflight Checks](#button-bim_preflight); ![Annotation Styles](toolbar-icons/Draft_AnnotationStyleEditor.png) [Annotation Styles](#button-draft_annotationstyleeditor) |

#### Changes made / buttons consolidated or omitted

- Optional Reinforcement addons replace Rebar with their own dropdown; other addon menus depend on installation. The lists below cover built-in commands, not an invented addon inventory.
- No workbench-specific toolbar command removal found in the compared definitions; Plus changes presentation/routing and applies the shared Home/View rules above.

#### Plus UI tabs and sections

**BIM → Tools**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| Drafting Tools | ![New Sketch](../../../src/Mod/BIM/Resources/icons/Sketch.svg) [New Sketch](#button-bim_sketch) **S**; ![Line](toolbar-icons/Draft_Line.png) [Line](#button-draft_line) **L**; ![Polyline](toolbar-icons/Draft_Wire.png) [Polyline](#button-draft_wire) **L**; ![Rectangle](toolbar-icons/Draft_Rectangle.png) [Rectangle](#button-draft_rectangle) **S**; ![Arc Tools](../../../src/Mod/Draft/Resources/icons/Draft_Arc.svg) [Arc Tools](#button-bim_arctools) **S**; ![Circle](toolbar-icons/Draft_Circle.png) [Circle](#button-draft_circle) **S**; ![Ellipse](toolbar-icons/Draft_Ellipse.png) [Ellipse](#button-draft_ellipse) **S**; ![Polygon](toolbar-icons/Draft_Polygon.png) [Polygon](#button-draft_polygon) **S**; ![Spline Tools](../../../src/Mod/Draft/Resources/icons/Draft_BSpline.svg) [Spline Tools](#button-bim_splinetools) **S**; ![Point](toolbar-icons/Draft_Point.png) [Point](#button-draft_point) **S**; ![Fillet](toolbar-icons/Draft_Fillet.png) [Fillet](#button-draft_fillet) **S** |
| Draft Snap | ![Snap Lock](toolbar-icons/Draft_Snap_Lock.png) [Snap Lock](#button-draft_snap_lock) **S**; ![Snap Endpoint](toolbar-icons/Draft_Snap_Endpoint.png) [Snap Endpoint](#button-draft_snap_endpoint) **S**; ![Snap Midpoint](toolbar-icons/Draft_Snap_Midpoint.png) [Snap Midpoint](#button-draft_snap_midpoint) **S**; ![Snap Center](toolbar-icons/Draft_Snap_Center.png) [Snap Center](#button-draft_snap_center) **S**; ![Snap Angle](toolbar-icons/Draft_Snap_Angle.png) [Snap Angle](#button-draft_snap_angle) **S**; ![Snap Intersection](toolbar-icons/Draft_Snap_Intersection.png) [Snap Intersection](#button-draft_snap_intersection) **S**; ![Snap Perpendicular](toolbar-icons/Draft_Snap_Perpendicular.png) [Snap Perpendicular](#button-draft_snap_perpendicular) **S**; ![Snap Extension](toolbar-icons/Draft_Snap_Extension.png) [Snap Extension](#button-draft_snap_extension) **S**; ![Snap Parallel](toolbar-icons/Draft_Snap_Parallel.png) [Snap Parallel](#button-draft_snap_parallel) **S**; ![Snap Special](toolbar-icons/Draft_Snap_Special.png) [Snap Special](#button-draft_snap_special) **S**; ![Snap Near](toolbar-icons/Draft_Snap_Near.png) [Snap Near](#button-draft_snap_near) **S**; ![Snap Ortho](toolbar-icons/Draft_Snap_Ortho.png) [Snap Ortho](#button-draft_snap_ortho) **S**; ![Snap Grid](toolbar-icons/Draft_Snap_Grid.png) [Snap Grid](#button-draft_snap_grid) **S**; ![Snap Working Plane](toolbar-icons/Draft_Snap_WorkingPlane.png) [Snap Working Plane](#button-draft_snap_workingplane) **S**; ![Snap Dimensions](toolbar-icons/Draft_Snap_Dimensions.png) [Snap Dimensions](#button-draft_snap_dimensions) **S**; ![Toggle Grid](toolbar-icons/Draft_ToggleGrid.png) [Toggle Grid](#button-draft_togglegrid) **S** |
| 3D/BIM Tools | ![Site](../../../src/Mod/BIM/Resources/icons/Arch_Site.svg) [Site](#button-arch_site) **S**; ![Building](../../../src/Mod/BIM/Resources/icons/Arch_Building.svg) [Building](#button-arch_building) **S**; ![Level](../../../src/Mod/BIM/Resources/icons/Arch_Floor.svg) [Level](#button-arch_level) **S**; ![Space](../../../src/Mod/BIM/Resources/icons/Arch_Space.svg) [Space](#button-arch_space) **S**; ![Wall](../../../src/Mod/BIM/Resources/icons/Arch_Wall.svg) [Wall](#button-arch_wall) **S**; ![Curtain Wall](../../../src/Mod/BIM/Resources/icons/Arch_CurtainWall.svg) [Curtain Wall](#button-arch_curtainwall) **S**; ![Column](../../../src/Mod/BIM/Resources/icons/BIM_Column.svg) [Column](#button-bim_column) **S**; ![Beam](../../../src/Mod/BIM/Resources/icons/BIM_Beam.svg) [Beam](#button-bim_beam) **S**; ![Slab](../../../src/Mod/BIM/Resources/icons/BIM_Slab.svg) [Slab](#button-bim_slab) **S**; ![Door](../../../src/Mod/BIM/Resources/icons/BIM_Door.svg) [Door](#button-bim_door) **S**; ![Window](../../../src/Mod/BIM/Resources/icons/Arch_Window.svg) [Window](#button-arch_window) **S**; ![Covering](../../../src/Mod/BIM/Resources/icons/BIM_Covering.svg) [Covering](#button-bim_covering) **S**; ![Pipe](../../../src/Mod/BIM/Resources/icons/Arch_Pipe.svg) [Pipe](#button-arch_pipe) **S**; ![Connector](../../../src/Mod/BIM/Resources/icons/Arch_PipeConnector.svg) [Connector](#button-arch_pipeconnector) **S**; ![Stairs](../../../src/Mod/BIM/Resources/icons/Arch_Stairs.svg) [Stairs](#button-arch_stairs) **S**; ![Roof](../../../src/Mod/BIM/Resources/icons/Arch_Roof.svg) [Roof](#button-arch_roof) **S**; ![Panel](../../../src/Mod/BIM/Resources/icons/Arch_Panel.svg) [Panel](#button-arch_panel) **S**; ![Frame](../../../src/Mod/BIM/Resources/icons/Arch_Frame.svg) [Frame](#button-arch_frame) **S**; ![Fence](../../../src/Mod/BIM/Resources/icons/Arch_Fence.svg) [Fence](#button-arch_fence) **S**; ![Truss](../../../src/Mod/BIM/Resources/icons/Arch_Truss.svg) [Truss](#button-arch_truss) **S**; ![Equipment](../../../src/Mod/BIM/Resources/icons/Arch_Equipment.svg) [Equipment](#button-arch_equipment) **S**; ![Custom Rebar](../../../src/Mod/BIM/Resources/icons/Arch_Rebar.svg) [Custom Rebar](#button-arch_rebar) **S**; ![Generic 3D Tools](../../../src/Mod/BIM/Resources/icons/BIM_Box.svg) [Generic 3D Tools](#button-bim_generictools) **S** |
| Annotation Tools | ![Aligned Dimension](../../../src/Mod/BIM/Resources/icons/BIM_DimensionAligned.svg) [Aligned Dimension](#button-bim_dimensionaligned) **S**; ![Horizontal Dimension](../../../src/Mod/BIM/Resources/icons/BIM_DimensionHorizontal.svg) [Horizontal Dimension](#button-bim_dimensionhorizontal) **S**; ![Vertical Dimension](../../../src/Mod/BIM/Resources/icons/BIM_DimensionVertical.svg) [Vertical Dimension](#button-bim_dimensionvertical) **S**; ![Text](../../../src/Mod/Draft/Resources/icons/Draft_Text.svg) [Text](#button-bim_text) **S**; ![Leader](../../../src/Mod/BIM/Resources/icons/BIM_Leader.svg) [Leader](#button-bim_leader) **S**; ![Label](toolbar-icons/Draft_Label.png) [Label](#button-draft_label) **S**; ![Hatch](toolbar-icons/Draft_Hatch.png) [Hatch](#button-draft_hatch) **S**; ![Axis Tools](../../../src/Mod/BIM/Resources/icons/Arch_Axis.svg) [Axis Tools](#button-bim_axistools) **S**; ![Grid](../../../src/Mod/BIM/Resources/icons/Arch_Grid.svg) [Grid](#button-arch_grid) **S**; ![Section Plane](../../../src/Mod/BIM/Resources/icons/Arch_SectionPlane.svg) [Section Plane](#button-arch_sectionplane) **S**; — [Create 2D Views](#button-bim_create2dviews) **S**; ![New Page](../../../src/Mod/BIM/Resources/icons/BIM_PageDefault.svg) [New Page](#button-bim_tdpage) **S**; ![New View](../../../src/Mod/BIM/Resources/icons/BIM_InsertView.svg) [New View](#button-bim_tdview) **S** |
| General Tools | ![Move](toolbar-icons/Draft_Move.png) [Move](#button-draft_move) **S**; ![Rotate](toolbar-icons/Draft_Rotate.png) [Rotate](#button-draft_rotate) **S**; ![Scale](toolbar-icons/Draft_Scale.png) [Scale](#button-draft_scale) **S**; ![Mirror](toolbar-icons/Draft_Mirror.png) [Mirror](#button-draft_mirror) **S**; ![Cloning Tools](../../../src/Mod/BIM/Resources/icons/BIM_Clone.svg) [Cloning Tools](#button-bim_clonetools) **S**; ![Copy](../../../src/Mod/BIM/Resources/icons/BIM_Copy.svg) [Copy](#button-bim_copy) **S**; ![Simple Copy](../../../src/Mod/BIM/Resources/icons/Tree_Part.svg) [Simple Copy](#button-bim_simplecopy) **S**; ![Compound](../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Compound.svg) [Compound](#button-bim_compound) **S** |
| 2D Tools | — [Offset Tools](#button-bim_offsettools) **S**; ![Trimex](../../../src/Mod/Draft/Resources/icons/Draft_Trimex.svg) [Trimex](#button-bim_trimex) **S**; ![Join](toolbar-icons/Draft_Join.png) [Join](#button-draft_join) **S**; ![Split](toolbar-icons/Draft_Split.png) [Split](#button-draft_split) **S**; ![Stretch](toolbar-icons/Draft_Stretch.png) [Stretch](#button-draft_stretch) **S**; ![Draft to Sketch](toolbar-icons/Draft_Draft2Sketch.png) [Draft to Sketch](#button-draft_draft2sketch) **S**; ![Edit](toolbar-icons/Draft_Edit.png) [Edit](#button-draft_edit) **S** |
| Object Tools | ![Upgrade](toolbar-icons/Draft_Upgrade.png) [Upgrade](#button-draft_upgrade) **S**; ![Downgrade](toolbar-icons/Draft_Downgrade.png) [Downgrade](#button-draft_downgrade) **S**; ![Add Component](../../../src/Mod/BIM/Resources/icons/Arch_Add.svg) [Add Component](#button-arch_add) **S**; ![Remove Component](../../../src/Mod/BIM/Resources/icons/Arch_Remove.svg) [Remove Component](#button-arch_remove) **S** |
| 3D Tools | ![Array Tools](../../../src/Mod/Draft/Resources/icons/Draft_Array.svg) [Array Tools](#button-bim_arraytools) **S**; ![Cut With Plane](../../../src/Mod/BIM/Resources/icons/Arch_CutPlane.svg) [Cut With Plane](#button-arch_cutplane) **S**; ![Extrude](../../../src/Mod/Part/Gui/Resources/icons/tools/Part_Extrude.svg) [Extrude](#button-bim_extrude) **S**; ![Extrude Face](../../../src/Mod/BIM/Resources/icons/BIM_ExtrudeFace.svg) [Extrude Face](#button-bim_extrudeface) **S**; — [Boolean Tools](#button-bim_booleantools) **S** |
| Manage Tools | ![BIM Setup](../../../src/Gui/Icons/preferences-system.svg) [BIM Setup](#button-bim_setup) **S**; ![Setup Project](../../../src/Mod/BIM/Resources/icons/BIM_ProjectManager.svg) [Setup Project](#button-bim_projectmanager) **S**; ![Manage Doors and Windows](../../../src/Mod/BIM/Resources/icons/BIM_Windows.svg) [Manage Doors and Windows](#button-bim_windows) **S**; ![IFC Management](../../../src/Mod/BIM/Resources/icons/BIM_IfcElements.svg) [IFC Management](#button-bim_ifcmanagetools) **S**; ![Manage Layers](../../../src/Mod/BIM/Resources/icons/BIM_Layers.svg) [Manage Layers](#button-bim_layers) **S**; ![Material](../../../src/Mod/BIM/Resources/icons/BIM_Material.svg) [Material](#button-bim_material) **S**; ![Report Tools](../../../src/Mod/BIM/Resources/icons/BIM_Report.svg) [Report Tools](#button-bim_reporttools) **S**; ![Preflight Checks](../../../src/Mod/BIM/Resources/icons/BIM_Preflight.svg) [Preflight Checks](#button-bim_preflight) **S**; ![Annotation Styles](toolbar-icons/Draft_AnnotationStyleEditor.png) [Annotation Styles](#button-draft_annotationstyleeditor) **S** |

<a id="workbench-openscadworkbench"></a>
### OpenSCAD (`OpenSCADWorkbench`)

Definition: [`src/Mod/OpenSCAD/InitGui.py`](../../../src/Mod/OpenSCAD/InitGui.py). Shared Classic groups are listed once above.

**Source-only / not packaged in the inspected build.** These toolbar definitions exist in source. When the workbench is installed and registered, its Plus mode uses shared Home/View and these native groups in Tools. No executable/icon-menu acceptance is claimed for this workbench.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| OpenSCAD Tools | ![Replace Object](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_ReplaceObject.svg) [Replace Object](#button-openscad_replaceobject); ![Remove Objects and Children](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_RemoveSubtree.svg) [Remove Objects and Children](#button-openscad_removesubtree); ![Explode Group](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Explode_Group.svg) [Explode Group](#button-openscad_explodegroup); ![Refine Shape Feature](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_RefineShapeFeature.svg) [Refine Shape Feature](#button-openscad_refineshapefeature); ![Increase Tolerance Feature](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_IncreaseToleranceFeature.svg) [Increase Tolerance Feature](#button-openscad_increasetolerancefeature); ![Add OpenSCAD Element](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_AddOpenSCADElement.svg) [Add OpenSCAD Element](#button-openscad_addopenscadelement); ![Mesh Boolean](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_MeshBooleans.svg) [Mesh Boolean](#button-openscad_meshboolean); ![Hull](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Hull.svg) [Hull](#button-openscad_hull); ![Minkowski Sum](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Minkowski.svg) [Minkowski Sum](#button-openscad_minkowski) |
| Frequently-used Part WB tools | ![Check Geometry](toolbar-icons/Part_CheckGeometry.png) [Check Geometry](#button-part_checkgeometry); ![Primitive](toolbar-icons/Part_Primitives.png) [Primitive](#button-part_primitives); ![Shape Builder](toolbar-icons/Part_Builder.png) [Shape Builder](#button-part_builder); ![Cut](toolbar-icons/Part_Cut.png) [Cut](#button-part_cut); ![Union](toolbar-icons/Part_Fuse.png) [Union](#button-part_fuse); ![Intersection](toolbar-icons/Part_Common.png) [Intersection](#button-part_common); ![Extrude](toolbar-icons/Part_Extrude.png) [Extrude](#button-part_extrude); ![Revolve](toolbar-icons/Part_Revolve.png) [Revolve](#button-part_revolve) |

#### Changes made / buttons consolidated or omitted

- The final four OpenSCAD Tools choices (Add OpenSCAD Element, Mesh Boolean, Hull and Minkowski) require a configured external OpenSCAD executable. They are shown as conditional source choices.
- No workbench-specific toolbar command removal found in the compared definitions; Plus changes presentation/routing and applies the shared Home/View rules above.

#### Plus UI tabs and sections

**OpenSCAD → Tools**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| OpenSCAD Tools | ![Replace Object](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_ReplaceObject.svg) [Replace Object](#button-openscad_replaceobject) **S**; ![Remove Objects and Children](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_RemoveSubtree.svg) [Remove Objects and Children](#button-openscad_removesubtree) **S**; ![Explode Group](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Explode_Group.svg) [Explode Group](#button-openscad_explodegroup) **S**; ![Refine Shape Feature](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_RefineShapeFeature.svg) [Refine Shape Feature](#button-openscad_refineshapefeature) **S**; ![Increase Tolerance Feature](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_IncreaseToleranceFeature.svg) [Increase Tolerance Feature](#button-openscad_increasetolerancefeature) **S**; ![Add OpenSCAD Element](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_AddOpenSCADElement.svg) [Add OpenSCAD Element](#button-openscad_addopenscadelement) **S**; ![Mesh Boolean](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_MeshBooleans.svg) [Mesh Boolean](#button-openscad_meshboolean) **S**; ![Hull](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Hull.svg) [Hull](#button-openscad_hull) **S**; ![Minkowski Sum](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Minkowski.svg) [Minkowski Sum](#button-openscad_minkowski) **S** |
| Frequently-used Part WB tools | ![Check Geometry](toolbar-icons/Part_CheckGeometry.png) [Check Geometry](#button-part_checkgeometry) **S**; ![Primitive](toolbar-icons/Part_Primitives.png) [Primitive](#button-part_primitives) **S**; ![Shape Builder](toolbar-icons/Part_Builder.png) [Shape Builder](#button-part_builder) **S**; ![Cut](toolbar-icons/Part_Cut.png) [Cut](#button-part_cut) **S**; ![Union](toolbar-icons/Part_Fuse.png) [Union](#button-part_fuse) **S**; ![Intersection](toolbar-icons/Part_Common.png) [Intersection](#button-part_common) **S**; ![Extrude](toolbar-icons/Part_Extrude.png) [Extrude](#button-part_extrude) **S**; ![Revolve](toolbar-icons/Part_Revolve.png) [Revolve](#button-part_revolve) **S** |

<a id="workbench-testworkbench"></a>
### Test Framework (`TestWorkbench`)

Definition: [`src/Mod/Test/InitGui.py`](../../../src/Mod/Test/InitGui.py). Shared Classic groups are listed once above.

#### Classic upstream toolbar groups

| Section / toolbar group | Buttons in display order |
| --- | --- |
| TestTools | ![Self-test...](../../../src/Gui/Icons/preferences-general.svg) [Self-test...](#button-test_test); ![Test all](toolbar-icons/Test_TestAll.png) [Test all](#button-test_testall); ![Test Document](toolbar-icons/Test_TestDoc.png) [Test Document](#button-test_testdoc); ![Test base](toolbar-icons/Test_TestBase.png) [Test base](#button-test_testbase) |

#### Changes made / buttons consolidated or omitted

- No workbench-specific toolbar command removal found in the compared definitions; Plus changes presentation/routing and applies the shared Home/View rules above.

#### Plus UI tabs and sections

**Home:** shared sections above; Home excludes the Design-only Sketch and Tools sections.

**Test Framework → Tools**

| Section / toolbar group | Buttons in display order |
| --- | --- |
| TestTools | ![Self-test...](../../../src/Gui/Icons/preferences-general.svg) [Self-test...](#button-test_test) **S**; ![Test all](toolbar-icons/Test_TestAll.png) [Test all](#button-test_testall) **S**; ![Test Document](toolbar-icons/Test_TestDoc.png) [Test Document](#button-test_testdoc) **S**; ![Test base](toolbar-icons/Test_TestBase.png) [Test base](#button-test_testbase) **S** |

**View:** shared sections above.

### Other bundled and addon workbenches

BIM and OpenSCAD are not registered in the inspected build. Their source-defined toolbars are listed below; when registered, Plus would project their workbench groups into Tools. 3D printing is an addon mode only when an installed workbench registers it; this checkout has no authoritative addon button inventory.

**BIM:** Drafting Tools; Draft Snap; 3D/BIM Tools; Annotation Tools; 2D Tools; Manage Tools; General Tools; Object Tools; 3D Tools; &2D Drafting; &3D/BIM; &Reinforcement Tools; &Annotation; &Snapping; M&odify; Ma&nage; &IFC; &Flamingo. See [native definition](../../../src/Mod/BIM/InitGui.py) for conditional button lists. No Plus-specific toolbar change is recorded for this workbench.

**OpenSCAD:** OpenSCAD Tools; Frequently-used Part WB tools. See [native definition](../../../src/Mod/OpenSCAD/InitGui.py) for conditional button lists. No Plus-specific toolbar change is recorded for this workbench.

## Complete toolbar button/function catalog

This catalog contains every command referenced by the Classic/Plus tables above, plus every native compound-button choice. A compound command's first action is its current/default choice; it may change after the user selects another choice. Menu-only fork additions are not relabeled as toolbar buttons. Descriptions come from native status/help text or source GetResources. Command IDs disambiguate identically named buttons.

<a id="button-arch_add"></a>
### Add Component — `Arch_Add`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Add Component](../../../src/Mod/BIM/Resources/icons/Arch_Add.svg) | Add Component | Adds the selected components to the active object |

<a id="button-arch_axis"></a>
### Axis — `Arch_Axis`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Axis](../../../src/Mod/BIM/Resources/icons/Arch_Axis.svg) | Axis | Creates a set of axes |

<a id="button-arch_axissystem"></a>
### Axis System — `Arch_AxisSystem`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Axis System](../../../src/Mod/BIM/Resources/icons/Arch_Axis_System.svg) | Axis System | Creates an axis system from a set of axes |

<a id="button-arch_building"></a>
### Building — `Arch_Building`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Building](../../../src/Mod/BIM/Resources/icons/Arch_Building.svg) | Building | Creates a building object |

<a id="button-arch_component"></a>
### Component — `Arch_Component`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Component](../../../src/Mod/BIM/Resources/icons/Arch_Component.svg) | Component | Creates an undefined architectural component |

<a id="button-arch_curtainwall"></a>
### Curtain Wall — `Arch_CurtainWall`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Curtain Wall](../../../src/Mod/BIM/Resources/icons/Arch_CurtainWall.svg) | Curtain Wall | Creates a curtain wall object from selected line or from scratch |

<a id="button-arch_cutplane"></a>
### Cut With Plane — `Arch_CutPlane`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cut With Plane](../../../src/Mod/BIM/Resources/icons/Arch_CutPlane.svg) | Cut With Plane | Cuts an object with a plane |

<a id="button-arch_equipment"></a>
### Equipment — `Arch_Equipment`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Equipment](../../../src/Mod/BIM/Resources/icons/Arch_Equipment.svg) | Equipment | Creates an equipment from a selected object (Part or Mesh) |

<a id="button-arch_fence"></a>
### Fence — `Arch_Fence`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Fence](../../../src/Mod/BIM/Resources/icons/Arch_Fence.svg) | Fence | Creates a fence object from a selected section, post and path |

<a id="button-arch_frame"></a>
### Frame — `Arch_Frame`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Frame](../../../src/Mod/BIM/Resources/icons/Arch_Frame.svg) | Frame | Creates a frame object from a planar 2D object (the extrusion path(s)) and a profile. Make sure objects are selected in that order. |

<a id="button-arch_grid"></a>
### Grid — `Arch_Grid`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Grid](../../../src/Mod/BIM/Resources/icons/Arch_Grid.svg) | Grid | Creates a customizable grid object |

<a id="button-arch_level"></a>
### Level — `Arch_Level`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Level](../../../src/Mod/BIM/Resources/icons/Arch_Floor.svg) | Level | Creates a building part object that represents a level |

<a id="button-arch_panel"></a>
### Panel — `Arch_Panel`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Panel](../../../src/Mod/BIM/Resources/icons/Arch_Panel.svg) | Panel | Creates a panel object from scratch or from a selected object (sketch, wire, face or solid) |

<a id="button-arch_pipe"></a>
### Pipe — `Arch_Pipe`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Pipe](../../../src/Mod/BIM/Resources/icons/Arch_Pipe.svg) | Pipe | Creates a pipe object from a given wire or line |

<a id="button-arch_pipeconnector"></a>
### Connector — `Arch_PipeConnector`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Connector](../../../src/Mod/BIM/Resources/icons/Arch_PipeConnector.svg) | Connector | Creates a connector between 2 or 3 selected pipes |

<a id="button-arch_profile"></a>
### Profile — `Arch_Profile`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Profile](../../../src/Mod/BIM/Resources/icons/Arch_Profile.svg) | Profile | Creates a profile |

<a id="button-arch_rebar"></a>
### Custom Rebar — `Arch_Rebar`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Custom Rebar](../../../src/Mod/BIM/Resources/icons/Arch_Rebar.svg) | Custom Rebar | Creates a reinforcement bar from the selected face of solid object and/or a sketch |

<a id="button-arch_reference"></a>
### External Reference — `Arch_Reference`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![External Reference](../../../src/Mod/BIM/Resources/icons/Arch_Reference.svg) | External Reference | Creates an external reference object |

<a id="button-arch_remove"></a>
### Remove Component — `Arch_Remove`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Remove Component](../../../src/Mod/BIM/Resources/icons/Arch_Remove.svg) | Remove Component | Removes the selected components from their parents, or creates a hole in a component |

<a id="button-arch_roof"></a>
### Roof — `Arch_Roof`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Roof](../../../src/Mod/BIM/Resources/icons/Arch_Roof.svg) | Roof | Creates a roof object from the selected wire. |

<a id="button-arch_schedule"></a>
### Schedule — `Arch_Schedule`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Schedule](../../../src/Mod/BIM/Resources/icons/Arch_Schedule.svg) | Schedule | Creates a schedule to collect data from the model |

<a id="button-arch_sectionplane"></a>
### Section Plane — `Arch_SectionPlane`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Section Plane](../../../src/Mod/BIM/Resources/icons/Arch_SectionPlane.svg) | Section Plane | Creates a section plane object, including the selected objects |

<a id="button-arch_site"></a>
### Site — `Arch_Site`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Site](../../../src/Mod/BIM/Resources/icons/Arch_Site.svg) | Site | Creates a site including selected objects |

<a id="button-arch_space"></a>
### Space — `Arch_Space`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Space](../../../src/Mod/BIM/Resources/icons/Arch_Space.svg) | Space | Creates a space object from selected boundary objects |

<a id="button-arch_stairs"></a>
### Stairs — `Arch_Stairs`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Stairs](../../../src/Mod/BIM/Resources/icons/Arch_Stairs.svg) | Stairs | Creates a flight of stairs |

<a id="button-arch_survey"></a>
### Survey — `Arch_Survey`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Survey](../../../src/Mod/BIM/Resources/icons/Arch_Survey.svg) | Survey | Starts survey |

<a id="button-arch_truss"></a>
### Truss — `Arch_Truss`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Truss](../../../src/Mod/BIM/Resources/icons/Arch_Truss.svg) | Truss | Creates a truss object from the selected line or from scratch |

<a id="button-arch_wall"></a>
### Wall — `Arch_Wall`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Wall](../../../src/Mod/BIM/Resources/icons/Arch_Wall.svg) | Wall | Creates a wall object from scratch or from a selected object (wire, face or solid) |

<a id="button-arch_window"></a>
### Window — `Arch_Window`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Window](../../../src/Mod/BIM/Resources/icons/Arch_Window.svg) | Window | Creates a window object from a selected object (wire, rectangle or sketch) |

<a id="button-assembly_createassembly"></a>
### New Assembly — `Assembly_CreateAssembly`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![New Assembly](toolbar-icons/Assembly_CreateAssembly.png) | New Assembly | Creates an assembly object in the current document, or in the current active assembly (if any). Limit of one root assembly per file. |

<a id="button-assembly_createbom"></a>
### Bill of Materials — `Assembly_CreateBom`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Bill of Materials](toolbar-icons/Assembly_CreateBom.png) | Bill of Materials | Creates a bill of materials of the current assembly. If an assembly is active, it will be a BOM of this assembly. Else it will be a BOM of the whole document. The BOM object is a document object that stores the settings of your BOM. It is also a spreadsheet object so you can easily visualize the BOM. If you do not need the BOM object to be saved as a document object, you can simply export and cancel the task. The columns 'Index', 'Name', 'File Name' and 'Quantity' are automatically generated on recompute. The 'Description' and custom columns are not overwritten. |

<a id="button-assembly_createjointangle"></a>
### Angle Joint — `Assembly_CreateJointAngle`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Angle Joint](toolbar-icons/Assembly_CreateJointAngle.png) | Angle Joint | Creates an angle joint that fixes the angle between the Z-axis of the selected coordinate systems |

<a id="button-assembly_createjointball"></a>
### Ball Joint — `Assembly_CreateJointBall`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Ball Joint](toolbar-icons/Assembly_CreateJointBall.png) | Ball Joint | Creates a ball joint that connects parts at a point, allowing unrestricted movement as long as the connection points remain in contact |

<a id="button-assembly_createjointbelt"></a>
### Belt Joint — `Assembly_CreateJointBelt`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Belt Joint](toolbar-icons/Assembly_CreateJointBelt.png) | Belt Joint | Creates a belt joint that links 2 rotating objects together. They will have the same rotation direction. Select the same coordinate systems as the revolute joints. |

<a id="button-assembly_createjointcylindrical"></a>
### Cylindrical Joint — `Assembly_CreateJointCylindrical`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cylindrical Joint](toolbar-icons/Assembly_CreateJointCylindrical.png) | Cylindrical Joint | Creates a cylindrical joint that allows rotation around and translation along a single axis between assembled parts |

<a id="button-assembly_createjointdistance"></a>
### Distance Joint — `Assembly_CreateJointDistance`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Distance Joint](toolbar-icons/Assembly_CreateJointDistance.png) | Distance Joint | Creates a distance joint that fixes the distance between the selected objects Creates one of several different joints based on the selection. For example, a distance of 0 between a plane and a cylinder creates a tangent joint. A distance of 0 between planes will make them co-planar. |

<a id="button-assembly_createjointfixed"></a>
### Fixed Joint — `Assembly_CreateJointFixed`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Fixed Joint](toolbar-icons/Assembly_CreateJointFixed.png) | Fixed Joint | 1 - If an assembly is active : Creates a joint statically locking two parts together, preventing any movement or rotation 2 - If a part is active: Positions sub-parts by matching selected coordinate systems. The second part selected will move. |

<a id="button-assembly_createjointgearbelt"></a>
### Gears Joint — `Assembly_CreateJointGearBelt`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Gears Joint](toolbar-icons/Assembly_CreateJointGearBelt.png) | Gears Joint | Creates a gears joint that links 2 rotating gears together. They will have inverse rotation direction. Select the same coordinate systems as the revolute joints. |
| ![Belt Joint](toolbar-icons/Assembly_CreateJointGearBelt_1.png) | Belt Joint | Creates a belt joint that links 2 rotating objects together. They will have the same rotation direction. Select the same coordinate systems as the revolute joints. |

<a id="button-assembly_createjointgears"></a>
### Gears Joint — `Assembly_CreateJointGears`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Gears Joint](toolbar-icons/Assembly_CreateJointGears.png) | Gears Joint | Creates a gears joint that links 2 rotating gears together. They will have inverse rotation direction. Select the same coordinate systems as the revolute joints. |

<a id="button-assembly_createjointparallel"></a>
### Parallel Joint — `Assembly_CreateJointParallel`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Parallel Joint](toolbar-icons/Assembly_CreateJointParallel.png) | Parallel Joint | Creates a parallel joint that makes the Z-axis of the selected coordinate systems parallel |

<a id="button-assembly_createjointperpendicular"></a>
### Perpendicular Joint — `Assembly_CreateJointPerpendicular`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Perpendicular Joint](toolbar-icons/Assembly_CreateJointPerpendicular.png) | Perpendicular Joint | Creates a perpendicular joint that makes the Z-axis of the selected coordinate systems perpendicular |

<a id="button-assembly_createjointrackpinion"></a>
### Rack and Pinion Joint — `Assembly_CreateJointRackPinion`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Rack and Pinion Joint](toolbar-icons/Assembly_CreateJointRackPinion.png) | Rack and Pinion Joint | Creates a rack and pinion joint that links a part with a slider joint to a part with a revolute joint Select the same coordinate systems as the revolute and slider joints. The pitch radius defines the movement ratio between the rack and the pinion. |

<a id="button-assembly_createjointrevolute"></a>
### Revolute Joint — `Assembly_CreateJointRevolute`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Revolute Joint](toolbar-icons/Assembly_CreateJointRevolute.png) | Revolute Joint | Creates a revolute joint allowing rotation around a single axis between selected parts |

<a id="button-assembly_createjointrigidgroup"></a>
### Create Rigid Group — `Assembly_CreateJointRigidGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Create Rigid Group](toolbar-icons/Assembly_CreateJointRigidGroup.png) | Create Rigid Group | Create a rigid group. Creates a rigid group that permanently locks the selected components together. |

<a id="button-assembly_createjointscrew"></a>
### Screw Joint — `Assembly_CreateJointScrew`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Screw Joint](toolbar-icons/Assembly_CreateJointScrew.png) | Screw Joint | Creates a screw joint that links a part with a slider joint to a part with a revolute joint Select the same coordinate systems as the revolute and slider joints. The pitch radius defines the movement ratio between the rotating screw and the sliding part. |

<a id="button-assembly_createjointslider"></a>
### Slider Joint — `Assembly_CreateJointSlider`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Slider Joint](toolbar-icons/Assembly_CreateJointSlider.png) | Slider Joint | Creates a slider joint that allows linear movement along a single axis, but restricts rotation between selected parts |

<a id="button-assembly_createsimulation"></a>
### Simulation — `Assembly_CreateSimulation`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Simulation](toolbar-icons/Assembly_CreateSimulation.png) | Simulation | Creates a new simulation of the current assembly |

<a id="button-assembly_createsnapshot"></a>
### Snapshot — `Assembly_CreateSnapshot`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Snapshot](toolbar-icons/Assembly_CreateSnapshot.png) | Snapshot | Captures the current assembly state (placements and visibility). Double-clicking the Snapshot object restores the assembly to that state. |

<a id="button-assembly_createview"></a>
### Exploded View — `Assembly_CreateView`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Exploded View](toolbar-icons/Assembly_CreateView.png) | Exploded View | Creates an exploded view of the current assembly |

<a id="button-assembly_insert"></a>
### Insert Component — `Assembly_Insert`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Insert Component](toolbar-icons/Assembly_Insert.png) | Insert Component | Inserts a component into the active assembly. This will create dynamic links to parts, bodies, primitives, and assemblies. To insert external components, make sure that the file is open in the current session Insert by left clicking items in the list. Remove by right clicking items in the list. Press shift to add several instances of the component while clicking on the view. |
| ![Add Component](toolbar-icons/Assembly_Insert_1.png) | Add Component | Adds a component to the active component or assembly. |

<a id="button-assembly_insertlink"></a>
### Insert Component — `Assembly_InsertLink`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Insert Component](toolbar-icons/Assembly_InsertLink.png) | Insert Component | Inserts a component into the active assembly. This will create dynamic links to parts, bodies, primitives, and assemblies. To insert external components, make sure that the file is open in the current session Insert by left clicking items in the list. Remove by right clicking items in the list. Press shift to add several instances of the component while clicking on the view. |

<a id="button-assembly_insertnewpart"></a>
### Add Component — `Assembly_InsertNewPart`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Add Component](toolbar-icons/Assembly_InsertNewPart.png) | Add Component | Adds a component to the active component or assembly. |

<a id="button-assembly_solveassembly"></a>
### Solve Assembly — `Assembly_SolveAssembly`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Solve Assembly](toolbar-icons/Assembly_SolveAssembly.png) | Solve Assembly | Solves the currently active assembly. |

<a id="button-assembly_togglegrounded"></a>
### Toggle Grounded — `Assembly_ToggleGrounded`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Toggle Grounded](toolbar-icons/Assembly_ToggleGrounded.png) | Toggle Grounded | Toggles the grounding of a part. Grounding a part permanently locks its position in the assembly, preventing any movement or rotation. |

<a id="button-bim_arctools"></a>
### Arc Tools — `BIM_ArcTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Arc Tools](../../../src/Mod/Draft/Resources/icons/Draft_Arc.svg) | Arc Tools | Arc Tools |

Source-defined dropdown choices: ![Arc](toolbar-icons/Draft_Arc.png) [Arc](#button-draft_arc); ![Arc From 3 Points](toolbar-icons/Draft_Arc_3Points.png) [Arc From 3 Points](#button-draft_arc_3points).

<a id="button-bim_arraytools"></a>
### Array Tools — `BIM_ArrayTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Array Tools](../../../src/Mod/Draft/Resources/icons/Draft_Array.svg) | Array Tools | Array Tools |

Source-defined dropdown choices: ![Array](toolbar-icons/Draft_OrthoArray.png) [Array](#button-draft_orthoarray); ![Path Link Array](toolbar-icons/Draft_PathLinkArray.png) [Path Link Array](#button-draft_pathlinkarray); ![Polar Array](toolbar-icons/Draft_PolarArray.png) [Polar Array](#button-draft_polararray); ![Point Link Array](toolbar-icons/Draft_PointLinkArray.png) [Point Link Array](#button-draft_pointlinkarray).

<a id="button-bim_axistools"></a>
### Axis Tools — `BIM_AxisTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Axis Tools](../../../src/Mod/BIM/Resources/icons/Arch_Axis.svg) | Axis Tools | Axis Tools |

Source-defined dropdown choices: ![Axis](../../../src/Mod/BIM/Resources/icons/Arch_Axis.svg) [Axis](#button-arch_axis); ![Axis System](../../../src/Mod/BIM/Resources/icons/Arch_Axis_System.svg) [Axis System](#button-arch_axissystem).

<a id="button-bim_beam"></a>
### Beam — `BIM_Beam`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Beam](../../../src/Mod/BIM/Resources/icons/BIM_Beam.svg) | Beam | Creates a beam between two points |

<a id="button-bim_booleantools"></a>
### Boolean Tools — `BIM_BooleanTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| — | Boolean Tools | Boolean Tools |

Source-defined dropdown choices: ![Union](../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Fuse.svg) [Union](#button-bim_fuse); ![Difference](../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Cut.svg) [Difference](#button-bim_cut); ![Intersection](../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Common.svg) [Intersection](#button-bim_common).

<a id="button-bim_box"></a>
### Box — `BIM_Box`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Box](../../../src/Mod/BIM/Resources/icons/BIM_Box.svg) | Box | Graphically creates a generic box in the current document |

<a id="button-bim_builder"></a>
### Shape Builder — `BIM_Builder`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Shape Builder](../../../src/Mod/Part/Gui/Resources/icons/create/Part_Shapebuilder.svg) | Shape Builder | Advanced utility to create shapes |

<a id="button-bim_classification"></a>
### Manage Classification — `BIM_Classification`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Manage Classification](../../../src/Mod/BIM/Resources/icons/BIM_Classification.svg) | Manage Classification | Manages classification systems and apply classification to objects |

<a id="button-bim_clone"></a>
### Clone — `BIM_Clone`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Clone](../../../src/Mod/BIM/Resources/icons/BIM_Clone.svg) | Clone | Clones selected objects to another location |

<a id="button-bim_clonetools"></a>
### Cloning Tools — `BIM_CloneTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cloning Tools](../../../src/Mod/BIM/Resources/icons/BIM_Clone.svg) | Cloning Tools | Cloning Tools |

Source-defined dropdown choices: ![Clone](../../../src/Mod/BIM/Resources/icons/BIM_Clone.svg) [Clone](#button-bim_clone); ![Make Link](../../../src/Gui/Icons/Link.svg) [Make Link](#button-bim_linkmake); ![Unclone](../../../src/Mod/BIM/Resources/icons/BIM_Unclone.svg) [Unclone](#button-bim_unclone).

<a id="button-bim_column"></a>
### Column — `BIM_Column`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Column](../../../src/Mod/BIM/Resources/icons/BIM_Column.svg) | Column | Creates a column at a specified location |

<a id="button-bim_common"></a>
### Intersection — `BIM_Common`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Intersection](../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Common.svg) | Intersection | Creates an intersection of two shapes |

<a id="button-bim_compound"></a>
### Compound — `BIM_Compound`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Compound](../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Compound.svg) | Compound | Creates a compound of several shapes |

<a id="button-bim_copy"></a>
### Copy — `BIM_Copy`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Copy](../../../src/Mod/BIM/Resources/icons/BIM_Copy.svg) | Copy | Copies selected objects to another location |

<a id="button-bim_covering"></a>
### Covering — `BIM_Covering`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Covering](../../../src/Mod/BIM/Resources/icons/BIM_Covering.svg) | Covering | Creates a covering (floor finish, cladding) on a selected face |

<a id="button-bim_create2dviews"></a>
### Create 2D Views — `BIM_Create2DViews`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| — | Create 2D Views | Create 2D Views |

Source-defined dropdown choices: ![2D Drawing](../../../src/Mod/BIM/Resources/icons/BIM_ArchView.svg) [2D Drawing](#button-bim_drawingview); ![Section View](../../../src/Mod/BIM/Resources/icons/Arch_BuildingPart_Tree.svg) [Section View](#button-bim_shape2dview); ![Section Cut](../../../src/Mod/BIM/Resources/icons/Arch_View_Cut.svg) [Section Cut](#button-bim_shape2dcut); ![Force 2D View Update](toolbar-icons/Draft_UpdateShape2DView.png) [Force 2D View Update](#button-draft_updateshape2dview).

<a id="button-bim_cut"></a>
### Difference — `BIM_Cut`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Difference](../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Cut.svg) | Difference | Creates a difference between two shapes |

<a id="button-bim_dimensionaligned"></a>
### Aligned Dimension — `BIM_DimensionAligned`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Aligned Dimension](../../../src/Mod/BIM/Resources/icons/BIM_DimensionAligned.svg) | Aligned Dimension | Creates an aligned dimension |

<a id="button-bim_dimensionhorizontal"></a>
### Horizontal Dimension — `BIM_DimensionHorizontal`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Horizontal Dimension](../../../src/Mod/BIM/Resources/icons/BIM_DimensionHorizontal.svg) | Horizontal Dimension | Creates an horizontal dimension |

<a id="button-bim_dimensionvertical"></a>
### Vertical Dimension — `BIM_DimensionVertical`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Vertical Dimension](../../../src/Mod/BIM/Resources/icons/BIM_DimensionVertical.svg) | Vertical Dimension | Creates a vertical dimension |

<a id="button-bim_door"></a>
### Door — `BIM_Door`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Door](../../../src/Mod/BIM/Resources/icons/BIM_Door.svg) | Door | Places a door at a given location |

<a id="button-bim_drawingview"></a>
### 2D Drawing — `BIM_DrawingView`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![2D Drawing](../../../src/Mod/BIM/Resources/icons/BIM_ArchView.svg) | 2D Drawing | Creates a drawing container to contain elements of a 2D view |

<a id="button-bim_extrude"></a>
### Extrude — `BIM_Extrude`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Extrude](../../../src/Mod/Part/Gui/Resources/icons/tools/Part_Extrude.svg) | Extrude | Extrudes a selected 2D shape |

<a id="button-bim_extrudeface"></a>
### Extrude Face — `BIM_ExtrudeFace`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Extrude Face](../../../src/Mod/BIM/Resources/icons/BIM_ExtrudeFace.svg) | Extrude Face | Extrudes a selected face into a solid |

<a id="button-bim_fuse"></a>
### Union — `BIM_Fuse`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Union](../../../src/Mod/Part/Gui/Resources/icons/booleans/Part_Fuse.svg) | Union | Creates a union of several shapes |

<a id="button-bim_generictools"></a>
### Generic 3D Tools — `BIM_GenericTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Generic 3D Tools](../../../src/Mod/BIM/Resources/icons/BIM_Box.svg) | Generic 3D Tools | Generic 3D Tools |

Source-defined dropdown choices: ![Profile](../../../src/Mod/BIM/Resources/icons/Arch_Profile.svg) [Profile](#button-arch_profile); ![Box](../../../src/Mod/BIM/Resources/icons/BIM_Box.svg) [Box](#button-bim_box); ![Shape Builder](../../../src/Mod/Part/Gui/Resources/icons/create/Part_Shapebuilder.svg) [Shape Builder](#button-bim_builder); ![Facebinder](toolbar-icons/Draft_Facebinder.png) [Facebinder](#button-draft_facebinder); ![Objects Library](../../../src/Mod/BIM/Resources/icons/BIM_Library.svg) [Objects Library](#button-bim_library); ![Component](../../../src/Mod/BIM/Resources/icons/Arch_Component.svg) [Component](#button-arch_component); ![External Reference](../../../src/Mod/BIM/Resources/icons/Arch_Reference.svg) [External Reference](#button-arch_reference).

<a id="button-bim_ifcelements"></a>
### Manage IFC Elements — `BIM_IfcElements`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Manage IFC Elements](../../../src/Mod/BIM/Resources/icons/BIM_IfcElements.svg) | Manage IFC Elements | Manages how the different elements of the BIM project will be exported to IFC |

<a id="button-bim_ifcmanagetools"></a>
### IFC Management — `BIM_IfcManageTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![IFC Management](../../../src/Mod/BIM/Resources/icons/BIM_IfcElements.svg) | IFC Management | IFC Management |

Source-defined dropdown choices: ![Manage IFC Elements](../../../src/Mod/BIM/Resources/icons/BIM_IfcElements.svg) [Manage IFC Elements](#button-bim_ifcelements); ![Manage IFC Quantities](../../../src/Mod/BIM/Resources/icons/BIM_IfcQuantities.svg) [Manage IFC Quantities](#button-bim_ifcquantities); ![Manage IFC Properties](../../../src/Mod/BIM/Resources/icons/BIM_IfcProperties.svg) [Manage IFC Properties](#button-bim_ifcproperties); ![Manage Classification](../../../src/Mod/BIM/Resources/icons/BIM_Classification.svg) [Manage Classification](#button-bim_classification).

<a id="button-bim_ifcproperties"></a>
### Manage IFC Properties — `BIM_IfcProperties`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Manage IFC Properties](../../../src/Mod/BIM/Resources/icons/BIM_IfcProperties.svg) | Manage IFC Properties | Manages the different IFC properties of the BIM objects |

<a id="button-bim_ifcquantities"></a>
### Manage IFC Quantities — `BIM_IfcQuantities`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Manage IFC Quantities](../../../src/Mod/BIM/Resources/icons/BIM_IfcQuantities.svg) | Manage IFC Quantities | Manages how the quantities of different elements of the BIM project will be exported to IFC |

<a id="button-bim_layers"></a>
### Manage Layers — `BIM_Layers`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Manage Layers](../../../src/Mod/BIM/Resources/icons/BIM_Layers.svg) | Manage Layers | Sets/modifies the different layers of your BIM project |

<a id="button-bim_leader"></a>
### Leader — `BIM_Leader`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Leader](../../../src/Mod/BIM/Resources/icons/BIM_Leader.svg) | Leader | Creates a polyline with an arrow at its endpoint |

<a id="button-bim_library"></a>
### Objects Library — `BIM_Library`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Objects Library](../../../src/Mod/BIM/Resources/icons/BIM_Library.svg) | Objects Library | Opens the objects library |

<a id="button-bim_linkmake"></a>
### Make Link — `BIM_LinkMake`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Make Link](../../../src/Gui/Icons/Link.svg) | Make Link | Creates a Link to the selected object and immediately enables moving it |

<a id="button-bim_material"></a>
### Material — `BIM_Material`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Material](../../../src/Mod/BIM/Resources/icons/BIM_Material.svg) | Material | Sets or creates a material for selected objects |

<a id="button-bim_offset2d"></a>
### 2D Offset — `BIM_Offset2D`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![2D Offset](../../../src/Mod/Part/Gui/Resources/icons/tools/Part_Offset2D.svg) | 2D Offset | Utility to offset planar shapes |

<a id="button-bim_offsettools"></a>
### Offset Tools — `BIM_OffsetTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| — | Offset Tools | Offset Tools |

Source-defined dropdown choices: ![2D Offset](../../../src/Mod/Part/Gui/Resources/icons/tools/Part_Offset2D.svg) [2D Offset](#button-bim_offset2d); ![Offset](toolbar-icons/Draft_Offset.png) [Offset](#button-draft_offset).

<a id="button-bim_preflight"></a>
### Preflight Checks — `BIM_Preflight`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Preflight Checks](../../../src/Mod/BIM/Resources/icons/BIM_Preflight.svg) | Preflight Checks | Checks several characteristics of this model before exporting to IFC |

<a id="button-bim_projectmanager"></a>
### Setup Project — `BIM_ProjectManager`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Setup Project](../../../src/Mod/BIM/Resources/icons/BIM_ProjectManager.svg) | Setup Project | Creates or manages a BIM project |

<a id="button-bim_report"></a>
### Report — `BIM_Report`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Report](../../../src/Mod/BIM/Resources/icons/BIM_Report.svg) | Report | Create a new BIM Report to query model data with SQL |

<a id="button-bim_reporttools"></a>
### Report Tools — `BIM_ReportTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Report Tools](../../../src/Mod/BIM/Resources/icons/BIM_Report.svg) | Report Tools | Report Tools |

Source-defined dropdown choices: ![Report](../../../src/Mod/BIM/Resources/icons/BIM_Report.svg) [Report](#button-bim_report); ![Schedule](../../../src/Mod/BIM/Resources/icons/Arch_Schedule.svg) [Schedule](#button-arch_schedule); ![Survey](../../../src/Mod/BIM/Resources/icons/Arch_Survey.svg) [Survey](#button-arch_survey).

<a id="button-bim_setup"></a>
### BIM Setup — `BIM_Setup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![BIM Setup](../../../src/Gui/Icons/preferences-system.svg) | BIM Setup | Sets common FreeCAD preferences for a BIM workflow |

<a id="button-bim_shape2dcut"></a>
### Section Cut — `BIM_Shape2DCut`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Section Cut](../../../src/Mod/BIM/Resources/icons/Arch_View_Cut.svg) | Section Cut | Creates a 2D projection of only the intersecting faces of the selected objects on the XY-plane. |

<a id="button-bim_shape2dview"></a>
### Section View — `BIM_Shape2DView`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Section View](../../../src/Mod/BIM/Resources/icons/Arch_BuildingPart_Tree.svg) | Section View | Creates a 2D projection of the selected objects on the XY-plane. The initial projection direction is the opposite of the current active view direction. |

<a id="button-bim_simplecopy"></a>
### Simple Copy — `BIM_SimpleCopy`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Simple Copy](../../../src/Mod/BIM/Resources/icons/Tree_Part.svg) | Simple Copy | Creates a simple non-parametric copy |

<a id="button-bim_sketch"></a>
### New Sketch — `BIM_Sketch`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![New Sketch](../../../src/Mod/BIM/Resources/icons/Sketch.svg) | New Sketch | Creates a new sketch in the current working plane |

<a id="button-bim_slab"></a>
### Slab — `BIM_Slab`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Slab](../../../src/Mod/BIM/Resources/icons/BIM_Slab.svg) | Slab | Creates a slab from a planar shape |

<a id="button-bim_splinetools"></a>
### Spline Tools — `BIM_SplineTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Spline Tools](../../../src/Mod/Draft/Resources/icons/Draft_BSpline.svg) | Spline Tools | Spline Tools |

Source-defined dropdown choices: ![B-Spline](toolbar-icons/Draft_BSpline.png) [B-Spline](#button-draft_bspline); ![Bézier Curve](toolbar-icons/Draft_BezCurve.png) [Bézier Curve](#button-draft_bezcurve); ![Cubic Bézier Curve](toolbar-icons/Draft_CubicBezCurve.png) [Cubic Bézier Curve](#button-draft_cubicbezcurve).

<a id="button-bim_tdpage"></a>
### New Page — `BIM_TDPage`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![New Page](../../../src/Mod/BIM/Resources/icons/BIM_PageDefault.svg) | New Page | Creates a new TechDraw page from a template |

<a id="button-bim_tdview"></a>
### New View — `BIM_TDView`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![New View](../../../src/Mod/BIM/Resources/icons/BIM_InsertView.svg) | New View | Inserts a drawing view on a page. To choose where to insert the view when multiple pages are available, select both the view and the page before executing the command. |

<a id="button-bim_text"></a>
### Text — `BIM_Text`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Text](../../../src/Mod/Draft/Resources/icons/Draft_Text.svg) | Text | Create a text in the current 3D view or TechDraw page |

<a id="button-bim_trimex"></a>
### Trimex — `BIM_Trimex`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Trimex](../../../src/Mod/Draft/Resources/icons/Draft_Trimex.svg) | Trimex | Trims or extends the selected object |

<a id="button-bim_unclone"></a>
### Unclone — `BIM_Unclone`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Unclone](../../../src/Mod/BIM/Resources/icons/BIM_Unclone.svg) | Unclone | Creates a selected clone object independent from its original |

<a id="button-bim_windows"></a>
### Manage Doors and Windows — `BIM_Windows`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Manage Doors and Windows](../../../src/Mod/BIM/Resources/icons/BIM_Windows.svg) | Manage Doors and Windows | Manages the different doors and windows of the BIM project |

<a id="button-cam_adaptive"></a>
### Adaptive — `CAM_Adaptive`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Adaptive](toolbar-icons/CAM_Adaptive.png) | Adaptive | Adaptive clearing and profiling |

<a id="button-cam_array"></a>
### Array — `CAM_Array`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Array](toolbar-icons/CAM_Array.png) | Array | Creates an array from selected toolpaths |

<a id="button-cam_dressuptools"></a>
### Array — `CAM_DressupTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Array](toolbar-icons/CAM_DressupTools.png) | Array | Creates an array from a selected toolpath |
| ![Axis Map](toolbar-icons/CAM_DressupTools_1.png) | Axis Map | Remaps one axis to another |
| ![Boundary](toolbar-icons/CAM_DressupTools_2.png) | Boundary | Creates a boundary dress-up from a selected toolpath |
| ![Boundary2](toolbar-icons/CAM_DressupTools_3.png) | Boundary2 | Creates a boundary dress-up from a selected toolpath |
| ![Dogbone](toolbar-icons/CAM_DressupTools_4.png) | Dogbone | Creates a dogbone dress-up object from a selected toolpath |
| ![Drag Knife](toolbar-icons/CAM_DressupTools_5.png) | Drag Knife | Modifies a toolpath to add dragknife corner actions |
| ![Lead In/Out](toolbar-icons/CAM_DressupTools_6.png) | Lead In/Out | Creates entry and exit motions for a selected path |
| ![Mirror](toolbar-icons/CAM_DressupTools_7.png) | Mirror | Creates mirror of a selected path |
| ![Plunge Milling](toolbar-icons/CAM_DressupTools_8.png) | Plunge Milling | Creates plunge milling for a selected path |
| ![Ramp Entry](toolbar-icons/CAM_DressupTools_9.png) | Ramp Entry | Creates a ramp entry dress-up object from a selected toolpath |
| ![Tag](toolbar-icons/CAM_DressupTools_10.png) | Tag | Creates a tag dress-up object from a selected toolpath |
| ![Z Depth Correction](toolbar-icons/CAM_DressupTools_11.png) | Z Depth Correction | Corrects Z depth using a probe map |

<a id="button-cam_drillingtools"></a>
### Drilling — `CAM_DrillingTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Drilling](toolbar-icons/CAM_DrillingTools.png) | Drilling | Creates a Drilling toolpath from the features of a base object |
| ![Thread Milling](toolbar-icons/CAM_DrillingTools_1.png) | Thread Milling | Creates a Thread Milling toolpath from features of a base object |

<a id="button-cam_engravetools"></a>
### Engrave — `CAM_EngraveTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Engrave](toolbar-icons/CAM_EngraveTools.png) | Engrave | Creates an Engraving toolpath around a Draft ShapeString |
| ![Deburr](toolbar-icons/CAM_EngraveTools_1.png) | Deburr | Creates a Deburr toolpath along Edges or around Faces |
| ![Vcarve](toolbar-icons/CAM_EngraveTools_2.png) | Vcarve | Creates a medial line engraving toolpath |

<a id="button-cam_helix"></a>
### Helix — `CAM_Helix`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Helix](toolbar-icons/CAM_Helix.png) | Helix | Creates a Helical toolpath from the features of a base object |

<a id="button-cam_holdingtab"></a>
### Holding Tab — `CAM_HoldingTab`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Holding Tab](../../../src/Gui/Icons/preferences-general.svg) | Holding Tab | Creates a stock bridge preserved by Parallel and Waterline paths |

<a id="button-cam_indexedsetup"></a>
### Indexed Setup — `CAM_IndexedSetup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Indexed Setup](toolbar-icons/CAM_IndexedSetup.png) | Indexed Setup | Creates another manually indexed side of a Job, including its stock and tabs |

<a id="button-cam_inspect"></a>
### Inspect Toolpath — `CAM_Inspect`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Inspect Toolpath](toolbar-icons/CAM_Inspect.png) | Inspect Toolpath | Inspects the contents of a toolpath object |

<a id="button-cam_job"></a>
### New Job — `CAM_Job`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![New Job](toolbar-icons/CAM_Job.png) | New Job | Creates a CAM job |

<a id="button-cam_meshpreparation"></a>
### Review CAM mesh... — `CAM_MeshPreparation`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Review CAM mesh...](toolbar-icons/CAM_MeshPreparation.png) | Review CAM mesh... | Inspect an imported mesh and optionally create an independent reversed-normal copy |

<a id="button-cam_millfacing"></a>
### Mill Facing — `CAM_MillFacing`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Mill Facing](toolbar-icons/CAM_MillFacing.png) | Mill Facing | Create a Mill Facing Operation to machine the top surface of stock |

<a id="button-cam_opactivetoggle"></a>
### Toggle Operation — `CAM_OpActiveToggle`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Toggle Operation](toolbar-icons/CAM_OpActiveToggle.png) | Toggle Operation | Toggles the active state of the operation |

<a id="button-cam_operationcopy"></a>
### Copy Operation — `CAM_OperationCopy`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Copy Operation](toolbar-icons/CAM_OperationCopy.png) | Copy Operation | Copies the operation in the job |

<a id="button-cam_planarsurface"></a>
### Parallel / Waterline — `CAM_PlanarSurface`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Parallel / Waterline](toolbar-icons/CAM_PlanarSurface.png) | Parallel / Waterline | Machines an STL or CAD model with Parallel or Waterline paths |

<a id="button-cam_pocket_shape"></a>
### Pocket Shape — `CAM_Pocket_Shape`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Pocket Shape](toolbar-icons/CAM_Pocket_Shape.png) | Pocket Shape | Creates a pocket toolpath from a face or faces |

<a id="button-cam_posttools"></a>
### Post Process — `CAM_PostTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Post Process](toolbar-icons/CAM_PostTools.png) | Post Process | Post Processes the selected Job |
| ![Post Process Selected](toolbar-icons/CAM_PostTools_1.png) | Post Process Selected | Post Processes the selected operations |

<a id="button-cam_profile"></a>
### Profile — `CAM_Profile`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Profile](toolbar-icons/CAM_Profile.png) | Profile | Profile entire model, selected face(s) or selected edge(s) |

<a id="button-cam_sanity"></a>
### Sanity Check — `CAM_Sanity`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Sanity Check](toolbar-icons/CAM_Sanity.png) | Sanity Check | Checks the CAM job for common errors |

<a id="button-cam_selectloop"></a>
### Finish Selecting Loop — `CAM_SelectLoop`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Finish Selecting Loop](toolbar-icons/CAM_SelectLoop.png) | Finish Selecting Loop | Completes the selection of edges or faces that forms a loop. Works in described sequence, but can be forced by modifier key. Face selection: Vertical face: searching loops faces which forms the walls or vertical faces with same center height (SHIFT). Horizontal face: searching inner edges of the face (CTRL), outer edges of the face (CTRL + ALT) or horizontal faces at the same height (SHIFT). Otherwise select all edges of the face (ALT). Edge selection: One edge: searching loop edges in horizontal plane. Two edges: searching loop edges in wires of the shape or tangent edges (CTRL). Otherwise searching horizontal wires which contain selected edges (ALT). Without sub selection: Select all edges, faces (ALT) or vertexes (CTRL) of the model. |

<a id="button-cam_simtools"></a>
### CAM Simulator — `CAM_SimTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![CAM Simulator](toolbar-icons/CAM_SimTools.png) | CAM Simulator | Simulates G-code on stock |
| ![Legacy CAM Simulator](toolbar-icons/CAM_SimTools_1.png) | Legacy CAM Simulator | Simulates G-code on stock |

<a id="button-cam_simplecopy"></a>
### Simple Copy — `CAM_SimpleCopy`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Simple Copy](toolbar-icons/CAM_SimpleCopy.png) | Simple Copy | Creates a non-parametric copy of another toolpath Several operations can be used with identical tool controller and coolant mode |

<a id="button-cam_slot"></a>
### Slot — `CAM_Slot`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Slot](toolbar-icons/CAM_Slot.png) | Slot | Create a single horizontal slot between two points. Points can be specified through selected geometry or custom points. Allowed selection only from one model: - two vertexes, - one or two edges, - one horizontal or vertical face, - one or two vertical faces. |

<a id="button-cam_toolbitdock"></a>
### Add Toolbit… — `CAM_ToolBitDock`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Add Toolbit…](toolbar-icons/CAM_ToolBitDock.png) | Add Toolbit… | Opens the toolbit selection dialog |

<a id="button-cam_workplane"></a>
### Work Plane — `CAM_Workplane`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Work Plane](toolbar-icons/CAM_Workplane.png) | Work Plane | Create a named work plane on the Job, from a selected planar face or at the Job origin. Operations can share one work plane. |

<a id="button-draft_addconstruction"></a>
### Add to Construction Group — `Draft_AddConstruction`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Add to Construction Group](toolbar-icons/Draft_AddConstruction.png) | Add to Construction Group | Adds the selected objects to the construction group, and changes their appearance to the construction style. The construction group is created if it does not exist. |

<a id="button-draft_addnamedgroup"></a>
### New Named Group — `Draft_AddNamedGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![New Named Group](toolbar-icons/Draft_AddNamedGroup.png) | New Named Group | Adds a group with a given name |

<a id="button-draft_addtogroup"></a>
### Add to Group — `Draft_AddToGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Add to Group](toolbar-icons/Draft_AddToGroup.png) | Add to Group | Adds selected objects to a group, or removes them from any group |

<a id="button-draft_addtolayer"></a>
### Add to Layer — `Draft_AddToLayer`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Add to Layer](toolbar-icons/Draft_AddToLayer.png) | Add to Layer | Adds selected objects to a layer, or removes them from any layer |

<a id="button-draft_annotationstyleeditor"></a>
### Annotation Styles — `Draft_AnnotationStyleEditor`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Annotation Styles](toolbar-icons/Draft_AnnotationStyleEditor.png) | Annotation Styles | Opens an editor to manage or create annotation styles |

<a id="button-draft_arc"></a>
### Arc — `Draft_Arc`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Arc](toolbar-icons/Draft_Arc.png) | Arc | Creates a circular arc from a center point and a radius |

<a id="button-draft_arctools"></a>
### Arc — `Draft_ArcTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Arc](toolbar-icons/Draft_ArcTools.png) | Arc | Creates a circular arc from a center point and a radius |
| ![Arc From 3 Points](toolbar-icons/Draft_ArcTools_1.png) | Arc From 3 Points | Creates a circular arc from 3 points |

<a id="button-draft_arc_3points"></a>
### Arc From 3 Points — `Draft_Arc_3Points`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Arc From 3 Points](toolbar-icons/Draft_Arc_3Points.png) | Arc From 3 Points | Creates a circular arc from 3 points |

<a id="button-draft_arraytools"></a>
### Array — `Draft_ArrayTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Array](toolbar-icons/Draft_ArrayTools.png) | Array | Creates copies of the selected object in an orthogonal pattern |
| ![Polar Array](toolbar-icons/Draft_ArrayTools_1.png) | Polar Array | Creates copies of the selected object in a polar pattern |
| ![Circular Array](toolbar-icons/Draft_ArrayTools_2.png) | Circular Array | Creates copies of the selected object in a radial pattern with 1 or more circular layers |
| ![Path Array](toolbar-icons/Draft_ArrayTools_3.png) | Path Array | Creates copies of the selected object along a selected path |
| ![Path Link Array](toolbar-icons/Draft_ArrayTools_4.png) | Path Link Array | Creates linked copies of the selected object along a selected path |
| ![Point Array](toolbar-icons/Draft_ArrayTools_5.png) | Point Array | Creates copies of the selected object at the points of a point object |
| ![Point Link Array](toolbar-icons/Draft_ArrayTools_6.png) | Point Link Array | Creates linked copies of the selected object at the points of a point object |
| ![Twisted Path Array](toolbar-icons/Draft_ArrayTools_7.png) | Twisted Path Array | Creates twisted copies of the selected object along a selected path |
| ![Twisted Path Link Array](toolbar-icons/Draft_ArrayTools_8.png) | Twisted Path Link Array | Creates twisted linked copies of the selected object along a selected path |

<a id="button-draft_bspline"></a>
### B-Spline — `Draft_BSpline`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![B-Spline](toolbar-icons/Draft_BSpline.png) | B-Spline | Creates a multiple-point B-spline |

<a id="button-draft_bezcurve"></a>
### Bézier Curve — `Draft_BezCurve`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Bézier Curve](toolbar-icons/Draft_BezCurve.png) | Bézier Curve | Creates an n-degree Bézier curve. The more points, the higher the degree. |

<a id="button-draft_beziertools"></a>
### Cubic Bézier Curve — `Draft_BezierTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cubic Bézier Curve](toolbar-icons/Draft_BezierTools.png) | Cubic Bézier Curve | Creates a Bézier curve made of 2nd degree (quadratic) and 3rd degree (cubic) segments. Clicking and dragging allows to define segments. Control points and properties of each knot can be edited after creation. |
| ![Bézier Curve](toolbar-icons/Draft_BezierTools_1.png) | Bézier Curve | Creates an n-degree Bézier curve. The more points, the higher the degree. |

<a id="button-draft_circle"></a>
### Circle — `Draft_Circle`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Circle](toolbar-icons/Draft_Circle.png) | Circle | Creates a circle (full circular arc) |

<a id="button-draft_circulararray"></a>
### Circular Array — `Draft_CircularArray`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Circular Array](toolbar-icons/Draft_CircularArray.png) | Circular Array | Creates copies of the selected object in a radial pattern with 1 or more circular layers |

<a id="button-draft_clone"></a>
### Clone — `Draft_Clone`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Clone](toolbar-icons/Draft_Clone.png) | Clone | Creates a clone of the selected objects |

<a id="button-draft_cubicbezcurve"></a>
### Cubic Bézier Curve — `Draft_CubicBezCurve`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cubic Bézier Curve](toolbar-icons/Draft_CubicBezCurve.png) | Cubic Bézier Curve | Creates a Bézier curve made of 2nd degree (quadratic) and 3rd degree (cubic) segments. Clicking and dragging allows to define segments. Control points and properties of each knot can be edited after creation. |

<a id="button-draft_dimension"></a>
### Dimension — `Draft_Dimension`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Dimension](toolbar-icons/Draft_Dimension.png) | Dimension | Creates a linear dimension for a straight edge, a circular edge, or 2 picked points, or an angular dimension for 2 straight edges |

<a id="button-draft_downgrade"></a>
### Downgrade — `Draft_Downgrade`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Downgrade](toolbar-icons/Draft_Downgrade.png) | Downgrade | Downgrades the selected objects into simpler shapes. The result of the operation depends on the types of objects, which may be downgraded several times in a row. For example, a 3D solid is deconstructed into separate faces, wires, and then edges. Faces can also be subtracted. |

<a id="button-draft_draft2sketch"></a>
### Draft to Sketch — `Draft_Draft2Sketch`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Draft to Sketch](toolbar-icons/Draft_Draft2Sketch.png) | Draft to Sketch | Converts bidirectionally between Draft objects and sketches. Multiple selected Draft objects are converted into a single sketch. However, a single sketch with disconnected traces is converted into several individual Draft objects. |

<a id="button-draft_edit"></a>
### Edit — `Draft_Edit`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Edit](toolbar-icons/Draft_Edit.png) | Edit | Edits the active object |

<a id="button-draft_ellipse"></a>
### Ellipse — `Draft_Ellipse`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Ellipse](toolbar-icons/Draft_Ellipse.png) | Ellipse | Creates an ellipse |

<a id="button-draft_facebinder"></a>
### Facebinder — `Draft_Facebinder`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Facebinder](toolbar-icons/Draft_Facebinder.png) | Facebinder | Creates a facebinder from the selected faces |

<a id="button-draft_fillet"></a>
### Fillet — `Draft_Fillet`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Fillet](toolbar-icons/Draft_Fillet.png) | Fillet | Creates a fillet between 2 selected edges |

<a id="button-draft_flipdimension"></a>
### Flip Dimension — `Draft_FlipDimension`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Flip Dimension](toolbar-icons/Draft_FlipDimension.png) | Flip Dimension | Flips the normal direction of the selected dimensions (linear, radial, angular). If other objects are selected they are ignored. |

<a id="button-draft_hatch"></a>
### Hatch — `Draft_Hatch`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Hatch](toolbar-icons/Draft_Hatch.png) | Hatch | Creates hatches on the faces of a selected object |

<a id="button-draft_join"></a>
### Join — `Draft_Join`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Join](toolbar-icons/Draft_Join.png) | Join | Joins the selected lines or polylines into a single object. The lines must share a common point at the start or at the end. |

<a id="button-draft_label"></a>
### Label — `Draft_Label`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Label](toolbar-icons/Draft_Label.png) | Label | Creates a label, optionally attached to a selected object or subelement |

<a id="button-draft_layermanager"></a>
### Manage Layers — `Draft_LayerManager`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Manage Layers](toolbar-icons/Draft_LayerManager.png) | Manage Layers | Allows to modify the layers |

<a id="button-draft_line"></a>
### Line — `Draft_Line`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Line](toolbar-icons/Draft_Line.png) | Line | Creates a 2-point line |

<a id="button-draft_mirror"></a>
### Mirror — `Draft_Mirror`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Mirror](toolbar-icons/Draft_Mirror.png) | Mirror | Mirrors the selected objects along a line defined by 2 points |

<a id="button-draft_move"></a>
### Move — `Draft_Move`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Move](toolbar-icons/Draft_Move.png) | Move | Moves the selected objects. If the "Copy" option is active, it creates displaced copies. |

<a id="button-draft_offset"></a>
### Offset — `Draft_Offset`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Offset](toolbar-icons/Draft_Offset.png) | Offset | Offsets the selected object. It can also create an offset copy of the original object. |

<a id="button-draft_orthoarray"></a>
### Array — `Draft_OrthoArray`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Array](toolbar-icons/Draft_OrthoArray.png) | Array | Creates copies of the selected object in an orthogonal pattern |

<a id="button-draft_patharray"></a>
### Path Array — `Draft_PathArray`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Path Array](toolbar-icons/Draft_PathArray.png) | Path Array | Creates copies of the selected object along a selected path |

<a id="button-draft_pathlinkarray"></a>
### Path Link Array — `Draft_PathLinkArray`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Path Link Array](toolbar-icons/Draft_PathLinkArray.png) | Path Link Array | Creates linked copies of the selected object along a selected path |

<a id="button-draft_pathtwistedarray"></a>
### Twisted Path Array — `Draft_PathTwistedArray`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Twisted Path Array](toolbar-icons/Draft_PathTwistedArray.png) | Twisted Path Array | Creates twisted copies of the selected object along a selected path |

<a id="button-draft_pathtwistedlinkarray"></a>
### Twisted Path Link Array — `Draft_PathTwistedLinkArray`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Twisted Path Link Array](toolbar-icons/Draft_PathTwistedLinkArray.png) | Twisted Path Link Array | Creates twisted linked copies of the selected object along a selected path |

<a id="button-draft_point"></a>
### Point — `Draft_Point`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Point](toolbar-icons/Draft_Point.png) | Point | Creates a point |

<a id="button-draft_pointarray"></a>
### Point Array — `Draft_PointArray`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Point Array](toolbar-icons/Draft_PointArray.png) | Point Array | Creates copies of the selected object at the points of a point object |

<a id="button-draft_pointlinkarray"></a>
### Point Link Array — `Draft_PointLinkArray`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Point Link Array](toolbar-icons/Draft_PointLinkArray.png) | Point Link Array | Creates linked copies of the selected object at the points of a point object |

<a id="button-draft_polararray"></a>
### Polar Array — `Draft_PolarArray`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Polar Array](toolbar-icons/Draft_PolarArray.png) | Polar Array | Creates copies of the selected object in a polar pattern |

<a id="button-draft_polygon"></a>
### Polygon — `Draft_Polygon`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Polygon](toolbar-icons/Draft_Polygon.png) | Polygon | Creates a regular polygon (triangle, square, pentagon…) |

<a id="button-draft_rectangle"></a>
### Rectangle — `Draft_Rectangle`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Rectangle](toolbar-icons/Draft_Rectangle.png) | Rectangle | Creates a 2-point rectangle |

<a id="button-draft_rotate"></a>
### Rotate — `Draft_Rotate`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Rotate](toolbar-icons/Draft_Rotate.png) | Rotate | Rotates the selected objects. If the "Copy" option is active, it will create rotated copies. |

<a id="button-draft_scale"></a>
### Scale — `Draft_Scale`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Scale](toolbar-icons/Draft_Scale.png) | Scale | Scales the selected objects from a base point |

<a id="button-draft_selectgroup"></a>
### Select Group — `Draft_SelectGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Select Group](toolbar-icons/Draft_SelectGroup.png) | Select Group | Selects the contents of selected groups. For selected non-group objects, the contents of the group they are in are selected. |

<a id="button-draft_shape2dview"></a>
### Shape 2D View — `Draft_Shape2DView`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Shape 2D View](toolbar-icons/Draft_Shape2DView.png) | Shape 2D View | Creates a 2D projection of the selected objects on the XY-plane. The initial projection direction is the opposite of the current active view direction. |

<a id="button-draft_shapestring"></a>
### Shape From Text — `Draft_ShapeString`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Shape From Text](toolbar-icons/Draft_ShapeString.png) | Shape From Text | Creates a shape from a text string and a specified font |

<a id="button-draft_slope"></a>
### Set Slope — `Draft_Slope`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Set Slope](toolbar-icons/Draft_Slope.png) | Set Slope | Sets the slope of the selected line by changing the value of the Z value of one of its points. If a polyline is selected, it will apply the slope transformation to each of its segments. The slope will always change the Z value, therefore this command only works well for straight Draft lines that are drawn on the XY-plane. |

<a id="button-draft_snap_angle"></a>
### Snap Angle — `Draft_Snap_Angle`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Snap Angle](toolbar-icons/Draft_Snap_Angle.png) | Snap Angle | Snaps to the special cardinal points on circular edges, at multiples of 30° and 45° |

<a id="button-draft_snap_center"></a>
### Snap Center — `Draft_Snap_Center`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Snap Center](toolbar-icons/Draft_Snap_Center.png) | Snap Center | Snaps to the center point of faces and circular edges, and to the placement point of working plane proxies and building parts |

<a id="button-draft_snap_dimensions"></a>
### Snap Dimensions — `Draft_Snap_Dimensions`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Snap Dimensions](toolbar-icons/Draft_Snap_Dimensions.png) | Snap Dimensions | Shows temporary X and Y dimensions |

<a id="button-draft_snap_endpoint"></a>
### Snap Endpoint — `Draft_Snap_Endpoint`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Snap Endpoint](toolbar-icons/Draft_Snap_Endpoint.png) | Snap Endpoint | Snaps to the endpoints of edges |

<a id="button-draft_snap_extension"></a>
### Snap Extension — `Draft_Snap_Extension`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Snap Extension](toolbar-icons/Draft_Snap_Extension.png) | Snap Extension | Snaps to an imaginary line that extends beyond the endpoints of straight edges |

<a id="button-draft_snap_grid"></a>
### Snap Grid — `Draft_Snap_Grid`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Snap Grid](toolbar-icons/Draft_Snap_Grid.png) | Snap Grid | Snaps to the intersections of grid lines |

<a id="button-draft_snap_intersection"></a>
### Snap Intersection — `Draft_Snap_Intersection`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Snap Intersection](toolbar-icons/Draft_Snap_Intersection.png) | Snap Intersection | Snaps to the intersection of 2 edges, and the intersection of a face and an edge |

<a id="button-draft_snap_lock"></a>
### Snap Lock — `Draft_Snap_Lock`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Snap Lock](toolbar-icons/Draft_Snap_Lock.png) | Snap Lock | Enables or disables snapping globally |

<a id="button-draft_snap_midpoint"></a>
### Snap Midpoint — `Draft_Snap_Midpoint`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Snap Midpoint](toolbar-icons/Draft_Snap_Midpoint.png) | Snap Midpoint | Snaps to the midpoint of edges |

<a id="button-draft_snap_near"></a>
### Snap Near — `Draft_Snap_Near`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Snap Near](toolbar-icons/Draft_Snap_Near.png) | Snap Near | Snaps to the nearest point on faces and edges |

<a id="button-draft_snap_ortho"></a>
### Snap Ortho — `Draft_Snap_Ortho`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Snap Ortho](toolbar-icons/Draft_Snap_Ortho.png) | Snap Ortho | Snaps to imaginary lines that cross the previous point at multiples of 45° |

<a id="button-draft_snap_parallel"></a>
### Snap Parallel — `Draft_Snap_Parallel`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Snap Parallel](toolbar-icons/Draft_Snap_Parallel.png) | Snap Parallel | Snaps to an imaginary line parallel to straight edges |

<a id="button-draft_snap_perpendicular"></a>
### Snap Perpendicular — `Draft_Snap_Perpendicular`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Snap Perpendicular](toolbar-icons/Draft_Snap_Perpendicular.png) | Snap Perpendicular | Snaps to the perpendicular points on faces and edges |

<a id="button-draft_snap_special"></a>
### Snap Special — `Draft_Snap_Special`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Snap Special](toolbar-icons/Draft_Snap_Special.png) | Snap Special | Snaps to special points defined by the object |

<a id="button-draft_snap_workingplane"></a>
### Snap Working Plane — `Draft_Snap_WorkingPlane`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Snap Working Plane](toolbar-icons/Draft_Snap_WorkingPlane.png) | Snap Working Plane | Projects snap points onto the current working plane |

<a id="button-draft_split"></a>
### Split — `Draft_Split`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Split](toolbar-icons/Draft_Split.png) | Split | Splits the selected line or polyline at a specified point |

<a id="button-draft_stretch"></a>
### Stretch — `Draft_Stretch`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Stretch](toolbar-icons/Draft_Stretch.png) | Stretch | Stretches the selected objects |

<a id="button-draft_subelementhighlight"></a>
### Highlight Subelements — `Draft_SubelementHighlight`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Highlight Subelements](toolbar-icons/Draft_SubelementHighlight.png) | Highlight Subelements | Highlights the subelements of the selected objects, to be able to move, rotate, and scale them |

<a id="button-draft_text"></a>
### Text — `Draft_Text`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Text](toolbar-icons/Draft_Text.png) | Text | Creates a multi-line annotation |

<a id="button-draft_toggledisplaymode"></a>
### Toggle Wireframe — `Draft_ToggleDisplayMode`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Toggle Wireframe](toolbar-icons/Draft_ToggleDisplayMode.png) | Toggle Wireframe | Switches the view style of the selected objects from Flat Lines to Wireframe and back |

<a id="button-draft_togglegrid"></a>
### Toggle Grid — `Draft_ToggleGrid`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Toggle Grid](toolbar-icons/Draft_ToggleGrid.png) | Toggle Grid | Toggles the visibility of the Draft grid |

<a id="button-draft_trimex"></a>
### Trimex — `Draft_Trimex`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Trimex](toolbar-icons/Draft_Trimex.png) | Trimex | Trims or extends the selected object |

<a id="button-draft_updateshape2dview"></a>
### Force 2D View Update — `Draft_UpdateShape2DView`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Force 2D View Update](toolbar-icons/Draft_UpdateShape2DView.png) | Force 2D View Update | Forces an update of the selected 2D Views or all 2D Views in the document. The 'Auto Update' property of the views is ignored. |

<a id="button-draft_upgrade"></a>
### Upgrade — `Draft_Upgrade`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Upgrade](toolbar-icons/Draft_Upgrade.png) | Upgrade | Upgrades the selected objects into more complex shapes. The result of the operation depends on the types of objects, which may be able to be upgraded several times in a row. For example, it can join the selected objects into one, convert simple edges into parametric polylines, convert closed edges into filled faces and parametric polygons, and merge faces into a single face. |

<a id="button-draft_wire"></a>
### Polyline — `Draft_Wire`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Polyline](toolbar-icons/Draft_Wire.png) | Polyline | Creates a polyline |

<a id="button-draft_wiretobspline"></a>
### Convert Wire/B-Spline — `Draft_WireToBSpline`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Convert Wire/B-Spline](toolbar-icons/Draft_WireToBSpline.png) | Convert Wire/B-Spline | Converts the selected polyline to a B-spline, or the selected B-spline to a polyline |

<a id="button-draft_workingplaneproxy"></a>
### Working Plane Proxy — `Draft_WorkingPlaneProxy`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Working Plane Proxy](toolbar-icons/Draft_WorkingPlaneProxy.png) | Working Plane Proxy | Creates a proxy object from the current working plane that allows to restore the camera position and visibility of objects |

<a id="button-fem_analysis"></a>
### New Analysis — `FEM_Analysis`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![New Analysis](../../../src/Mod/Fem/Gui/Resources/icons/FEM_Analysis.svg) | New Analysis | Creates an analysis container with default solver |

<a id="button-fem_clippingplaneadd"></a>
### Clipping Plane on Face — `FEM_ClippingPlaneAdd`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Clipping Plane on Face](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ClippingPlaneAdd.svg) | Clipping Plane on Face | Adds a clipping plane on a selected face |

<a id="button-fem_clippingplaneremoveall"></a>
### Remove All Clipping Planes — `FEM_ClippingPlaneRemoveAll`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Remove All Clipping Planes](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ClippingPlaneRemoveAll.svg) | Remove All Clipping Planes | Removes all clipping planes |

<a id="button-fem_compemconstraints"></a>
### Electromagnetic Boundary Conditions — `FEM_CompEmConstraints`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| — | Electromagnetic Boundary Conditions | Electromagnetic boundary conditions |

Source-defined dropdown choices: ![Electromagnetic Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintElectromagnetic.svg) [Electromagnetic Boundary Condition](#button-fem_constraintelectromagnetic); ![Current Density Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintCurrentDensity.svg) [Current Density Boundary Condition](#button-fem_constraintcurrentdensity); ![Magnetization Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintMagnetization.svg) [Magnetization Boundary Condition](#button-fem_constraintmagnetization); ![Electric Charge Density](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintElectricChargeDensity.svg) [Electric Charge Density](#button-fem_constraintelectricchargedensity).

<a id="button-fem_compemequations"></a>
### Electromagnetic Equations — `FEM_CompEmEquations`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| — | Electromagnetic Equations | Electromagnetic equations for the Elmer solver |

Source-defined dropdown choices: ![Electrostatic Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationElectrostatic.svg) [Electrostatic Equation](#button-fem_equationelectrostatic); ![Electricforce Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationElectricforce.svg) [Electricforce Equation](#button-fem_equationelectricforce); ![Magnetodynamic Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationMagnetodynamic.svg) [Magnetodynamic Equation](#button-fem_equationmagnetodynamic); ![Magnetodynamic 2D Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationMagnetodynamic2D.svg) [Magnetodynamic 2D Equation](#button-fem_equationmagnetodynamic2d); ![Static Current Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationStaticCurrent.svg) [Static Current Equation](#button-fem_equationstaticcurrent).

<a id="button-fem_compmechequations"></a>
### Mechanical Equations — `FEM_CompMechEquations`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| — | Mechanical Equations | Mechanical equations for the Elmer solver |

Source-defined dropdown choices: ![Elasticity Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationElasticity.svg) [Elasticity Equation](#button-fem_equationelasticity); ![Deformation Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationDeformation.svg) [Deformation Equation](#button-fem_equationdeformation).

<a id="button-fem_compsolvers"></a>
### Solvers — `FEM_CompSolvers`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| — | Solvers | Creates a FEM solver |

Source-defined dropdown choices: ![Solver CalculiX](../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverStandard.svg) [Solver CalculiX](#button-fem_solvercalculix); ![Solver Elmer](../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverElmer.svg) [Solver Elmer](#button-fem_solverelmer); ![Solver Mystran](../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverMystran.svg) [Solver Mystran](#button-fem_solvermystran); ![Solver Z88](../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverZ88.svg) [Solver Z88](#button-fem_solverz88).

<a id="button-fem_constraintbodyheatsource"></a>
### Body Heat Source — `FEM_ConstraintBodyHeatSource`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Body Heat Source](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintBodyHeatSource.svg) | Body Heat Source | Creates a body heat source |

<a id="button-fem_constraintcentrif"></a>
### Centrifugal Load — `FEM_ConstraintCentrif`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Centrifugal Load](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintCentrif.svg) | Centrifugal Load | Creates a centrifugal load |

<a id="button-fem_constraintcontact"></a>
### Contact Constraint — `FEM_ConstraintContact`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Contact Constraint](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintContact.svg) | Contact Constraint | Creates a contact constraint between faces |

<a id="button-fem_constraintcurrentdensity"></a>
### Current Density Boundary Condition — `FEM_ConstraintCurrentDensity`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Current Density Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintCurrentDensity.svg) | Current Density Boundary Condition | Creates a current density boundary condition |

<a id="button-fem_constraintdisplacement"></a>
### Displacement Boundary Condition — `FEM_ConstraintDisplacement`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Displacement Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintDisplacement.svg) | Displacement Boundary Condition | Creates a displacement boundary condition for a geometric entity |

<a id="button-fem_constraintelectricchargedensity"></a>
### Electric Charge Density — `FEM_ConstraintElectricChargeDensity`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Electric Charge Density](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintElectricChargeDensity.svg) | Electric Charge Density | Creates an electric charge density |

<a id="button-fem_constraintelectromagnetic"></a>
### Electromagnetic Boundary Condition — `FEM_ConstraintElectromagnetic`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Electromagnetic Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintElectromagnetic.svg) | Electromagnetic Boundary Condition | Creates an electromagnetic boundary condition |

<a id="button-fem_constraintfixed"></a>
### Fixed Boundary Condition — `FEM_ConstraintFixed`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Fixed Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintFixed.svg) | Fixed Boundary Condition | Creates a fixed boundary condition for a geometric entity |

<a id="button-fem_constraintflowvelocity"></a>
### Flow Velocity Boundary Condition — `FEM_ConstraintFlowVelocity`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Flow Velocity Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintFlowVelocity.svg) | Flow Velocity Boundary Condition | Creates a flow velocity boundary condition |

<a id="button-fem_constraintforce"></a>
### Force Load — `FEM_ConstraintForce`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Force Load](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintForce.svg) | Force Load | Creates a force load applied to a geometric entity |

<a id="button-fem_constraintheatflux"></a>
### Heat Flux Load — `FEM_ConstraintHeatflux`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Heat Flux Load](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintHeatflux.svg) | Heat Flux Load | Creates a heat flux load acting on a face |

<a id="button-fem_constraintinitialflowvelocity"></a>
### Initial Flow Velocity Condition — `FEM_ConstraintInitialFlowVelocity`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Initial Flow Velocity Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialFlowVelocity.svg) | Initial Flow Velocity Condition | Creates an initial flow velocity condition |

<a id="button-fem_constraintinitialpressure"></a>
### Initial Pressure Condition — `FEM_ConstraintInitialPressure`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Initial Pressure Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialPressure.svg) | Initial Pressure Condition | Creates an initial pressure condition |

<a id="button-fem_constraintinitialtemperature"></a>
### Initial Temperature — `FEM_ConstraintInitialTemperature`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Initial Temperature](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintInitialTemperature.svg) | Initial Temperature | Creates an initial temperature acting on a body |

<a id="button-fem_constraintmagnetization"></a>
### Magnetization Boundary Condition — `FEM_ConstraintMagnetization`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Magnetization Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintMagnetization.svg) | Magnetization Boundary Condition | Creates a magnetization boundary condition |

<a id="button-fem_constraintplanerotation"></a>
### Plane Multi-Point Constraint — `FEM_ConstraintPlaneRotation`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Plane Multi-Point Constraint](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintPlaneRotation.svg) | Plane Multi-Point Constraint | Creates a plane multi-point constraint for a face |

<a id="button-fem_constraintpressure"></a>
### Pressure Load — `FEM_ConstraintPressure`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Pressure Load](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintPressure.svg) | Pressure Load | Creates a pressure load acting on a face |

<a id="button-fem_constraintrigidbody"></a>
### Rigid Body Constraint — `FEM_ConstraintRigidBody`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Rigid Body Constraint](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintRigidBody.svg) | Rigid Body Constraint | Creates a rigid body constraint for a geometric entity |

<a id="button-fem_constraintsectionprint"></a>
### Section Print Feature — `FEM_ConstraintSectionPrint`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Section Print Feature](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSectionPrint.svg) | Section Print Feature | Creates a section print feature |

<a id="button-fem_constraintselfweight"></a>
### Gravity Load — `FEM_ConstraintSelfWeight`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Gravity Load](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSelfWeight.svg) | Gravity Load | Creates a gravity load |

<a id="button-fem_constraintspring"></a>
### Spring Boundary Condition — `FEM_ConstraintSpring`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Spring Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintSpring.svg) | Spring Boundary Condition | Creates a spring boundary condition on a face |

<a id="button-fem_constrainttemperature"></a>
### Temperature Boundary Condition — `FEM_ConstraintTemperature`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Temperature Boundary Condition](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTemperature.svg) | Temperature Boundary Condition | Creates a temperature/concentrated heat flux load acting on a face |

<a id="button-fem_constrainttie"></a>
### Tie Constraint — `FEM_ConstraintTie`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Tie Constraint](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTie.svg) | Tie Constraint | Creates a tie constraint |

<a id="button-fem_constrainttransform"></a>
### Local Coordinate System — `FEM_ConstraintTransform`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Local Coordinate System](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ConstraintTransform.svg) | Local Coordinate System | Creates a local coordinate system on a face |

<a id="button-fem_elementfluid1d"></a>
### Fluid Section for 1D Flow — `FEM_ElementFluid1D`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Fluid Section for 1D Flow](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementFluid1D.svg) | Fluid Section for 1D Flow | Creates a fluid section for 1D flow |

<a id="button-fem_elementgeometry1d"></a>
### Beam Cross Section — `FEM_ElementGeometry1D`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Beam Cross Section](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementGeometry1D.svg) | Beam Cross Section | Creates a beam cross section |

<a id="button-fem_elementgeometry2d"></a>
### Shell Plate Thickness — `FEM_ElementGeometry2D`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Shell Plate Thickness](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementGeometry2D.svg) | Shell Plate Thickness | Creates a shell plate thickness |

<a id="button-fem_elementrotation1d"></a>
### Beam Rotation — `FEM_ElementRotation1D`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Beam Rotation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ElementRotation1D.svg) | Beam Rotation | Creates a beam rotation |

<a id="button-fem_equationdeformation"></a>
### Deformation Equation — `FEM_EquationDeformation`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Deformation Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationDeformation.svg) | Deformation Equation | Creates an equation for deformation (nonlinear elasticity) |

<a id="button-fem_equationelasticity"></a>
### Elasticity Equation — `FEM_EquationElasticity`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Elasticity Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationElasticity.svg) | Elasticity Equation | Creates an equation for elasticity (stress) |

<a id="button-fem_equationelectricforce"></a>
### Electricforce Equation — `FEM_EquationElectricforce`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Electricforce Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationElectricforce.svg) | Electricforce Equation | Creates an equation for electric forces |

<a id="button-fem_equationelectrostatic"></a>
### Electrostatic Equation — `FEM_EquationElectrostatic`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Electrostatic Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationElectrostatic.svg) | Electrostatic Equation | Creates an equation for electrostatic |

<a id="button-fem_equationflow"></a>
### Flow Equation — `FEM_EquationFlow`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Flow Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationFlow.svg) | Flow Equation | Creates an equation for flow |

<a id="button-fem_equationflux"></a>
### Flux Equation — `FEM_EquationFlux`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Flux Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationFlux.svg) | Flux Equation | Creates an equation for flux |

<a id="button-fem_equationheat"></a>
### Heat Equation — `FEM_EquationHeat`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Heat Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationHeat.svg) | Heat Equation | Creates an equation for heat |

<a id="button-fem_equationmagnetodynamic"></a>
### Magnetodynamic Equation — `FEM_EquationMagnetodynamic`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Magnetodynamic Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationMagnetodynamic.svg) | Magnetodynamic Equation | Creates an equation for magnetodynamic forces |

<a id="button-fem_equationmagnetodynamic2d"></a>
### Magnetodynamic 2D Equation — `FEM_EquationMagnetodynamic2D`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Magnetodynamic 2D Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationMagnetodynamic2D.svg) | Magnetodynamic 2D Equation | Creates an equation for 2D magnetodynamic forces |

<a id="button-fem_equationstaticcurrent"></a>
### Static Current Equation — `FEM_EquationStaticCurrent`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Static Current Equation](../../../src/Mod/Fem/Gui/Resources/icons/FEM_EquationStaticCurrent.svg) | Static Current Equation | Creates an equation for static current |

<a id="button-fem_examples"></a>
### FEM Examples — `FEM_Examples`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![FEM Examples](../../../src/Mod/Fem/Gui/Resources/icons/FemWorkbench.svg) | FEM Examples | Opens the FEM examples |

<a id="button-fem_femmesh2mesh"></a>
### FEM Mesh to Mesh — `FEM_FEMMesh2Mesh`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![FEM Mesh to Mesh](../../../src/Mod/Fem/Gui/Resources/icons/FEM_FEMMesh2Mesh.svg) | FEM Mesh to Mesh | Converts the surface of a FEM mesh to a mesh |

<a id="button-fem_materialeditor"></a>
### Material Editor — `FEM_MaterialEditor`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Material Editor](../../../src/Mod/BIM/Resources/icons/Arch_Material_Group.svg) | Material Editor | Opens the FreeCAD material editor |

<a id="button-fem_materialfluid"></a>
### Fluid Material — `FEM_MaterialFluid`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Fluid Material](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialFluid.svg) | Fluid Material | Creates a fluid material |

<a id="button-fem_materialmechanicalnonlinear"></a>
### Non-Linear Mechanical Material — `FEM_MaterialMechanicalNonlinear`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Non-Linear Mechanical Material](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialMechanicalNonlinear.svg) | Non-Linear Mechanical Material | Add non-linear mechanical properties to material |

<a id="button-fem_materialreinforced"></a>
### Reinforced Material (Concrete) — `FEM_MaterialReinforced`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Reinforced Material (Concrete)](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialReinforced.svg) | Reinforced Material (Concrete) | Creates a material for reinforced matrix material such as concrete |

<a id="button-fem_materialsolid"></a>
### Solid Material — `FEM_MaterialSolid`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Solid Material](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MaterialSolid.svg) | Solid Material | Creates a solid material |

<a id="button-fem_meshadvanced"></a>
### Advanced Refinement Types — `FEM_MeshAdvanced`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Advanced Refinement Types](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshAdvanced.svg) | Advanced Refinement Types | Allows to define the mesh size by various advanced means |

<a id="button-fem_meshboundarylayer"></a>
### 2D Boundary Layer — `FEM_MeshBoundaryLayer`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![2D Boundary Layer](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshBoundaryLayer.svg) | 2D Boundary Layer | Adds a structured layer of mesh elements on 2D model boundaries |

<a id="button-fem_meshdistance"></a>
### Distance-Based Refinement — `FEM_MeshDistance`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Distance-Based Refinement](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshDistance.svg) | Distance-Based Refinement | Sets mesh size based on the distance to vertices, edges, and faces |

<a id="button-fem_meshgmshrefinement"></a>
### GMSH Refinements — `FEM_MeshGMSHRefinement`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| — | GMSH Refinements | Mesh refinements for the GMSH mesh generation |

Source-defined dropdown choices: ![Distance-Based Refinement](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshDistance.svg) [Distance-Based Refinement](#button-fem_meshdistance); ![2D Boundary Layer](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshBoundaryLayer.svg) [2D Boundary Layer](#button-fem_meshboundarylayer); ![Shape-Based Refinement](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshShape.svg) [Shape-Based Refinement](#button-fem_meshshape); ![Manipulate Refinement](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshManipulate.svg) [Manipulate Refinement](#button-fem_meshmanipulate); ![Advanced Refinement Types](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshAdvanced.svg) [Advanced Refinement Types](#button-fem_meshadvanced); ![Structured Transfinite Curve](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshTransfiniteCurve.svg) [Structured Transfinite Curve](#button-fem_meshtransfinitecurve); ![Structured Transfinite Surface](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshTransfiniteSurface.svg) [Structured Transfinite Surface](#button-fem_meshtransfinitesurface); ![Structured Transfinite Volume](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshTransfiniteVolume.svg) [Structured Transfinite Volume](#button-fem_meshtransfinitevolume).

<a id="button-fem_meshgmshfromshape"></a>
### Mesh From Shape by Gmsh — `FEM_MeshGmshFromShape`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Mesh From Shape by Gmsh](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshGmshFromShape.svg) | Mesh From Shape by Gmsh | Creates a FEM mesh from a shape by Gmsh mesher |

<a id="button-fem_meshgroup"></a>
### Mesh Group — `FEM_MeshGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Mesh Group](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshGroup.svg) | Mesh Group | Creates a mesh group |

<a id="button-fem_meshmanipulate"></a>
### Manipulate Refinement — `FEM_MeshManipulate`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Manipulate Refinement](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshManipulate.svg) | Manipulate Refinement | Allows to manipulate the output of a refinement in various ways |

<a id="button-fem_meshnetgenfromshape"></a>
### Mesh From Shape by Netgen — `FEM_MeshNetgenFromShape`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Mesh From Shape by Netgen](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshNetgenFromShape.svg) | Mesh From Shape by Netgen | Creates a FEM mesh from a solid or face shape by Netgen internal mesher |

<a id="button-fem_meshregion"></a>
### Mesh Refinement — `FEM_MeshRegion`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Mesh Refinement](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshRegion.svg) | Mesh Refinement | Creates a FEM mesh refinement |

<a id="button-fem_meshshape"></a>
### Shape-Based Refinement — `FEM_MeshShape`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Shape-Based Refinement](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshShape.svg) | Shape-Based Refinement | Sets mesh size within and outside of a geometric shape (box, sphere, cylinder) |

<a id="button-fem_meshtransfinitecurve"></a>
### Structured Transfinite Curve — `FEM_MeshTransfiniteCurve`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Structured Transfinite Curve](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshTransfiniteCurve.svg) | Structured Transfinite Curve | Creates a fixed number of nodes on an edge with a structured algorithm |

<a id="button-fem_meshtransfinitesurface"></a>
### Structured Transfinite Surface — `FEM_MeshTransfiniteSurface`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Structured Transfinite Surface](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshTransfiniteSurface.svg) | Structured Transfinite Surface | Creates a structured mesh on a face |

<a id="button-fem_meshtransfinitevolume"></a>
### Structured Transfinite Volume — `FEM_MeshTransfiniteVolume`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Structured Transfinite Volume](../../../src/Mod/Fem/Gui/Resources/icons/FEM_MeshTransfiniteVolume.svg) | Structured Transfinite Volume | Creates a structured mesh in a 4- or 5-sided volume bounded by transfinite surfaces |

<a id="button-fem_postapplychanges"></a>
### Apply Changes to Pipeline — `FEM_PostApplyChanges`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Apply Changes to Pipeline](../../../src/Gui/Icons/view-refresh.svg) | Apply Changes to Pipeline | Applies changes to parameters directly and not on recompute only |

<a id="button-fem_postbranchfilter"></a>
### Pipeline Branch — `FEM_PostBranchFilter`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Pipeline Branch](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostBranchFilter.svg) | Pipeline Branch | Branches the pipeline into a new path |

<a id="button-fem_postcreatefunctions"></a>
### Filter Functions — `FEM_PostCreateFunctions`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| — | Filter Functions | Functions for use in postprocessing filter |

<a id="button-fem_postfiltercalculator"></a>
### Calculator Filter — `FEM_PostFilterCalculator`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Calculator Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterCalculator.svg) | Calculator Filter | Creates a new field from current data |

<a id="button-fem_postfilterclipregion"></a>
### Region Clip Filter — `FEM_PostFilterClipRegion`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Region Clip Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterClipRegion.svg) | Region Clip Filter | Defines a clip filter which uses functions to define the clipped region |

<a id="button-fem_postfilterclipscalar"></a>
### Scalar Clip Filter — `FEM_PostFilterClipScalar`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Scalar Clip Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterClipScalar.svg) | Scalar Clip Filter | Defines a clip filter which clips a field with a scalar value |

<a id="button-fem_postfiltercontours"></a>
### Contours Filter — `FEM_PostFilterContours`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Contours Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterContours.svg) | Contours Filter | Defines a contours filter that displays iso contours |

<a id="button-fem_postfiltercutfunction"></a>
### Function Cut Filter — `FEM_PostFilterCutFunction`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Function Cut Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterCutFunction.svg) | Function Cut Filter | Cuts the data along an implicit function |

<a id="button-fem_postfilterdataalongline"></a>
### Line Clip Filter — `FEM_PostFilterDataAlongLine`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Line Clip Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterDataAlongLine.svg) | Line Clip Filter | Defines a clip filter which clips a field along a line |

<a id="button-fem_postfilterdataatpoint"></a>
### Data at Point Clip Filter — `FEM_PostFilterDataAtPoint`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Data at Point Clip Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterDataAtPoint.svg) | Data at Point Clip Filter | Defines a clip filter which clips a field data at point |

<a id="button-fem_postfilterglyph"></a>
### Glyph Filter — `FEM_PostFilterGlyph`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Glyph Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterGlyph.svg) | Glyph Filter | Adds a post-processing filter that adds glyphs to the mesh vertices for vertex data visualization |

<a id="button-fem_postfilterlinearizedstresses"></a>
### Stress Linearization Plot — `FEM_PostFilterLinearizedStresses`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Stress Linearization Plot](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterLinearizedStresses.svg) | Stress Linearization Plot | Defines a stress linearization plot |

<a id="button-fem_postfilterwarp"></a>
### Warp Filter — `FEM_PostFilterWarp`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Warp Filter](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostFilterWarp.svg) | Warp Filter | Warps the geometry along a vector field by a certain factor |

<a id="button-fem_postpipelinefromresult"></a>
### Post Pipeline From Result — `FEM_PostPipelineFromResult`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Post Pipeline From Result](../../../src/Mod/Fem/Gui/Resources/icons/FEM_PostPipelineFromResult.svg) | Post Pipeline From Result | Creates a post processing pipeline from a result object |

<a id="button-fem_postvisualization"></a>
### Data Visualizations — `FEM_PostVisualization`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| — | Data Visualizations | Different visualizations to show post processing data in |

<a id="button-fem_resultshow"></a>
### Show Result — `FEM_ResultShow`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Show Result](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ResultShow.svg) | Show Result | Shows and visualizes the selected result data |

<a id="button-fem_resultspurge"></a>
### Purge Results — `FEM_ResultsPurge`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Purge Results](../../../src/Mod/Fem/Gui/Resources/icons/FEM_ResultsPurge.svg) | Purge Results | Purges all results from the active analysis |

<a id="button-fem_solvercalculix"></a>
### Solver CalculiX — `FEM_SolverCalculiX`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Solver CalculiX](../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverStandard.svg) | Solver CalculiX | Creates a FEM solver CalculiX |

<a id="button-fem_solvercontrol"></a>
### Solver Job Control — `FEM_SolverControl`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Solver Job Control](../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverControl.svg) | Solver Job Control | Changes solver attributes and runs the calculations for the selected solver |

<a id="button-fem_solverelmer"></a>
### Solver Elmer — `FEM_SolverElmer`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Solver Elmer](../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverElmer.svg) | Solver Elmer | Creates a FEM solver Elmer |

<a id="button-fem_solvermystran"></a>
### Solver Mystran — `FEM_SolverMystran`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Solver Mystran](../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverMystran.svg) | Solver Mystran | Creates a FEM solver Mystran |

<a id="button-fem_solverrun"></a>
### Run Solver — `FEM_SolverRun`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Run Solver](../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverRun.svg) | Run Solver | Runs the calculations for the selected solver |

<a id="button-fem_solverz88"></a>
### Solver Z88 — `FEM_SolverZ88`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Solver Z88](../../../src/Mod/Fem/Gui/Resources/icons/FEM_SolverZ88.svg) | Solver Z88 | Creates a FEM solver Z88 |

<a id="button-inspection_inspectelement"></a>
### Inspection… — `Inspection_InspectElement`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Inspection…](../../../src/Mod/Inspection/Gui/Resources/icons/inspect_pipette.svg) | Inspection… | Inspects distance information |

<a id="button-inspection_visualinspection"></a>
### Visual Inspection — `Inspection_VisualInspection`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Visual Inspection](../../../src/Mod/Inspection/Gui/Resources/icons/InspectionWorkbench.svg) | Visual Inspection | Inspects the objects visually |

<a id="button-material_edit"></a>
### Edit — `Material_Edit`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Edit](toolbar-icons/Material_Edit.png) | Edit | Edits material properties |

<a id="button-meshpart_mesher"></a>
### Mesh From Shape — `MeshPart_Mesher`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Mesh From Shape](../../../src/Gui/Icons/preferences-general.svg) | Mesh From Shape | Tessellate shape |

<a id="button-mesh_addfacet"></a>
### Add Triangle — `Mesh_AddFacet`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Add Triangle](toolbar-icons/Mesh_AddFacet.png) | Add Triangle | Adds a triangle manually to a mesh |

<a id="button-mesh_boundingbox"></a>
### Bounding Box Info — `Mesh_BoundingBox`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Bounding Box Info](toolbar-icons/Mesh_BoundingBox.png) | Bounding Box Info | Shows the bounding box coordinates of the selected mesh |

<a id="button-mesh_buildregularsolid"></a>
### Regular Solid — `Mesh_BuildRegularSolid`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Regular Solid](toolbar-icons/Mesh_BuildRegularSolid.png) | Regular Solid | Builds a regular solid |

<a id="button-mesh_crosssections"></a>
### Cross-Sections — `Mesh_CrossSections`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cross-Sections](toolbar-icons/Mesh_CrossSections.png) | Cross-Sections | Creates cross-sections of the mesh |

<a id="button-mesh_curvatureinfo"></a>
### Curvature Info — `Mesh_CurvatureInfo`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Curvature Info](toolbar-icons/Mesh_CurvatureInfo.png) | Curvature Info | Displays information about the curvature |

<a id="button-mesh_decimating"></a>
### Decimate — `Mesh_Decimating`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Decimate](toolbar-icons/Mesh_Decimating.png) | Decimate | Decimates a mesh |

<a id="button-mesh_difference"></a>
### Difference — `Mesh_Difference`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Difference](toolbar-icons/Mesh_Difference.png) | Difference | Creates a boolean difference of the selected meshes |

<a id="button-mesh_evaluatefacet"></a>
### Face Info — `Mesh_EvaluateFacet`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Face Info](toolbar-icons/Mesh_EvaluateFacet.png) | Face Info | Displays information about the selected faces |

<a id="button-mesh_evaluatesolid"></a>
### Evaluate Solid — `Mesh_EvaluateSolid`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Evaluate Solid](toolbar-icons/Mesh_EvaluateSolid.png) | Evaluate Solid | Checks whether the mesh is a solid |

<a id="button-mesh_evaluation"></a>
### Evaluate and Repair — `Mesh_Evaluation`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Evaluate and Repair](toolbar-icons/Mesh_Evaluation.png) | Evaluate and Repair | Opens a dialog to analyze and repair a mesh |

<a id="button-mesh_export"></a>
### Export Mesh… — `Mesh_Export`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Export Mesh…](toolbar-icons/Mesh_Export.png) | Export Mesh… | Exports a mesh to a file |

<a id="button-mesh_fillinteractivehole"></a>
### Close Hole — `Mesh_FillInteractiveHole`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Close Hole](toolbar-icons/Mesh_FillInteractiveHole.png) | Close Hole | Closes a hole interactively in the mesh |

<a id="button-mesh_fillupholes"></a>
### Fill Holes — `Mesh_FillupHoles`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Fill Holes](toolbar-icons/Mesh_FillupHoles.png) | Fill Holes | Fills holes in the mesh |

<a id="button-mesh_flipnormals"></a>
### Flip Normals — `Mesh_FlipNormals`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Flip Normals](toolbar-icons/Mesh_FlipNormals.png) | Flip Normals | Flips the normals of the selected mesh |

<a id="button-mesh_frompartshape"></a>
### Mesh From Shape — `Mesh_FromPartShape`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Mesh From Shape](toolbar-icons/Mesh_FromPartShape.png) | Mesh From Shape | Tessellates the selected shape to a mesh |

<a id="button-mesh_harmonizenormals"></a>
### Harmonize Normals — `Mesh_HarmonizeNormals`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Harmonize Normals](toolbar-icons/Mesh_HarmonizeNormals.png) | Harmonize Normals | Harmonizes the normals of the mesh |

<a id="button-mesh_import"></a>
### Import Mesh… — `Mesh_Import`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Import Mesh…](toolbar-icons/Mesh_Import.png) | Import Mesh… | Imports a mesh from a file |

<a id="button-mesh_intersection"></a>
### Intersection — `Mesh_Intersection`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Intersection](toolbar-icons/Mesh_Intersection.png) | Intersection | Creates a boolean intersection from the selected meshes |

<a id="button-mesh_merge"></a>
### Merge — `Mesh_Merge`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Merge](toolbar-icons/Mesh_Merge.png) | Merge | Merges selected meshes into one |

<a id="button-mesh_polycut"></a>
### Cut — `Mesh_PolyCut`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cut](toolbar-icons/Mesh_PolyCut.png) | Cut | Cuts the mesh with a selected polygon |

<a id="button-mesh_polytrim"></a>
### Trim — `Mesh_PolyTrim`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Trim](toolbar-icons/Mesh_PolyTrim.png) | Trim | Trims a mesh with a picked polygon |

<a id="button-mesh_remeshgmsh"></a>
### Refinement — `Mesh_RemeshGmsh`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Refinement](toolbar-icons/Mesh_RemeshGmsh.png) | Refinement | Refines an existing mesh |

<a id="button-mesh_removecomponents"></a>
### Remove Components — `Mesh_RemoveComponents`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Remove Components](toolbar-icons/Mesh_RemoveComponents.png) | Remove Components | Removes topologically independent components from the mesh |

<a id="button-mesh_scale"></a>
### Scale — `Mesh_Scale`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Scale](toolbar-icons/Mesh_Scale.png) | Scale | Scales the selected mesh objects |

<a id="button-mesh_sectionbyplane"></a>
### Section From Plane — `Mesh_SectionByPlane`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Section From Plane](toolbar-icons/Mesh_SectionByPlane.png) | Section From Plane | Sections the mesh with the selected plane |

<a id="button-mesh_segmentation"></a>
### Segmentation — `Mesh_Segmentation`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Segmentation](toolbar-icons/Mesh_Segmentation.png) | Segmentation | Creates new mesh segments from the mesh |

<a id="button-mesh_segmentationbestfit"></a>
### Segmentation From Best-Fit Surfaces — `Mesh_SegmentationBestFit`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Segmentation From Best-Fit Surfaces](toolbar-icons/Mesh_SegmentationBestFit.png) | Segmentation From Best-Fit Surfaces | Creates new mesh segments from the best-fit surfaces |

<a id="button-mesh_smoothing"></a>
### Smooth — `Mesh_Smoothing`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Smooth](toolbar-icons/Mesh_Smoothing.png) | Smooth | Smoothes the selected meshes |

<a id="button-mesh_splitcomponents"></a>
### Split by Components — `Mesh_SplitComponents`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Split by Components](toolbar-icons/Mesh_SplitComponents.png) | Split by Components | Splits the selected mesh into its components |

<a id="button-mesh_trimbyplane"></a>
### Trim With Plane — `Mesh_TrimByPlane`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Trim With Plane](toolbar-icons/Mesh_TrimByPlane.png) | Trim With Plane | Trims a mesh by removing faces on one side of a selected plane |

<a id="button-mesh_union"></a>
### Union — `Mesh_Union`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Union](toolbar-icons/Mesh_Union.png) | Union | Unifies the selected meshes |

<a id="button-mesh_vertexcurvature"></a>
### Curvature Plot — `Mesh_VertexCurvature`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Curvature Plot](toolbar-icons/Mesh_VertexCurvature.png) | Curvature Plot | Calculates the curvature of the vertices of a mesh |

<a id="button-openscad_addopenscadelement"></a>
### Add OpenSCAD Element — `OpenSCAD_AddOpenSCADElement`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Add OpenSCAD Element](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_AddOpenSCADElement.svg) | Add OpenSCAD Element | Adds an OpenSCAD element based on entered OpenSCAD code using the OpenSCAD binary |

<a id="button-openscad_explodegroup"></a>
### Explode Group — `OpenSCAD_ExplodeGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Explode Group](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Explode_Group.svg) | Explode Group | Explodes a fusion or compound and applies random colors |

<a id="button-openscad_hull"></a>
### Hull — `OpenSCAD_Hull`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Hull](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Hull.svg) | Hull | Creates a hull |

<a id="button-openscad_increasetolerancefeature"></a>
### Increase Tolerance Feature — `OpenSCAD_IncreaseToleranceFeature`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Increase Tolerance Feature](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_IncreaseToleranceFeature.svg) | Increase Tolerance Feature | Creates a feature to increase the tolerance |

<a id="button-openscad_meshboolean"></a>
### Mesh Boolean — `OpenSCAD_MeshBoolean`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Mesh Boolean](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_MeshBooleans.svg) | Mesh Boolean | Performs a boolean operation using the OpenSCAD binary |

<a id="button-openscad_minkowski"></a>
### Minkowski Sum — `OpenSCAD_Minkowski`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Minkowski Sum](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_Minkowski.svg) | Minkowski Sum | Creates a Minkowski sum |

<a id="button-openscad_refineshapefeature"></a>
### Refine Shape Feature — `OpenSCAD_RefineShapeFeature`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Refine Shape Feature](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_RefineShapeFeature.svg) | Refine Shape Feature | Creates a refined shape |

<a id="button-openscad_removesubtree"></a>
### Remove Objects and Children — `OpenSCAD_RemoveSubtree`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Remove Objects and Children](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_RemoveSubtree.svg) | Remove Objects and Children | Removes the selected objects and all children that are not referenced by other objects |

<a id="button-openscad_replaceobject"></a>
### Replace Object — `OpenSCAD_ReplaceObject`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Replace Object](../../../src/Mod/OpenSCAD/Resources/icons/OpenSCAD_ReplaceObject.svg) | Replace Object | Replaces an object in the Tree View |

<a id="button-partdesign_addreferenceobject"></a>
### Add Reference Object — `PartDesign_AddReferenceObject`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Add Reference Object](toolbar-icons/PartDesign_AddReferenceObject.png) | Add Reference Object | Reference evaluated geometry from a direct child of the active component |

<a id="button-partdesign_additivehelix"></a>
### Additive Helix — `PartDesign_AdditiveHelix`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Additive Helix](toolbar-icons/PartDesign_AdditiveHelix.png) | Additive Helix | Sweeps the selected sketch or profile along a helix and adds it to the body |

<a id="button-partdesign_additiveloft"></a>
### Additive Loft — `PartDesign_AdditiveLoft`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Additive Loft](toolbar-icons/PartDesign_AdditiveLoft.png) | Additive Loft | Lofts the selected sketch or profile through one or more sections and adds it to the body |

<a id="button-partdesign_additivepipe"></a>
### Additive Pipe — `PartDesign_AdditivePipe`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Additive Pipe](toolbar-icons/PartDesign_AdditivePipe.png) | Additive Pipe | Sweeps the selected sketch or profile along a path and adds it to the body |

<a id="button-partdesign_body"></a>
### New Body — `PartDesign_Body`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![New Body](toolbar-icons/PartDesign_Body.png) | New Body | Creates a new body and activates it |

<a id="button-partdesign_boolean"></a>
### Boolean Operation — `PartDesign_Boolean`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Boolean Operation](toolbar-icons/PartDesign_Boolean.png) | Boolean Operation | Applies boolean operations with the selected objects and the active body |

<a id="button-partdesign_chamfer"></a>
### Chamfer — `PartDesign_Chamfer`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Chamfer](toolbar-icons/PartDesign_Chamfer.png) | Chamfer | Applies a chamfer to the selected edges or faces |

<a id="button-partdesign_circularpattern"></a>
### Circular Pattern — `PartDesign_CircularPattern`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Circular Pattern](../../../src/Mod/PartDesign/Gui/Resources/icons/PartDesign_CircularPattern.svg) | Circular Pattern | Duplicates the selected features or the active body in concentric circular patterns |

<a id="button-partdesign_clone"></a>
### Clone — `PartDesign_Clone`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Clone](toolbar-icons/PartDesign_Clone.png) | Clone | Copies a solid object parametrically as the base feature of a new body |

<a id="button-partdesign_compprimitiveadditive"></a>
### Additive Box — `PartDesign_CompPrimitiveAdditive`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Additive Box](toolbar-icons/PartDesign_CompPrimitiveAdditive.png) | Additive Box | Creates an additive box by its width, height, and length |
| ![Additive Cylinder](toolbar-icons/PartDesign_CompPrimitiveAdditive_1.png) | Additive Cylinder | Creates an additive cylinder by its radius, height, and angle |
| ![Additive Sphere](toolbar-icons/PartDesign_CompPrimitiveAdditive_2.png) | Additive Sphere | Creates an additive sphere by its radius and various angles |
| ![Additive Cone](toolbar-icons/PartDesign_CompPrimitiveAdditive_3.png) | Additive Cone | Creates an additive cone |
| ![Additive Ellipsoid](toolbar-icons/PartDesign_CompPrimitiveAdditive_4.png) | Additive Ellipsoid | Creates an additive ellipsoid |
| ![Additive Torus](toolbar-icons/PartDesign_CompPrimitiveAdditive_5.png) | Additive Torus | Creates an additive torus |
| ![Additive Prism](toolbar-icons/PartDesign_CompPrimitiveAdditive_6.png) | Additive Prism | Creates an additive prism |
| ![Additive Wedge](toolbar-icons/PartDesign_CompPrimitiveAdditive_7.png) | Additive Wedge | Creates an additive wedge |

<a id="button-partdesign_compprimitivesubtractive"></a>
### Subtractive Box — `PartDesign_CompPrimitiveSubtractive`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Subtractive Box](toolbar-icons/PartDesign_CompPrimitiveSubtractive.png) | Subtractive Box | Creates a subtractive box by its width, height and length |
| ![Subtractive Cylinder](toolbar-icons/PartDesign_CompPrimitiveSubtractive_1.png) | Subtractive Cylinder | Creates a subtractive cylinder by its radius, height and angle |
| ![Subtractive Sphere](toolbar-icons/PartDesign_CompPrimitiveSubtractive_2.png) | Subtractive Sphere | Creates a subtractive sphere by its radius and various angles |
| ![Subtractive Cone](toolbar-icons/PartDesign_CompPrimitiveSubtractive_3.png) | Subtractive Cone | Creates a subtractive cone |
| ![Subtractive Ellipsoid](toolbar-icons/PartDesign_CompPrimitiveSubtractive_4.png) | Subtractive Ellipsoid | Creates a subtractive ellipsoid |
| ![Subtractive Torus](toolbar-icons/PartDesign_CompPrimitiveSubtractive_5.png) | Subtractive Torus | Creates a subtractive torus |
| ![Subtractive Prism](toolbar-icons/PartDesign_CompPrimitiveSubtractive_6.png) | Subtractive Prism | Creates a subtractive prism |
| ![Subtractive Wedge](toolbar-icons/PartDesign_CompPrimitiveSubtractive_7.png) | Subtractive Wedge | Creates a subtractive wedge |

<a id="button-partdesign_compsketches"></a>
### New Sketch — `PartDesign_CompSketches`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![New Sketch](toolbar-icons/PartDesign_CompSketches.png) | New Sketch | Creates a new sketch |
| ![Attach Sketch](toolbar-icons/PartDesign_CompSketches_1.png) | Attach Sketch | Attaches a sketch to the selected geometry element |
| ![Edit Sketch](toolbar-icons/PartDesign_CompSketches_2.png) | Edit Sketch | Opens the selected sketch for editing |

<a id="button-partdesign_defeaturing"></a>
### Defeaturing — `PartDesign_Defeaturing`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Defeaturing](toolbar-icons/PartDesign_Defeaturing.png) | Defeaturing | Removes selected faces from a solid |

<a id="button-partdesign_draft"></a>
### Draft — `PartDesign_Draft`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Draft](toolbar-icons/PartDesign_Draft.png) | Draft | Applies a draft to the selected faces |

<a id="button-partdesign_extrude"></a>
### Extrude — `PartDesign_Extrude`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Extrude](toolbar-icons/PartDesign_Extrude.png) | Extrude | Extrudes a profile with Add or Subtract selected in the task panel |

<a id="button-partdesign_fillet"></a>
### Fillet — `PartDesign_Fillet`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Fillet](toolbar-icons/PartDesign_Fillet.png) | Fillet | Applies a fillet to the selected edges or faces |

<a id="button-partdesign_groove"></a>
### Groove — `PartDesign_Groove`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Groove](toolbar-icons/PartDesign_Groove.png) | Groove | Revolves the sketch or profile around a line or axis and removes it from the body |

<a id="button-partdesign_hole"></a>
### Hole — `PartDesign_Hole`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Hole](toolbar-icons/PartDesign_Hole.png) | Hole | Creates holes in the active body at the center points of circles or arcs of the selected sketch or profile |

<a id="button-partdesign_linearpattern"></a>
### Linear Pattern — `PartDesign_LinearPattern`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Linear Pattern](toolbar-icons/PartDesign_LinearPattern.png) | Linear Pattern | Duplicates the selected features or the active body in a linear pattern |

<a id="button-partdesign_mirrored"></a>
### Mirror — `PartDesign_Mirrored`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Mirror](toolbar-icons/PartDesign_Mirrored.png) | Mirror | Mirrors the selected features or active body |

<a id="button-partdesign_multitransform"></a>
### Multi-Transform — `PartDesign_MultiTransform`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Multi-Transform](toolbar-icons/PartDesign_MultiTransform.png) | Multi-Transform | Applies multiple transformations to the selected features or active body |

<a id="button-partdesign_newsketch"></a>
### New Sketch — `PartDesign_NewSketch`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![New Sketch](toolbar-icons/PartDesign_NewSketch.png) | New Sketch | Creates a new sketch |

<a id="button-partdesign_pad"></a>
### Pad — `PartDesign_Pad`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Pad](toolbar-icons/PartDesign_Pad.png) | Pad | Extrudes a sketch or profile selected before or within the task panel and adds it to the body |

<a id="button-partdesign_pathpattern"></a>
### Path Pattern — `PartDesign_PathPattern`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Path Pattern](../../../src/Mod/PartDesign/Gui/Resources/icons/PartDesign_PathPattern.svg) | Path Pattern | Duplicates the selected features or the active body along a path |

<a id="button-partdesign_pattern"></a>
### Pattern — `PartDesign_Pattern`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Pattern](toolbar-icons/PartDesign_Pattern.png) | Pattern | Creates a linear or circular pattern; select the type and features in the task pane |

<a id="button-partdesign_pocket"></a>
### Pocket — `PartDesign_Pocket`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Pocket](toolbar-icons/PartDesign_Pocket.png) | Pocket | Extrudes the selected sketch or profile and removes it from the body |

<a id="button-partdesign_pointpattern"></a>
### Point Pattern — `PartDesign_PointPattern`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Point Pattern](../../../src/Mod/PartDesign/Gui/Resources/icons/PartDesign_PointPattern.svg) | Point Pattern | Duplicates the selected features or the active body at points from a shape |

<a id="button-partdesign_polarpattern"></a>
### Polar Pattern — `PartDesign_PolarPattern`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Polar Pattern](toolbar-icons/PartDesign_PolarPattern.png) | Polar Pattern | Duplicates the selected features or the active body in a circular pattern |

<a id="button-partdesign_revolution"></a>
### Revolve — `PartDesign_Revolution`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Revolve](toolbar-icons/PartDesign_Revolution.png) | Revolve | Revolves the selected sketch or profile around a line or axis and adds it to the body |

<a id="button-partdesign_subshapebinder"></a>
### Sub-Shape Binder — `PartDesign_SubShapeBinder`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Sub-Shape Binder](toolbar-icons/PartDesign_SubShapeBinder.png) | Sub-Shape Binder | Creates a reference to geometry from one or more objects, allowing it to be used inside or outside a body. It tracks relative placements, supports multiple geometry types (solids, faces, edges, vertices), and can work with objects in the same or external documents. |

<a id="button-partdesign_subtractivehelix"></a>
### Subtractive Helix — `PartDesign_SubtractiveHelix`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Subtractive Helix](toolbar-icons/PartDesign_SubtractiveHelix.png) | Subtractive Helix | Sweeps the selected sketch or profile along a helix and removes it from the body |

<a id="button-partdesign_subtractiveloft"></a>
### Subtractive Loft — `PartDesign_SubtractiveLoft`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Subtractive Loft](toolbar-icons/PartDesign_SubtractiveLoft.png) | Subtractive Loft | Lofts the selected sketch or profile through one or more sections and removes it from the body |

<a id="button-partdesign_subtractivepipe"></a>
### Subtractive Pipe — `PartDesign_SubtractivePipe`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Subtractive Pipe](toolbar-icons/PartDesign_SubtractivePipe.png) | Subtractive Pipe | Sweeps the selected sketch or profile along a path and removes it from the body |

<a id="button-partdesign_thickness"></a>
### Thickness — `PartDesign_Thickness`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Thickness](toolbar-icons/PartDesign_Thickness.png) | Thickness | Applies thickness and removes the selected faces |

<a id="button-part_boolean"></a>
### Boolean Operation — `Part_Boolean`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Boolean Operation](toolbar-icons/Part_Boolean.png) | Boolean Operation | Applies a boolean operation with the selected shapes |

<a id="button-part_booleanfragments"></a>
### Boolean Fragments — `Part_BooleanFragments`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Boolean Fragments](toolbar-icons/Part_BooleanFragments.png) | Boolean Fragments | Creates a boolean union which is sliced at the intersections of the selected shapes |

<a id="button-part_box"></a>
### Cube — `Part_Box`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cube](toolbar-icons/Part_Box.png) | Cube | Creates a solid cube |

<a id="button-part_builder"></a>
### Shape Builder — `Part_Builder`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Shape Builder](toolbar-icons/Part_Builder.png) | Shape Builder | Advanced utility to create shapes |

<a id="button-part_chamfer"></a>
### Chamfer — `Part_Chamfer`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Chamfer](toolbar-icons/Part_Chamfer.png) | Chamfer | Chamfers the selected edges of a shape |

<a id="button-part_checkgeometry"></a>
### Check Geometry — `Part_CheckGeometry`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Check Geometry](toolbar-icons/Part_CheckGeometry.png) | Check Geometry | Analyzes the selected shapes for errors |

<a id="button-part_colorperface"></a>
### Appearance per Face — `Part_ColorPerFace`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Appearance per Face](toolbar-icons/Part_ColorPerFace.png) | Appearance per Face | Sets the appearance of individual faces of the selected object |

<a id="button-part_common"></a>
### Intersection — `Part_Common`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Intersection](toolbar-icons/Part_Common.png) | Intersection | Intersects the selected shapes |

<a id="button-part_compcompoundtools"></a>
### Compound — `Part_CompCompoundTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Compound](toolbar-icons/Part_CompCompoundTools.png) | Compound | Compounds the selected shapes |
| ![Explode Compound](toolbar-icons/Part_CompCompoundTools_1.png) | Explode Compound | Splits up a compound of shapes into separate objects, creating a compound filter for each shape |
| ![Compound Filter](toolbar-icons/Part_CompCompoundTools_2.png) | Compound Filter | Filters out objects from the selected compound by characteristics like volume, area, or length, or by choosing specific items. If a second object is selected, it will be used as reference, for example, for collision or distance filtering. |

<a id="button-part_compjoinfeatures"></a>
### Connect Shapes — `Part_CompJoinFeatures`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Connect Shapes](toolbar-icons/Part_CompJoinFeatures.png) | Connect Shapes | Fuses shapes, taking care to preserve voids |
| ![Embed Shapes](toolbar-icons/Part_CompJoinFeatures_1.png) | Embed Shapes | Fuses one shape into another, taking care to preserve voids |
| ![Cutout Shape](toolbar-icons/Part_CompJoinFeatures_2.png) | Cutout Shape | Creates a cutout in the selected shape to fit another shape |

<a id="button-part_compoffset"></a>
### 3D Offset — `Part_CompOffset`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![3D Offset](toolbar-icons/Part_CompOffset.png) | 3D Offset | Offsets shapes in 3D |
| ![2D Offset](toolbar-icons/Part_CompOffset_1.png) | 2D Offset | Offsets planar shapes in 2D |

<a id="button-part_compsplitfeatures"></a>
### Boolean Fragments — `Part_CompSplitFeatures`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Boolean Fragments](toolbar-icons/Part_CompSplitFeatures.png) | Boolean Fragments | Creates a boolean union which is sliced at the intersections of the selected shapes |
| ![Slice Apart](toolbar-icons/Part_CompSplitFeatures_1.png) | Slice Apart | Slices the selected object by other objects, and splits it apart, creating a compound filter for each slide |
| ![Slice to Compound](toolbar-icons/Part_CompSplitFeatures_2.png) | Slice to Compound | Slices the selected object by using other objects as cutting tools and storing the results in one compound |
| ![Boolean XOR](toolbar-icons/Part_CompSplitFeatures_3.png) | Boolean XOR | Performs an 'exclusive OR' boolean operation with two or more selected objects, or with the shapes inside a compound. Overlapping volumes of the shapes will be removed. |

<a id="button-part_compound"></a>
### Compound — `Part_Compound`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Compound](toolbar-icons/Part_Compound.png) | Compound | Compounds the selected shapes |

<a id="button-part_compoundfilter"></a>
### Compound Filter — `Part_CompoundFilter`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Compound Filter](toolbar-icons/Part_CompoundFilter.png) | Compound Filter | Filters out objects from the selected compound by characteristics like volume, area, or length, or by choosing specific items. If a second object is selected, it will be used as reference, for example, for collision or distance filtering. |

<a id="button-part_cone"></a>
### Cone — `Part_Cone`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cone](toolbar-icons/Part_Cone.png) | Cone | Creates a solid cone |

<a id="button-part_crosssections"></a>
### Cross-Sections — `Part_CrossSections`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cross-Sections](toolbar-icons/Part_CrossSections.png) | Cross-Sections | Creates cross-sections |

<a id="button-part_cut"></a>
### Cut — `Part_Cut`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cut](toolbar-icons/Part_Cut.png) | Cut | Cuts 2 selected shapes |

<a id="button-part_cylinder"></a>
### Cylinder — `Part_Cylinder`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cylinder](toolbar-icons/Part_Cylinder.png) | Cylinder | Creates a solid cylinder |

<a id="button-part_datums"></a>
### Coordinate System — `Part_Datums`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Coordinate System](toolbar-icons/Part_Datums.png) | Coordinate System | Creates a coordinate system that can be attached to other objects |
| ![Datum Plane](toolbar-icons/Part_Datums_1.png) | Datum Plane | Creates a datum plane that can be attached to other objects |
| ![Datum Line](toolbar-icons/Part_Datums_2.png) | Datum Line | Creates a datum line that can be attached to other objects |
| ![Datum Point](toolbar-icons/Part_Datums_3.png) | Datum Point | Creates a datum point that can be attached to other objects |

<a id="button-part_defeaturing"></a>
### Defeaturing — `Part_Defeaturing`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Defeaturing](toolbar-icons/Part_Defeaturing.png) | Defeaturing | Removes the selected features from a shape |

<a id="button-part_explodecompound"></a>
### Explode Compound — `Part_ExplodeCompound`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Explode Compound](toolbar-icons/Part_ExplodeCompound.png) | Explode Compound | Splits up a compound of shapes into separate objects, creating a compound filter for each shape |

<a id="button-part_extrude"></a>
### Extrude — `Part_Extrude`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Extrude](toolbar-icons/Part_Extrude.png) | Extrude | Extrudes the selected sketch or profile |

<a id="button-part_fillet"></a>
### Fillet — `Part_Fillet`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Fillet](toolbar-icons/Part_Fillet.png) | Fillet | Fillets the selected edges of a shape |

<a id="button-part_fuse"></a>
### Union — `Part_Fuse`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Union](toolbar-icons/Part_Fuse.png) | Union | Unites the selected shapes |

<a id="button-part_isoclinecurve"></a>
### Isocline Curve — `Part_IsoclineCurve`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Isocline Curve](toolbar-icons/Part_IsoclineCurve.png) | Isocline Curve | Create associative draft-angle curves on selected faces |

<a id="button-part_joinconnect"></a>
### Connect Shapes — `Part_JoinConnect`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Connect Shapes](toolbar-icons/Part_JoinConnect.png) | Connect Shapes | Fuses shapes, taking care to preserve voids |

<a id="button-part_joincutout"></a>
### Cutout Shape — `Part_JoinCutout`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cutout Shape](toolbar-icons/Part_JoinCutout.png) | Cutout Shape | Creates a cutout in the selected shape to fit another shape |

<a id="button-part_joinembed"></a>
### Embed Shapes — `Part_JoinEmbed`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Embed Shapes](toolbar-icons/Part_JoinEmbed.png) | Embed Shapes | Fuses one shape into another, taking care to preserve voids |

<a id="button-part_linkarrays"></a>
### Circular Link Array — `Part_LinkArrays`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Circular Link Array](toolbar-icons/Part_LinkArrays.png) | Circular Link Array | Creates a concentric circular array of linked objects |
| ![Linear Link Array](toolbar-icons/Part_LinkArrays_1.png) | Linear Link Array | Creates a linear array of linked objects |
| ![Path Link Array](toolbar-icons/Part_LinkArrays_2.png) | Path Link Array | Creates an array of linked objects along a path |
| ![Point Link Array](toolbar-icons/Part_LinkArrays_3.png) | Point Link Array | Creates an array of linked objects at each point of a sketch or shape |
| ![Polar Link Array](toolbar-icons/Part_LinkArrays_4.png) | Polar Link Array | Creates a polar array of linked objects |

<a id="button-part_loft"></a>
### Loft — `Part_Loft`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Loft](toolbar-icons/Part_Loft.png) | Loft | Lofts the selected profiles |

<a id="button-part_makeface"></a>
### Face From Wires — `Part_MakeFace`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Face From Wires](toolbar-icons/Part_MakeFace.png) | Face From Wires | Creates a face from the selected wires (e.g. from a sketch) |

<a id="button-part_mirror"></a>
### Mirror — `Part_Mirror`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Mirror](toolbar-icons/Part_Mirror.png) | Mirror | Mirrors the selected shape |

<a id="button-part_offset"></a>
### 3D Offset — `Part_Offset`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![3D Offset](toolbar-icons/Part_Offset.png) | 3D Offset | Offsets shapes in 3D |

<a id="button-part_offset2d"></a>
### 2D Offset — `Part_Offset2D`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![2D Offset](toolbar-icons/Part_Offset2D.png) | 2D Offset | Offsets planar shapes in 2D |

<a id="button-part_primitives"></a>
### Primitive — `Part_Primitives`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Primitive](toolbar-icons/Part_Primitives.png) | Primitive | Creates solid geometric primitives parametrically |

<a id="button-part_projectiononsurface"></a>
### Project on Surface — `Part_ProjectionOnSurface`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Project on Surface](toolbar-icons/Part_ProjectionOnSurface.png) | Project on Surface | Projects edges, wires, or faces of one shape onto a face of another shape. The camera view determines the direction of the projection. |

<a id="button-part_revolve"></a>
### Revolve — `Part_Revolve`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Revolve](toolbar-icons/Part_Revolve.png) | Revolve | Revolves the selected shape |

<a id="button-part_ruledsurface"></a>
### Ruled Surface — `Part_RuledSurface`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Ruled Surface](toolbar-icons/Part_RuledSurface.png) | Ruled Surface | Creates a ruled surface between 2 selected wires |

<a id="button-part_scale"></a>
### Scale — `Part_Scale`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Scale](toolbar-icons/Part_Scale.png) | Scale | Scales the selected shape |

<a id="button-part_section"></a>
### Section — `Part_Section`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Section](toolbar-icons/Part_Section.png) | Section | Sections 2 selected shapes |

<a id="button-part_selectfilter"></a>
### Vertex Selection — `Part_SelectFilter`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Vertex Selection](toolbar-icons/Part_SelectFilter.png) | Vertex Selection | Only allows the selection of vertices |
| ![Edge Selection](toolbar-icons/Part_SelectFilter_1.png) | Edge Selection | Only allows the selection of edges |
| ![Face Selection](toolbar-icons/Part_SelectFilter_2.png) | Face Selection | Only allows the selection of faces |
| ![No Selection Filters](toolbar-icons/Part_SelectFilter_3.png) | No Selection Filters | Clears all selection filters |

<a id="button-part_slice"></a>
### Slice to Compound — `Part_Slice`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Slice to Compound](toolbar-icons/Part_Slice.png) | Slice to Compound | Slices the selected object by using other objects as cutting tools and storing the results in one compound |

<a id="button-part_sliceapart"></a>
### Slice Apart — `Part_SliceApart`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Slice Apart](toolbar-icons/Part_SliceApart.png) | Slice Apart | Slices the selected object by other objects, and splits it apart, creating a compound filter for each slide |

<a id="button-part_sphere"></a>
### Sphere — `Part_Sphere`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Sphere](toolbar-icons/Part_Sphere.png) | Sphere | Creates a solid sphere |

<a id="button-part_sweep"></a>
### Sweep — `Part_Sweep`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Sweep](toolbar-icons/Part_Sweep.png) | Sweep | Sweeps profiles along a wire |

<a id="button-part_thickness"></a>
### Thickness — `Part_Thickness`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Thickness](toolbar-icons/Part_Thickness.png) | Thickness | Removes the selected faces and offsets the remaining shape outward to add thickness |

<a id="button-part_torus"></a>
### Torus — `Part_Torus`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Torus](toolbar-icons/Part_Torus.png) | Torus | Creates a solid torus |

<a id="button-part_trimbody"></a>
### Trim Body — `Part_TrimBody`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Trim Body](toolbar-icons/Part_TrimBody.png) | Trim Body | Trim a solid or sheet with a plane, face, or sheet and choose the side to keep |

<a id="button-part_tube"></a>
### Tube — `Part_Tube`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Tube](toolbar-icons/Part_Tube.png) | Tube | Creates a tube |

<a id="button-part_xor"></a>
### Boolean XOR — `Part_XOR`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Boolean XOR](toolbar-icons/Part_XOR.png) | Boolean XOR | Performs an 'exclusive OR' boolean operation with two or more selected objects, or with the shapes inside a compound. Overlapping volumes of the shapes will be removed. |

<a id="button-points_convert"></a>
### Convert to Points — `Points_Convert`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Convert to Points](../../../src/Mod/Points/Gui/Resources/icons/Points_Convert.svg) | Convert to Points | Converts to points |

<a id="button-points_export"></a>
### Export Points… — `Points_Export`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Export Points…](../../../src/Mod/Points/Gui/Resources/icons/Points_Export_Point_cloud.svg) | Export Points… | Exports a point cloud |

<a id="button-points_import"></a>
### Import Points… — `Points_Import`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Import Points…](../../../src/Mod/Points/Gui/Resources/icons/Points_Import_Point_cloud.svg) | Import Points… | Imports a point cloud |

<a id="button-points_merge"></a>
### Merge Point Clouds — `Points_Merge`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Merge Point Clouds](../../../src/Mod/Points/Gui/Resources/icons/Points_Merge.svg) | Merge Point Clouds | Merges several point clouds into one |

<a id="button-points_polycut"></a>
### Cut Point Cloud — `Points_PolyCut`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cut Point Cloud](../../../src/Gui/Icons/PolygonPick.svg) | Cut Point Cloud | Cuts a point cloud with a selected polygon |

<a id="button-points_structure"></a>
### Structured Point Cloud — `Points_Structure`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Structured Point Cloud](../../../src/Mod/Points/Gui/Resources/icons/Points_Structure.svg) | Structured Point Cloud | Converts points to a structured point cloud |

<a id="button-reen_approxsurface"></a>
### Approximate B-Spline Surface… — `Reen_ApproxSurface`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Approximate B-Spline Surface…](../../../src/Mod/ReverseEngineering/Gui/Resources/icons/actions/FitSurface.svg) | Approximate B-Spline Surface… | Approximates a B-spline surface |

<a id="button-robot_create"></a>
### Place Robot — `Robot_Create`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Place Robot](../../../src/Mod/Robot/Gui/Resources/icons/Robot_CreateRobot.svg) | Place Robot | Places a robot in the scene |

<a id="button-robot_createtrajectory"></a>
### Trajectory — `Robot_CreateTrajectory`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_CreateTrajectory.svg) | Trajectory | Creates a new empty trajectory |

<a id="button-robot_edge2trac"></a>
### Edge to Trajectory — `Robot_Edge2Trac`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Edge to Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_Edge2Trac.svg) | Edge to Trajectory | Generates a trajectory from the selected edges |

<a id="button-robot_insertwaypoint"></a>
### Insert in Trajectory — `Robot_InsertWaypoint`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Insert in Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_InsertWaypoint.svg) | Insert in Trajectory | Inserts the robot tool location into the trajectory |

<a id="button-robot_insertwaypointpreselect"></a>
### Insert in Trajectory — `Robot_InsertWaypointPreselect`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Insert in Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_InsertWaypointPre.svg) | Insert in Trajectory | Inserts the preselection position into the trajectory (W) |

<a id="button-robot_restorehomepos"></a>
### Move to Home — `Robot_RestoreHomePos`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Move to Home](../../../src/Mod/Robot/Gui/Resources/icons/Robot_RestoreHomePos.svg) | Move to Home | Moves to the home position |

<a id="button-robot_sethomepos"></a>
### Set Home Position — `Robot_SetHomePos`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Set Home Position](../../../src/Mod/Robot/Gui/Resources/icons/Robot_SetHomePos.svg) | Set Home Position | Sets the home position |

<a id="button-robot_simulate"></a>
### Simulate Trajectory — `Robot_Simulate`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Simulate Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_Simulate.svg) | Simulate Trajectory | Simulates robot movement along a selected trajectory |

<a id="button-robot_trajectorycompound"></a>
### Trajectory Compound — `Robot_TrajectoryCompound`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Trajectory Compound](../../../src/Mod/Robot/Gui/Resources/icons/Robot_TrajectoryCompound.svg) | Trajectory Compound | Groups and connects multiple trajectories into one |

<a id="button-robot_trajectorydressup"></a>
### Dress-Up Trajectory — `Robot_TrajectoryDressUp`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Dress-Up Trajectory](../../../src/Mod/Robot/Gui/Resources/icons/Robot_TrajectoryDressUp.svg) | Dress-Up Trajectory | Creates a dress-up object that overrides aspects of a trajectory |

<a id="button-sketcher_arcoverlay"></a>
### Toggle Circular Helper for Arcs — `Sketcher_ArcOverlay`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Toggle Circular Helper for Arcs](toolbar-icons/Sketcher_ArcOverlay.png) | Toggle Circular Helper for Arcs | Toggles the visibility of the circular helpers for all arcs |

<a id="button-sketcher_bsplineconverttonurbs"></a>
### Geometry to B-Spline — `Sketcher_BSplineConvertToNURBS`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Geometry to B-Spline](toolbar-icons/Sketcher_BSplineConvertToNURBS.png) | Geometry to B-Spline | Converts the selected geometry to B-splines |

<a id="button-sketcher_bsplinedecreasedegree"></a>
### Decrease B-Spline Degree — `Sketcher_BSplineDecreaseDegree`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Decrease B-Spline Degree](toolbar-icons/Sketcher_BSplineDecreaseDegree.png) | Decrease B-Spline Degree | Decreases the degree of the B-spline |

<a id="button-sketcher_bsplineincreasedegree"></a>
### Increase B-Spline Degree — `Sketcher_BSplineIncreaseDegree`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Increase B-Spline Degree](toolbar-icons/Sketcher_BSplineIncreaseDegree.png) | Increase B-Spline Degree | Increases the degree of the B-spline |

<a id="button-sketcher_bsplineinsertknot"></a>
### Insert Knot — `Sketcher_BSplineInsertKnot`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Insert Knot](toolbar-icons/Sketcher_BSplineInsertKnot.png) | Insert Knot | Inserts a knot at a given parameter. If a knot already exists at that parameter, its multiplicity is increased by 1. |

<a id="button-sketcher_carboncopy"></a>
### Carbon Copy — `Sketcher_CarbonCopy`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Carbon Copy](toolbar-icons/Sketcher_CarbonCopy.png) | Carbon Copy | Copies the geometry of another sketch |

<a id="button-sketcher_compbsplineshowhidegeometryinformation"></a>
### Toggle B-Spline Degree — `Sketcher_CompBSplineShowHideGeometryInformation`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Toggle B-Spline Degree](toolbar-icons/Sketcher_CompBSplineShowHideGeometryInformation.png) | Toggle B-Spline Degree | Toggles the visibility of the degree for all B-splines |
| ![Toggle B-Spline Control Polygon](toolbar-icons/Sketcher_CompBSplineShowHideGeometryInformation_1.png) | Toggle B-Spline Control Polygon | Toggles the visibility of the control polygons for all B-splines |
| ![Toggle B-Spline Curvature Comb](toolbar-icons/Sketcher_CompBSplineShowHideGeometryInformation_2.png) | Toggle B-Spline Curvature Comb | Toggles the visibility of the curvature comb for all B-splines |
| ![Toggle B-Spline Knot Multiplicity](toolbar-icons/Sketcher_CompBSplineShowHideGeometryInformation_3.png) | Toggle B-Spline Knot Multiplicity | Toggles the visibility of the knot multiplicity for all B-splines |
| ![Toggle B-Spline Control Point Weight](toolbar-icons/Sketcher_CompBSplineShowHideGeometryInformation_4.png) | Toggle B-Spline Control Point Weight | Toggles the visibility of the control point weight for all B-splines |

<a id="button-sketcher_compcreatearc"></a>
### Arc From Center — `Sketcher_CompCreateArc`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Arc From Center](toolbar-icons/Sketcher_CompCreateArc.png) | Arc From Center | Creates an arc defined by a center point and an end point |
| ![Arc From 3 Points](toolbar-icons/Sketcher_CompCreateArc_1.png) | Arc From 3 Points | Creates an arc defined by 2 end points and 1 point on the arc |
| ![Elliptical Arc](toolbar-icons/Sketcher_CompCreateArc_2.png) | Elliptical Arc | Creates an elliptical arc |
| ![Hyperbolic Arc](toolbar-icons/Sketcher_CompCreateArc_3.png) | Hyperbolic Arc | Creates a hyperbolic arc |
| ![Parabolic Arc](toolbar-icons/Sketcher_CompCreateArc_4.png) | Parabolic Arc | Creates a parabolic arc |

<a id="button-sketcher_compcreatebspline"></a>
### B-Spline — `Sketcher_CompCreateBSpline`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![B-Spline](toolbar-icons/Sketcher_CompCreateBSpline.png) | B-Spline | Creates a B-spline curve defined by control points |
| ![Periodic B-Spline](toolbar-icons/Sketcher_CompCreateBSpline_1.png) | Periodic B-Spline | Creates a periodic B-spline curve defined by control points |
| ![B-Spline From Knots](toolbar-icons/Sketcher_CompCreateBSpline_2.png) | B-Spline From Knots | Creates a B-spline from knots, i.e. from interpolation |
| ![Periodic B-Spline From Knots](toolbar-icons/Sketcher_CompCreateBSpline_3.png) | Periodic B-Spline From Knots | Creates a periodic B-spline defined by knots using interpolation |

<a id="button-sketcher_compcreateconic"></a>
### Circle From Center — `Sketcher_CompCreateConic`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Circle From Center](toolbar-icons/Sketcher_CompCreateConic.png) | Circle From Center | Creates a circle from a center and rim point |
| ![Circle From 3 Points](toolbar-icons/Sketcher_CompCreateConic_1.png) | Circle From 3 Points | Creates a circle from 3 perimeter points |
| ![Ellipse From Center](toolbar-icons/Sketcher_CompCreateConic_2.png) | Ellipse From Center | Creates an ellipse from a center and rim point |
| ![Ellipse From 3 Points](toolbar-icons/Sketcher_CompCreateConic_3.png) | Ellipse From 3 Points | Creates an ellipse from 3 points on its perimeter |

<a id="button-sketcher_compcreatefillets"></a>
### Fillet — `Sketcher_CompCreateFillets`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Fillet](toolbar-icons/Sketcher_CompCreateFillets.png) | Fillet | Creates a fillet between 2 selected curves or at coincident points |
| ![Chamfer](toolbar-icons/Sketcher_CompCreateFillets_1.png) | Chamfer | Creates a chamfer between 2 selected curves or at coincident points |

<a id="button-sketcher_compcreaterectangles"></a>
### Rectangle — `Sketcher_CompCreateRectangles`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Rectangle](toolbar-icons/Sketcher_CompCreateRectangles.png) | Rectangle | Creates a rectangle from 2 corner points |
| ![Centered Rectangle](toolbar-icons/Sketcher_CompCreateRectangles_1.png) | Centered Rectangle | Creates a centered rectangle from a center and a corner point |
| ![Rounded Rectangle](toolbar-icons/Sketcher_CompCreateRectangles_2.png) | Rounded Rectangle | Creates a rounded rectangle from 2 corner points |

<a id="button-sketcher_compcreateregularpolygon"></a>
### Triangle — `Sketcher_CompCreateRegularPolygon`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Triangle](toolbar-icons/Sketcher_CompCreateRegularPolygon.png) | Triangle | Creates an equilateral triangle from a center and corner point |
| ![Square](toolbar-icons/Sketcher_CompCreateRegularPolygon_1.png) | Square | Creates a square from a center and corner point |
| ![Pentagon](toolbar-icons/Sketcher_CompCreateRegularPolygon_2.png) | Pentagon | Creates a pentagon from a center and corner point |
| ![Hexagon](toolbar-icons/Sketcher_CompCreateRegularPolygon_3.png) | Hexagon | Creates a hexagon from a center and corner point |
| ![Heptagon](toolbar-icons/Sketcher_CompCreateRegularPolygon_4.png) | Heptagon | Creates a heptagon from a center and corner point |
| ![Octagon](toolbar-icons/Sketcher_CompCreateRegularPolygon_5.png) | Octagon | Creates an octagon from a center and corner point |
| ![Polygon](toolbar-icons/Sketcher_CompCreateRegularPolygon_6.png) | Polygon | Creates a regular polygon from a center and corner point |

<a id="button-sketcher_compcurveedition"></a>
### Trim Edge — `Sketcher_CompCurveEdition`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Trim Edge](toolbar-icons/Sketcher_CompCurveEdition.png) | Trim Edge | Trims an edge with respect to the selected position |
| ![Split Edge](toolbar-icons/Sketcher_CompCurveEdition_1.png) | Split Edge | Splits an edge into 2 segments while preserving constraints |
| ![Extend Edge](toolbar-icons/Sketcher_CompCurveEdition_2.png) | Extend Edge | Extends an edge with respect to the selected position |

<a id="button-sketcher_compdimensiontools"></a>
### Dimension — `Sketcher_CompDimensionTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Dimension](toolbar-icons/Sketcher_CompDimensionTools.png) | Dimension | Constrains contextually based on the selection. The type can be changed with the M key. |
| ![Horizontal Dimension](toolbar-icons/Sketcher_CompDimensionTools_2.png) | Horizontal Dimension | Constrains the horizontal distance between two points, or from a point to the origin if only one is selected |
| ![Vertical Dimension](toolbar-icons/Sketcher_CompDimensionTools_3.png) | Vertical Dimension | Constrains the vertical distance between two points, or from a point to the origin if only one is selected |
| ![Distance Dimension](toolbar-icons/Sketcher_CompDimensionTools_4.png) | Distance Dimension | Constrains the vertical distance between two points, or from a point to the origin if one is selected |
| ![Radius/Diameter Dimension](toolbar-icons/Sketcher_CompDimensionTools_5.png) | Radius/Diameter Dimension | Constrains the radius of the selected arc or the diameter of the selected circle |
| ![Radius Dimension](toolbar-icons/Sketcher_CompDimensionTools_6.png) | Radius Dimension | Constrains the radius of the selected circle or arc |
| ![Diameter Dimension](toolbar-icons/Sketcher_CompDimensionTools_7.png) | Diameter Dimension | Constrains the diameter of the selected circle or arc |
| ![Angle Dimension](toolbar-icons/Sketcher_CompDimensionTools_8.png) | Angle Dimension | Constrains the angle between two straight lines or between one line and the X-axis of the sketch if only one is selected |
| ![Lock Position](toolbar-icons/Sketcher_CompDimensionTools_9.png) | Lock Position | Constrains the selected vertices by adding horizontal and vertical distance constraints |

<a id="button-sketcher_compexternal"></a>
### External Projection — `Sketcher_CompExternal`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![External Projection](toolbar-icons/Sketcher_CompExternal.png) | External Projection | Creates the projection of external geometry in the sketch plane |
| ![External Intersection](toolbar-icons/Sketcher_CompExternal_1.png) | External Intersection | Creates the intersection of external geometry with the sketch plane |

<a id="button-sketcher_comphorver"></a>
### Horizontal Constraint — `Sketcher_CompHorVer`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Horizontal Constraint](toolbar-icons/Sketcher_CompHorVer.png) | Horizontal Constraint | Constrains the selected elements horizontally |
| ![Vertical Constraint](toolbar-icons/Sketcher_CompHorVer_1.png) | Vertical Constraint | Constrains the selected elements vertically |

<a id="button-sketcher_compline"></a>
### Polyline — `Sketcher_CompLine`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Polyline](toolbar-icons/Sketcher_CompLine.png) | Polyline | Creates a polyline in the sketch. M key cycles through segment modes. |
| ![Line](toolbar-icons/Sketcher_CompLine_1.png) | Line | Creates a line |

<a id="button-sketcher_compmodifyknotmultiplicity"></a>
### Increase knot multiplicity — `Sketcher_CompModifyKnotMultiplicity`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Increase knot multiplicity](toolbar-icons/Sketcher_CompModifyKnotMultiplicity.png) | Increase knot multiplicity | Increases the multiplicity of the selected knot of a B-spline |
| ![Decrease knot multiplicity](toolbar-icons/Sketcher_CompModifyKnotMultiplicity_1.png) | Decrease knot multiplicity | Decreases the multiplicity of the selected knot of a B-spline |

<a id="button-sketcher_compslot"></a>
### Slot — `Sketcher_CompSlot`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Slot](toolbar-icons/Sketcher_CompSlot.png) | Slot | Creates a slot |
| ![Arc Slot](toolbar-icons/Sketcher_CompSlot_1.png) | Arc Slot | Creates an arc slot |

<a id="button-sketcher_comptoggleconstraints"></a>
### Toggle Driving/Reference Constraints — `Sketcher_CompToggleConstraints`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Toggle Driving/Reference Constraints](toolbar-icons/Sketcher_CompToggleConstraints.png) | Toggle Driving/Reference Constraints | Toggles between driving and reference mode of the selected constraints and commands |
| ![Toggle Constraints](toolbar-icons/Sketcher_CompToggleConstraints_1.png) | Toggle Constraints | Toggles the state of the selected constraints |

<a id="button-sketcher_constrainangle"></a>
### Angle Dimension — `Sketcher_ConstrainAngle`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Angle Dimension](toolbar-icons/Sketcher_ConstrainAngle.png) | Angle Dimension | Constrains the angle between two straight lines or between one line and the X-axis of the sketch if only one is selected |

<a id="button-sketcher_constrainblock"></a>
### Block Constraint — `Sketcher_ConstrainBlock`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Block Constraint](toolbar-icons/Sketcher_ConstrainBlock.png) | Block Constraint | Constrains the selected edges as fixed |

<a id="button-sketcher_constraincoincidentunified"></a>
### Coincident Constraint — `Sketcher_ConstrainCoincidentUnified`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Coincident Constraint](toolbar-icons/Sketcher_ConstrainCoincidentUnified.png) | Coincident Constraint | Constrains the selected elements to be coincident |

<a id="button-sketcher_constraindiameter"></a>
### Diameter Dimension — `Sketcher_ConstrainDiameter`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Diameter Dimension](toolbar-icons/Sketcher_ConstrainDiameter.png) | Diameter Dimension | Constrains the diameter of the selected circle or arc |

<a id="button-sketcher_constraindistance"></a>
### Distance Dimension — `Sketcher_ConstrainDistance`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Distance Dimension](toolbar-icons/Sketcher_ConstrainDistance.png) | Distance Dimension | Constrains the vertical distance between two points, or from a point to the origin if one is selected |

<a id="button-sketcher_constraindistancex"></a>
### Horizontal Dimension — `Sketcher_ConstrainDistanceX`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Horizontal Dimension](toolbar-icons/Sketcher_ConstrainDistanceX.png) | Horizontal Dimension | Constrains the horizontal distance between two points, or from a point to the origin if only one is selected |

<a id="button-sketcher_constraindistancey"></a>
### Vertical Dimension — `Sketcher_ConstrainDistanceY`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Vertical Dimension](toolbar-icons/Sketcher_ConstrainDistanceY.png) | Vertical Dimension | Constrains the vertical distance between two points, or from a point to the origin if only one is selected |

<a id="button-sketcher_constrainequal"></a>
### Equal Constraint — `Sketcher_ConstrainEqual`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Equal Constraint](toolbar-icons/Sketcher_ConstrainEqual.png) | Equal Constraint | Constrains the selected edges or circles to be equal |

<a id="button-sketcher_constraingroup"></a>
### Group Constraint (Development preview) — `Sketcher_ConstrainGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Group Constraint (Development preview)](toolbar-icons/Sketcher_ConstrainGroup.png) | Group Constraint (Development preview) | Constrains the selected geometries together as a single entity.The position and size of the grouped geometries can be defined by constraining the construction line that is generated.Constraints applied to grouped edges are ignored as long as the Group constraint is here. |

<a id="button-sketcher_constrainlock"></a>
### Lock Position — `Sketcher_ConstrainLock`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Lock Position](toolbar-icons/Sketcher_ConstrainLock.png) | Lock Position | Constrains the selected vertices by adding horizontal and vertical distance constraints |

<a id="button-sketcher_constrainparallel"></a>
### Parallel Constraint — `Sketcher_ConstrainParallel`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Parallel Constraint](toolbar-icons/Sketcher_ConstrainParallel.png) | Parallel Constraint | Constrains the selected lines to be parallel |

<a id="button-sketcher_constrainperpendicular"></a>
### Perpendicular Constraint — `Sketcher_ConstrainPerpendicular`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Perpendicular Constraint](toolbar-icons/Sketcher_ConstrainPerpendicular.png) | Perpendicular Constraint | Constrains the selected lines to be perpendicular |

<a id="button-sketcher_constrainradiam"></a>
### Radius/Diameter Dimension — `Sketcher_ConstrainRadiam`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Radius/Diameter Dimension](toolbar-icons/Sketcher_ConstrainRadiam.png) | Radius/Diameter Dimension | Constrains the radius of the selected arc or the diameter of the selected circle |

<a id="button-sketcher_constrainradius"></a>
### Radius Dimension — `Sketcher_ConstrainRadius`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Radius Dimension](toolbar-icons/Sketcher_ConstrainRadius.png) | Radius Dimension | Constrains the radius of the selected circle or arc |

<a id="button-sketcher_constrainsnellslaw"></a>
### Refraction Constraint — `Sketcher_ConstrainSnellsLaw`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Refraction Constraint](toolbar-icons/Sketcher_ConstrainSnellsLaw.png) | Refraction Constraint | Constrains the selected elements based on the refraction law (Snell's Law) |

<a id="button-sketcher_constrainsymmetric"></a>
### Symmetric Constraint — `Sketcher_ConstrainSymmetric`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Symmetric Constraint](toolbar-icons/Sketcher_ConstrainSymmetric.png) | Symmetric Constraint | Constrains the selected elements to be symmetric |

<a id="button-sketcher_constraintangent"></a>
### Tangent/Collinear Constraint — `Sketcher_ConstrainTangent`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Tangent/Collinear Constraint](toolbar-icons/Sketcher_ConstrainTangent.png) | Tangent/Collinear Constraint | Constrains the selected elements to be tangent or collinear |

<a id="button-sketcher_createpoint"></a>
### Point — `Sketcher_CreatePoint`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Point](toolbar-icons/Sketcher_CreatePoint.png) | Point | Creates a point |

<a id="button-sketcher_createtext"></a>
### Text (Experimental) — `Sketcher_CreateText`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Text (Experimental)](toolbar-icons/Sketcher_CreateText.png) | Text (Experimental) | Creates text geometries controlled by a Text constraint. To Edit: Double-click the Text constraint to change the text content and font. To Position/Size: Apply constraints to the group's construction line. Note: While the Text constraint is active, any constraints applied directly to the text geometries will be ignored. |

<a id="button-sketcher_dimension"></a>
### Auto Dimension — `Sketcher_Dimension`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Dimension](toolbar-icons/Sketcher_Dimension.png) | Dimension | Constrains contextually based on the selection. The type can be changed with the M key. |

<a id="button-sketcher_editsketch"></a>
### Edit Sketch — `Sketcher_EditSketch`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Edit Sketch](toolbar-icons/Sketcher_EditSketch.png) | Edit Sketch | Opens the selected sketch for editing |

<a id="button-sketcher_joincurves"></a>
### Join Curves — `Sketcher_JoinCurves`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Join Curves](toolbar-icons/Sketcher_JoinCurves.png) | Join Curves | Joins 2 curves at selected end points |

<a id="button-sketcher_leavesketch"></a>
### Leave Sketch — `Sketcher_LeaveSketch`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Leave Sketch](toolbar-icons/Sketcher_LeaveSketch.png) | Leave Sketch | Finishes editing the active sketch. Press Escape to exit. |

<a id="button-sketcher_mapsketch"></a>
### Attach Sketch — `Sketcher_MapSketch`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Attach Sketch](toolbar-icons/Sketcher_MapSketch.png) | Attach Sketch | Attaches a sketch to the selected geometry element |

<a id="button-sketcher_mergesketches"></a>
### Merge Sketches — `Sketcher_MergeSketches`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Merge Sketches](toolbar-icons/Sketcher_MergeSketches.png) | Merge Sketches | Creates a new sketch by merging at least 2 selected sketches |

<a id="button-sketcher_mirrorsketch"></a>
### Mirror Sketch — `Sketcher_MirrorSketch`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Mirror Sketch](toolbar-icons/Sketcher_MirrorSketch.png) | Mirror Sketch | Creates a new mirrored sketch for each selected sketch by using the X or Y axes, or the origin point, as mirroring reference |

<a id="button-sketcher_newsketch"></a>
### New Sketch — `Sketcher_NewSketch`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![New Sketch](toolbar-icons/Sketcher_NewSketch.png) | New Sketch | Creates a new sketch |

<a id="button-sketcher_offset"></a>
### Offset — `Sketcher_Offset`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Offset](toolbar-icons/Sketcher_Offset.png) | Offset | Adds an equidistant closed contour around selected geometry: positive values offset outward, negative values inward |

<a id="button-sketcher_removeaxesalignment"></a>
### Remove Axes Alignment — `Sketcher_RemoveAxesAlignment`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Remove Axes Alignment](toolbar-icons/Sketcher_RemoveAxesAlignment.png) | Remove Axes Alignment | Modifies the constraints to remove axes alignment while trying to preserve the constraint relationship of the selection |

<a id="button-sketcher_reorientsketch"></a>
### Reorient Sketch — `Sketcher_ReorientSketch`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Reorient Sketch](toolbar-icons/Sketcher_ReorientSketch.png) | Reorient Sketch | Places the selected sketch on one of the global coordinate planes. This will clear the AttachmentSupport property. |

<a id="button-sketcher_restoreinternalalignmentgeometry"></a>
### Toggle Internal Geometry — `Sketcher_RestoreInternalAlignmentGeometry`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Toggle Internal Geometry](toolbar-icons/Sketcher_RestoreInternalAlignmentGeometry.png) | Toggle Internal Geometry | Toggles the visibility of all internal geometry |

<a id="button-sketcher_rotate"></a>
### Rotate / Polar Transform — `Sketcher_Rotate`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Rotate / Polar Transform](toolbar-icons/Sketcher_Rotate.png) | Rotate / Polar Transform | Rotates the selected geometry by creating 'n' total elements, enabling circular pattern creation |

<a id="button-sketcher_scale"></a>
### Scale — `Sketcher_Scale`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Scale](toolbar-icons/Sketcher_Scale.png) | Scale | Scales the selected geometries |

<a id="button-sketcher_selectconstraints"></a>
### Select Associated Constraints — `Sketcher_SelectConstraints`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Select Associated Constraints](toolbar-icons/Sketcher_SelectConstraints.png) | Select Associated Constraints | Selects the constraints associated with the selected geometrical elements |

<a id="button-sketcher_selectelementsassociatedwithconstraints"></a>
### Select Associated Geometry — `Sketcher_SelectElementsAssociatedWithConstraints`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Select Associated Geometry](toolbar-icons/Sketcher_SelectElementsAssociatedWithConstraints.png) | Select Associated Geometry | Selects the geometrical elements associated with the selected constraints |

<a id="button-sketcher_switchvirtualspace"></a>
### Switch Virtual Space — `Sketcher_SwitchVirtualSpace`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Switch Virtual Space](toolbar-icons/Sketcher_SwitchVirtualSpace.png) | Switch Virtual Space | Switches the selected constraints or the view to the other virtual space |

<a id="button-sketcher_symmetry"></a>
### Mirror — `Sketcher_Symmetry`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Mirror](toolbar-icons/Sketcher_Symmetry.png) | Mirror | Creates a mirrored copy of the selected geometry |

<a id="button-sketcher_toggleconstruction"></a>
### Toggle Construction Geometry — `Sketcher_ToggleConstruction`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Toggle Construction Geometry](toolbar-icons/Sketcher_ToggleConstruction.png) | Toggle Construction Geometry | Toggles between defining geometry and construction geometry modes |

<a id="button-sketcher_translate"></a>
### Move / Array Transform — `Sketcher_Translate`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Move / Array Transform](toolbar-icons/Sketcher_Translate.png) | Move / Array Transform | Translates the selected geometries and enables the creation of 'i' * 'j' total elements |

<a id="button-sketcher_validatesketch"></a>
### Validate Sketch — `Sketcher_ValidateSketch`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Validate Sketch](toolbar-icons/Sketcher_ValidateSketch.png) | Validate Sketch | Validates a sketch by checking for missing coincidences, invalid constraints, and degenerate geometry |

<a id="button-sketcher_viewsection"></a>
### Toggle Section View — `Sketcher_ViewSection`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Toggle Section View](toolbar-icons/Sketcher_ViewSection.png) | Toggle Section View | Toggles between section view and full view |

<a id="button-sketcher_viewsketch"></a>
### Align View to Sketch — `Sketcher_ViewSketch`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Align View to Sketch](toolbar-icons/Sketcher_ViewSketch.png) | Align View to Sketch | Aligns the camera orientation perpendicular to the active sketch plane |

<a id="button-spreadsheet_alignbottom"></a>
### Align Bottom — `Spreadsheet_AlignBottom`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Align Bottom](toolbar-icons/Spreadsheet_AlignBottom.png) | Align Bottom | Aligns cell contents to the bottom |

<a id="button-spreadsheet_aligncenter"></a>
### Align Horizontal Center — `Spreadsheet_AlignCenter`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Align Horizontal Center](toolbar-icons/Spreadsheet_AlignCenter.png) | Align Horizontal Center | Aligns cell contents to the horizontal center |

<a id="button-spreadsheet_alignleft"></a>
### Align Left — `Spreadsheet_AlignLeft`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Align Left](toolbar-icons/Spreadsheet_AlignLeft.png) | Align Left | Aligns cell contents to the left |

<a id="button-spreadsheet_alignright"></a>
### Align Right — `Spreadsheet_AlignRight`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Align Right](toolbar-icons/Spreadsheet_AlignRight.png) | Align Right | Aligns cell contents to the right |

<a id="button-spreadsheet_aligntop"></a>
### Align Top — `Spreadsheet_AlignTop`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Align Top](toolbar-icons/Spreadsheet_AlignTop.png) | Align Top | Aligns cell contents to the top |

<a id="button-spreadsheet_alignvcenter"></a>
### Align Vertical Center — `Spreadsheet_AlignVCenter`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Align Vertical Center](toolbar-icons/Spreadsheet_AlignVCenter.png) | Align Vertical Center | Aligns cell contents to the vertical center |

<a id="button-spreadsheet_createsheet"></a>
### New Spreadsheet — `Spreadsheet_CreateSheet`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![New Spreadsheet](toolbar-icons/Spreadsheet_CreateSheet.png) | New Spreadsheet | Creates a new spreadsheet |

<a id="button-spreadsheet_export"></a>
### Export Spreadsheet — `Spreadsheet_Export`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Export Spreadsheet](toolbar-icons/Spreadsheet_Export.png) | Export Spreadsheet | Exports the spreadsheet to a CSV file |

<a id="button-spreadsheet_import"></a>
### Import Spreadsheet — `Spreadsheet_Import`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Import Spreadsheet](toolbar-icons/Spreadsheet_Import.png) | Import Spreadsheet | Imports a CSV file into a new spreadsheet |

<a id="button-spreadsheet_mergecells"></a>
### Merge Cells — `Spreadsheet_MergeCells`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Merge Cells](toolbar-icons/Spreadsheet_MergeCells.png) | Merge Cells | Merges the selected cells |

<a id="button-spreadsheet_setalias"></a>
### Set Alias — `Spreadsheet_SetAlias`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Set Alias](toolbar-icons/Spreadsheet_SetAlias.png) | Set Alias | Sets an alias for the selected cell |

<a id="button-spreadsheet_splitcell"></a>
### Split Cell — `Spreadsheet_SplitCell`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Split Cell](toolbar-icons/Spreadsheet_SplitCell.png) | Split Cell | Splits a previously merged cell |

<a id="button-spreadsheet_stylebold"></a>
### Bold Text — `Spreadsheet_StyleBold`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Bold Text](toolbar-icons/Spreadsheet_StyleBold.png) | Bold Text | Sets the text in the selected cells bold |

<a id="button-spreadsheet_styleitalic"></a>
### Italic Text — `Spreadsheet_StyleItalic`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Italic Text](toolbar-icons/Spreadsheet_StyleItalic.png) | Italic Text | Sets the text in the selected cells italic |

<a id="button-spreadsheet_styleunderline"></a>
### Underline Text — `Spreadsheet_StyleUnderline`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Underline Text](toolbar-icons/Spreadsheet_StyleUnderline.png) | Underline Text | Underlines the text in the selected cells |

<a id="button-std_aligntoselection"></a>
### Align to Selection — `Std_AlignToSelection`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Align to Selection](toolbar-icons/Std_AlignToSelection.png) | Align to Selection | Aligns the camera view to the selected elements in the 3D view |

<a id="button-std_commandsearch"></a>
### Command search... — `Std_CommandSearch`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Command search...](../../../src/Gui/Icons/zoom-in.svg) | Command search... | Find commands by name, familiar alias or shortcut |

<a id="button-std_componentstructure"></a>
### Components — `Std_ComponentStructure`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Components](toolbar-icons/Std_ComponentStructure.png) | Components | Show Models, Part Tree and History |

<a id="button-std_copy"></a>
### Copy — `Std_Copy`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Copy](toolbar-icons/Std_Copy.png) | Copy | Copies the selection to the clipboard |

<a id="button-std_cut"></a>
### Cut — `Std_Cut`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cut](toolbar-icons/Std_Cut.png) | Cut | Removes the selection and copies it to the clipboard |

<a id="button-std_delete"></a>
### Delete — `Std_Delete`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Delete](toolbar-icons/Std_Delete.png) | Delete | Deletes the selected objects |

<a id="button-std_dlgmacroexecute"></a>
### Macros — `Std_DlgMacroExecute`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Macros](toolbar-icons/Std_DlgMacroExecute.png) | Macros | Opens a dialog to execute a recorded macro |

<a id="button-std_dlgmacroexecutedirect"></a>
### Execute Macro — `Std_DlgMacroExecuteDirect`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Execute Macro](toolbar-icons/Std_DlgMacroExecuteDirect.png) | Execute Macro | Executes the macro in the editor |

<a id="button-std_dlgmacrorecord"></a>
### Record Macro — `Std_DlgMacroRecord`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Record Macro](toolbar-icons/Std_DlgMacroRecord.png) | Record Macro | Opens a dialog to record a macro |

<a id="button-std_dlgpreferences"></a>
### Preferences — `Std_DlgPreferences`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Preferences](toolbar-icons/Std_DlgPreferences.png) | Preferences | Opens a dialog to edit the preferences |

<a id="button-std_dockviewmenu"></a>
### Panels — `Std_DockViewMenu`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Panels](../../../src/Gui/Icons/Std_ToggleBottomPanels.svg) | Panels | Lists available dock panels |

<a id="button-std_drawstyle"></a>
### As Is — `Std_DrawStyle`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![As Is](toolbar-icons/Std_DrawStyle.png) | As Is | Normal mode |
| ![Points](toolbar-icons/Std_DrawStyle_1.png) | Points | Points mode |
| ![Wireframe](toolbar-icons/Std_DrawStyle_2.png) | Wireframe | Wireframe mode |
| ![Hidden Line](toolbar-icons/Std_DrawStyle_3.png) | Hidden Line | Hidden line mode |
| ![No Shading](toolbar-icons/Std_DrawStyle_4.png) | No Shading | No shading mode |
| ![Shaded](toolbar-icons/Std_DrawStyle_5.png) | Shaded | Shaded mode |
| ![Flat Lines](toolbar-icons/Std_DrawStyle_6.png) | Flat Lines | Flat lines mode |

<a id="button-std_entityselectionfilter"></a>
### Selection filters… — `Std_EntitySelectionFilter`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Selection filters…](../../../src/Gui/Icons/view-select.svg) | Selection filters… | Restrict new picks to vertices, edges, faces or whole objects |

<a id="button-std_export"></a>
### Export… — `Std_Export`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Export…](toolbar-icons/Std_Export.png) | Export… | Exports an object in the active document |

<a id="button-std_group"></a>
### New Group — `Std_Group`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![New Group](toolbar-icons/Std_Group.png) | New Group | Creates a group, which is a general-purpose container to group objects in the tree view, regardless of their data type. It is a simple folder to organize the objects in a model. |

<a id="button-std_import"></a>
### Import… — `Std_Import`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Import…](toolbar-icons/Std_Import.png) | Import… | Imports a file into the active document |

<a id="button-std_linkactions"></a>
### Make Link — `Std_LinkActions`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Make Link](toolbar-icons/Std_LinkActions.png) | Make Link | A link is an object that references another object, either within the same or in another document. Unlike clones, links reference the original shape directly, making them more memory-efficient, which helps with the creation of complex assemblies. |
| ![Make Sub-Link](toolbar-icons/Std_LinkActions_1.png) | Make Sub-Link | Creates a sub-object or sub-element link |
| ![Replace With Link](toolbar-icons/Std_LinkActions_2.png) | Replace With Link | Replaces the selected objects with links |
| ![Unlink](toolbar-icons/Std_LinkActions_3.png) | Unlink | Unlinks the object by placing it directly in the container |
| ![Import Links](toolbar-icons/Std_LinkActions_4.png) | Import Links | Imports selected external links |
| ![Import All Links](toolbar-icons/Std_LinkActions_5.png) | Import All Links | Imports all links of the active document |

<a id="button-std_massproperties"></a>
### Mass Properties — `Std_MassProperties`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Mass Properties](toolbar-icons/Std_MassProperties.png) | Mass Properties | Calculates mass properties of selected objects |

<a id="button-std_measure"></a>
### Measure — `Std_Measure`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Measure](toolbar-icons/Std_Measure.png) | Measure | Measures a feature |

<a id="button-std_new"></a>
### New File — `Std_New`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![New Document](toolbar-icons/Std_New.png) | New Document | Creates a new empty document |

<a id="button-std_open"></a>
### Open… — `Std_Open`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Open…](toolbar-icons/Std_Open.png) | Open… | Opens a document or imports files |

<a id="button-std_part"></a>
### Add part — `Std_Part`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Add Component](toolbar-icons/Std_Part.png) | Add Component | Adds a component to the active component. |

<a id="button-std_paste"></a>
### Paste — `Std_Paste`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Paste](toolbar-icons/Std_Paste.png) | Paste | Pastes the contents of the clipboard |

<a id="button-std_redo"></a>
### Redo — `Std_Redo`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Redo](toolbar-icons/Std_Redo.png) | Redo | Redoes a previously undone action |

<a id="button-std_refresh"></a>
### Recompute — `Std_Refresh`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Recompute](toolbar-icons/Std_Refresh.png) | Recompute | Recomputes the active document |

<a id="button-std_save"></a>
### Save — `Std_Save`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Save](toolbar-icons/Std_Save.png) | Save | Saves the active document |

<a id="button-std_saveas"></a>
### Save As… — `Std_SaveAs`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Save As…](toolbar-icons/Std_SaveAs.png) | Save As… | Saves the active document under a new file name |

<a id="button-std_toolbarmenu"></a>
### Toolbars — `Std_ToolBarMenu`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Toolbars](../../../src/Gui/Icons/preferences-workbenches.svg) | Toolbars | Toggles this window |

<a id="button-std_undo"></a>
### Undo — `Std_Undo`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Undo](toolbar-icons/Std_Undo.png) | Undo | Undoes the previous action |

<a id="button-std_varset"></a>
### Variable Set — `Std_VarSet`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Variable Set](toolbar-icons/Std_VarSet.png) | Variable Set | Creates a variable set, which is an object that maintains a set of properties to be used as variables |

<a id="button-std_viewbottom"></a>
### Bottom — `Std_ViewBottom`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Bottom](toolbar-icons/Std_ViewBottom.png) | Bottom | Sets the camera to the bottom view |

<a id="button-std_viewfitall"></a>
### Fit All — `Std_ViewFitAll`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Fit All](toolbar-icons/Std_ViewFitAll.png) | Fit All | Fits all content into the 3D view |

<a id="button-std_viewfitselection"></a>
### Fit Selection — `Std_ViewFitSelection`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Fit Selection](toolbar-icons/Std_ViewFitSelection.png) | Fit Selection | Fits the selected content into the 3D view |

<a id="button-std_viewfront"></a>
### Front — `Std_ViewFront`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Front](toolbar-icons/Std_ViewFront.png) | Front | Sets the camera to the front view |

<a id="button-std_viewgroup"></a>
### Isometric — `Std_ViewGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Isometric](toolbar-icons/Std_ViewGroup.png) | Isometric | Sets the camera to the isometric view |
| ![Front](toolbar-icons/Std_ViewGroup_1.png) | Front | Sets the camera to the front view |
| ![Top](toolbar-icons/Std_ViewGroup_2.png) | Top | Sets the camera to the top view |
| ![Right](toolbar-icons/Std_ViewGroup_3.png) | Right | Sets the camera to the right view |
| ![Rear](toolbar-icons/Std_ViewGroup_4.png) | Rear | Sets the camera to the rear view |
| ![Bottom](toolbar-icons/Std_ViewGroup_5.png) | Bottom | Sets the camera to the bottom view |
| ![Left](toolbar-icons/Std_ViewGroup_6.png) | Left | Sets the camera to the left view |

<a id="button-std_viewisometric"></a>
### Isometric — `Std_ViewIsometric`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Isometric](toolbar-icons/Std_ViewIsometric.png) | Isometric | Sets the camera to the isometric view |

<a id="button-std_viewleft"></a>
### Left — `Std_ViewLeft`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Left](toolbar-icons/Std_ViewLeft.png) | Left | Sets the camera to the left view |

<a id="button-std_viewrear"></a>
### Rear — `Std_ViewRear`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Rear](toolbar-icons/Std_ViewRear.png) | Rear | Sets the camera to the rear view |

<a id="button-std_viewright"></a>
### Right — `Std_ViewRight`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Right](toolbar-icons/Std_ViewRight.png) | Right | Sets the camera to the right view |

<a id="button-std_viewstatusbar"></a>
### Status Bar — `Std_ViewStatusBar`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Status Bar](../../../src/Gui/Icons/info.svg) | Status Bar | Toggles the status bar |

<a id="button-std_viewtop"></a>
### Top — `Std_ViewTop`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Top](toolbar-icons/Std_ViewTop.png) | Top | Sets the camera to the top view |

<a id="button-std_whatsthis"></a>
### What's This? — `Std_WhatsThis`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![What's This?](toolbar-icons/Std_WhatsThis.png) | What's This? | Opens the documentation for the selected command |

<a id="button-std_workbench"></a>
### Assembly — `Std_Workbench`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Assembly](toolbar-icons/Std_Workbench.png) | Assembly | Selects the 'Assembly' workbench |
| ![CAM](toolbar-icons/Std_Workbench_1.png) | CAM | Selects the 'CAM' workbench |
| ![Draft](toolbar-icons/Std_Workbench_2.png) | Draft | Selects the 'Draft' workbench |
| ![Material](toolbar-icons/Std_Workbench_3.png) | Material | Selects the 'Material' workbench |
| ![Mesh](toolbar-icons/Std_Workbench_4.png) | Mesh | Selects the 'Mesh' workbench |
| ![Part Design](toolbar-icons/Std_Workbench_5.png) | Part Design | Selects the 'Part Design' workbench |
| ![Part](toolbar-icons/Std_Workbench_6.png) | Part | Selects the 'Part' workbench |
| ![Sketcher](toolbar-icons/Std_Workbench_7.png) | Sketcher | Selects the 'Sketcher' workbench |
| ![Spreadsheet](toolbar-icons/Std_Workbench_8.png) | Spreadsheet | Selects the 'Spreadsheet' workbench |
| ![Surface](toolbar-icons/Std_Workbench_9.png) | Surface | Selects the 'Surface' workbench |
| ![TechDraw](toolbar-icons/Std_Workbench_10.png) | TechDraw | Selects the 'TechDraw' workbench |
| ![](toolbar-icons/Std_Workbench_11.png) |  | Select the ' ' workbench |
| ![Test Framework](toolbar-icons/Std_Workbench_12.png) | Test Framework | Select the 'Test Framework' workbench |

<a id="button-surface_blendcurve"></a>
### Blend Curve — `Surface_BlendCurve`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Blend Curve](toolbar-icons/Surface_BlendCurve.png) | Blend Curve | Joins 2 edges with continuity |

<a id="button-surface_curveonmesh"></a>
### Curve on Mesh — `Surface_CurveOnMesh`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Curve on Mesh](toolbar-icons/Surface_CurveOnMesh.png) | Curve on Mesh | Creates an approximated curve on top of a mesh. This command only works with a mesh object. |

<a id="button-surface_extendface"></a>
### Extend Face — `Surface_ExtendFace`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Extend Face](toolbar-icons/Surface_ExtendFace.png) | Extend Face | Extrapolates the selected face or surface at its boundaries with its local U and V parameters |

<a id="button-surface_filling"></a>
### Filling — `Surface_Filling`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Filling](toolbar-icons/Surface_Filling.png) | Filling | Creates a surface from a series of selected boundary edges. Additionally, the surface may be constrained by edges and vertices that are not on the boundary. |

<a id="button-surface_geomfillsurface"></a>
### Fill Boundary Curves — `Surface_GeomFillSurface`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Fill Boundary Curves](toolbar-icons/Surface_GeomFillSurface.png) | Fill Boundary Curves | Creates a surface from 2, 3, or 4 boundary edges |

<a id="button-surface_sections"></a>
### Sections — `Surface_Sections`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Sections](toolbar-icons/Surface_Sections.png) | Sections | Creates a surface from a series of sectional edges |

<a id="button-techdraw_2pointcosmeticline"></a>
### Cosmetic Line Through 2 Points — `TechDraw_2PointCosmeticLine`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cosmetic Line Through 2 Points](toolbar-icons/TechDraw_2PointCosmeticLine.png) | Cosmetic Line Through 2 Points | Adds a cosmetic line that passes through 2 selected points |

<a id="button-techdraw_3ptangledimension"></a>
### Angle Dimension From 3 Points — `TechDraw_3PtAngleDimension`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Angle Dimension From 3 Points](toolbar-icons/TechDraw_3PtAngleDimension.png) | Angle Dimension From 3 Points | Inserts an angle dimension between 3 selected points |

<a id="button-techdraw_activeview"></a>
### Active View — `TechDraw_ActiveView`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Active View](toolbar-icons/TechDraw_ActiveView.png) | Active View | Inserts an image of the open 3D view in the current page. If multiple 3D views are open, a selection dialog will be shown. |

<a id="button-techdraw_angledimension"></a>
### Angle Dimension — `TechDraw_AngleDimension`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Angle Dimension](toolbar-icons/TechDraw_AngleDimension.png) | Angle Dimension | Inserts an angle dimension between two edges |

<a id="button-techdraw_areadimension"></a>
### Area Annotation — `TechDraw_AreaDimension`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Area Annotation](toolbar-icons/TechDraw_AreaDimension.png) | Area Annotation | Inserts an annotation showing the area of a selected face |

<a id="button-techdraw_axolengthdimension"></a>
### Axonometric Length Dimension — `TechDraw_AxoLengthDimension`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Axonometric Length Dimension](toolbar-icons/TechDraw_AxoLengthDimension.png) | Axonometric Length Dimension | Creates a length dimension in with axonometric view, using selected edges or vertex pairs to define direction and measurement |

<a id="button-techdraw_balloon"></a>
### Balloon Annotation — `TechDraw_Balloon`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Balloon Annotation](toolbar-icons/TechDraw_Balloon.png) | Balloon Annotation | Inserts a new balloon annotation in the selected view |

<a id="button-techdraw_brokenview"></a>
### Broken View — `TechDraw_BrokenView`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Broken View](toolbar-icons/TechDraw_BrokenView.png) | Broken View | Inserts a new broken view for the selected objects or base view and break definition objects |

<a id="button-techdraw_centerlinegroup"></a>
### Centerline on Face — `TechDraw_CenterLineGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Centerline on Face](toolbar-icons/TechDraw_CenterLineGroup.png) | Centerline on Face | Adds a centerline to selected faces |
| ![Centerline Between 2 Lines](toolbar-icons/TechDraw_CenterLineGroup_1.png) | Centerline Between 2 Lines | Adds a centerline between 2 selected lines |
| ![Centerline Between 2 Points](toolbar-icons/TechDraw_CenterLineGroup_2.png) | Centerline Between 2 Points | Adds a centerline between 2 selected points |

<a id="button-techdraw_clipgroup"></a>
### Clip Group — `TechDraw_ClipGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Clip Group](toolbar-icons/TechDraw_ClipGroup.png) | Clip Group | Inserts a new clip group for the selected view |

<a id="button-techdraw_commandaddoffsetvertex"></a>
### Offset Vertex — `TechDraw_CommandAddOffsetVertex`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Offset Vertex](toolbar-icons/TechDraw_CommandAddOffsetVertex.png) | Offset Vertex | Creates an offset from one selected vertex |

<a id="button-techdraw_commandvertexcreationgroup"></a>
### Cosmetic Intersection Vertices — `TechDraw_CommandVertexCreationGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cosmetic Intersection Vertices](toolbar-icons/TechDraw_CommandVertexCreationGroup.png) | Cosmetic Intersection Vertices | Cosmetic Intersection Vertices |
| ![Offset Vertex](toolbar-icons/TechDraw_CommandVertexCreationGroup_1.png) | Offset Vertex | Creates an offset from one selected vertex |

<a id="button-techdraw_compdimensiontools"></a>
### Dimension — `TechDraw_CompDimensionTools`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Dimension](toolbar-icons/TechDraw_CompDimensionTools.png) | Dimension | Inserts new contextual dimensions to the selection. Depending on your selection you might have several dimensions available. You can cycle through them using the M key. Left clicking on empty space will validate the current dimension. Right clicking or pressing Esc will cancel. |
| ![Length Dimension](toolbar-icons/TechDraw_CompDimensionTools_2.png) | Length Dimension | Inserts a length dimension of an edge or distance between two points |
| ![Horizontal Length Dimension](toolbar-icons/TechDraw_CompDimensionTools_3.png) | Horizontal Length Dimension | Inserts a horizontal length dimension of an edge or distance between two points |
| ![Vertical Length Dimension](toolbar-icons/TechDraw_CompDimensionTools_4.png) | Vertical Length Dimension | Inserts a vertical length dimension of an edge or distance between two points |
| ![Radius Dimension](toolbar-icons/TechDraw_CompDimensionTools_5.png) | Radius Dimension | Inserts a radius dimension of a circular edge or arc |
| ![Diameter Dimension](toolbar-icons/TechDraw_CompDimensionTools_6.png) | Diameter Dimension | Inserts a diameter dimension of a circular edge or arc |
| ![Angle Dimension](toolbar-icons/TechDraw_CompDimensionTools_7.png) | Angle Dimension | Inserts an angle dimension between two edges |
| ![Angle Dimension From 3 Points](toolbar-icons/TechDraw_CompDimensionTools_8.png) | Angle Dimension From 3 Points | Inserts an angle dimension between 3 selected points |
| ![Area Annotation](toolbar-icons/TechDraw_CompDimensionTools_9.png) | Area Annotation | Inserts an annotation showing the area of a selected face |
| ![Arc Length Dimension](toolbar-icons/TechDraw_CompDimensionTools_10.png) | Arc Length Dimension | Arc Length Dimension |
| ![Horizontal Extent Dimension](toolbar-icons/TechDraw_CompDimensionTools_12.png) | Horizontal Extent Dimension | Inserts a dimension showing the horizontal extent (overall length) of an object or feature |
| ![Vertical Extent Dimension](toolbar-icons/TechDraw_CompDimensionTools_13.png) | Vertical Extent Dimension | Inserts a dimension showing the vertical extent (overall length) of an object or feature |
| ![Horizontal Chain Dimension](toolbar-icons/TechDraw_CompDimensionTools_15.png) | Horizontal Chain Dimension | Horizontal Chain Dimension |
| ![Vertical Chain Dimension](toolbar-icons/TechDraw_CompDimensionTools_16.png) | Vertical Chain Dimension | Vertical Chain Dimension |
| ![Oblique Chain Dimension](toolbar-icons/TechDraw_CompDimensionTools_17.png) | Oblique Chain Dimension | Oblique Chain Dimension |
| ![Horizontal Coordinate Dimension](toolbar-icons/TechDraw_CompDimensionTools_19.png) | Horizontal Coordinate Dimension | Horizontal Coordinate Dimension |
| ![Vertical Coordinate Dimension](toolbar-icons/TechDraw_CompDimensionTools_20.png) | Vertical Coordinate Dimension | Vertical Coordinate Dimension |
| ![Oblique Coordinate Dimension](toolbar-icons/TechDraw_CompDimensionTools_21.png) | Oblique Coordinate Dimension | Oblique Coordinate Dimension |
| ![Horizontal Chamfer Dimension](toolbar-icons/TechDraw_CompDimensionTools_23.png) | Horizontal Chamfer Dimension | Horizontal Chamfer Dimension |
| ![Vertical Chamfer Dimension](toolbar-icons/TechDraw_CompDimensionTools_24.png) | Vertical Chamfer Dimension | Vertical Chamfer Dimension |

<a id="button-techdraw_cosmeticvertexgroup"></a>
### Cosmetic Vertex — `TechDraw_CosmeticVertexGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cosmetic Vertex](toolbar-icons/TechDraw_CosmeticVertexGroup.png) | Cosmetic Vertex | Inserts a cosmetic vertex into a view |
| ![Midpoint Vertices](toolbar-icons/TechDraw_CosmeticVertexGroup_1.png) | Midpoint Vertices | Inserts cosmetic vertices at the midpoint of the selected edges |
| ![Quadrant Vertices](toolbar-icons/TechDraw_CosmeticVertexGroup_2.png) | Quadrant Vertices | Inserts cosmetic vertices at the quadrant points of the selected circles |

<a id="button-techdraw_decorateline"></a>
### Edit Line Appearance — `TechDraw_DecorateLine`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Edit Line Appearance](toolbar-icons/TechDraw_DecorateLine.png) | Edit Line Appearance | Opens the 'Line decoration' dialog to edit the selected lines |

<a id="button-techdraw_detailview"></a>
### Detail View — `TechDraw_DetailView`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Detail View](toolbar-icons/TechDraw_DetailView.png) | Detail View | Inserts a new detail view based on the selected view in the current page |

<a id="button-techdraw_diameterdimension"></a>
### Diameter Dimension — `TechDraw_DiameterDimension`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Diameter Dimension](toolbar-icons/TechDraw_DiameterDimension.png) | Diameter Dimension | Inserts a diameter dimension of a circular edge or arc |

<a id="button-techdraw_dimension"></a>
### Dimension — `TechDraw_Dimension`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Dimension](toolbar-icons/TechDraw_Dimension.png) | Dimension | Inserts new contextual dimensions to the selection. Depending on your selection you might have several dimensions available. You can cycle through them using the M key. Left clicking on empty space will validate the current dimension. Right clicking or pressing Esc will cancel. |

<a id="button-techdraw_dimensionrepair"></a>
### Repair Dimension References — `TechDraw_DimensionRepair`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Repair Dimension References](toolbar-icons/TechDraw_DimensionRepair.png) | Repair Dimension References | Repairs broken or incorrect dimension references |

<a id="button-techdraw_draftview"></a>
### Draft View — `TechDraw_DraftView`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Draft View](toolbar-icons/TechDraw_DraftView.png) | Draft View | Inserts a view of a Draft object |

<a id="button-techdraw_exportpagedxf"></a>
### Export Page as DXF — `TechDraw_ExportPageDXF`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Export Page as DXF](toolbar-icons/TechDraw_ExportPageDXF.png) | Export Page as DXF | Exports the current page as a DXF |

<a id="button-techdraw_exportpagesvg"></a>
### Export Page as SVG — `TechDraw_ExportPageSVG`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Export Page as SVG](toolbar-icons/TechDraw_ExportPageSVG.png) | Export Page as SVG | Exports the current page as an SVG |

<a id="button-techdraw_extensionarclengthannotation"></a>
### Arc Length Annotation — `TechDraw_ExtensionArcLengthAnnotation`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Arc Length Annotation](toolbar-icons/TechDraw_ExtensionArcLengthAnnotation.png) | Arc Length Annotation | Inserts an annotation with the calculated arc length of the selected edges |

<a id="button-techdraw_extensionareaannotation"></a>
### Area Annotation — `TechDraw_ExtensionAreaAnnotation`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Area Annotation](toolbar-icons/TechDraw_ExtensionAreaAnnotation.png) | Area Annotation | Calculates the area of multiple selected faces |

<a id="button-techdraw_extensionchamferdimensiongroup"></a>
### Horizontal Chamfer Dimension — `TechDraw_ExtensionChamferDimensionGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Horizontal Chamfer Dimension](toolbar-icons/TechDraw_ExtensionChamferDimensionGroup.png) | Horizontal Chamfer Dimension | Horizontal Chamfer Dimension |
| ![Vertical Chamfer Dimension](toolbar-icons/TechDraw_ExtensionChamferDimensionGroup_1.png) | Vertical Chamfer Dimension | Vertical Chamfer Dimension |

<a id="button-techdraw_extensionchangelineattributes"></a>
### Change Line Attributes — `TechDraw_ExtensionChangeLineAttributes`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Change Line Attributes](toolbar-icons/TechDraw_ExtensionChangeLineAttributes.png) | Change Line Attributes | Change Line Attributes |

<a id="button-techdraw_extensioncirclecenterlinesgroup"></a>
### Circle Centerlines — `TechDraw_ExtensionCircleCenterLinesGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Circle Centerlines](toolbar-icons/TechDraw_ExtensionCircleCenterLinesGroup.png) | Circle Centerlines | Circle Centerlines |
| ![Bolt Circle Centerlines](toolbar-icons/TechDraw_ExtensionCircleCenterLinesGroup_1.png) | Bolt Circle Centerlines | Bolt Circle Centerlines |

<a id="button-techdraw_extensioncreatechaindimensiongroup"></a>
### Horizontal Chain Dimension — `TechDraw_ExtensionCreateChainDimensionGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Horizontal Chain Dimension](toolbar-icons/TechDraw_ExtensionCreateChainDimensionGroup.png) | Horizontal Chain Dimension | Horizontal Chain Dimension |
| ![Vertical Chain Dimension](toolbar-icons/TechDraw_ExtensionCreateChainDimensionGroup_1.png) | Vertical Chain Dimension | Vertical Chain Dimension |
| ![Oblique Chain Dimension](toolbar-icons/TechDraw_ExtensionCreateChainDimensionGroup_2.png) | Oblique Chain Dimension | Oblique Chain Dimension |

<a id="button-techdraw_extensioncreatecoorddimensiongroup"></a>
### Horizontal Coordinate Dimension — `TechDraw_ExtensionCreateCoordDimensionGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Horizontal Coordinate Dimension](toolbar-icons/TechDraw_ExtensionCreateCoordDimensionGroup.png) | Horizontal Coordinate Dimension | Horizontal Coordinate Dimension |
| ![Vertical Coordinate Dimension](toolbar-icons/TechDraw_ExtensionCreateCoordDimensionGroup_1.png) | Vertical Coordinate Dimension | Vertical Coordinate Dimension |
| ![Oblique Coordinate Dimension](toolbar-icons/TechDraw_ExtensionCreateCoordDimensionGroup_2.png) | Oblique Coordinate Dimension | Oblique Coordinate Dimension |

<a id="button-techdraw_extensioncreatelengtharc"></a>
### Arc Length Dimension — `TechDraw_ExtensionCreateLengthArc`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Arc Length Dimension](toolbar-icons/TechDraw_ExtensionCreateLengthArc.png) | Arc Length Dimension | Arc Length Dimension |

<a id="button-techdraw_extensioncustomizeformat"></a>
### Customize Format Label — `TechDraw_ExtensionCustomizeFormat`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Customize Format Label](toolbar-icons/TechDraw_ExtensionCustomizeFormat.png) | Customize Format Label | Customizes the format label of a selected dimension or balloon |

<a id="button-techdraw_extensiondrawcirclesgroup"></a>
### Cosmetic 1 Point Circle — `TechDraw_ExtensionDrawCirclesGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cosmetic 1 Point Circle](toolbar-icons/TechDraw_ExtensionDrawCirclesGroup.png) | Cosmetic 1 Point Circle | Cosmetic 1 Point Circle |
| ![Cosmetic 2 Point Circle](toolbar-icons/TechDraw_ExtensionDrawCirclesGroup_1.png) | Cosmetic 2 Point Circle | Cosmetic 2 Point Circle |
| ![Cosmetic 3 Point Circle](toolbar-icons/TechDraw_ExtensionDrawCirclesGroup_2.png) | Cosmetic 3 Point Circle | Cosmetic 3 Point Circle |
| ![Cosmetic Arc](toolbar-icons/TechDraw_ExtensionDrawCirclesGroup_3.png) | Cosmetic Arc | Cosmetic Arc |

<a id="button-techdraw_extensionextendshortenlinegroup"></a>
### Extend Line — `TechDraw_ExtensionExtendShortenLineGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Extend Line](toolbar-icons/TechDraw_ExtensionExtendShortenLineGroup.png) | Extend Line | Extend Line |
| ![Shorten Line](toolbar-icons/TechDraw_ExtensionExtendShortenLineGroup_1.png) | Shorten Line | Shorten Line |

<a id="button-techdraw_extensionincreasedecreasegroup"></a>
### Increase Decimal Places — `TechDraw_ExtensionIncreaseDecreaseGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Increase Decimal Places](toolbar-icons/TechDraw_ExtensionIncreaseDecreaseGroup.png) | Increase Decimal Places | Increase Decimal Places |
| ![Decrease Decimal Places](toolbar-icons/TechDraw_ExtensionIncreaseDecreaseGroup_1.png) | Decrease Decimal Places | Decrease Decimal Places |

<a id="button-techdraw_extensioninsertprefixgroup"></a>
### Insert '⌀' Prefix — `TechDraw_ExtensionInsertPrefixGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Insert '⌀' Prefix](toolbar-icons/TechDraw_ExtensionInsertPrefixGroup.png) | Insert '⌀' Prefix | Insert '⌀' Prefix |
| ![Insert '□' Prefix](toolbar-icons/TechDraw_ExtensionInsertPrefixGroup_1.png) | Insert '□' Prefix | Insert '□' Prefix |
| ![Insert 'n×' Prefix](toolbar-icons/TechDraw_ExtensionInsertPrefixGroup_2.png) | Insert 'n×' Prefix | Insert 'n×' Prefix |
| ![Remove Prefix](toolbar-icons/TechDraw_ExtensionInsertPrefixGroup_3.png) | Remove Prefix | Remove Prefix |

<a id="button-techdraw_extensionlineppgroup"></a>
### Cosmetic Parallel Line — `TechDraw_ExtensionLinePPGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cosmetic Parallel Line](toolbar-icons/TechDraw_ExtensionLinePPGroup.png) | Cosmetic Parallel Line | Cosmetic Parallel Line |
| ![Cosmetic Perpendicular Line](toolbar-icons/TechDraw_ExtensionLinePPGroup_1.png) | Cosmetic Perpendicular Line | Cosmetic Perpendicular Line |

<a id="button-techdraw_extensionlockunlockview"></a>
### Toggle View Lock — `TechDraw_ExtensionLockUnlockView`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Toggle View Lock](toolbar-icons/TechDraw_ExtensionLockUnlockView.png) | Toggle View Lock | Toggle View Lock |

<a id="button-techdraw_extensionpositionsectionview"></a>
### Position Section View — `TechDraw_ExtensionPositionSectionView`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Position Section View](toolbar-icons/TechDraw_ExtensionPositionSectionView.png) | Position Section View | Aligns the selected section view with its source view orthogonally or the selected edge in the section view to the selected vertex in the base view |

<a id="button-techdraw_extensionselectlineattributes"></a>
### Select Line Attributes, Cascade Spacing and Delta Distance — `TechDraw_ExtensionSelectLineAttributes`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Select Line Attributes, Cascade Spacing and Delta Distance](toolbar-icons/TechDraw_ExtensionSelectLineAttributes.png) | Select Line Attributes, Cascade Spacing and Delta Distance | Select Line Attributes, Cascade Spacing and Delta Distance |

<a id="button-techdraw_extensionthreadsgroup"></a>
### Cosmetic Thread Hole Side View — `TechDraw_ExtensionThreadsGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cosmetic Thread Hole Side View](toolbar-icons/TechDraw_ExtensionThreadsGroup.png) | Cosmetic Thread Hole Side View | Cosmetic Thread Hole Side View |
| ![Cosmetic Thread Hole Bottom View](toolbar-icons/TechDraw_ExtensionThreadsGroup_1.png) | Cosmetic Thread Hole Bottom View | Cosmetic Thread Hole Bottom View |
| ![Cosmetic Thread Bolt Side View](toolbar-icons/TechDraw_ExtensionThreadsGroup_2.png) | Cosmetic Thread Bolt Side View | Cosmetic Thread Bolt Side View |
| ![Cosmetic Thread Bolt Bottom View](toolbar-icons/TechDraw_ExtensionThreadsGroup_3.png) | Cosmetic Thread Bolt Bottom View | Cosmetic Thread Bolt Bottom View |

<a id="button-techdraw_extensionvertexatintersection"></a>
### Cosmetic Intersection Vertices — `TechDraw_ExtensionVertexAtIntersection`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Cosmetic Intersection Vertices](toolbar-icons/TechDraw_ExtensionVertexAtIntersection.png) | Cosmetic Intersection Vertices | Cosmetic Intersection Vertices |

<a id="button-techdraw_extentgroup"></a>
### Horizontal extent — `TechDraw_ExtentGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Horizontal extent](toolbar-icons/TechDraw_ExtentGroup.png) | Horizontal extent | Insert horizontal extent dimension |
| ![Vertical extent](toolbar-icons/TechDraw_ExtentGroup_1.png) | Vertical extent | Insert vertical extent dimension |

<a id="button-techdraw_filltemplatefields"></a>
### Update Template Fields — `TechDraw_FillTemplateFields`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Update Template Fields](toolbar-icons/TechDraw_FillTemplateFields.png) | Update Template Fields | Uses document info to populate the template fields |

<a id="button-techdraw_geometrichatch"></a>
### Geometric Hatch — `TechDraw_GeometricHatch`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Geometric Hatch](toolbar-icons/TechDraw_GeometricHatch.png) | Geometric Hatch | Applies a geometric hatch pattern to the selected faces |

<a id="button-techdraw_hatch"></a>
### Image Hatch — `TechDraw_Hatch`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Image Hatch](toolbar-icons/TechDraw_Hatch.png) | Image Hatch | Applies a hatch pattern to the selected faces using an image file |

<a id="button-techdraw_holeshaftfit"></a>
### Hole/Shaft Fit — `TechDraw_HoleShaftFit`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Hole/Shaft Fit](toolbar-icons/TechDraw_HoleShaftFit.png) | Hole/Shaft Fit | Adds a hole or shaft fit to a selected length or diameter dimension |

<a id="button-techdraw_horizontaldimension"></a>
### Horizontal Length Dimension — `TechDraw_HorizontalDimension`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Horizontal Length Dimension](toolbar-icons/TechDraw_HorizontalDimension.png) | Horizontal Length Dimension | Inserts a horizontal length dimension of an edge or distance between two points |

<a id="button-techdraw_leaderline"></a>
### Leader Line — `TechDraw_LeaderLine`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Leader Line](toolbar-icons/TechDraw_LeaderLine.png) | Leader Line | Adds a leader line |

<a id="button-techdraw_lengthdimension"></a>
### Length Dimension — `TechDraw_LengthDimension`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Length Dimension](toolbar-icons/TechDraw_LengthDimension.png) | Length Dimension | Inserts a length dimension of an edge or distance between two points |

<a id="button-techdraw_pagedefault"></a>
### New Page — `TechDraw_PageDefault`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![New Page](toolbar-icons/TechDraw_PageDefault.png) | New Page | Creates a new page with the default template |

<a id="button-techdraw_pagetemplate"></a>
### New Page From Template — `TechDraw_PageTemplate`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![New Page From Template](toolbar-icons/TechDraw_PageTemplate.png) | New Page From Template | Creates a new page from a custom template |

<a id="button-techdraw_printall"></a>
### Print All Pages — `TechDraw_PrintAll`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Print All Pages](toolbar-icons/TechDraw_PrintAll.png) | Print All Pages | Prints all pages with the print dialog |

<a id="button-techdraw_radiusdimension"></a>
### Radius Dimension — `TechDraw_RadiusDimension`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Radius Dimension](toolbar-icons/TechDraw_RadiusDimension.png) | Radius Dimension | Inserts a radius dimension of a circular edge or arc |

<a id="button-techdraw_redrawpage"></a>
### Redraw Page — `TechDraw_RedrawPage`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Redraw Page](toolbar-icons/TechDraw_RedrawPage.png) | Redraw Page | Redraws the current page |

<a id="button-techdraw_richtextannotation"></a>
### Rich Text Annotation — `TechDraw_RichTextAnnotation`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Rich Text Annotation](toolbar-icons/TechDraw_RichTextAnnotation.png) | Rich Text Annotation | Inserts a rich text annotation in the current page |

<a id="button-techdraw_sectiongroup"></a>
### Section View — `TechDraw_SectionGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Section View](toolbar-icons/TechDraw_SectionGroup.png) | Section View | Inserts a simple section view |
| ![Complex Section View](toolbar-icons/TechDraw_SectionGroup_1.png) | Complex Section View | Inserts a complex section view |

<a id="button-techdraw_showall"></a>
### Toggle Edge Visibility — `TechDraw_ShowAll`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Toggle Edge Visibility](toolbar-icons/TechDraw_ShowAll.png) | Toggle Edge Visibility | Toggles the visibility of the selected edges |

<a id="button-techdraw_spreadsheetview"></a>
### Spreadsheet View — `TechDraw_SpreadsheetView`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Spreadsheet View](toolbar-icons/TechDraw_SpreadsheetView.png) | Spreadsheet View | Inserts a view of a spreadsheet in the current page |

<a id="button-techdraw_stackgroup"></a>
### Stack Top — `TechDraw_StackGroup`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Stack Top](toolbar-icons/TechDraw_StackGroup.png) | Stack Top | Moves the view to the top of the stack |
| ![Stack Bottom](toolbar-icons/TechDraw_StackGroup_1.png) | Stack Bottom | Moves the view to the bottom of the stack |
| ![Stack Up](toolbar-icons/TechDraw_StackGroup_2.png) | Stack Up | Moves the view up one level |
| ![Stack Down](toolbar-icons/TechDraw_StackGroup_3.png) | Stack Down | Moves the view down one level |

<a id="button-techdraw_surfacefinishsymbols"></a>
### Surface Finish Symbol — `TechDraw_SurfaceFinishSymbols`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Surface Finish Symbol](toolbar-icons/TechDraw_SurfaceFinishSymbols.png) | Surface Finish Symbol | Adds a surface finish symbol in the selected view |

<a id="button-techdraw_toggleframe"></a>
### Toggle View Frames — `TechDraw_ToggleFrame`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Toggle View Frames](toolbar-icons/TechDraw_ToggleFrame.png) | Toggle View Frames | Toggles visibility of view frames and vertices |

<a id="button-techdraw_verticaldimension"></a>
### Vertical Length Dimension — `TechDraw_VerticalDimension`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Vertical Length Dimension](toolbar-icons/TechDraw_VerticalDimension.png) | Vertical Length Dimension | Inserts a vertical length dimension of an edge or distance between two points |

<a id="button-techdraw_view"></a>
### New View — `TechDraw_View`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![New View](toolbar-icons/TechDraw_View.png) | New View | Inserts a new view into the current page based on the selected object in the tree view or 3D view. If no object is selected, a file browser opens to select an SVG or image file. |

<a id="button-techdraw_weldsymbol"></a>
### Weld Symbol — `TechDraw_WeldSymbol`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Weld Symbol](toolbar-icons/TechDraw_WeldSymbol.png) | Weld Symbol | Adds welding information to the selected leader line |

<a id="button-test_test"></a>
### Self-test... — `Test_Test`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Self-test...](../../../src/Gui/Icons/preferences-general.svg) | Self-test... | Runs a self-test to check if the application works properly |

<a id="button-test_testall"></a>
### Test all — `Test_TestAll`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Test all](toolbar-icons/Test_TestAll.png) | Test all | Runs all tests at once (can take very long!) |

<a id="button-test_testbase"></a>
### Test base — `Test_TestBase`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Test base](toolbar-icons/Test_TestBase.png) | Test base | Test the basic functions of FreeCAD |

<a id="button-test_testdoc"></a>
### Test Document — `Test_TestDoc`

| Icon | Button / dropdown choice | Function |
| --- | --- | --- |
| ![Test Document](toolbar-icons/Test_TestDoc.png) | Test Document | Test the document (creation, save, load and destruction) |
