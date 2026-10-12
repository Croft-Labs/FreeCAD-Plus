// SPDX-License-Identifier: LGPL-2.1-or-later
#ifndef GUI_PLUS_SELECTION_H
#define GUI_PLUS_SELECTION_H

#include <QVariant>
#include <Gui/MainWindow.h>

namespace Gui
{
// The separate Plus presentation sets this transient property only in Design.
// An absent property preserves the native Classic policy in every caller.
struct PlusSelectionPolicy
{
    bool enabled = false;
    bool directional = true;
    bool persistent = false;

    bool crossing(bool rightToLeft) const
    {
        return rightToLeft && (!enabled || directional);
    }
};

inline PlusSelectionPolicy plusSelectionPolicy()
{
    auto* window = getMainWindow();
    if (!window) {
        return {};
    }
    const auto value = window->property("FreeCADPlusDirectionalSelection");
    return {value.isValid(), value.isValid() ? value.toBool() : true,
            value.isValid() && window->property("FreeCADPlusPersistentSelection").toBool()};
}
}  // namespace Gui
#endif
