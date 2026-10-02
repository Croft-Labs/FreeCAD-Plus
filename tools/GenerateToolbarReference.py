# SPDX-License-Identifier: LGPL-2.1-or-later
"""Generate the icon-backed toolbar reference from exported native metadata.

Usage: python tools/GenerateToolbarReference.py <inventory.json> [upstream-ref]
The upstream ref is a recorded local source snapshot, not a network refresh.
"""
import ast
import html
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ai-instructions/details/ui/TOOLBARS.md"
ASSETS = OUT.parent / "toolbar-icons"
inventory_path = Path(sys.argv[1])
data = json.loads(inventory_path.read_text(encoding="utf-8"))
pending_native = {"PartDesign_CircularPattern", "PartDesign_PathPattern", "PartDesign_PointPattern"} - {
    name for name, actions in data["commands"].items() if actions}
pattern_bindings_status = (
    "Those three bindings remain pending native rebuild/GUI validation in the inspected executable. "
    if pending_native else "The inspected executable registers all three restored native bindings. "
)
REF = sys.argv[2] if len(sys.argv) > 2 else "upstream/main"
def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8")
upstream = git("rev-parse", REF).strip()
fork = git("rev-parse", "HEAD").strip()
def stock(path):
    return git("show", f"{upstream}:{path}")
def clean(text):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]*>", " ", text))).replace("&", "").strip()
def cell(text):
    return text.replace("|", "\\|").replace("\n", " ")
def body(text, start):
    begin = text.index("{", start)
    depth = 1
    i = begin + 1
    while depth:
        if text[i] == "{": depth += 1
        elif text[i] == "}": depth -= 1
        i += 1
    return text[begin + 1:i - 1]
def uncomment(text):
    return re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.S)
def cpp_groups(text, class_name="Workbench", helpers=""):
    text = uncomment(text)
    helpers = uncomment(helpers)
    match = re.search(r"\b" + class_name + r"::setupToolBars\(\) const", text)
    if not match: return {}
    section = body(text, match.end())
    definitions = text + "\n" + helpers
    def commands(chunk, seen=()):
        found = re.findall(r'<<\s*"([A-Za-z][A-Za-z0-9_]*)"', chunk)
        for call in re.finditer(r"\b((?:addSketcherWorkbench|SketcherAddWorkbench)\w+)\s*\(", chunk):
            name = call[1]
            if name in seen: continue
            candidates = list(re.finditer(r"\b" + name + r"(?:<[^>]+>)?\([^;{}]*\)\s*\{", definitions))
            selected = next((m for m in candidates if "ToolBarItem" in m[0]), None)
            selected = selected or next((m for m in candidates if "T&" in m[0]), None)
            if selected:
                found.extend(commands(body(definitions, selected.end() - 1), seen + (name,)))
        return found
    groups = {}
    matches = list(re.finditer(r'(\w+)->setCommand\("([^"\n]+)"\);', section))
    for i, match in enumerate(matches):
        chunk = section[match.end():matches[i+1].start() if i+1 < len(matches) else len(section)]
        groups[match[2]] = commands(chunk)
    return groups

standard = cpp_groups(stock("src/Gui/Workbench.cpp"), "StdWorkbench")
standard["Structure"].insert(standard["Structure"].index("Std_Group"), "Part_Datums")
standard["View"].insert(standard["View"].index("Std_DrawStyle")+1, "Part_SelectFilter")
helpers = stock("src/Mod/Sketcher/Gui/Workbench.cpp")
modules = {"PartDesignWorkbench": "PartDesign", "SketcherWorkbench": "Sketcher",
           "PartWorkbench": "Part", "SurfaceWorkbench": "Surface", "MeshWorkbench": "Mesh",
           "TechDrawWorkbench": "TechDraw", "SpreadsheetWorkbench": "Spreadsheet",
           "MaterialWorkbench": "Material", "FemWorkbench": "Fem", "PointsWorkbench": "Points",
           "MeshPartWorkbench": "MeshPart", "RobotWorkbench": "Robot",
           "ReverseEngineeringWorkbench": "ReverseEngineering", "InspectionWorkbench": "Inspection"}
