"""Read-only check of the owner's recent files in a disposable app profile."""
import hashlib,json,os,unittest,xml.etree.ElementTree as ET,zipfile
from pathlib import Path
import FreeCAD as App,FreeCADGui as Gui
from PySide6 import QtCore,QtWidgets,QtTest
from TestStartThumbnails import ROOT,IMAGE_ROLE,THUMB

class TestOwnerPreviews(unittest.TestCase):
    def test_saved_previews_display_without_modifying_owner_files(self):
        profile=ROOT/'profiles/owner-test/user.cfg'
        profile_hash=hashlib.sha256(profile.read_bytes()).hexdigest()
        paths=[Path(n.text) for n in ET.parse(profile).findall(".//FCParamGroup[@Name='RecentFiles']/FCText")]
        self.assertEqual(len(paths),4)
        hashes={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        recent=App.ParamGet('User parameter:BaseApp/Preferences/RecentFiles')
        recent.SetInt('RecentFiles',len(paths))
        for i,p in enumerate(paths):recent.SetString('MRU'+str(i),str(p))
        import StartGui
        old=Gui.getMainWindow().findChild(QtWidgets.QWidget,'StartView')
        if old:
            old.close();old.deleteLater()
            QtCore.QCoreApplication.sendPostedEvents(None,QtCore.QEvent.DeferredDelete)
        Gui.runCommand('Start_Start');QtTest.QTest.qWait(350)
        start=Gui.getMainWindow().findChild(QtWidgets.QWidget,'StartView')
        view=next(v for v in start.findChildren(QtWidgets.QListView)
                  if v.model() and 'RecentFilesModel' in v.model().metaObject().className())
        self.assertEqual(view.model().rowCount(),4)
        for i,path in enumerate(paths):
            with zipfile.ZipFile(path) as archive:expected=archive.read(THUMB)
            self.assertEqual(bytes(view.model().index(i,0).data(IMAGE_ROLE)),expected)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),hashes[path])
        self.assertEqual(hashlib.sha256(profile.read_bytes()).hexdigest(),profile_hash)
        # Local-only screenshot; private owner filenames are not copied into Git evidence.
        start.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'owner-recent-files.png'))
        (Path(os.environ['PLUS_TEST_DIR'])/'owner-check.json').write_text(json.dumps(
            dict(recent_files=4,embedded_previews_match=True,files_unchanged=True,owner_profile_unchanged=True)))
