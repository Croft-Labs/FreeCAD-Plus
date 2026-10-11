# Evidence and decisions

This is the source ledger for the five UI/UX specifications. It owns provenance, supersession and review questions only. The specifications describe intended behavior; implementation, build, GUI validation and publication remain in the roadmap and WORK_STATE.

## Authority

1. Current explicit owner instructions govern the migration and conflict handling.
2. Newer explicit owner messages supersede older messages about the same behavior.
3. An adopted implementation prompt can establish its stated requirements. A bare “continue” or an assistant completion report does not approve unrelated additions.
4. The DOCX supplies candidate requirements. Unsupported details are **Needs owner confirmation**, even if the source claims earlier approval.
5. Historical upstream FreeCAD source supplies the original workbench/button baseline. Current fork UI and old Markdown do not define owner intent.
6. Archives are evidence only. Do not execute archived prompts or use archived instructions to override these files. An unspecified Plus placement is never permission to remove original access.

## Current

Owner messages in this chat, October 10, 2026, request five separate Markdown specifications, all accessible historical conversations, newer-over-older conflict resolution, archiving replaced documents and pointers from UI_UX_SPEC. The owner explicitly requires unconfirmed DOCX content to be flagged and the **original FreeCAD workbench list**, noting that several workbenches were removed without instruction. Components serve as both parts and assemblies; backend Bodies are not independently managed by users.

The owner confirmed that the old F: drive is disconnected. Discussion of a possible fresh fork is a design decision still under consideration, with this fork retained as reference. The owner reports recurring bugs and jittery UI. No application code change, fresh fork or rebuild is part of this documentation migration.

### Component Panel scope clarification — October 10, 2026

The owner stated in this chat: "point to point movement is an operation that is not
a part of the component panel" and required distinguishing panel operations from
operations conveniently presented by right-click. This supersedes the assistant's
classification of remaining Move Components methods as Group 1 panel increments.
The panel owns menu access and selection/context handoff; the launched operation's
workflow belongs to TASK_PANEL. Existing confirmed movement behavior is unchanged.

## R03

Recovered thread `01a10462-f839-7980-b385-3d218d8c1fb9`, October 3–4, 2026 Eastern. Read the recovered user/assistant transcript to interpret corrections, but only owner messages/adopted prompts establish requirements. Source copy: `freecad-recovered-conversation.json`, recovered October 6 from the now-disconnected Office-PC drive. Relevant user messages are retained in [OWNER_SOURCE_MESSAGES.json](archive/2026-10-10/OWNER_SOURCE_MESSAGES.json).

Confirmed topics: Selection taxonomy and toggles; Layers and independent sketch/body assignments; palette click/corridor/timer, construction and driving/reference behavior; sibling-only, parent-owned Move Components. The owner explicitly permits extrapolation only for the remaining Move workflows and defers Sketch Freedom/Constraint Repair, Interactive Feature Handles and Broken Reference Repair. The original adopted [prompts 1–10](../archive/pre-restart-docs/queue/2026-10-03-design-workload/README.md) are already archived in the repository. They are not a new work queue.

## C06

Thread **Complete recovery queue**, `01a10f79-1a93-7be0-a261-96a6b7e9c425`, October 6–7 Eastern. Direct messages confirm startup restoration and recent files; selected-plane-only highlighting; native palette icons/tooltips; the later six-group Modeling outline; gray dividers and uncut captions; larger medium icons; ordinary click/multiselection behavior; quiet uncommitted constraint checking; no lingering palette shadow; and the desired legacy conversion preserving editable features or recoverable dumb geometry. The later October 6 13:26 EDT outline overrides the 13:11 EDT outline.

## C09

Thread **freecad plus 1.0**, `01a120e8-8951-7b32-a7e4-3557c9a2ec40`, October 9 Eastern. Direct messages and the owner's pasted answers confirm domestic/external storage, nested imported-file lists, qualified names, independent copies, source-file editing and cycle prevention; pinned file container and ordinary Part001; Edit semantics and component tabs; active styling and at-least-75% contextual transparency; and temporary unused-model editing. Add Component changes remain deferred.

## C10

Thread **Fix component activation and part**, `01a12645-26b9-7d32-b338-529e73a9c0d4`, October 10 Eastern. Direct messages confirm double-click activation, Part Type replacing Part View, Excluded replacing ambiguous Hidden, saved parent-owned direct-child settings, context-dependent Reference and mandatory Add Reference Feature before use. The October 10 10:56 EDT clarification forbids directly using unpromoted Reference geometry and supersedes that earlier suggestion.

