// SPDX-License-Identifier: LGPL-2.1-or-later

/******************************************************************************
 *   Copyright (c) 2012 Jan Rheinländer <jrheinlaender@users.sourceforge.net> *
 *                                                                            *
 *   This file is part of the FreeCAD CAx development system.                 *
 *                                                                            *
 *   This library is free software; you can redistribute it and/or            *
 *   modify it under the terms of the GNU Library General Public              *
 *   License as published by the Free Software Foundation; either             *
 *   version 2 of the License, or (at your option) any later version.         *
 *                                                                            *
 *   This library  is distributed in the hope that it will be useful,         *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of           *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            *
 *   GNU Library General Public License for more details.                     *
 *                                                                            *
 *   You should have received a copy of the GNU Library General Public        *
 *   License along with this library; see the file COPYING.LIB. If not,       *
 *   write to the Free Software Foundation, Inc., 59 Temple Place,            *
 *   Suite 330, Boston, MA  02111-1307, USA                                   *
 *                                                                            *
 ******************************************************************************/

#include <QMessageBox>
#include <QVBoxLayout>
#include <Bnd_Box.hxx>
#include <BRepBndLib.hxx>
#include <gp_Ax2.hxx>
#include <gp_Dir.hxx>
#include <gp_Vec.hxx>
#include <gp_Pnt.hxx>
#include <Standard_Failure.hxx>

#include <BRep_Builder.hxx>
#include <TopoDS_Compound.hxx>

#include <algorithm>
#include <list>
#include <optional>

#include <App/Document.h>
#include <App/DocumentObject.h>
#include <App/Origin.h>
#include <Mod/PartDesign/App/FeaturePattern.h>
#include <Base/Console.h>
#include <Gui/Application.h>
#include <Gui/MainWindow.h>
#include <Gui/BitmapFactory.h>
#include <QLabel>
#include <QPushButton>
#include <QVBoxLayout>
#include <Gui/Selection/Selection.h>
#include <Gui/Command.h>
#include <Gui/View3DInventor.h>
#include <Gui/View3DInventorViewer.h>
#include <Gui/ViewProviderCoordinateSystem.h>
#include <Mod/PartDesign/App/Body.h>
#include <Mod/PartDesign/App/DatumLine.h>
#include <Mod/PartDesign/App/DatumPlane.h>
#include <Mod/PartDesign/App/FeatureCircularPattern.h>
#include <Mod/PartDesign/App/FeatureLinearPattern.h>
#include <Mod/PartDesign/App/FeaturePathPattern.h>
#include <Mod/PartDesign/App/FeaturePointPattern.h>
#include <Mod/PartDesign/App/FeaturePolarPattern.h>
#include <Mod/PartDesign/App/FeatureAddSub.h>
#include <Mod/Part/Gui/PatternParametersWidget.h>
#include <Mod/Part/App/Tools.h>

#include "ui_TaskPatternParameters.h"
#include "TaskPatternParameters.h"
#include "ReferenceSelection.h"
#include "TaskMultiTransformParameters.h"


using namespace PartDesignGui;
using namespace Gui;

namespace
{

Base::Vector3d transformedVector(const Base::Vector3d& vector, const gp_Trsf& transform)
{
    gp_Vec vec = Base::convertTo<gp_Vec>(vector);
    vec.Transform(transform);
    return Base::convertTo<Base::Vector3d>(vec);
}

}  // namespace

/* TRANSLATOR PartDesignGui::TaskPatternParameters */

TaskPatternParameters::TaskPatternParameters(ViewProviderTransformed* TransformedView, QWidget* parent)
    : TaskTransformedParameters(TransformedView, parent)
    , ui(new Ui_TaskPatternParameters)
{
    setupUI();
    connect(
        this,
        &TaskTransformedParameters::originalsChanged,
        this,
        &TaskPatternParameters::refreshReferences
    );
    updatePatternSpacingLabels();
}

TaskPatternParameters::TaskPatternParameters(
    TaskMultiTransformParameters* parentTask,
    QWidget* parameterWidget
)
    : TaskTransformedParameters(parentTask)
    , ui(new Ui::TaskPatternParameters)
{
    setupParameterUI(parameterWidget);
    connect(
        parentTask,
        &TaskTransformedParameters::originalsChanged,
        this,
        &TaskPatternParameters::refreshReferences
    );
    updatePatternSpacingLabels();
}

