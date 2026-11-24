import os,sys,importlib.util,json
from pathlib import Path
sys.dont_write_bytecode=True
from PySide6 import QtWidgets,QtCore,QtGui
worktree,output=map(Path,sys.argv[1:3])
spec=importlib.util.spec_from_file_location('pattern_group_ui',worktree/'pattern_group_ui.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
app=QtWidgets.QApplication([]);app.setStyle('Fusion')
palette=QtGui.QPalette()
for role,color in ((QtGui.QPalette.Window,'#efefef'),(QtGui.QPalette.WindowText,'#111111'),
                   (QtGui.QPalette.Base,'#ffffff'),(QtGui.QPalette.Text,'#111111'),
                   (QtGui.QPalette.Button,'#efefef'),(QtGui.QPalette.ButtonText,'#111111'),
                   (QtGui.QPalette.Highlight,'#308cc6'),(QtGui.QPalette.HighlightedText,'#ffffff')):
    palette.setColor(role,QtGui.QColor(color))
app.setPalette(palette)
widget=module.build();widget.show()
def capture():
    widget.grab().save(str(output));app.quit()
QtCore.QTimer.singleShot(250,capture)
app.exec()
assert output.exists()
print(json.dumps(dict(ok=True,grouped=module.GROUPED,hidden_graphics=module.HIDE_ALL_SPACING_GRAPHICS)))
