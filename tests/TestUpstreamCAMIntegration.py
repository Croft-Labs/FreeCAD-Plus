# SPDX-License-Identifier: LGPL-2.1-or-later
"""Source-overlay regressions for the October 7 upstream CAM integration.

Uses the existing fork's geometry engine; this does not validate rebuilt native
CAM, GUI, or Coin code. Run with tests/RunComponentDocument.ps1 -TestFiles
tests/TestUpstreamCAMIntegration.py and an isolated validation directory.
"""
import importlib.util
import os
from pathlib import Path
import sys
import types
import unittest

SOURCE = Path(__file__).resolve().parents[1]
CAM = SOURCE / "src/Mod/CAM"
sys.path.insert(0, str(CAM))
for name in list(sys.modules):
    if name in ("Path", "PathScripts", "CAMTests", "Machine") or name.startswith(
        ("Path.", "PathScripts.", "CAMTests.", "Machine.")
    ):
        del sys.modules[name]

# CAMTests.__init__ imports a CMake-generated test catalogue which is absent
# from the source tree. Load the selected helpers as a namespace instead.
cam_tests = types.ModuleType("CAMTests")
cam_tests.__path__ = [str(CAM / "CAMTests")]
sys.modules["CAMTests"] = cam_tests

from Path.Base import Util
from Path.Dressup import Utils


class TestSharedDressupResolver(unittest.TestCase):
    def testFrameLookupRejectsCycles(self):
        from types import SimpleNamespace
        proxy = type("Dressup", (), {"__module__": "Path.Dressup.Fixture"})()
        first = SimpleNamespace(Name="First", Proxy=proxy)
        second = SimpleNamespace(Name="Second", Proxy=proxy, Base=first)
        first.Base = second
        self.assertIs(Utils.baseOp, Util.baseOp)
        with self.assertRaisesRegex(ValueError, "Cyclic"):
            Util.workplaneForOp(first)

    def testDisconnectedBaseHasIdentityFrame(self):
        from types import SimpleNamespace
        proxy = type("Dressup", (), {"__module__": "Path.Dressup.Fixture"})()
        dressup = SimpleNamespace(Name="Detached", Proxy=proxy, Base=None)
        self.assertIsNone(Util.baseOp(dressup))
        self.assertTrue(Util.workplaneForOp(dressup).isIdentity())

    def testSourceModulesAreActuallyLoaded(self):
        self.assertTrue(Path(Util.__file__).resolve().is_relative_to(CAM))
        self.assertTrue(Path(Utils.__file__).resolve().is_relative_to(CAM))


def load_tests(loader, standard_tests, pattern):
    selected = os.environ.get("FREECAD_PLUS_UPSTREAM_CAM_NAMES", "")
    for relative in (
        "tests/TestCAMInvalidInputs.py",
        "tests/TestIssueSurfaceAvoidance.py",
        "src/Mod/CAM/CAMTests/TestPathWorkplaneFrame.py",
    ):
        path = SOURCE / relative
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if selected:
            names = [name for name in selected.split(",")
                     if hasattr(module, name.split(".")[0])]
            standard_tests.addTests(loader.loadTestsFromNames(names, module))
        else:
            standard_tests.addTests(loader.loadTestsFromModule(module))
    return standard_tests
