// SPDX-License-Identifier: LGPL-2.1-or-later

/***************************************************************************
 *   Copyright (c) 2011 Werner Mayer <wmayer[at]users.sourceforge.net>     *
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


#include <Mod/Part/App/ShapeAnalysis_FreeBoundsFix.h>
#include <Precision.hxx>
#include <QLabel>
#include <QMessageBox>
#include <QTextStream>
#include <QTreeWidget>
#include <ShapeAnalysis_FreeBounds.hxx>
#include <TopoDS.hxx>
#include <TopoDS_Iterator.hxx>
#include <TopTools_HSequenceOfShape.hxx>


#include <App/Application.h>
#include <App/Document.h>
#include <App/DocumentObject.h>
#include <Gui/Application.h>
#include <Gui/BitmapFactory.h>
#include <Gui/Command.h>
#include <Gui/Document.h>
#include <Gui/Selection/Selection.h>
#include <Gui/ViewProvider.h>

#include <Mod/Part/App/PartFeature.h>
#include <Mod/Part/App/PartFeatures.h>

#include <BRep_Tool.hxx>
#include <TopExp_Explorer.hxx>

#include "TaskLoft.h"
#include "ui_TaskLoft.h"


using namespace PartGui;

class LoftWidget::Private
{
public:
    Ui_TaskLoft ui;
    std::string document;
    QLabel* review {nullptr};
    Private() = default;
    ~Private() = default;
};

/* TRANSLATOR PartGui::LoftWidget */

LoftWidget::LoftWidget(QWidget* parent)
    : d(new Private())
{
    Q_UNUSED(parent);
    Gui::Command::runCommand(Gui::Command::App, "from FreeCAD import Base");
    Gui::Command::runCommand(Gui::Command::App, "import Part");

    d->ui.setupUi(this);
    d->ui.selector->setAvailableLabel(tr("Available profiles"));
    d->ui.selector->setSelectedLabel(tr("Sections in loft order"));
    d->ui.selector->selectedTreeWidget()->setToolTip(tr("Top to bottom is section order. Use Move up/down to change it."));
    d->ui.checkClosed->setToolTip(tr("Connect the last section back to the first; this does not cap an open section."));
    d->review = new QLabel(this);
    d->review->setObjectName(QStringLiteral("loftSectionReview"));
    d->review->setWordWrap(true);
    d->review->setTextFormat(Qt::PlainText);
    d->ui.gridLayout->addWidget(d->review, 2, 0, 1, 4);
    auto* model = d->ui.selector->selectedTreeWidget()->model();
    connect(model, &QAbstractItemModel::rowsInserted, this, &LoftWidget::updateReview);
    connect(model, &QAbstractItemModel::rowsRemoved, this, &LoftWidget::updateReview);
    connect(model, &QAbstractItemModel::rowsMoved, this, &LoftWidget::updateReview);
    connect(d->ui.checkSolid, &QCheckBox::toggled, this, &LoftWidget::updateReview);
    connect(d->ui.checkRuledSurface, &QCheckBox::toggled, this, &LoftWidget::updateReview);
    connect(d->ui.checkClosed, &QCheckBox::toggled, this, &LoftWidget::updateReview);

    // clang-format off
    connect(d->ui.selector->availableTreeWidget(), &QTreeWidget::currentItemChanged,
            this, &LoftWidget::onCurrentItemChanged);
    connect(d->ui.selector->selectedTreeWidget(), &QTreeWidget::currentItemChanged,
            this, &LoftWidget::onCurrentItemChanged);
    // clang-format on

    findShapes();
    updateReview();
}

LoftWidget::~LoftWidget()
{
    delete d;
}

