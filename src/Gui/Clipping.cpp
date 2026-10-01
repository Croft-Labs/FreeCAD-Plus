/***************************************************************************
 *   Copyright (c) 2013 Werner Mayer <wmayer[at]users.sourceforge.net>     *
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

#include <array>
#include <cmath>
#include <limits>
#include <functional>

#include <Inventor/actions/SoGetBoundingBoxAction.h>
#include <Inventor/nodes/SoClipPlane.h>
#include <Inventor/nodes/SoGroup.h>
#include <Inventor/sensors/SoTimerSensor.h>
#include <QDockWidget>
#include <QPointer>
#include <QFileDialog>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QSaveFile>
#include <QSignalBlocker>
#include <QScrollArea>

#include <App/Application.h>

#include "Clipping.h"
#include "ui_Clipping.h"
#include "DockWindowManager.h"
#include "View3DInventor.h"
#include "View3DInventorViewer.h"

using namespace Gui::Dialog;

class Clipping::Private
{
public:
    Ui_Clipping ui;
    QPointer<Gui::View3DInventor> view;
    SoGroup* node;
    SoClipPlane* clipX;
    SoClipPlane* clipY;
    SoClipPlane* clipZ;
    SoClipPlane* clipView;
    bool flipX {false};
    bool flipY {false};
    bool flipZ {false};
    SoTimerSensor* sensor;
    App::Document* shownOn {nullptr};
    QDockWidget* dockWidget {nullptr};
    fastsignals::scoped_connection activeDocConnection;

    Private()
    {
        clipX = new SoClipPlane();
        clipX->on.setValue(false);
        clipX->plane.setValue(SbPlane(SbVec3f(1, 0, 0), 0));
        clipX->ref();

        clipY = new SoClipPlane();
        clipY->on.setValue(false);
        clipY->plane.setValue(SbPlane(SbVec3f(0, 1, 0), 0));
        clipY->ref();

        clipZ = new SoClipPlane();
        clipZ->on.setValue(false);
        clipZ->plane.setValue(SbPlane(SbVec3f(0, 0, 1), 0));
        clipZ->ref();

        clipView = new SoClipPlane();
        clipView->on.setValue(false);
        clipView->plane.setValue(SbPlane(SbVec3f(0, 0, 1), 0));
        clipView->ref();

        node = nullptr;
        sensor = new SoTimerSensor(moveCallback, this);
    }
    ~Private()
    {
        clipX->unref();
        clipY->unref();
        clipZ->unref();
        clipView->unref();
        delete sensor;
    }
    void showDirection(const SbVec3f& direction)
    {
        const QSignalBlocker x(ui.dirX), y(ui.dirY), z(ui.dirZ);
        ui.dirX->setValue(direction[0]);
        ui.dirY->setValue(direction[1]);
        ui.dirZ->setValue(direction[2]);
    }
    static void moveCallback(void* data, SoSensor* sensor)
    {
        Q_UNUSED(sensor);
        auto self = static_cast<Private*>(data);
        if (self->view) {
            Gui::View3DInventorViewer* view = self->view->getViewer();
            SoClipPlane* clip = self->clipView;
            SbPlane pln = clip->plane.getValue();
            clip->plane.setValue(SbPlane(view->getViewDirection(), pln.getDistanceFromOrigin()));
            self->showDirection(view->getViewDirection());
        }
    }
};

/* TRANSLATOR Gui::Dialog::Clipping */

