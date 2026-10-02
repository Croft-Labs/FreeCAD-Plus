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
        if key in ("PRIMARY_COMMANDS", "DIMENSION_CHOICES", "COMMAND_FAMILIES", "ICON_FALLBACKS", "COLLAPSED_GROUPS", "COORDINATE_CHOICES", "COMMON_GROUPS", "HOME_GROUPS"):
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
        return f'<img src="toolbar-icons/{filename}" width="11" height="11" alt="{html.escape(clean(act["text"]), quote=True)}">'
    fallback = constants["ICON_FALLBACKS"].get(name, "preferences-general.svg") if data["commands"].get(name) else ""
    pixmap = Path(act.get("pixmap", "") or fallback).stem or name
    path = svg_index.get(pixmap) or svg_index.get(name)
    if path:
        import os
        return f'<img src="{Path(os.path.relpath(path, OUT.parent)).as_posix()}" width="11" height="11" alt="{html.escape(clean(act["text"]), quote=True)}">'
    return "—"
def label(name):
    return {"Std_New": "New File", "Std_Part": "Add Component", "Std_Workbench": "Mode selector",
            "Part_Datums": "Datums", "Sketcher_Dimension": "Auto Dimension"}.get(name, clean(action(name)["text"]))
def button(name, classic=False):
    if name == "Separator": return " · "
    catalog.add(name)
    caption = {"Std_New":"New Document", "Std_Part":"New Part", "Std_Workbench":"Workbench selector"}.get(name,label(name)) if classic else label(name)
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

# Owner outline completed in the native-action projection; conditional modes retain source groups.
order = ["PartDesignWorkbench", "PartWorkbench", "SketcherWorkbench", "SurfaceWorkbench", "MeshWorkbench",
         "DraftWorkbench", "AssemblyWorkbench", "CAMWorkbench", "TechDrawWorkbench", "FemWorkbench",
         "SpreadsheetWorkbench", "MaterialWorkbench", "MeshPartWorkbench", "PointsWorkbench", "RobotWorkbench",
         "ReverseEngineeringWorkbench", "InspectionWorkbench", "BIMWorkbench", "OpenSCADWorkbench", "TestWorkbench"]
design = data["workbenches"]["PartDesignWorkbench"]
common = {"File": ["Std_New", "Std_Open", "Std_Save", "Std_SaveAs"],
          "Edit": ["Std_Undo", "Std_Redo", "Std_Refresh"],
          "Clipboard": ["Std_Cut", "Std_Copy", "Std_Paste"]}
coordinate_choices = ["Part_CoordinateSystem", "Part_DatumPlane", "Part_DatumLine", "Part_DatumPoint"]
home = {
    "Main": ["Std_NewComponent", "Std_Part", "PartDesign_NewSketch", "Part_CoordinateSystem"],
    "Modeling": ["PartDesign_Extrude", "PartDesign_Revolution", "PartDesign_Fillet", "PartDesign_Pattern"],
    "Surface": ["Surface_Filling", "Surface_GeomFillSurface", "Surface_ExtendFace"],
    "Sketch": ["Sketcher_EditSketch", "Sketcher_MapSketch", "Sketcher_CompLine",
               "Sketcher_CompCreateRectangles", "Sketcher_Dimension", "Sketcher_ToggleConstruction"],
    "Assembly": ["Assembly_CreateAssembly", "Assembly_Insert", "Assembly_SolveAssembly", "Assembly_CreateJointFixed"],
    "Mesh": ["Mesh_Import", "Mesh_FromPartShape", "Mesh_Evaluation"],
    "View": ["Std_ViewFitAll", "Std_ViewIsometric", "Std_DrawStyle", "Std_EntitySelectionFilter"],
    "Structure": ["Std_ComponentStructure", "Std_Group", "Std_LinkActions", "Std_VarSet", "PartDesign_AddReferenceObject"],
    "Utilities": ["Std_Import", "Std_Export", "Std_DlgPreferences", "Std_CommandSearch", "Std_Measure", "Std_MassProperties", "Std_Delete"],
    "Help": dict(design["plus"]["Home"])["Help"], "Macro": dict(design["plus"]["Home"])["Macro"]}
