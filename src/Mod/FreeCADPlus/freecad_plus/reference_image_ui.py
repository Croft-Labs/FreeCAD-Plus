# SPDX-License-Identifier: LGPL-2.1-or-later
"""Reference image task controls; placement uses existing planes only."""
from PySide6 import QtCore, QtGui, QtWidgets
from .quantity_fields import QuantityNumber
from .task_status import TaskStatus


def note(text):
    label = QtWidgets.QLabel(text)
    label.setWordWrap(True)
    return label


class ImageNumber(QuantityNumber):
    def textFromValue(self,value):
        if getattr(self,'_unit','mm')=='deg':
            return self.locale().toString(value,'f',2)+' °'
        return super().textFromValue(value)


def number(value=0, suffix=' mm', minimum=-100000):
    field = ImageNumber()
    field.setDecimals(2)
    field.setRange(minimum, 100000)
    field.setValue(value)
    field.setSuffix(suffix)
    field.setKeyboardTracking(False)
    field.setMinimumWidth(106)
    if suffix == '°':
        field.setSingleStep(0.01)
    return field


class Form(QtWidgets.QWidget):
    def __init__(self,owner):
        super().__init__()
        self.setWindowTitle('Reference image')
        self.setAutoFillBackground(True)
        palette=self.palette();palette.setColor(QtGui.QPalette.Window,QtGui.QColor('#efefef'));self.setPalette(palette)
        self.setMinimumWidth(460)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(7)
        layout.addWidget(note('Component: '+owner.Label))
        def group(title):
            box = QtWidgets.QGroupBox(title)
            inner = QtWidgets.QVBoxLayout(box)
            inner.setContentsMargins(9, 8, 9, 8)
            inner.setSpacing(5)
            layout.addWidget(box)
            return inner
        image = group('Image')
        row = QtWidgets.QHBoxLayout()
        self.file = QtWidgets.QLineEdit()
        self.file.setReadOnly(True)
        self.file.setPlaceholderText('Choose an image…')
        self.browse = QtWidgets.QPushButton('Browse…')
        row.addWidget(self.file, 1); row.addWidget(self.browse); image.addLayout(row)
        image.addWidget(note('The image will be stored inside this part file.'))

        support = group('Plane / attachment')
        self.plane = QtWidgets.QComboBox()
        support.addWidget(self.plane)
        self.attached_hint = note('The image follows its plane. Offset is along the plane normal.')
        support.addWidget(self.attached_hint)

        size = group('Size')
        row = QtWidgets.QHBoxLayout()
        self.width = number(100, minimum=0.001); self.height = number(100, minimum=0.001)
        row.addWidget(QtWidgets.QLabel('Width')); row.addWidget(self.width,1)
        row.addWidget(QtWidgets.QLabel('Height')); row.addWidget(self.height,1); size.addLayout(row)
        self.aspect = QtWidgets.QCheckBox('Keep aspect ratio'); self.aspect.setChecked(True)
        row = QtWidgets.QHBoxLayout(); row.addWidget(self.aspect)
        self.calibrate = QtWidgets.QPushButton('Calibrate from 2 points…'); self.calibrate.setCheckable(True)
        row.addWidget(self.calibrate); size.addLayout(row)
        self.calibration = QtWidgets.QWidget(); cal = QtWidgets.QVBoxLayout(self.calibration); cal.setContentsMargins(0,0,0,0)
        self.points = QtWidgets.QListWidget(); self.points.setFixedHeight(54)
        cal.addWidget(self.points)
        row = QtWidgets.QHBoxLayout()
        self.known = number(100,minimum=0.01)
        row.addWidget(QtWidgets.QLabel('Known distance')); row.addWidget(self.known)
        self.pick_points = QtWidgets.QPushButton('Pick 2 points'); row.addWidget(self.pick_points)
        cal.addLayout(row); size.addWidget(self.calibration); self.calibration.hide()
        self.calibrate.toggled.connect(self.calibration.setVisible)
        self.ratio=1.
        self.width.valueChanged.connect(lambda value: self.sync_size(self.height,value/self.ratio))
        self.height.valueChanged.connect(lambda value: self.sync_size(self.width,value*self.ratio))

        anchor = group('Scale and rotation anchor')
        row = QtWidgets.QHBoxLayout()
        self.preset = QtWidgets.QRadioButton('Preset'); self.preset.setChecked(True)
        self.custom = QtWidgets.QRadioButton('Picked image point')
        row.addWidget(self.preset); row.addWidget(self.custom); row.addStretch(); anchor.addLayout(row)
        self.anchor_grid = QtWidgets.QWidget(); grid = QtWidgets.QGridLayout(self.anchor_grid)
        grid.setContentsMargins(0,0,0,0); grid.setSpacing(3)
        self.anchor_buttons = QtWidgets.QButtonGroup(self)
        for i,text in enumerate(('Top left','Top middle','Top right','Middle left','Center','Middle right','Bottom left','Bottom middle','Bottom right')):
            button = QtWidgets.QPushButton(text); button.setCheckable(True)
            self.anchor_buttons.addButton(button,i); grid.addWidget(button,i//3,i%3)
            if i==4: button.setChecked(True)
        anchor.addWidget(self.anchor_grid)
        self.custom_row = QtWidgets.QWidget(); row = QtWidgets.QHBoxLayout(self.custom_row); row.setContentsMargins(0,0,0,0)
        self.anchor_point = QtWidgets.QLineEdit(); self.anchor_point.setReadOnly(True); self.anchor_point.setPlaceholderText('No image point selected')
        self.pick_anchor = QtWidgets.QPushButton('Pick point')
        row.addWidget(self.anchor_point,1); row.addWidget(self.pick_anchor); anchor.addWidget(self.custom_row)
        self.custom_row.hide()
        self.custom.toggled.connect(self.custom_row.setVisible)
        self.custom.toggled.connect(lambda checked:self.anchor_grid.setVisible(not checked))
        anchor.addWidget(note('Resizing and rotation keep this point fixed. Changing the anchor does not move the image.'))

        placement = group('Anchor position and rotation')
        row = QtWidgets.QHBoxLayout(); self.position_labels=[]; self.positions=[]
        for title in ('U','V','Offset'):
            label=QtWidgets.QLabel(title); self.position_labels.append(label)
            field=number(); self.positions.append(field); row.addWidget(label); row.addWidget(field,1)
        placement.addLayout(row)
        self.normal_row = QtWidgets.QWidget(); row=QtWidgets.QHBoxLayout(self.normal_row); row.setContentsMargins(0,0,0,0)
        row.addWidget(QtWidgets.QLabel('Rotation on plane'))
        self.angle = number(0,'°',-360); self.angle.setMaximum(360)
        row.addWidget(self.angle,1)
        self.flip=QtWidgets.QCheckBox('Flip normal'); row.addWidget(self.flip); placement.addWidget(self.normal_row)
        self.free_row = QtWidgets.QWidget(); row=QtWidgets.QHBoxLayout(self.free_row); row.setContentsMargins(0,0,0,0)
        self.rotations=[]
        for axis in ('X','Y','Z'):
            row.addWidget(QtWidgets.QLabel(axis)); field=number(0,'°',-360); field.setMaximum(360); row.addWidget(field,1); self.rotations.append(field)
        placement.addWidget(self.free_row)
        self.precision_hint=note('Rotation step: 0.01°. U and V are along the attached plane.')
        placement.addWidget(self.precision_hint)
        self.plane.currentIndexChanged.connect(self.mode_changed)

        display = group('Display')
        row = QtWidgets.QHBoxLayout(); row.addWidget(QtWidgets.QLabel('Transparency'))
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal); self.slider.setRange(0,100)
        self.alpha = QtWidgets.QSpinBox(); self.alpha.setRange(0,100); self.alpha.setSuffix(' %')
        self.slider.valueChanged.connect(self.alpha.setValue); self.alpha.valueChanged.connect(self.slider.setValue)
        row.addWidget(self.slider,1); row.addWidget(self.alpha); display.addLayout(row)
        self.preview=QtWidgets.QCheckBox('Show preview'); self.preview.setChecked(True); display.addWidget(self.preview)
        self.status=TaskStatus('Choose an image.'); layout.addWidget(self.status)
        layout.addWidget(note('Apply adds this image and resets for another. Cancel discards unapplied changes.'))
        row=QtWidgets.QHBoxLayout()
        self.done=QtWidgets.QPushButton('Done'); self.apply=QtWidgets.QPushButton('Apply'); self.cancel=QtWidgets.QPushButton('Cancel')
        for button in (self.done,self.apply,self.cancel):row.addWidget(button)
        layout.addLayout(row); layout.addStretch()

    def sync_size(self,other,value):
        if self.aspect.isChecked():
            blocker=QtCore.QSignalBlocker(other); other.setValue(value)

    def mode_changed(self,index):
        free=self.plane.currentData() is None
        self.attached_hint.setText('Position is relative to the component coordinate system.' if free else 'The image follows its plane. Offset is along the plane normal.')
        for label,text in zip(self.position_labels,('X','Y','Z') if free else ('U','V','Offset')):label.setText(text)
        self.normal_row.setVisible(not free); self.free_row.setVisible(free)
        self.precision_hint.setText('Rotation step: 0.01°. X, Y and Z rotations are around the anchor.' if free else 'Rotation step: 0.01°. U and V are along the attached plane.')