void TaskPatternParameters::setupParameterUI(QWidget* widget)
{
    ui->setupUi(widget);  // Setup the Task's own minimal UI (placeholder)
    QMetaObject::connectSlotsByName(this);

    if (auto* point = freecad_cast<PartDesign::PointPattern*>(getObject())) {
        ui->parametersWidgetPlaceholder2->hide();
        setupPointPatternParameterUI(widget, ui->parametersWidgetPlaceholder, this, &point->PointObject);
    }
    else if (auto* path = freecad_cast<PartDesign::PathPattern*>(getObject())) {
        ui->parametersWidgetPlaceholder2->hide();
        setupPathPatternParameterUI(
            widget,
            ui->parametersWidgetPlaceholder,
            this,
            &path->Path,
            &path->Count,
            &path->SpacingMode,
            &path->Spacing,
            &path->StartOffset,
            &path->EndOffset,
            &path->ReversePath,
            &path->Align
        );
    }
    else if (auto* circular = freecad_cast<PartDesign::CircularPattern*>(getObject())) {
        ui->parametersWidgetPlaceholder2->hide();
        setupCircularPatternParameterUI(
            widget,
            ui->parametersWidgetPlaceholder,
            this,
            &circular->Axis,
            &circular->RadialDistance,
            &circular->TangentialDistance,
            &circular->NumberCircles,
            &circular->Symmetry
        );
    }
    else {
        setupPatternParameterUI(
            widget,
            ui->parametersWidgetPlaceholder,
            ui->parametersWidgetPlaceholder2,
            getTopTransformedView()->getViewer(),
            this
        );
    }

    // --- Task Specific Setup ---
    setupReferenceCollectors();
    showOriginAxes(true);  // Show origin helper axes
}

const App::PropertyLinkSub* TaskPatternParameters::referenceProperty(bool secondary) const
{
    if (auto linear = getObject<PartDesign::LinearPattern>()) {
        return secondary ? &linear->Direction2 : &linear->Direction;
    }
    if (auto polar = getObject<PartDesign::PolarPattern>()) {
        return secondary ? nullptr : &polar->Axis;
    }
    return nullptr;
}

void TaskPatternParameters::setupReferenceCollectors()
{
    auto top = getTopTransformedObject();
    if (!top || !top->isDerivedFrom<PartDesign::Pattern>()) {
        return;
    }
    const auto addCollector = [this](PartGui::PatternParametersWidget* widget, bool secondary) {
        if (!widget) {
            return;
        }
        auto layout = widget->findChild<QVBoxLayout*>(QStringLiteral("mainLayout"));
        if (!layout) {
            return;
        }
        auto status = new QLabel(widget);
        status->setTextFormat(Qt::PlainText);
        status->setWordWrap(true);
        status->setObjectName(secondary ? QStringLiteral("patternReferenceStatus2")
                                        : QStringLiteral("patternReferenceStatus"));
        auto highlight = new QPushButton(widget);
        highlight->setObjectName(secondary ? QStringLiteral("patternHighlightReference2")
                                           : QStringLiteral("patternHighlightReference"));
        layout->insertWidget(1, status);
        layout->insertWidget(2, highlight);
        if (secondary) {
            referenceStatus2 = status;
            referenceHighlight2 = highlight;
        }
        else {
            referenceStatus = status;
            referenceHighlight = highlight;
        }
        connect(highlight, &QPushButton::clicked, this, [this, secondary] {
            if (auto property = referenceProperty(secondary); property && property->getValue()) {
                auto object = property->getValue();
                const auto subs = property->getSubValues();
                highlightReference(object, subs);
                // Inspection cancels pending picking. Restore both combos from
                // their saved links so OK cannot apply a "Select reference" item.
                if (auto primary = getPrimaryParametersWidget()) {
                    primary->updateReferenceUI();
                }
                if (auto secondaryWidget = getSecondaryParametersWidget()) {
                    secondaryWidget->updateReferenceUI();
                }
                updateReferenceCollectors();
            }
        });
    };
    addCollector(getPrimaryParametersWidget(), false);
    addCollector(getSecondaryParametersWidget(), true);
    updateReferenceCollectors();
}

