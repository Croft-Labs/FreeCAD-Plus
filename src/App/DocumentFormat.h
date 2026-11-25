// SPDX-License-Identifier: LGPL-2.1-or-later
#pragma once

#include <string>
#include <boost/algorithm/string/predicate.hpp>
#include <App/Document.h>
#include <App/DocumentObject.h>
#include <App/PropertyStandard.h>

namespace App {
// Format belongs to document content, independently of the selected UI mode.
inline bool isComponentDocument(const Document& doc)
{
    for (const auto obj : doc.getObjects()) {
        const auto prop = dynamic_cast<const PropertyString*>(obj->getPropertyByName("PlusFormat"));
        if (prop && std::string(prop->getValue()) == "FreeCADPlus.ComponentDocument") {
            return true;
        }
    }
    return false;
}

inline std::string nativeDocumentFileName(const Document& doc, std::string name)
{
    const std::string extension = isComponentDocument(doc) ? ".cadprt" : ".FCStd";
    const auto dot = name.find_last_of('.');
    const auto slash = name.find_last_of("/\\");
    if (dot != std::string::npos && (slash == std::string::npos || dot > slash)) {
        const auto suffix = name.substr(dot);
        if (boost::iequals(suffix, extension)) {
            return name;
        }
        // Replace the other native format, never produce .FCStd.cadprt or vice versa.
        if (boost::iequals(suffix, ".cadprt") || boost::iequals(suffix, ".FCStd") || suffix == ".") {
            name.resize(dot);
        }
    }
    return name + extension;
}
}
