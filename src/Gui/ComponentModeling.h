// SPDX-License-Identifier: LGPL-2.1-or-later
#ifndef GUI_COMPONENT_MODELING_H
#define GUI_COMPONENT_MODELING_H

#include <App/Document.h>
#include <App/DocumentObject.h>

namespace Gui
{
inline bool isComponentModelingDocument(App::Document* document)
{
    if (document) {
        for (auto object : document->getObjects()) {
            if (object->getPropertyByName("PlusFormat")) {
                return true;
            }
        }
    }
    return false;
}
}
#endif
