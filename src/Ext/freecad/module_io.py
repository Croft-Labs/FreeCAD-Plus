# SPDX-License-Identifier: LGPL-2.1-or-later

from FreeCAD import Base
import importlib

def OpenInsertObject(importerName, objectPath, importMethod, docName = ""):
    try:
        importArgs = []
        importKwargs = {}

        importerModule = importlib.import_module(importerName)

        if docName:
            importArgs.append(docName)
        if hasattr(importerModule, "importOptions"):
            importKwargs["options"] = importerModule.importOptions(objectPath)

        # Native mesh readers create document-level objects. Plus owns modeling
        # content in the edited component, including meshes in its History.
        if importerName == "Mesh" and importMethod == "insert" and docName:
            import FreeCAD as App
            doc = App.getDocument(docName)
            if doc and any("PlusFormat" in obj.PropertiesList for obj in doc.Objects):
                from freecad_plus.document_import import insert_mesh
                return insert_mesh(objectPath, doc, importerModule.insert, **importKwargs)

        getattr(importerModule, importMethod)(objectPath, *importArgs, **importKwargs)
    except Base.AbortIOException:
        pass