design_tabs = {"Home": list(home.items()), "Modeling": design["plus"]["Modeling"],
               "Surface": data["workbenches"]["SurfaceWorkbench"]["plus"]["Surface"],
               "Sketch": data["workbenches"]["SketcherWorkbench"]["plus"]["Sketch"],
               "Assembly": data["workbenches"]["AssemblyWorkbench"]["plus"]["Tools"],
               "Mesh": data["workbenches"]["MeshWorkbench"]["plus"]["Mesh"],
               "View": design["plus"]["View"]}

def choices_for(name, family_choices=None):
    if name == "Part_CoordinateSystem": return coordinate_choices
    if name == "Assembly_CreateJointFixed": return list(family_choices or [])
    return list(family_choices or source_choices.get(name, []))

def size_for(name, tab, group):
    if tab == "Common toolbar": return "Small"
    if group == "Main": return "Medium (half size)"
    if tab == "Home":
        if name in ("PartDesign_Extrude", "PartDesign_Revolution"): return "Full size"
        return "Medium (half size)" if group in dict(constants["HOME_GROUPS"]) or group == "Frequent operations" else "Small"
    return "Full size" if name in primary else "Small"

# Keep placement lookup independent of rendering, so Classic rows map to target.
placements = {}
def place(name, mode, tab):
    value = (mode, tab)
    if value not in placements.setdefault(name, []): placements[name].append(value)

for group, names in common.items():
    for name in names: place(name, "All", "Common toolbar")
for tab, groups in design_tabs.items():
    for group, names in groups:
        for name, family_choices in projection(names):
            place(name, "All" if tab == "View" else "Design", tab)
            for choice in choices_for(name, family_choices): place(choice, "All" if tab == "View" else "Design", tab)
place("PartDesign_Pad", "Design", "Home / Modeling → Extrude")
place("PartDesign_Pocket", "Design", "Home / Modeling → Extrude")
place("PartDesign_LinearPattern", "Design", "Home / Modeling → Pattern task")
place("PartDesign_PolarPattern", "Design", "Home / Modeling → Pattern task")
place("Part_Datums", "Design", "Home → Coordinate System dropdown")
place("Std_Workbench", "All", "Mode selector")
for name in order:
    if name in ("PartDesignWorkbench", "SketcherWorkbench", "SurfaceWorkbench", "MeshWorkbench"): continue
    entry = data["workbenches"].get(name)
    if not entry: continue
    for group, names in entry.get("plus", {}).get("Tools", []):
        for command, family_choices in projection(names):
            place(command, entry["label"], "Tools")
            for choice in choices_for(command, family_choices): place(choice, entry["label"], "Tools")

def mapping(name):
    values = placements.get(name, [])
    # Shared controls are specified once, independent of active workbench.
    if any(mode == "All" for mode, tab in values): values = [v for v in values if v[0] == "All"]
    if not values: return "Menus / shortcuts", "No dedicated ribbon button"
    return cell(" / ".join(dict.fromkeys(m for m,t in values))), cell("; ".join(dict.fromkeys(t for m,t in values)))

def classic_groups(groups):
    result = []
    for group, names in groups.items():
        result += [f"#### {group}", "", "| Command | Plus mode | Plus tab / location |", "| --- | --- | --- |"]
        for name in names:
            if name == "Separator": continue
            mode, tab = mapping(name)
            result.append(f"| {button(name, True)} | {mode} | {tab} |")
        result += [""]
    return result

