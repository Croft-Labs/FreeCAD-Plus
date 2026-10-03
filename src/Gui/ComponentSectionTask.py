# SPDX-License-Identifier: LGPL-2.1-or-later
"""Shared ordered-section and sketch-curve collection for Loft and Pipe."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from freecad.gui.ComponentOperationTask import OperationTask


def tr(text):
    return App.Qt.translate("ComponentSection", text)


class SectionTask(OperationTask):
    def build_collectors(self, main, title):
        self.ordered = QtWidgets.QListWidget()
        self.ordered.model().rowsInserted.connect(self.update_curve_display)
        self.ordered.model().rowsRemoved.connect(self.update_curve_display)
        self.ordered.setMinimumHeight(85)
        self.ordered.setMaximumHeight(125)
        main.addRow(tr(title), self.ordered)
        self.buttons(main, (("Remove section", self.remove_section), ("Clear sections", self.clear_sections)))
        self.build_profile_collector(main, sections=True)
        self.buttons(main, (("Append section", self.append_section), ("Replace section", self.replace_section)))

    def curve_display_inputs(self):
        sections = [self.ordered.item(i).data(QtCore.Qt.UserRole) for i in range(self.ordered.count())]
        return sections + super().curve_display_inputs()

    def add_row(self, obj, elements, index=None):
        label = obj.Label + " / " + (", ".join(elements) if elements is not None else tr("Whole profile"))
        row = QtWidgets.QListWidgetItem(label)
        row.setData(QtCore.Qt.UserRole, (obj.Name, elements))
        if index is None:
            self.ordered.addItem(row)
        else:
            self.ordered.insertItem(index, row)

    def collect_section(self, replace=False):
        try:
            source = self.component.Document.getObject(self.profile.currentData() or "")
            elements = None if self.whole_profile else self.curve_names()
            self.backend.section_shape(self.component, source, elements, self.operation)
            index = self.ordered.currentRow()
            if replace and index < 0:
                raise ValueError(tr("Select the section to replace."))
            if replace:
                self.ordered.takeItem(index)
            self.add_row(source, elements, index if replace else None)
            self.changed()
        except Exception as error:
            self.status.setText(str(error))

    def append_section(self):
        self.collect_section()

    def replace_section(self):
        self.collect_section(True)

    def remove_section(self):
        row = self.ordered.currentRow()
        if row >= 0:
            self.ordered.takeItem(row)
            self.changed()

    def clear_sections(self):
        self.ordered.clear()
        self.changed()

    def move_section(self, offset):
        row = self.ordered.currentRow()
        if 0 <= row + offset < self.ordered.count() and row >= 0:
            item = self.ordered.takeItem(row)
            self.ordered.insertItem(row + offset, item)
            self.ordered.setCurrentRow(row + offset)
            self.changed()

    def reverse_sections(self):
        rows = [self.ordered.takeItem(0) for _ in range(self.ordered.count())]
        for row in reversed(rows):
            self.ordered.addItem(row)
        self.changed()

    def inspect_section(self, row):
        if row < 0:
            return
        name, elements = self.ordered.item(row).data(QtCore.Qt.UserRole)
        self.profile.setCurrentIndex(self.profile.findData(name))
        if elements is not None:
            self.set_curves(elements, False)
        else:
            self.profile_changed()

    def use_selection(self, picks=None, toggle=False):
        from freecad.gui import ComponentSelection as Selection
        picks = picks if isinstance(picks, list) else [(p.item, p.element) for p in Selection.selected(self.component, Gui.Selection.getSelectionEx("*", 0)) if p.item is not None]
        # Each section has its own curve collector; choosing another source starts a new draft.
        if picks and len({obj for obj, element in picks}) == 1:
            obj = picks[0][0]
            index = self.profile.findData(obj.Name)
            if index >= 0:
                self.profile.setCurrentIndex(index)
                elements = [element for source, element in picks if element]
                if len(elements) == 1 and elements[0].startswith("Vertex"):
                    self.collect_curves(elements, toggle)
                    return
        super().use_selection(picks, toggle)
