# SPDX-License-Identifier: LGPL-2.1-or-later
"""#6864: fixed stepover must not leave strips at region boundaries."""
import math
import unittest
import surface_generator


class TestLineCoverage(unittest.TestCase):
    def lines(self, polygons, step=3, angle=0, zigzag=False, reverse=False):
        points = [p for poly in polygons for p in poly]
        return surface_generator.generate_linear_pattern_cpp(
            min(p[0] for p in points), max(p[0] for p in points),
            min(p[1] for p in points), max(p[1] for p in points),
            step, angle, zigzag, reverse, polygons)

    def testNonIntegralWidthReachesBothEdges(self):
        poly = [[0, 0], [30, 0], [30, 20], [0, 20]]
        for step in (3, 2.6, 5):
            with self.subTest(step=step):
                lines = self.lines([poly], step)
                levels = sorted({round(p[1], 5) for line in lines for p in line})
                self.assertAlmostEqual(levels[0], 0, delta=0.001)
                self.assertAlmostEqual(levels[-1], 20, delta=0.001)
                self.assertLessEqual(max(b-a for a,b in zip(levels, levels[1:])), step+0.001)

    def testDisconnectedRegionsReachTheirOwnEdges(self):
        polys = [[[0, y], [30, y], [30, y+10], [0, y+10]] for y in (0, 20)]
        lines = self.lines(polys, 4)
        ys = [p[1] for line in lines for p in line]
        for edge in (0, 10, 20, 30):
            self.assertLess(min(abs(y-edge) for y in ys), 0.001)
        for line in lines:
            self.assertFalse(10.001 < line[0][1] < 19.999)

    def testRotatedAndReversedBoundaryCoverage(self):
        angle = math.radians(30)
        c, s = math.cos(angle), math.sin(angle)
        poly = [[x*c-y*s, x*s+y*c] for x,y in ((0,0),(30,0),(30,20),(0,20))]
        lines = self.lines([poly], angle=30, zigzag=True)
        levels = [-p[0]*s+p[1]*c for line in lines for p in line]
        self.assertAlmostEqual(min(levels), 0, delta=0.001)
        self.assertAlmostEqual(max(levels), 20, delta=0.001)
        self.assertEqual(self.lines([poly], angle=30, zigzag=True, reverse=True), list(reversed(lines)))

    def testAddedPassesRemainOutsideHole(self):
        outer = [[0, 0], [30, 0], [30, 20], [0, 20]]
        hole = [[10, 7], [20, 7], [20, 13], [10, 13]]
        lines = self.lines([outer, hole], 3)
        for line in lines:
            y = line[0][1]
            if 7 < y < 13:
                xs = sorted(p[0] for p in line)
                self.assertTrue(xs[-1] <= 10.005 or xs[0] >= 19.995)
