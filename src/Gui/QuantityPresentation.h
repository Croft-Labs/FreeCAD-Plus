// SPDX-License-Identifier: LGPL-2.1-or-later
#pragma once

#include <algorithm>
#include <cmath>
#include <QLocale>
#include <QObject>
#include <QRegularExpression>
#include <App/Application.h>
#include <App/DocumentObject.h>
#include <App/ObjectIdentifier.h>
#include <App/PropertyStandard.h>
#include <Base/Quantity.h>
#include <Base/Exception.h>
#include <Base/UnitsApi.h>
#include <Base/UnitsSchema.h>

namespace Gui::QuantityPresentation {
// Presentation metadata never changes the physical quantity or its expression.
inline QString explicitUnit(const QString& text, const Base::Unit& expected)
{
    static const QRegularExpression pattern(QStringLiteral(
        R"(^\s*[+-]?(?:\d+(?:[.,]\d*)?|[.,]\d+)(?:[eE][+-]?\d+)?\s*([A-Za-zµ°'"][A-Za-z0-9µ°'"/*^ .-]*)\s*$)"));
    const auto match = pattern.match(text);
    if (match.hasMatch()) {
        try {
            auto unit = match.captured(1);
            auto q = Base::Quantity::parse((QStringLiteral("1 ") + unit).toStdString());
            if (q.getUnit() == expected && q.getValue() > 0 && !q.isDimensionless())
                return unit;
        } catch (const Base::Exception&) {}
    }
    return {};
}

inline int decimals(const Base::Quantity& value, const QString& unit)
{
    auto prefs = App::GetApplication().GetParameterGroupByPath("User parameter:BaseApp/Preferences/Units");
    int result = prefs->GetInt("Decimals", Base::UnitsApi::getDecimals());
    if (!unit.isEmpty()) {
        try {
            auto secondary = Base::UnitsApi::createSchema(prefs->GetInt("SecondarySchema", 3));
            double primaryFactor, secondaryFactor;
            std::string primaryUnit, secondaryUnit;
            value.getUserString(primaryFactor, primaryUnit);
            value.getUserString(secondary.get(), secondaryFactor, secondaryUnit);
            const double factor = Base::Quantity::parse((QStringLiteral("1 ") + unit).toStdString()).getValue();
            if (std::abs(factor-secondaryFactor) < 1e-12 && std::abs(factor-primaryFactor) > 1e-12)
                result = prefs->GetInt("SecondaryDecimals", 3);
        } catch (const Base::Exception&) {}
    }
    return std::clamp(result, 0, 16);
}

inline QString format(const Base::Quantity& value, QString unit, bool editing,
                      double& factor, QString& actualUnit, Base::UnitsSchema* schema = nullptr)
{
    std::string nativeUnit;
    if (schema) value.getUserString(schema, factor, nativeUnit);
    else value.getUserString(factor, nativeUnit);
    if (!unit.isEmpty()) {
        try {
            const auto q = Base::Quantity::parse((QStringLiteral("1 ") + unit).toStdString());
            if (q.getUnit() == value.getUnit()) factor = q.getValue();
            else unit.clear();
        } catch (const Base::Exception&) { unit.clear(); }
    }
    actualUnit = unit.isEmpty() ? QString::fromStdString(nativeUnit) : unit;
    const int places = decimals(value, unit);
    const double number = value.getValue()/factor;
    QLocale locale;
    locale.setNumberOptions(locale.numberOptions() | QLocale::OmitGroupSeparator);
    QString result = locale.toString(number, 'f', editing ? std::max(6, places) : places);
    if (editing) {
        // Six fractional places for normal input; retain older/more precise data.
        if (std::abs(locale.toDouble(result)-number) > std::max(1e-12, std::abs(number)*1e-15))
            result = locale.toString(number, 'g', 17);
        else {
            while (result.endsWith(QLatin1Char('0')) && result.size()-result.indexOf(locale.decimalPoint())-1 > places)
                result.chop(1);
            if (result.endsWith(locale.decimalPoint())) result.chop(1);
        }
    }
    return actualUnit.isEmpty() ? result : result + QLatin1Char(' ') + actualUnit;
}

inline std::string key(const App::ObjectIdentifier& path)
{
    return path.getPropertyName() + path.getSubPathStr();
}

inline QString display(const Base::Quantity& value, const std::string& unit)
{
    double factor;
    QString actualUnit;
    return format(value, QString::fromStdString(unit), false, factor, actualUnit);
}

inline void restore(QObject* editor, const App::ObjectIdentifier& path)
{
    if (auto obj = path.getDocumentObject()) {
        if (auto map = dynamic_cast<App::PropertyMap*>(obj->getPropertyByName("QuantityPresentationUnits"))) {
            auto it = map->getValues().find(key(path));
            if (it != map->getValues().end()) editor->setProperty("presentationUnit", QString::fromStdString(it->second));
        }
    }
}

inline void remember(QObject* editor, const App::ObjectIdentifier& path)
{
    const auto unit = editor->property("presentationUnit").toString();
    auto obj = path.getDocumentObject();
    // Sketch constraints own their metadata so reindexing/deletion is safe.
    if (!obj || unit.isEmpty() || !editor->property("presentationEdited").toBool() || path.getPropertyName() == "Constraints") return;
    auto map = dynamic_cast<App::PropertyMap*>(obj->getPropertyByName("QuantityPresentationUnits"));
    if (!map) {
        map = dynamic_cast<App::PropertyMap*>(obj->addDynamicProperty("App::PropertyMap", "QuantityPresentationUnits", "Units", "Explicit presentation units"));
        if (map) map->setStatus(App::Property::Hidden, true);
    }
    if (map && (map->getValues().find(key(path)) == map->getValues().end() || (*map)[key(path)] != unit.toStdString()))
        map->setValue(key(path), unit.toStdString());
}
}