STANDARD = set(standard)
baselines = {}
for name, module in modules.items():
    baselines[name] = cpp_groups(stock(f"src/Mod/{module}/Gui/Workbench.cpp"), helpers=helpers)
    if name == "PartDesignWorkbench" and pending_native:
        local = cpp_groups((ROOT / f"src/Mod/{module}/Gui/Workbench.cpp").read_text(encoding="utf-8"),helpers=helpers)
        data["workbenches"][name]["classic"].update(local)
        data["workbenches"][name]["plus"]["Modeling"] = [(k,local[k]) for k in (
            "Part Design Modeling Features","Part Design Transformation Features",
            "Part Design Dress-Up Features","Part Design Helper Features")]
    if name not in data["workbenches"]:
        path = ROOT / f"src/Mod/{module}/Gui/Workbench.cpp"
        local = cpp_groups(path.read_text(encoding="utf-8"), helpers=helpers)
        data["workbenches"][name] = {"label": "FEM" if module == "Fem" else module,
            "classic": {**standard, **local}, "plus": {"Tools": list(local.items())},
            "source_only": True}
for name, entry in data["workbenches"].items():
    if name in baselines: continue
    groups = {key: list(values) for key, values in entry.get("classic", {}).items() if key not in STANDARD}
    if name == "CAMWorkbench":
        groups["Project Setup"] = [c for c in groups["Project Setup"]
            if c not in ("CAM_MeshPreparation", "CAM_HoldingTab", "CAM_IndexedSetup")]
        groups["New Operations"] = [c for c in groups["New Operations"] if c != "CAM_PlanarSurface"]
    baselines[name] = groups

# Sketcher toolbar definitions are identical in the fork; only its menus differ.
# Preserve the actual default constraint/geometry preference branches, rather
# than displaying the union of mutually exclusive C++ branches as one toolbar.
baselines["SketcherWorkbench"] = {k:v for k,v in data["workbenches"]["SketcherWorkbench"]["classic"].items() if k not in STANDARD}

def python_groups(text):
    """Resolve literal builtin lists; do not import or run addon discovery."""
    tree = ast.parse(text)
    values = {}
    def value(node):
        if isinstance(node, ast.Constant): return node.value
        if isinstance(node, (ast.List, ast.Tuple)): return [value(n) for n in node.elts]
        if isinstance(node, ast.Name): return values.get(node.id)
        if isinstance(node, ast.Attribute): return values.get(node.attr)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "get_draft_snap_commands":
            snap_tree = ast.parse(stock("src/Mod/Draft/draftutils/init_tools.py"))
            function = next(n for n in snap_tree.body if isinstance(n,ast.FunctionDef) and n.name=="get_draft_snap_commands")
            return ast.literal_eval(next(n.value for n in function.body if isinstance(n,ast.Return)))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "QT_TRANSLATE_NOOP": return value(node.args[-1])
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            a,b = value(node.left),value(node.right)
            return a+b if isinstance(a,list) and isinstance(b,list) else None
    groups = {}
    for node in sorted(ast.walk(tree), key=lambda n:(getattr(n,"lineno",0),getattr(n,"col_offset",0))):
        if isinstance(node, ast.Assign):
            resolved = value(node.value)
            for target in node.targets:
                key = target.id if isinstance(target, ast.Name) else target.attr if isinstance(target,ast.Attribute) else None
                if key and resolved is not None: values[key] = resolved
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "appendToolbar":
            title,commands = value(node.args[0]),value(node.args[1])
            if isinstance(title,str) and isinstance(commands,list): groups[title] = commands
    if "OpenSCAD Tools" in groups:
        for node in ast.walk(tree):
            if (isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=="extend"
                    and isinstance(node.func.value,ast.Name) and node.func.value.id=="toolbarcommands"):
                groups["OpenSCAD Tools"].extend(ast.literal_eval(node.args[0]))
    return groups
