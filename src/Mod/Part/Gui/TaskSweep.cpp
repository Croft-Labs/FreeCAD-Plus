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


#include <BRepBuilderAPI_MakeWire.hxx>
#include <Mod/Part/App/ShapeAnalysis_FreeBoundsFix.h>
#include <Precision.hxx>
#include <QApplication>
#include <QMessageBox>
#include <QLabel>
#include <QStringList>
#include <QTextStream>
#include <QTimer>
#include <QTreeWidget>
#include <ShapeAnalysis_FreeBounds.hxx>
#include <TopExp_Explorer.hxx>
#include <TopoDS.hxx>
#include <TopoDS_Iterator.hxx>
#include <TopTools_HSequenceOfShape.hxx>


#include <App/Application.h>
#include <App/Document.h>
#include <App/DocumentObject.h>
#include <App/Link.h>
#include <Base/Tools.h>
#include <Gui/Application.h>
#include <Gui/BitmapFactory.h>
#include <Gui/Command.h>
#include <Gui/Document.h>
#include <Gui/Selection/Selection.h>
#include <Gui/Selection/SelectionFilter.h>
#include <Gui/Selection/SelectionObject.h>
#include <Gui/ViewProvider.h>
#include <Gui/WaitCursor.h>
#include <Mod/Part/App/PartFeature.h>
#include <Mod/Part/App/PartFeatures.h>

#include "TaskSweep.h"
#include "ui_TaskSweep.h"


using namespace PartGui;

class SweepWidget::Private
{
public:
    Ui_TaskSweep ui;
    QString buttonText;
    std::string document;
    std::vector<Gui::SelectionObject> pathSelection;
    unsigned long long pathId {0};
    QLabel* review {nullptr};
    Private() = default;
    ~Private() = default;

    class EdgeSelection: public Gui::SelectionFilterGate
    {
    public:
        EdgeSelection()
            : Gui::SelectionFilterGate(nullPointer())
        {}
        bool allow(App::Document* /*pDoc*/, App::DocumentObject* pObj, const char* sSubName) override
        {
            if (Base::Tools::isNullOrEmpty(sSubName)) {
                // If selecting again the same edge the passed sub-element is empty. If the whole
                // shape is an edge or wire we can use it completely.
                Part::TopoShape topoShape = Part::Feature::getTopoShape(
                    pObj,
                    Part::ShapeOption::ResolveLink | Part::ShapeOption::Transform
                );
                if (topoShape.isNull()) {
                    return false;
                }
                const TopoDS_Shape shape = topoShape.getShape();
                if (!shape.IsNull()) {
                    // a single edge
                    if (shape.ShapeType() == TopAbs_EDGE) {
                        return true;
                    }
                    // a single wire
                    if (shape.ShapeType() == TopAbs_WIRE) {
                        return true;
                    }
                    // a compound of only edges or wires
                    if (shape.ShapeType() == TopAbs_COMPOUND) {
                        TopoDS_Iterator it(shape);
                        for (; it.More(); it.Next()) {
                            if (it.Value().IsNull()) {
                                return false;
                            }
                            if ((it.Value().ShapeType() != TopAbs_EDGE)
                                && (it.Value().ShapeType() != TopAbs_WIRE)) {
                                return false;
                            }
                        }

                        return true;
                    }
                }
            }
            else {
                std::string element(sSubName);
                return element.substr(0, 4) == "Edge";
            }

            return false;
        }
    };
};

/* TRANSLATOR PartGui::SweepWidget */

SweepWidget::SweepWidget(QWidget* parent)
    : d(new Private())
{
    Q_UNUSED(parent);
    Gui::Command::runCommand(Gui::Command::App, "from FreeCAD import Base");
    Gui::Command::runCommand(Gui::Command::App, "import Part");

    d->ui.setupUi(this);
    d->ui.selector->setAvailableLabel(tr("Available profiles"));
    d->ui.selector->setSelectedLabel(tr("Sections in sweep order"));
    d->ui.labelPath->setTextFormat(Qt::PlainText);
    d->ui.labelPath->setWordWrap(true);
    d->review = new QLabel(this);
    d->review->setObjectName(QStringLiteral("sweepInputReview"));
    d->review->setWordWrap(true);
    d->review->setTextFormat(Qt::PlainText);
    d->ui.gridLayout->addWidget(d->review, 4, 0, 1, 3);
    auto* model = d->ui.selector->selectedTreeWidget()->model();
    connect(model, &QAbstractItemModel::rowsInserted, this, &SweepWidget::updateReview);
    connect(model, &QAbstractItemModel::rowsRemoved, this, &SweepWidget::updateReview);
    connect(model, &QAbstractItemModel::rowsMoved, this, &SweepWidget::updateReview);
    connect(d->ui.checkSolid, &QCheckBox::toggled, this, &SweepWidget::updateReview);
    connect(d->ui.checkFrenet, &QCheckBox::toggled, this, &SweepWidget::updateReview);
    d->ui.labelPath->clear();

    // clang-format off
    connect(d->ui.buttonPath, &QPushButton::toggled,
            this, &SweepWidget::onButtonPathToggled);
    connect(d->ui.selector->availableTreeWidget(), &QTreeWidget::currentItemChanged,
            this, &SweepWidget::onCurrentItemChanged);
    connect(d->ui.selector->selectedTreeWidget(), &QTreeWidget::currentItemChanged,
            this, &SweepWidget::onCurrentItemChanged);
    // clang-format on

    findShapes();
    updateReview();
}

