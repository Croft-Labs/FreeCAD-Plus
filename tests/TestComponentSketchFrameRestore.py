# SPDX-License-Identifier: LGPL-2.1-or-later
"""Reopen persisted soft support in a separate application process."""
import os
from pathlib import Path
import unittest
import FreeCAD as App
import ComponentModel as Model

class TestComponentSketchFrameRestore(unittest.TestCase):
    def testColdRestoreFollowsThenSurvivesDeletion(self):
        fixture=Path(os.environ['FREECAD_PLUS_FRAME_FIXTURE'])
        doc=App.openDocument(str(fixture))
        try:
            doc.recompute()
            sk=next(obj for obj in doc.Objects if hasattr(obj,'FrameSupport'))
            source=sk.FrameSupport[0][0]
            before=App.Placement(sk.Placement)
            source.Placement.Base=source.Placement.Base+App.Vector(10,20,30)
            doc.recompute()
            self.assertTrue(sk.Placement.isSame(App.Placement(before.Base+App.Vector(10,20,30),before.Rotation),1e-7))
            saved=App.Placement(sk.Placement)
            doc.removeObject(source.Name);doc.recompute()
            self.assertTrue(sk.Placement.isSame(saved,1e-7))
            self.assertFalse(Model.current_shape(sk).isNull())
        finally:
            App.closeDocument(doc.Name)