for module in ("BIM", "OpenSCAD"):
    groups = python_groups(stock(f"src/Mod/{module}/InitGui.py"))
    name = module+"Workbench"
    baselines[name] = groups
    data["workbenches"][name] = {"label": module, "classic": {**standard,**groups},
        "plus": {"Tools": list(groups.items())}, "source_only": True}

# Read source-only descriptions without importing disabled workbench modules.
source_resources = {}
source_choices = {}
for path in (ROOT / "src").rglob("*.py"):
    if "Resources" in path.parts or "Test" in path.name: continue
    try: tree = ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeError): continue
    classes = {}
    def literal(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, str): return node.value
        if isinstance(node, ast.Call):
            values = [literal(arg) for arg in node.args]
            return next((v for v in reversed(values) if v), "")
        return ""
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            resources = {}
            variables = {}
            for sub in ast.walk(node):
                if isinstance(sub, ast.Assign):
                    for target in sub.targets:
                        if isinstance(target, ast.Name): variables[target.id] = variables.get(sub.value.id,"") if isinstance(sub.value,ast.Name) else literal(sub.value)
                        if isinstance(target, ast.Attribute) and target.attr in ("menutext", "tooltip", "icon", "pixmap"):
                            resources[{"menutext":"MenuText", "tooltip":"ToolTip", "icon":"Pixmap", "pixmap":"Pixmap"}[target.attr]] = literal(sub.value)
                        if isinstance(target,ast.Subscript) and literal(target.slice) in ("MenuText","ToolTip","Pixmap"):
                            resources[literal(target.slice)] = literal(sub.value)
                        if isinstance(target,ast.Attribute) and target.attr=="commands" and isinstance(sub.value,(ast.List,ast.Tuple)):
                            resources["choices"] = [literal(n) for n in sub.value.elts]
                if isinstance(sub,ast.FunctionDef) and sub.name=="GetCommands":
                    returned = next((n.value for n in sub.body if isinstance(n,ast.Return)),None)
                    if isinstance(returned,(ast.Tuple,ast.List)):
                        resources["choices"] = [literal(n) for n in returned.elts]
            for sub in ast.walk(node):
                if isinstance(sub, ast.Dict):
                    for key, value in zip(sub.keys, sub.values):
                        if literal(key) in ("MenuText", "ToolTip", "Pixmap", "Icon"):
                            resolved = variables.get(value.id, "") if isinstance(value,ast.Name) else literal(value)
                            if resolved: resources["Pixmap" if literal(key)=="Icon" else literal(key)] = resolved
            classes[node.name] = resources
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "addCommand" and len(node.args) >= 2):
            name = literal(node.args[0])
            obj = node.args[1]
            if name and isinstance(obj, ast.Call) and isinstance(obj.func, ast.Name):
                source_resources[name] = classes.get(obj.func.id, {})
    for classname, res in classes.items():
        if path.parts[-2] == "femcommands" and classname.startswith("_"):
            source_resources.setdefault("FEM"+classname, res)
for name,res in source_resources.items():
    if res.get("choices"): source_choices[name] = [c for c in res["choices"] if c]
source_resources["BIM_Trimex"] = dict(source_resources["Draft_Trimex"])

