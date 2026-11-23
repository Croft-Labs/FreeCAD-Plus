from PySide6 import QtCore,QtWidgets

def proposed():return True

class OneEnter(QtCore.QObject):
    def __init__(self,field,dialog,parent):
        super().__init__(parent);self.field=field;self.dialog=dialog
    def eventFilter(self,widget,event):
        if widget is self.field and event.type()==QtCore.QEvent.KeyPress and event.key() in (QtCore.Qt.Key_Return,QtCore.Qt.Key_Enter):
            self.field.focusNextChild();self.dialog.accept();return True
        return False

def install(field,dialog,parent):
    observer=OneEnter(field,dialog,parent)
    QtWidgets.QApplication.instance().installEventFilter(observer)
    return observer
