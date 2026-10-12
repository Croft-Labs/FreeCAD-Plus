# SPDX-License-Identifier: LGPL-2.1-or-later
"""Contextual fading checked against actual normal-framebuffer pixels."""
import ctypes
import json
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtGui, QtWidgets, QtOpenGLWidgets, QtTest
from freecad_plus import document, display, editing, hierarchy, panel, isolation
import TestComponentPanel as fixtures
from TestUnusedModels import visibility


def capture(view, output, *, prepare=True):
    widget=view.graphicsView().viewport()
    if prepare:
        main=Gui.getMainWindow();area=main.findChild(QtWidgets.QMdiArea)
        window=next(w for w in area.subWindowList() if w.isAncestorOf(view.graphicsView()))
        area.setActiveSubWindow(window);window.showMaximized()
        main.showNormal();main.raise_();main.activateWindow()
        Gui.Selection.clearSelection()
        widget=view.graphicsView().viewport()
        QtTest.QTest.mouseMove(widget,QtCore.QPoint(5,5))
    QtTest.QTest.qWait(150);view.redraw();QtTest.QTest.qWait(150)
    assert isinstance(widget,QtOpenGLWidgets.QOpenGLWidget)
    previous=QtGui.QOpenGLContext.currentContext()
    surface=previous.surface() if previous else None
    widget.makeCurrent();gl=ctypes.WinDLL('opengl32')
    def integer(key):
        value=ctypes.c_int();gl.glGetIntegerv(key,ctypes.byref(value));return value.value
    keys=(0x0D05,0x0D02,0x0D03,0x0D04)
    saved={key:integer(key) for key in keys};read=integer(0x0C02)
    ratio=widget.devicePixelRatioF();width=round(widget.width()*ratio);height=round(widget.height()*ratio)
    try:
        assert integer(0x8CA6)==widget.defaultFramebufferObject()
        assert integer(0x8CAA)==widget.defaultFramebufferObject()
        for key in keys:gl.glPixelStorei(key,1 if key==0x0D05 else 0)
        gl.glReadBuffer(0x8CE0)
        pixels=(ctypes.c_ubyte*(width*height*4))()
        gl.glReadPixels(0,0,width,height,0x1908,0x1401,pixels)
        assert gl.glGetError()==0
        image=QtGui.QImage(bytes(pixels),width,height,width*4,QtGui.QImage.Format_RGBA8888).copy().mirrored(False,True)
        assert image.save(str(output))
        return image,ratio
    finally:
        for key,value in saved.items():gl.glPixelStorei(key,value)
        gl.glReadBuffer(read)
        if previous and surface:
            previous.makeCurrent(surface)
        else:
            widget.doneCurrent()


def sample(view,frame,x):
    image,ratio=frame;point=view.getPointOnScreen(App.Vector(x,0,8))
    # FreeCAD returns physical viewport pixels; do not apply Qt scaling twice.
    px=round(point[0]);py=image.height()-1-round(point[1])
    color=image.pixelColor(px,py)
    return tuple(color.getRgb()[:3])


