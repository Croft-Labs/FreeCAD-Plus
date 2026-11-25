import os,unittest,json,struct,winreg
from pathlib import Path
import FreeCAD as App,FreeCADGui as Gui
from PySide6 import QtCore,QtGui,QtWidgets,QtTest
from freecad_plus import document,panel,component_add
ROOT=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')

def green(icon,size=48):
    assert not icon.isNull()
    image=icon.pixmap(size,size).toImage()
    points=[]
    for y in range(image.height()):
        for x in range(image.width()):
            c=image.pixelColor(x,y)
            if c.alpha()>100 and c.green()>c.red()*1.6 and c.green()>c.blue()*1.3:points.append((x,y))
    return points,image

class TestPlusIcon(unittest.TestCase):
    def setUp(self):
        self.out=Path(os.environ['PLUS_TEST_DIR']);self.before=set(App.listDocuments())
    def tearDown(self):
        for name in set(App.listDocuments())-self.before:App.closeDocument(name)
    def assertPlus(self,icon):
        points,image=green(icon);self.assertGreater(len(points),20)
        self.assertTrue(all(x>=image.width()/2 and y>=image.height()/2 for x,y in points))
    def test_assets_executable_window_and_shell(self):
        self.assertEqual(App.ConfigGet('AppIcon'),'freecad-plus')
        expected=Gui.getIcon(':/icons/freecad-plus.svg');self.assertPlus(expected)
        appicon=QtWidgets.QApplication.windowIcon();self.assertPlus(appicon)
        self.assertPlus(Gui.getMainWindow().windowIcon())
        iconpath=ROOT/'app/bin/FreeCADPlus.ico';ico=QtGui.QIcon(str(iconpath));self.assertPlus(ico)
        contents=iconpath.read_bytes();self.assertEqual(struct.unpack_from('<HHH',contents),(0,1,10))
        for size in (16,20,24,32,40,48,64,96,128,256):self.assertFalse(ico.pixmap(size,size).isNull())
        provider=QtWidgets.QFileIconProvider()
        executable=provider.icon(QtCore.QFileInfo(str(ROOT/'app/bin/FreeCAD.exe')));self.assertPlus(executable)
        self.assertPlus(provider.icon(QtCore.QFileInfo('C:/Users/dgium/Desktop/freecad plus 0.1.0.lnk')))
        plus=document.new_document('IconPart');document.save_document(plus,self.out/'Bracket.cadprt')
        classic=App.newDocument('ClassicIcon');classic.saveAs(str(self.out/'Classic.FCStd'))
        shell=provider.icon(QtCore.QFileInfo(str(self.out/'Bracket.cadprt')));self.assertPlus(shell)
        old=provider.icon(QtCore.QFileInfo(str(self.out/'Classic.FCStd')));self.assertEqual(len(green(old)[0]),0)
        self.assertEqual(len(green(Gui.getIcon(':/icons/freecad.svg'))[0]),0)
        # Capture icons supplied by the real application and Windows provider.
        widget=QtWidgets.QGroupBox();widget.setWindowTitle('Installed icon verification');layout=QtWidgets.QHBoxLayout(widget)
        for title,icon in [('App window',appicon),('Executable',executable),('.cadprt file',shell),('Classic .FCStd',old)]:
            column=QtWidgets.QVBoxLayout();label=QtWidgets.QLabel();label.setPixmap(icon.pixmap(96,96));label.setAlignment(QtCore.Qt.AlignCenter)
            column.addWidget(label);caption=QtWidgets.QLabel(title);caption.setAlignment(QtCore.Qt.AlignCenter);column.addWidget(caption);layout.addLayout(column)
        widget.resize(620,160);widget.show();QtTest.QTest.qWait(120);widget.grab().save(str(self.out/'installed-icons.png'));widget.close();widget.deleteLater()
    def test_actual_open_dialog_provider_and_catalog_icon(self):
        App.ParamGet('User parameter:BaseApp/Preferences/Dialog').SetBool('DontUseNativeDialog',True)
        doc=document.new_document('FileIcons');document.save_document(doc,self.out/'FileIcons.cadprt')
        outcome=[]
        def inspect():
            dialog=QtWidgets.QApplication.activeModalWidget()
            try:
                self.assertIsInstance(dialog,QtWidgets.QFileDialog)
                provider=dialog.iconProvider()
                self.assertPlus(provider.icon(QtCore.QFileInfo(str(self.out/'FileIcons.cadprt'))))
                self.assertPlus(provider.icon(QtCore.QFileInfo(str(self.out/'Upper.CADPRT'))))
                self.assertEqual(len(green(provider.icon(QtCore.QFileInfo(str(self.out/'Classic.FCStd'))))[0]),0)
                dialog.setDirectory(str(self.out));QtTest.QTest.qWait(150);dialog.grab().save(str(self.out/'open-file-icons.png'))
            except BaseException as error:outcome.append(error)
            finally:
                if dialog:dialog.reject()
        QtCore.QTimer.singleShot(200,inspect);Gui.runCommand('Std_Open')
        if outcome:raise outcome[0]
        library=document.new_document('IconLibrary');document.validate(library).Definitions[0].Label='Library part'
        document.save_document(library,self.out/'IconLibrary.cadprt')
        App.setActiveDocument(doc.Name);QtTest.QTest.qWait(80)
        picker=component_add.Picker(panel.show_panel())
        try:
            group=next(picker.choices.topLevelItem(i) for i in range(picker.choices.topLevelItemCount()) if picker.choices.topLevelItem(i).text(0)=='IconLibrary.cadprt')
            self.assertPlus(group.icon(0))
        finally:picker.reject();picker.deleteLater()
    def test_association_registration(self):
        def read(path):
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT,path) as key:return winreg.QueryValueEx(key,'')[0]
        self.assertEqual(read('.cadprt'),'FreeCADPlus.Document')
        self.assertIn('FreeCADPlus.ico',read('FreeCADPlus.Document\\DefaultIcon'))
        command=read('FreeCADPlus.Document\\shell\\open\\command')
        self.assertIn(str(ROOT/'app/bin/FreeCAD.exe').replace('/','\\'),command)
        self.assertIn('"%1"',command);self.assertIn('--single-instance',command)
        self.assertEqual(read('.FCStd'),'FreeCAD.Document')
        self.assertIn('Program Files\\FreeCAD 1.1.4',read('FreeCAD.Document\\DefaultIcon'))
        (self.out/'associations.json').write_text(json.dumps(dict(cadprt=read('.cadprt'),icon=read('FreeCADPlus.Document\\DefaultIcon'),command=command,classic=read('.FCStd'),classic_icon=read('FreeCAD.Document\\DefaultIcon')),indent=2))
