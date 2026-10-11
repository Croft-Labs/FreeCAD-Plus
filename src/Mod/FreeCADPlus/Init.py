# SPDX-License-Identifier: LGPL-2.1-or-later
import FreeCAD

FreeCAD.addImportType("FreeCAD Plus component (*.cadprt)", "freecad_plus.document_import")

FreeCAD.__unit_test__ += ["TestComponentPilot", "TestLegacyConversion", "TestComponentHierarchy", "TestExternalDefinitions", "TestComponentPanel", "TestUnusedModels", "TestComponentWindows", "TestComponentClipboard", "TestComponentMove", "TestComponentRotate", "TestComponentDisplay"]
