// SPDX-License-Identifier: LGPL-2.1-or-later
#ifndef SKETCHERGUI_DRAWSKETCHHANDLERPATTERN_H
#define SKETCHERGUI_DRAWSKETCHHANDLERPATTERN_H

#include <QApplication>
#include <QDynamicPropertyChangeEvent>
#include <QPointer>
#include <QTimer>
#include <functional>
#include <boost/signals2/connection.hpp>
#include <Base/Interpreter.h>
#include <Gui/BitmapFactory.h>
#include <Gui/Document.h>
#include <Gui/PythonWrapper.h>
#include <Mod/Part/App/GeometryPy.h>
#include "DrawSketchHandler.h"
#include "Utils.h"
#include "ViewProviderSketch.h"

namespace SketcherGui
{
// Native ownership and tool lifetime; the existing Plus Python UI services own
// the controls and pattern calculation. No global selection observer or timer.
class PatternHostWidget: public QWidget
{
public:
    std::function<void(const QString&)> action;
    bool event(QEvent* event) override
    {
        if (event->type() == QEvent::DynamicPropertyChange
            && static_cast<QDynamicPropertyChangeEvent*>(event)->propertyName() == "patternSerial") {
            const auto callback = action;
            if (callback) callback(property("patternAction").toString());
        }
        return QWidget::event(event);
    }
};

class DrawSketchHandlerPattern: public DrawSketchHandler
{
    Q_DECLARE_TR_FUNCTIONS(SketcherGui::DrawSketchHandlerPattern)
public:
    explicit DrawSketchHandlerPattern(std::vector<int> ids, std::string group = {})
        : initialIds(std::move(ids)), editGroup(std::move(group)) {}
    ~DrawSketchHandlerPattern() override
    {
        if (widget) widget->action = {};
        call("detach");
        if (sketchgui) sketchgui->setPatternPreviewHidden({}, {});
        Base::PyGILStateLocker lock;
        panel = Py::None();
    }

    void mouseMove(SnapManager::SnapHandle) override {}
    bool releaseButton(Base::Vector2d) override { return true; }
    bool pressButton(Base::Vector2d) override
    {
        if (!widget) return true;
        int geo = getPreselectCurve();
        if (geo < 0 && geo > Sketcher::GeoEnum::RefExt) geo = Sketcher::GeoEnum::GeoUndef;
        Sketcher::PointPos pos = Sketcher::PointPos::none;
        const bool geometryPicking = widget->property("patternGeometryPicking").toBool();
        if (!geometryPicking) {
            const auto& preselection = Gui::Selection().getPreselection();
            const std::string name = preselection.pSubName ? preselection.pSubName : "";
            if (preselection.Object.getObject() == sketchgui->getObject() && name.starts_with("Constraint")) {
                Base::PyGILStateLocker lock;
                Py::Tuple args(2); args[0] = Py::String(name); args[1] = Py::Boolean(removing());
                call("pick_constraint", args);
                return true;
            }
        }
        if ((!geometryPicking || geo == Sketcher::GeoEnum::GeoUndef) && getPreselectPoint() >= 0) {
            getSketchObject()->getGeoVertexIndex(getPreselectPoint(), geo, pos);
        }
        else if (!geometryPicking) {
            if (getPreselectCross() == 0) {
                geo = Sketcher::GeoEnum::RtPnt;
                pos = Sketcher::PointPos::start;
            }
            else if (getPreselectCross() == 1) geo = Sketcher::GeoEnum::HAxis;
            else if (getPreselectCross() == 2) geo = Sketcher::GeoEnum::VAxis;
        }
        pick(geo, static_cast<int>(pos));
        if (geometryPicking && geo >= 0 && geo < getSketchObject()->Geometry.getSize()) {
            const auto sub = std::string("Edge") + std::to_string(geo + 1);
            syncing = true;
            const auto* object = sketchgui->getObject();
            if (removing()) Gui::Selection().rmvSelection(object->getDocument()->getName(), object->getNameInDocument(), sub.c_str());
            else Gui::Selection().addSelection(object->getDocument()->getName(), object->getNameInDocument(), sub.c_str());
            syncing = false;
        }
        return true;
    }

