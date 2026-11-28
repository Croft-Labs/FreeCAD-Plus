// SPDX-License-Identifier: LGPL-2.1-or-later
// Dependent pattern curves are generated between acyclic native solve phases.
#include <Python.h>
#include <set>
#include <map>
#include <memory>
#include <Base/Interpreter.h>
#include <Base/Exception.h>
#include <Base/Console.h>
#include <Base/Tools.h>
#include <Mod/Part/App/GeometryPy.h>
#include "SketchObject.h"

using namespace Sketcher;

bool SketchObject::hasLinkedPatterns() const
{
    for (const auto* geo : Geometry.getValues())
        if (GeometryFacade::getFacade(geo)->testGeometryMode(GeometryMode::PatternGenerated))
            return true;
    return false;
}

void SketchObject::prepareLinkedPatternDeletion(const std::vector<int>& ids)
{
    Base::PyGILStateLocker gil;
    try {
        Py::Module module(PyImport_ImportModule("freecad_plus.sketch_pattern_linked"), true);
        Py::List geometry;
        for (int id : ids) geometry.append(Py::Long(id));
        module.callMemberFunction("prepare_delete", Py::TupleN(Py::Object(getPyObject(), true), geometry));
    }
    catch (Py::Exception&) {
        Base::PyException error;
        throw Base::ValueError(error.what());
    }
}

int SketchObject::solveLinkedPatterns(bool updateGeometry, bool fromSolver)
{
    Base::StateLocker lock(managedoperation, true);
    Base::PyGILStateLocker gil;
    try {
        Py::Module module(PyImport_ImportModule("freecad_plus.sketch_pattern_linked"), true);
        Py::Object self(getPyObject(), true);
        Py::List phases(module.callMemberFunction("plan", Py::TupleN(self)));
        std::vector<std::unique_ptr<Part::Geometry>> working;
        if (fromSolver) {
            for (auto* geo : solvedSketch.extractGeometry()) working.emplace_back(geo);
        }
        else for (auto* geo : Geometry.getValues()) working.emplace_back(geo->clone());
        const auto external = getCompleteGeometry();
        auto complete = [&]() {
            std::vector<Part::Geometry*> result;
            for (auto& geo : working) result.push_back(geo.get());
            result.insert(result.end(), external.begin() + Geometry.getSize(), external.end());
            return result;
        };
        lastSolveTime = 0.;
        std::map<int, double> referenceValues;
        for (Py_ssize_t n = 0; n < phases.length(); ++n) {
            Py::Tuple phase(phases[n]);
            Py::List groups(phase[2]);
            if (groups.length()) {
                Py::List geometry;
                for (auto& geo : working) geometry.append(Py::Object(geo->getPyObject(), true));
                Py::List replacements(module.callMemberFunction("generate", Py::TupleN(self, geometry, groups)));
                for (Py_ssize_t i = 0; i < replacements.length(); ++i) {
                    Py::Tuple pair(replacements[i]);
                    const int index = int(Py::Long(pair[0]));
                    if (index < 0 || index >= int(working.size())
                        || !PyObject_TypeCheck(pair[1].ptr(), &Part::GeometryPy::Type))
                        throw Base::ValueError("Invalid linked pattern geometry replacement");
                    auto replacement = std::unique_ptr<Part::Geometry>(
                        static_cast<Part::GeometryPy*>(pair[1].ptr())->getGeometryPtr()->clone());
                    const bool construction = GeometryFacade::getFacade(replacement.get())->getConstruction();
                    for (const auto& extension : working[index]->getExtensions())
                        if (auto ext = extension.lock())
                            replacement->setExtension(ext->copy());
                    GeometryFacade::setConstruction(replacement.get(), construction);
                    working[index] = std::move(replacement);
                }
            }
            Py::List active(phase[0]), enabled(phase[1]);
            if (!active.length() && !enabled.length()) continue;
            std::set<int> fixed, enabledIds;
            for (int i = 0; i < int(working.size()); ++i) fixed.insert(i);
            for (Py_ssize_t i = 0; i < active.length(); ++i) fixed.erase(int(Py::Long(active[i])));
            for (Py_ssize_t i = 0; i < enabled.length(); ++i) enabledIds.insert(int(Py::Long(enabled[i])));
            std::vector<std::unique_ptr<Constraint>> copies;
            std::vector<Constraint*> constraints;
            int index = 0;
            for (const auto* c : Constraints.getValues()) {
                copies.emplace_back(c->clone());
                if (!enabledIds.contains(index++)) copies.back()->isActive = false;
                constraints.push_back(copies.back().get());
            }
            lastDoF = solvedSketch.setUpSketch(complete(), constraints, getExternalGeometryCount(), fixed);
            retrieveSolverDiagnostics();
            if (lastDoF < 0 || lastHasConflict || lastHasRedundancies || lastHasMalformedConstraints) {
                lastSolverStatus = GCS::Failed;
                signalSolverUpdate();
                return lastHasMalformedConstraints ? -5 : lastDoF < 0 ? -4 : lastHasConflict ? -3 : -2;
            }
            lastSolverStatus = solvedSketch.solve();
            lastSolveTime += solvedSketch.getSolveTime();
            if (lastSolverStatus) { signalSolverUpdate(); return -1; }
            for (int id : enabledIds)
                if (!copies[id]->isDriving) referenceValues[id] = copies[id]->getValue();
            auto output = solvedSketch.extractGeometry();
            working.clear();
            for (auto* geo : output) working.emplace_back(geo);
        }
        // Leave the normal native solver in sync for display, hit testing and drag.
        // Generated curves are fixed parameters, with no substitute constraints.
        lastDoF = solvedSketch.setUpSketch(complete(), Constraints.getValues(), getExternalGeometryCount());
        retrieveSolverDiagnostics();
        if (lastDoF < 0 || lastHasConflict || lastHasRedundancies || lastHasMalformedConstraints) {
            lastSolverStatus = GCS::Failed;
            signalSolverUpdate();
            return -1;
        }
        for (const auto& [id, value] : referenceValues) Constraints.getValues()[id]->setValue(value);
        solverNeedsUpdate = false;
        lastSolverStatus = GCS::Success;
        FullyConstrained.setValue(lastDoF == 0);
        if (updateGeometry) {
            Part::PropertyGeometryList tmp;
            std::vector<Part::Geometry*> output;
            for (auto& geo : working) output.push_back(geo.release());
            tmp.setValues(std::move(output));
            if (!Geometry.isSame(tmp)) Geometry.moveValues(std::move(tmp));
        }
        signalSolverUpdate();
        return 0;
    }
    catch (Py::Exception&) {
        Base::PyException error; error.reportException();
    }
    catch (const Base::Exception& error) { Base::Console().error("Linked pattern: %s\n", error.what()); }
    lastSolverStatus = GCS::Failed;
    signalSolverUpdate();
    return -1;
}

int SketchObject::moveLinkedPatternsTemporary(const std::vector<GeoElementId>& ids,
                                             const Base::Vector3d& point, bool relative)
{
    for (const auto& id : ids)
        if (id.GeoId >= 0 && id.GeoId < Geometry.getSize()
            && getGeometryFacade(id.GeoId)->testGeometryMode(GeometryMode::PatternGenerated))
            return -1;
    // Each UI motion supplies a displacement from the saved drag origin. Rebuild
    // from the unchanged document, not the previous frame's generated result.
    if (solveLinkedPatterns(false) != 0) return -1;
    const int status = solvedSketch.moveGeometries(ids, point, relative);
    return status ? status : solveLinkedPatterns(false, true);
}
