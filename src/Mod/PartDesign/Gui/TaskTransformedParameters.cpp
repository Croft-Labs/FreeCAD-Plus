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


#include <QAction>
#include <QListWidget>
#include <QLabel>
#include <QPushButton>
#include <QSignalBlocker>
#include <QStringList>
#include <set>


#include <App/Application.h>
#include <App/Document.h>
#include <App/DocumentObject.h>
#include <App/Transactions.h>
#include <App/Origin.h>
#include <Base/Console.h>
#include <Base/Tools.h>
#include <Gui/Application.h>
#include <Gui/Document.h>
#include <Gui/BitmapFactory.h>
#include <Gui/ViewProvider.h>
#include <Gui/Selection/Selection.h>
#include <Gui/Command.h>
#include <Gui/Tools.h>
#include <Mod/PartDesign/App/Body.h>
#include <Mod/PartDesign/App/FeatureAddSub.h>
#include <Mod/PartDesign/App/FeatureTransformed.h>
#include <Mod/PartDesign/App/FeaturePattern.h>

#include "ui_TaskTransformedParameters.h"
#include "TaskTransformedParameters.h"
#include "TaskMultiTransformParameters.h"
#include "ReferenceSelection.h"


FC_LOG_LEVEL_INIT("PartDesign", true, true)

using namespace PartDesignGui;
using namespace Gui;

/* TRANSLATOR PartDesignGui::TaskTransformedParameters */

TaskTransformedParameters::TaskTransformedParameters(
    ViewProviderTransformed* TransformedView,
    QWidget* parent
)
    : TaskBox(
          Gui::BitmapFactory().pixmap(TransformedView->featureIcon().c_str()),
          TransformedView->menuName,
          true,
          parent
      )
    , TransformedView(TransformedView)
    , ui(new Ui_TaskTransformedParameters)
{
    Gui::Document* doc = TransformedView->getDocument();
    this->attachDocument(doc);
}

TaskTransformedParameters::TaskTransformedParameters(TaskMultiTransformParameters* parentTask)
    : TaskBox(QPixmap(), tr(""), true, parentTask)
    , parentTask(parentTask)
    , insideMultiTransform(true)
{}

TaskTransformedParameters::~TaskTransformedParameters()
{
    restoreOriginalsVisibility();
    // make sure to remove selection gate in all cases
    Gui::Selection().rmvSelectionGate();

    delete proxy;
}

