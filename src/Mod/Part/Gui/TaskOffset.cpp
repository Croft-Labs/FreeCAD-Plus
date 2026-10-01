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

#include <QMessageBox>

#include <App/Application.h>
#include <App/Document.h>
#include <App/DocumentObject.h>
#include <Gui/Application.h>
#include <Gui/BitmapFactory.h>
#include <Gui/CommandT.h>
#include <Gui/Document.h>
#include <Gui/ViewProvider.h>
#include <Mod/Part/App/FeatureOffset.h>

#include "TaskOffset.h"
#include "ui_TaskOffset.h"


using namespace PartGui;

class OffsetWidget::Private
{
public:
    Ui_TaskOffset ui {};
    Part::Offset* offset {nullptr};
};

/* TRANSLATOR PartGui::OffsetWidget */

OffsetWidget::OffsetWidget(Part::Offset* offset, QWidget* parent)
    : d(new Private())
{
    Q_UNUSED(parent);
    Gui::Command::runCommand(Gui::Command::App, "from FreeCAD import Base");
    Gui::Command::runCommand(Gui::Command::App, "import Part");

    d->offset = offset;
    // Direct setEdit/Std_Edit also needs a transaction for preview rollback.
    if (!offset->getDocument()->hasPendingTransaction()) {
        offset->getDocument()->openTransaction("Edit offset");
    }
    d->ui.setupUi(this);
    setupConnections();

    d->ui.spinOffset->setUnit(Base::Unit::Length);
    d->ui.spinOffset->setRange(-std::numeric_limits<int>::max(), std::numeric_limits<int>::max());
    d->ui.spinOffset->setSingleStep(0.1);
    d->ui.facesButton->hide();

    bool is_2d = d->offset->isDerivedFrom<Part::Offset2D>();
    d->ui.selfIntersection->setVisible(!is_2d);
    if (is_2d) {
        d->ui.modeType->removeItem(2);  // remove Recto-Verso mode, not supported by 2d offset
    }

    // block signals to fill values read out from feature...
    bool block = true;
    d->ui.fillOffset->blockSignals(block);
    d->ui.intersection->blockSignals(block);
    d->ui.selfIntersection->blockSignals(block);
    d->ui.modeType->blockSignals(block);
    d->ui.joinType->blockSignals(block);
    d->ui.spinOffset->blockSignals(block);

    // read values from feature
    d->ui.spinOffset->setValue(d->offset->Value.getValue());
    d->ui.fillOffset->setChecked(offset->Fill.getValue());
    d->ui.intersection->setChecked(offset->Intersection.getValue());
    d->ui.selfIntersection->setChecked(offset->SelfIntersection.getValue());
    long mode = offset->Mode.getValue();
    if (mode >= 0 && mode < d->ui.modeType->count()) {
        d->ui.modeType->setCurrentIndex(mode);
    }
    long join = offset->Join.getValue();
    if (join >= 0 && join < d->ui.joinType->count()) {
        d->ui.joinType->setCurrentIndex(join);
    }

    // unblock signals
    block = false;
    d->ui.fillOffset->blockSignals(block);
    d->ui.intersection->blockSignals(block);
    d->ui.selfIntersection->blockSignals(block);
    d->ui.modeType->blockSignals(block);
    d->ui.joinType->blockSignals(block);
    d->ui.spinOffset->blockSignals(block);

    d->ui.spinOffset->bind(d->offset->Value);
    d->ui.reverseSide->setVisible(!is_2d);
    d->ui.sideHelp->setVisible(!is_2d);
    d->ui.resultStatus->setVisible(!is_2d);
    if (!is_2d) {
        d->ui.fillOffset->setText(tr("Fill between source and offset"));
        d->ui.labelOffset->setText(tr("Signed distance"));
    }
    updateResultStatus();
}

OffsetWidget::~OffsetWidget()
{
    delete d;
}

