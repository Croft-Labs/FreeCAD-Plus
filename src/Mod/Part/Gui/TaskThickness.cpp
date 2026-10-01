// SPDX-License-Identifier: LGPL-2.1-or-later

/***************************************************************************
 *   Copyright (c) 2012 Werner Mayer <wmayer[at]users.sourceforge.net>     *
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

#include <limits>

#include <App/Application.h>
#include <App/Document.h>
#include <App/DocumentObject.h>
#include <Base/Tools.h>
#include <Gui/Application.h>
#include <Gui/BitmapFactory.h>
#include <Gui/Command.h>
#include <Gui/CommandT.h>
#include <Gui/Document.h>
#include <Gui/Selection/Selection.h>
#include <Gui/Selection/SelectionFilter.h>
#include <Gui/Selection/SelectionObject.h>
#include <Gui/ViewProvider.h>
#include <Gui/Inventor/Draggers/Gizmo.h>
#include <Mod/Part/App/GizmoHelper.h>
#include <Mod/Part/App/PartFeatures.h>

#include "TaskThickness.h"
#include "ViewProvider.h"
#include "ui_TaskOffset.h"


using namespace PartGui;

class ThicknessWidget::Private
{
public:
    Ui_TaskOffset ui {};
    QString text;
    std::string selection;
    Part::Thickness* thickness {nullptr};

    class FaceSelection: public Gui::SelectionFilterGate
    {
        const App::DocumentObject* object;

    public:
        explicit FaceSelection(const App::DocumentObject* obj)
            : Gui::SelectionFilterGate(nullPointer())
            , object(obj)
        {}
        bool allow(App::Document* /*pDoc*/, App::DocumentObject* pObj, const char* sSubName) override
        {
            if (pObj != this->object) {
                return false;
            }
            if (Base::Tools::isNullOrEmpty(sSubName)) {
                return false;
            }
            std::string element(sSubName);
            return element.substr(0, 4) == "Face";
        }
    };
};

/* TRANSLATOR PartGui::ThicknessWidget */

ThicknessWidget::ThicknessWidget(Part::Thickness* thickness, QWidget* parent)
    : d(new Private())
{
    Q_UNUSED(parent);
    Gui::Command::runCommand(Gui::Command::App, "from FreeCAD import Base");
    Gui::Command::runCommand(Gui::Command::App, "import Part");

    d->thickness = thickness;
    d->ui.setupUi(this);
    setupConnections();

    d->ui.fillOffset->hide();
    d->ui.labelOffset->setText(tr("Signed thickness"));
    d->ui.facesButton->setText(tr("Removed faces"));
    d->ui.labelFaces->setWordWrap(true);
    d->ui.labelFaces->setTextFormat(Qt::PlainText);

    QSignalBlocker blockOffset(d->ui.spinOffset);
    d->ui.spinOffset->setRange(-std::numeric_limits<int>::max(), std::numeric_limits<int>::max());
    d->ui.spinOffset->setSingleStep(0.1);
    d->ui.spinOffset->setValue(d->thickness->Value.getValue());

    int mode = d->thickness->Mode.getValue();
    d->ui.modeType->setCurrentIndex(mode);

    int join = d->thickness->Join.getValue();
    d->ui.joinType->setCurrentIndex(join);

    QSignalBlocker blockIntSct(d->ui.intersection);
    bool intsct = d->thickness->Intersection.getValue();
    d->ui.intersection->setChecked(intsct);

    QSignalBlocker blockSelfInt(d->ui.selfIntersection);
    bool selfint = d->thickness->SelfIntersection.getValue();
    d->ui.selfIntersection->setChecked(selfint);

    d->ui.spinOffset->bind(d->thickness->Value);

    // The interactive gizmos are implemented for this operation just as a proof
    // of concept. And so, it is kept disabled until the other operations of the
    // Part workbench are covered.
    // setupGizmos();
    updateResultStatus();
}

ThicknessWidget::~ThicknessWidget()
{
    delete d;
    Gui::Selection().rmvSelectionGate();
}

