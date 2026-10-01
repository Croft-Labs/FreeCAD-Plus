// SPDX-License-Identifier: LGPL-2.1-or-later

/****************************************************************************
 *                                                                          *
 *   Copyright (c) 2025 Pierre-Louis Boyer                                  *
 *                                                                          *
 *   This file is part of FreeCAD.                                          *
 *                                                                          *
 *   FreeCAD is free software: you can redistribute it and/or modify it     *
 *   under the terms of the GNU Lesser General Public License as            *
 *   published by the Free Software Foundation, either version 2.1 of the   *
 *   License, or (at your option) any later version.                        *
 *                                                                          *
 *   FreeCAD is distributed in the hope that it will be useful, but         *
 *   WITHOUT ANY WARRANTY; without even the implied warranty of             *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU       *
 *   Lesser General Public License for more details.                        *
 *                                                                          *
 *   You should have received a copy of the GNU Lesser General Public       *
 *   License along with FreeCAD. If not, see                                *
 *   <https://www.gnu.org/licenses/>.                                       *
 *                                                                          *
 ***************************************************************************/

#include <QVBoxLayout>
#include <QLabel>
#include <QPushButton>

#include <App/Application.h>
#include <App/Document.h>
#include <Gui/Selection/Selection.h>
#include <Gui/Application.h>
#include <Gui/BitmapFactory.h>
#include <Gui/Command.h>
#include <Mod/Assembly/App/AssemblyObject.h>
#include <Mod/Assembly/App/AssemblyUtils.h>

#include "TaskAssemblyMessages.h"
#include "ViewProviderAssembly.h"

using namespace AssemblyGui;
using namespace Gui::TaskView;
namespace sp = std::placeholders;

TaskAssemblyMessages::TaskAssemblyMessages(ViewProviderAssembly* vp)
    : TaskSolverMessages(Gui::BitmapFactory().pixmap("Geoassembly"), tr("Solver messages"))
    , vp(vp)
{
    freedomExplanation = new QLabel(this);
    freedomExplanation->setObjectName(QStringLiteral("assemblyFreedomExplanation"));
    freedomExplanation->setTextFormat(Qt::PlainText);
    freedomExplanation->setWordWrap(true);
    freedomExplanation->setTextInteractionFlags(Qt::TextSelectableByMouse);
    groupLayout()->addWidget(freedomExplanation);
    selectGrounded = new QPushButton(tr("Select grounded components"), this);
    selectGrounded->setObjectName(QStringLiteral("selectAssemblyGrounded"));
    selectGrounded->setToolTip(tr("Select components held by native grounding, read-only placement "
                                  "or a grounded rigid group. Does not add or remove joints."));
    groupLayout()->addWidget(selectGrounded);
    selectUnconnected = new QPushButton(tr("Select unconnected components"), this);
    selectUnconnected->setObjectName(QStringLiteral("selectAssemblyUnconnected"));
    selectUnconnected->setToolTip(tr("Select components without a joint path to ground. "
                                     "Connected sliders and hinges can still move."));
    groupLayout()->addWidget(selectUnconnected);
    connect(selectGrounded, &QPushButton::clicked, this, [this] { selectComponents(true); });
    connect(selectUnconnected, &QPushButton::clicked, this, [this] { selectComponents(false); });
    selectGrounded->setEnabled(false);
    selectUnconnected->setEnabled(false);
    // NOLINTBEGIN
    connectionSetUp = vp->signalSetUp.connect(
        std::bind(&TaskAssemblyMessages::showSolverState, this, sp::_1, sp::_2, sp::_3, sp::_4)
    );
    // NOLINTEND
}