void OffsetWidget::setupConnections()
{
    // clang-format off
    connect(d->ui.spinOffset, qOverload<double>(&Gui::QuantitySpinBox::valueChanged),
            this, &OffsetWidget::onSpinOffsetValueChanged);
    connect(d->ui.modeType, qOverload<int>(&QComboBox::activated),
            this, &OffsetWidget::onModeTypeActivated);
    connect(d->ui.joinType, qOverload<int>(&QComboBox::activated),
            this, &OffsetWidget::onJoinTypeActivated);
    connect(d->ui.intersection, &QCheckBox::toggled,
            this, &OffsetWidget::onIntersectionToggled);
    connect(d->ui.selfIntersection, &QCheckBox::toggled,
            this, &OffsetWidget::onSelfIntersectionToggled);
    connect(d->ui.fillOffset, &QCheckBox::toggled,
            this, &OffsetWidget::onFillOffsetToggled);
    connect(d->ui.updateView, &QCheckBox::toggled,
            this, &OffsetWidget::onUpdateViewToggled);
    connect(d->ui.reverseSide, &QPushButton::clicked, this, &OffsetWidget::onReverseSide);
    // clang-format on
}

Part::Offset* OffsetWidget::getObject() const
{
    return d->offset;
}

void OffsetWidget::onSpinOffsetValueChanged(double val)
{
    d->offset->Value.setValue(val);
    updatePreview();
}

void OffsetWidget::onModeTypeActivated(int val)
{
    d->offset->Mode.setValue(val);
    updatePreview();
}

void OffsetWidget::onJoinTypeActivated(int val)
{
    d->offset->Join.setValue((long)val);
    updatePreview();
}

void OffsetWidget::onIntersectionToggled(bool on)
{
    d->offset->Intersection.setValue(on);
    updatePreview();
}

void OffsetWidget::onSelfIntersectionToggled(bool on)
{
    d->offset->SelfIntersection.setValue(on);
    updatePreview();
}

void OffsetWidget::onFillOffsetToggled(bool on)
{
    d->offset->Fill.setValue(on);
    updatePreview();
}

void OffsetWidget::onUpdateViewToggled(bool)
{
    updatePreview();
}

void OffsetWidget::onReverseSide()
{
    // Never replace a saved formula with its evaluated number.
    if (d->ui.spinOffset->hasExpression()) {
        d->ui.resultStatus->setText(tr("Edit the distance expression to reverse its side."));
        return;
    }
    d->ui.spinOffset->setValue(-d->ui.spinOffset->value().getValue());
}

void OffsetWidget::updatePreview()
{
    if (d->ui.updateView->isChecked()) {
        d->offset->getDocument()->recomputeFeature(d->offset);
    }
    updateResultStatus();
}

void OffsetWidget::updateResultStatus()
{
    if (d->offset->isDerivedFrom<Part::Offset2D>()) {
        return;
    }
    d->ui.sideHelp->setText(
        tr("Positive follows the sheet normals; negative uses the opposite side. "
           "For a filled sheet, the absolute distance is the one-sided thickness. "
           "The result is separate and remains linked to its source.")
    );
    d->ui.reverseSide->setEnabled(!d->ui.spinOffset->hasExpression());
    d->ui.reverseSide->setToolTip(tr("Reverse the distance sign. For a formula, edit its expression."));
    if (!d->offset->isValid()) {
        d->ui.resultStatus->setText(
            tr("Offset failed. Displayed geometry may be from the last successful result. "
               "Adjust the distance/side or cancel.\n%1")
                .arg(QString::fromUtf8(d->offset->getStatusString()))
        );
        return;
    }
    if (!d->ui.updateView->isChecked() && d->offset->isTouched()) {
        d->ui.resultStatus->setText(tr("Preview pending. Enable Update view or press OK to recompute."));
        return;
    }
    const auto& shape = d->offset->Shape.getShape();
    if (shape.isNull()) {
        d->ui.resultStatus->setText(tr("No result. Adjust the offset settings."));
        return;
    }
    const auto solids = shape.countSubShapes(TopAbs_SOLID);
    const auto faces = shape.countSubShapes(TopAbs_FACE);
    if (solids > 0 && shape.isValid()) {
        d->ui.resultStatus->setText(tr("Valid result: %1 solid(s), %2 face(s).")
                                      .arg(qulonglong(solids)).arg(qulonglong(faces)));
    }
    else {
        d->ui.resultStatus->setText(tr("Offset sheet result: %1 face(s), no validated solid.")
                                      .arg(qulonglong(faces)));
    }
}