void TaskTransformedParameters::setupUI()
{
    // we need a separate container widget to add all controls to
    proxy = new QWidget(this);
    ui->setupUi(proxy);
    QMetaObject::connectSlotsByName(this);

    connect(
        ui->buttonAddFeature,
        &QToolButton::toggled,
        this,
        &TaskTransformedParameters::onButtonAddFeature
    );
    connect(
        ui->buttonRemoveFeature,
        &QToolButton::toggled,
        this,
        &TaskTransformedParameters::onButtonRemoveFeature
    );

    // Create context menu
    auto action = new QAction(tr("Remove"), this);
    action->setShortcut(Gui::QtTools::deleteKeySequence());

    // display shortcut behind the context menu entry
    action->setShortcutVisibleInContextMenu(true);
    ui->listWidgetFeatures->addAction(action);
    connect(action, &QAction::triggered, this, &TaskTransformedParameters::onFeatureDeleted);
    ui->listWidgetFeatures->setContextMenuPolicy(Qt::ActionsContextMenu);

    connect(ui->checkBoxUpdateView, &QCheckBox::toggled, this, &TaskTransformedParameters::onUpdateView);

    // Get the feature data
    auto pcTransformed = getObject<PartDesign::Transformed>();

    using Mode = PartDesign::Transformed::Mode;
    if (getObject<PartDesign::Pattern>()) {
        ui->radioTransformToolShapes->setText(tr("Selected features"));
        ui->radioTransformBody->setText(tr("Whole body"));
        ui->verticalLayout_3->insertWidget(0, ui->radioTransformToolShapes);
        originalsStatus = new QLabel(proxy);
        originalsStatus->setObjectName(QStringLiteral("patternOriginalsStatus"));
        originalsStatus->setTextFormat(Qt::PlainText);
        originalsStatus->setWordWrap(true);
        ui->verticalLayout->insertWidget(1, originalsStatus);
        originalsHint = new QLabel(proxy);
        originalsHint->setObjectName(QStringLiteral("patternOriginalsHint"));
        originalsHint->setTextFormat(Qt::PlainText);
        originalsHint->setWordWrap(true);
        originalsHint->hide();
        ui->verticalLayout->insertWidget(2, originalsHint);
        clearOriginalsButton = new QPushButton(ui->groupFeatureList);
        clearOriginalsButton->setObjectName(QStringLiteral("patternClearOriginals"));
        ui->verticalLayout_2->addWidget(clearOriginalsButton);
        connect(clearOriginalsButton, &QPushButton::clicked, this, &TaskTransformedParameters::clearOriginals);
        connect(this, &TaskTransformedParameters::originalsChanged, this, &TaskTransformedParameters::updateOriginalsFeedback);
        highlightOriginalsButton = new QPushButton(ui->groupFeatureList);
        highlightOriginalsButton->setObjectName(QStringLiteral("patternHighlightOriginals"));
        ui->verticalLayout_2->addWidget(highlightOriginalsButton);
        connect(highlightOriginalsButton, &QPushButton::clicked, this, &TaskTransformedParameters::highlightOriginals);
        connect(ui->listWidgetFeatures, &QListWidget::itemSelectionChanged, this, [this] {
            if (!ui->listWidgetFeatures->selectedItems().isEmpty()) {
                highlightOriginals();
            }
        });
    }

    ui->buttonGroupMode->setId(ui->radioTransformBody, static_cast<int>(Mode::WholeShape));
    ui->buttonGroupMode->setId(ui->radioTransformToolShapes, static_cast<int>(Mode::Features));

    connect(ui->buttonGroupMode, &QButtonGroup::idClicked, this, &TaskTransformedParameters::onModeChanged);

    auto const mode = static_cast<Mode>(pcTransformed->TransformMode.getValue());
    ui->groupFeatureList->setEnabled(mode == Mode::Features);
    switch (mode) {
        case Mode::WholeShape:
            ui->radioTransformBody->setChecked(true);
            break;
        case Mode::Features:
            ui->radioTransformToolShapes->setChecked(true);
            break;
    }

    std::vector<App::DocumentObject*> originals = pcTransformed->getSortedOriginals();
    // Fill data into dialog elements
    for (auto obj : originals) {
        if (obj) {
            auto item = new QListWidgetItem();
            item->setText(QString::fromUtf8(obj->Label.getValue()));
            item->setData(Qt::UserRole, QString::fromLatin1(obj->getNameInDocument()));
            ui->listWidgetFeatures->addItem(item);
        }
    }

    setupParameterUI(ui->featureUI);  // create parameter UI widgets
    this->groupLayout()->addWidget(proxy);
    updateOriginalsFeedback();
}

void TaskTransformedParameters::updateOriginalsFeedback()
{
    if (!originalsStatus) {
        return;
    }
    auto pattern = getObject<PartDesign::Pattern>();
    if (!pattern) {
        return;
    }
    const bool whole = pattern->TransformMode.getValue()
        == static_cast<long>(PartDesign::Transformed::Mode::WholeShape);
    const int count = static_cast<int>(pattern->Originals.getValues().size());
    QString state = tr("Originals picking inactive");
    if (whole) {
        state = tr("Whole body; selected features are retained for switching back.");
    }
    else if (selectionMode == SelectionMode::AddFeature) {
        state = tr("Picking: add original feature");
    }
    else if (selectionMode == SelectionMode::RemoveFeature) {
        state = tr("Picking: remove original feature");
    }
    originalsStatus->setText(tr("Originals: %1\nAccepts: additive/subtractive features from this body.\n%2")
        .arg(count).arg(state));
    clearOriginalsButton->setText(tr("Clear"));
    clearOriginalsButton->setToolTip(tr("Clear selected features and start picking replacements"));
    clearOriginalsButton->setEnabled(!whole && count > 0);
    highlightOriginalsButton->setText(tr("Highlight"));
    highlightOriginalsButton->setToolTip(tr("Inspect the selected original, or all originals if no row is selected"));
    highlightOriginalsButton->setEnabled(!whole && count > 0);
}

