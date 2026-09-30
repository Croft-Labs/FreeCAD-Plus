# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *   Copyright (c) 2018 sliptonic <shopinthewoods@gmail.com>               *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

import FreeCAD
import Path

translate = FreeCAD.Qt.translate


def selection(verbose=False):
    """selection() ... return object if selected one operation or dressup.
    Allow to send error messages to Report view if verbose=True"""
    if FreeCAD.ActiveDocument and FreeCAD.GuiUp:
        import FreeCADGui

        selected = FreeCADGui.Selection.getSelection()
        if len(selected) != 1:
            if verbose:
                Path.Log.warning(translate("CAM_Dressup", "Select one toolpath object\n"))
            return None
        if not selected[0].isDerivedFrom("Path::Feature"):
            if verbose:
                Path.Log.warning(
                    translate("CAM_Dressup", "The selected object is not a toolpath\n")
                )
            return None
        if not isOp(selected[0]):
            if verbose:
                Path.Log.warning(
                    translate("CAM_Dressup", "The selected object is not an operation or dressup\n")
                )
            return None
        return selected[0]

    return None


def isOp(obj):
    """isOp(obj) ... return true if obj is operation or dressup."""
    if not getattr(obj, "Proxy", None):
        return False
    proxy = obj.Proxy.__module__
    return "Path.Op" in proxy or "Path.Dressup" in proxy


def _isDressup(path):
    """Recognize current proxies, retaining the legacy naming convention."""
    module = getattr(getattr(path, "Proxy", None), "__module__", "")
    if module.startswith("Path.Op."):
        # Operations have geometric Base links; they are not dressup chains.
        return False
    if module.startswith("Path.Dressup."):
        return True
    if "Dressup" not in getattr(path, "Name", "") or not hasattr(path, "Base"):
        return False
    if isinstance(path, FreeCAD.DocumentObject):
        # A legacy/native dressup has one object link, not a profile LinkSubList.
        return (path.isDerivedFrom("Path::Feature")
                and path.getTypeIdOfProperty("Base") == "App::PropertyLink")
    return True  # Preserve legacy duck-typed callers.


def baseOp(path):
    """Return the underlying operation, or None for a disconnected dressup.

    Reject cycles rather than recursing forever. Do not follow geometry references
    on ordinary operations, even when their names contain the word Dressup.
    """
    seen = set()
    while path is not None and _isDressup(path):
        if isinstance(path, FreeCAD.DocumentObject):
            key = (path.Document.Name, path.Name)
        else:
            key = id(path)
        if key in seen:
            raise ValueError("Cyclic CAM dressup base chain")
        seen.add(key)
        path = getattr(path, "Base", None)
    return path


def toolController(path, default=None):
    """toolController(path) ... return the tool controller from the base op."""
    return getattr(baseOp(path), "ToolController", default)
