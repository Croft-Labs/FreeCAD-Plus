# SPDX-License-Identifier: LGPL-2.1-or-later
"""Common modeling lifecycle with axis/face reference picking."""
import FreeCAD as App
from freecad.gui.ComponentExtrudeTask import ExtrudeTask


def tr(text):
    return App.Qt.translate("ComponentOperation", text)


class OperationTask(ExtrudeTask):
    def begin_reference_pick(self, field):
        self.reference_pick = field
        self.status.setText(tr("Pick a local axis, edge, plane or limiting face."))

    def addSelection(self, document, name, subname, *args):
        if self.reference_pick is not None:
            import ComponentModel as Model
            doc = App.listDocuments().get(document)
            base = doc.getObject(name) if doc else None
            item = base.getSubObject(subname, 1) if base and subname else base
            if item and (Model.owner(item) == self.component or item in self.component.Origin.OriginFeatures):
                element = subname.rsplit(".", 1)[-1]
                self.reference_pick.setText(item.Name + ("." + element if element.startswith(("Face", "Edge")) else ""))
                self.reference_pick = None
                return
        super().addSelection(document, name, subname, *args)
