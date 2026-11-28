# SPDX-License-Identifier: LGPL-2.1-or-later
import os
import unittest
from pathlib import Path
import FreeCAD as App, FreeCADGui as Gui, Part
from pivy import coin
from freecad_plus import appearance_task, appearance_highlight as highlight, panel, document
from TestAppearance import TestAppearance, colors, settle


class TestAppearanceEdges(unittest.TestCase):
    setUp = TestAppearance.setUp
    tearDown = TestAppearance.tearDown

    def test_boundaries_use_actual_edges_and_contrast_not_triangle_lines(self):
        face = Part.makePlane(30,20).cut(Part.Face(Part.Wire(Part.makeCircle(3,App.Vector(10,10,0)))))
        face = face.Faces[0]
        for color, expected in ((0xff8000ff,(0.,0.,0.)),(0x001144ff,(1.,1.,1.))):
            node = highlight.outline(face,color)
            depth = node.getChild(0)
            self.assertTrue(depth.test.getValue());self.assertFalse(depth.getField('write').getValue())
            material = node.getChild(1)
            self.assertEqual(tuple(material.diffuseColor[0].getValue()),expected)
            lines = node.getChild(node.getNumChildren()-1)
            self.assertEqual(lines.getTypeId(),coin.SoLineSet.getClassTypeId())
            self.assertEqual(len(lines.numVertices.getValues()),len(face.Edges))

    def test_highlights_preferences_cleanup_and_materials_unchanged(self):
        prefs = App.ParamGet('User parameter:BaseApp/Preferences/View')
        saved = highlight.preferences()
        self.box.Visibility=False;self.lid.Visibility=False
        with document.transaction(self.doc,'Highlight fixture'):
            plate=self.owner.newObject('Part::Feature','Plate')
            shape=Part.makeBox(70,48,10)
            for x,y in ((12,12),(58,12),(12,36),(58,36)):
                shape=shape.cut(Part.makeCylinder(4.5,10,App.Vector(x,y,0)))
            plate.Shape=shape
        self.box=plate
        face='Face'+str(max(range(len(plate.Shape.Faces)),key=lambda i:plate.Shape.Faces[i].CenterOfMass.z)+1)
        before = colors(self.box);undo = self.doc.UndoCount
        try:
            prefs.SetBool('EnableSelection',True);prefs.SetBool('EnablePreselection',True)
            prefs.SetUnsigned('SelectionColor',0xff8000ff);prefs.SetUnsigned('HighlightColor',0xff8000ff)
            task = appearance_task.open_task(self.owner,((panel.identity(self.box),face),))
            task.refresh_highlights();node = task.highlights.node
            self.assertEqual(str(node.getChild(node.getNumChildren()-1).getName()),'FreeCADPlusAppearanceBoundary')
            view = Gui.activeDocument().activeView();view.setAnimationEnabled(False);view.viewAxonometric();view.fitAll();settle()
            view.saveImage(str(Path(os.environ['PLUS_TEST_DIR'])/'appearance-selected-edges.png'),800,650,'Current')
            task.form.clear_targets();task.setPreselection(self.doc.Name,self.box.Name,face);settle()
            view.saveImage(str(Path(os.environ['PLUS_TEST_DIR'])/'appearance-hover-edges.png'),800,650,'Current')
            self.assertIsNotNone(task.highlights.node)
            prefs.SetBool('EnablePreselection',False);task.check_preferences()
            self.assertIsNone(task.highlights.node)
            task.reject();self.assertEqual(colors(self.box),before);self.assertEqual(self.doc.UndoCount,undo)
            self.assertEqual(view.getSceneGraph().findChild(node),-1)
        finally:
            prefs.SetBool('EnableSelection',saved[0]);prefs.SetUnsigned('SelectionColor',saved[1])
            prefs.SetBool('EnablePreselection',saved[2]);prefs.SetUnsigned('HighlightColor',saved[3])
