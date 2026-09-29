// SPDX-License-Identifier: LGPL-2.1-or-later

#include <App/Document.h>

#include "FeaturePattern.h"
#include "Body.h"
#include "FeatureLinearPattern.h"
#include "FeaturePolarPattern.h"

using namespace PartDesign;

PROPERTY_SOURCE(PartDesign::Pattern, PartDesign::MultiTransform)

Pattern::Pattern()
{
    static const char* types[] = {"Linear", "Circular", nullptr};
    ADD_PROPERTY(PatternType, (0L));
    PatternType.setEnums(types);
    ADD_PROPERTY_TYPE(
        PatternSettings,
        (nullptr),
        "Pattern",
        App::Prop_Hidden,
        "The retained linear and circular pattern parameters"
    );
    PatternSettings.setSize(0);
    Transformations.setStatus(App::Property::Hidden, true);
    Transformations.setStatus(App::Property::ReadOnly, true);
}

void Pattern::setupObject()
{
    MultiTransform::setupObject();
    auto* doc = getDocument();
    auto* linear = static_cast<LinearPattern*>(
        doc->addObject("PartDesign::LinearPattern", "LinearPatternSettings")
    );
    auto* circular = static_cast<PolarPattern*>(
        doc->addObject("PartDesign::PolarPattern", "CircularPatternSettings")
    );
    linear->Length.setValue(100);
    linear->Occurrences.setValue(2);
    circular->Occurrences.setValue(2);
    linear->Visibility.setValue(false);
    circular->Visibility.setValue(false);
    PatternSettings.setValues({linear, circular});
}

Transformed* Pattern::getActivePattern() const
{
    const auto& settings = PatternSettings.getValues();
    const auto index = static_cast<std::size_t>(PatternType.getValue());
    if (index >= settings.size()) {
        return nullptr;
    }
    auto* setting = settings[index];
    if ((index == 0 && !freecad_cast<LinearPattern*>(setting))
        || (index == 1 && !freecad_cast<PolarPattern*>(setting))) {
        return nullptr;
    }
    return freecad_cast<Transformed*>(setting);
}

App::DocumentObjectExecReturn* Pattern::execute()
{
    if (TransformMode.getValue() == static_cast<long>(Transformed::Mode::Features)
        && Originals.getValues().empty()) {
        Shape.setValue(TopoDS_Shape());
        return new App::DocumentObjectExecReturn("Select at least one feature to pattern");
    }
    if (!getActivePattern()) {
        return new App::DocumentObjectExecReturn("Pattern settings are missing or invalid");
    }
    return MultiTransform::execute();
}

App::DocumentObjectExecReturn* Pattern::recomputePreview()
{
    if (TransformMode.getValue() == static_cast<long>(Transformed::Mode::Features)
        && Originals.getValues().empty()) {
        PreviewShape.setValue(TopoDS_Shape());
        return App::DocumentObject::StdReturn;
    }
    return MultiTransform::recomputePreview();
}

void Pattern::selectPattern()
{
    auto* active = getActivePattern();
    const std::vector<App::DocumentObject*> selected = active
        ? std::vector<App::DocumentObject*> {active}
        : std::vector<App::DocumentObject*> {};
    if (Transformations.getValues() != selected) {
        Transformations.setValues(selected);
    }
}

void Pattern::onChanged(const App::Property* prop)
{
    MultiTransform::onChanged(prop);
    if (prop == &_Body && !isRestoring() && getDocument()
        && !getDocument()->isPerformingTransaction()) {
        if (auto* body = getFeatureBody()) {
            for (auto* setting : PatternSettings.getValues()) {
                if (setting && !body->hasObject(setting)) {
                    body->insertObject(setting, this, false);
                }
            }
        }
    }
    if ((prop == &PatternType || prop == &PatternSettings) && !isRestoring() && getDocument()
        && !getDocument()->isPerformingTransaction()) {
        selectPattern();
    }
}

void Pattern::onDocumentRestored()
{
    MultiTransform::onDocumentRestored();
    selectPattern();
}