def plus_groups(groups, tab, common_bar=False):
    result = []
    for group, names in groups:
        result += [f"#### {group} group", "", "| Command | Icon size | Dropdown / choices |", "| --- | --- | --- |"]
        if group in constants["COLLAPSED_GROUPS"]:
            result.append(f"| {group} | Small | Dropdown |")
            for name in names:
                if name != "Separator": result.append(f"| ↳ {button(name)} | Menu item | — |")
        else:
            for name, family_choices in projection(names):
                caption = {"Std_Part": "Add Component", "Part_CoordinateSystem": "Coordinate System"}.get(name)
                command = button(name) if not caption else f"{icon_for(name)} [{caption}](#button-{name.lower()})"
                choices = [] if common_bar else choices_for(name, family_choices)
                native_menu = not common_bar and len(data["commands"].get(name, [])) > 1
                result.append(f"| {command} | {size_for(name, tab, group)} | {'Dropdown' if choices or native_menu else '—'} |")
                for choice in choices:
                    result.append(f"| ↳ {button(choice)} | Menu item | — |")
                if native_menu and not choices:
                    result.append(f"| ↳ Native choices for [{cell(label(name))}](#button-{name.lower()}) | Menu items | See function catalog |")
        result += [""]
    return result

lines = ["# FreeCAD Plus toolbar reference", "",
    "Classic inventory comes first, followed by the implemented Plus layout, the change map, and the function catalog. "
    "Each command has its own row. Reference icons are displayed at **11 × 11 px**, approximately one third of the previous 32 px renders.", "",
    "The Plus layout implements the owner's revised direction and completes the incomplete outline with native command placements. "
    "**This layout is incorporated in the October 2 audit build; earlier 10/2 folders retain their previous layout.** Native IDs, icons and command descriptions come from the inspected payload. "
    "[UI rules](../../UI_UX_SPEC.md#toolbar-ui-styles) govern interaction; [WORK_STATE](../../WORK_STATE.md) records implementation/build acceptance.", "",
    "- [Classic toolbars](#classic-toolbars)", "- [Plus UI target layout](#plus-ui-target-layout)",
    "- [Changes and retained access](#changes-and-retained-access)", "- [Complete function catalog](#complete-toolbar-buttonfunction-catalog)", "",
    "## Classic toolbars", "",
    f"Recorded upstream source: `{upstream[:12]}`. Native metadata: application `{data['version'][7][:12]}`. "
    "Conditional/edit-only toolbars are included; they are not all shown simultaneously. Shared desktop groups are listed once. "
    "Plus locations below refer to the implemented layout; menu-only access is explicitly marked.", "",
    "### All workbenches — shared desktop", ""]
lines += classic_groups(standard)
for name in order:
    entry = data["workbenches"].get(name)
    if not entry: continue
    lines += [f'<a id="workbench-{name.lower()}"></a>', f"### {entry['label']} workbench", ""]
    module = modules.get(name)
    path = f"src/Mod/{module}/Gui/Workbench.cpp" if module else f"src/Mod/{name.removesuffix('Workbench')}/InitGui.py"
    lines += [f"Definition: [`{path}`](../../../{path})." +
              (" **Source-only; unavailable in the inspected build.**" if entry.get("source_only") else ""), ""]
    lines += classic_groups(baselines.get(name, {}))

lines += ["## Plus UI target layout", "",
    "### Size and dropdown key", "",
    "| Treatment | Use |", "| --- | --- |",
    "| Full size / big | Primary operations; one row, bounded captions |",
    "| Medium / half size | Frequently used actions that need less visual weight; bounded captions |",
    "| Small | Secondary actions; no visible caption; three-row grid inside the ribbon |",
    "| Dropdown | A separate property, compatible with any icon size; related or rare choices appear in its menu |", "",
    "Full icons are 40 logical pixels, medium icons 20, and small icons 16. Full buttons span the 76px grid; two medium buttons (38px each) or three small buttons (24px each) fit a column. "
    "Documentation icon size is independent of application button size. Every icon retains a tooltip and accessible name.", "",
    "### All Modes", "",
    "**Horizontal common toolbar above the ribbon.** These native actions remain visible when modes or tabs change. "
    "All use small icons in one horizontal row. They belong to Plus UI; Classic toolbar restoration must not duplicate them.", ""]