    bool onSelectionChanged(const Gui::SelectionChanges& msg) override
    {
        if (syncing || msg.Type != Gui::SelectionChanges::AddSelection || !widget
            || msg.Object.getObject() != sketchgui->getObject()) return false;
        int geo = Sketcher::GeoEnum::GeoUndef;
        Sketcher::PointPos pos = Sketcher::PointPos::none;
        std::string name = msg.pSubName ? msg.pSubName : "";
        if (name.starts_with("Constraint")) {
            Base::PyGILStateLocker lock;
            Py::Tuple args(2); args[0] = Py::String(name); args[1] = Py::Boolean(removing());
            call("pick_constraint", args);
        }
        else {
            getIdsFromName(name.c_str(), getSketchObject(), geo, pos);
            pick(geo, static_cast<int>(pos));
        }
        return true;
    }

protected:
    std::string getToolName() const override { return "DSH_Pattern"; }
    QString getCrosshairCursorSVGName() const override { return QStringLiteral("Sketcher_Pointer_Create_Translate"); }
    std::unique_ptr<QWidget> createWidget() const override { return std::make_unique<PatternHostWidget>(); }
    bool isWidgetVisible() const override { return true; }
    QPixmap getToolIcon() const override { return Gui::BitmapFactory().pixmap("Sketcher_Translate"); }
    QString getToolWidgetText() const override { return tr("Sketch Pattern"); }
    void activated() override
    {
        setAxisPickStyle(true);
        setConstraintPickStyle(true);
        undoConnection = sketchgui->getDocument()->signalUndoDocument.connect([this](const Gui::Document&) { call("reset_inputs"); });
        redoConnection = sketchgui->getDocument()->signalRedoDocument.connect([this](const Gui::Document&) { call("reset_inputs"); });
    }
    void onWidgetChanged() override
    {
        widget = static_cast<PatternHostWidget*>(toolwidget);
        if (!widget) return;
        Base::PyGILStateLocker lock;
        try {
            Gui::PythonWrapper wrapper;
            wrapper.loadGuiModule();
            wrapper.loadWidgetsModule();
            Py::Module module(PyImport_ImportModule("freecad_plus.sketch_pattern_task"), true);
            Py::Tuple args(4);
            args[0] = wrapper.fromQWidget(widget);
            args[1] = Py::Object(getSketchObject()->getPyObject(), true);
            Py::List ids;
            for (int id : initialIds) ids.append(Py::Long(id));
            args[2] = ids;
            args[3] = Py::String(editGroup);
            panel = Py::Callable(module.getAttr("create")).apply(args);
            widget->action = [this](const QString& action) {
                if (action == QStringLiteral("finish")) {
                    QTimer::singleShot(0, widget, [host = widget] {
                        if (!host) return;
                        const auto action = host->action;
                        if (action) action(QStringLiteral("quit"));
                    });
                }
                else if (action == QStringLiteral("quit")) quit();
                else if (action == QStringLiteral("preview")) updatePreview();
            };
            updatePreview();
        }
        catch (Py::Exception&) { Base::PyException().reportException(); }
    }

private:
    static bool removing()
    {
        const auto intent = qApp->property("FreeCADPlusSelectionRemove");
        return intent.isValid() ? intent.toBool() : QApplication::keyboardModifiers().testFlag(Qt::ShiftModifier);
    }
    void call(const char* name)
    {
        Base::PyGILStateLocker lock;
        call(name, Py::Tuple());
    }
    void call(const char* name, const Py::Tuple& args)
    {
        Base::PyGILStateLocker lock;
        if (panel.isNone()) return;
        try { Py::Callable(panel.getAttr(name)).apply(args); }
        catch (Py::Exception&) { Base::PyException().reportException(); }
    }
    void pick(int geo, int pos)
    {
        Base::PyGILStateLocker lock;
        Py::Tuple args(3); args[0] = Py::Long(geo); args[1] = Py::Long(pos); args[2] = Py::Boolean(removing());
        call("pick", args);
    }
    void updatePreview()
    {
        clearEdit();
        Base::PyGILStateLocker lock;
        if (panel.isNone()) return;
        try {
            Py::List hidden(Py::Callable(panel.getAttr("get_hidden_geometry")).apply(Py::Tuple()));
            std::set<int> ids;
            for (const Py::Object& id : hidden) ids.insert(int(Py::Long(id)));
            Py::String group(Py::Callable(panel.getAttr("get_edit_group")).apply(Py::Tuple()));
            sketchgui->setPatternPreviewHidden(std::move(ids), group.as_std_string());
            Py::List geometries(Py::Callable(panel.getAttr("get_preview")).apply(Py::Tuple()));
            std::vector<Part::Geometry*> preview;
            for (Py::Object geometry : geometries) {
                if (PyObject_TypeCheck(geometry.ptr(), &Part::GeometryPy::Type)) {
                    preview.push_back(static_cast<Part::GeometryPy*>(geometry.ptr())->getGeometryPtr());
                }
            }
            if (!preview.empty()) drawEdit(preview);
        }
        catch (Py::Exception&) { Base::PyException().reportException(); }
    }
    std::vector<int> initialIds;
    std::string editGroup;
    QPointer<PatternHostWidget> widget;
    Py::Object panel;
    bool syncing = false;
    boost::signals2::scoped_connection undoConnection, redoConnection;
};
}
#endif
