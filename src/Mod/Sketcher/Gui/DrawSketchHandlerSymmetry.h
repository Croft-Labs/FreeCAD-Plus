/***************************************************************************
 *   Copyright (c) 2022 Boyer Pierre-Louis <pierrelouis.boyer@gmail.com>   *
 *                                                                         *
 *   This file is part of the FreeCAD CAx development system.              *
 *                                                                         *
 *   This library is free software; you can redistribute it and/or         *
 *   modify it under the terms of the GNU Library General Public           *
 *   License as published by the Free Software Foundation; either          *
 *   version 2 of the License, or (at your option) any later version.      *
 *                                                                         *
 *   This library  is distributed in the hope that it will be useful,      *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU Library General Public License for more details.                  *
 *                                                                         *
 *   You should have received a copy of the GNU Library General Public     *
 *   License along with this library; see the file COPYING.LIB. If not,    *
 *   write to the Free Software Foundation, Inc., 59 Temple Place,         *
 *   Suite 330, Boston, MA  02111-1307, USA                                *
 *                                                                         *
 ***************************************************************************/


#ifndef SKETCHERGUI_DrawSketchHandlerSymmetry_H
#define SKETCHERGUI_DrawSketchHandlerSymmetry_H

#include <QApplication>
#include <QCheckBox>
#include <QKeyEvent>
#include <QLabel>
#include <QLineEdit>
#include <QListWidget>
#include <QPointer>
#include <QPushButton>
#include <QScrollArea>
#include <QVBoxLayout>
#include <functional>
#include <algorithm>
#include <Inventor/events/SoKeyboardEvent.h>
#include <boost/signals2/connection.hpp>

#include <Gui/BitmapFactory.h>
#include <Gui/Command.h>
#include <Gui/Document.h>
#include <Mod/Sketcher/App/SketchObject.h>
#include "DrawSketchHandler.h"
#include "Utils.h"
#include "ViewProviderSketch.h"

namespace SketcherGui
{

// Owned by TaskSketcherTool. Callbacks are detached when the drawing handler ends.
class SymmetryTaskWidget: public QWidget
{
public:
    explicit SymmetryTaskWidget()
    {
        setObjectName(QStringLiteral("SketchSymmetryTask"));
        auto* layout = new QVBoxLayout(this);
        layout->setContentsMargins(0, 0, 0, 0);
        layout->addWidget(new QLabel(tr("Geometry"), this));
        geometry = new QListWidget(this);
        geometry->setObjectName(QStringLiteral("SymmetryGeometry"));
        geometry->setSelectionMode(QAbstractItemView::ExtendedSelection);
        geometry->setMinimumHeight(360);
        geometry->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
        geometry->installEventFilter(this);
        geometry->viewport()->installEventFilter(this);
        layout->addWidget(geometry, 1);
        auto* row = new QHBoxLayout;
        auto* remove = new QPushButton(tr("Remove"), this);
        remove->setObjectName(QStringLiteral("SymmetryRemove"));
        auto* clear = new QPushButton(tr("Clear"), this);
        clear->setObjectName(QStringLiteral("SymmetryClear"));
        row->addWidget(remove);
        row->addWidget(clear);
        layout->addLayout(row);
        layout->addWidget(new QLabel(tr("Axis of symmetry"), this));
        axis = new QLineEdit(this);
        axis->setObjectName(QStringLiteral("SymmetryAxis"));
        axis->setReadOnly(true);
        axis->setPlaceholderText(tr("Select an axis or straight line"));
        axis->installEventFilter(this);
        layout->addWidget(axis);
        auto* hint = new QLabel(tr("Select a sketch axis or straight line. A point can be used as a symmetry center."), this);
        hint->setWordWrap(true);
        layout->addWidget(hint);
        deleteOriginal = new QCheckBox(tr("Delete original geometries (U)"), this);
        symmetryConstraints = new QCheckBox(tr("Create symmetry constraints (J)"), this);
        deleteOriginal->setObjectName(QStringLiteral("SymmetryDeleteOriginal"));
        symmetryConstraints->setObjectName(QStringLiteral("SymmetryConstraints"));
        symmetryConstraints->setChecked(true);
        layout->addWidget(deleteOriginal);
        layout->addWidget(symmetryConstraints);
        connect(deleteOriginal, &QCheckBox::toggled, this, [this](bool checked) {
            if (checked) symmetryConstraints->setChecked(false);
        });
        connect(symmetryConstraints, &QCheckBox::toggled, this, [this](bool checked) {
            if (checked) deleteOriginal->setChecked(false);
        });
        status = new QLabel(this);
        status->setObjectName(QStringLiteral("SymmetryStatus"));
        status->setTextFormat(Qt::PlainText);
        status->setWordWrap(true);
        layout->addWidget(status);
        row = new QHBoxLayout;
        apply = new QPushButton(tr("Apply"), this);
        apply->setObjectName(QStringLiteral("SymmetryApply"));
        auto* done = new QPushButton(tr("Done"), this);
        done->setObjectName(QStringLiteral("SymmetryDone"));
        auto* cancel = new QPushButton(tr("Cancel"), this);
        cancel->setObjectName(QStringLiteral("SymmetryCancel"));
        row->addWidget(done);
        row->addWidget(apply);
        row->addWidget(cancel);
        layout->addLayout(row);
        connect(remove, &QPushButton::clicked, this, [this] { invoke(removeSelection); });
        connect(clear, &QPushButton::clicked, this, [this] { invoke(clearSelection); });
        connect(apply, &QPushButton::clicked, this, [this] { invoke(applySelection); });
        connect(done, &QPushButton::clicked, this, [this] { invoke(acceptSelection); });
        connect(cancel, &QPushButton::clicked, this, [this] { invoke(finish); });
        setAxisPicking(false);
    }