Clipping::Clipping(Gui::View3DInventor* view, App::Document* showOn, QWidget* parent)
    : QDialog(parent)
    , d(new Private)
{
    // create widgets
    d->ui.setupUi(this);
    setupConnections();

    constexpr int max = std::numeric_limits<int>::max();
    d->ui.clipView->setRange(-max, max);
    d->ui.clipView->setSingleStep(0.1f);
    d->ui.clipX->setRange(-max, max);
    d->ui.clipX->setSingleStep(0.1f);
    d->ui.clipY->setRange(-max, max);
    d->ui.clipY->setSingleStep(0.1f);
    d->ui.clipZ->setRange(-max, max);
    d->ui.clipZ->setSingleStep(0.1f);

    d->ui.dirX->setRange(-max, max);
    d->ui.dirX->setSingleStep(0.1f);
    d->ui.dirY->setRange(-max, max);
    d->ui.dirY->setSingleStep(0.1f);
    d->ui.dirZ->setRange(-max, max);
    d->ui.dirZ->setSingleStep(0.1f);
    for (auto* offset : {d->ui.clipX, d->ui.clipY, d->ui.clipZ, d->ui.clipView}) {
        offset->setSuffix(tr(" mm"));
        offset->setToolTip(tr("Signed world-coordinate offset in millimetres. Flip changes the retained side."));
    }
    for (auto* direction : {d->ui.dirX, d->ui.dirY, d->ui.dirZ}) {
        direction->setDecimals(6);
        direction->setMinimumHeight(direction->sizeHint().height());
    }
    d->ui.dirZ->setValue(1.0f);
    d->shownOn = showOn;

    d->view = view;
    View3DInventorViewer* viewer = view->getViewer();
    d->node = static_cast<SoGroup*>(viewer->getSceneGraph());
    d->node->ref();
    int index = -1;
    if (auto editingRoot = viewer->getEditingRoot()) {
        index = d->node->findChild(editingRoot);
    }
    d->node->insertChild(d->clipX, index + 1);
    d->node->insertChild(d->clipY, index + 1);
    d->node->insertChild(d->clipZ, index + 1);
    d->node->insertChild(d->clipView, index + 1);

    SoGetBoundingBoxAction action(viewer->getSoRenderManager()->getViewportRegion());
    action.apply(viewer->getSceneGraph());
    SbBox3f box = action.getBoundingBox();

    if (!box.isEmpty()) {
        SbVec3f cnt = box.getCenter();
        d->ui.clipView->setValue(cnt[2]);
        d->ui.clipX->setValue(cnt[0]);
        d->ui.clipY->setValue(cnt[1]);
        d->ui.clipZ->setValue(cnt[2]);

        int minDecimals = 2;
        float lenx, leny, lenz;
        box.getSize(lenx, leny, lenz);
        int steps = 100;
        float minlen = std::min<float>(lenx, std::min<float>(leny, lenz));

        // determine the single step values
        {
            minlen = minlen / steps;
            int dim = static_cast<int>(log10(std::max(minlen, 1e-6f)));
            double singleStep = pow(10.0, dim);
            d->ui.clipView->setSingleStep(singleStep);
            minDecimals = std::max(minDecimals, -dim);
        }
        {
            lenx = lenx / steps;
            int dim = static_cast<int>(log10(std::max(lenx, 1e-6f)));
            double singleStep = pow(10.0, dim);
            d->ui.clipX->setSingleStep(singleStep);
        }
        {
            leny = leny / steps;
            int dim = static_cast<int>(log10(std::max(leny, 1e-6f)));
            double singleStep = pow(10.0, dim);
            d->ui.clipY->setSingleStep(singleStep);
        }
        {
            lenz = lenz / steps;
            int dim = static_cast<int>(log10(std::max(lenz, 1e-6f)));
            double singleStep = pow(10.0, dim);
            d->ui.clipZ->setSingleStep(singleStep);
        }

        // set decimals
        d->ui.clipView->setDecimals(minDecimals);
        d->ui.clipX->setDecimals(minDecimals);
        d->ui.clipY->setDecimals(minDecimals);
        d->ui.clipZ->setDecimals(minDecimals);
    }
}

Clipping* Clipping::makeDockWidget(Gui::View3DInventor* view, App::Document* showOn)
{
    // embed this dialog into a QDockWidget
    auto clipping = new Clipping(view, showOn);
    // Keep numeric controls reachable when the dock is shorter than its content.
    clipping->layout()->setSizeConstraint(QLayout::SetMinimumSize);
    auto scroll = new QScrollArea();
    scroll->setWindowTitle(clipping->windowTitle());
    scroll->setWidgetResizable(true);
    scroll->setWidget(clipping);
    Gui::DockWindowManager* pDockMgr = Gui::DockWindowManager::instance();
    QDockWidget* dw = pDockMgr->addDockWindow("Clipping", scroll, Qt::LeftDockWidgetArea);
    dw->setFeatures(QDockWidget::DockWidgetMovable | QDockWidget::DockWidgetFloatable);
    dw->show();
    clipping->d->dockWidget = dw;

    return clipping;
}

/** Destroys the object and frees any allocated resources */
Clipping::~Clipping()
{
    d->activeDocConnection.disconnect();
    d->node->removeChild(d->clipX);
    d->node->removeChild(d->clipY);
    d->node->removeChild(d->clipZ);
    d->node->removeChild(d->clipView);
    d->node->unref();
    delete d;
}

