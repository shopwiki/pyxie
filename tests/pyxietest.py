#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""pyxie tests."""

from unittest import TestCase
from pyxie import packer

class LineTest(TestCase):
    def test_line_contains(self):
        """Test the line class & intersection detection."""
        Line, Point = packer.Line, packer.Point
        l1 = Line(Point(10, 10), Point(10, 50))
        l2 = Line(Point(10, 5), Point(32, 5))

        self.failUnless(l1.vertical)
        self.failUnless(not l2.vertical)

        # test middle intersections
        self.failUnless(Point(10, 30) in l1)
        self.failUnless(Point(25, 5) in l2)

        # test endpoint intersections
        self.failUnless(Point(10, 10) in l1)
        self.failUnless(Point(10, 50) in l1)
        self.failUnless(Point(10, 5) in l2)
        self.failUnless(Point(32, 5) in l2)

        # test non intersecting points at beginning & end of lines
        self.failUnless(Point(10, 9) not in l1)
        self.failUnless(Point(10, 51) not in l1)
        self.failUnless(Point(9, 5) not in l2)
        self.failUnless(Point(33, 5) not in l2)

        # test that weird lines are exceptions
        def skewed(p1, p2):
            return Line(p1, p2)

        self.assertRaises(Exception, skewed, (Point(10, 10), Point(20, 20)))
        self.assertRaises(Exception, skewed, (Point(10, 10), Point(10, 10)))

    def test_line_overlap(self):
        """Test that the line class correctly detects overlap."""
        Line, Point = packer.Line, packer.Point
        l1 = Line(Point(10, 10), Point(10, 30))
        l2 = Line(Point(20, 20), Point(80, 20))

        self.failUnless(l1.vertical)
        self.failUnless(not l2.vertical)

        self.failUnless(not l1.overlap(35, 50))
        self.failUnless(l1.overlap(5, 15)) # overlap
        self.failUnless(l1.overlap(5, 50)) # region contains line
        self.failUnless(l1.overlap(15, 25)) # line contains region

        self.failUnless(not l2.overlap(90, 95))
        self.failUnless(l2.overlap(15, 40)) # overlap
        self.failUnless(l2.overlap(15, 110)) # region contains line
        self.failUnless(l2.overlap(40, 65)) # line contains region