    void setAxisPicking(bool enabled)
    {
        axisPicking = enabled;
        geometry->setStyleSheet(enabled ? QString() : QStringLiteral("QListWidget {border:2px solid #347bb7;}"));
        axis->setStyleSheet(enabled ? QStringLiteral("QLineEdit {border:2px solid #347bb7;}") : QString());
    }

    void message(const QString& text, bool error = false)
    {
        // Same native presentation as freecad_plus.task_status.TaskStatus.
        status->setStyleSheet(error ? QStringLiteral(
            "QLabel {border:2px solid #bd780b;border-radius:3px;background:#fff3d6;"
            "color:#875300;padding:8px;font-weight:600;}") : QString());
        status->setText(text);
        if (error) {
            apply->setEnabled(false);
            for (QWidget* p = parentWidget(); p; p = p->parentWidget()) {
                if (auto* scroll = qobject_cast<QScrollArea*>(p)) {
                    scroll->ensureWidgetVisible(status);
                    break;
                }
            }
        }
    }

    bool eventFilter(QObject* object, QEvent* event) override
    {
        if (event->type() == QEvent::FocusIn || event->type() == QEvent::MouseButtonPress) {
            setAxisPicking(object == axis);
        }
        if (event->type() == QEvent::KeyPress) {
            auto* key = static_cast<QKeyEvent*>(event);
            if (key->key() == Qt::Key_Delete) {
                invoke(object == axis ? clearAxis : removeSelection);
                return true;
            }
            if (key->key() == Qt::Key_Escape) {
                invoke(finish);
                return true;
            }
        }
        return QWidget::eventFilter(object, event);
    }

    void detach()
    {
        removeSelection = clearSelection = clearAxis = applySelection = acceptSelection = finish = {};
    }

    QListWidget* geometry;
    QLineEdit* axis;
    QCheckBox* deleteOriginal;
    QCheckBox* symmetryConstraints;
    QLabel* status;
    QPushButton* apply;
    bool axisPicking = false;
    std::function<void()> removeSelection, clearSelection, clearAxis, applySelection, acceptSelection, finish;

private:
    static void invoke(std::function<void()> fn)
    {
        if (fn) fn(); // Copy permits the callback to destroy its handler.
    }
};

class DrawSketchHandlerSymmetry: public DrawSketchHandler
{
    Q_DECLARE_TR_FUNCTIONS(SketcherGui::DrawSketchHandlerSymmetry)
public:
    explicit DrawSketchHandlerSymmetry(std::vector<int> geometryIds)
        : geometryIds(std::move(geometryIds))
    {}