lines += plus_groups(common.items(), "Common toolbar", True)
lines += ["### Design Mode", "",
    "Tabs: **Home → Modeling → Surface → Sketch → Assembly → Mesh → View**. "
    "Sketch is retained from the earlier design because the owner's new outline is incomplete. "
    "Assembly is added to Design. Home contains curated frequent actions from the other tabs; specialist groups remain in their own tabs.", ""]
for tab, groups in design_tabs.items():
    lines += [f"#### {tab} tab", ""]
    # Deeper section headings keep groups nested under the tab in the outline.
    lines += [line.replace("#### ", "##### ", 1) if line.startswith("#### ") else line
              for line in plus_groups(groups, tab)]

for name in order:
    if name in ("PartDesignWorkbench", "SketcherWorkbench", "SurfaceWorkbench", "MeshWorkbench"): continue
    entry = data["workbenches"].get(name)
    if not entry: continue
    lines += [f"### {entry['label']} Mode", ""]
    if entry.get("source_only"):
        lines += ["**Conditional / source-only:** show this mode only when its workbench is installed and registered.", ""]
    lines += ["#### Home tab", "",
              "Component access, this mode's frequent operations, and shared utilities. "
              "File/Edit/Clipboard stay in the common toolbar above the ribbon.", ""]
    native_groups = entry.get("plus", {}).get("Tools", [])
    frequent = next(([c for c in ns if c != "Separator"][:3] for g,ns in native_groups if ns), [])
    mode_home = entry.get("plus", {}).get("Home") or [("Main", ["Std_Part", "Std_ComponentStructure"]), ("Frequent operations", frequent),
                 ("Utilities", home["Utilities"]), ("Help", home["Help"]), ("Macro", home["Macro"])]
    lines += [line.replace("#### ", "##### ", 1) if line.startswith("#### ") else line
              for line in plus_groups(mode_home, "Home")]
    lines += ["#### Tools tab", ""]
    lines += [line.replace("#### ", "##### ", 1) if line.startswith("#### ") else line
              for line in plus_groups(native_groups, "Tools")]
    lines += ["#### View tab", "", "Use the **Design → View** groups and sizes above; each mode activates its native view actions.", ""]
lines += ["### 3D Printing and other addon modes", "",
    "Only show a mode when an installed workbench registers it. Use the common toolbar, Home/Tools/View structure, "
    "and the same size hierarchy. Populate Tools from that workbench's actual groups; addon command lists remain unknown until installed. "
    "OpenSCAD's external-tool operations and BIM's reinforcement addons remain conditional.", "",
    "## Changes and retained access", "",
    "### Owner changes and completion of the outline", "",
    "| Change | Status / effect |", "| --- | --- |",
    "| Common toolbar above ribbon | Owner direction; File/Edit/Clipboard move out of Home and stay available in all modes |",
    "| Medium / half size | Owner direction; added between full and small, independent of dropdown behavior |",
    "| Home Main | Owner direction: New Component, Add Component, New Sketch, Coordinate System; medium icons |",
    "| Coordinate System dropdown | Owner direction: coordinate system, plane, axis, point; mapped to existing Part datum commands |",
    "| Home domain groups | Owner direction; individual common commands and sizes complete the outline |",
    "| Design Assembly tab | Owner outline; populated with existing Assembly and Assembly Joints groups |",
    "| Design Sketch tab | Retained as a completion of the incomplete outline |",
    "| Other modes | Existing native Tools groups retained; frequent Home subsets and sizes complete the outline |",
    "| New Component | Std_NewComponent creates an embedded model with zero instances and opens its editing tab; Add Component inserts an occurrence |", "",
    "### Classic-to-Plus consolidations", "",
    "| Classic commands | Plus access |", "| --- | --- |",
    f"| {button('PartDesign_Pad', True)} | Extrude → Add |",
    f"| {button('PartDesign_Pocket', True)} | Extrude → Subtract |"]
