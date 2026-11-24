"""UI-only Qt simulation, based on the existing Sketcher constraint presentation.
No solver, persistence or production behavior is implemented here.
"""
from PySide6 import QtCore,QtGui,QtWidgets
GROUPED=True
HIDE_ALL_SPACING_GRAPHICS=True
ICON='C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus/src/Mod/Sketcher/Gui/Resources/icons/tools/Sketcher_RectangularArray.svg'

class SketchView(QtWidgets.QWidget):
    def __init__(self,hidden=False):
        super().__init__();self.hidden=hidden;self.setMinimumSize(740,430)
    def paintEvent(self,event):
        p=QtGui.QPainter(self);p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.fillRect(self.rect(),QtGui.QColor('#ffffff'))
        p.setPen(QtGui.QPen(QtGui.QColor('#e67d7d'),1));p.drawLine(26,387,705,387)
        p.setPen(QtGui.QPen(QtGui.QColor('#7ebf88'),1));p.drawLine(48,22,48,411)
        points=[QtCore.QPointF(115+x*44,55+y*26) for x in range(12) for y in range(12)]
        if not self.hidden:
            p.setPen(QtGui.QPen(QtGui.QColor('#668bd1'),1,QtCore.Qt.DashLine))
            for x in range(12):
                for y in range(12):
                    a=points[x*12+y]
                    if x<11:
                        b=points[(x+1)*12+y]
                        p.drawLine(a,b);p.drawLine(a+QtCore.QPointF(17,0),b+QtCore.QPointF(17,0))
                    if x==0 and y<11:
                        b=points[y+1];p.drawLine(a,b);p.drawLine(a+QtCore.QPointF(17,0),b+QtCore.QPointF(17,0))
        p.setPen(QtGui.QPen(QtGui.QColor('#262626'),2))
        for a in points:p.drawLine(a,a+QtCore.QPointF(17,0))
        p.setPen(QtGui.QPen(QtGui.QColor('#d33030'),1));p.setFont(QtGui.QFont('Segoe UI',10))
        p.drawLine(115,38,132,38);p.drawLine(115,34,115,44);p.drawLine(132,34,132,44)
        p.drawText(103,27,'4.00 mm')
        if GROUPED:
            if not self.hidden:
                QtGui.QIcon(ICON).paint(p,QtCore.QRect(643,338,26,26))
                p.drawText(675,358,'1')
        else:
            if not self.hidden:
                for n,a in enumerate(points):
                    p.drawText(a+QtCore.QPointF(18,-3),'=' if n%2 else '//')
                    if n%3==0:p.drawEllipse(a+QtCore.QPointF(26,0),2,2)
            if not self.hidden or not HIDE_ALL_SPACING_GRAPHICS:
                p.drawLine(115,361,159,361);p.drawText(110,380,'20.00 mm')
                p.drawLine(85,55,85,81);p.drawText(12,75,'20.00 mm')
        p.end()

class State(QtWidgets.QWidget):
    def __init__(self,hidden=False):
        super().__init__();outer=QtWidgets.QVBoxLayout(self)
        title=QtWidgets.QLabel('Hide spacing chain checked' if hidden else 'Spacing chain shown')
        title.setStyleSheet('font-size:16px;font-weight:600');outer.addWidget(title)
        row=QtWidgets.QHBoxLayout();outer.addLayout(row)
        row.addWidget(SketchView(hidden),1)
        panel=QtWidgets.QWidget();panel.setFixedWidth(326);layout=QtWidgets.QVBoxLayout(panel)
        label=QtWidgets.QLabel('Constraints');label.setStyleSheet('font-weight:600;font-size:15px');layout.addWidget(label)
        options=QtWidgets.QHBoxLayout();options.addWidget(QtWidgets.QLabel('Filter'))
        filter=QtWidgets.QComboBox();filter.addItems(['All']);options.addWidget(filter,1);layout.addLayout(options)
        listing=QtWidgets.QListWidget();listing.setObjectName('ConstraintListPreview');layout.addWidget(listing,1)
        listing.addItem('1  Length = 4.00 mm')
        if GROUPED:
            item=QtWidgets.QListWidgetItem(QtGui.QIcon(ICON),'Pattern 1 — 12 × 12',listing)
            item.setToolTip('Linear pattern · all generated relationships')
            if hidden:item.setForeground(QtGui.QColor('#777777'))
        else:
            for n,kind in enumerate(['Equal','Coincident','Coincident','Equal','Parallel','Coincident','Coincident','Parallel','Distance = 20.00 mm','Equal','Coincident','Parallel'],2):
                listing.addItem(str(n)+'  '+kind)
        check=QtWidgets.QCheckBox('Hide spacing chain');check.setChecked(hidden);layout.addWidget(check)
        row.addWidget(panel)

def build():
    widget=QtWidgets.QWidget();widget.setStyleSheet('QWidget {font-family: Segoe UI; font-size: 12px;} QListWidget {background:white;}')
    layout=QtWidgets.QVBoxLayout(widget)
    label=QtWidgets.QLabel('Sketch Pattern — single-icon proposal' if GROUPED else 'Sketch Pattern — current presentation')
    label.setStyleSheet('font-size:20px;font-weight:600');layout.addWidget(label)
    note=QtWidgets.QLabel('Qt UI simulation • 12 × 12 fixed-length lines • original length remains separate')
    layout.addWidget(note);layout.addWidget(State(False));layout.addWidget(State(True))
    widget.resize(1160,1010);return widget