    ~DrawSketchHandlerSymmetry() override
    {
        if (widget) widget->detach();
    }

    void mouseMove(SnapManager::SnapHandle) override
    {} // Committed picks, rather than hover, define the preview.

    bool pressButton(Base::Vector2d) override
    {
        if (!widget) return true;
        int geo = getPreselectCurve();
        if (geo < 0 && geo > Sketcher::GeoEnum::RefExt) geo = Sketcher::GeoEnum::GeoUndef;
        Sketcher::PointPos pos = Sketcher::PointPos::none;
        if (!widget->axisPicking && getPreselectPoint() >= 0 && !eligibleGeometry(geo)) {
            getSketchObject()->getGeoVertexIndex(getPreselectPoint(), geo, pos);
        }
        if (widget->axisPicking) {
            const int vertex = getPreselectPoint();
            const int cross = getPreselectCross();
            if (vertex >= 0) {
                getSketchObject()->getGeoVertexIndex(vertex, geo, pos);
            }
            else if (cross == 0) {
                geo = Sketcher::GeoEnum::RtPnt;
                pos = Sketcher::PointPos::start;
            }
            else if (cross == 1) geo = Sketcher::GeoEnum::HAxis;
            else if (cross == 2) geo = Sketcher::GeoEnum::VAxis;
        }
        const bool remove = removing();
        pick(geo, pos, remove);
        if (!widget->axisPicking && eligibleGeometry(geo)) {
            const auto sub = std::string("Edge") + std::to_string(geo + 1);
            syncing = true;
            const auto* object = sketchgui->getObject();
            if (remove) Gui::Selection().rmvSelection(object->getDocument()->getName(), object->getNameInDocument(), sub.c_str());
            else Gui::Selection().addSelection(object->getDocument()->getName(), object->getNameInDocument(), sub.c_str());
            syncing = false;
        }
        return true;
    }

    bool releaseButton(Base::Vector2d) override { return true; }

    bool onSelectionChanged(const Gui::SelectionChanges& msg) override
    {
        if (syncing || msg.Type != Gui::SelectionChanges::AddSelection || !widget) return false;
        if (msg.Object.getObject() != sketchgui->getObject()) return false;
        int geo = Sketcher::GeoEnum::GeoUndef;
        Sketcher::PointPos pos = Sketcher::PointPos::none;
        getIdsFromName(msg.pSubName ? msg.pSubName : "", getSketchObject(), geo, pos);
        pick(geo, pos, removing());
        return true;
    }

    void registerPressedKey(bool pressed, int key) override
    {
        if (!pressed && widget && key == SoKeyboardEvent::U) {
            widget->deleteOriginal->toggle();
        }
        else if (!pressed && widget && key == SoKeyboardEvent::J) {
            widget->symmetryConstraints->toggle();
        }
        else DrawSketchHandler::registerPressedKey(pressed, key);
    }

protected:
    std::string getToolName() const override { return "DSH_Symmetry"; }
    QString getCrosshairCursorSVGName() const override { return QStringLiteral("Sketcher_Pointer_Create_Symmetry"); }
    std::unique_ptr<QWidget> createWidget() const override { return std::make_unique<SymmetryTaskWidget>(); }
    bool isWidgetVisible() const override { return true; }
    QPixmap getToolIcon() const override { return Gui::BitmapFactory().pixmap("Sketcher_Symmetry"); }
    QString getToolWidgetText() const override { return tr("Symmetry Parameters"); }

    void activated() override
    {
        undoConnection = sketchgui->getDocument()->signalUndoDocument.connect([this](const Gui::Document&) { resetInputs(); });
        redoConnection = sketchgui->getDocument()->signalRedoDocument.connect([this](const Gui::Document&) { resetInputs(); });
        setAxisPickStyle(true);
    }

