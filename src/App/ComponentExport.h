// SPDX-License-Identifier: LGPL-2.1-or-later
#ifndef APP_COMPONENT_EXPORT_H
#define APP_COMPONENT_EXPORT_H

#include <CXX/Objects.hxx>
#include <App/DocumentObject.h>
#include <App/DocumentObjectPy.h>

namespace App
{
// Keeps temporary component output alive until a synchronous writer has finished.
// Ordinary inputs do not import the Part workbench's component policy module.
class ComponentExport
{
public:
    explicit ComponentExport(PyObject* objects)
        : output(objects), context(Py::None())
    {
        Py::Sequence list(objects);
        bool component = false;
        for (const auto& entry : list) {
            PyObject* item = entry.ptr();
            if (PyTuple_Check(item) && PyTuple_Size(item) == 2) {
                item = PyTuple_GetItem(item, 0);
            }
            if (PyObject_TypeCheck(item, &DocumentObjectPy::Type)) {
                auto* object = static_cast<DocumentObjectPy*>(item)->getDocumentObjectPtr();
                if (object->getPropertyByName("ComponentRole")) {
                    component = true;
                    break;
                }
            }
        }
        if (!component) {
            return;
        }
        Py::Module module("ComponentModel");
        Py::Tuple args(1);
        args.setItem(0, output);
        context = Py::Callable(module.getAttr("export_objects")).apply(args);
        output = Py::Callable(context.getAttr("__enter__")).apply(Py::Tuple());
        entered = true;
    }

    ComponentExport(const ComponentExport&) = delete;
    ComponentExport& operator=(const ComponentExport&) = delete;

    ~ComponentExport()
    {
        if (!entered) {
            return;
        }
        // Preserve a writer's Python error while closing the scratch document.
        PyObject *type = nullptr, *value = nullptr, *trace = nullptr;
        PyErr_Fetch(&type, &value, &trace);
        PyObject* result = PyObject_CallMethod(context.ptr(), "__exit__", "OOO",
                                              Py_None, Py_None, Py_None);
        if (!result) {
            PyErr_WriteUnraisable(context.ptr());
        }
        else {
            Py_DECREF(result);
        }
        PyErr_Restore(type, value, trace);
    }

    PyObject* objects() const { return output.ptr(); }

private:
    Py::Object output;
    Py::Object context;
    bool entered = false;
};
}

#endif
