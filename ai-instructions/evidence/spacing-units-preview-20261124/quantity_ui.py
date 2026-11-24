from pathlib import Path
import FreeCADGui as Gui
from PySide6 import QtCore, QtGui, QtWidgets

PROPOSED = True

class Review(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FreeCAD Plus — spacing and units review')
        self.setFixedWidth(900)
        outer = QtWidgets.QVBoxLayout(self)
        title = QtWidgets.QLabel('Preferences → General · Language and Number Format')
        title.setStyleSheet('font-size: 18px; font-weight: 600; padding: 6px;')
        outer.addWidget(title)
        self.title = title
        self.stack = QtWidgets.QStackedWidget(); outer.addWidget(self.stack)
        self.preference = Gui.PySideUic.loadUi(str(Path(__file__).with_name('General.ui')))
        group = self.preference.findChild(QtWidgets.QGroupBox, 'GroupBox7')
        group.setParent(None)
        self.stack.addWidget(group)
        languages = group.findChild(QtWidgets.QComboBox, 'Languages'); languages.addItem('English')
        units = group.findChild(QtWidgets.QComboBox, 'comboBox_UnitSystem')
        units.addItem('Standard (mm, kg, s, °)')
        group.findChild(QtWidgets.QSpinBox, 'spinBoxDecimals').setValue(2)
        secondary = group.findChild(QtWidgets.QComboBox, 'SecondaryUnits')
        if secondary:
            secondary.addItems(['Imperial decimal (in, lb, s, °)', 'Standard (mm, kg, s, °)', 'MKS (m, kg, s, °)'])
            group.findChild(QtWidgets.QSpinBox, 'SecondaryDecimals').setValue(3)
        self.make_values()
        self.make_spacing()
        footer = QtWidgets.QLabel('UI simulation only — preferences, geometry and saved documents are not changed.')
        footer.setWordWrap(True); footer.setStyleSheet('color: #666; padding: 8px;')
        outer.addWidget(footer)

    def make_values(self):
        page = QtWidgets.QWidget(); layout = QtWidgets.QVBoxLayout(page)
        intro = QtWidgets.QLabel('Enter six decimal places without rounding the stored value. Leader precision controls display only.' if PROPOSED else 'Current task fields and global dimension formatting')
        intro.setWordWrap(True); layout.addWidget(intro)
        cases = [('Metric input', '1.29999 mm', '1.30 mm', '1.29999 mm'),
                 ('Explicit inch input', '0.100 in', '0.100 in' if PROPOSED else '2.54 mm', '0.100 in' if PROPOSED else '2.54 mm'),
                 ('Six-decimal input', '0.123456 in', '0.123 in' if PROPOSED else '3.14 mm', '0.123456 in' if PROPOSED else '3.14 mm')]
        self.fields = []
        for title, entry, label, reopened in cases:
            box = QtWidgets.QGroupBox(title); grid = QtWidgets.QGridLayout(box)
            grid.addWidget(QtWidgets.QLabel('Value / dimension editor'), 0, 0)
            field = QtWidgets.QLineEdit(entry if PROPOSED else ('1.30 mm' if title=='Metric input' else label))
            field.setMinimumWidth(220); grid.addWidget(field, 0, 1)
            grid.addWidget(QtWidgets.QLabel('Dimension leader'), 1, 0)
            leader = QtWidgets.QLabel(label); leader.setStyleSheet('font-size: 18px; padding: 8px; border-bottom: 1px solid #347bb7;')
            grid.addWidget(leader, 1, 1)
            grid.addWidget(QtWidgets.QLabel('Reopen for editing'), 2, 0)
            grid.addWidget(QtWidgets.QLineEdit(reopened), 2, 1)
            layout.addWidget(box); self.fields.append(field)
        note = QtWidgets.QLabel('Type a compatible unit suffix (mm, in, ft, cm, °, rad…). Explicit units stay with the value. Counts remain whole numbers.')
        note.setWordWrap(True); layout.addWidget(note)
        self.stack.addWidget(page)

    def make_spacing(self):
        page = QtWidgets.QWidget(); layout = QtWidgets.QVBoxLayout(page)
        row = QtWidgets.QHBoxLayout()
        option = QtWidgets.QCheckBox('Create spacing constraints' if PROPOSED else 'Create dimensions')
        option.setChecked(True); row.addWidget(option); row.addStretch(); layout.addLayout(row)
        hide = QtWidgets.QCheckBox('Hide spacing chain'); layout.addWidget(hide)
        form = QtWidgets.QFormLayout()
        form.addRow('Pitch', QtWidgets.QLineEdit('0.100 in' if PROPOSED else '2.54 mm'))
        form.addRow('Instances', QtWidgets.QSpinBox())
        form.itemAt(1, QtWidgets.QFormLayout.FieldRole).widget().setValue(5)
        layout.addLayout(form)
        scene = QtWidgets.QGraphicsScene(0, 0, 830, 280, page)
        geometry = QtGui.QPen(QtGui.QColor('#333333'), 2)
        spacing = QtGui.QPen(QtGui.QColor('#2879b8'), 2, QtCore.Qt.DashLine)
        chain = []
        for i in range(5):
            x = 60 + i * 170
            scene.addRect(x, 100, 55, 60, geometry)
            if i < 4:
                chain.append(scene.addLine(x, 160, x+170, 160, spacing))
                marker = scene.addText('=   ∥' if PROPOSED else 'ΔX / ΔY')
                marker.setDefaultTextColor(QtGui.QColor('#2879b8')); marker.setPos(x+60, 165)
                chain.append(marker)
            if PROPOSED: chain.append(scene.addEllipse(x-4, 156, 8, 8, spacing))
        scene.addLine(60, 212, 230, 212, geometry)
        scene.addLine(60, 199, 60, 223, geometry); scene.addLine(230, 199, 230, 223, geometry)
        label = scene.addText('0.100 in' if PROPOSED else '2.54 mm'); label.setPos(100, 220)
        label.setDefaultTextColor(QtGui.QColor('#151515'))
        view = QtWidgets.QGraphicsView(scene); view.setFixedHeight(290); layout.addWidget(view)
        text = ('One driving length for each independent pitch. Remaining construction lines are equal and parallel/collinear, with coincident endpoints forming a continuous chain.' if PROPOSED else 'Copies receive individual relative coordinate dimensions.')
        note = QtWidgets.QLabel(text); note.setWordWrap(True); layout.addWidget(note)
        if PROPOSED:
            note = QtWidgets.QLabel('Separate pitches in opposite directions keep separate chains. Hiding the chain preserves constraints and the driving dimension.')
            note.setWordWrap(True); layout.addWidget(note)
        hide.toggled.connect(lambda checked: [item.setVisible(not checked) for item in chain])
        option.toggled.connect(hide.setEnabled)
        self.hide_linear = hide
        self.stack.addWidget(page)
        self.make_radial()

    def make_radial(self):
        import math
        page = QtWidgets.QWidget(); layout = QtWidgets.QVBoxLayout(page)
        hide = QtWidgets.QCheckBox('Hide spacing chain'); layout.addWidget(hide)
        scene = QtWidgets.QGraphicsScene(0, 0, 830, 390, page)
        geometry = QtGui.QPen(QtGui.QColor('#333333'), 2)
        construction = QtGui.QPen(QtGui.QColor('#2879b8'), 2, QtCore.Qt.DashLine)
        center = QtCore.QPointF(190, 320); radii = (110, 180, 250); angles = (0, 30, 60, 90)
        chain=[]
        for radius in radii:
            for angle in angles:
                theta=math.radians(angle); x=center.x()+radius*math.cos(theta); y=center.y()-radius*math.sin(theta)
                scene.addEllipse(x-9, y-9, 18, 18, geometry)
            for angle in angles[:-1]:
                path=QtGui.QPainterPath(); rect=QtCore.QRectF(center.x()-radius,center.y()-radius,2*radius,2*radius)
                path.arcMoveTo(rect,angle); path.arcTo(rect,angle,30)
                chain.append(scene.addPath(path,construction))
        for angle in angles:
            theta=math.radians(angle)
            for first,last in zip(radii,radii[1:]):
                chain.append(scene.addLine(center.x()+first*math.cos(theta),center.y()-first*math.sin(theta),center.x()+last*math.cos(theta),center.y()-last*math.sin(theta),construction))
        scene.addEllipse(center.x()-3,center.y()-3,6,6,geometry)
        for x,y,text in [(515,55,'Angular spacing: connected arcs'),(515,90,'Equal angular spans • 30.00°'),(515,155,'Radial spacing: connected lines'),(515,190,'Equal lengths • 0.100 in'),(515,255,'Coincident chain endpoints'),(515,290,'One driver per independent pitch')]:
            label=scene.addText(text); label.setPos(x,y); label.setDefaultTextColor(QtGui.QColor('#151515'))
        view=QtWidgets.QGraphicsView(scene);view.setFixedHeight(400);layout.addWidget(view)
        note=QtWidgets.QLabel('Arc centers remain at the rotation center. Each ring has equal angular steps; different ring radii naturally have different arc lengths. Hide changes visibility only and persists with the sketch.')
        note.setWordWrap(True);layout.addWidget(note)
        hide.toggled.connect(lambda checked:[item.setVisible(not checked) for item in chain])
        self.hide_radial=hide
        self.stack.addWidget(page)

    def show_page(self, index):
        self.stack.setCurrentIndex(index)
        for i in range(self.stack.count()):
            self.stack.widget(i).setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred if i==index else QtWidgets.QSizePolicy.Ignored)
        self.title.setText(['Preferences → General · Language and Number Format', 'Task fields · stored value and dimension leader', 'Sketch Pattern · connected spacing lines', 'Circular Pattern · angular arcs and radial lines'][index])
        self.stack.setFixedHeight(self.stack.currentWidget().sizeHint().height())
        self.adjustSize()