SweepWidget::~SweepWidget()
{
    delete d;
    Gui::Selection().rmvSelectionGate();
}

void SweepWidget::findShapes()
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

        // also allow compounds with a single face, wire or vertex or
        // if there are only edges building one wire
        if (shape.ShapeType() == TopAbs_COMPOUND) {
            Handle(TopTools_HSequenceOfShape) hEdges = new TopTools_HSequenceOfShape();
            Handle(TopTools_HSequenceOfShape) hWires = new TopTools_HSequenceOfShape();

            TopoDS_Iterator it(shape);
            int numChilds = 0;
            TopoDS_Shape child;
            for (; it.More(); it.Next(), numChilds++) {
                if (!it.Value().IsNull()) {
                    child = it.Value();
                    if (child.ShapeType() == TopAbs_EDGE) {
                        hEdges->Append(child);
                    }
                }
            }

            // a single child
            if (numChilds == 1) {
                shape = child;
            }
            // or all children are edges
            else if (hEdges->Length() == numChilds) {
                Part::Fix_ShapeAnalysis_FreeBounds_ConnectEdgesToWires(
                    hEdges,
                    Precision::Confusion(),
                    Standard_False,
                    hWires
                );
                if (hWires->Length() == 1) {
                    shape = hWires->Value(1);
                }
            }
        }

        if (!shape.Infinite()
            && (shape.ShapeType() == TopAbs_FACE || shape.ShapeType() == TopAbs_WIRE
                || shape.ShapeType() == TopAbs_EDGE || shape.ShapeType() == TopAbs_VERTEX)) {
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
    }
}

bool SweepWidget::isPathValid(const Gui::SelectionObject& sel) const
{
    const App::DocumentObject* path = sel.getObject();
    if (!path) {
        return false;
    }
    const std::vector<std::string>& sub = sel.getSubNames();

    TopoDS_Shape pathShape;
    Part::TopoShape shape = Part::Feature::getTopoShape(
        path,
        Part::ShapeOption::ResolveLink | Part::ShapeOption::Transform
    );
    if (shape.isNull()) {
        return false;
    }
    try {
        // Wire validation must not change flags on the selected source topology.
        shape = shape.makeElementCopy();
    }
    catch (...) {
        return false;
    }
    if (!sub.empty()) {
        try {
            BRepBuilderAPI_MakeWire mkWire;
            for (const auto& it : sub) {
                TopoDS_Shape subshape = shape.getSubShape(it.c_str());
                mkWire.Add(TopoDS::Edge(subshape));
            }
            pathShape = mkWire.Wire();
        }
        catch (...) {
            return false;
        }
    }
    else if (shape.getShape().ShapeType() == TopAbs_EDGE) {
        pathShape = shape.getShape();
    }
    else if (shape.getShape().ShapeType() == TopAbs_WIRE) {
        BRepBuilderAPI_MakeWire mkWire(TopoDS::Wire(shape.getShape()));
        pathShape = mkWire.Wire();
    }
    else if (shape.getShape().ShapeType() == TopAbs_COMPOUND) {
        try {
            TopoDS_Iterator it(shape.getShape());
            for (; it.More(); it.Next()) {
                if ((it.Value().ShapeType() != TopAbs_EDGE)
                    && (it.Value().ShapeType() != TopAbs_WIRE)) {
                    return false;
                }
            }
            Handle(TopTools_HSequenceOfShape) hEdges = new TopTools_HSequenceOfShape();
            Handle(TopTools_HSequenceOfShape) hWires = new TopTools_HSequenceOfShape();
            for (TopExp_Explorer xp(shape.getShape(), TopAbs_EDGE); xp.More(); xp.Next()) {
                hEdges->Append(xp.Current());
            }

            Part::Fix_ShapeAnalysis_FreeBounds_ConnectEdgesToWires(
                hEdges,
                Precision::Confusion(),
                Standard_True,
                hWires
            );
            int len = hWires->Length();
            if (len != 1) {
                return false;
            }
            pathShape = hWires->Value(1);
        }
        catch (...) {
            return false;
        }
    }

    return (!pathShape.IsNull());
}