void Clipping::setupConnections()
{
    // clang-format off
    d->activeDocConnection = App::GetApplication().signalActiveDocument.connect(
            std::bind(&Clipping::onActiveDocument, this, std::placeholders::_1));
    connect(d->ui.groupBoxX, &QGroupBox::toggled,
            this, &Clipping::onGroupBoxXToggled);
    connect(d->ui.groupBoxY, &QGroupBox::toggled,
            this, &Clipping::onGroupBoxYToggled);
    connect(d->ui.groupBoxZ, &QGroupBox::toggled,
            this, &Clipping::onGroupBoxZToggled);
    connect(d->ui.clipX, qOverload<double>(&QDoubleSpinBox::valueChanged),
            this, &Clipping::onClipXValueChanged);
    connect(d->ui.clipY, qOverload<double>(&QDoubleSpinBox::valueChanged),
            this, &Clipping::onClipYValueChanged);
    connect(d->ui.clipZ, qOverload<double>(&QDoubleSpinBox::valueChanged),
            this, &Clipping::onClipZValueChanged);
    connect(d->ui.flipClipX, &QPushButton::clicked,
            this, &Clipping::onFlipClipXClicked);
    connect(d->ui.flipClipY, &QPushButton::clicked,
            this, &Clipping::onFlipClipYClicked);
    connect(d->ui.flipClipZ, &QPushButton::clicked,
            this, &Clipping::onFlipClipZClicked);
    connect(d->ui.groupBoxView, &QGroupBox::toggled,
            this, &Clipping::onGroupBoxViewToggled);
    connect(d->ui.clipView, qOverload<double>(&QDoubleSpinBox::valueChanged),
            this, &Clipping::onClipViewValueChanged);
    connect(d->ui.fromView, &QPushButton::clicked,
            this, &Clipping::onFromViewClicked);
    connect(d->ui.adjustViewdirection, &QCheckBox::toggled,
            this, &Clipping::onAdjustViewdirectionToggled);
    connect(d->ui.dirX, qOverload<double>(&QDoubleSpinBox::valueChanged),
            this, &Clipping::onDirXValueChanged);
    connect(d->ui.dirY, qOverload<double>(&QDoubleSpinBox::valueChanged),
            this, &Clipping::onDirYValueChanged);
    connect(d->ui.dirZ, qOverload<double>(&QDoubleSpinBox::valueChanged),
            this, &Clipping::onDirZValueChanged);
    // clang-format on
    connect(d->ui.saveSection, &QPushButton::clicked, this, [this] {
        const QString path = QFileDialog::getSaveFileName(
            this, tr("Save section planes"), QString(), tr("Section planes (*.fcsection)"));
        if (!path.isEmpty()) {
            saveSection(path);
        }
    });
    connect(d->ui.loadSection, &QPushButton::clicked, this, [this] {
        const QString path = QFileDialog::getOpenFileName(
            this, tr("Load section planes"), QString(), tr("Section planes (*.fcsection)"));
        if (!path.isEmpty()) {
            loadSection(path);
        }
    });
}

void Clipping::reject()
{
    QDialog::reject();
    auto dw = d->dockWidget;
    if (dw) {
        dw->deleteLater();
    }
}
void Clipping::onActiveDocument(const App::Document& doc)
{
    if (!d || !d->dockWidget) {
        return;
    }
    if (&doc == d->shownOn) {
        d->dockWidget->show();
    }
    else {
        d->dockWidget->hide();
    }
}
void Clipping::onGroupBoxXToggled(bool on)
{
    if (on) {
        d->ui.groupBoxView->setChecked(false);
    }

    d->clipX->on.setValue(on);
}

void Clipping::onGroupBoxYToggled(bool on)
{
    if (on) {
        d->ui.groupBoxView->setChecked(false);
    }

    d->clipY->on.setValue(on);
}

void Clipping::onGroupBoxZToggled(bool on)
{
    if (on) {
        d->ui.groupBoxView->setChecked(false);
    }

    d->clipZ->on.setValue(on);
}

void Clipping::onClipXValueChanged(double val)
{
    SbPlane pln = d->clipX->plane.getValue();
    d->clipX->plane.setValue(SbPlane(pln.getNormal(), d->flipX ? -val : val));
}

void Clipping::onClipYValueChanged(double val)
{
    SbPlane pln = d->clipY->plane.getValue();
    d->clipY->plane.setValue(SbPlane(pln.getNormal(), d->flipY ? -val : val));
}