# Native constructors supply descriptions for disabled C++ workbenches and
# upstream pattern commands that are no longer registered in the fork binary.
for path in (ROOT / "src").rglob("Command*.cpp"):
    text = path.read_text(encoding="utf-8")
    for match in re.finditer(r':\s*(?:Group)?Command\("([^"]+)"\)\s*\{',text):
        chunk = body(text,match.end()-1)
        res = {}
        for field,key in (("sMenuText","MenuText"),("sToolTipText","ToolTip"),("sPixmap","Pixmap")):
            assigned = re.search(r'\b'+field+r'\s*=\s*(.*?);',chunk,re.S)
            if assigned:
                expr = assigned[1]
                strings = re.findall(r'"((?:[^"\\]|\\.)*)"',expr)
                if "QT_TRANSLATE_NOOP" in expr: strings = strings[1:]
                res[key] = "".join(strings).replace("\\n"," ")
        source_resources.setdefault(match[1], res)
        if "Comp" in match[1]:
            constructor = text[max(0,match.start()-120):match.start()]
            cls = re.search(r'(\w+)::\1\(\)\s*$',constructor)
            if cls:
                activation = re.search(r'\b'+cls[1]+r'::activated\([^)]*\)',text)
                if activation:
                    source_choices[match[1]] = re.findall(r'runCommandByName\("([^"]+)"\)',body(text,activation.end()))

# Commands present in recorded upstream but removed from current constructors.
upstream_command = stock("src/Mod/PartDesign/Gui/Command.cpp")
for name in ("PartDesign_CircularPattern", "PartDesign_PathPattern", "PartDesign_PointPattern"):
    match = re.search(r':\s*Command\("'+name+r'"\)\s*\{',upstream_command)
    if match:
        chunk = body(upstream_command,match.end()-1)
        res = {}
        for field,key in (("sMenuText","MenuText"),("sToolTipText","ToolTip"),("sPixmap","Pixmap")):
            assigned = re.search(r'\b'+field+r'\s*=\s*(.*?);',chunk,re.S)
            if assigned:
                expr=assigned[1]
                strings=re.findall(r'"((?:[^"\\]|\\.)*)"',expr)
                if "QT_TRANSLATE_NOOP" in expr: strings=strings[1:]
                res[key]="".join(strings).replace("\\n"," ")
        source_resources[name]=res
svg_index = {}
for path in (ROOT / "src").rglob("*.svg"):
    svg_index.setdefault(path.stem, path)

# Keep the executable projection definitions authoritative, without importing GUI.
ribbon_tree = ast.parse((ROOT / "src/Gui/PlusRibbon.py").read_text(encoding="utf-8"))
constants = {}
def constant(node):
    if isinstance(node,ast.Name): return constants[node.id]
    if isinstance(node,ast.Tuple): return tuple(constant(n) for n in node.elts)
    if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Add): return constant(node.left)+constant(node.right)
    return ast.literal_eval(node)
for node in ribbon_tree.body:
    if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name):
        key = node.targets[0].id
        if key in ("PRIMARY_COMMANDS", "DIMENSION_CHOICES", "COMMAND_FAMILIES", "ICON_FALLBACKS", "COLLAPSED_GROUPS"):
            constants[key] = constant(node.value)
primary = constants["PRIMARY_COMMANDS"]
families = constants["COMMAND_FAMILIES"]
catalog = set()
used_icons = set()
ASSETS.mkdir(parents=True, exist_ok=True)
def action(name):
    native = data["commands"].get(name, [])
    if native: return native[0]
    res = source_resources.get(name, {})
    return {"text": res.get("MenuText") or name.removeprefix("FEM_").replace("_", " "),
            "status": res.get("ToolTip", ""), "icon": "", "pixmap": res.get("Pixmap", "")}
def icon_for(name, act=None):
    act = act or action(name)
    filename = act.get("icon", "")
    if filename:
        used_icons.add(filename)
        shutil.copyfile(inventory_path.parent / "icons" / filename, ASSETS / filename)
        return f"![{cell(clean(act['text']))}](toolbar-icons/{filename})"
    fallback = constants["ICON_FALLBACKS"].get(name, "preferences-general.svg") if data["commands"].get(name) else ""
    pixmap = Path(act.get("pixmap", "") or fallback).stem or name
    path = svg_index.get(pixmap) or svg_index.get(name)
    if path:
        import os
        return f"![{cell(clean(act['text']))}]({Path(os.path.relpath(path, OUT.parent)).as_posix()})"
    return "—"