void TaskTransformedParameters::highlightOriginals()
{
    auto pattern = getObject<PartDesign::Pattern>();
    if (!pattern || pattern->TransformMode.getValue()
        != static_cast<long>(PartDesign::Transformed::Mode::Features)) {
        return;
    }
    Base::StateLocker inspecting(inspectingOriginals, true);
    prepareOriginalsSelection();
    exitSelectionMode();
    const auto showForInspection = [this](App::DocumentObject* object, bool visible) {
        if (auto view = Gui::Application::Instance->getViewProvider(object)) {
            inspectionVisibility.emplace(object->getNameInDocument(), view->isVisible());
            view->setVisible(visible);
        }
    };
    showForInspection(pattern, false);
    Gui::Selection().clearSelection();
    const bool all = ui->listWidgetFeatures->selectedItems().isEmpty();
    for (int row = 0; row < ui->listWidgetFeatures->count(); ++row) {
        auto item = ui->listWidgetFeatures->item(row);
        if (!all && !item->isSelected()) {
            continue;
        }
        const auto name = item->data(Qt::UserRole).toString().toLatin1();
        if (auto object = pattern->getDocument()->getObject(name.constData())) {
            showForInspection(object, true);
            Gui::Selection().addSelection(pattern->getDocument()->getName(), name.constData());
        }
    }
}

void TaskTransformedParameters::restoreOriginalsVisibility()
{
    if (inspectionVisibility.empty()) {
        return;
    }
    if (auto pattern = getTopTransformedObject()) {
        for (const auto& [name, visible] : inspectionVisibility) {
            if (auto object = pattern->getDocument()->getObject(name.c_str())) {
                if (auto view = Gui::Application::Instance->getViewProvider(object)) {
                    view->setVisible(visible);
                }
            }
        }
    }
    inspectionVisibility.clear();
}

void TaskTransformedParameters::clearOriginals()
{
    auto pattern = getObject<PartDesign::Pattern>();
    if (!pattern || pattern->TransformMode.getValue()
        != static_cast<long>(PartDesign::Transformed::Mode::Features)) {
        return;
    }
    prepareOriginalsSelection();
    exitSelectionMode();
    setupTransaction();
    pattern->Originals.setValues({});
    setOriginalsHint({});
    const QSignalBlocker blocker(ui->listWidgetFeatures);
    ui->listWidgetFeatures->clear();
    Q_EMIT originalsChanged();
    recomputeFeature();
    startFeatureSelection();
}

void TaskTransformedParameters::startFeatureSelection()
{
    ui->buttonAddFeature->setChecked(true);
}

void TaskTransformedParameters::insertWorkflowHeader(QWidget* widget)
{
    ui->verticalLayout->insertWidget(0, widget);
}

void TaskTransformedParameters::slotDeletedObject(const Gui::ViewProviderDocumentObject& Obj)
{
    if (TransformedView == &Obj) {
        restoreOriginalsVisibility();
        TransformedView = nullptr;
    }
}

void TaskTransformedParameters::changeEvent(QEvent* event)
{
    TaskBox::changeEvent(event);
    if (event->type() == QEvent::LanguageChange && proxy) {
        ui->retranslateUi(proxy);
        retranslateParameterUI(ui->featureUI);
        updateOriginalsFeedback();
    }
}

void TaskTransformedParameters::onSelectionChanged(const Gui::SelectionChanges& msg)
{
    if (originalSelected(msg)) {
        exitSelectionMode();
    }
}

void TaskTransformedParameters::clearButtons()
{
    if (insideMultiTransform) {
        parentTask->clearButtons();
    }
    else {
        restoreOriginalsVisibility();
        ui->buttonAddFeature->setChecked(false);
        ui->buttonRemoveFeature->setChecked(false);
    }
}

int TaskTransformedParameters::getUpdateViewTimeout() const
{
    return 500;
}

