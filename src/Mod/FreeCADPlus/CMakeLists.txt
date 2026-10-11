# SPDX-License-Identifier: LGPL-2.1-or-later
set(FreeCADPlus_SRCS
    Init.py
    TestComponentPilot.py
    TestLegacyConversion.py
    TestComponentHierarchy.py
    TestExternalDefinitions.py
    TestComponentPanel.py
    TestUnusedModels.py
    TestComponentWindows.py
    TestComponentVisibility.py
    TestComponentDisplay.py
    TestComponentRotate.py
    TestComponentMove.py
    TestComponentClipboard.py
    freecad_plus/__init__.py
    freecad_plus/display.py
    freecad_plus/document.py
    freecad_plus/conversion.py
    freecad_plus/hierarchy.py
    freecad_plus/legacy_hierarchy.py
    freecad_plus/external.py
    freecad_plus/panel.py
    freecad_plus/movement.py
    freecad_plus/isolation.py
    freecad_plus/editing.py
    freecad_plus/document_import.py
)
add_custom_target(FreeCADPlusScripts ALL SOURCES ${FreeCADPlus_SRCS})
fc_copy_sources(FreeCADPlusScripts "${CMAKE_BINARY_DIR}/Mod/FreeCADPlus" ${FreeCADPlus_SRCS})
install(FILES Init.py TestComponentPilot.py TestLegacyConversion.py TestComponentHierarchy.py TestExternalDefinitions.py TestComponentPanel.py TestUnusedModels.py TestComponentWindows.py TestComponentClipboard.py TestComponentMove.py TestComponentRotate.py TestComponentDisplay.py TestComponentVisibility.py DESTINATION Mod/FreeCADPlus)
install(FILES
    freecad_plus/__init__.py
    freecad_plus/display.py
    freecad_plus/document.py
    freecad_plus/conversion.py
    freecad_plus/hierarchy.py
    freecad_plus/legacy_hierarchy.py
    freecad_plus/external.py
    freecad_plus/panel.py
    freecad_plus/movement.py
    freecad_plus/isolation.py
    freecad_plus/editing.py
    freecad_plus/document_import.py
    DESTINATION Mod/FreeCADPlus/freecad_plus
)