def label(name):
    return {"Std_New": "New File", "Std_Part": "Add part", "Sketcher_Dimension": "Auto Dimension"}.get(name, clean(action(name)["text"]))
def button(name, classic=False):
    if name == "Separator": return " · "
    catalog.add(name)
    caption = {"Std_New":"New Document", "Std_Part":"New Part"}.get(name,label(name)) if classic else label(name)
    return f"{icon_for(name)} [{cell(caption)}](#button-{name.lower()})"
def projection(commands):
    result = []
    emitted = set()
    for name in commands:
        if name == "Separator": continue
        family = next((f for f in families if name in f[1]), None)
        root, choices = (family[0], family[2]) if family else (name, None)
        if root in emitted: continue
        emitted.add(root)
        # The actual renderer omits commands without registered QAction instances.
        result.append((root, choices))
    return result
def group_table(groups, plus=False, source_only=False):
    lines = ["| Section / toolbar group | Buttons in display order |", "| --- | --- |"]
    for title, names in groups:
        buttons = []
        if plus and title in constants["COLLAPSED_GROUPS"]:
            catalog.update(c for c in names if c != "Separator")
            buttons = [title + " dropdown → " + "; ".join(button(c) for c in names if c != "Separator")]
        elif plus:
            for name, choices in projection(names):
                if not source_only and not data["commands"].get(name): continue
                text = button(name) + (" **L**" if name in primary else " **S**")
                variants = choices or ([name] if len(data["commands"].get(name, [])) > 1 else [])
                if variants:
                    text += " **▼**"
                    if choices:
                        text += " {" + "; ".join(button(choice) for choice in choices) + "}"
                buttons.append(text)
        else:
            buttons = [button(name, True) for name in names]
        lines.append(f"| {cell(title)} | {'; '.join(buttons) if buttons else 'No operation buttons'} |")
    return lines + [""]

lines = ["# FreeCAD Plus toolbar governance and visual reference", "",
    "## Authority and maintenance", "",
    "This is the governing command-placement reference for Classic versus Plus toolbars. "
    "The [UI specification](../../UI_UX_SPEC.md#toolbar-ui-styles) owns shared interaction and sizing rules. "
    "Change this reference whenever a toolbar command, section, dropdown or caption changes; "
    "preserve command IDs and native action behavior. Do not silently remove a function when consolidating buttons.", "",
    "Common actions use large buttons (**L**); secondary actions use small icons (**S**) in three rows; "
    "related/rare variants use dropdowns (**▼**). Icons below identify commands; these Markdown tables show "
    "membership and order, not exact ribbon pixel layout. Plus and Classic are mutually exclusive. "
    "Default UI is Plus; explicit saved Classic choices remain valid.", "",
    f"Snapshot: 2026-10-02. Fork source `{fork[:12]}`; recorded upstream FreeCAD/main `{upstream[:12]}`. "
    "Upstream means that local source snapshot, not a claim that the remote has no later commits. "
    f"Native action metadata/icons were read from the fork executable at application source `{data['version'][7][:12]}`; "
    "Plus grouping/projection was read from current source. Build and acceptance status are recorded in "
    "[WORK_STATE](../../WORK_STATE.md). Runtime export is an inventory check, not functional acceptance of every command.", "",
    "For every toolbar change, review placement, native command identity, retained functionality, "
    "icon/caption, large/small/dropdown priority, enabled/checked states and accessibility. "
    "Record new implementations and build/acceptance status in the existing roadmap/WORK_STATE, "
    "rather than treating this catalog as a release record.", "",
    "Classic tables list upstream definitions, including context-dependent/edit-only groups. "
    "They do not claim all groups are visible simultaneously. Compound toolbar buttons keep native choices; "
    "the final catalog expands those choices. Separators are shown as dots.", "",
    "To refresh: run [ExportToolbarReference.FCMacro](../../../tools/ExportToolbarReference.FCMacro) with "
    "isolated preferences against this fork, then "
    "`python tools/GenerateToolbarReference.py <inventory.json> <recorded-upstream-ref>`. "
    "Review upstream-specific differences and source-only entries before accepting generated changes. "
    "PNG icons are native action renders of the existing FreeCAD artwork; original licensing remains in "
    "[LICENSE](../../../LICENSE) and the corresponding source resource folders.", "",
    "## Shared desktop toolbars", "", "### Classic upstream groups", ""]
