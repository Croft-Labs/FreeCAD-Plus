// SPDX-License-Identifier: LGPL-2.1-or-later
#ifndef PARTGUI_COMPONENT_BOOLEAN_H
#define PARTGUI_COMPONENT_BOOLEAN_H

#include <Gui/ComponentGeometry.h>

namespace PartGui
{
inline bool isComponentBooleanDocument(App::Document* doc)
{
    if (doc) {
        for (auto obj : doc->getObjects()) {
            if (obj->getPropertyByName("PlusFormat")) {
                return true;
            }
        }
    }
    return false;
}

inline std::string componentBooleanError(
    App::Document* doc,
    const std::optional<std::vector<App::SubObjectT>>& inputs = std::nullopt)
{
    if (!isComponentBooleanDocument(doc)) {
        return {};
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
                list.append(Py::TupleN(Py::Object(obj->getPyObject(), true), Py::String(ref.getSubName())));
            }
            references = list;
        }
        Py::Module module(PyImport_ImportModule("freecad_plus.geometry"), true);
        module.callMemberFunction("require_part_boolean_inputs",
                                  Py::TupleN(Py::Object(doc->getPyObject(), true), references));
    }
    catch (Py::Exception&) {
        Base::PyException error;
        return error.what();
    }
    return {};
}
}
#endif
