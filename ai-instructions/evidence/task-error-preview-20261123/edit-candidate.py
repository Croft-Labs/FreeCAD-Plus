from pathlib import Path
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/app-render-companion/sessions/16176df60dd2/candidate')
assert root.name=='candidate'
(root/'task_status.py').write_text('''# SPDX-License-Identifier: LGPL-2.1-or-later
"""UI-only shared error treatment under screenshot review."""
from PySide6 import QtCore, QtWidgets

class TaskStatus(QtWidgets.QLabel):
    def __init__(self, text=''):
        super().__init__(text)
        self.setWordWrap(True)
        self.setTextFormat(QtCore.Qt.PlainText)
        self.error=False

    def setText(self, text):
        self.error=False
        self.setStyleSheet('')
        super().setText(text)

    def setError(self, text):
        reveal=not self.error or self.text()!=text
        self.error=True
        self.setStyleSheet('QLabel { border: 2px solid #bd780b; border-radius: 3px; '
                          'background: #fff3d6; color: #875300; padding: 8px; font-weight: 600; }')
        super().setText(text)
        if reveal:QtCore.QTimer.singleShot(50,self.revealError)

    def revealError(self, settle=True):
        try:
            if not self.error:return
            parent=self.parentWidget()
            while parent is not None:
                if isinstance(parent,QtWidgets.QScrollArea):
                    viewport=parent.viewport()
                    top=self.mapTo(viewport,QtCore.QPoint()).y()
                    bottom=top+self.height()
                    delta=bottom+12-viewport.height() if bottom+12>viewport.height() else min(0,top-12)
                    bar=parent.verticalScrollBar()
                    bar.setValue(bar.value()+delta)
                    # Native task groups can resize once more after scrolling.
                    if settle:QtCore.QTimer.singleShot(50,lambda:self.revealError(False))
                    return
                parent=parent.parentWidget()
        except RuntimeError:
            pass  # Task was closed before the queued UI update.
''',encoding='utf-8')
for name in ('plane_task.py','sketch_task.py','extrude_task.py'):
    path=root/name;text=(Path(__file__).parent/'review-source'/name).read_text(encoding='utf-8')
    text=text.replace('self.status.setText(str(exc))','self.status.setError(str(exc))')
    if name=='plane_task.py':
        text=text.replace('from pivy import coin','from pivy import coin\nfrom .task_status import TaskStatus')
        text=text.replace("self.status = label('Under-defined", "self.status = TaskStatus('Under-defined")
        text=text.replace("self.status.setText(('Invalid — '","self.status.setError(('Invalid — '")
        text=text.replace("except planes.IncompletePlane as exc:\n            self.valid = False; self.status.setError(str(exc))",
                          "except planes.IncompletePlane as exc:\n            self.valid = False; self.status.setText(str(exc))")
    elif name=='extrude_task.py':
        text=text.replace('from freecad_plus.plane_task import Section, label, number, buttons',
                          'from freecad_plus.plane_task import Section, label, number, buttons\nfrom .task_status import TaskStatus')
        text=text.replace("self.status = label('Select a profile.')", "self.status = TaskStatus('Select a profile.')")
    path.write_text(text,encoding='utf-8')
