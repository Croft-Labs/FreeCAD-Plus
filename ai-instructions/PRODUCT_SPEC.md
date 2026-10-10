# FreeCAD Plus: Product specification

## Purpose

Develop the owner's intended component-based CAD interface and workflows using a
controlled official FreeCAD baseline. Preserve useful original workbenches and
native engineering behavior while applying only confirmed changes.

## Current source scope

Official FreeCAD 1.1.4 is the starting application. No prior Plus implementation
has been transferred. The previous fork is retained for comparison and reuse only
after each relevant behavior is checked against owner intent.

The [UI specification collection](UI_UX_SPEC.md) defines confirmed intended behavior,
including components serving as parts and assemblies and user-facing sketches,
features and geometry with backend Bodies. These are future implementation
requirements, not a claim that stock 1.1.4 already implements the Plus model.

## Authority and boundaries

Newer explicit owner instructions override older ones. Unverified details and
archived plans remain review material. Do not treat the current application,
historical technical choices or a successful build as proof of owner acceptance.
Preserve source licensing, document/property identities, original workbench access,
source archives and the user's saved data. No reimplementation is begun merely
because this baseline exists.