void TaskTransformedParameters::addObject(App::DocumentObject* obj)
{
    QString label = QString::fromUtf8(obj->Label.getValue());
    QString objectName = QString::fromLatin1(obj->getNameInDocument());

    auto item = new QListWidgetItem();
    item->setText(label);
    item->setData(Qt::UserRole, objectName);
    ui->listWidgetFeatures->addItem(item);
}

void TaskTransformedParameters::removeObject(App::DocumentObject* obj)
{
    const QSignalBlocker blocker(ui->listWidgetFeatures);
    const QString name = QString::fromLatin1(obj->getNameInDocument());
    for (int row = ui->listWidgetFeatures->count() - 1; row >= 0; --row) {
        if (ui->listWidgetFeatures->item(row)->data(Qt::UserRole).toString() == name) {
            delete ui->listWidgetFeatures->takeItem(row);
        }
    }
}

QString TaskTransformedParameters::originalSelectionError(App::DocumentObject* object) const
{
    auto transformed = getObject();
    if (!object || !transformed) {
        return tr("The selected feature is no longer available.");
    }
    if (object->getDocument() != transformed->getDocument()) {
        return tr("Select a feature in this document.");
    }
    if (object == transformed || transformed->getInListEx(true).count(object)) {
        return tr("The result and features depending on it cannot be originals.");
    }
    if (!object->isDerivedFrom<PartDesign::FeatureAddSub>()) {
        return tr("Select an additive or subtractive feature, not a body, sketch or datum.");
    }
    auto body = transformed->getFeatureBody();
    if (!body || PartDesign::Body::findBodyOf(object) != body) {
        return tr("Select a feature in the active body.");
    }
    return {};
}

void TaskTransformedParameters::setOriginalsHint(const QString& text)
{
    if (originalsHint) {
        originalsHint->setText(text);
        originalsHint->setVisible(!text.isEmpty());
    }
}

bool TaskTransformedParameters::changeOriginal(App::DocumentObject* object, bool add)
{
    const auto error = originalSelectionError(object);
    if (!error.isEmpty()) {
        setOriginalsHint(error);
        return false;
    }
    auto transformed = getObject();
    auto originals = transformed->getSortedOriginals();
    const auto found = std::ranges::find(originals, object);
    if (add) {
        if (found != originals.end()) {
            setOriginalsHint(tr("This feature is already an original."));
            return false;
        }
        originals.push_back(object);
    }
    else {
        if (found == originals.end()) {
            setOriginalsHint(tr("This feature is not in Originals. Select a listed feature to remove."));
            return false;
        }
        originals.erase(found);
    }
    setupTransaction();
    transformed->Originals.setValues(originals);
    if (add) {
        addObject(object);
    }
    else {
        removeObject(object);
    }
    setOriginalsHint({});
    Q_EMIT originalsChanged();
    return true;
}

void TaskTransformedParameters::setOriginalsPreselection(
    const std::vector<Gui::SelectionObject>& selection
)
{
    if (!getObject<PartDesign::Pattern>()) {
        return;
    }
    QStringList ignored;
    std::set<App::DocumentObject*> seen;
    bool changed = false;
    for (auto item : selection) {
        auto object = item.getObject();
        if (!object || !seen.insert(object).second) {
            continue;
        }
        const auto error = originalSelectionError(object);
        if (!error.isEmpty()) {
            ignored << tr("Ignored %1: %2").arg(QString::fromUtf8(object->Label.getValue()), error);
        }
        else {
            changed = changeOriginal(object, true) || changed;
        }
    }
    if (changed) {
        recomputeFeature();
        exitSelectionMode();
    }
    setOriginalsHint(ignored.join(QLatin1Char('\n')));
}

bool TaskTransformedParameters::originalSelected(const Gui::SelectionChanges& msg)
{
    if (inspectingOriginals || msg.Type != Gui::SelectionChanges::AddSelection
        || (selectionMode != SelectionMode::AddFeature
            && selectionMode != SelectionMode::RemoveFeature)) {
        return false;
    }
    auto transformed = getObject();
    if (!transformed) {
        return false;
    }
    if (strcmp(msg.pDocName, transformed->getDocument()->getName()) != 0) {
        setOriginalsHint(tr("Select a feature in this document."));
        return false;
    }
    auto object = transformed->getDocument()->getObject(msg.pObjectName);
    if (!changeOriginal(object, selectionMode == SelectionMode::AddFeature)) {
        return false;
    }
    recomputeFeature();
    return true;
}

