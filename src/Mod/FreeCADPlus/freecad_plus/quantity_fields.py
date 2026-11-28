# SPDX-License-Identifier: LGPL-2.1-or-later
"""Unit-aware deferred task numbers. Physical values stay in native mm/degrees."""
import math
import re
import FreeCAD as App
from PySide6 import QtCore, QtGui, QtWidgets


class QuantityNumber(QtWidgets.QDoubleSpinBox):
    committed = QtCore.Signal()

    def __init__(self, parent=None):
        self._unit = 'mm'
        self._dimension = App.Units.Quantity('1 mm').Unit
        super().__init__(parent)
        super().setDecimals(15)
        self.setKeyboardTracking(False)

    def setDecimals(self, places):
        # QDoubleSpinBox rounds its stored double to this precision. Keep the
        # storage independent from the six-place editing presentation.
        super().setDecimals(max(15, places))

    def setSuffix(self, unit):
        self._unit = unit.strip().replace('°', 'deg')
        self._dimension = App.Units.Quantity('1 ' + self._unit).Unit
        self.lineEdit().setText(self.textFromValue(self.value()))

    def suffix(self):
        return ' ' + self._unit

    def parse(self, text):
        text = text.strip().replace(self.locale().decimalPoint(), '.')
        q = App.DocumentObject.evalExpression(text)
        if isinstance(q, (int, float)): q = App.Units.Quantity(q)
        if q.Unit == App.Units.Unit():
            q = q * App.Units.Quantity('1 ' + self._unit)
        if q.Unit != self._dimension or not math.isfinite(q.Value):
            raise ValueError('Enter a compatible unit and a finite value.')
        return q.Value

    def validate(self, text, pos):
        try:
            value = self.parse(text)
            state = QtGui.QValidator.Acceptable if self.minimum() <= value <= self.maximum() else QtGui.QValidator.Intermediate
        except Exception:
            state = QtGui.QValidator.Intermediate
        return state, text, pos

    def valueFromText(self, text):
        try:
            value = self.parse(text)
            match = re.fullmatch(r'''\s*[+-]?(?:\d+(?:[.,]\d*)?|[.,]\d+)(?:[eE][+-]?\d+)?\s*([A-Za-zµ°'"][A-Za-z0-9µ°'"/*^ .-]*)\s*''', text)
            if match:
                candidate = match[1].replace('°', 'deg')
                q = App.Units.Quantity('1 ' + candidate)
                if q.Unit == self._dimension: self._unit = candidate
            return value
        except Exception:
            return self.value()

    def textFromValue(self, value):
        factor = App.Units.Quantity('1 ' + self._unit).Value
        number = value/factor
        prefs = App.ParamGet('User parameter:BaseApp/Preferences/Units')
        places = prefs.GetInt('Decimals', 2)
        # getUserPreferred supports all native schemas, not an inch-only table.
        try:
            q = App.Units.Quantity(value, self._dimension)
            secondary = App.Units.schemaTranslate(q, prefs.GetInt('SecondarySchema', 3))
            primary = q.getUserPreferred()
            if abs(secondary[1]-factor)<1e-12 and abs(primary[1]-factor)>1e-12:
                places = prefs.GetInt('SecondaryDecimals', 3)
        except (AttributeError, TypeError):
            if self._unit == 'in' and prefs.GetInt('SecondarySchema', 3) == 3:
                places = prefs.GetInt('SecondaryDecimals', 3)
        places = max(0, min(16, places))
        result = f'{number:.{max(6, places)}f}'
        if abs(float(result)-number) > max(1e-12, abs(number)*1e-15):
            result = format(number, '.17g')
        else:
            while result.endswith('0') and len(result.rsplit('.',1)[-1])>places:
                result=result[:-1]
            result=result.rstrip('.')
        return result.replace('.', self.locale().decimalPoint()) + (' ' + self._unit if self._unit else '')

    def stepBy(self, steps):
        self.interpretText()
        before = self.value()
        self.setValue(before + steps*self.singleStep()*App.Units.Quantity('1 '+self._unit).Value)
        if self.value() != before: self.committed.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.committed.emit()


def restore(feature, fields):
    restore_units(fields, getattr(feature, 'QuantityPresentationUnits', {}))


def restore_units(fields, units):
    """Restore optional presentation metadata without changing physical values."""
    if not isinstance(units, dict): return
    for key, field in fields.items():
        unit = units.get(key)
        if unit:
            try:
                if App.Units.Quantity('1 '+unit).Unit == field._dimension:
                    field._unit = unit
                    field.lineEdit().setText(field.textFromValue(field.value()))
            except Exception: pass


def units(fields):
    return {key: field._unit for key, field in fields.items()}


def native_units(fields):
    return {key: field.property('presentationUnit') or '' for key, field in fields.items()}


def restore_native_units(fields, values):
    """Native unbound controls need their units saved by the owning task recipe."""
    for key, field in fields.items():
        unit = values.get(key, '') if isinstance(values, dict) else ''
        try:
            if unit and App.Units.Quantity('1 '+unit).Unit != App.Units.Quantity('1 '+field.property('unit')).Unit:
                unit = ''
        except (ValueError, TypeError, RuntimeError): unit = ''
        field.setProperty('presentationUnit', unit)
        field.setProperty('rawValue', field.property('rawValue'))


def save(feature, values):
    if not values: return
    if 'QuantityPresentationUnits' not in feature.PropertiesList:
        feature.addProperty('App::PropertyMap', 'QuantityPresentationUnits', 'Units', 'Explicit presentation units')
        feature.setEditorMode('QuantityPresentationUnits', 2)
    saved = dict(feature.QuantityPresentationUnits)
    saved.update(values)
    feature.QuantityPresentationUnits = saved