class TestComponentFading(unittest.TestCase):
    tearDown=fixtures.TestComponentPanel.tearDown
    rows=fixtures.TestComponentPanel.rows
    occurrence=fixtures.TestComponentPanel.occurrence

    def setUp(self):
        fixtures.TestComponentPanel.setUp(self)
        # Single faces make framebuffer opacity measurable without a back face.
        self.pad.ViewObject.Visibility=False
        self.face=self.doc.addObject('Part::Feature','OpacityFace')
        self.face.Shape=Part.makePlane(4,4,App.Vector(-2,-2,8))
        self.child.addObject(self.face)
        self.face.ViewObject.ShapeColor=(0.9,0.15,0.05)
        self.doc.recompute();editing.edit_file(self.doc);fixtures.settle()
        self.view=Gui.activeDocument().activeView()
        self.view.setAnimationEnabled(False);self.view.viewTop();self.view.fitAll()
        main=Gui.getMainWindow();main.hide();main.showNormal();QtTest.QTest.qWait(200)

    def frame(self,name,view=None):return capture(view or self.view,self.output/(name+'.png'))
    def near(self,actual,expected,tolerance=4):
        self.assertLessEqual(max(abs(a-b) for a,b in zip(actual,expected)),tolerance,(actual,expected))
    def background(self):
        self.view.setComponentHiddenPaths(self.root,[self.first.Name+'.',self.second.Name+'.'])
        frame=self.frame('background');self.view.setComponentHiddenPaths();return frame

    def test_pixels_active_descendants_faded_other_and_file_restore(self):
        normal=self.frame('normal');background=self.background()
        baseline=[sample(self.view,normal,x) for x in (0,25)]
        bg=[sample(self.view,background,x) for x in (0,25)]
        self.assertGreater(max(abs(a-b) for a,b in zip(baseline[0],bg[0])),30)
        editing.edit((self.second,));fixtures.settle();faded=self.frame('second_active')
        self.near(sample(self.view,faded,25),baseline[1])
        self.near(sample(self.view,faded,0),tuple(.25*a+.75*b for a,b in zip(baseline[0],bg[0])))
        editing.edit((self.first,self.nested));fixtures.settle();swapped=self.frame('first_active')
        self.near(sample(self.view,swapped,0),baseline[0])
        self.near(sample(self.view,swapped,25),tuple(.25*a+.75*b for a,b in zip(baseline[1],bg[1])))
        editing.edit_file(self.doc);fixtures.settle();restored=self.frame('file_restored')
        for i,x in enumerate((0,25)):self.near(sample(self.view,restored,x),baseline[i])
        (self.output/'pixels.json').write_text(json.dumps({'normal':baseline,'background':bg,'faded':[sample(self.view,faded,x) for x in (0,25)]}))

    def test_independent_views_authored_transparency_and_cleanup(self):
        self.face.ViewObject.Transparency=90;fixtures.settle();normal=self.frame('authored90')
        editing.edit((self.second,));fixtures.settle();faded=self.frame('authored90_edit')
        for x in (0,25):self.near(sample(self.view,faded,x),sample(self.view,normal,x))
        self.face.ViewObject.Transparency=0;fixtures.settle()
        original=self.frame('second_context')
        other=self.widget.open_row(self.occurrence((self.first,)).data(0,panel._ROLE));fixtures.settle()
        other.setAnimationEnabled(False);other.setCamera(self.view.getCamera())
        other_frame=self.frame('first_context',other)
        self.assertGreater(max(abs(a-b) for a,b in zip(sample(other,other_frame,0),sample(self.view,original,0))),20)
        again=self.frame('original_context_again')
        for x in (0,25):self.near(sample(self.view,again,x),sample(self.view,original,x))
        area=Gui.getMainWindow().findChild(QtWidgets.QMdiArea)
        next(w for w in area.subWindowList() if w.isAncestorOf(other.graphicsView())).close();fixtures.settle()
        self.widget.close();fixtures.settle();restored=self.frame('panel_closed')
        self.assertGreater(max(abs(a-b) for a,b in zip(sample(self.view,restored,0),sample(self.view,original,0))),20)
        self.assertEqual(self.face.ViewObject.Transparency,0)

    def test_mixed_face_materials_keep_higher_transparency(self):
        self.face.Shape=Part.makeCompound([Part.makePlane(4,4,App.Vector(x-2,-2,8)) for x in (0,5)])
        self.doc.recompute()
        self.frame('mixed_geometry_ready')  # Native face bindings follow lazy tessellation.
        opaque=App.Material();opaque.DiffuseColor=(0.9,0.15,0.05);opaque.Transparency=0
        transparent=App.Material();transparent.DiffuseColor=(0.05,0.3,0.9);transparent.Transparency=0.9
        self.face.ViewObject.ShapeAppearance=[opaque,transparent]
        authored=[(tuple(m.DiffuseColor),m.Transparency) for m in self.face.ViewObject.ShapeAppearance]
        self.view.fitAll();fixtures.settle()
        normal=self.frame('mixed_normal');background=self.background()
        editing.edit((self.second,));fixtures.settle();faded=self.frame('mixed_edit')
        self.near(sample(self.view,faded,0),tuple(.25*a+.75*b for a,b in
                  zip(sample(self.view,normal,0),sample(self.view,background,0))))
        for x in (5,25,30):self.near(sample(self.view,faded,x),sample(self.view,normal,x))
        self.assertEqual([(tuple(m.DiffuseColor),m.Transparency) for m in self.face.ViewObject.ShapeAppearance],authored)

    def test_unavailable_draw_path_preserves_rows_and_recovers_without_polling(self):
        normal=self.frame('normal');background=self.background()
        baseline=[sample(self.view,normal,x) for x in (0,25)]
        bg=sample(self.view,background,0)
        editing.edit((self.second,self.nested));fixtures.settle()
        self.root.ViewObject.Visibility=False;fixtures.settle()
        self.assertFalse(self.view.setComponentFade(self.root,hierarchy.subname((self.second,self.nested))))
        self.widget.refresh()
        self.assertGreater(len(self.rows(0)),0)
        self.assertGreater(len(self.rows(1)),0)
        state=self.widget._state((self.doc,self.view))
        self.assertTrue(state['fade_pending'])
        self.frame('temporarily_hidden')
        fixtures.settle();self.widget.refresh_count=0
        self.frame('second_hidden_paint');fixtures.settle()
        self.assertEqual(self.widget.refresh_count,0)
        self.root.ViewObject.Visibility=True;fixtures.settle()
        restored=self.frame('native_path_restored')
        self.assertFalse(state['fade_pending'])
        self.near(sample(self.view,restored,25),baseline[1])
        self.near(sample(self.view,restored,0),tuple(.25*a+.75*b for a,b in zip(baseline[0],bg)))

    def test_identity_recompute_undo_hidden_unused_and_save(self):
        ids={o.Name:o.ID for o in self.doc.Objects};vis=visibility(self.doc)
        undo=self.doc.UndoCount;color=tuple(self.face.ViewObject.ShapeColor)
        editing.edit((self.second,));fixtures.settle()
        self.assertIsNotNone(self.view.getObjectInfoRay(App.Vector(.3,.2,20),App.Vector(0,0,-1)))
        with self.assertRaises(ValueError):self.view.setComponentFade(self.root,'Missing.')
        with document.transaction(self.doc,'Change native geometry'):self.pad.Length=7
        self.doc.recompute();fixtures.settle();self.doc.undo();self.doc.recompute();fixtures.settle()
        self.assertEqual(self.pad.Length.Value,5)
        display.set_state(self.root,self.first,shown=False);fixtures.settle()
        self.assertIsNone(self.view.getObjectInfoRay(App.Vector(.3,.2,20),App.Vector(0,0,-1)))
        self.widget.refresh_count=0;QtTest.QTest.qWait(250);self.assertEqual(self.widget.refresh_count,0)
        editing.edit_unused(self.doc,self.unused);fixtures.settle();self.assertIsNotNone(isolation.current(self.view))
        editing.edit_file(self.doc);fixtures.settle()
        self.assertEqual(ids,{o.Name:o.ID for o in self.doc.Objects});self.assertEqual(vis,visibility(self.doc))
        self.assertEqual(color,tuple(self.face.ViewObject.ShapeColor));self.assertEqual(self.face.ViewObject.Transparency,0)
        self.assertEqual(self.doc.UndoCount,undo+1)
        editing.edit((self.second,));fixtures.settle()
        document.save_document(self.doc,self.output/'Fading.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':ids,'visibility':vis,'face':self.face.Name,'color':color}))


def verify_fresh_process(output):
    folder=Path(output)/'test_identity_recompute_undo_hidden_unused_and_save'
    expected=json.loads((folder/'expected.json').read_text());doc=document.open_document(folder/'Fading.cadprt')
    try:
        assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
        assert visibility(doc)==expected['visibility']
        face=doc.getObject(expected['face']);assert face.ViewObject.Transparency==0
        # Native PropertyMaterialList persists colors as rounded 8-bit RGBA.
        actual=list(face.ViewObject.ShapeColor)
        assert len(actual)==len(expected['color'])
        assert max(abs(a-b) for a,b in zip(actual,expected['color'])) <= 0.5/255+1e-7, (actual,expected['color'])
        widget=panel.show_panel();editing.edit_file(doc);fixtures.settle();widget.close();fixtures.settle()
    finally:App.closeDocument(doc.Name)