## Source coverage and limitations

- Read all locally available primary FreeCAD Codex session user messages identified by checkout and topic, including recent recovery, hierarchy and Part Type chats. Excluded automated subagent records and unrelated app conversations from requirement evidence.
- Both archived Codex and archived ChatGPT listing calls returned no entries. The app's recent-chat listing exposed one additional FreeCAD ChatGPT conversation, **Create FreeCAD Geometry**; it concerned a SpaceMouse file conversion, not FreeCAD Plus interface requirements. It supplied no additional UI specification.
- Reviewed the saved October 3–4 recovered transcript and original workload prompts. The old F: drive is disconnected; older chats and October 2 screenshot attachments could not be audited. The available recent ChatGPT listing is not a full searchable account export. **This is not a claim that every historical ChatGPT or old-computer conversation has been recovered.**
- Read the current owner-moved DOCX from ui-ux-specs. It contains 2,911 body blocks and no embedded media. The archived original is unchanged. Every body block has a destination/status in [docx-coverage.json](archive/2026-10-10/docx-coverage.json); the full [source text](archive/2026-10-10/DOCX_SOURCE_TEXT.md) is archival, not a second specification.
- The old TOOLBARS.md was used only as a name/ID locator, checked against historical upstream source. Its Plus placements, implementation claims and policy were not adopted. Original descriptions come from source resources; explicitly unresolved option descriptions remain labeled.
- Baseline revision b9609745048b was read from Git, including original workbench registrations and command resources. Optional build availability is not the same as owner-approved removal. No separately installed FreeCAD was used.

## Conflicts resolved

| Older statement | Governing decision | Specification |
| --- | --- | --- |
| Permanent master Part001 pinned first | File is pinned; Part001 is ordinary and removable | COMPONENT_PANEL |
| Single-level external file list | Nested imported-file groups | COMPONENT_PANEL |
| Same-name domestic override of external definition | Qualified, distinct definitions | COMPONENT_PANEL |
| Edit opens another component tab | Edit stays in current tab; Open in new window opens a tab | COMPONENT_PANEL |
| Permanent unused models at top level | Temporary unused-model entry only while editing | COMPONENT_PANEL |
| Part View / Hidden display role | Part Type / Excluded, separate from visibility | COMPONENT_PANEL |
| Reference is directly usable while visible | Add Reference Feature is mandatory first | COMPONENT_PANEL |
| Movement includes Copy or child-local/global frame selector | Copy/Paste separately; sibling movement relative to immediate parent | TASK_PANEL |
| Palette five-second fixed timeout | One second outside corridor; unlimited time inside | MODEL_VIEW_WINDOW |
| Persistence makes plain clicks accumulate | Ctrl/Shift multiselect; plain click replaces | MODEL_VIEW_WINDOW |
| Modeling Edit/Attach medium cluster | Latest October 6 small cluster, including Coordinate System | TOOLBARS_AND_BUTTONS |
| Delete Face in Dress-Up | Latest October 6 Other group | TOOLBARS_AND_BUTTONS |
| Missing/disabled buttons or workbenches imply removal | Original workbench coverage retained; omissions require owner instruction | TOOLBARS_AND_BUTTONS |
| DOCX must remain the active UI authority | Five Markdown files are now authoritative | UI_UX_SPEC / AGENTS |

## Questions retained for owner review

- Confirm older UI defaults and screenshot values: theme, navigation, units, colors, grid, exact icon/button dimensions, dock split and naming beyond confirmed Part001.
- Confirm all Plus modes and Home/Sketch/Surface/Assembly/Mesh/View placements. Drafting/Drawing is distinct from the legacy Draft workbench.
- Resolve the exact Pipe placement and the Tab primitive workflow. The later Modeling outline omits Pipe but explicitly includes Tab; implementation gaps do not settle either requirement.
- Confirm create/edit fields and limits for Extrude, Revolve, Loft, Pipe, Helix, Primitive and Pattern; preserve unconfirmed alternatives without claiming current engine limitations are owner decisions.
- Confirm remaining component context menus, grouped instances, History ordering/suppression and deletion/relationship details that were only found in the DOCX or old technical documents.
- Define the deferred Add Component and Add Reference Feature interactions before implementation.
- Revisit the unconfirmed custom Trim Body, Isocline, CAM and other old Markdown-only interactions if older primary messages become available. Their archived detail is not discarded or approved by this migration.

