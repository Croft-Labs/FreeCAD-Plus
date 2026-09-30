# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *   Copyright (c) 2022 sliptonic <shopinthewoods@gmail.com>               *
# *   Copyright (c) 2022-2025 Larry Woestman <LarryWoestman2@gmail.com>     *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

import FreeCAD

import Path
import CAMTests.PathTestUtils as PathTestUtils
from Path.Post.Processor import PostProcessorFactory
import Path.Dressup.Utils as PathDressup

Path.Log.setLevel(Path.Log.Level.DEBUG, Path.Log.thisModule())
Path.Log.trackModule(Path.Log.thisModule())


class TestDressupPost(PathTestUtils.PathTestBase):
    """Test the test_post.py postprocessor command line arguments."""

    @classmethod
    def setUpClass(cls):
        """setUpClass()...

        This method is called upon instantiation of this test class.  Add code
        and objects here that are needed for the duration of the test() methods
        in this class.  In other words, set up the 'global' test environment
        here; use the `setUp()` method to set up a 'local' test environment.
        This method does not have access to the class `self` reference, but it
        is able to call static methods within this same class.
        """
        FreeCAD.ConfigSet("SuppressRecomputeRequiredDialog", "True")
        cls.doc = FreeCAD.open(FreeCAD.getHomePath() + "/Mod/CAM/CAMTests/dressuptest.FCStd")
        cls.job = cls.doc.getObject("Job")
        cls.post = PostProcessorFactory.get_post_processor(cls.job, "test")

        # there are 4 operations in dressuptest.FCStd
        # every operation uses a different ToolController
        # each operation uses one more dressup to check nested dressups also work correctly

        cls.ops = cls.job.Operations.Group

    @classmethod
    def tearDownClass(cls):
        """tearDownClass()...

        This method is called prior to destruction of this test class.  Add
        code and objects here that cleanup the test environment after the
        test() methods in this class have been executed.  This method does
        not have access to the class `self` reference.  This method is able
        to call static methods within this same class.
        """
        FreeCAD.closeDocument(cls.doc.Name)
        FreeCAD.ConfigSet("SuppressRecomputeRequiredDialog", "")

    # Setup and tear down methods called before and after each unit test

    def setUp(self):
        """setUp()...

        This method is called prior to each `test()` method.  Add code and
        objects here that are needed for multiple `test()` methods.
        """
        # allow a full length "diff" if an error occurs
        self.maxDiff = None
        #
        # reinitialize the postprocessor data structures between tests
        #
        self.post.reinitialize()
        # Restored fixtures and edited operation properties must be recomputed
        # before exporting; cached paths are no longer accepted while dirty.
        self.doc.recompute()

    def tearDown(self):
        """tearDown()...

        This method is called after each test() method. Add cleanup instructions here.
        Such cleanup instructions will likely undo those in the setUp() method.
        """
        pass

    def test001(self):
        # test handling of Active state in postprocessor and nested dressups

        self.post.values["OUTPUT_COMMENTS"] = True
        self.post.values["SHOW_OPERATION_LABELS"] = True

        # set all operations to Active = False

        for op in self.ops:
            PathDressup.baseOp(op).Active = False

        # check that none of the operations is in the output

        gcode = self.post.export()[0][1].splitlines()

        for op in self.ops:
            expected = "(Begin operation: " + op.Label + ")"
            self.assertNotIn(expected, gcode)

        # set all operations back to Active = True

        for op in self.ops:
            PathDressup.baseOp(op).Active = True

        self.doc.recompute()

        # check that all operations are in the output

        gcode = self.post.export()[0][1].splitlines()

        for op in self.ops:
            expected = "(Begin operation: " + op.Label + ")"
            self.assertIn(expected, gcode)

    def test002(self):
        # test handling of ToolController in postprocessor and nested dressups

        self.post.values["OUTPUT_TOOL_CHANGE"] = True

        gcode = self.post.export()[0][1].splitlines()

        self.assertIn("M6 T1", gcode)
        self.assertIn("M6 T2", gcode)
        self.assertIn("M6 T3", gcode)
        self.assertIn("M6 T4", gcode)

    def testModelRemovalClearsNestedPathsAndRecovers(self):
        model = self.job.Model
        operations = self.job.Proxy.allOperations()
        self.assertGreater(len(operations), len(self.ops))
        self.assertTrue(all(op.Path.Commands for op in operations))
        try:
            self.job.Model = None
            for op in operations:
                self.assertEqual(len(op.Path.Commands), 0, op.Label)
                if hasattr(op, "ModelDependencies"):
                    self.assertEqual(op.ModelDependencies, [])
            self.doc.recompute()
            self.assertTrue(all(not op.Path.Commands for op in operations))
            self.assertTrue(all("Invalid" not in op.State for op in operations))
        finally:
            self.job.Model = model
            self.doc.recompute()
        self.assertTrue(all(op.Path.Commands for op in operations))
        self.assertTrue(self.post.export())

    def testModelReplacementRebindsNestedOperations(self):
        previous = self.job.Model
        models = list(previous.Group)
        replacement = self.doc.addObject("App::DocumentObjectGroup", "ReplacementModel")
        try:
            self.job.Model = replacement
            for op in self.job.Proxy.allOperations():
                self.assertEqual(len(op.Path.Commands), 0, op.Label)
                if hasattr(op, "ModelDependencies"):
                    self.assertEqual(op.ModelDependencies, [replacement])
                    self.assertNotIn(previous, op.OutList)
            previous.Group = []
            replacement.Group = models
            self.doc.recompute()
            self.assertTrue(all(op.Path.Commands for op in self.job.Proxy.allOperations()))
            self.assertTrue(self.post.export())
        finally:
            replacement.Group = []
            previous.Group = models
            self.job.Model = previous
            self.doc.removeObject(replacement.Name)
            self.doc.recompute()

    def testLeadGenerationFailureClearsCachedPath(self):
        from unittest.mock import patch
        from Path.Dressup.Gui import LeadInOut

        dressup = next(op for op in self.job.Proxy.allOperations()
                       if isinstance(op.Proxy, LeadInOut.ObjectDressup))
        self.assertTrue(dressup.Path.Commands)
        with patch.object(LeadInOut.leadinout.LeadInOut, "generate",
                          side_effect=RuntimeError("Deliberate lead failure")):
            with self.assertRaisesRegex(RuntimeError, "Deliberate lead failure"):
                dressup.Proxy.execute(dressup)
        self.assertEqual(len(dressup.Path.Commands), 0)
        dressup.touch()
        self.doc.recompute()
        self.assertTrue(dressup.Path.Commands)

    def testDisabledLeadsCopyBaseWithoutGeneration(self):
        from unittest.mock import patch
        from Path.Dressup.Gui import LeadInOut
        from PathScripts import PathUtils

        dressup = next(op for op in self.job.Proxy.allOperations()
                       if isinstance(op.Proxy, LeadInOut.ObjectDressup))
        original = dressup.LeadIn, dressup.LeadOut
        try:
            dressup.LeadIn = False
            dressup.LeadOut = False
            with patch.object(LeadInOut.leadinout.LeadInOut, "generate",
                              side_effect=AssertionError("Disabled leads invoked generator")):
                dressup.Proxy.execute(dressup)
            self.assertEqual(dressup.Path.toGCode(),
                             PathUtils.getPathWithPlacement(dressup.Base).toGCode())
        finally:
            dressup.LeadIn, dressup.LeadOut = original
            self.doc.recompute()

    def test003(self):
        # test handling of CoolantMode in postprocessor and nested dressups

        self.post.values["ENABLE_COOLANT"] = True

        for op in self.ops:
            base = PathDressup.baseOp(op)
            base.CoolantMode = "Mist"
            self.doc.recompute()

            gcode = self.post.export()[0][1].splitlines()

            self.assertIn("M7", gcode)
            self.assertIn("M9", gcode)

            base.CoolantMode = "None"
