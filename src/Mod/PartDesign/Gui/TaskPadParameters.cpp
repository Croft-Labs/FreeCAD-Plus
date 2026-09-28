// SPDX-License-Identifier: LGPL-2.1-or-later

/***************************************************************************
 *   Copyright (c) 2011 Juergen Riegel <FreeCAD@juergen-riegel.net>        *
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

#include <algorithm>
#include <cstring>
#include <Precision.hxx>
#include <QEvent>
#include <QGroupBox>
#include <QLabel>
#include <QListWidget>
#include <QPushButton>
#include <QSignalBlocker>
#include <QVBoxLayout>


#include <App/Document.h>
#include <Gui/Application.h>
#include <Gui/CommandT.h>
#include <Mod/Part/App/Part2DObject.h>
#include <Mod/PartDesign/App/Body.h>
#include <Mod/PartDesign/App/FeatureExtrude.h>

#include "ReferenceSelection.h"
#include "ui_TaskPadPocketParameters.h"
#include "TaskPadParameters.h"


using namespace PartDesignGui;
using namespace Gui;

namespace
{
// An extrusion profile is one source object, optionally restricted to several curves
// or faces. Keep cross-body references and dependency cycles out of the editor.
class ExtrudeProfileSelection: public Gui::SelectionFilterGate
{
public:
    explicit ExtrudeProfileSelection(const PartDesign::FeatureExtrude* pad)
        : Gui::SelectionFilterGate(nullPointer())
        , pad(pad)
    {}

    bool allow(App::Document* doc, App::DocumentObject* object, const char* subName) override
    {
        if (!object || doc != pad->getDocument() || object == pad
            || !object->isDerivedFrom<Part::Feature>() || object->isDerivedFrom<PartDesign::Body>()
            || PartDesign::Body::findBodyOf(object) != PartDesign::Body::findBodyOf(pad)
            || !pad->testIfLinkDAGCompatible(object)) {
            return false;
        }

        if (!subName || !*subName) {
            const auto& shape = static_cast<Part::Feature*>(object)->Shape.getValue();
            return !shape.isNull() && !shape.hasSubShape(TopAbs_SOLID)
                && shape.hasSubShape(TopAbs_EDGE);
        }

        ReferenceSelection geometry(pad, AllowSelection::EDGE | AllowSelection::FACE);
        return geometry.allow(doc, object, subName);
    }

private:
    const PartDesign::FeatureExtrude* pad;
};
}  // namespace

/* TRANSLATOR PartDesignGui::TaskPadParameters */

TaskPadParameters::TaskPadParameters(ViewProviderExtrude* PadView, QWidget* parent, bool newObj)
    : TaskExtrudeParameters(PadView, parent, "PartDesign_Pad", tr("Extrude Parameters"))
{
    ui->offsetEdit->setToolTip(tr("Offset from the face at which the extrusion will end on side 1"));
    ui->offsetEdit2->setToolTip(tr("Offset from the face at which the extrusion will end on side 2"));
    ui->checkBoxReversed->setToolTip(tr("Reverses extrusion direction"));

    // set the history path
    ui->lengthEdit->setEntryName(QByteArray("Length"));
    ui->lengthEdit->setParamGrpPath(QByteArray("User parameter:BaseApp/History/PadLength"));
    ui->lengthEdit2->setEntryName(QByteArray("Length2"));
    ui->lengthEdit2->setParamGrpPath(QByteArray("User parameter:BaseApp/History/PadLength2"));
    ui->offsetEdit->setEntryName(QByteArray("Offset"));
    ui->offsetEdit->setParamGrpPath(QByteArray("User parameter:BaseApp/History/PadOffset"));
    ui->offsetEdit2->setEntryName(QByteArray("Offset2"));
    ui->offsetEdit2->setParamGrpPath(QByteArray("User parameter:BaseApp/History/PadOffset2"));
    ui->taperEdit->setEntryName(QByteArray("TaperAngle"));
    ui->taperEdit->setParamGrpPath(QByteArray("User parameter:BaseApp/History/PadTaperAngle"));
    ui->taperEdit2->setEntryName(QByteArray("TaperAngle2"));
    ui->taperEdit2->setParamGrpPath(QByteArray("User parameter:BaseApp/History/PadTaperAngle2"));

    setupProfileSelection();
    setupDialog();
    setupOperationSelection();

    // if it is a newly created object use the last value of the history
    if (newObj) {
        readValuesFromHistory();
    }

    updateProfileList();
    if (!getObject<PartDesign::FeatureExtrude>()->Profile.getValue()) {
        setSelectionMode(SelectProfile);
    }
}

