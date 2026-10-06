# Legacy conversion inventory and planning

Task one exposes `CadDocument.legacy_plan(document)` for an already-open, native
legacy document. It delegates to `LegacyConversion.inventory`, returns JSON-safe
data and does not open/convert/save/recompute files, assign identities, change
ownership or create fallback objects. Existing automatic conversion is unchanged.

The version-one plan records native document/object keys and any existing ObjectId,
types, labels, states, property serialization fingerprints, ownership/Group/Tip,
local and available world frames, LinkPlacement/LinkTransform/scale/array count,
links and expressions. Stored Shape properties supply BREP fingerprints, validity,
topology counts, volume/area and bounds. BREP hashes detect changes within a snapshot;
they are not geometric equivalence proofs across native serialization/reopen.
Links without a native world-frame accessor retain local frames and owner/target
references; subsequent occurrence conversion must resolve full native transforms.

App::Part objects propose definitions; standalone Bodies propose definitions.
Bodies inside a Part remain result/history candidates in that Part. Existing links
propose retained occurrences of their targets. The file master is a separate
permanent context. Root geometry targeted by links proposes one shared definition;
internal-feature targets are explicitly unresolved boundaries, not silently moved.
Definitions' container placements propose future instances. These are proposals,
not permission to execute structural migration or merge geometrically equal models.

Dependency order uses native link/expression inputs. Group, Origin, OriginFeatures
and the private native `_Body` backlink are structural, not computational inputs.
Cycles and nodes dependent on cycles remain blocked. External object/file references
are recorded without opening or converting dependencies. Unresolved links and
snapshot failures produce issues while independent objects/geometry remain visible.

Every later task must follow the approved recovery ladder: feature adapter, retained
editable native feature, explicit dumb geometry recovery, reported unavailable
output. The inventory distinguishes dumb body/sheet/curve/point candidates, invalid
geometry, missing geometry and stale/dependency-stale caches. A valid cached shape
is only an available candidate: later recovery must verify freshness, full placement
and loss of parametrics. Never report a dumb result as complete feature conversion.

Run `TestLegacyConversionPlan` in the fork runtime. Native fixtures cover nested
Parts, Body/sketch/Pad history, shared Links, attached sketch/datum dependencies,
expressions/cycles, external files, missing links, unsupported objects, all recovery
kinds, touched caches, partial fingerprint errors and no mutation. FCStd save/reopen
checks preserved Body Group/Tip/sketch constraints and native bidirectional solid
differences. Source-mode checks use `FREECAD_PLUS_PROFILE_SOURCE=1` and explicitly
record loaded source hashes; they are not installed-payload or owner-GUI acceptance.
Batch packaging with subsequent structural conversion work.