void TaskAssemblyMessages::showSolverState(const QString& state, const QString& message,
                                           const QString& link, const QString& linkText)
{
    slotSetUp(state, message, link, linkText);
    const bool under = state == QStringLiteral("under_constrained");
    selectGrounded->setEnabled(state != QStringLiteral("empty"));
    selectUnconnected->setEnabled(under);
    if (under) {
        freedomExplanation->setText(tr(
            "Remaining freedom can include connected sliders or hinges. The count is for the "
            "assembly, not each component. Unconnected selection only finds components without "
            "a joint path to ground; it does not find every movable component."));
    }
    else if (state == QStringLiteral("fully_constrained")) {
        freedomExplanation->setText(tr(
            "The last solve reports no remaining assembly freedom. Grounded components are held "
            "by native grounding, read-only placement or grounded rigid groups; connected "
            "components may instead be held by joints. Use Select Component Joints to inspect them."));
    }
    else if (state == QStringLiteral("empty")) {
        freedomExplanation->setText(tr("Add components and declare grounding before inspecting movement."));
    }
    else {
        freedomExplanation->setText(tr(
            "Resolve the solver issue above before interpreting movement. A failed or conflicting "
            "solve does not establish component freedom. Grounded selection shows the native "
            "grounding relationship only; it does not certify a successful solve."));
    }
}

void TaskAssemblyMessages::selectComponents(bool grounded)
{
    auto* assembly = vp->getObject<Assembly::AssemblyObject>();
    if (App::GetApplication().getActiveDocument() != assembly->getDocument()
        || assembly->isTouched() || !assembly->isValid()) {
        freedomExplanation->setText(tr("Recompute the active assembly before selecting its current relationships."));
        return;
    }
    if (!grounded && (assembly->getLastSolverStatus() != 0 || assembly->getLastDoF() <= 0
        || assembly->getLastHasRedundancies() || assembly->getLastHasMalformedConstraints())) {
        return;
    }
    const auto groundedParts = assembly->getGroundedParts();
    std::vector<App::DocumentObject*> selected;
    for (auto* part : Assembly::getAssemblyComponents(assembly)) {
        if (!part || !part->isValid() || part->isTouched()) {
            freedomExplanation->setText(tr("A component is not current. Resolve its reference or recompute before selecting relationships."));
            return;
        }
        if (grounded ? groundedParts.count(part) != 0 : !assembly->isPartConnected(part)) {
            selected.push_back(part);
        }
    }
    Gui::Selection().clearSelection();
    for (auto* part : selected) {
        Gui::Selection().addSelection(part->getDocument()->getName(), part->getNameInDocument());
    }
}

TaskAssemblyMessages::~TaskAssemblyMessages()
{
    connectionSetUp.disconnect();
}

void TaskAssemblyMessages::updateToolTip(const QString& link)
{
    if (link == QStringLiteral("#conflicting")) {
        setLinkTooltip(tr("Selects these conflicting joints"));
    }
    else if (link == QStringLiteral("#redundant")) {
        setLinkTooltip(tr("Selects these redundant joints"));
    }
    else if (link == QStringLiteral("#dofs")) {
        setLinkTooltip(
            tr("The assembly has unconstrained components giving rise to those "
               "Degrees Of Freedom.\nSelects these unconstrained components.\nNote: Currently "
               "this selects only unconnected parts, not constrained parts that still have free "
               "DoF.")
        );
    }
    else if (link == QStringLiteral("#malformed")) {
        setLinkTooltip(tr("Selects these malformed joints"));
    }
}

void TaskAssemblyMessages::onLabelStatusLinkClicked(const QString& str)
{
    if (str == QStringLiteral("#conflicting")) {
        Gui::Application::Instance->commandManager().runCommandByName(
            "Assembly_SelectConflictingConstraints"
        );
    }
    else if (str == QStringLiteral("#redundant")) {
        Gui::Application::Instance->commandManager().runCommandByName(
            "Assembly_SelectRedundantConstraints"
        );
    }
    else if (str == QStringLiteral("#dofs")) {
        selectComponents(false);
    }
    else if (str == QStringLiteral("#malformed")) {
        Gui::Application::Instance->commandManager().runCommandByName(
            "Assembly_SelectMalformedConstraints"
        );
    }
}

#include "moc_TaskAssemblyMessages.cpp"
