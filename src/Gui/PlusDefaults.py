# SPDX-License-Identifier: LGPL-2.1-or-later
"""Initial Plus preferences; explicit user choices remain editable and persist."""
import FreeCAD as App


def screenshot_defaults():
    """Native preference keys approved by the owner on October 2, 2026."""
    def rgba(rgb):
        return (int(rgb, 16) << 8) | 255

    colors = {
        "BackgroundColor": "f7f7f7", "HighlightColor": "ffff00",
        "SelectionColor": "ffbf00", "CbLabelColor": "212529",
        "CreateLineColor": "212529", "CursorTextColor": "212529",
        "CursorCrosshairColor": "212529", "FullyConstraintElementColor": "005500",
        "EditedEdgeColor": "00aa00", "FullyConstraintConstructionElementColor": "5555ff",
        "ConstructionColor": "00aaff", "FullyConstraintInternalAlignmentColor": "5555ff",
        "InternalAlignedGeoColor": "00aaff", "ExternalColor": "ff00ff",
        "ExternalDefiningColor": "cc3399", "FullyConstrainedColor": "000000",
        "InvalidSketchColor": "ff0000", "ConstrainedIcoColor": "0000ff",
        "ConstrainedDimColor": "0000ff", "NonDrivingConstrDimColor": "00aaff",
        "ExprBasedConstrDimColor": "ff00ff", "DeactivatedConstrDimColor": "868e96",
        "SketchVertexColor": "000000", "SketchEdgeColor": "000000",
    }
    defaults = {
        "General": [("String", "Language", "English"), ("Int", "UseLocaleFormatting", 0),
                    ("Bool", "SubstituteDecimalSeparator", False), ("Int", "ToolbarIconSize", 24),
                    ("Bool", "EnableCursorBlinking", True), ("Bool", "ShowSplasher", True)],
        "Units": [("Int", "UserSchema", App.Units.listSchemas().index("ImperialDecimal")),
                  ("Int", "Decimals", 3), ("Bool", "IgnoreProjectSchema", False)],
        "MainWindow": [("String", "Theme", "FreeCAD Light"), ("String", "QtStyle", "FreeCAD"),
                       ("String", "StyleSheet", "FreeCAD.qss"),
                       ("String", "OverlayActiveStyleSheet", "Freecad Overlay.qss"),
                       ("Bool", "TiledBackground", False)],
        "RecentFiles": [("Int", "RecentFiles", 4)],
        "Themes": [("Unsigned", "ThemeAccentColor1", 11272191),
                   ("Unsigned", "ThemeAccentColor2", 3027763199),
                   ("Unsigned", "ThemeAccentColor3", 1434171135)],
        "DockWindows": [("Bool", "ActivateOverlay", False)],
        "DockWindows/ComboView": [("Bool", "Enabled", True)],
        "DockWindows/TreeView": [("Bool", "Enabled", False)],
        "DockWindows/PropertyView": [("Bool", "Enabled", False)],
        "TreeView": [("Bool", k, False) for k in
                     ("PreSelection", "SyncView", "SyncSelection", "RecordSelection", "CheckBoxesSelection")]
                    + [("Unsigned", "TreeEditColor", rgba("00aaff")),
                       ("Unsigned", "TreeActiveColor", rgba("5bb413"))],
        "View": [("Bool", "EnablePreselection", True), ("Bool", "EnableSelection", True),
                 ("Float", "PickRadius", 5.0), ("Bool", "Simple", True),
                 ("Bool", "Gradient", False), ("Bool", "RadialGradient", False),
                 ("Int", "CbLabelTextSize", 13)]
                + [("Unsigned", k, rgba(v)) for k, v in colors.items()],
        "Mod/Sketcher/View": [("Float", k, 2.0) for k in
                              ("EdgeWidth", "ConstructionWidth", "InternalWidth", "ExternalWidth", "ExternalDefiningWidth")]
                             + [("Int", "EdgePattern", 0xffff), ("Int", "ConstructionPattern", 0xfcfc),
                                ("Int", "InternalPattern", 0xfcfc), ("Int", "ExternalPattern", 0xeeee),
                                ("Int", "ExternalDefiningPattern", 0xffff)],
        "Mod/Sketcher/General": [("Unsigned", "SketchFaceColor", rgba("cbdff4")),
                                 ("Bool", "ShowGrid", False)],
    }
    return defaults


def apply_screenshot_defaults(overwrite=False):
    """Seed fresh profiles; overwrite only for an explicitly requested reset."""
    for path, entries in screenshot_defaults().items():
        group = App.ParamGet("User parameter:BaseApp/Preferences/" + path)
        existing = {entry[1] for entry in (group.GetContents() or [])}
        for kind, name, value in entries:
            if overwrite or name not in existing:
                getattr(group, "Set" + kind)(name, value)


def initialize():
    apply_screenshot_defaults()
    view = App.ParamGet("User parameter:BaseApp/Preferences/View")
    if not view.GetString("NavigationStyle", ""):
        view.SetString("NavigationStyle", "Gui::BlenderNavigationStyle")
    units = App.ParamGet("User parameter:BaseApp/Preferences/Units")
    if units.GetInt("UserSchema", -1) < 0:
        imperial = App.Units.listSchemas().index("ImperialDecimal")
        units.SetInt("UserSchema", imperial)
        App.Units.setSchema(imperial)
    App.Units.setSchema(units.GetInt("UserSchema"))
