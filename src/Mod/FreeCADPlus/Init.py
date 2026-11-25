# SPDX-License-Identifier: LGPL-2.1-or-later
import FreeCAD
from freecad_plus import naming
naming.install()

FreeCAD.addImportType("FreeCAD Plus document (*.cadprt)", "freecad_plus.document_import")
FreeCAD.__unit_test__ += ["TestFeatureCenteredModeling"]
FreeCAD.__unit_test__ += ["TestFileWorkflows"]
FreeCAD.__unit_test__ += ["TestComponentNames"]
FreeCAD.__unit_test__ += ["TestInstanceDisplay"]
FreeCAD.__unit_test__ += ["TestInstanceQuantity"]

FreeCAD.__unit_test__ += ["TestPlusToolbars", "TestComponentPilot", "TestLegacyConversion", "TestLegacyBooleanConversion", "TestComponentHierarchy", "TestExternalDefinitions", "TestComponentPanel", "TestComponentRename", "TestComponentImport", "TestUnusedModels", "TestComponentWindows", "TestComponentClipboard", "TestMoveWorkflow", "TestComponentDisplay", "TestComponentVisibility", "TestComponentFading", "TestComponentBodiesOnly", "TestComponentEligibility", "TestComponentExport", "TestComponentExternalExport", "TestComponentModeling", "TestComponentReferences", "TestComponentInputEditors", "TestComponentSweepInputs", "TestComponentDressUpInputs", "TestComponentCommandInputs", "TestComponentBooleanOwnership", "TestComponentBooleanInputs", "TestPartBooleanInputs"]
