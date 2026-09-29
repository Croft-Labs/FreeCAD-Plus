# FreeCAD upstream issue watchlist

Reviewed: 2026-09-29. Source: [FreeCAD/FreeCAD issues](https://github.com/FreeCAD/FreeCAD/issues).

Small, curated reference for basic reliability and FreeCAD Plus workflow work; not a complete issue export or a ranked upstream backlog. Only issue numbers, short summaries, and links are retained. Status reflects the GitHub pages reviewed and may change. These reports have not been reproduced in FreeCAD Plus; check the linked issue and our source revision before planning a fix.

## Open issues to watch

| Issue | Basic problem / relevance |
| --- | --- |
| [#29376](https://github.com/FreeCAD/FreeCAD/issues/29376) | Severe slowdown after 5–30 minutes of use; upstream high priority and confirmed. |
| [#28412](https://github.com/FreeCAD/FreeCAD/issues/28412) | Expanding/collapsing tree containers can select unintended objects; upstream high priority and confirmed. |
| [#32706](https://github.com/FreeCAD/FreeCAD/issues/32706) | Mirror using a face inside an Assembly can ignore the parent Body placement; awaiting confirmation. |
| [#27751](https://github.com/FreeCAD/FreeCAD/issues/27751) | Surface/Waterline CAM refactoring tracker; relevant to toolpath reliability and future indexed machining. |

## Closed issues worth retaining as regression references

Closed upstream does not establish whether a fix is included or validated in this fork.

| Issue | Basic problem to check when changing this area |
| --- | --- |
| [#18044](https://github.com/FreeCAD/FreeCAD/issues/18044) | Crash recovery can ignore recovery files when the project file is newer, even if corrupted. |
| [#32717](https://github.com/FreeCAD/FreeCAD/issues/32717) | Numeric fields can lose arrow/scroll changes when focus moves. |
| [#32718](https://github.com/FreeCAD/FreeCAD/issues/32718) | Task-dialog changes can fail to update the model, including Pad length. |
| [#32700](https://github.com/FreeCAD/FreeCAD/issues/32700) | Numeric fields can ignore document units; relevant to CAM stock entry. |
| [#32690](https://github.com/FreeCAD/FreeCAD/issues/32690) | CAM wire offsets can flip an arc and produce an incorrect offset shape. |
| [#10584](https://github.com/FreeCAD/FreeCAD/issues/10584) | CAM MillFace can ignore a chosen start point and generate the wrong approach. |

## Links for later review

- [Open blockers](https://github.com/FreeCAD/FreeCAD/issues?q=is%3Aissue%20is%3Aopen%20label%3ABlocker)
- [Open high-priority issues](https://github.com/FreeCAD/FreeCAD/issues?q=is%3Aissue%20is%3Aopen%20label%3A%22Priority%3A%20High%22)
- [Open Part Design issues](https://github.com/FreeCAD/FreeCAD/issues?q=is%3Aissue%20is%3Aopen%20label%3A%22Mod%3A%20Part%20Design%22)
- [Open CAM issues](https://github.com/FreeCAD/FreeCAD/issues?q=is%3Aissue%20is%3Aopen%20label%3A%22Mod%3A%20CAM%22)
- [Open topological-reference issues](https://github.com/FreeCAD/FreeCAD/issues?q=is%3Aissue%20is%3Aopen%20topological)

Keep this file short when refreshing it. Follow issue links for reproduction steps, discussions, attachments, and fixes rather than copying them here. Accepted FreeCAD Plus work belongs in [the development roadmap](DEVELOPMENT_ROADMAP.md).
