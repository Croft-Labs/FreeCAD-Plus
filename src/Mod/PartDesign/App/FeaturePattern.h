// SPDX-License-Identifier: LGPL-2.1-or-later

#pragma once

#include "FeatureMultiTransform.h"

namespace PartDesign
{

/** One editable pattern, retaining independent linear and circular parameters.
 * Reuses the existing transformation engines without replacing the result object
 * (and therefore without breaking downstream references when its type changes).
 */
class PartDesignExport Pattern: public MultiTransform
{
    PROPERTY_HEADER_WITH_OVERRIDE(PartDesign::Pattern);

public:
    Pattern();

    App::PropertyEnumeration PatternType;
    App::PropertyLinkList PatternSettings;

    Transformed* getActivePattern() const;
    App::DocumentObjectExecReturn* execute() override;
    App::DocumentObjectExecReturn* recomputePreview() override;
    void onDocumentRestored() override;

protected:
    void setupObject() override;
    void onChanged(const App::Property* prop) override;

private:
    void selectPattern();
};

}  // namespace PartDesign
