# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *   Copyright (c) 2023 Werner Mayer <wmayer[at]users.sourceforge.net>     *
# *                                                                         *
# *   This file is part of FreeCAD.                                         *
# *                                                                         *
# *   FreeCAD is free software: you can redistribute it and/or modify it    *
# *   under the terms of the GNU Lesser General Public License as           *
# *   published by the Free Software Foundation, either version 2.1 of the  *
# *   License, or (at your option) any later version.                       *
# *                                                                         *
# *   FreeCAD is distributed in the hope that it will be useful, but        *
# *   WITHOUT ANY WARRANTY; without even the implied warranty of            *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU      *
# *   Lesser General Public License for more details.                       *
# *                                                                         *
# *   You should have received a copy of the GNU Lesser General Public      *
# *   License along with FreeCAD. If not, see                               *
# *   <https://www.gnu.org/licenses/>.                                      *
# *                                                                         *
# ***************************************************************************

__title__ = "BOPTools.BOPFeatures module"
__author__ = "Werner Mayer"
__url__ = "https://www.freecad.org"
__doc__ = "Helper class to create the features for Boolean operations."

import FreeCAD
import Part


class BOPFeatures:
    def __init__(self, doc):
        self.doc = doc

    def component_target(self, inputNames=None):
        if any("PlusFormat" in obj.PropertiesList for obj in self.doc.Objects):
            from freecad_plus.geometry import require_part_boolean_inputs
            return require_part_boolean_inputs(
                self.doc, None if inputNames is None else
                [(self.doc.getObject(name), "") for name in inputNames])
        return None

    def make_section(self, inputNames):
        component = self.component_target(inputNames)
        obj = self.doc.addObject("Part::Section", "Section")
        obj.Base = self.doc.getObject(inputNames[0])
        obj.Tool = self.doc.getObject(inputNames[1])
        self.copy_visual_attributes(obj, obj.Base)
        target = self.move_input_objects([obj.Base, obj.Tool], component)
        if target:
            target.addObject(obj)
        return obj

    def make_cut(self, inputNames):
        component = self.component_target(inputNames)
        obj = self.doc.addObject("Part::Cut", "Cut")
        obj.Base = self.doc.getObject(inputNames[0])
        obj.Tool = self.doc.getObject(inputNames[1])
        self.copy_visual_attributes(obj, obj.Base)
        target = self.move_input_objects([obj.Base, obj.Tool], component)
        if target:
            target.addObject(obj)
        return obj

    def make_common(self, inputNames):
        component = self.component_target(inputNames)
        obj = self.doc.addObject("Part::Common", "Common")
        obj.Base = self.doc.getObject(inputNames[0])
        obj.Tool = self.doc.getObject(inputNames[1])
        self.copy_visual_attributes(obj, obj.Base)
        target = self.move_input_objects([obj.Base, obj.Tool], component)
        if target:
            target.addObject(obj)
        return obj

    def make_multi_common(self, inputNames):
        component = self.component_target(inputNames)
        obj = self.doc.addObject("Part::MultiCommon", "Common")
        obj.Shapes = [self.doc.getObject(name) for name in inputNames]
        self.copy_visual_attributes(obj, obj.Shapes[0])
        target = self.move_input_objects(obj.Shapes, component)
        if target:
            target.addObject(obj)
        return obj

    def make_fuse(self, inputNames):
        component = self.component_target(inputNames)
        obj = self.doc.addObject("Part::Fuse", "Fusion")
        obj.Base = self.doc.getObject(inputNames[0])
        obj.Tool = self.doc.getObject(inputNames[1])
        self.copy_visual_attributes(obj, obj.Base)
        target = self.move_input_objects([obj.Base, obj.Tool], component)
        if target:
            target.addObject(obj)
        return obj

    def make_multi_fuse(self, inputNames):
        component = self.component_target(inputNames)
        obj = self.doc.addObject("Part::MultiFuse", "Fusion")
        obj.Shapes = [self.doc.getObject(name) for name in inputNames]
        self.copy_visual_attributes(obj, obj.Shapes[0])
        target = self.move_input_objects(obj.Shapes, component)
        if target:
            target.addObject(obj)
        return obj

    def move_input_objects(self, objects, component=None):
        if component is not None:
            # Native Part dependencies are references, not component ownership.
            # Keep the input features in their original containers and own only
            # the new result in the edited definition.
            for obj in objects:
                obj.Visibility = False
            return component
        targetGroup = None
        for obj in objects:
            obj.Visibility = False
            parent = obj.getParent()
            if parent:
                parent.removeObject(obj)
                targetGroup = parent
        return targetGroup

    def copy_visual_attributes(self, target, source):
        if target.ViewObject:
            displayMode = source.ViewObject.DisplayMode
            src = source
            while displayMode == "Link":
                if getattr(src, "LinkedObject", None):
                    src = src.LinkedObject
                elif getattr(src, "Base", None):
                    # Draft Link array
                    src = src.Base
                else:
                    break
                if not hasattr(src, "ViewObject"):
                    break
                displayMode = src.ViewObject.DisplayMode
            if displayMode in target.ViewObject.getEnumerationsOfProperty("DisplayMode"):
                target.ViewObject.DisplayMode = displayMode


def prepare_component_command():
    """Preflight unresolved GUI inputs before opening a split/join transaction."""
    import FreeCADGui
    from PySide import QtGui

    try:
        return True, BOPFeatures(FreeCAD.ActiveDocument).component_target()
    except ValueError as error:
        QtGui.QMessageBox.warning(
            FreeCADGui.getMainWindow(),
            FreeCAD.Qt.translate("Part", "Ineligible geometry"), str(error))
        return False, None


def own_command_results(component, objects_expression):
    """Record ownership in the native command's macro and transaction.

    objects_expression is an internal Python expression naming the result list.
    Ordinary legacy commands keep their original parenting.
    """
    if component is not None:
        import FreeCADGui
        # Related filters can expand to the same native coordinate-system links.
        # Insert sequentially so each native call sees the updated membership.
        FreeCADGui.doCommand(
            "for __component_result in {}: "
            "App.getDocument({!r}).getObject({!r}).addObject(__component_result)".format(
                objects_expression, component.Document.Name, component.Name))
        FreeCADGui.doCommand("globals().pop('__component_result', None)")