void ThicknessWidget::setupConnections()
{
    // clang-format off
    connect(d->ui.spinOffset, qOverload<double>(&Gui::QuantitySpinBox::valueChanged),
            this, &ThicknessWidget::onSpinOffsetValueChanged);
    connect(d->ui.modeType, qOverload<int>(&QComboBox::activated),
            this, &ThicknessWidget::onModeTypeActivated);
    connect(d->ui.joinType, qOverload<int>(&QComboBox::activated),
            this, &ThicknessWidget::onJoinTypeActivated);
    connect(d->ui.intersection, &QCheckBox::toggled,
            this, &ThicknessWidget::onIntersectionToggled);
    connect(d->ui.selfIntersection, &QCheckBox::toggled,
            this, &ThicknessWidget::onSelfIntersectionToggled);
    connect(d->ui.facesButton, &QPushButton::toggled,
            this, &ThicknessWidget::onFacesButtonToggled);
    connect(d->ui.updateView, &QCheckBox::toggled,
            this, &ThicknessWidget::onUpdateViewToggled);
    connect(d->ui.reverseSide, &QPushButton::clicked, this, [this]() {
        if (!d->ui.spinOffset->hasExpression()) {
            d->ui.spinOffset->setValue(-d->ui.spinOffset->value().getValue());
        }
    });
    // clang-format on
}

Part::Thickness* ThicknessWidget::getObject() const
{
    return d->thickness;
}

void ThicknessWidget::onSpinOffsetValueChanged(double val)
{
    d->thickness->Value.setValue(val);
    updatePreview();
}

void ThicknessWidget::onModeTypeActivated(int val)
{
    d->thickness->Mode.setValue(val);
    updatePreview();
}

void ThicknessWidget::onJoinTypeActivated(int val)
{
    d->thickness->Join.setValue((long)val);
    updatePreview();
}

void ThicknessWidget::onIntersectionToggled(bool on)
{
    d->thickness->Intersection.setValue(on);
    updatePreview();
}

void ThicknessWidget::onSelfIntersectionToggled(bool on)
{
    d->thickness->SelfIntersection.setValue(on);
    updatePreview();
}

void ThicknessWidget::onFacesButtonToggled(bool on)
{
    if (on) {
        QList<QWidget*> c = this->findChildren<QWidget*>();
        for (auto it : c) {
            it->setEnabled(false);
        }
        d->ui.facesButton->setEnabled(true);
        d->ui.labelFaces->setText(tr("Select faces of the source object and press 'Done'"));
        d->ui.labelFaces->setEnabled(true);
        d->text = d->ui.facesButton->text();
        d->ui.facesButton->setText(tr("Done"));

        Gui::Application::Instance->showViewProvider(d->thickness->Faces.getValue());
        Gui::Application::Instance->hideViewProvider(d->thickness);
        Gui::Selection().clearSelection();
        Gui::Selection().addSelectionGate(new Private::FaceSelection(d->thickness->Faces.getValue()));
        // Seed the native collector so reopening it preserves the current choice.
        for (const auto& face : d->thickness->Faces.getSubValues()) {
            Gui::Selection().addSelection(d->thickness->getDocument()->getName(),
                                          d->thickness->Faces.getValue()->getNameInDocument(),
                                          face.c_str());
        }

        if (gizmoContainer) {
            gizmoContainer->visible = false;
        }
    }
    else {
        QList<QWidget*> c = this->findChildren<QWidget*>();
        for (auto it : c) {
            it->setEnabled(true);
        }
        d->ui.facesButton->setText(d->text);
        d->ui.labelFaces->clear();

        std::vector<std::string> faces;
        for (const auto& item : Gui::Selection().getSelectionEx()) {
            if (item.getObject() == d->thickness->Faces.getValue()) {
                faces = item.getSubNames();
                break;
            }
        }
        d->thickness->Faces.setValue(d->thickness->Faces.getValue(), faces);
        d->selection = Gui::Command::getPythonTuple(
            d->thickness->Faces.getValue()->getNameInDocument(),
            d->thickness->Faces.getSubValues()
        );
        Gui::Selection().rmvSelectionGate();
        Gui::Application::Instance->showViewProvider(d->thickness);
        Gui::Application::Instance->hideViewProvider(d->thickness->Faces.getValue());
        updatePreview();

        if (gizmoContainer) {
            gizmoContainer->visible = true;
            setGizmoPositions();
        }
    }
}