void TaskTransformedParameters::setupTransaction()
{
    if (!isEnabledTransaction()) {
        return;
    }

    auto obj = getObject();
    if (!obj) {
        return;
    }

    int tid = obj->getDocument()->getBookedTransactionID();
    if (tid != App::NullTransaction) {
        return;
    }

    // open a transaction if none is active
    // where is this transaction committed - theo-vt?
    std::string name("Edit ");
    name += obj->Label.getValue();
    transactionID = obj->getDocument()->openTransaction(name.c_str());
}

void TaskTransformedParameters::setEnabledTransaction(bool on)
{
    enableTransaction = on;
}

bool TaskTransformedParameters::isEnabledTransaction() const
{
    return enableTransaction;
}

void TaskTransformedParameters::onModeChanged(int mode_id)
{
    if (mode_id < 0) {
        return;
    }

    auto pcTransformed = getObject<PartDesign::Transformed>();
    setupTransaction();
    pcTransformed->TransformMode.setValue(mode_id);

    using Mode = PartDesign::Transformed::Mode;
    Mode const mode = static_cast<Mode>(mode_id);

    ui->groupFeatureList->setEnabled(mode == Mode::Features);
    const QSignalBlocker blocker(ui->listWidgetFeatures);
    ui->listWidgetFeatures->clear();
    if (mode == Mode::Features) {
        for (auto* original : pcTransformed->getSortedOriginals()) {
            if (original) {
                addObject(original);
            }
        }
    }
    exitSelectionMode();
    Q_EMIT originalsChanged();
    recomputeFeature();
}

void TaskTransformedParameters::onButtonAddFeature(bool checked)
{
    if (checked) {
        restoreOriginalsVisibility();
        prepareOriginalsSelection();
        const QSignalBlocker blocker(ui->buttonAddFeature);
        ui->buttonAddFeature->setChecked(true);
        hideObject();
        showBase();
        selectionMode = SelectionMode::AddFeature;
        Gui::Selection().clearSelection();
    }
    else {
        exitSelectionMode();
    }

    ui->buttonRemoveFeature->setDisabled(checked);
    updateOriginalsFeedback();
}

// Make sure only some feature before the given one is visible
void TaskTransformedParameters::checkVisibility()
{
    auto feat = getObject();
    auto body = feat->getFeatureBody();
    if (!body) {
        return;
    }
    auto inset = feat->getInListEx(true);
    inset.emplace(feat);
    for (auto obj : body->Group.getValues()) {
        if (!obj->Visibility.getValue() || !obj->isDerivedFrom<PartDesign::Feature>()) {
            continue;
        }
        if (inset.count(obj) > 0) {
            break;
        }
        return;
    }
    FCMD_OBJ_SHOW(getBaseObject());
}

void TaskTransformedParameters::onButtonRemoveFeature(bool checked)
{
    if (checked) {
        restoreOriginalsVisibility();
        prepareOriginalsSelection();
        const QSignalBlocker blocker(ui->buttonRemoveFeature);
        ui->buttonRemoveFeature->setChecked(true);
        checkVisibility();
        selectionMode = SelectionMode::RemoveFeature;
        Gui::Selection().clearSelection();
    }
    else {
        exitSelectionMode();
    }

    ui->buttonAddFeature->setDisabled(checked);
    updateOriginalsFeedback();
}

void TaskTransformedParameters::onFeatureDeleted()
{
    PartDesign::Transformed* pcTransformed = getObject();
    std::vector<App::DocumentObject*> originals = pcTransformed->getSortedOriginals();
    int currentRow = ui->listWidgetFeatures->currentRow();
    if (currentRow < 0) {
        Base::Console().error("PartDesign Pattern: No feature selected for removing.\n");
        return;  // no current row selected
    }
    const auto name = ui->listWidgetFeatures->item(currentRow)->data(Qt::UserRole).toString();
    auto* original = pcTransformed->getDocument()->getObject(name.toLatin1().constData());
    std::erase(originals, original);
    setupTransaction();
    pcTransformed->Originals.setValues(originals);
    const QSignalBlocker blocker(ui->listWidgetFeatures);
    ui->listWidgetFeatures->model()->removeRow(currentRow);
    Q_EMIT originalsChanged();
    recomputeFeature();
}