for command in ("PartDesign_LinearPattern", "PartDesign_PolarPattern"):
    lines.append(f"| {button(command, True)} | Pattern task → Linear / Circular type |")
for root, members, choices in families:
    for member in members:
        lines.append(f"| {button(member, True)} | {cell(label(root))} dropdown / task choices |")
lines += [f"| {button('Std_Workbench', True)} | Plus mode selector |", "",
    "Shared native menus and shortcuts remain available. A toolbar omission is not removal of the underlying function. "
    "Legacy Body creation is not promoted in Home; component results remain background objects. "
    "The restored Circular/Path/Point bindings exist in the inspected build. Toolbar placement here does not expand their geometry scope.", ""]
for name in order:
    entry = data["workbenches"].get(name)
    if not entry: continue
    old = {c for cs in baselines.get(name, {}).values() for c in cs if c != "Separator"}
    local = {c for g,cs in entry.get("classic", {}).items() if g not in STANDARD for c in cs if c != "Separator"}
    added, removed = sorted(local-old), sorted(old-local)
    lines += [f"### {entry['label']} native toolbar differences", ""]
    if not added and not removed:
        lines += ["No native command addition/removal in the compared toolbar definitions. Plus changes placement and presentation.", ""]
    else:
        lines += ["| Command | Native toolbar change |", "| --- | --- |"]
        for command in added: lines.append(f"| {button(command)} | Added in fork |")
        for command in removed: lines.append(f"| {button(command, True)} | Omitted from fork toolbar; consolidation/menu access noted above |")
        lines += [""]

lines += ["## Maintenance", "",
    "This reference owns command placement; the UI specification owns shared behavior/sizing. "
    "The owner's outline is incomplete: group membership and sizes remain reviewable. "
    "Refresh native metadata with [ExportToolbarReference.FCMacro](../../../tools/ExportToolbarReference.FCMacro), then "
    "`python tools/GenerateToolbarReference.py <inventory.json> <recorded-upstream-ref>`. Review the generator's target placements when owner decisions change.", "",
    "Artwork retains its original [license](../../../LICENSE). HTML width/height attributes scale reference icons without changing PNG/SVG assets.", ""]
pending = list(catalog)
while pending:
    for choice in source_choices.get(pending.pop(), []):
        if choice not in catalog:
            catalog.add(choice); pending.append(choice)
lines += ["## Complete toolbar button/function catalog", "",
    "Every Classic/Plus command and native compound-button choice is listed below. Native IDs disambiguate similar captions. "
    "Descriptions come from native help/status text or source resources. Dropdown child choices have their own rows. "
    "New Component is a registered native Python command with its own ID and function row.", "",
    "| Icon | Command / choice | Native ID | Function |", "| --- | --- | --- | --- |"]
for name in sorted(catalog):
    entries = data["commands"].get(name) or [action(name)]
    for index, entry in enumerate(entries):
        if not any(entry.get(key) for key in ("text", "status", "tooltip", "icon")): continue
        description = clean(entry.get("status", "")) or clean(entry.get("tooltip", ""))
        description = description or "Source-only command; consult its linked workbench definition."
        anchor = f'<a id="button-{name.lower()}"></a>' if index == 0 else "↳ "
        lines.append(f"| {icon_for(name, entry)} | {anchor}{cell(clean(entry['text']))} | `{name}` | {cell(description)} |")
lines += [""]
OUT.write_text("\n".join(lines).rstrip()+"\n", encoding="utf-8")
print(json.dumps({"file": str(OUT), "toolbar_commands": len(catalog), "icon_files": len(used_icons),
                  "reference_icon_px": 11, "layout_status": "incorporated in October 2 audit build"}, indent=2))
