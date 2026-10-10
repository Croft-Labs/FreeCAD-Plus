# ADR 003: component documents over native persistence

Date: 2026-10-01. Status: accepted initial production mapping for roadmap 7.8.
The [approved component contract](COMPONENT_DOCUMENT_CONTRACT.md) owns semantics;
the roadmap owns implementation and acceptance status.

## Decision

Use native `App::Part` definitions and `App::Link` occurrences with distinct stable
identities. A hidden document metadata object identifies the root. Definitions
hold ordered object names for History and a separate result registry, avoiding
reverse dependency edges from operations to their owning component. Native object
types, properties, geometry, transactions and serialization remain intact.

Publish evaluated geometry as independently identified `Part::FeaturePython`
results with links to native producing operations. Direct-child references retain
source occurrence/object identities and copy evaluated geometry into the parent's
coordinates. They never copy sketch constraints or producer history. The service
owns pending/ready/repair state, refresh and parameter deletion. Freezing an output
retains its identity; shared producers are removed only when no other consumers
need them. Native geometry consumers can continue to consume these shape objects.

This selects the result-layer direction considered in ADR 001. It does not turn
the experimental split/merge adapters into production code, replace the native
kernel or establish arbitrary topology correspondence. Ambiguous multi-solid
outputs require explicit identified output roles; silently assigning solid indices
would violate the approved identity contract. Native Body history remains available
for converted documents and unmigrated Part Design commands.

## Archive and reader contract

`.cadprt` uses the native ZIP writer and its atomic replacement/backup behavior.
It adds exactly one UTF-8 `ComponentManifest.json` alongside native `Document.xml`,
GUI/view payloads and geometry files. The JSON contains:

| Field | Meaning |
| --- | --- |
| `format`, `version` | `org.freecad-plus.component-document`, schema integer 1 |
| `required` | `components-v1`, `native-objects-v1`, `evaluated-references-v1` |
| `document`, `root` | Stable document and root-definition identities |
| `definitions` | Definition identity/native object name, ordered history/result names, occurrence identity/name/definition/external flag |
| `dependencies` | External document identity to relative path, including unused explicit imports; absolute path when Windows drives differ |
| `imports` | Optional explicit file-import identity/native object name/document identity list; requires `component-file-imports-v1` |

Native properties retain the actual link graph, placements, parameters, display
overrides and reference bindings. The manifest is an integrity and capability
envelope, not a competing geometry serializer. The writer validates before touching
output. Native restore preflights required capabilities even for renamed archives
and backup extensions, before clearing objects or restoring proxies. The component
reader verifies native metadata/history against the manifest after restore and
opens external dependencies fully before resolving links. Missing files open in a
repairable state; saving unresolved component links is refused. Missing reference
geometry remains editable and saveable with its source identity and repair status;
invalid format/component identities still refuse opening. Activation refreshes every
independent reference before reporting broken branches. Locate Component File
requires the original definition and referenced-object identities.

Save As/Copy preserve semantic identities. Failed Save As restores the original
location and label. The October 9 copy workflow regenerates the copied domestic
closure's definition/object/occurrence identities, remaps native links and semantic
registries, and retains already-external children as explicitly shared imports.
Selected domestic placement replacement is a separate transaction retaining link
identity and transform. Expression-driven copies and unmapped external consumers
fail preflight rather than silently changing bindings. The earlier identity-moving
`externalize` service remains for legacy/internal callers, not the user copy action.

Explicit imports are hidden native `App::FeaturePython` records with a `PropertyXLink`
to the source root, stable record identity and expected source document identity.
They persist unused files without synthesizing placements. Readers cross-check records
against the envelope. Only files with these records require the additive capability;
older occurrence-only files retain their previous capability set and derive their
inventory from links without an automatic write migration. Native restore/preflight
continues to delegate to CadDocument. Missing imports open for identity-based repair;
unresolved imports cannot be saved. File-graph DFS allows shared diamonds and blocks
cycles independently of occurrence-graph validation. Models projects this nested graph;
insertion choices use the active defining file's domestic/direct-import inventory.

## Compatibility and integration boundaries

Standard GUI New creates a component document. Standard GUI Open converts supported
FCStd objects in memory, reports retained unsupported payloads and clears the save
location. The original is protected from overwrite. Native `App.newDocument` and
`App.openDocument` retain their API behavior for scripts, legacy tests and internal
scratch documents. A renamed FCStd without a manifest is not valid `.cadprt`.

Owner feedback 7.8.7u supersedes the original navigator projection: Models lists
definitions and instance counts, Part Tree projects the permanent root
context followed by child occurrence links (owner follow-up 7.8.7v),
and Attributes replaces the native Model pane while reusing its property editor.
History displays owned objects and operations. Native LinkView
projections implement occurrence-path display and isolated views without changing
the source geometry. This is separate from BOM/mass participation.

Remaining gates include production multi-result lineage, complete command/task-pane
migration, assembly solver integration, complete BOM/mass consumer integration,
general expression remapping, deep hierarchy copying and broader native selection,
recovery and engineering-consumer acceptance. The persistence foundation does not
close those gates. See roadmap 7.8 and [the owner procedure](../../tests/ComponentDocument.md).
