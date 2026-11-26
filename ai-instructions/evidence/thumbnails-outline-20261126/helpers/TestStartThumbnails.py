"""Exercise real Start-page models/delegates with isolated native documents."""
import hashlib
import os
from pathlib import Path
import unittest
import zipfile
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtGui, QtWidgets, QtTest
from freecad_plus import document

REPO = Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
ROOT = Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
IMAGE_ROLE = int(QtCore.Qt.UserRole) + 2
PATH_ROLE = int(QtCore.Qt.UserRole) + 10
THUMB = 'thumbnails/Thumbnail.png'

class TestStartThumbnails(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = Path(os.environ['PLUS_TEST_DIR'])
        App.ParamGet('User parameter:BaseApp/Preferences/Document').SetBool('SaveThumbnail', True)
        cls.paths = []
        for name, classic, color in [('Bracket.cadprt',False,(0.25,0.6,0.85)),
                                     ('Upper.CADPRT',False,(0.9,0.4,0.2)),
                                     ('Classic.FCStd',True,(0.3,0.75,0.4))]:
            doc = App.newDocument('ClassicPreview') if classic else document.new_document('PreviewPart')
            owner = doc if classic else document.validate(doc).Definitions[0]
            box = owner.addObject('Part::Box','Box') if classic else owner.newObject('Part::Box','Box')
            box.Length, box.Width, box.Height = 18, 12, 5
            box.ViewObject.ShapeColor = color
            doc.recompute(); Gui.activeDocument().activeView().viewAxonometric()
            Gui.activeDocument().activeView().fitAll(); Gui.updateGui(); QtTest.QTest.qWait(120)
            path = cls.out/name; doc.saveAs(str(path)); App.closeDocument(doc.Name)
            cls.paths.append(path)
        no_preview = cls.out/'Without preview.cadprt'
        with zipfile.ZipFile(cls.paths[0]) as source, zipfile.ZipFile(no_preview,'w') as target:
            for entry in source.infolist():
                if entry.filename != THUMB: target.writestr(entry,source.read(entry.filename))
        cls.paths.append(no_preview)
        macro = cls.out/'Example.FCMacro'; macro.write_text('# Thumbnail fallback fixture\n')
        cls.paths.append(macro)
        cls.hashes = {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in cls.paths}
        recent = App.ParamGet('User parameter:BaseApp/Preferences/RecentFiles')
        recent.SetInt('RecentFiles',len(cls.paths))
        for i,p in enumerate(cls.paths): recent.SetString('MRU'+str(i),str(p))
        start = App.ParamGet('User parameter:BaseApp/Preferences/Mod/Start')
        start.SetBool('FirstStart2024',False)
        start.SetString('f3d', str(cls.out/'deliberately-absent-f3d.exe'))
        import StartGui
        old = Gui.getMainWindow().findChild(QtWidgets.QWidget,'StartView')
        if old:
            old.close(); old.deleteLater()
            QtCore.QCoreApplication.sendPostedEvents(None,QtCore.QEvent.DeferredDelete)
        Gui.runCommand('Start_Start'); QtTest.QTest.qWait(500)
        cls.start = Gui.getMainWindow().findChild(QtWidgets.QWidget,'StartView')
        cls.view = next(v for v in cls.start.findChildren(QtWidgets.QListView)
                        if v.model() and 'RecentFilesModel' in v.model().metaObject().className())
        cls.model = cls.view.model()
        cls.start.grab().save(str(cls.out/'recent-files.png'))

    def test_01_plus_embedded_preview_bytes(self):
        self.assertEqual(self.model.rowCount(),len(self.paths))
        for row in (0,1):
            with self.subTest(extension=self.paths[row].suffix):
                with zipfile.ZipFile(self.paths[row]) as archive: expected = archive.read(THUMB)
                actual = bytes(self.model.index(row,0).data(IMAGE_ROLE) or b'')
                self.assertEqual(actual,expected)
                self.assertFalse(QtGui.QImage.fromData(actual).isNull())

    def test_02_classic_embedded_preview_unchanged(self):
        with zipfile.ZipFile(self.paths[2]) as archive: expected=archive.read(THUMB)
        self.assertEqual(bytes(self.model.index(2,0).data(IMAGE_ROLE)),expected)

    def test_03_missing_thumbnail_and_macro_fallback(self):
        for row in (3,4):
            self.assertFalse(self.model.index(row,0).data(IMAGE_ROLE))
            self.view.scrollTo(self.model.index(row,0)); QtTest.QTest.qWait(80)
            rect = self.view.visualRect(self.model.index(row,0))
            self.assertTrue(rect.isValid())
            image = self.view.viewport().grab(rect).toImage()
            colors = {image.pixelColor(x,y).rgba() for x in range(15,min(120,image.width()))
                      for y in range(15,min(120,image.height()))}
            self.assertGreater(len(colors),20,'Fallback icon must paint, not an empty card')

    def test_04_original_files_untouched(self):
        for path,digest in self.hashes.items():
            self.assertEqual(hashlib.sha256(Path(path).read_bytes()).hexdigest(),digest)
        for row,path in enumerate(self.paths):
            self.assertEqual(Path(self.model.index(row,0).data(PATH_ROLE)),path)

    def test_05_native_icon_matches_approved_svg(self):
        resource=QtCore.QFile(':/icons/freecad-plus.svg')
        self.assertTrue(resource.open(QtCore.QIODevice.ReadOnly))
        actual=bytes(resource.readAll()); resource.close()
        self.assertEqual(actual,(REPO/'src/Gui/Icons/freecad-plus.svg').read_bytes())
        self.assertIn(b'freecad-peripheral-outline',actual)
        expected=(REPO/'src/Main/icon.ico').read_bytes()
        self.assertEqual((ROOT/'app/bin/FreeCADPlus.ico').read_bytes(),expected)

    def test_06_recent_card_opens_native_plus(self):
        index=self.model.index(0,0)
        self.view.scrollTo(index); QtTest.QTest.qWait(100)
        QtTest.QTest.mouseClick(self.view.viewport(),QtCore.Qt.LeftButton,
                              QtCore.Qt.NoModifier,self.view.visualRect(index).center())
        QtTest.QTest.qWait(200)
        doc=App.activeDocument()
        self.assertIsNotNone(doc)
        self.assertEqual(Path(doc.FileName),self.paths[0])
        self.assertIsNotNone(document.validate(doc))
        App.closeDocument(doc.Name)

    @classmethod
    def tearDownClass(cls):
        cls.start.grab().save(str(cls.out/'recent-files.png'))