void LoftWidget::findShapes()
{
    App::Document* activeDoc = App::GetApplication().getActiveDocument();
    Gui::Document* activeGui = Gui::Application::Instance->getDocument(activeDoc);
    if (!activeGui) {
        return;
    }
    d->document = activeDoc->getName();

    std::vector<App::DocumentObject*> objs = activeDoc->getObjectsOfType<App::DocumentObject>();

    for (auto obj : objs) {
        Part::TopoShape topoShape = Part::Feature::getTopoShape(
            obj,
            Part::ShapeOption::ResolveLink | Part::ShapeOption::Transform
        );
        if (topoShape.isNull()) {
            continue;
        }
        TopoDS_Shape shape = topoShape.getShape();
        if (shape.IsNull()) {
            continue;
        }

        const auto wires = topoShape.countSubShapes(TopAbs_WIRE);
        const auto edges = topoShape.countSubShapes(TopAbs_EDGE);
        const auto vertices = topoShape.countSubShapes(TopAbs_VERTEX);
        const bool viable = wires == 1 || (wires == 0 && edges == 1)
            || (edges == 0 && vertices == 1);

        if (viable) {
            QString label = QString::fromUtf8(obj->Label.getValue());
            QString name = QString::fromLatin1(obj->getNameInDocument());
            QTreeWidgetItem* child = new QTreeWidgetItem();
            child->setText(0, label);
            child->setToolTip(0, label + QStringLiteral(" [") + name + QStringLiteral("]"));
            child->setData(0, Qt::UserRole, name);
            child->setData(0, Qt::UserRole + 1, static_cast<qulonglong>(obj->getID()));
            Gui::ViewProvider* vp = activeGui->getViewProvider(obj);
            if (vp) {
                child->setIcon(0, vp->getIcon());
            }
            d->ui.selector->availableTreeWidget()->addTopLevelItem(child);
        }
    }  // end for objs
}

void LoftWidget::updateReview()
{
    const int count = d->ui.selector->selectedTreeWidget()->topLevelItemCount();
    d->review->setText(tr("%1 sections, top to bottom. %2 %3 %4 "
                         "Creates a separate associative Loft. Guides, explicit correspondence "
                         "and twist preview are not available in this task.")
        .arg(count)
        .arg(d->ui.checkSolid->isChecked() ? tr("Solid output requires closed profiles.")
                                         : tr("Surface output accepts open or closed profiles."))
        .arg(d->ui.checkRuledSurface->isChecked() ? tr("Ruled joins connect adjacent sections.")
                                                : tr("Smooth interpolation through sections."))
        .arg(d->ui.checkClosed->isChecked() ? tr("Last section connects back to first.")
                                          : tr("First and last sections remain separate.")));
}

