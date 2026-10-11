// SPDX-License-Identifier: LGPL-2.1-or-later
#ifndef GUI_COMPONENT_GEOMETRY_H
#define GUI_COMPONENT_GEOMETRY_H

#include <optional>
#include <vector>
#include <App/Document.h>
#include <App/DocumentObject.h>
#include <App/DocumentObserver.h>
#include <Base/Interpreter.h>
#include <Base/PyObjectBase.h>

namespace Gui
{
// Consumer boundary only: never a global selection gate or a recompute hook.
inline std::string componentGeometryError(
    App::DocumentObject* consumer,
    const std::optional<std::vector<App::SubObjectT>>& inputs = std::nullopt
)
{
    if (!consumer) {
        return "The modeling object is no longer available";
    }
    bool component = false;
    for (auto obj : consumer->getDocument()->getObjects()) {
        if (obj->getPropertyByName("PlusFormat")) {
            component = true;
            break;
        }
    }
    if (!component) {
        return {};  // Original workbench behavior in ordinary FreeCAD documents.
    }
    Base::PyGILStateLocker lock;
    try {
        Py::Object references = Py::None();
        if (inputs) {
            Py::List list;
            for (const auto& ref : *inputs) {
                auto obj = ref.getObject();
                if (!obj) {
                    return "The geometry reference is no longer available";
                }
                list.append(Py::TupleN(Py::Object(obj->getPyObject(), true),
                                       Py::String(ref.getSubName())));
            }
            references = list;
        }
        Py::Module module(PyImport_ImportModule("freecad_plus.geometry"), true);
        module.callMemberFunction(
            "require_modeling_inputs",
            Py::TupleN(Py::Object(consumer->getPyObject(), true), references)
        );
    }
    catch (Py::Exception&) {
        Base::PyException error;
        return error.what();
    }
    return {};
}
}
#endif
