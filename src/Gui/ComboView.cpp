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

#include <QEvent>
#include <QGridLayout>

#include "ComboView.h"
#include "PropertyView.h"
#include "Tree.h"


using namespace Gui;
using namespace Gui::DockWnd;


/* TRANSLATOR Gui::DockWnd::ComboView */

ComboView::ComboView(Gui::Document* pcDocument, QWidget* parent)
    : DockWindow(pcDocument, parent)
{
    auto pLayout = new QGridLayout(this);
    pLayout->setSpacing(0);
    pLayout->setContentsMargins(0, 0, 0, 0);

    // Retain the native tree infrastructure for command integration, without a
    // second public hierarchy competing with the component occurrence navigator.
    tree = new TreePanel("ComboView", this);
    tree->hide();

    // property view
    prop = new PropertyView(this);
    pLayout->addWidget(prop, 0, 0);
}

ComboView::~ComboView() = default;

#include "moc_ComboView.cpp"
