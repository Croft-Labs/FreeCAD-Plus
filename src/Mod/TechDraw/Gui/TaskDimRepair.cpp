// SPDX-License-Identifier: LGPL-2.1-or-later

/***************************************************************************
 *   Copyright (c) 2022 WandererFan <wandererfan@gmail.com>                *
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

#include <cmath>
#include <stdexcept>
#include <string>
#include <vector>

#include <QLabel>
#include <QMessageBox>
#include <QTableWidgetItem>

#include <Base/Exception.h>
#include <App/Application.h>
#include <App/Document.h>
#include <Gui/BitmapFactory.h>
#include <Gui/Command.h>
#include <Gui/MainWindow.h>
#include <Gui/Selection/Selection.h>
#include <Mod/TechDraw/App/DrawView.h>
#include <Mod/TechDraw/App/DrawViewPart.h>

#include "DimensionValidators.h"
#include "TaskDimRepair.h"
#include "ui_TaskDimRepair.h"


using namespace Gui;
using namespace TechDraw;
using namespace TechDrawGui;

TaskDimRepair::TaskDimRepair(TechDraw::DrawViewDimension* inDvd)
    : ui(new Ui_TaskDimRepair),
      m_dim(inDvd)
{
    ui->setupUi(this);
    ui->twReferences3d->setEditTriggers(QAbstractItemView::NoEditTriggers);
    m_status = new QLabel(this);
    m_status->setObjectName(QStringLiteral("dimensionRepairStatus"));
    m_status->setWordWrap(true);
    m_status->setTextFormat(Qt::PlainText);
    m_status->setText(tr("Select replacement geometry and use the selection to review it. "
                         "OK validates before committing. Drawing dimensions measure geometry; "
                         "this repair does not drive the source model."));
    ui->verticalLayout->addWidget(m_status);

    connect(ui->pbSelection, &QPushButton::clicked, this, &TaskDimRepair::slotUseSelection);

    saveDimState();
    setUiPrimary();
}

TaskDimRepair::~TaskDimRepair()
{}

void TaskDimRepair::setUiPrimary()
{
    setWindowTitle(QObject::tr("Dimension Repair"));
    ui->leName->setReadOnly(true);
    ui->leLabel->setReadOnly(true);

    ui->leName->setText(QString::fromStdString(m_dim->getNameInDocument()));
    ui->leLabel->setText(QString::fromStdString(m_dim->Label.getValue()));

    DrawViewPart* viewPart = m_dim->getViewPart();
    std::string objName = viewPart ?  viewPart->getNameInDocument() : "";
    std::string objLabel = viewPart ?  viewPart->Label.getValue() : "";
    ui->leObject2d->setText(QString::fromStdString(objName + " / " + objLabel));
    const std::vector<std::string>& subElements2d = m_dim->References2D.getSubValues();
    std::vector<std::string> labelsInOut(subElements2d.size());
    fillList(ui->lwGeometry2d, labelsInOut, subElements2d);

    QStringList headers;
    headers << tr("Object") << tr("Label") << tr("Sub-Element");
    ui->twReferences3d->setHorizontalHeaderLabels(headers);

    ReferenceVector references3d = m_dim->getReferences3d();
    loadTableWidget(ui->twReferences3d, references3d);
}

void TaskDimRepair::saveDimState()
{
    m_saveMeasureType = m_dim->MeasureType.getValue();
    m_saveDimType = m_dim->Type.getValue();
    m_saveRefs3d = m_dim->getReferences3d();
    m_saveRefs2d = m_dim->getReferences2d();
    m_saveDvp = m_dim->getViewPart();
}

//restore the start conditions
void TaskDimRepair::restoreDimState()
{
    if (m_dim) {
        m_dim->setReferences2d(m_saveRefs2d);
        m_dim->setReferences3d(m_saveRefs3d);
    }
}

//similar to code in CommandCreateDims.cpp
//use the current selection to replace the references in dim
void TaskDimRepair::slotUseSelection()
{
    m_toApply2d.clear();
    m_toApply3d.clear();
    m_status->setText(tr("No reviewed replacement. Select compatible geometry and use the selection again."));
    const std::vector<App::DocumentObject*> dimObjects =
        Gui::Selection().getObjectsOfType(TechDraw::DrawViewDimension::getClassTypeId());
    if (dimObjects.empty()) {
        //selection does not include a dimension, so we need to add our dimension to keep the
        //validators happy
        //bool accepted =
        static_cast<void>(Gui::Selection().addSelection(m_dim->getDocument()->getName(),
                                                        m_dim->getNameInDocument()));
    }
    ReferenceVector references2d;
    ReferenceVector references3d;
    TechDraw::DrawViewPart* dvp = TechDraw::getReferencesFromSelection(references2d, references3d);
     if (dvp != m_saveDvp) {
        int ret = QMessageBox::warning(Gui::getMainWindow(),
                                       QObject::tr("Incorrect Selection?"),
                                       QObject::tr("This will change the dimension's owner view. Continue?"),
                                       QMessageBox::Cancel | QMessageBox::Ok);
        if (ret == QMessageBox::Cancel) {
            return;
        }
    }

    StringVector acceptableGeometry({ "Edge", "Vertex", "Face" });
    std::vector<int> minimumCounts({1, 1, 1});
    std::vector<DimensionGeometry> acceptableDimensionGeometrys;//accept anything
    DimensionGeometry geometryRefs2d = validateDimSelection(
        references2d, acceptableGeometry, minimumCounts, acceptableDimensionGeometrys);
    if (geometryRefs2d == DimensionGeometry::isInvalid) {
        QMessageBox::warning(Gui::getMainWindow(),
                             QObject::tr("Incorrect Selection"),
                             QObject::tr("Cannot make dimension from selection"));
        return;
    }
    //what 3d geometry configuration did we receive?
    DimensionGeometry geometryRefs3d(DimensionGeometry::isInvalid);
    if (geometryRefs2d == DimensionGeometry::isViewReference && !references3d.empty()) {
        geometryRefs3d = validateDimSelection3d(
            dvp, references3d, acceptableGeometry, minimumCounts, acceptableDimensionGeometrys);
        if (geometryRefs3d == DimensionGeometry::isInvalid) {
            QMessageBox::warning(Gui::getMainWindow(),
                                 QObject::tr("Incorrect Selection"),
                                 QObject::tr("Cannot make dimension from selection"));
            return;
        }
    }

    m_toApply2d = references2d;
    if (references3d.empty()) {
        m_toApply3d.clear();
    } else {
        m_toApply3d = references3d;
    }
    updateUi();
    m_status->setText(m_toApply3d.empty()
        ? tr("Reviewed replacement: projected 2D geometry. Previous 3D references will be cleared. "
             "OK recomputes before committing; source geometry is unchanged.")
        : tr("Reviewed replacement: true 3D model geometry. The drawing remains linked to the selected "
             "source references. OK recomputes before committing; this does not drive the model."));
}

void TaskDimRepair::updateUi()
{
    // if the dimension is very broken, it may not have a valid 2d view reference.  This can happen if the
    // restore process breaks and the reference target object does not get properly loaded.

    DrawViewPart* viewPart = m_toApply2d.empty() ? m_dim->getViewPart()
        : Base::freecad_cast<DrawViewPart*>(m_toApply2d.front().getObject());

    std::string objName = viewPart ?  viewPart->getNameInDocument() : "";
    std::string objLabel = viewPart ?  viewPart->Label.getValue() : "";
    ui->leObject2d->setText(QString::fromStdString(objName + " / " + objLabel));

    std::vector<std::string> subElements2d;
    for (auto& ref : m_toApply2d) {
        subElements2d.push_back(ref.getSubName());
    }
    std::vector<std::string> labelsInOut(subElements2d.size());
    fillList(ui->lwGeometry2d, labelsInOut, subElements2d);

    loadTableWidget(ui->twReferences3d, m_toApply3d);
}

void TaskDimRepair::loadTableWidget(QTableWidget* tw, ReferenceVector refs)
{
    tw->clearContents();
    tw->setRowCount(refs.size() + 1);
    size_t iRow = 0;
    for (auto& ref : refs) {
        QString qName = QString::fromStdString(ref.getObject()->getNameInDocument());
        QTableWidgetItem* itemName = new QTableWidgetItem(qName);
        itemName->setTextAlignment(Qt::AlignRight | Qt::AlignVCenter);
        tw->setItem(iRow, 0, itemName);
        QString qLabel = QString::fromStdString(std::string(ref.getObject()->Label.getValue()));
        QTableWidgetItem* itemLabel = new QTableWidgetItem(qLabel);
        itemLabel->setTextAlignment(Qt::AlignRight | Qt::AlignVCenter);
        tw->setItem(iRow, 1, itemLabel);
        QString qSubName = QString::fromStdString(ref.getSubName());
        QTableWidgetItem* itemSubName = new QTableWidgetItem(qSubName);
        itemSubName->setTextAlignment(Qt::AlignRight | Qt::AlignVCenter);
        tw->setItem(iRow, 2, itemSubName);
        iRow++;
    }
}

void TaskDimRepair::fillList(QListWidget* lwItems, std::vector<std::string> labels,
                             std::vector<std::string> names)
{
    QListWidgetItem* item;
    QString qLabel;
    QString qName;
    QString qText;
    int labelCount = labels.size();
    int i = 0;
    lwItems->clear();
    for (; i < labelCount; i++) {
        qLabel = QString::fromStdString(labels[i]);
        qName = QString::fromStdString(names[i]);
        qText = QStringLiteral("%1 %2").arg(qName, qLabel);
        item = new QListWidgetItem(qText, lwItems);
        item->setTextAlignment(Qt::AlignRight | Qt::AlignVCenter);
        item->setData(Qt::UserRole, qName);
    }
}
void TaskDimRepair::replaceReferences()
{
    if (!m_dim || m_toApply2d.empty()) {
        return;
    }

    m_dim->setReferences2d(m_toApply2d);

    // An empty 3D set is an explicit switch back to projected references.
    m_dim->setReferences3d(m_toApply3d);
    if (m_toApply3d.empty()) {
        m_dim->clear3DMeasurements();
        m_dim->MeasureType.setValue("Projected");
    }
    else {
        m_dim->MeasureType.setValue("True");
        m_dim->setAll3DMeasurement();
    }
}

bool TaskDimRepair::accept()
{
    if (m_toApply2d.empty()) {
        m_status->setText(tr("Choose replacement geometry with Use Selection before accepting."));
        return false;
    }
    auto* doc = m_dim->getDocument();
    if (App::GetApplication().getActiveDocument() != doc || doc->hasPendingTransaction()
        || doc->getBookedTransactionID() > 0) {
        m_status->setText(tr("Activate the dimension document and finish the other edit transaction first."));
        return false;
    }
    int tid = Gui::Command::openActiveDocumentCommand(tr("Repair dimension").toStdString().c_str());
    try {
        replaceReferences();
        for (const auto& ref : m_dim->getEffectiveReferences()) {
            auto* object = ref.getObject();
            if (!object || !object->isValid() || object->isTouched()
                || (!ref.getSubName().empty() && !ref.hasGeometry())) {
                throw std::runtime_error("A replacement reference is missing or not current.");
            }
        }
        if (!m_dim->validateReferenceForm()
            || !m_dim->getViewPart() || !m_dim->getViewPart()->hasGeometry()
            || (m_toApply3d.empty() && !m_dim->checkReferences2D())
            || !m_dim->recomputeFeature() || !std::isfinite(m_dim->getDimValue())) {
            throw std::runtime_error("The dimension cannot evaluate these references.");
        }
        Gui::Command::commitCommand(tid);
    }
    catch (const Base::Exception& error) {
        Gui::Command::abortCommand(tid);
        m_dim->recomputeFeature();
        m_status->setText(tr("Repair was not applied. Original references were restored. "
                             "Choose compatible geometry and try again.\n%1")
                             .arg(QString::fromUtf8(error.what())));
        return false;
    }
    catch (const std::exception& error) {
        Gui::Command::abortCommand(tid);
        m_dim->recomputeFeature();
        m_status->setText(tr("Repair was not applied. Original references were restored. "
                             "Choose compatible geometry and try again.\n%1")
                             .arg(QString::fromUtf8(error.what())));
        return false;
    }
    Gui::Selection().clearSelection();
    return true;
}

bool TaskDimRepair::reject()
{
    // Collection is read-only; failed acceptance already aborts its own transaction.
    Gui::Selection().clearSelection();
    return true;
}

void TaskDimRepair::changeEvent(QEvent* e)
{
    if (e->type() == QEvent::LanguageChange) {
        ui->retranslateUi(this);
    }
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
TaskDlgDimReference::TaskDlgDimReference(TechDraw::DrawViewDimension* inDvd)
    : TaskDialog()
{
    widget = new TaskDimRepair(inDvd);
    taskbox = new Gui::TaskView::TaskBox(
        Gui::BitmapFactory().pixmap("TechDraw_DimensionRepair"), widget->windowTitle(), true, 0);
    taskbox->groupLayout()->addWidget(widget);
    Content.push_back(taskbox);
}


TaskDlgDimReference::~TaskDlgDimReference()
{}

void TaskDlgDimReference::update()
{
    //widget->updateTask();
}

//==== calls from the TaskView ===============================================================
void TaskDlgDimReference::open()
{}

void TaskDlgDimReference::clicked(int i)
{
    Q_UNUSED(i);
}

bool TaskDlgDimReference::accept()
{
    return widget->accept();
}

bool TaskDlgDimReference::reject()
{
    widget->reject();
    return true;
}

#include <Mod/TechDraw/Gui/moc_TaskDimRepair.cpp>