lines += ["The shared list includes Part's upstream toolbar manipulator additions: "
    "Datums in Structure and the native selection filter in View, once PartGui is loaded. "
    "The Classic Workbench control is a selector, not an Assembly operation button.", ""]
lines += group_table(standard.items())
lines += ["### Changes in Plus", "",
    "- The Workbench selector is replaced visually by the mode dropdown (Design, Draft, CAM, etc.).",
    "- File adds Save As, Import and Export; New uses the document icon and caption **New File**, "
    "with the component-document workflow. Native command identity remains `Std_New`.",
    "- Edit adds Delete and Preferences. Clipboard remains its native section.",
    "- Home Structure uses Components, Add part, Group, Link Actions and Add Reference Object. "
    "The audit correction restores native Datums as one dropdown and Variable Set as a small button. "
    "Coordinate System/Datum Plane creation is also exposed through the idle component Tasks pane.",
    "- View and Individual Views move to the View tab; Display adds selection filters, toolbar menu, dock menu and status-bar toggle.",
    "- Help and Macro each use one compact dropdown; record, macro manager and direct execution retain native states. "
    "The audit correction restores Macro ribbon access.",
    "- Iconless native actions get a ribbon-only icon from existing artwork. Their native QAction icons, "
    "states and menu identities remain unchanged. Native compound-menu separators are omitted from button-choice lists.",
    "- Home common Tools adds Command Search, Measure and Mass Properties in Design. "
    "Workbenches retain their native menu/shortcut commands even where the ribbon omits a toolbar button.", "",
    "### Plus shared sections", ""]
design = data["workbenches"]["PartDesignWorkbench"]
lines += group_table(design["plus"]["Home"], True)
lines += ["**View tab** (shared projection of each active workbench's native View / Individual Views groups):", ""]
lines += group_table(design["plus"]["View"], True)
lines += ["## Workbench comparisons", "",
    "Design tabs are **Home → Modeling → Surface → Sketch → Mesh → View**. Part Design supplies Home/Modeling; "
    "Surface, Sketcher and Mesh supply their namesake tabs. Other registered modes use **Home → Tools → View**. "
    "Part is a separate mode with its native operation groups under Tools; it is not a separate Design tab.", ""]
order = ["PartDesignWorkbench", "PartWorkbench", "SketcherWorkbench", "SurfaceWorkbench", "MeshWorkbench",
    "DraftWorkbench", "AssemblyWorkbench", "CAMWorkbench", "TechDrawWorkbench", "FemWorkbench",
    "SpreadsheetWorkbench", "MaterialWorkbench", "MeshPartWorkbench", "PointsWorkbench", "RobotWorkbench",
    "ReverseEngineeringWorkbench", "InspectionWorkbench", "BIMWorkbench", "OpenSCADWorkbench", "TestWorkbench"]