void ThicknessWidget::onUpdateViewToggled(bool)
{
    updatePreview();
}

void ThicknessWidget::updatePreview()
{
    if (d->ui.updateView->isChecked()) {
        d->thickness->getDocument()->recomputeFeature(d->thickness);
    }
    updateResultStatus();
}

void ThicknessWidget::updateResultStatus()
{
    d->ui.reverseSide->setEnabled(!d->ui.spinOffset->hasExpression());
    d->ui.reverseSide->setToolTip(tr("Reverse the thickness sign. For a formula, edit its expression."));
    d->ui.sideHelp->setText(tr("Positive thickness grows outward; negative grows inward for an "
                             "outward-oriented solid. Selected faces become openings. "
                             "The result stays linked to its source."));
    auto* source = d->thickness->Faces.getValue();
    QStringList faces;
    for (const auto& face : d->thickness->Faces.getSubValues()) {
        faces.append(QString::fromStdString(face));
    }
    if (!d->ui.facesButton->isChecked()) {
        d->ui.labelFaces->setText(tr("Source: %1\nRemoved faces: %2")
            .arg(source ? QString::fromStdString(source->getFullName()) : tr("missing"))
            .arg(faces.isEmpty() ? tr("none (closed thick solid)") : faces.join(QStringLiteral(", "))));
    }
    if (!d->thickness->isValid()) {
        d->ui.resultStatus->setText(tr("Thickness failed. Displayed geometry may be the last valid result. "
                                      "Adjust thickness, faces or join type, or cancel.\n%1")
            .arg(QString::fromUtf8(d->thickness->getStatusString())));
    }
    else if (!d->ui.updateView->isChecked() && d->thickness->isTouched()) {
        d->ui.resultStatus->setText(tr("Preview pending. Enable Update view or press OK to recompute."));
    }
    else {
        const auto& shape = d->thickness->Shape.getShape();
        d->ui.resultStatus->setText(!shape.isNull() && shape.isValid()
            ? tr("Valid result: %1 solid(s), %2 face(s).")
                .arg(qulonglong(shape.countSubShapes(TopAbs_SOLID)))
                .arg(qulonglong(shape.countSubShapes(TopAbs_FACE)))
            : tr("No valid result. Adjust settings or cancel."));
    }
}

bool ThicknessWidget::accept()
{
    if (d->ui.facesButton->isChecked()) {
        return false;
    }

    try {
        if (!d->selection.empty()) {
            Gui::cmdAppObjectArgs(d->thickness, "Faces = %s", d->selection.c_str());
        }
        Gui::cmdAppObjectArgs(d->thickness, "Value = %.17g", d->ui.spinOffset->value().getValue());
        d->ui.spinOffset->apply();
        Gui::cmdAppObjectArgs(d->thickness, "Mode = %d", d->ui.modeType->currentIndex());
        Gui::cmdAppObjectArgs(d->thickness, "Join = %d", d->ui.joinType->currentIndex());
        Gui::cmdAppObjectArgs(
            d->thickness,
            "Intersection = %s",
            d->ui.intersection->isChecked() ? "True" : "False"
        );
        Gui::cmdAppObjectArgs(
            d->thickness,
            "SelfIntersection = %s",
            d->ui.selfIntersection->isChecked() ? "True" : "False"
        );

        Gui::cmdAppDocument(d->thickness, "recompute()");
        updateResultStatus();
        const auto& shape = d->thickness->Shape.getShape();
        if (!d->thickness->isValid()) {
            throw Base::CADKernelError(d->thickness->getStatusString());
        }
        if (shape.isNull() || !shape.isValid() || shape.countSubShapes(TopAbs_SOLID) != 1) {
            throw Base::CADKernelError("Thickness did not produce one valid solid.");
        }
        auto* doc = d->thickness->getDocument();
        Gui::cmdGuiDocument(d->thickness, "resetEdit()");
        doc->commitTransaction();  // ViewProviderDocumentObject::startDefaultEditMode()
    }
    catch (const Base::Exception& e) {
        // Keep the native edit transaction alive for correction. Aborting can delete
        // a newly created feature while this panel still holds its pointer.
        d->ui.resultStatus->setText(tr("Cannot accept thickness. Displayed geometry may be the last valid result. "
                                         "Adjust settings or cancel.\n%1")
            .arg(QCoreApplication::translate("Exception", e.what())));
        return false;
    }

    return true;
}

