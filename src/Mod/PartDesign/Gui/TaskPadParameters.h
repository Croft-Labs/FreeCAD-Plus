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

#pragma once

#include <map>

#include "TaskExtrudeParameters.h"
#include "ViewProviderPad.h"

class QComboBox;
class QGroupBox;
class QLabel;
class QListWidget;
class QPushButton;

namespace App
{
class Property;
}

namespace Gui
{
class ViewProvider;
}

namespace PartDesignGui
{


class TaskPadParameters: public TaskExtrudeParameters
{
    Q_OBJECT

public:
    explicit TaskPadParameters(ViewProviderPad* PadView, QWidget* parent = nullptr, bool newObj = false);
    ~TaskPadParameters() override;

    void apply() override;
    void setSelectionMode(SelectionMode mode, Side side = Side::First) override;

protected:
    void onSelectionChanged(const Gui::SelectionChanges& msg) override;
    void changeEvent(QEvent* event) override;

private:
    void setupProfileSelection();
    void updateProfileList();
    void updateProfile(App::DocumentObject* object, const std::vector<std::string>& subNames);
    void removeSelectedProfileItems();
    void showProfileForSelection(App::DocumentObject* object);
    void restoreProfileVisibility();
    void translateProfileSelection();

    void onModeChanged(int index, Side side) override;
    void translateModeList(QComboBox* box, int index) override;
    void updateUI(Side side) override;

    QGroupBox* profileGroup = nullptr;
    QListWidget* profileList = nullptr;
    QLabel* profileHint = nullptr;
    QPushButton* selectProfile = nullptr;
    QPushButton* removeProfile = nullptr;
    QPushButton* clearProfile = nullptr;
    std::map<std::string, bool> profileVisibility;
};

/// simulation dialog for the TaskView
class TaskDlgPadParameters: public TaskDlgExtrudeParameters
{
    Q_OBJECT

public:
    explicit TaskDlgPadParameters(ViewProviderPad* PadView, bool newObj = false);

protected:
    TaskExtrudeParameters* getTaskParameters() override
    {
        return parameters;
    }

private:
    TaskPadParameters* parameters;
};

}  // namespace PartDesignGui
