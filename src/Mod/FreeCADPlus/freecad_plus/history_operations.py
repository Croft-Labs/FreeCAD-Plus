# SPDX-License-Identifier: LGPL-2.1-or-later
"""History-only operation labels and tinted native glyphs; no document writes."""
from collections import OrderedDict
from PySide6 import QtGui

COLORS = {'New Solid': '#fce94f', 'Add': '#fce94f', 'Subtract': '#d63e3e'}
_ENGINES = ('Extrude', 'Revolve', 'Loft', 'Thicken')
_PRIMITIVES = ('Box', 'Cylinder', 'Sphere', 'Cone', 'Ellipsoid', 'Torus', 'Prism', 'Wedge')
_ADDITIVE = frozenset(('PartDesign::Pad', 'PartDesign::Revolution',
                      'PartDesign::AdditiveLoft', 'PartDesign::AdditivePipe',
                      'PartDesign::AdditiveHelix') +
                     tuple('PartDesign::Additive' + name for name in _PRIMITIVES))
_SUBTRACTIVE = frozenset(('PartDesign::Pocket', 'PartDesign::Groove',
                         'PartDesign::SubtractiveLoft', 'PartDesign::SubtractivePipe',
                         'PartDesign::SubtractiveHelix') +
                        tuple('PartDesign::Subtractive' + name for name in _PRIMITIVES))
_PART_NEW = frozenset(('Part::Extrusion', 'Part::Revolution', 'Part::Loft', 'Part::Sweep'))
_icons = OrderedDict()


def describe(obj):
    """Read supported saved operation contracts, never infer from a display name."""
    for name in _ENGINES:
        version = getattr(obj, 'Plus' + name + 'Version', None)
        if version is None:
            continue
        if version != 1:
            return None
        operation = getattr(obj, name + '_operation', None)
        output = getattr(obj, name + '_output', 'Solid')
        if operation not in COLORS or output not in ('Solid', 'Sheet'):
            return None
        if output == 'Sheet' and operation != 'New Solid':
            return None  # Unsupported/corrupt combination, not an invented Boolean mode.
        suffix = ('new surface' if output == 'Sheet' else 'new body') if operation == 'New Solid' else operation.lower()
        return operation, suffix
    if obj.TypeId in _SUBTRACTIVE:
        return 'Subtract', 'subtract'
    if obj.TypeId in _ADDITIVE:
        if 'BaseFeature' not in obj.PropertiesList:
            return None
        predecessor = obj.BaseFeature
        if predecessor is None:
            return 'New Solid', 'new body'
        shape = getattr(predecessor, 'Shape', None)
        if shape is not None and not shape.isNull() and shape.Solids:
            return 'Add', 'add'
        return None  # A broken predecessor must not be advertised as a new body.
    if obj.TypeId in _PART_NEW and 'Solid' in obj.PropertiesList:
        return 'New Solid', 'new body' if obj.Solid else 'new surface'
    return None


def colored(icon, operation):
    """Retain the approved native outline/shading; cache bounded, UI-only copies."""
    if icon.isNull():
        return icon
    key = (icon.cacheKey(), COLORS[operation])
    if key in _icons:
        _icons.move_to_end(key)
        return _icons[key]
    base = QtGui.QColor(COLORS[operation]); result = QtGui.QIcon()
    for size in (16, 20, 24, 32, 48, 64):
        image = icon.pixmap(size, size).toImage().convertToFormat(QtGui.QImage.Format_ARGB32)
        for y in range(image.height()):
            for x in range(image.width()):
                color = image.pixelColor(x, y)
                if not color.alpha():
                    continue
                channels = (color.red(), color.green(), color.blue())
                if max(channels) < 48 or (min(channels) > 225 and max(channels) - min(channels) < 20):
                    continue
                luminance = (.2126 * color.red() + .7152 * color.green() + .0722 * color.blue()) / 255.
                factor = .35 + .75 * luminance
                tinted = QtGui.QColor(min(255, round(base.red() * factor)),
                                     min(255, round(base.green() * factor)),
                                     min(255, round(base.blue() * factor)), color.alpha())
                image.setPixelColor(x, y, tinted)
        result.addPixmap(QtGui.QPixmap.fromImage(image))
    _icons[key] = result
    if len(_icons) > 256:
        _icons.popitem(last=False)
    return result


def presentation(obj, label, icon):
    info = describe(obj)
    if info is None:
        return label, icon
    operation, suffix = info
    return label + ' (' + suffix + ')', colored(icon, operation)
