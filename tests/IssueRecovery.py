# SPDX-License-Identifier: LGPL-2.1-or-later
"""Exercise real startup recovery using only generated, isolated test documents."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import time
import traceback
import xml.etree.ElementTree as ET
import zipfile

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]).resolve()
    cache = Path(App.ConfigGet("UserCachePath")).resolve()
    data = Path(App.getUserAppDataDir()).resolve()
    assert cache.is_relative_to(output) and data.is_relative_to(output), "Not isolated"
    doc = App.newDocument("RecoveryFixture")
    box = doc.addObject("Part::Box", "Box")
    box.Length, box.Width, box.Height = 11, 7, 3
    doc.recompute()
    template = output / "template.FCStd"
    doc.saveAs(str(template))
    App.closeDocument(doc.Name)
    with zipfile.ZipFile(template) as archive:
        contents = {name: archive.read(name) for name in archive.namelist()}
    assert "Document.xml" in contents and "GuiDocument.xml" in contents
    cases = []
    # A synthetic unlocked instance, recognized by the native recovery finder.
    instance = "issue18044fixture"
    executable = Path(App.ConfigGet("ExeName")).stem or "FreeCAD"
    (cache / f"{executable}_{instance}.lock").write_bytes(b"")
    for name in ("bad_zip", "bad_document_xml", "bad_gui_xml", "valid_newer", "valid_older"):
        folder = cache / f"{executable}_Doc_{name}_{instance}"
        folder.mkdir()
        recovery = folder / "fc_recovery_file.fcstd"
        shutil.copyfile(template, recovery)
        original = output / (name + ".FCStd")
        if name == "bad_zip":
            original.write_bytes(b"Truncated project fixture")
        else:
            entries = dict(contents)
            if name == "bad_document_xml":
                entries["Document.xml"] = b"<Document><broken>"
            elif name == "bad_gui_xml":
                entries["GuiDocument.xml"] = b"<GuiDocument><broken>"
            with zipfile.ZipFile(original, "w", zipfile.ZIP_DEFLATED) as archive:
                for entry, value in entries.items():
                    archive.writestr(entry, value)
        now = time.time()
        os.utime(recovery, (now - 60, now - 60))
        stamp = now - 120 if name == "valid_older" else now
        os.utime(original, (stamp, stamp))
        root = ET.Element("AutoRecovery", SchemaVersion="1")
        for key, value in (("Status", "Created"), ("Label", name), ("FileName", str(original))):
            ET.SubElement(root, key).text = value
        ET.ElementTree(root).write(folder / "fc_recovery_file.xml", encoding="utf-8", xml_declaration=True)
        cases.append({"name": name, "original": str(original), "sha256": digest(original),
                      "offered": name != "valid_newer"})
    (output / "fixtures.json").write_text(json.dumps(cases, indent=2), encoding="utf-8")
    module = data / "Mod" / "IssueRecoveryValidation"
    module.mkdir(parents=True)
    # This hook runs before the startup recovery dialog enters its modal loop.
    helper = Path(__file__).resolve()
    (module / "InitGui.py").write_text(
        "import os, runpy\n"
        "if os.environ.get('FREECAD_PLUS_RECOVERY_PHASE') == 'verify':\n"
        f"    runpy.run_path({str(helper)!r})['observe']()\n", encoding="utf-8")
    (output / "prepared.json").write_text(json.dumps({"cache": str(cache), "data": str(data),
        "executable": executable, "version": App.Version()}, indent=2), encoding="utf-8")
    QtCore.QTimer.singleShot(100, QtWidgets.QApplication.instance().quit)


def observe():
    output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
    Gui.getMainWindow().setAttribute(QtCore.Qt.WA_DontShowOnScreen, True)
    (output / "observer.started").write_text("Startup hook loaded", encoding="utf-8")
    cases = json.loads((output / "fixtures.json").read_text(encoding="utf-8"))
    report = {"version": App.Version(), "application": App.ConfigGet("AppHomePath"),
              "cases": cases, "passed": False}
    deadline = time.monotonic() + 90
    timer = QtCore.QTimer(Gui.getMainWindow())
    # Keep the Python wrapper/callback alive after the temporary startup namespace.
    Gui._issueRecoveryTimer = timer

    def finish(dialog=None):
        timer.stop()
        if dialog is not None:
            dialog.reject()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        (output / "recovery-results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        QtCore.QTimer.singleShot(100, QtWidgets.QApplication.instance().quit)

    def inspect():
        (output / "observer.tick").write_text("Timer active", encoding="utf-8")
        dialog = next((w for w in QtWidgets.QApplication.topLevelWidgets()
                       if "DocumentRecovery" in w.metaObject().className()), None)
        if dialog is None:
            if time.monotonic() > deadline:
                report["error"] = "Startup recovery dialog did not appear"
                report["windows"] = [(w.objectName(), w.metaObject().className())
                                     for w in QtWidgets.QApplication.topLevelWidgets()]
                finish()
            return
        timer.stop()
        try:
            tree = dialog.findChild(QtWidgets.QTreeWidget, "treeWidget")
            rows = [tree.topLevelItem(i).text(0) for i in range(tree.topLevelItemCount())]
            report["offered"] = sorted(rows)
            assert sorted(rows) == sorted(c["name"] for c in cases if c["offered"]), rows
            dialog.findChild(QtWidgets.QDialogButtonBox, "buttonBox").button(
                QtWidgets.QDialogButtonBox.Ok).click()
            report["statuses"] = [tree.topLevelItem(i).text(1) for i in range(tree.topLevelItemCount())]
            docs = list(App.listDocuments().values())
            assert len(docs) == 4, f"Expected four recovered documents, got {len(docs)}"
            report["volumes"] = [doc.getObject("Box").Shape.Volume for doc in docs]
            assert all(abs(v - 231) < 1e-7 for v in report["volumes"])
            for case in cases:
                assert digest(Path(case["original"])) == case["sha256"], "Original overwritten"
            report["passed"] = True
        except BaseException:
            report["error"] = traceback.format_exc()
        finally:
            finish(dialog)

    timer.timeout.connect(inspect)
    timer.start(100)
