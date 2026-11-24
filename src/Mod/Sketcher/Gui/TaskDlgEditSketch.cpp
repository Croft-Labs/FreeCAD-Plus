/***************************************************************************
 *   Copyright (c) 2009 Jürgen Riegel <juergen.riegel@web.de>              *
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


#include <Gui/Command.h>
#include <Gui/Application.h>
#include <Gui/Document.h>
#include <Gui/MDIView.h>
#include <QPushButton>
#include <QTimer>
#include <Inventor/events/SoKeyboardEvent.h>

#include "TaskDlgEditSketch.h"
#include "ViewProviderSketch.h"


using namespace SketcherGui;

namespace sp = std::placeholders;

//**************************************************************************
//**************************************************************************
// TaskDialog
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

TaskDlgEditSketch::TaskDlgEditSketch(ViewProviderSketch* sketchView)
    : TaskDialog()
    , sketchView(sketchView)
{
    assert(sketchView);
    ToolSettings = new TaskSketcherTool(sketchView);
    Constraints = new TaskSketcherConstraints(sketchView);
    Elements = new TaskSketcherElements(sketchView);
    Messages = new TaskSketcherMessages(sketchView);
    SolverAdvanced = new TaskSketcherSolverAdvanced(sketchView);

    ParameterGrp::handle hGrp = App::GetApplication().GetParameterGroupByPath(
        "User parameter:BaseApp/Preferences/Mod/Sketcher"
    );
    setEscapeButtonEnabled(hGrp->GetBool("LeaveSketchWithEscape", true));

    Content.push_back(ToolSettings);
    Content.push_back(Messages);

    if (hGrp->GetBool("ShowSolverAdvancedWidget", false)) {
        Content.push_back(SolverAdvanced);
    }

    Content.push_back(Constraints);
    Content.push_back(Elements);

    if (!hGrp->GetBool("ExpandedMessagesWidget", true)) {
        Messages->hideGroupBox();
    }
    if (!hGrp->GetBool("ExpandedSolverAdvancedWidget", false)) {
        SolverAdvanced->hideGroupBox();
    }
    if (!hGrp->GetBool("ExpandedConstraintsWidget", true)) {
        Constraints->hideGroupBox();
    }
    if (!hGrp->GetBool("ExpandedElementsWidget", true)) {
        Elements->hideGroupBox();
    }

    connectionToolSettings = sketchView->registerToolChanged(
        std::bind(&SketcherGui::TaskDlgEditSketch::slotToolChanged, this, sp::_1)
    );

    ToolSettings->setHidden(true);

    associateToObject3dView(sketchView->getObject());
}

TaskDlgEditSketch::~TaskDlgEditSketch()
{
    // to make sure to delete the advanced solver panel
    // it must be part to the 'Content' array
    if (const auto it = std::ranges::find(Content, SolverAdvanced); it == Content.end()) {
        Content.push_back(SolverAdvanced);
    }

    connectionToolSettings.disconnect();
}

void TaskDlgEditSketch::slotToolChanged(const std::string& toolname)
{
    if (toolname == "DSH_Symmetry" && symmetryPanelVisibility.empty()) {
        for (QWidget* panel : {static_cast<QWidget*>(Messages), static_cast<QWidget*>(Constraints),
                               static_cast<QWidget*>(Elements), static_cast<QWidget*>(SolverAdvanced)}) {
            symmetryPanelVisibility.emplace_back(panel, !panel->isHidden());
            panel->hide();
        }
    }
    else if (toolname != "DSH_Symmetry" && !symmetryPanelVisibility.empty()) {
        for (const auto& [panel, visible] : symmetryPanelVisibility) {
            panel->setVisible(visible);
        }
        symmetryPanelVisibility.clear();
    }
    bool widgetvisible = false;

    if (toolname != "DSH_None") {
        widgetvisible = sketchView->toolManager.isWidgetVisible();

        ToolSettings->toolChanged(toolname);
    }

    ToolSettings->setHidden(!widgetvisible);
    // Deactivation notifies before clearing the handler. DSH_None can also be
    // an active constraint tool without a settings widget, so inspect the mode
    // after the transition, with this dialog guarding the queued callback.
    QTimer::singleShot(0, this, &TaskDlgEditSketch::updateCancelButton);
}

void TaskDlgEditSketch::modifyStandardButtons(QDialogButtonBox* box)
{
    if (auto* close = box->button(QDialogButtonBox::Close)) {
        close->setText(tr("Exit Sketch"));
    }
    cancelButton = box->addButton(tr("Cancel"), QDialogButtonBox::ActionRole);
    cancelButton->setObjectName(QStringLiteral("SketchCancelAction"));
    cancelButton->setToolTip(tr("Cancel the current sketch action (Escape)"));
    connect(cancelButton, &QPushButton::clicked, this, &TaskDlgEditSketch::cancelCurrentAction);
    updateCancelButton();
}

void TaskDlgEditSketch::updateCancelButton()
{
    if (cancelButton) {
        cancelButton->setVisible(
            sketchView && sketchView->getSketchMode() == ViewProviderSketch::STATUS_SKETCH_UseHandler
        );
    }
}

void TaskDlgEditSketch::cancelCurrentAction()
{
    if (sketchView && sketchView->getSketchMode() == ViewProviderSketch::STATUS_SKETCH_UseHandler) {
        if (auto* document = Gui::Application::Instance->activeDocument()) {
            if (auto* view = document->getActiveView()) {
                view->setFocus();
            }
        }
        // Delegate one Escape pair to the native handler. Some drawing tools
        // reset an unfinished step and remain active; do not purge them here.
        sketchView->keyPressed(true, SoKeyboardEvent::ESCAPE);
        sketchView->keyPressed(false, SoKeyboardEvent::ESCAPE);
    }
    updateCancelButton();
}

//==== calls from the TaskView ===============================================================


void TaskDlgEditSketch::open()
{}

void TaskDlgEditSketch::clicked(int)
{}

bool TaskDlgEditSketch::accept()
{
    return true;
}

bool TaskDlgEditSketch::reject()
{
    ParameterGrp::handle hGrp = App::GetApplication().GetParameterGroupByPath(
        "User parameter:BaseApp/Preferences/Mod/Sketcher"
    );
    hGrp->SetBool("ExpandedMessagesWidget", Messages->isGroupVisible());
    hGrp->SetBool("ExpandedSolverAdvancedWidget", SolverAdvanced->isGroupVisible());
    hGrp->SetBool("ExpandedConstraintsWidget", Constraints->isGroupVisible());
    hGrp->SetBool("ExpandedElementsWidget", Elements->isGroupVisible());

    if (sketchView && sketchView->getSketchMode() != ViewProviderSketch::STATUS_NONE) {
        sketchView->purgeHandler();
    }

    std::string document = getDocumentName();  // needed because resetEdit() deletes this instance
    Gui::Command::doCommand(Gui::Command::Gui, "Gui.getDocument('%s').resetEdit()", document.c_str());
    Gui::Command::doCommand(Gui::Command::Doc, "App.getDocument('%s').recompute()", document.c_str());

    return true;
}

QDialogButtonBox::StandardButtons TaskDlgEditSketch::getStandardButtons() const
{
    return QDialogButtonBox::Close;
}

void TaskDlgEditSketch::autoClosedOnClosedView()
{
    // Make sure the edit mode is exited when the view is closed.
    reject();
}

#include "moc_TaskDlgEditSketch.cpp"