void SweepWidget::updateReview()
{
    d->review->setText(tr("%1 sections, top to bottom. %2 %3 "
                         "Creates a separate associative Sweep. No twist preview or Boolean target is provided.")
        .arg(d->ui.selector->selectedTreeWidget()->topLevelItemCount())
        .arg(d->ui.checkSolid->isChecked() ? tr("Solid output requires closed profiles.")
                                         : tr("Surface output is requested."))
        .arg(d->ui.checkFrenet->isChecked() ? tr("Native Frenet frame enabled.")
                                          : tr("Native corrected frame enabled.")));
    if (!d->ui.buttonPath->isChecked()) {
        if (d->pathSelection.empty()) {
            d->ui.labelPath->setText(tr("No path captured. Choose Sweep Path, select connected edges, then Done."));
        }
        else {
            const auto& path = d->pathSelection.front();
            QStringList edges;
            for (const auto& sub : path.getSubNames()) {
                edges << QString::fromStdString(sub);
            }
            d->ui.labelPath->setText(tr("Captured path: %1 [%2] - %3. Profile selection does not change it.")
                .arg(QString::fromUtf8(path.getDocName()), QString::fromUtf8(path.getFeatName()),
                     edges.isEmpty() ? tr("whole edge/wire") : edges.join(QStringLiteral(", "))));
        }
    }
}

bool SweepWidget::accept()
{
    if (d->ui.buttonPath->isChecked()) {
        d->review->setText(tr("Finish path selection with Done before creating the sweep."));
        return false;
    }
    auto* appDoc = App::GetApplication().getDocument(d->document.c_str());
    if (!appDoc || App::GetApplication().getActiveDocument() != appDoc
        || appDoc->hasPendingTransaction() || appDoc->getBookedTransactionID() > 0) {
        d->review->setText(tr("Activate the section document and finish other edit transactions first."));
        return false;
    }
    if (d->pathSelection.empty()) {
        d->review->setText(tr("Capture a path with Sweep Path and Done before creating the sweep."));
        return false;
    }
    const auto& path = d->pathSelection.front();
    const auto* docobj = path.getObject();
    if (!docobj || docobj->getDocument() != appDoc || docobj->getID() != d->pathId
        || !docobj->isValid() || docobj->isTouched() || !isPathValid(path)) {
        d->review->setText(tr("The captured path is missing, replaced, stale or invalid. Recompute and capture it again."));
        return false;
    }
    const auto selection = path.getAsPropertyLinkSubString();
    const std::string spineObject = path.getFeatName();

    QString list, solid, frenet;
    if (d->ui.checkSolid->isChecked()) {
        solid = QStringLiteral("True");
    }
    else {
        solid = QStringLiteral("False");
    }

    if (d->ui.checkFrenet->isChecked()) {
        frenet = QStringLiteral("True");
    }
    else {
        frenet = QStringLiteral("False");
    }

    QTextStream str(&list);

    int count = d->ui.selector->selectedTreeWidget()->topLevelItemCount();
    if (count < 1) {
        d->review->setText(tr("Choose at least one section in sweep order."));
        return false;
    }
    for (int i = 0; i < count; i++) {
        QTreeWidgetItem* child = d->ui.selector->selectedTreeWidget()->topLevelItem(i);
        QString name = child->data(0, Qt::UserRole).toString();
        auto* section = appDoc->getObject(name.toUtf8().constData());
        if (!section || section->getID() != child->data(0, Qt::UserRole + 1).toULongLong()
            || !section->isValid() || section->isTouched()) {
            d->review->setText(tr("A section is missing, replaced or not current. Recompute or reopen the task."));
            return false;
        }
        if (name == QLatin1String(spineObject.c_str())) {
            d->review->setText(tr("A section cannot also be the sweep path."));
            return false;
        }
        str << "App.getDocument('" << d->document.c_str() << "')." << name << ", ";
    }

    int transaction = 0;
    try {
        Gui::WaitCursor wc;
        QString cmd;
        cmd = QStringLiteral(
                  "App.getDocument('%5').addObject('Part::Sweep','Sweep')\n"
                  "App.getDocument('%5').ActiveObject.Sections=[%1]\n"
                  "App.getDocument('%5').ActiveObject.Spine=%2\n"
                  "App.getDocument('%5').ActiveObject.Solid=%3\n"
                  "App.getDocument('%5').ActiveObject.Frenet=%4\n"
        )
                  .arg(list, selection.c_str(), solid, frenet, d->document.c_str());

        Gui::Document* doc = Gui::Application::Instance->getDocument(d->document.c_str());
        if (!doc) {
            throw Base::RuntimeError("Document doesn't exist anymore");
        }
        transaction = Gui::Command::openActiveDocumentCommand(tr("Sweep").toStdString());
        Gui::Command::runCommand(Gui::Command::App, cmd.toUtf8());
        doc->getDocument()->recompute();
        auto* sweep = dynamic_cast<Part::Sweep*>(doc->getDocument()->getActiveObject());
        if (!sweep) {
            throw Base::RuntimeError("Sweep creation failed");
        }
        if (!sweep->isValid()) {
            throw Base::RuntimeError(sweep->getStatusString());
        }
        if (sweep->Shape.getShape().isNull() || !sweep->Shape.getShape().isValid()) {
            throw Base::RuntimeError("Sweep did not produce a valid shape");
        }
        if (d->ui.checkSolid->isChecked()
            && sweep->Shape.getShape().countSubShapes(TopAbs_SOLID) != 1) {
            throw Base::RuntimeError("The sections and path did not produce one solid");
        }
        Gui::Command::commitCommand(transaction);
    }
    catch (const Base::Exception& e) {
        Gui::Command::abortCommand(transaction);
        d->review->setText(tr("Sweep was not created. Original inputs were preserved. "
                             "Check the sections, path and output mode, then try again.\n%1")
                          .arg(QCoreApplication::translate("Exception", e.what())));
        return false;
    }

    return true;
}