for name in order:
    entry = data["workbenches"].get(name)
    if not entry: continue
    lines += [f"### {entry['label']} (`{name}`)", ""]
    module = modules.get(name)
    path = f"src/Mod/{module}/Gui/Workbench.cpp" if module else f"src/Mod/{name.removesuffix('Workbench').replace('Test', 'Test')}/InitGui.py"
    lines += [f"Definition: [`{path}`](../../../{path}). Shared Classic groups are listed once above.", ""]
    if entry.get("source_only"):
        lines += ["**Source-only / not packaged in the inspected build.** These toolbar definitions exist in source. "
            "When the workbench is installed and registered, its Plus mode uses shared Home/View and these native groups in Tools. "
            "No executable/icon-menu acceptance is claimed for this workbench.", ""]
    lines += ["#### Classic upstream toolbar groups", ""]
    baseline = baselines.get(name, {})
    lines += group_table(baseline.items())
    local = {k:v for k,v in entry.get("classic", {}).items() if k not in STANDARD}
    old = {c for cs in baseline.values() for c in cs if c != "Separator"}
    new = {c for cs in local.values() for c in cs if c != "Separator"}
    lines += ["#### Changes made / buttons consolidated or omitted", ""]
    if name == "PartDesignWorkbench":
        lines += [f"- {button('PartDesign_Pad')} + {button('PartDesign_Pocket')} → {button('PartDesign_Extrude')}. "
            "Add/Subtract is selected in the task pane; the component workflow also supports separate background solid results.",
            f"- {button('PartDesign_LinearPattern')}, {button('PartDesign_PolarPattern')}, "
            f"{button('PartDesign_CircularPattern')}, {button('PartDesign_PathPattern')}, {button('PartDesign_PointPattern')} "
            f"share {button('PartDesign_Pattern')} as the primary ribbon entry. "
            "The unified task offers linear/circular patterns; the dropdown adds native concentric Circular, Path and Point tasks. "
            f"The audit correction restores their upstream commands and view providers in source, without changing geometry. {pattern_bindings_status}"
            "Classic exposes their individual native buttons; Mirrored and MultiTransform remain separate buttons.",
            "- Additive/Subtractive Loft, Pipe and Helix each share one dropdown. Both variants remain selectable."]
    if name == "SketcherWorkbench":
        lines += ["- Dimension buttons are consolidated under large Auto Dimension, with vertical, horizontal, "
            "angle, radius, diameter, distance, radius/diameter, lock and Snell's-law choices. "
            "Native geometry/B-spline/constraint compound dropdowns remain native.",
            "- Sketch support review, reusable copy and constraint-repair review are menu additions, "
            "not new buttons in the upstream Sketcher toolbar groups."]
    if name == "CAMWorkbench":
        lines += ["- Project Setup adds Mesh Preparation, Holding Tabs and Indexed Setup.",
            "- New Operations exposes Parallel / Waterline (`CAM_PlanarSurface`) with OpenCAMLib. "
            "Stock upstream makes advanced 3D operations conditional; grouping can change when the advanced setting is enabled."]
    if name == "OpenSCADWorkbench":
        lines += ["- The final four OpenSCAD Tools choices (Add OpenSCAD Element, Mesh Boolean, Hull and Minkowski) "
            "require a configured external OpenSCAD executable. They are shown as conditional source choices."]
    if name == "BIMWorkbench":
        lines += ["- Optional Reinforcement addons replace Rebar with their own dropdown; other addon menus depend "
            "on installation. The lists below cover built-in commands, not an invented addon inventory."]
    added = sorted(new-old)
    removed = sorted(old-new)
    if added: lines += ["- Added to native toolbar definitions: " + "; ".join(button(c) for c in added) + "."]
    if removed and name != "PartDesignWorkbench": lines += ["- Removed from native toolbar definitions: " + "; ".join(button(c) for c in removed) + "."]
    if not added and not removed:
        lines += ["- No workbench-specific toolbar command removal found in the compared definitions; "
            "Plus changes presentation/routing and applies the shared Home/View rules above."]
    lines += ["", "#### Plus UI tabs and sections", ""]
    for tab, groups in entry.get("plus", {}).items():
        if tab in ("Home", "View"):
            lines += [f"**{tab}:** shared sections above" + ("; Home excludes the Design-only Sketch and Tools sections." if name not in ("PartDesignWorkbench",) and tab == "Home" else "."), ""]
            continue
        lines += [f"**{'Design → ' if name in ('PartDesignWorkbench','SketcherWorkbench','SurfaceWorkbench','MeshWorkbench') else entry['label']+' → '}{tab}**", ""]
        lines += group_table(groups, True, entry.get("source_only", False))