    void onWidgetChanged() override
    {
        widget = static_cast<SymmetryTaskWidget*>(toolwidget);
        if (!widget) return;
        widget->removeSelection = [this] {
            for (auto* item : widget->geometry->selectedItems()) {
                std::erase(geometryIds, item->data(Qt::UserRole).toInt());
            }
            refresh();
        };
        widget->clearSelection = [this] { geometryIds.clear(); refresh(); };
        widget->clearAxis = [this] { refGeoId = Sketcher::GeoEnum::GeoUndef; refresh(); };
        widget->applySelection = [this] { apply(); };
        widget->acceptSelection = [this] {
            if (geometryIds.empty()) { quit(); return; }
            if (!widget->apply->isEnabled()) {
                widget->message(tr("Complete the mirror inputs before choosing Done, or Cancel to discard them."), true);
                return;
            }
            if (apply()) quit();
        };
        widget->finish = [this] { quit(); };
        refresh();
    }

private:
    static bool removing()
    {
        const auto intent = qApp->property("FreeCADPlusSelectionRemove");
        return intent.isValid() ? intent.toBool()
                               : QApplication::keyboardModifiers().testFlag(Qt::ShiftModifier);
    }

    bool eligibleGeometry(int id) const
    {
        return id >= 0 && id < static_cast<int>(sketchgui->getSketchObject()->Geometry.getSize());
    }

    QString referenceName() const
    {
        if (refGeoId == Sketcher::GeoEnum::GeoUndef) return {};
        if (refGeoId == Sketcher::GeoEnum::RtPnt && refPosId != Sketcher::PointPos::none) return tr("Sketch origin");
        if (refGeoId == Sketcher::GeoEnum::HAxis) return tr("Horizontal sketch axis");
        if (refGeoId == Sketcher::GeoEnum::VAxis) return tr("Vertical sketch axis");
        QString name = refGeoId >= 0 ? tr("Edge%1").arg(refGeoId + 1)
                                    : tr("ExternalEdge%1").arg(-refGeoId - 2);
        if (refPosId != Sketcher::PointPos::none) name += tr(" — point %1").arg(static_cast<int>(refPosId));
        return name;
    }

    void pick(int geo, Sketcher::PointPos pos, bool remove)
    {
        if (widget->axisPicking) {
            if (remove) {
                if (geo == refGeoId && pos == refPosId) refGeoId = Sketcher::GeoEnum::GeoUndef;
            }
            else {
                const auto* geometry = geo == Sketcher::GeoEnum::GeoUndef ? nullptr : getSketchObject()->getGeometry(geo);
                if (!geometry || (pos == Sketcher::PointPos::none && !isLineSegment(*geometry))) {
                    widget->message(tr("Select a straight line, sketch axis, or point for the symmetry reference."), true);
                    return;
                }
                refGeoId = geo;
                refPosId = pos;
            }
        }
        else {
            if (eligibleGeometry(geo) && isPoint(*getSketchObject()->getGeometry(geo))) {
                pos = Sketcher::PointPos::none;
            }
            if (!eligibleGeometry(geo) || pos != Sketcher::PointPos::none) {
                if (!remove) widget->message(tr("Select geometry belonging to this sketch."), true);
                return;
            }
            if (remove) std::erase(geometryIds, geo);
            else if (std::ranges::find(geometryIds, geo) == geometryIds.end()) geometryIds.push_back(geo);
        }
        refresh();
    }

    void resetInputs()
    {
        geometryIds.clear();
        refGeoId = Sketcher::GeoEnum::GeoUndef;
        refresh();
    }