bool ThicknessWidget::reject()
{
    if (d->ui.facesButton->isChecked()) {
        return false;
    }

    auto* doc = d->thickness->getDocument();
    // Aborting may delete the feature and task panel; retain only its document.
    doc->abortTransaction();
    Gui::Command::doCommand(Gui::Command::Gui, "Gui.getDocument('%s').resetEdit()", doc->getName());
    Gui::Command::updateActive();

    return true;
}

void ThicknessWidget::changeEvent(QEvent* e)
{
    QWidget::changeEvent(e);
    if (e->type() == QEvent::LanguageChange) {
        d->ui.retranslateUi(this);
        d->ui.labelOffset->setText(tr("Signed thickness"));
        d->ui.facesButton->setText(tr("Removed faces"));
        updateResultStatus();
    }
}

void ThicknessWidget::setupGizmos()
{
    if (!Gui::GizmoContainer::isEnabled()) {
        return;
    }

    linearGizmo = new Gui::LinearGizmo(d->ui.spinOffset);

    auto vp = Base::freecad_cast<ViewProviderPart*>(
        Gui::Application::Instance->getViewProvider(d->thickness)
    );
    if (!vp) {
        delete linearGizmo;
        return;
    }
    gizmoContainer = Gui::GizmoContainer::create({linearGizmo}, vp);

    setGizmoPositions();
}

void ThicknessWidget::setGizmoPositions()
{
    if (!gizmoContainer) {
        return;
    }

    Part::Thickness* thickness = getObject();
    auto base = Part::Thickness::getTopoShape(
        thickness->Faces.getValue(),
        Part::ShapeOption::ResolveLink | Part::ShapeOption::Transform
    );
    auto faces = thickness->Faces.getSubValues(true);

    if (faces.size() == 0) {
        gizmoContainer->visible = false;
    }

    Part::TopoShape face = base.getSubTopoShape(faces[0].c_str());
    if (face.getShape().ShapeType() == TopAbs_FACE) {
        auto edges = getAdjacentEdgesFromFace(face);
        assert(edges.size() != 0 && "A face without any edges? Please file a bug report");
        DraggerPlacementProps props = getDraggerPlacementFromEdgeAndFace(edges[0], face);

        // The part thickness operation by default goes creates towards outside
        // so -props.dir is taken
        linearGizmo->Gizmo::setDraggerPlacement(props.position, -props.dir);

        gizmoContainer->visible = true;

        return;
    }
}


/* TRANSLATOR PartGui::TaskThickness */

TaskThickness::TaskThickness(Part::Thickness* offset)
{
    widget = new ThicknessWidget(offset);
    widget->setWindowTitle(ThicknessWidget::tr("Thickness"));
    addTaskBox(Gui::BitmapFactory().pixmap("Part_Thickness"), widget);
}

Part::Thickness* TaskThickness::getObject() const
{
    return widget->getObject();
}

void TaskThickness::open()
{}

void TaskThickness::clicked(int)
{}

bool TaskThickness::accept()
{
    return widget->accept();
}

bool TaskThickness::reject()
{
    return widget->reject();
}

#include "moc_TaskThickness.cpp"