bool LoftWidget::accept()
{
    QString list, solid, ruled, closed;
    if (d->ui.checkSolid->isChecked()) {
        solid = QStringLiteral("True");
    }
    else {
        solid = QStringLiteral("False");
    }

    if (d->ui.checkRuledSurface->isChecked()) {
        ruled = QStringLiteral("True");
    }
    else {
        ruled = QStringLiteral("False");
    }

    if (d->ui.checkClosed->isChecked()) {
        closed = QStringLiteral("True");
    }
    else {
        closed = QStringLiteral("False");
    }

    QTextStream str(&list);

    int count = d->ui.selector->selectedTreeWidget()->topLevelItemCount();
    if (count < 2) {
        d->review->setText(tr("Choose at least two sections in loft order."));
        return false;
    }
    auto* appDoc = App::GetApplication().getDocument(d->document.c_str());
    if (!appDoc || App::GetApplication().getActiveDocument() != appDoc
        || appDoc->hasPendingTransaction() || appDoc->getBookedTransactionID() > 0) {
        d->review->setText(tr("Activate the section document and finish other edit transactions first."));
        return false;
    }
    for (int i = 0; i < count; i++) {
        QTreeWidgetItem* child = d->ui.selector->selectedTreeWidget()->topLevelItem(i);
        QString name = child->data(0, Qt::UserRole).toString();
        auto* section = appDoc->getObject(name.toUtf8().constData());
        if (!section || section->getID() != child->data(0, Qt::UserRole + 1).toULongLong()
            || !section->isValid() || section->isTouched()) {
            d->review->setText(tr("A section is missing, replaced or not current. Recompute or reopen the task to select current sections."));
            return false;
        }
        str << "App.getDocument('" << d->document.c_str() << "')." << name << ", ";
    }

    int transaction = 0;
    try {
        QString cmd;
        cmd = QStringLiteral(
                  "App.getDocument('%5').addObject('Part::Loft','Loft')\n"
                  "App.getDocument('%5').ActiveObject.Sections=[%1]\n"
                  "App.getDocument('%5').ActiveObject.Solid=%2\n"
                  "App.getDocument('%5').ActiveObject.Ruled=%3\n"
                  "App.getDocument('%5').ActiveObject.Closed=%4\n"
        )
                  .arg(list, solid, ruled, closed, d->document.c_str());

        Gui::Document* doc = Gui::Application::Instance->getDocument(d->document.c_str());
        if (!doc) {
            throw Base::RuntimeError("Document doesn't exist anymore");
        }
        transaction = Gui::Command::openActiveDocumentCommand(tr("Loft").toStdString());
        Gui::Command::runCommand(Gui::Command::App, cmd.toUtf8());
        doc->getDocument()->recompute();
        auto* loft = dynamic_cast<Part::Loft*>(doc->getDocument()->getActiveObject());
        if (!loft) {
            throw Base::RuntimeError("Loft creation failed");
        }
        if (!loft->isValid()) {
            throw Base::RuntimeError(loft->getStatusString());
        }
        if (loft->Shape.getShape().isNull() || !loft->Shape.getShape().isValid()) {
            throw Base::RuntimeError("Loft did not produce a valid shape");
        }
        if (d->ui.checkSolid->isChecked()
            && loft->Shape.getShape().countSubShapes(TopAbs_SOLID) != 1) {
            throw Base::RuntimeError(
                "The sections did not produce one solid. Use closed profiles or turn off Create solid.");
        }
        Gui::Command::commitCommand(transaction);
    }
    catch (const Base::Exception& e) {
        Gui::Command::abortCommand(transaction);
        d->review->setText(tr("Loft was not created. Original sections were preserved. "
                             "Check section order and output mode, then try again.\n%1")
                          .arg(QCoreApplication::translate("Exception", e.what())));
        return false;
    }

    return true;
}

bool LoftWidget::reject()
{
    return true;
}

void LoftWidget::onCurrentItemChanged(QTreeWidgetItem* current, QTreeWidgetItem* previous)
{
    if (previous) {
        Gui::Selection().rmvSelection(
            d->document.c_str(),
            (const char*)previous->data(0, Qt::UserRole).toByteArray()
        );
    }
    if (current) {
        Gui::Selection().addSelection(
            d->document.c_str(),
            (const char*)current->data(0, Qt::UserRole).toByteArray()
        );
    }
}

void LoftWidget::changeEvent(QEvent* e)
{
    QWidget::changeEvent(e);
    if (e->type() == QEvent::LanguageChange) {
        d->ui.retranslateUi(this);
        d->ui.selector->setAvailableLabel(tr("Available profiles"));
        d->ui.selector->setSelectedLabel(tr("Sections in loft order"));
        updateReview();
    }
}


/* TRANSLATOR PartGui::TaskLoft */

TaskLoft::TaskLoft()
{
    setAutoCloseOnDeletedDocument(true);
    widget = new LoftWidget();
    addTaskBox(Gui::BitmapFactory().pixmap("Part_Loft"), widget);
}

TaskLoft::~TaskLoft() = default;

void TaskLoft::open()
{}

void TaskLoft::clicked(int)
{}

bool TaskLoft::accept()
{
    return widget->accept();
}

bool TaskLoft::reject()
{
    return widget->reject();
}

#include "moc_TaskLoft.cpp"