class PackerTest(TestCase):

    def test_packer_placement(self):
        # if these are from largest to smallest, we should mostly know the result
        rects = [packer.Rectangle(*args) for args in [
            (128, 64),
            (128, 32),
            (64, 64),
            (128, 16),
            (32, 32),
        ]]
        f = packer.Field()

        # add 128x64 to the top left:
        # +-------------+
        # |             | 128x64
        # +-------------+
        #
        f.add_rectangle(rects[0]) # 128, 64
        self.failUnless(f.area() == 8192)
        self.failUnless(f.x == 128)
        self.failUnless(f.y == 64)

        # add 128x32 to bottom left to make a 128x96 field:
        # +-------------+
        # |             | 128x64
        # +-------------+
        # +-------------+ 128x32
        #
        f.add_rectangle(rects[1]) # 128, 32
        self.failUnless(f.area() == 12288)
        self.failUnless(f.x == 128)
        self.failUnless(f.y == 96)

        # add 64x64 to top-right of 128x64 to increase to 192x96, < 128x160
        # +-------------+-------+
        # |  128x64     | 64x64 |
        # +-------------+-------+
        # +-------------+ 128x32
        #
        f.add_rectangle(rects[2]) # 64, 64
        self.failUnless(f.area() == (192*96))
        self.failUnless(f.x == 192)
        self.failUnless(f.y == 96)

        # add 128x16 to bottom-left of 128x32 to increase to 192x112, < 256x96
        # +-------------+-------+
        # |  128x64     | 64x64 |
        # +-------------+-------+
        # +-------------+ 128x32
        # +-------------+ 128x16
        #
        f.add_rectangle(rects[3]) # 128, 16
        self.failUnless(f.area() == (192*112))
        self.failUnless(f.x == 192)
        self.failUnless(f.y == 112)

        # finally, add 32x32 to the top-right of 128x32 (or bottom-left of 64x64)
        # +-------------+-------+
        # |  128x64     | 64x64 |
        # +-------------+---+---+
        # +-------------+---+ 32x32
        # +-------------+ 128x16
        #    128x32
        f.add_rectangle(rects[4]) # 32, 32
        self.failUnless(f.area() == (192*112))
        self.failUnless(f.x == 192)
        self.failUnless(f.y == 112)
        self.failUnless(len(f.rectangles) == len(rects))

    def test_vertical_run_detection(self):
        """Test the packer's ability to detect vertical runs;  when the addition
        of a rectangle to the top-right of one rectangle's corner actually blocks
        more than one rectangle's top-right corner."""
        rects = [packer.Rectangle(*args) for args in [
            (128, 64),
            (128, 32),
            (64, 96),
        ]]
        f = packer.Field()

        # add 128x64 to the top left:
        # +-------------+
        # |             | 128x64
        # +-------------+
        #
        f.add_rectangle(rects[0]) # 128, 64
        self.failUnless(f.area() == 8192)
        self.failUnless(f.x == 128)
        self.failUnless(f.y == 64)

        # add 128x32 to bottom left to make a 128x96 field:
        # +-------------+
        # |             | 128x64
        # +-------------+
        # +-------------+ 128x32
        #
        f.add_rectangle(rects[1]) # 128, 32
        self.failUnless(f.area() == 12288)
        self.failUnless(f.x == 128)
        self.failUnless(f.y == 96)

        # add 64x64 to top-right of 128x64 to increase to 192x96, < 128x160
        # +-------------+-------+
        # |  128x64     | 64x96 |
        # +-------------+       |
        # +-------------+-------+
        #    128x32
        f.add_rectangle(rects[2]) # 64, 96
        self.failUnless(f.area() == (192*96))
        self.failUnless(f.x == 192)
        self.failUnless(f.y == 96)

        # make sure that only 2 rectangles have tr set, and that it is
        # the first two we've added.
        has_top_right = [r for r in f.rectangles if r.tr]
        self.failUnless(len(has_top_right) == 2)
        self.failUnless(f.rectangles[0].tr)
        self.failUnless(f.rectangles[1].tr)

    def test_horizontal_run_detection(self):
        """Test the packer's ability to detect horizontal runs;  when the
        addition of a rectangle to the bottom-left of one rectangle's corner
        blocks more than one rectangle's bottom-left corner."""
        rects = [packer.Rectangle(*args) for args in [
            (128, 64),
            (64, 16),
            (32, 16),
            (32, 16),
            (128, 2),
        ]]
        f = packer.Field()

        # add 128x64 to the top left:
        # +-------------+
        # |             | 128x64
        # +-------------+
        #
        f.add_rectangle(rects[0]) # 128, 64
        self.failUnless(f.area() == 8192)
        self.failUnless(f.x == 128)
        self.failUnless(f.y == 64)

        # add 64x16 to bottom left to make a 128x80 field:
        # +-------------+
        # |             | 128x64
        # +-----+-------+
        # +-----+ 64x16
        #
        f.add_rectangle(rects[1]) # 64, 16
        self.failUnless(f.area() == (128 * 80))
        self.failUnless(f.x == 128)
        self.failUnless(f.y == 80)

        # add two 32x16 to fill out the bottom of 128x64
        # +-------------+
        # |             | 128x64
        # +-----+---+---+
        # +-----+---+---+ 64x16, 32x16, 32x16
        #
        f.add_rectangle(rects[2]) # 32, 32
        self.failUnless(f.area() == (128 * 80))
        self.failUnless(f.x == 128)
        self.failUnless(f.y == 80)

        f.add_rectangle(rects[3]) # 32, 32
        self.failUnless(f.area() == (128 * 80))
        self.failUnless(f.x == 128)
        self.failUnless(f.y == 80)

        # add the long 128x2 rectangle, which should go to the bottom-left of
        # the 64x64 rectangle and take up the bottom-left of rects 2,3 and 4
        # +-------------+
        # |             | 128x64
        # +-----+---+---+ 
        # +-----+---+---+ 64x16, 32x16, 32x16
        # +-------------+ 128x2
        f.add_rectangle(rects[4]) # 128, 2
        self.failUnless(f.area() == (128 * 82))
        self.failUnless(f.x == 128)
        self.failUnless(f.y == 82)

        has_free_bottom_left = [r for r in f.rectangles if not r.bl]
        self.failUnless(len(has_free_bottom_left) == 1)
        self.failUnless(f.rectangles[1].bl)
        self.failUnless(f.rectangles[2].bl)
        self.failUnless(f.rectangles[3].bl)