void TaskTransformedParameters::removeItemFromListWidget(QListWidget* widget, const QString& itemstr)
{
    QList<QListWidgetItem*> items = widget->findItems(itemstr, Qt::MatchExactly);
    if (!items.empty()) {
        for (auto item : items) {
            delete widget->takeItem(widget->row(item));
        }
    }
}

void TaskTransformedParameters::fillAxisCombo(Gui::ComboLinks& combolinks, Part::Part2DObject* sketch)
{
    combolinks.clear();

    // add sketch axes
    if (sketch) {
        combolinks.addLink(sketch, "H_Axis", tr("Horizontal sketch axis"));
        combolinks.addLink(sketch, "V_Axis", tr("Vertical sketch axis"));
        combolinks.addLink(sketch, "N_Axis", tr("Normal sketch axis"));
        for (int i = 0; i < sketch->getAxisCount(); i++) {
            QString itemText = tr("Construction line %1").arg(i + 1);
            std::stringstream sub;
            sub << "Axis" << i;
            combolinks.addLink(sketch, sub.str(), itemText);
        }
    }

    // add part axes
    App::DocumentObject* obj = getTopTransformedObject();
    PartDesign::Body* body = PartDesign::Body::findBodyOf(obj);

    if (body) {
        try {
            App::Origin* orig = body->getOrigin();
            combolinks.addLink(orig->getX(), "", tr("Base X-axis"));
            combolinks.addLink(orig->getY(), "", tr("Base Y-axis"));
            combolinks.addLink(orig->getZ(), "", tr("Base Z-axis"));
        }
        catch (const Base::Exception& ex) {
            Base::Console().error("{}\n", ex.what());
        }
    }

    // add "Select reference"
    combolinks.addLink(nullptr, std::string(), tr("Select reference…"));
}

void TaskTransformedParameters::fillPlanesCombo(Gui::ComboLinks& combolinks, Part::Part2DObject* sketch)
{
    combolinks.clear();

    // add sketch axes
    if (sketch) {
        combolinks.addLink(sketch, "V_Axis", QObject::tr("Vertical sketch axis"));
        combolinks.addLink(sketch, "H_Axis", QObject::tr("Horizontal sketch axis"));
        for (int i = 0; i < sketch->getAxisCount(); i++) {
            QString itemText = tr("Construction line %1").arg(i + 1);
            std::stringstream sub;
            sub << "Axis" << i;
            combolinks.addLink(sketch, sub.str(), itemText);
        }
    }

    // add part baseplanes
    App::DocumentObject* obj = getTopTransformedObject();
    PartDesign::Body* body = PartDesign::Body::findBodyOf(obj);

    if (body) {
        try {
            App::Origin* orig = body->getOrigin();
            combolinks.addLink(orig->getXY(), "", tr("Base XY-plane"));
            combolinks.addLink(orig->getYZ(), "", tr("Base YZ-plane"));
            combolinks.addLink(orig->getXZ(), "", tr("Base XZ-plane"));
        }
        catch (const Base::Exception& ex) {
            Base::Console().error("{}\n", ex.what());
        }
    }

    // add "Select reference"
    combolinks.addLink(nullptr, std::string(), tr("Select reference…"));
}

void TaskTransformedParameters::recomputeFeature()
{
    getTopTransformedView()->recomputeFeature();
}

PartDesignGui::ViewProviderTransformed* TaskTransformedParameters::getTopTransformedView() const
{
    return insideMultiTransform ? parentTask->TransformedView : TransformedView;
}

PartDesign::Transformed* TaskTransformedParameters::getTopTransformedObject() const
{
    ViewProviderTransformed* vp = getTopTransformedView();
    if (!vp) {
        return nullptr;
    }

    App::DocumentObject* transform = vp->getObject();
    assert(transform->isDerivedFrom<PartDesign::Transformed>());
    return static_cast<PartDesign::Transformed*>(transform);
}