void Clipping::onClipZValueChanged(double val)
{
    SbPlane pln = d->clipZ->plane.getValue();
    d->clipZ->plane.setValue(SbPlane(pln.getNormal(), d->flipZ ? -val : val));
}

void Clipping::onFlipClipXClicked()
{
    d->flipX = !d->flipX;
    SbPlane pln = d->clipX->plane.getValue();
    d->clipX->plane.setValue(SbPlane(-pln.getNormal(), -pln.getDistanceFromOrigin()));
}

void Clipping::onFlipClipYClicked()
{
    d->flipY = !d->flipY;
    SbPlane pln = d->clipY->plane.getValue();
    d->clipY->plane.setValue(SbPlane(-pln.getNormal(), -pln.getDistanceFromOrigin()));
}

void Clipping::onFlipClipZClicked()
{
    d->flipZ = !d->flipZ;
    SbPlane pln = d->clipZ->plane.getValue();
    d->clipZ->plane.setValue(SbPlane(-pln.getNormal(), -pln.getDistanceFromOrigin()));
}

void Clipping::onGroupBoxViewToggled(bool on)
{
    if (on) {
        d->ui.groupBoxX->setChecked(false);
        d->ui.groupBoxY->setChecked(false);
        d->ui.groupBoxZ->setChecked(false);
    }

    d->clipView->on.setValue(on);
    if (on) {
        onDirXValueChanged(0);
    }
}

void Clipping::onClipViewValueChanged(double val)
{
    SbPlane pln = d->clipView->plane.getValue();
    d->clipView->plane.setValue(SbPlane(pln.getNormal(), val));
}

void Clipping::onFromViewClicked()
{
    if (d->view) {
        Gui::View3DInventorViewer* view = d->view->getViewer();
        SbVec3f dir = view->getViewDirection();
        SbPlane pln = d->clipView->plane.getValue();
        d->clipView->plane.setValue(SbPlane(dir, pln.getDistanceFromOrigin()));
        d->showDirection(dir);
        d->clipView->on.setValue(d->ui.groupBoxView->isChecked());
        d->ui.sectionStatus->clear();
    }
}

void Clipping::onAdjustViewdirectionToggled(bool on)
{
    d->ui.dirX->setDisabled(on);
    d->ui.dirY->setDisabled(on);
    d->ui.dirZ->setDisabled(on);
    d->ui.fromView->setDisabled(on);

    if (on) {
        onFromViewClicked();
        d->sensor->schedule();
    }
    else {
        d->sensor->unschedule();
    }
}

void Clipping::onDirXValueChanged(double)
{
    SbVec3f normal(d->ui.dirX->value(), d->ui.dirY->value(), d->ui.dirZ->value());
    if (normal.normalize() == 0.0f) {
        d->clipView->on.setValue(false);
        d->ui.sectionStatus->setText(tr("Direction cannot be zero. Custom clipping is paused until corrected."));
        return;
    }
    d->ui.sectionStatus->clear();
    const auto plane = d->clipView->plane.getValue();
    d->clipView->plane.setValue(SbPlane(normal, plane.getDistanceFromOrigin()));
    d->clipView->on.setValue(d->ui.groupBoxView->isChecked());
}

void Clipping::onDirYValueChanged(double value)
{
    onDirXValueChanged(value);
}

void Clipping::onDirZValueChanged(double value)
{
    onDirXValueChanged(value);
}

bool Clipping::saveSection(const QString& path)
{
    if (d->ui.groupBoxView->isChecked() && !d->clipView->on.getValue()) {
        d->ui.sectionStatus->setText(tr("Correct the custom direction before saving."));
        return false;
    }
    // Capture the actual displayed normals, including a camera-following plane.
    QJsonArray planes;
    for (auto* clip : {d->clipX, d->clipY, d->clipZ, d->clipView}) {
        const auto plane = clip->plane.getValue();
        const auto normal = plane.getNormal();
        planes.append(QJsonObject {
            {QStringLiteral("enabled"), bool(clip->on.getValue())},
            {QStringLiteral("normal"), QJsonArray {normal[0], normal[1], normal[2]}},
            {QStringLiteral("offsetMm"), plane.getDistanceFromOrigin()}
        });
    }
    const QJsonDocument json(QJsonObject {
        {QStringLiteral("format"), QStringLiteral("FreeCADPlus.SectionPlanes")},
        {QStringLiteral("version"), 1},
        {QStringLiteral("frame"), QStringLiteral("world")},
        {QStringLiteral("planes"), planes}
    });
    QSaveFile file(path);
    const auto bytes = json.toJson();
    if (!file.open(QIODevice::WriteOnly) || file.write(bytes) != bytes.size() || !file.commit()) {
        d->ui.sectionStatus->setText(tr("Could not save section planes. Check the destination."));
        return false;
    }
    d->ui.sectionStatus->setText(tr("Section planes saved. Camera-following direction was captured as a fixed plane."));
    return true;
}