TaskPadParameters::~TaskPadParameters()
{
    // The document may also close without accepting or rejecting the dialog.
    if (getObject()) {
        setSelectionMode(None);
    }
}

void TaskPadParameters::translateOperationSelection()
{
    const QSignalBlocker blocker(ui->comboOperation);
    auto feature = getObject<PartDesign::FeatureExtrude>();
    const QString operation = QString::fromLatin1(feature->Operation.getValueAsString());
    // Preserve editing of existing Common features without changing their meaning.
    const bool showCommon = operation == QStringLiteral("Common") || ui->comboOperation->count() > 2;
    ui->comboOperation->clear();
    ui->comboOperation->addItem(tr("Add"), QStringLiteral("Union"));
    ui->comboOperation->addItem(tr("Subtract"), QStringLiteral("Subtraction"));
    if (showCommon) {
        ui->comboOperation->addItem(tr("Intersect"), QStringLiteral("Common"));
    }
    ui->comboOperation->setCurrentIndex(ui->comboOperation->findData(operation));
    ui->comboOperation->setDisabled(feature->Operation.isReadOnly());
}

void TaskPadParameters::setupOperationSelection()
{
    translateOperationSelection();
    QWidget::setTabOrder(ui->comboOperation, selectProfile);
    connect(ui->comboOperation, qOverload<int>(&QComboBox::activated), this, [this](int index) {
        auto feature = getObject<PartDesign::FeatureExtrude>();
        feature->Operation.setValue(
            ui->comboOperation->itemData(index).toString().toLatin1().constData()
        );
        recomputeFeature();
        updateUI(Side::First);
        setGizmoPositions();
        updateProfileList();
    });
}

void TaskPadParameters::setupProfileSelection()
{
    profileGroup = new QGroupBox(proxy);
    profileGroup->setObjectName(QStringLiteral("padProfileGroup"));
    auto layout = new QVBoxLayout(profileGroup);
    profileHint = new QLabel(profileGroup);
    profileHint->setObjectName(QStringLiteral("padProfileHint"));
    profileHint->setWordWrap(true);
    layout->addWidget(profileHint);

    profileList = new QListWidget(profileGroup);
    profileList->setObjectName(QStringLiteral("padProfileList"));
    profileList->setSelectionMode(QAbstractItemView::ExtendedSelection);
    profileList->setMaximumHeight(120);
    layout->addWidget(profileList);

    auto buttons = new QHBoxLayout;
    selectProfile = new QPushButton(profileGroup);
    selectProfile->setObjectName(QStringLiteral("padSelectProfile"));
    selectProfile->setCheckable(true);
    removeProfile = new QPushButton(profileGroup);
    removeProfile->setObjectName(QStringLiteral("padRemoveProfile"));
    clearProfile = new QPushButton(profileGroup);
    clearProfile->setObjectName(QStringLiteral("padClearProfile"));
    buttons->addWidget(selectProfile);
    buttons->addWidget(removeProfile);
    buttons->addWidget(clearProfile);
    layout->addLayout(buttons);
    ui->verticalLayout->insertWidget(1, profileGroup);

    connect(selectProfile, &QPushButton::toggled, this, [this](bool checked) {
        setSelectionMode(checked ? SelectProfile : None);
    });
    connect(removeProfile, &QPushButton::clicked, this, &TaskPadParameters::removeSelectedProfileItems);
    connect(clearProfile, &QPushButton::clicked, this, [this] {
        updateProfile(nullptr, {});
        setSelectionMode(SelectProfile);
    });
    connect(profileList, &QListWidget::itemSelectionChanged, this, [this] {
        removeProfile->setEnabled(!profileList->selectedItems().isEmpty());
    });
    translateProfileSelection();
}

void TaskPadParameters::translateProfileSelection()
{
    profileGroup->setTitle(tr("Profile"));
    selectProfile->setText(selectionMode == SelectProfile ? tr("Done") : tr("Select"));
    selectProfile->setToolTip(
        tr("Select a sketch, or edges and faces from one object in the active body")
    );
    removeProfile->setText(tr("Remove"));
    clearProfile->setText(tr("Clear"));
}

void TaskPadParameters::changeEvent(QEvent* event)
{
    TaskExtrudeParameters::changeEvent(event);
    if (event->type() == QEvent::LanguageChange && profileGroup) {
        translateOperationSelection();
        translateProfileSelection();
        updateProfileList();
    }
}