PartDesign::Transformed* TaskTransformedParameters::getObject() const
{
    if (insideMultiTransform) {
        return parentTask->getSubFeature();
    }
    if (TransformedView) {
        return TransformedView->getObject<PartDesign::Transformed>();
    }
    return nullptr;
}

App::DocumentObject* TaskTransformedParameters::getBaseObject() const
{
    PartDesign::Feature* feature = getTopTransformedObject();
    if (!feature) {
        return nullptr;
    }

    // NOTE: getBaseObject() throws if there is no base; shouldn't happen here.
    App::DocumentObject* base = feature->getBaseObject(true);
    if (!base) {
        auto body = feature->getFeatureBody();
        if (body) {
            base = body->getPrevSolidFeature(feature);
        }
    }
    return base;
}

App::DocumentObject* TaskTransformedParameters::getSketchObject() const
{
    PartDesign::Transformed* feature = getTopTransformedObject();
    return feature ? feature->getSketchObject() : nullptr;
}

void TaskTransformedParameters::hideObject()
{
    try {
        FCMD_OBJ_HIDE(getTopTransformedObject());
    }
    catch (const Base::Exception& e) {
        e.reportException();
    }
}

void TaskTransformedParameters::showObject()
{
    try {
        FCMD_OBJ_SHOW(getTopTransformedObject());
    }
    catch (const Base::Exception& e) {
        e.reportException();
    }
}

void TaskTransformedParameters::hideBase()
{
    try {
        FCMD_OBJ_HIDE(getBaseObject());
    }
    catch (const Base::Exception& e) {
        e.reportException();
    }
}

void TaskTransformedParameters::showBase()
{
    try {
        FCMD_OBJ_SHOW(getBaseObject());
    }
    catch (const Base::Exception& e) {
        e.reportException();
    }
}

void TaskTransformedParameters::exitSelectionMode()
{
    try {
        clearButtons();
        selectionMode = SelectionMode::None;
        Gui::Selection().rmvSelectionGate();
        updateOriginalsFeedback();
    }
    catch (Base::Exception& exc) {
        exc.reportException();
    }
}

void TaskTransformedParameters::addReferenceSelectionGate(AllowSelectionFlags allow)
{
    std::unique_ptr<Gui::SelectionFilterGate> gateRefPtr(
        new ReferenceSelection(getBaseObject(), allow)
    );
    std::unique_ptr<Gui::SelectionFilterGate> gateDepPtr(
        new NoDependentsSelection(getTopTransformedObject())
    );
    Gui::Selection().addSelectionGate(new CombineSelectionFilterGates(gateRefPtr, gateDepPtr));
}

//**************************************************************************
//**************************************************************************
// TaskDialog
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

TaskDlgTransformedParameters::TaskDlgTransformedParameters(ViewProviderTransformed* viewProvider)
    : TaskDlgFeatureParameters(viewProvider)
{}

//==== calls from the TaskView ===============================================================

bool TaskDlgTransformedParameters::accept()
{
    parameter->exitSelectionMode();
    parameter->apply();

    return TaskDlgFeatureParameters::accept();
}

bool TaskDlgTransformedParameters::reject()
{
    const auto originalSelection = selectionOnCancel;
    const bool restore = restoreSelectionOnCancel;
    // ensure that we are not in selection mode
    parameter->exitSelectionMode();
    const bool rejected = TaskDlgFeatureParameters::reject();
    if (rejected && restore) {
        Gui::Selection().clearSelection();
        for (const auto& item : originalSelection) {
            if (!item.getObject()) {
                continue;
            }
            if (item.getSubNames().empty()) {
                Gui::Selection().addSelection(item.getDocName(), item.getFeatName());
            }
            else {
                for (const auto& sub : item.getSubNames()) {
                    Gui::Selection().addSelection(item.getDocName(), item.getFeatName(), sub.c_str());
                }
            }
        }
    }
    return rejected;
}

#include "moc_TaskTransformedParameters.cpp"
