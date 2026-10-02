# SPDX-License-Identifier: LGPL-2.1-or-later
"""Initial Plus preferences; explicit user choices remain editable and persist."""
import FreeCAD as App


def initialize():
    view = App.ParamGet("User parameter:BaseApp/Preferences/View")
    if not view.GetString("NavigationStyle", ""):
        view.SetString("NavigationStyle", "Gui::BlenderNavigationStyle")
    units = App.ParamGet("User parameter:BaseApp/Preferences/Units")
    if units.GetInt("UserSchema", -1) < 0:
        imperial = App.Units.listSchemas().index("ImperialDecimal")
        units.SetInt("UserSchema", imperial)
        App.Units.setSchema(imperial)