void TaskPatternParameters::updateReferenceCollectors()
{
    const auto update = [this](bool secondary, QLabel* status, QPushButton* highlight) {
        if (!status) {
            return;
        }
        const auto property = referenceProperty(secondary);
        const bool assigned = property && property->getValue();
        const bool picking = selectionMode == SelectionMode::Reference
            && getActiveDirectionWidget() == (secondary ? getSecondaryParametersWidget()
                                                       : getPrimaryParametersWidget());
        status->setText(tr("References: %1\n%2").arg(assigned ? 1 : 0).arg(
            picking ? tr("Picking reference") : tr("Reference picking inactive")));
        status->setToolTip(tr("Accepts compatible edges, faces and datum axes."));
        highlight->setText(tr("Highlight reference"));
        highlight->setToolTip(tr("Inspect the stored reference without changing it"));
        highlight->setEnabled(assigned);
    };
    update(false, referenceStatus, referenceHighlight);
    update(true, referenceStatus2, referenceHighlight2);
}

void TaskPatternParameters::refreshReferences()
{
    if (auto* primary = getPrimaryParametersWidget()) {
        fillDirectionCombo(primary->dirLinks, Part::LinearPatternDirection::First);
    }
    if (auto* secondary = getSecondaryParametersWidget()) {
        fillDirectionCombo(secondary->dirLinks, Part::LinearPatternDirection::Second);
    }
    updatePatternParameterUI();
    updateReferenceCollectors();
    updatePatternSpacingLabels();
}

void TaskPatternParameters::retranslateParameterUI(QWidget* widget)
{
    ui->retranslateUi(widget);
    updateReferenceCollectors();
}

App::DocumentObject* TaskPatternParameters::getPatternObject() const
{
    return getObject();
}

void TaskPatternParameters::fillDirectionCombo(Gui::ComboLinks& combo, Part::LinearPatternDirection /*direction*/)
{
    auto* sketch = freecad_cast<Part::Part2DObject*>(getSketchObject());
    this->fillAxisCombo(combo, sketch);
}

void TaskPatternParameters::setupPatternTransaction()
{
    setupTransaction();
}

void TaskPatternParameters::recomputePatternFeature()
{
    recomputeFeature();
}

Base::Vector3d TaskPatternParameters::getPatternStartPoint() const
{
    return getStartPoint();
}

Base::Vector3d TaskPatternParameters::getLinearPatternFallbackDirection(
    Part::LinearPatternDirection direction
) const
{
    if (direction == Part::LinearPatternDirection::Second) {
        return Base::Vector3d::UnitY;
    }

    return Base::Vector3d::UnitZ;
}

Base::Vector3d TaskPatternParameters::transformLinearPatternDirection(
    const Base::Vector3d& direction
) const
{
    auto* transformed = freecad_cast<PartDesign::Transformed*>(getObject());
    if (!transformed) {
        return direction;
    }

    return transformedVector(direction, transformed->getLocation().Transformation());
}

Base::Vector3d TaskPatternParameters::getLinearPatternLabelPlaneNormal(Part::LinearPatternDirection) const
{
    return transformLinearPatternDirection(Base::Vector3d::UnitZ);
}

void TaskPatternParameters::transformPolarPatternAxis(gp_Ax2& axis) const
{
    auto* transformed = freecad_cast<PartDesign::Transformed*>(getObject());
    if (transformed) {
        axis.Transform(transformed->getLocation().Transformation());
    }
}

std::string TaskPatternParameters::buildDirectionReferencePythonString(
    const App::DocumentObject* obj,
    const std::vector<std::string>& subs
) const
{
    return buildLinkSingleSubPythonStr(obj, subs);
}

// --- Task-Specific Logic ---

void TaskPatternParameters::showOriginAxes(bool show)
{
    PartDesign::Body* body = PartDesign::Body::findBodyOf(getTopTransformedObject());
    if (body) {
        try {
            App::Origin* origin = body->getOrigin();
            auto vpOrigin = freecad_cast<ViewProviderCoordinateSystem*>(
                Gui::Application::Instance->getViewProvider(origin)
            );
            if (!vpOrigin) {
                return;
            }
            if (show) {
                vpOrigin->setTemporaryVisibility(Gui::DatumElement::Axes);
            }
            else {
                vpOrigin->resetTemporaryVisibility();
            }
        }
        catch (const Base::Exception& ex) {
            Base::Console().error("TaskPatternParameters: Error accessing origin axes: {}\n", ex.what());
        }
    }
}