bool Clipping::loadSection(const QString& path)
{
    auto invalid = [this] {
        d->ui.sectionStatus->setText(tr("Could not load section planes: unsupported or invalid preset. Current clipping is unchanged."));
        return false;
    };
    QFile file(path);
    if (!file.open(QIODevice::ReadOnly) || file.size() > 65536) {
        return invalid();
    }
    QJsonParseError error;
    const auto json = QJsonDocument::fromJson(file.readAll(), &error);
    const auto root = json.object();
    if (error.error != QJsonParseError::NoError
        || root.value(QStringLiteral("format")).toString() != QStringLiteral("FreeCADPlus.SectionPlanes")
        || root.value(QStringLiteral("version")).toDouble() != 1
        || root.value(QStringLiteral("frame")).toString() != QStringLiteral("world")) {
        return invalid();
    }
    const auto planes = root.value(QStringLiteral("planes")).toArray();
    if (planes.size() != 4) {
        return invalid();
    }
    std::array<SbPlane, 4> values;
    std::array<bool, 4> enabled;
    for (int i = 0; i < 4; ++i) {
        const auto entry = planes[i].toObject();
        const auto normal = entry.value(QStringLiteral("normal")).toArray();
        const auto offset = entry.value(QStringLiteral("offsetMm"));
        if (normal.size() != 3 || !entry.value(QStringLiteral("enabled")).isBool()
            || !offset.isDouble() || !std::isfinite(offset.toDouble())
            || std::abs(offset.toDouble()) > std::numeric_limits<int>::max()) {
            return invalid();
        }
        SbVec3f direction;
        for (int j = 0; j < 3; ++j) {
            if (!normal[j].isDouble() || !std::isfinite(normal[j].toDouble())
                || std::abs(normal[j].toDouble()) > 1) {
                return invalid();
            }
            direction[j] = float(normal[j].toDouble());
        }
        if (std::abs(direction.length() - 1.0f) > 1e-5f) {
            return invalid();
        }
        if (i < 3) {
            for (int j = 0; j < 3; ++j) {
                if (direction[j] != (i == j ? (direction[j] < 0 ? -1.0f : 1.0f) : 0.0f)) {
                    return invalid();
                }
            }
        }
        values[i] = SbPlane(direction, float(offset.toDouble()));
        enabled[i] = entry.value(QStringLiteral("enabled")).toBool();
    }
    if (enabled[3] && (enabled[0] || enabled[1] || enabled[2])) {
        return invalid();
    }
    // All validation precedes changes. Presets affect this view only, never model state.
    d->ui.adjustViewdirection->setChecked(false);
    d->flipX = values[0].getNormal()[0] < 0;
    d->flipY = values[1].getNormal()[1] < 0;
    d->flipZ = values[2].getNormal()[2] < 0;
    const std::array<QDoubleSpinBox*, 4> offsets {d->ui.clipX, d->ui.clipY, d->ui.clipZ, d->ui.clipView};
    const std::array<QGroupBox*, 4> groups {d->ui.groupBoxX, d->ui.groupBoxY, d->ui.groupBoxZ, d->ui.groupBoxView};
    const std::array<SoClipPlane*, 4> clips {d->clipX, d->clipY, d->clipZ, d->clipView};
    for (int i = 0; i < 4; ++i) {
        const QSignalBlocker block(offsets[i]), groupBlock(groups[i]);
        offsets[i]->setDecimals(6);
        const bool flip = i < 3 && values[i].getNormal()[i] < 0;
        offsets[i]->setValue(values[i].getDistanceFromOrigin() * (flip ? -1 : 1));
        groups[i]->setChecked(enabled[i]);
        clips[i]->plane.setValue(values[i]);
        clips[i]->on.setValue(enabled[i]);
    }
    d->showDirection(values[3].getNormal());
    d->ui.sectionStatus->setText(tr("Section planes loaded in world coordinates. Camera and model geometry are unchanged."));
    return true;
}

#include "moc_Clipping.cpp"