void TaskPadParameters::showProfileForSelection(App::DocumentObject* object)
{
    // The base solid's visibility is already managed by onSelectReference().
    if (!object || object == getObject<PartDesign::FeatureExtrude>()->getBaseObject(true)) {
        return;
    }
    auto view = Gui::Application::Instance->getViewProvider(object);
    if (view) {
        profileVisibility.emplace(object->getNameInDocument(), view->isVisible());
        view->show();
    }
}

void TaskPadParameters::restoreProfileVisibility()
{
    auto doc = getAppDocument();
    if (doc) {
        for (const auto& [name, visible] : profileVisibility) {
            if (auto object = doc->getObject(name.c_str())) {
                if (auto view = Gui::Application::Instance->getViewProvider(object)) {
                    view->setVisible(visible);
                }
            }
        }
    }
    profileVisibility.clear();
}

void TaskPadParameters::setSelectionMode(SelectionMode mode, Side side)
{
    if (selectionMode == mode && activeSelectionSide == side) {
        return;
    }
    if (selectionMode == SelectProfile) {
        // Restore the preview and any temporarily shown profile before entering
        // another selector (direction, start reference, or up-to face).
        onSelectReference(AllowSelection::NONE);
        restoreProfileVisibility();
    }
    TaskExtrudeParameters::setSelectionMode(mode, side);
    if (mode == SelectProfile) {
        auto pad = getObject<PartDesign::FeatureExtrude>();
        onSelectReference(AllowSelection::EDGE | AllowSelection::FACE);
        Gui::Selection().addSelectionGate(new ExtrudeProfileSelection(pad));
        showProfileForSelection(pad->Profile.getValue());
    }
    if (selectProfile) {
        const QSignalBlocker blocker(selectProfile);
        selectProfile->setChecked(mode == SelectProfile);
        translateProfileSelection();
    }
}

void TaskPadParameters::updateProfileList()
{
    auto pad = getObject<PartDesign::FeatureExtrude>();
    auto object = pad->Profile.getValue();
    profileList->clear();
    if (object) {
        const QString label = QString::fromUtf8(object->Label.getValue());
        const auto subs = pad->Profile.getSubValues(false);
        if (subs.empty()) {
            profileList->addItem(label + tr(" (whole profile)"));
        }
        else {
            for (const auto& sub : subs) {
                profileList->addItem(
                    sub.empty() ? label + tr(" (whole profile)")
                                : label + QStringLiteral(":") + QString::fromStdString(sub)
                );
            }
        }
    }
    clearProfile->setEnabled(object != nullptr);
    removeProfile->setEnabled(false);
    if (!object) {
        profileHint->setText(tr("Select a sketch in the tree, or click curves or faces in the "
                                "model. Curves must form a closed profile."));
    }
    else if (pad->isError()) {
        profileHint->setText(tr("Complete a closed profile or adjust the extrusion parameters.\n%1")
                                 .arg(QString::fromUtf8(pad->getStatusString())));
    }
    else {
        profileHint->setText(tr("Select adds curves or faces from this object. Clear the list to "
                                "choose a different profile."));
    }
}

void TaskPadParameters::updateProfile(App::DocumentObject* object, const std::vector<std::string>& subNames)
{
    auto pad = getObject<PartDesign::FeatureExtrude>();
    auto previous = pad->Profile.getValue();
    const bool followsNormal = !pad->ReferenceAxis.getValue()
        || (pad->ReferenceAxis.getValue() == previous
            && pad->ReferenceAxis.getSubValues() == std::vector<std::string> {"N_Axis"});
    pad->Profile.setValue(object, subNames);
    if (followsNormal) {
        if (object && object->isDerivedFrom<Part::Part2DObject>()) {
            pad->ReferenceAxis.setValue(object, {"N_Axis"});
        }
        else {
            pad->ReferenceAxis.setValue(nullptr, {});
        }
    }
    axesInList.clear();
    recomputeFeature();
    updateUI(Side::First);
    setGizmoPositions();
    updateProfileList();
    if (selectionMode == SelectProfile) {
        showProfileForSelection(object);
    }
}

