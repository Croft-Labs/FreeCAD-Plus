# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native create/edit task; preview never mutates a document."""
import json
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtWidgets, QtGui
from pivy import coin
from . import component_add, document, editing, hierarchy, instance_patterns as patterns, panel
from .instance_quantity_ui import InstanceForm
from . import isolation
from .quantity_fields import native_units, restore_native_units

_active = None


class InstanceTask(QtCore.QObject):
    def __init__(self, definitions=(), label=None, opened=(), pattern=None, row=None, initial=None):
        super().__init__()
        owner, self.expected = component_add.target()
        self.doc = App.ActiveDocument; self.view = Gui.activeDocument().activeView()
        self.pattern_ref = panel.identity(pattern) if pattern else None
        self.owner = patterns.owner_of(pattern) if pattern else owner
        self.owner_doc = self.owner.Document
        self.owner_ref = panel.identity(self.owner)
        current_assembly = component_add.active_assembly()
        self.assembly_ref = panel.identity(current_assembly) if current_assembly else None
        self.frame_row = row
        self.revision = (pattern.Configuration, tuple(panel.identity(o) for o in pattern.Members)) if pattern else None
        if pattern: definitions = [seed.LinkedObject for seed in pattern.Seeds]
        self.parts = tuple(panel.identity(p) for p in definitions); self.label = label
        self.opened = set(opened); self.refs = {}; self.collecting = None
        self.closed = False; self.busy = True; self.overlay = None
        self.scene = self.view.getSceneGraph()
        self.form = InstanceForm(self.owner, [p.Label for p in definitions] if label is None else [label], bool(pattern))
        self.timer = QtCore.QTimer(self); self.timer.setSingleShot(True); self.timer.timeout.connect(self.refresh)
        self.pick_timer = QtCore.QTimer(self); self.pick_timer.setSingleShot(True); self.pick_timer.timeout.connect(self.pick)
        if pattern: self.load(json.loads(pattern.Configuration), pattern.References)
        elif initial: self.load(*initial)
        self.form.change.clicked.connect(self.change_parts)
        for widget in self.form.findChildren(QtWidgets.QComboBox): widget.currentIndexChanged.connect(self.schedule)
        for widget in self.form.findChildren(QtWidgets.QSpinBox): widget.valueChanged.connect(self.schedule)
        for widget in self.form.findChildren(QtWidgets.QCheckBox): widget.toggled.connect(self.schedule)
        for widget in self.form.units.values():
            widget.valueChanged.connect(self.schedule); widget.parseError.connect(self.schedule)
        for widget in self.form.vectors.values(): widget.textChanged.connect(self.schedule)
        for key, widget in self.form.references.items():
            widget.activated.connect(lambda key=key: self.collect(key))
            widget.cleared.connect(lambda key=key: self.clear_reference(key))
        App.addDocumentObserver(self); Gui.Selection.addObserver(self, 0)
        editing.add_context_observer(self.schedule)
        self.mdi = Gui.getMainWindow().findChild(QtWidgets.QMdiArea)
        if self.mdi: self.mdi.subWindowActivated.connect(self.schedule)
        self.style_actions = [a for a in Gui.getMainWindow().findChildren(QtGui.QAction)
                              if a.objectName().startswith('Std_DrawStyle')]
        for action in self.style_actions: action.triggered.connect(self.schedule)
        self.busy = False

    def check(self):
        if self.closed: raise ValueError('This instance task is closed')
        if component_add.target(allow_task=True)[1] != self.expected:
            raise ValueError('The edited component or file tab changed. Cancel and reopen the task.')
        if panel.lookup(self.owner_ref) != self.owner: raise ValueError('The destination component changed')
        current_assembly = component_add.active_assembly()
        if not self.pattern_ref and (panel.identity(current_assembly) if current_assembly else None) != self.assembly_ref:
            raise ValueError('The active assembly changed. Cancel and reopen the task.')
        pattern = panel.lookup(self.pattern_ref) if self.pattern_ref else None
        if pattern and (pattern.Configuration, tuple(panel.identity(o) for o in pattern.Members)) != self.revision:
            raise ValueError('The pattern changed. Cancel and reopen Edit instance pattern.')
        return pattern

    def load(self, config, refs):
        f = self.form; mode = config['mode']; f.mode.setCurrentText(mode)
        f.count.setValue(config.get('count', 1)); f.columns.setValue(config.get('columns', 3)); f.rows.setValue(config.get('rows', 2))
        for widget, value in zip(f.positions[mode.lower()], config.get('position', (0, 0, 0))): widget.setProperty('rawValue', value)
        names = {'Linear': [('linear', 'direction')], 'Grid': [('columns', 'direction'), ('rows', 'row_direction')],
                 'Circular': [('circular', 'direction')]}.get(mode, [])
        mapping = dict(zip(config.get('reference_keys', []), refs))
        for key, axis in names:
            choice = config.get('direction_choices', {}).get(key)
            if choice is None:
                axes = {'Parent X': [1, 0, 0], 'Parent Y': [0, 1, 0], 'Parent Z': [0, 0, 1]}
                choice = 'Pick edge / axis' if axis in mapping else next(
                    (label for label, value in axes.items() if list(config[axis]) == value), 'Enter vector')
            if f.directions[key].findText(choice) < 0:
                raise ValueError('This saved direction needs an edge or axis reference before editing')
            f.directions[key].setCurrentText(choice)
            if choice == 'Enter vector': f.vectors[key].setText(', '.join(str(v) for v in config[axis]))
            if axis in mapping:
                self.refs[key] = mapping[axis]; self.show_reference(key)
        values = {'linear_spacing': config.get('spacing', 25), 'column_spacing': config.get('spacing', 25),
                  'row_spacing': config.get('row_spacing', 20), 'radius': config.get('radius', 50),
                  'angle': config.get('angle', 0), 'angular_spacing': config.get('angular_spacing', 60)}
        for key, value in values.items(): f.units[key].setProperty('rawValue', value)
        f.reverse.setChecked(config.get('reverse', False)); f.full.setChecked(config.get('full', True))
        f.orientation.setCurrentIndex(1 if config.get('rotate', False) else 0)
        restore_native_units(f.units, config.get('units', {}))

    def configuration(self):
        f = self.form; mode = f.mode.currentText()
        config = dict(mode=mode, count=f.count.value(), position=[f.value(w) for w in f.positions[mode.lower()]],
                      reference_keys=[], direction_choices={}, units=native_units(f.units))
        refs = []
        def direction(key, name):
            choice = f.directions[key].currentText(); config['direction_choices'][key] = choice
            if choice == 'Pick edge / axis':
                if key not in self.refs: raise ValueError('Pick the ' + key + ' edge or axis')
                config['reference_keys'].append(name); refs.append(self.refs[key])
                config[name] = list(patterns.reference_direction(self.owner, self.refs[key],
                                    panel.lookup(self.pattern_ref).Members if self.pattern_ref else ()))
            elif choice == 'Enter vector': config[name] = [float(v.strip()) for v in f.vectors[key].text().split(',')]
            else: config[name] = {'Parent X': [1, 0, 0], 'Parent Y': [0, 1, 0], 'Parent Z': [0, 0, 1]}[choice]
        if mode == 'Linear':
            direction('linear', 'direction'); config.update(spacing=f.value(f.units['linear_spacing']), reverse=f.reverse.isChecked())
        elif mode == 'Grid':
            direction('columns', 'direction'); direction('rows', 'row_direction')
            config.update(columns=f.columns.value(), rows=f.rows.value(), spacing=f.value(f.units['column_spacing']),
                          row_spacing=f.value(f.units['row_spacing']))
        elif mode == 'Circular':
            direction('circular', 'direction')
            config.update(radius=f.value(f.units['radius']), angle=f.value(f.units['angle']), full=f.full.isChecked(),
                          angular_spacing=f.value(f.units['angular_spacing']), rotate=f.orientation.currentIndex() == 1)
        return config, refs

    def collect(self, key):
        self.collecting = key; Gui.Selection.clearSelection()
        for name, widget in self.form.references.items():
            widget.setStyleSheet('QListWidget { border: 2px solid #2388cf; }' if name == key else '')

    def clear_reference(self, key):
        self.refs.pop(key, None); self.form.references[key].clear(); self.schedule()

    def show_reference(self, key):
        obj, subs = self.refs[key]; widget = self.form.references[key]; widget.clear()
        widget.addItem(obj.Label + (': ' + subs[0] if subs[0] else ''))

    def addSelection(self, *args):
        if self.collecting and not self.closed: self.pick_timer.start(0)

    def pick(self):
        if self.closed or not self.collecting: return
        try:
            self.check()
            from .selection_list import removing
            if removing(): self.clear_reference(self.collecting); return
            selections = [(e.Object, sub) for e in Gui.Selection.getSelectionEx('', 0) for sub in e.SubElementNames or ('',)]
            if not selections: return
            if len(selections) != 1: raise ValueError('Select one straight edge or axis')
            obj, sub = selections[0]
            if obj == self.owner: local = sub
            elif obj == document.validate(self.doc) and self.expected[4] and not self.pattern_ref:
                prefix = hierarchy.subname(tuple(panel.lookup(r) for r in self.expected[4]))
                if not sub.startswith(prefix): raise ValueError('Choose geometry in the destination component')
                local = sub[len(prefix):]
            elif self.frame_row and obj == document.validate(self.doc) and self.frame_row.path:
                prefix = hierarchy.subname(tuple(panel.lookup(r) for r in self.frame_row.path[:-1]))
                if not sub.startswith(prefix): raise ValueError('Choose geometry in the destination component')
                local = sub[len(prefix):]
            else:
                route = document.owned_path(self.owner, obj)
                if route is None: raise ValueError('Choose geometry in the destination component')
                local = ''.join(o.Name + '.' for o in route) + sub
            name, _, tail = local.partition('.')
            child = next((o for o in [self.owner.Origin, *self.owner.Group] if o.Name == name), None)
            ref = (child, [tail])
            patterns.reference_direction(self.owner, ref, panel.lookup(self.pattern_ref).Members if self.pattern_ref else ())
            if not child.Visibility: raise ValueError('Choose a visible edge or axis')
            self.refs[self.collecting] = ref; self.show_reference(self.collecting); self.refresh()
        except (ValueError, RuntimeError, ReferenceError) as error: self.form.status.setError(str(error))

    def frame(self):
        if self.frame_row:
            route = tuple(panel.lookup(r) for r in self.frame_row.path[:-1])
            if self.frame_row.anchor:
                anchor = panel.lookup(self.frame_row.anchor)
                return anchor.getSubObject(hierarchy.subname(route), 3) if route else anchor.Placement
        else: route = tuple(panel.lookup(r) for r in self.expected[4])
        return hierarchy.world_placement(self.doc, route) if route else self.owner.Placement

    def clear_preview(self):
        if self.overlay is not None:
            if self.scene.findChild(self.overlay) >= 0: self.scene.removeChild(self.overlay)
            self.overlay = None

    def refresh(self, *args):
        if self.closed or self.busy: return
        self.clear_preview()
        try:
            pattern = self.check(); config, refs = self.configuration()
            definitions = [panel.lookup(ref) for ref in self.parts]
            if pattern: _, values, _, _ = patterns.check_edit(pattern, config, refs)
            else:
                patterns.prepare(self.owner, definitions, self.label)
                values = patterns.placements(patterns.resolved_config(self.owner, config, refs))
            total = len(values) * (len(definitions) or 1); patterns.count(total)
            self.form.summary.setText(str(total) + (' instances in pattern' if pattern else ' new instances')
                                      + ' · ' + str(len(definitions) or 1) + ' shared component(s)')
            self.form.status.setText('Ready. One Undo step.')
            if not self.form.preview.isChecked(): return
            overlay = coin.SoSeparator(); pick = coin.SoPickStyle(); pick.style = coin.SoPickStyle.UNPICKABLE
            pick.setOverride(True); overlay.addChild(pick)
            frame = self.frame()
            for definition in definitions:
                # Copy the native view-provider tree after its draw-style update,
                # retaining its real edge/face switches and original face colors.
                geometry = isolation._preview(definition).copy()
                geometry.whichChild = coin.SO_SWITCH_ALL
                search = coin.SoSearchAction(); search.setType(coin.SoMaterial.getClassTypeId())
                search.setInterest(coin.SoSearchAction.ALL); search.setSearchingAll(True); search.apply(geometry)
                for path in search.getPaths():
                    material = path.getTail()
                    if str(material.getName()) == 'ShapeMaterial':
                        values_alpha = [max(.5, float(material.transparency[i]))
                                        for i in range(material.transparency.getNum())]
                        material.transparency.setValues(0, len(values_alpha), values_alpha)
                for value in values:
                    node = coin.SoSeparator(); transform = coin.SoTransform(); placement = frame.multiply(value)
                    transform.translation.setValue(*tuple(placement.Base)); transform.rotation.setValue(*placement.Rotation.Q)
                    node.addChild(transform); node.addChild(geometry); overlay.addChild(node)
            self.scene.addChild(overlay); self.overlay = overlay
        except (ValueError, OSError, RuntimeError, ReferenceError, TypeError) as error:
            self.form.status.setError(str(error))

    def schedule(self, *args):
        if not self.closed and not self.busy: self.timer.start(0)

    slotChangedObject = schedule
    slotDeletedObject = schedule
    slotRecomputedDocument = schedule
    slotActivateDocument = schedule

    def slotDeletedDocument(self, doc):
        if doc in (self.doc, self.owner_doc): self.finish()

    def accept(self):
        try:
            pattern = self.check(); config, refs = self.configuration(); self.busy = True
            if pattern: self.created = patterns.update(pattern, config, refs)
            else:
                self.created, self.created_pattern = patterns.create(self.owner, [panel.lookup(r) for r in self.parts], config, label=self.label, refs=refs)
            if self.owner.Document != self.doc: self.doc.recompute()
        except (ValueError, OSError, RuntimeError, ReferenceError, TypeError) as error:
            self.form.status.setError(str(error)); return False
        finally: self.busy = False
        self.finish()
        if panel._panel: panel._panel.refresh()
        return True

    def change_parts(self):
        try: self.check()
        except (ValueError, RuntimeError) as error: self.form.status.setError(str(error)); return
        try: initial = self.configuration()
        except (ValueError, RuntimeError, AttributeError): initial = None
        opened = set(self.opened); self.opened.clear(); self.finish()
        QtCore.QTimer.singleShot(0, lambda: component_add.open_picker(Gui.getMainWindow(), self.label is not None,
                               selected=self.parts, label=self.label, opened=opened, initial=initial))

    def finish(self):
        global _active
        if self.closed: return
        self.closed = True; self.clear_preview(); self.timer.stop(); self.pick_timer.stop()
        for action in self.style_actions:
            try: action.triggered.disconnect(self.schedule)
            except RuntimeError: pass
        App.removeDocumentObserver(self); Gui.Selection.removeObserver(self); editing.remove_context_observer(self.schedule)
        if self.mdi:
            try: self.mdi.subWindowActivated.disconnect(self.schedule)
            except RuntimeError: pass
        if _active is self: _active = None; Gui.Control.closeDialog()
        remaining = set(self.opened)
        while remaining:
            closable = [n for n in remaining if n not in App.listDocuments() or not App.getDocument(n).InList]
            if not closable: break
            for name in closable:
                if name in App.listDocuments(): App.closeDocument(name)
                remaining.remove(name)
        self.deleteLater()

    def reject(self): self.finish(); return True
    def getStandardButtons(self): return (QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel).value
    def isAllowedAlterDocument(self): return False
    def isAllowedAlterSelection(self): return True
    def isAllowedAlterView(self): return True


def open_task(definitions=(), label=None, opened=(), pattern=None, row=None, initial=None):
    global _active
    task = InstanceTask(definitions, label, opened, pattern, row, initial); _active = task
    try:
        Gui.Control.showDialog(task); task.refresh()
    except Exception: task.finish(); raise
    return task


def edit_row(row):
    if row.kind != 'occurrence': raise ValueError('Choose an individual pattern instance')
    panel._panel._checked(row)
    pattern = patterns.controller(panel.lookup(row.path[-1]))
    if pattern is None: raise ValueError('This instance is not in a pattern')
    return open_task(pattern=pattern, row=row)