void TaskPatternParameters::enterReferenceSelectionMode()
{
    if (selectionMode == SelectionMode::Reference) {
        return;
    }

    if (getTopTransformedObject()->isDerivedFrom<PartDesign::Pattern>()) {
        // The combined task has a separate originals controller. End its role
        // before accepting a pick for a direction or axis.
        exitSelectionMode();
    }

    hideObject();  // Hide the pattern feature itself
    showBase();    // Show the base features/body
    Gui::Selection().clearSelection();
    if (getObject()->isDerivedFrom<PartDesign::PointPattern>()) {
        // Clicking visible sketch/shape geometry produces a subelement selection, even though
        // PointObject stores the whole object. Accept every shape subelement here and discard the
        // subelement below when assigning the property.
        addReferenceSelectionGate(
            AllowSelection::POINT | AllowSelection::EDGE | AllowSelection::FACE | AllowSelection::WHOLE
        );
        Gui::getMainWindow()->showMessage(tr("Select a sketch or shape containing the pattern points"));
    }
    else if (getObject()->isDerivedFrom<PartDesign::PathPattern>()) {
        // Whole sketches and SubShapeBinders supply all their edges. A single selected edge is
        // also supported until a proper multi-reference selection widget is available.
        addReferenceSelectionGate(AllowSelection::EDGE | AllowSelection::FACE | AllowSelection::WHOLE);
        Gui::getMainWindow()->showMessage(tr("Select a sketch, Sub-Shape Binder, or path edge"));
    }
    else {
        const bool isPolar = getObject()->isDerivedFrom<PartDesign::PolarPattern>()
            || getObject()->isDerivedFrom<PartDesign::CircularPattern>();
        const AllowSelectionFlags commonReferences = AllowSelection::EDGE | AllowSelection::PLANAR;
        addReferenceSelectionGate(
            commonReferences | (isPolar ? AllowSelection::CIRCLE : AllowSelection::FACE)
        );
        Gui::getMainWindow()->showMessage(tr("Select a direction reference (edge, face, datum line)"));
    }
}

void TaskPatternParameters::exitReferenceSelectionMode()
{
    exitSelectionMode();

    hideBase();
    Gui::getMainWindow()->showMessage(QString());
    clearActiveDirectionWidget();
    updateReferenceCollectors();
}

void TaskPatternParameters::cancelReferenceSelection()
{
    if (selectionMode == SelectionMode::Reference) {
        exitReferenceSelectionMode();
    }
}


// --- SLOTS ---

void TaskPatternParameters::onReferenceSelectionRequested()
{
    // The embedded widget wants to enter reference selection mode
    enterReferenceSelectionMode();
    selectionMode = SelectionMode::Reference;
    updateReferenceCollectors();
}

void TaskPatternParameters::onPatternParametersChanged()
{
    updateReferenceCollectors();
    // A parameter in the embedded widget changed, trigger a recompute
    if (blockUpdate) {
        return;  // Avoid loops if change originated from Task update
    }
    PartGui::TaskPatternParameters::kickUpdateViewTimer();  // Debounce recompute
}

void TaskPatternParameters::onUpdateView(bool on)
{
    blockUpdate = !on;
    if (on) {
        PartGui::TaskPatternParameters::kickUpdateViewTimer();
    }
    else {
        cancelPendingUpdate();
    }
}

void TaskPatternParameters::onSelectionChanged(const Gui::SelectionChanges& msg)
{
    // Handle selection ONLY when in reference selection mode
    if (selectionMode == SelectionMode::None || msg.Type != Gui::SelectionChanges::AddSelection) {
        return;
    }

    if (originalSelected(msg)) {
        exitSelectionMode();
        return;
    }

    auto patternObj = getObject();
    if (!patternObj) {
        return;
    }

    std::vector<std::string> directions;
    App::DocumentObject* selObj = nullptr;
    getReferencedSelection(getTopTransformedObject(), msg, selObj, directions);
    if (!selObj) {
        const QString warning = [patternObj]() {
            if (patternObj->isDerivedFrom<PartDesign::PointPattern>()) {
                return tr("Invalid selection. Select a sketch or shape containing points.");
            }
            if (patternObj->isDerivedFrom<PartDesign::PathPattern>()) {
                return tr("Invalid selection. Select a sketch, Sub-Shape Binder, or path edge.");
            }
            return tr("Invalid selection. Select an edge, planar face, or datum line.");
        }();
        Base::Console().warning("{}\n", warning.toUtf8().constData());
        return;
    }

    // Note: ReferenceSelection has already checked the selection for validity
    if (selectionMode == SelectionMode::Reference || selObj->isDerivedFrom<App::Line>()) {
        setupTransaction();

        if (auto* linearPattern = freecad_cast<PartDesign::LinearPattern*>(patternObj)) {
            if (getActiveDirectionWidget() == getPrimaryParametersWidget()) {
                linearPattern->Direction.setValue(selObj, directions);
            }
            else {
                linearPattern->Direction2.setValue(selObj, directions);
            }
        }
        else if (auto* circularPattern = freecad_cast<PartDesign::CircularPattern*>(patternObj)) {
            circularPattern->Axis.setValue(selObj, directions);
        }
        else if (auto* pathPattern = freecad_cast<PartDesign::PathPattern*>(patternObj)) {
            pathPattern->Path.setValue(selObj, directions);
        }
        else if (auto* pointPattern = freecad_cast<PartDesign::PointPattern*>(patternObj)) {
            pointPattern->PointObject.setValue(selObj);
        }
        else if (auto* polarPattern = freecad_cast<PartDesign::PolarPattern*>(patternObj)) {
            polarPattern->Axis.setValue(selObj, directions);
        }
        recomputePatternFeature();
        updatePatternParameterUI();
    }
    exitReferenceSelectionMode();
}