void TaskPadParameters::onSelectionChanged(const Gui::SelectionChanges& msg)
{
    if (selectionMode != SelectProfile) {
        TaskExtrudeParameters::onSelectionChanged(msg);
        return;
    }
    // The profile list owns the selection: a normal viewport click clears the
    // global selection first, but must not discard curves already in the list.
    if (msg.Type != Gui::SelectionChanges::AddSelection) {
        return;
    }
    auto pad = getObject<PartDesign::FeatureExtrude>();
    if (std::strcmp(msg.pDocName, pad->getDocument()->getName()) != 0) {
        return;
    }
    auto object = pad->getDocument()->getObject(msg.pObjectName);
    ExtrudeProfileSelection gate(pad);
    if (!gate.allow(pad->getDocument(), object, msg.pSubName)) {
        return;
    }
    auto current = pad->Profile.getValue();
    if (current && current != object) {
        profileHint->setText(tr("An extrusion uses one profile object. Clear the list before "
                                "selecting a different object."));
        return;
    }
    const std::string sub = msg.pSubName;
    auto subs = pad->Profile.getSubValues(false);
    if (sub.empty()) {
        subs.clear();
    }
    else {
        if (current && (subs.empty() || std::find(subs.begin(), subs.end(), "") != subs.end())) {
            profileHint->setText(tr("The whole profile is selected. Clear the list to select "
                                    "individual curves or faces."));
            return;
        }
        if (std::find(subs.begin(), subs.end(), sub) == subs.end()) {
            subs.push_back(sub);
        }
    }
    updateProfile(object, subs);
}

void TaskPadParameters::removeSelectedProfileItems()
{
    auto pad = getObject<PartDesign::FeatureExtrude>();
    auto subs = pad->Profile.getSubValues(false);
    for (int row = profileList->count() - 1; row >= 0; --row) {
        if (profileList->item(row)->isSelected() && row < static_cast<int>(subs.size())) {
            subs.erase(subs.begin() + row);
        }
    }
    updateProfile(subs.empty() ? nullptr : pad->Profile.getValue(), subs);
}

void TaskPadParameters::translateModeList(QComboBox* box, int index)
{
    const QSignalBlocker blocker(box);
    box->clear();
    box->addItem(tr("Dimension"));
    box->addItem(tr("To last"));
    box->addItem(tr("To first"));
    box->addItem(tr("Up to face"));
    box->addItem(tr("Up to shape"));
    box->addItem(tr("Through all"));
    box->setCurrentIndex(index);
}

void TaskPadParameters::updateUI(Side side)
{
    // update direction combobox
    fillDirectionCombo();
    // set and enable checkboxes
    updateWholeUI(side);
}

void TaskPadParameters::onModeChanged(int index, Side side)
{
    auto& sideCtrl = getSideController(side);

    switch (static_cast<Mode>(index)) {
        case Mode::Dimension:
            sideCtrl.Type->setValue("Length");
            if (side == Side::First) {
                // Avoid error message
                double L = sideCtrl.lengthEdit->value().getValue();
                Side otherSide = side == Side::First ? Side::Second : Side::First;
                auto& sideCtrl2 = getSideController(otherSide);
                double L2 = static_cast<SidesMode>(getSidesMode()) == SidesMode::TwoSides
                    ? sideCtrl2.lengthEdit->value().getValue()
                    : 0;
                if (std::abs(L + L2) < Precision::Confusion()) {
                    sideCtrl.lengthEdit->setValue(5.0);
                }
            }
            break;
        case Mode::ThroughAll:
            sideCtrl.Type->setValue("ThroughAll");
            break;
        case Mode::ToLast:
            sideCtrl.Type->setValue("UpToLast");
            break;
        case Mode::ToFirst:
            sideCtrl.Type->setValue("UpToFirst");
            break;
        case Mode::ToFace:
            sideCtrl.Type->setValue("UpToFace");
            if (sideCtrl.lineFaceName->text().isEmpty()) {
                sideCtrl.buttonFace->setChecked(true);
                handleLineFaceNameClick(sideCtrl.lineFaceName);  // sets placeholder text
            }
            break;
        case Mode::ToShape:
            sideCtrl.Type->setValue("UpToShape");
            break;
    }

    updateUI(side);
    recomputeFeature();
}

void TaskPadParameters::apply()
{
    auto pad = getObject<PartDesign::FeatureExtrude>();
    auto profile = pad->Profile.getValue();
    if (!profile) {
        profileHint->setText(tr("Select a profile before accepting the extrusion."));
        setSelectionMode(SelectProfile);
        throw Base::ValueError("Select a profile before accepting the extrusion.");
    }
    FCMD_OBJ_CMD(
        pad,
        "Profile = (" << Gui::Command::getObjectCmd(profile) << ", "
                      << buildLinkSubPythonStr(profile, pad->Profile.getSubValues()) << ")"
    );
    applyParameters();
}

//**************************************************************************
//**************************************************************************
// TaskDialog
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

TaskDlgPadParameters::TaskDlgPadParameters(ViewProviderExtrude* PadView, bool /*newObj*/)
    : TaskDlgExtrudeParameters(PadView)
    , parameters(new TaskPadParameters(PadView))
{
    Content.push_back(parameters);
    Content.push_back(preview);
}

//==== calls from the TaskView ===============================================================

#include "moc_TaskPadParameters.cpp"
