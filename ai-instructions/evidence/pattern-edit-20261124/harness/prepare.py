from pathlib import Path
here=Path(__file__).parent
previous=here.parent/'pattern-group-validation'
text=(previous/'install.py').read_text(encoding='utf-8').replace('pattern-group-20261124','pattern-edit-20261124')
text=text.replace(",('Mod/Sketcher/Sketcher.pyd','lib/Sketcher.pyd')",'')
text=text.replace("changed+=['src/Mod/FreeCADPlus/TestPatternGroups.py']", "changed+=['src/Mod/FreeCADPlus/'+name for name in ('TestPatternEditing.py','freecad_plus/sketch_pattern_edit.py','freecad_plus/sketch_pattern_legacy.py')]")
(here/'install.py').write_text(text,encoding='utf-8')
text=(previous/'shortcut.py').read_text(encoding='utf-8').replace('pattern-group-20261124','pattern-edit-20261124')
text=text.replace("'TestPatternGroups.TestPatternGroupView'", "'TestPatternEditing.TestPatternEditingTask,TestPatternGroups.TestPatternGroupView.test_group_pitch_editor_preserves_units'")
(here/'shortcut.py').write_text(text,encoding='utf-8')
text=(here/'run.py').read_text(encoding='utf-8').replace("with_name('run.FCMacro')","with_name('reopen.FCMacro')")
(here/'reopen.py').write_text(text,encoding='utf-8')