    std::vector<int> operationGeometry() const
    {
        auto ids = geometryIds;
        // Match native Mirror's inclusion of the defining geometry of conics and splines.
        for (const auto* constraint : sketchgui->getSketchObject()->Constraints.getValues()) {
            if (constraint->Type == Sketcher::InternalAlignment
                && std::ranges::find(geometryIds, constraint->Second) != geometryIds.end()
                && std::ranges::find(ids, constraint->First) == ids.end()
                && eligibleGeometry(constraint->First)) {
                ids.push_back(constraint->First);
            }
        }
        return ids;
    }

    void refresh()
    {
        if (!widget) return;
        std::erase_if(geometryIds, [this](int id) { return !eligibleGeometry(id); });
        widget->geometry->clear();
        for (int id : geometryIds) {
            auto* item = new QListWidgetItem(tr("Edge%1").arg(id + 1), widget->geometry);
            item->setData(Qt::UserRole, id);
        }
        widget->axis->setText(referenceName());
        widget->apply->setEnabled(false);
        clearEdit();
        widget->message(tr("Select geometry, then choose the axis."));
        if (geometryIds.empty() || refGeoId == Sketcher::GeoEnum::GeoUndef) return;
        try {
            std::map<int, int> geoMap;
            std::map<int, bool> reversed;
            auto preview = getSketchObject()->getSymmetric(operationGeometry(), geoMap, reversed, refGeoId, refPosId);
            // Own native preview allocations even when tessellation throws.
            std::vector<std::unique_ptr<Part::Geometry>> owned;
            for (auto* geometry : preview) owned.emplace_back(geometry);
            if (preview.empty()) {
                widget->message(tr("The selected geometry cannot be mirrored. Select its defining geometry."), true);
                return;
            }
            drawEdit(preview);
            widget->apply->setEnabled(true);
            widget->message(tr("Ready to create mirrored geometry."));
        }
        catch (const Base::Exception& e) {
            widget->message(QString::fromUtf8(e.what()), true);
        }
    }

    bool apply()
    {
        if (!widget || !widget->apply->isEnabled()) return false;
        auto* sketch = getSketchObject();
        const auto ids = operationGeometry();
        const int previousReference = refGeoId;
        try {
            Gui::Command::openCommand(QT_TRANSLATE_NOOP("Command", "Symmetry geometries"));
            sketch->addSymmetric(ids, refGeoId, refPosId,
                                !widget->deleteOriginal->isChecked() && widget->symmetryConstraints->isChecked());
            if (widget->deleteOriginal->isChecked()) {
                if (sketch->delGeometriesExclusiveList(ids) != 0) {
                    throw Base::RuntimeError("Could not delete the original geometry");
                }
                if (refGeoId >= 0) {
                    if (std::ranges::find(ids, refGeoId) != ids.end()) {
                        refGeoId = Sketcher::GeoEnum::GeoUndef;
                    }
                    else {
                        refGeoId -= static_cast<int>(std::ranges::count_if(
                            ids, [this](int id) { return id < refGeoId; }));
                    }
                }
            }
            tryAutoRecomputeIfNotSolve(sketch);
            Gui::Command::commitCommand();
            widget->deleteOriginal->setChecked(false);
            widget->symmetryConstraints->setChecked(true);
            geometryIds.clear();
            refGeoId = Sketcher::GeoEnum::GeoUndef;
            refPosId = Sketcher::PointPos::none;
            widget->setAxisPicking(false);
            syncing = true;
            Gui::Selection().clearSelection();
            syncing = false;
            refresh();
            widget->message(tr("Mirrored geometry created. Select geometry for another set."));
            return true;
        }
        catch (const Base::Exception& e) {
            Gui::Command::abortCommand();
            refGeoId = previousReference;
            refresh();
            widget->message(tr("Could not create mirrored geometry: %1").arg(QString::fromUtf8(e.what())), true);
            return false;
        }
    }

    std::vector<int> geometryIds;
    int refGeoId = Sketcher::GeoEnum::GeoUndef;
    Sketcher::PointPos refPosId = Sketcher::PointPos::none;
    QPointer<SymmetryTaskWidget> widget;
    bool syncing = false;
    boost::signals2::scoped_connection undoConnection, redoConnection;
};

} // namespace SketcherGui
#endif