bool SweepWidget::reject()
{
    Gui::Selection().rmvSelectionGate();
    return true;
}

void SweepWidget::onCurrentItemChanged(QTreeWidgetItem* current, QTreeWidgetItem* previous)
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

void SweepWidget::onButtonPathToggled(bool on)
{
    if (on) {
        d->pathSelection.clear();
        d->pathId = 0;
        QList<QWidget*> c = this->findChildren<QWidget*>();
        for (auto it : c) {
            it->setEnabled(false);
        }
        d->buttonText = d->ui.buttonPath->text();
        d->ui.buttonPath->setText(tr("Done"));
        d->ui.buttonPath->setEnabled(true);
        d->ui.labelPath->setText(
            tr("Select one or more connected edges in the 3D view and press 'Done'")
        );
        d->ui.labelPath->setEnabled(true);

        Gui::Selection().clearSelection();
        Gui::Selection().addSelectionGate(new Private::EdgeSelection());
    }
    else {
        QList<QWidget*> c = this->findChildren<QWidget*>();
        for (auto it : c) {
            it->setEnabled(true);
        }
        d->ui.buttonPath->setText(d->buttonText);
        d->ui.labelPath->clear();
        Gui::Selection().rmvSelectionGate();

        const auto selected = Gui::Selection().getSelectionEx();
        if (selected.size() == 1 && selected.front().getDocName() == d->document
            && isPathValid(selected.front())) {
            d->pathSelection = selected;
            d->pathId = selected.front().getObject()->getID();
            updateReview();
        }
        else {
            d->pathSelection.clear();
            updateReview();
            d->review->setText(tr("No path captured: select connected edges from one object in this document."));
        }
    }
}

void SweepWidget::changeEvent(QEvent* e)
{
    QWidget::changeEvent(e);
    if (e->type() == QEvent::LanguageChange) {
        d->ui.retranslateUi(this);
        d->ui.selector->setAvailableLabel(tr("Available profiles"));
        d->ui.selector->setSelectedLabel(tr("Sections in sweep order"));
        updateReview();
    }
}


/* TRANSLATOR PartGui::TaskSweep */

TaskSweep::TaskSweep()
    : label(nullptr)
{
    setAutoCloseOnDeletedDocument(true);
    widget = new SweepWidget();
    addTaskBox(Gui::BitmapFactory().pixmap("Part_Sweep"), widget);
}

TaskSweep::~TaskSweep()
{
    delete label;
}

void TaskSweep::open()
{}

void TaskSweep::clicked(int id)
{
    if (id == QDialogButtonBox::Help) {
        QString help = QApplication::translate(
            "PartGui::TaskSweep",
            "Select at least 1 profile and an edge or wire\n"
            "in the 3D view for the sweep path."
        );
        if (!label) {
            label = new Gui::StatusWidget(widget);
            label->setStatusText(help);
        }

        label->show();
        QTimer::singleShot(3000, label, &Gui::StatusWidget::hide);
    }
}

bool TaskSweep::accept()
{
    return widget->accept();
}

bool TaskSweep::reject()
{
    return widget->reject();
}

#include "moc_TaskSweep.cpp"