lines += ["### Other bundled and addon workbenches", "",
    "BIM and OpenSCAD are not registered in the inspected build. Their source-defined toolbars are listed below; "
    "when registered, Plus would project their workbench groups into Tools. 3D printing is an addon mode only "
    "when an installed workbench registers it; this checkout has no authoritative addon button inventory.", ""]
for module in ("BIM", "OpenSCAD"):
    text = stock(f"src/Mod/{module}/InitGui.py")
    if module == "BIM":
        names = re.findall(r't\d\s*=\s*QT_TRANSLATE_NOOP\("Workbench",\s*"([^"]+)"\)', text)
    else:
        names = re.findall(r'appendToolbar\(\s*QT_TRANSLATE_NOOP\("Workbench",\s*"([^"]+)"', text)
    lines += [f"**{module}:** " + "; ".join(names) + ". "
        f"See [native definition](../../../src/Mod/{module}/InitGui.py) for conditional button lists. "
        "No Plus-specific toolbar change is recorded for this workbench.", ""]
pending = list(catalog)
while pending:
    name = pending.pop()
    for choice in source_choices.get(name,[]):
        if choice not in catalog:
            catalog.add(choice)
            pending.append(choice)
lines += ["## Complete toolbar button/function catalog", "",
    "This catalog contains every command referenced by the Classic/Plus tables above, plus every "
    "native compound-button choice. A compound command's first action is its current/default choice; "
    "it may change after the user selects another choice. Menu-only fork additions are not relabeled "
    "as toolbar buttons. Descriptions come from native status/help text or source GetResources. "
    "Command IDs disambiguate identically named buttons.", ""]
for name in sorted(catalog):
    entries = data["commands"].get(name) or [action(name)]
    lines += [f'<a id="button-{name.lower()}"></a>', f"### {cell(label(name))} — `{name}`", "",
        "| Icon | Button / dropdown choice | Function |", "| --- | --- | --- |"]
    for entry in entries:
        if not any(entry.get(key) for key in ("text","status","tooltip","icon")):
            continue  # Native compound-menu separators are not operation buttons.
        description = clean(entry.get("status", "")) or clean(entry.get("tooltip", ""))
        if not description:
            description = "Source-only command; consult the linked workbench definition for its resource description."
        lines.append(f"| {icon_for(name, entry)} | {cell(clean(entry['text']))} | {cell(description)} |")
    if source_choices.get(name) and not data["commands"].get(name):
        lines.append("\nSource-defined dropdown choices: " + "; ".join(button(c) for c in source_choices[name]) + ".")
    lines += [""]
OUT.parent.mkdir(parents=True, exist_ok=True)
# A compact navigation index makes the large final catalog usable in Markdown.
index = ["## Navigation", "", "- [Shared desktop toolbars](#shared-desktop-toolbars)"]
for name in order:
    if name in data["workbenches"]:
        index.append(f"- [{data['workbenches'][name]['label']}](#workbench-{name.lower()})")
        heading = f"### {data['workbenches'][name]['label']} (`{name}`)"
        where = lines.index(heading)
        lines[where:where] = [f'<a id="workbench-{name.lower()}"></a>']
index += ["- [Complete button/function catalog](#complete-toolbar-buttonfunction-catalog)", ""]
where = lines.index("## Shared desktop toolbars")
lines[where:where] = index
OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
print(json.dumps({"file": str(OUT), "toolbar_commands": len(catalog), "icon_files": len(used_icons),
    "missing_descriptions": [n for n in sorted(catalog) if not (action(n).get("status") or action(n).get("tooltip"))],
    "empty_baseline_groups": {n:[g for g,c in gs.items() if not c] for n,gs in baselines.items() if any(not c for c in gs.values())}}, indent=2))
