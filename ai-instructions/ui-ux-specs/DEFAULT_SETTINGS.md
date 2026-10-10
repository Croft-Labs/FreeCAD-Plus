# Default settings

Status: owner-intent specification, reconstructed 2026-10-10. **Only the confirmed requirements are authoritative.** Material headed **Needs owner confirmation** is preserved for review and must not be treated as an approved change. The current application, agent-written specifications and implementation reports do not establish owner approval. Newer explicit owner decisions supersede older decisions on the same subject. See [evidence and unresolved decisions](EVIDENCE_AND_DECISIONS.md).

## Confirmed defaults

Defaults and user customization are distinct. The explicit saved choices below remain persistent. Values recorded only in the DOCX are listed separately for confirmation; an old claim that a screenshot approved a value is not itself that screenshot or an owner instruction.

| Setting | Confirmed value or behavior | Evidence |
| --- | --- | --- |
| Initial Tasks docking | Right side; restore subsequent user customization of panels and toolbars | C06 |
| New file's first component | Part001, domestic, placed once and immediately active | C09 |
| Active component Part Type | Full Component | C10 |
| Direct children Part Type | Bodies Only, with saved parent-owned overrides | C10 |
| Contextual non-active transparency | At least 75%; preserve greater transparency | C09/C10 |
| Curve intent | Single Curve | R03 adopted Selection prompt |
| Directional Selection | On; retain saved choice | R03 |
| Persistent Selection | On; retain saved choice | R03 |
| Initial layer | Base; exactly one active layer | R03 |
| Newly created independent objects | Active layer | R03 |
| Origin layer | Base, protected | R03 |
| Constraint palette dismissal | One second outside travel corridor; no timeout inside | R03 |
| Move Components first method | Translate; exact method order in Task Panel | R03 |
| Translate initial/reset inputs | Direction unset, Distance zero, Reverse off | R03 adopted Translate prompt |
| Rotate reset inputs | Axis/pivot unset, angle zero, Reverse off | R03 adopted Rotate prompt |
| Align Axes | Make Coincident; Reverse Target Direction off | Adopted movement prompt 7 |
| Interactive pivot | Selected group center; axes aligned to active parent | Adopted movement prompt 9 |
| Interactive movement snapping | Off; deliberate distance/angle snapping available | Adopted movement prompt 9 |

Evidence keys resolve in [Evidence and Decisions](EVIDENCE_AND_DECISIONS.md). The detailed behaviors have one home in the other four specifications; this table is a lookup of their defaults.

## Decisions requiring owner confirmation

The accessible history does not include the October 2 screenshots or the complete older conversations. Therefore the DOCX's exact theme, navigation style, units, colors, pixel sizes, numeric formatting, grid visibility and initial left-panel split remain **Needs owner confirmation**. Do not use the present application settings to confirm them. Medium icons must be larger per C06, but the specific 32 px icon / 42 px button dimensions in the DOCX are not established by that request alone.

## Transferred DOCX requirements — Needs owner confirmation

The following source candidates are not instructions to implement. Exact values, added restrictions and implementation-derived details need owner confirmation. D numbers identify the archived DOCX paragraphs; [the coverage record](archive/2026-10-10/docx-coverage.json) accounts for every source block. Confirmed rules above override conflicting candidate wording. Implementation reports remain archival only.

### Basic defaults

**D2800 — Needs owner confirmation:** Create the first automatic part as Part001 and use untitled001 for the default file name.

**D2806 — Needs owner confirmation:** Toolbar interface: Plus UI.

**D2807 — Needs owner confirmation:** Navigation style: Blender.

**D2808 — Needs owner confirmation:** Units: Imperial Decimal.

**D2809 — Needs owner confirmation:** Default document name: untitled001.

**D2810 — Needs owner confirmation:** First automatically added part: Part001, then the next available number.

**D2811 — Needs owner confirmation:** First sketch in each component: Sketch001; first background Body: Body001.

**D2812 — Needs owner confirmation:** Origin visible for the active component; Origin Planes hidden.

**D2813 — Needs owner confirmation:** Preview: Overlay, using blue for New Body, green for Add and red for Subtract.

**D2814 — Needs owner confirmation:** Apply defaults to unset preferences; keep the selectors functional so the user can change and retain their choices.

### General and application preset

**D2816 — Needs owner confirmation:** General: English; Imperial Decimal (in, lb); 3 decimal places. Honor project units. Use operating-system number formatting; do not substitute the decimal separator.

**D2817 — Needs owner confirmation:** Application: FreeCAD Light theme; medium 24 px toolbar icons; Combined Tree View and Property View; 4 recent files. Tiled background off; cursor blinking and startup splash on. Panels start docked, with Tasks on the right. Migrate the old implicit Tasks overlay once; retain other overlay memberships and subsequent user customization. Retain Plus UI and Blender navigation defaults.

### Selection preset

**D2819 — Needs owner confirmation:** Preselection on, yellow #FFFF00; selection on, amber #FFBF00; pick radius 5 px. Tree hover preselection, automatic view switching, automatic tree expansion, selection history and tree selection checkboxes off.

### Display color preset

**D2821 — Needs owner confirmation:** Simple background #F7F7F7; linear and radial gradients off. Object being edited #00AAFF; active container #5BB413. Color bar label #212529, 13 pt.

### Sketcher preset

**D2823 — Needs owner confirmation:** Creating line, coordinate text and cursor crosshair: #212529.

**D2824 — Needs owner confirmation:** Geometry: constrained #005500; unconstrained #00AA00; solid lines, 2 px.

**D2825 — Needs owner confirmation:** Construction and internal alignment geometry: constrained #5555FF; unconstrained #00AAFF; dashed lines (6:2), 2 px.

**D2826 — Needs owner confirmation:** External construction geometry: #FF00FF; short dashed lines (3:1), 2 px. External defining geometry: #CC3399; solid lines, 2 px.

**D2827 — Needs owner confirmation:** Fully constrained sketch: #000000. Invalid sketch: #FF0000.

**D2828 — Needs owner confirmation:** Constraint symbols and dimensional constraints: #0000FF. Reference constraints: #00AAFF. Expression-dependent constraints: #FF00FF. Deactivated constraints: #868E96.

**D2829 — Needs owner confirmation:** Outside Sketcher: vertices and edges #000000; face swatch #CBDFF4.

### Preference preservation and superseded maintenance rule

**D2831 — Superseded:** The old mandatory DOCX-update rule is replaced by the October 10 instruction to maintain these five Markdown specifications. The original rule is archived.

**D2832 — Needs owner confirmation:** Apply these defaults to unset preferences in new profiles; preserve subsequent saved user choices. The owner explicitly requested applying this preset to the closed development build profile as well.


### Sketch grid

**D2857 — Needs owner confirmation:** Sketcher grid default: new sketches start with the grid hidden when no explicit grid preference is saved. Seed the native Mod/Sketcher/General ShowGrid preference to false. Keep the Sketcher grid toggle and preferences available so the user can enable it. Preserve explicit saved preferences and each existing sketch's stored grid visibility; do not reset the grid each time sketch edit opens. This preference-only change retains geometry, units and grid spacing.