bool OffsetWidget::accept()
{
    try {
        double offsetValue = d->ui.spinOffset->value().getValue();
        Gui::cmdAppObjectArgs(d->offset, "Value = %f", offsetValue);
        d->ui.spinOffset->apply();
        Gui::cmdAppObjectArgs(d->offset, "Mode = %d", d->ui.modeType->currentIndex());
        Gui::cmdAppObjectArgs(d->offset, "Join = %d", d->ui.joinType->currentIndex());
        Gui::cmdAppObjectArgs(
            d->offset,
            "Intersection = %s",
            d->ui.intersection->isChecked() ? "True" : "False"
        );
        Gui::cmdAppObjectArgs(
            d->offset,
            "SelfIntersection = %s",
            d->ui.selfIntersection->isChecked() ? "True" : "False"
        );
        Gui::cmdAppObjectArgs(d->offset, "Fill = %s", d->ui.fillOffset->isChecked() ? "True" : "False");

        Gui::cmdAppDocument(d->offset, "recompute()");
        updateResultStatus();
        if (!d->offset->isValid()) {
            throw Base::CADKernelError(d->offset->getStatusString());
        }

        auto* doc = d->offset->getDocument();
        Gui::cmdGuiDocument(d->offset, "resetEdit()");
        doc->commitTransaction();  // ViewProviderDocumentObject::startDefaultEditMode()
    }
    catch (const Base::Exception& e) {
        // Retain the edit transaction: aborting here can delete a newly created
        // offset while the task panel still holds its pointer. Cancel owns rollback.
        if (d->offset->isDerivedFrom<Part::Offset2D>()) {
            QMessageBox::warning(this, tr("Input error"),
                                 QCoreApplication::translate("Exception", e.what()));
        }
        else {
            d->ui.resultStatus->setText(tr("Cannot accept offset. Adjust settings or cancel.\n%1")
                .arg(QCoreApplication::translate("Exception", e.what())));
        }
        return false;
    }

    return true;
}

bool OffsetWidget::reject()
{
    auto* doc = d->offset->getDocument();
    // resetEdit commits a pending transaction, so rollback must happen first.
    // Aborting can delete both the feature and this task: keep only its document.
    doc->abortTransaction();  // ViewProviderDocumentObject::startDefaultEditMode()
    Gui::Command::doCommand(Gui::Command::Gui, "Gui.getDocument('%s').resetEdit()", doc->getName());
    Gui::Command::updateActive();
    return true;
}

void OffsetWidget::changeEvent(QEvent* e)
{
    QWidget::changeEvent(e);
    if (e->type() == QEvent::LanguageChange) {
        d->ui.retranslateUi(this);
        if (!d->offset->isDerivedFrom<Part::Offset2D>()) {
            d->ui.fillOffset->setText(tr("Fill between source and offset"));
            d->ui.labelOffset->setText(tr("Signed distance"));
        }
        updateResultStatus();
    }
}


/* TRANSLATOR PartGui::TaskOffset */

TaskOffset::TaskOffset(Part::Offset* offset)
{
    widget = new OffsetWidget(offset);
    addTaskBox(Gui::BitmapFactory().pixmap("Part_Offset"), widget);
}

TaskOffset::~TaskOffset() = default;

Part::Offset* TaskOffset::getObject() const
{
    return widget->getObject();
}

void TaskOffset::open()
{}

void TaskOffset::clicked(int)
{}

bool TaskOffset::accept()
{
    return widget->accept();
}

bool TaskOffset::reject()
{
    return widget->reject();
}

#include "moc_TaskOffset.cpp"