TaskPatternParameters::~TaskPatternParameters()
{
    cancelPendingUpdate();
    showOriginAxes(false);         // Clean up temporary visibility
    exitReferenceSelectionMode();  // Ensure gates are removed etc.
}

void TaskPatternParameters::apply()
{
    auto pattern = getObject();
    if (!pattern
        || (!getPrimaryParametersWidget() && !getCircularParametersWidget()
            && !getPathParametersWidget() && !getPointParametersWidget())) {
        return;
    }

    applyPatternParameters(pattern);

    // The user may have changed a value and immediately hit 'OK' or Enter.
    // This triggers accept() before the update timer for the 3D view has a
    // chance to fire. If the timer is active, it means a recompute is
    // pending.
    if (!consumePendingUpdate() && blockUpdate) {
        recomputePatternFeature();
    }
}

Base::Vector3d TaskPatternParameters::getStartPoint() const
{
    Base::Vector3d startPoint(0, 0, 0);

    auto* pattern = freecad_cast<PartDesign::Transformed*>(getObject());
    if (!pattern) {
        return startPoint;
    }

    std::vector<App::DocumentObject*> originals = getTopTransformedObject()->getOriginals();
    if (!originals.empty()) {
        BRep_Builder builder;
        TopoDS_Compound compoundShape;
        builder.MakeCompound(compoundShape);

        // 2. Collect the "delta" shapes from each original feature.
        for (App::DocumentObject* obj : originals) {
            // We are only interested in additive/subtractive features.
            if (auto* addSubFeature = freecad_cast<PartDesign::FeatureAddSub*>(obj)) {
                const Part::TopoShape& deltaShape = addSubFeature->AddSubShape.getShape();
                if (!deltaShape.getShape().IsNull()) {
                    TopoDS_Shape shape = deltaShape.getShape();
                    shape.Move(addSubFeature->getLocation());
                    builder.Add(compoundShape, shape);
                }
            }
        }

        // 3. If we collected any shapes, calculate the center of their combined bounding box.
        if (!compoundShape.IsNull()) {
            try {
                Bnd_Box bndBox;
                BRepBndLib::Add(compoundShape, bndBox);
                if (!bndBox.IsVoid()) {
                    double xmin, ymin, zmin, xmax, ymax, zmax;
                    bndBox.Get(xmin, ymin, zmin, xmax, ymax, zmax);
                    startPoint.x = (xmin + xmax) / 2.0;
                    startPoint.y = (ymin + ymax) / 2.0;
                    startPoint.z = (zmin + zmax) / 2.0;
                }
            }
            catch (const Base::Exception& e) {
                Base::Console().warning(
                    "Could not calculate center of patterned features: {}\n",
                    e.what()
                );
                // startPoint remains (0,0,0) as a fallback.
            }
        }
    }
    return startPoint;
}

//**************************************************************************
// TaskDialog Implementation (Remains largely the same)
//**************************************************************************

TaskDlgLinearPatternParameters::TaskDlgLinearPatternParameters(
    ViewProviderTransformed* LinearPatternView
)
    : TaskDlgTransformedParameters(LinearPatternView)  // Use base class constructor
{
    // Create the specific parameter task panel
    parameter = new TaskPatternParameters(LinearPatternView);
    // Add it to the dialog's content list
    Content.push_back(parameter);
    Content.push_back(preview);
}

#include "moc_TaskPatternParameters.cpp"