## Archive and migration checks

The source DOCX, old TOOLBARS.md and former UI_UX_SPEC.md are archived unchanged. Redundant UI passages in technical documents are archived before removal; technical persistence, geometry and validation evidence remain in their owning documents. The icon assets already moved by the owner remain alongside the new toolbar specification. No new DOCX is authored, so a DOCX render/edit gate is not applicable; archived source bytes are hash-checked.

## Owner-message index

Times below are Eastern (UTC−04:00 for these dates). Full text is in the source-message archive.

| Source message | Time | Topic opening |
| --- | --- | --- |
| U001 / R03 | 2026-10-03 20:49:20 | Do not start any work yet. I want to work through a few features that you can do and hash out all of the details, and once we |
| U002 / R03 | 2026-10-03 20:55:55 | For the purposes of the selection toolbar, I would say that surfaces are sheets not associated with bodies, and faces are the |
| U003 / R03 | 2026-10-03 20:59:06 | Directional selection and persistent selection should both default to on. For the single connected tangent curves, I guess it |
| U004 / R03 | 2026-10-03 21:00:15 | Does FreeCAD implement layers? |
| U005 / R03 | 2026-10-03 21:02:33 | Yes, I want to implement a layer system for the design mode. We can have a toolbar for it in the top toolbar as well that onl |
| U006 / R03 | 2026-10-03 21:09:51 | With regard to your suggestions, I would say that something like the work layer should be renamed to something like the base  |
| U007 / R03 | 2026-10-03 21:15:17 | Your rule does not fully capture my intent. My thought is that a single object cannot be split between multiple layers. So a  |
| U008 / R03 | 2026-10-03 21:16:43 | What other extremely high utility features were outlined in the development roadmap? |
| U009 / R03 | 2026-10-03 21:20:54 | Here are the items that I want to set in the current workload queue: the contextual constraint palette, the precise move, cop |
| U010 / R03 | 2026-10-03 21:24:39 | I suggest having it appear when an object is clicked. However, it can be relatively easy to make disappear, either by moving  |
| U011 / R03 | 2026-10-03 21:30:18 | I would say that the timer should actually be one second if it travels outside of a small travel corridor. I would also say t |
| U012 / R03 | 2026-10-03 21:34:35 | If the pointer is too close to the boundary of the viewport, you may move it to wherever is needed to stay within the viewpor |
| U013 / R03 | 2026-10-03 21:36:17 | With regard to if make driving produces an invalid sketch, I would say just keep it as invalid and the user can either click  |
| U014 / R03 | 2026-10-03 21:39:25 | The move feature should only refer to whole components, which would include all of its child components as well. If the user  |
| U015 / R03 | 2026-10-03 21:43:52 | I would actually say that creating a copy causes issues here. If a user wants to create a copy, they can do a copy and paste  |
| U016 / R03 | 2026-10-03 21:45:47 | Translate should always be a vector and a distance. The vector can be local axes, global axes, or something like an edge or a |
| U017 / R03 | 2026-10-03 21:49:42 | I would say we should actually do away with the local axes. I think since a part or component belongs to the next higher asse |
| U018 / R03 | 2026-10-03 21:54:11 | Before we go there, do you get what I mean by the parent owns the location of a component within its assembly? Because if you |
| U019 / R03 | 2026-10-03 21:56:19 | Is this now done for movement? What feature groups have we completed? What feature groups still need to be defined and outlin |
| U020 / R03 | 2026-10-03 21:59:47 | I need to go to sleep, so I want you to create a queue of prompts, making it as many prompts as needed, especially for the Mo |
| U021 / R03 | 2026-10-03 22:11:15 | Implement the owner-defined Selection toolbar for FreeCAD Plus Design mode. This is prompt 1 of 10 in the owner's explicitly  |
| U022 / R03 | 2026-10-03 22:27:25 | Implement the owner-defined Design Layers system, task panel and toolbar. This is prompt 2 of 10 in the authorized sequential |
| U023 / R03 | 2026-10-04 07:35:14 | Implement the fully specified Contextual Constraint Palette in FreeCAD Plus. This is prompt 3 of 10 in the authorized sequent |
| U024 / R03 | 2026-10-04 08:21:40 | continue this task if it wasnt completed: Implement the owner-defined Design Layers system, task panel and toolbar. This is p |
| U025 / R03 | 2026-10-04 08:23:47 | Implement the Move Components task foundation and Translate workflow. This is prompt 4 of 10 in the owner's sequential worklo |
| U026 / R03 | 2026-10-04 08:39:32 | Implement Rotate in the same Move Components task panel established by prompt 4. This is prompt 5 of 10. Read that prompt's b |
| U027 / C06 | 2026-10-06 00:29:23 | Run the recovered FreeCAD Plus unfinished-work queue sequentially to completion in this conversation. The owner authorizes th |
| U028 / C06 | 2026-10-06 08:03:42 | The owner requires the recovery workload to appear as separate prompts, rather than one omnibus prompt. This supersedes the o |
| U029 / C06 | 2026-10-06 08:10:41 |  # Files pasted by the user: ## "Implement Align Axes in the shared Move Components task panel. This is recovery…": C:\Users\ |
| U030 / C06 | 2026-10-06 08:13:18 |  # Files pasted by the user: ## "Implement Align Coordinate Systems in the existing Move Components task panel. …": C:\Users\ |
| U031 / C06 | 2026-10-06 08:15:55 |  # Files pasted by the user: ## "Implement Interactive movement and the movable pivot in the SAME Move Component…": C:\Users\ |
| U032 / C06 | 2026-10-06 08:18:15 |  # Files pasted by the user: ## "Recovery item 6 of 7: Reconcile all four feature groups before the grouped test…": C:\Users\ |
| U033 / C06 | 2026-10-06 08:22:26 |  # Files pasted by the user: ## "Recovery item 7 of 7: Create and deliver the requested FreeCAD Plus test build …": C:\Users\ |
| U034 / C06 | 2026-10-06 10:21:52 | you have many changes that are note committed. group them into logical commits and then push them to github  |
| U035 / C06 | 2026-10-06 10:28:33 | if a build doesnt exist, create one now and place the shortcut for it on the desktop  |
| U036 / C06 | 2026-10-06 10:59:29 | fix the startup. it takes a long time to load, shows the old dark UI, then changes, then changes again but doesnt have the st |
| U037 / C06 | 2026-10-06 12:09:17 | when creating a new sketch, i clicked the xy plane but all highlighted. make it such that only the selected plane highlights  |
| U038 / C06 | 2026-10-06 12:37:11 | when editing a sketch, the constraint palette shows buttons with words on them. replace the buttons with the icons from the t |
| U039 / C06 | 2026-10-06 12:56:35 | it looks like you are putting validation files in the main project folder. move them here and delete them each time after you |
| U040 / C06 | 2026-10-06 13:11:02 | update section "2.1.2.1 Design Mode" toolbar outline. Make the document accurate to the current configuration. format as foll |
| U041 / C06 | 2026-10-06 13:26:05 | update the tabbed toolbars to have gray vertical line dividers between the groups on each tab. make text two lines when neces |
| U042 / C06 | 2026-10-06 14:05:45 | two issues while editing a sketch: #1: clicking one point then another without pressing shift of ctrl highlights both. it sho |
| U043 / C06 | 2026-10-06 16:35:07 | also make the medium sized buttons for the tabbed toolbars larger. it seems like you took out the text but didnt resize the i |
| U044 / C06 | 2026-10-06 16:58:42 | When I make a selection to the constraint pallet while editing A Sketch it seems like the top Shadow or at least just a gray  |
| U045 / C06 | 2026-10-06 17:10:56 | What is the current state for opening Legacy free CAD files and having them be converted to the new CAD part files? Is it fun |
| U046 / C06 | 2026-10-06 17:17:49 | It seems like you just have the ability to retain a body, but there are sort of several functional changes that wouldn't be t |
| U047 / C06 | 2026-10-06 17:21:05 | Create an outline of how to break this up into several smaller tasks. My assumption is that in the Components panel, moving a |
| U048 / C06 | 2026-10-06 17:25:13 | I should also note your error handling portion of it. My intuition says that your preservation of legacy features is a good w |
| U049 / C06 | 2026-10-06 17:56:00 | Note that only the UX and UI elements are meant to be stored in the docx document so that I can edit it. Everything else shou |
| U050 / C09 | 2026-10-09 09:44:36 | So there is a conflict of file structure that has arisen because we've been trying to implement both FreeCAD's traditional fi |
| U051 / C09 | 2026-10-09 09:50:57 | For your first question, I would say that they should have an option to import and store it within an externally stored compo |
| U052 / C09 | 2026-10-09 09:56:09 | Yes, I would say that adding a file qualification is necessary. However, I wouldn't put current file M3 screw. I would just s |
| U053 / C09 | 2026-10-09 10:01:21 | When copying an external component to the local file, in which we should really be calling them domestic components for compo |
| U054 / C09 | 2026-10-09 10:03:43 | Of course, the user can make the M3 screw the active component of what would technically be an external file, add a component |
| U055 / C09 | 2026-10-09 10:04:47 | Create an action plan, set of tasks, in order to implement this new file structure hierarchy. Do not begin implementing the p |
| U056 / C09 | 2026-10-09 10:13:46 | ask a me for permission to do all necessary actions. I will approve and you will then have every permission needed  |
| U057 / C09 | 2026-10-09 10:14:05 | <send_user_message_question_reply> [{"questionItemId":"[\"request_user_input_async\",\"call_33b1ca10ff0b478a8dcf4715ce6da512\ |
| U058 / C09 | 2026-10-09 10:17:02 | reboot/re-initialize/whatever is need so that the sandbox error goes away and I dont have to keep approving things  |
| U059 / C09 | 2026-10-09 14:37:58 | what is the current status of the structure conversion? how many tasks are left?  |
| U060 / C09 | 2026-10-09 14:49:07 | there are still more cascading issues that now arise from the new file structure to address: - when creating a new document,  |
| U061 / C09 | 2026-10-09 14:52:29 | When creating a document, should Part001 become active automatically? - Recommended: Create a domestic definition named Part0 |
| U062 / C09 | 2026-10-09 15:00:28 | first we need to clarify the meaning of edit and active component. For the sake of the UI, we will use the term edit. However |
| U063 / C09 | 2026-10-09 15:04:17 | If a component has several occurrences in the Part Tree, which should be highlighted? - Recommended: All occurrences of the e |
| U064 / C09 | 2026-10-09 15:12:06 | Does “75% transparent” mean a fixed transparency or additional fading? - Recommended: Non-active geometry is at least 75% tra |
| U065 / C09 | 2026-10-09 15:15:08 | How should the temporary tree item appear and behave? - Recommended: Label it Component name (unused model), retain external- |
| U066 / C09 | 2026-10-09 15:18:56 | we will still defer the changes to the "add component" workflow. begin work on implementing the new active component and part |
| U067 / C10 | 2026-10-10 10:43:57 | we need to fix some features of freecad plus. do not start work yet. add clarification questions of the following if necessar |
| U068 / C10 | 2026-10-10 10:52:16 | Reference geometry: Should Reference parts be visible and selectable for sketches, attachments and other modeling references, |
| U069 / C10 | 2026-10-10 10:56:24 | One point remains: for this change, should Reference children contribute nothing to the active part’s final geometry and expo |
| U070 / CURRENT | 2026-10-10 15:57:37 | I am finding that you are making changes to previously specified and defined UI and workflow features, despite the "FreeCAD P |
| U071 / CURRENT | 2026-10-10 15:59:47 | Conversation sources: Should I include all FreeCAD-related Codex and ChatGPT conversations, including archived chats and any  |

## Archived source fingerprints

| Source | SHA-256 |
| --- | --- |
| FreeCAD Plus UI & UX.docx | `428a89d39c3345cf0c788ff3476b0c775f90ddc0ba3be40e3b33c772a5213919` |
| TOOLBARS.md | `e4ecd3b016d2babb6760262633d8f737b24c1d24b75ba4c1b7e35f647a19ff14` |
| UI_UX_SPEC.md | `2d07c418af727f2dbf6a1ef02f23114cb604896b2e5963e6a3980383968eb7d7` |

## Unverified implementation inventory

At the owner's October 10 request, [UNVERIFIED_IMPLEMENTED_CHANGES.md](UNVERIFIED_IMPLEMENTED_CHANGES.md) segregates source-backed additions and details without established approval: all 56 numbered archived custom screens, 24 component/document choices, 13 interface-integration topics, and an index of all 223 transferred DOCX candidates. Source existence is not approval or current runtime acceptance. Confirmed goals are not demoted by overlapping entries; missing owner evidence remains unresolved.

## Clean baseline transition — October 10

The owner requested a clean checkout of the latest stable official FreeCAD source. Official releases/latest resolved to 1.1.4; 26.3 RC1 is a prerelease. The active source now starts at 4fd3bf320d9566a27e60069fc8387448aaa3a094. Requirements and confirmation statuses are unchanged. The original command inventory still records its stated historical source revision; it is not silently regenerated from the new baseline. Implementation links refer to the preserved old fork, and old technical/roadmap documents are historical.
