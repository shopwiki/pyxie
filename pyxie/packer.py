#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Pyxie's image packing implementation.  Based on greedy algorithm described
in this stack overflow question:

http://stackoverflow.com/questions/1213394/algorithm-needed-for-packing-\
    rectangles-in-a-fairly-optimal-way

Start with the largest rectangle.  Add the next largest rectangle to the place
that extends the pack region as little as possible.  Repeat until you have
placed the smallest rectangle.
"""

class Rectangle(object):
    def __init__(self, x, y, data=None):
        self.x, self.y = x, y
        self.data = data

class Field(object):
    class PositionedRectangle(object):
        def __init__(self, x, y, rect):
            self.x, self.y, self.rect = x, y, rect
            self.bl, self.tr = None, None

    def __init__(self, x=0, y=0):
        self.x, self.y = x, y
        self.rectangles = []

    def area(self):
        return self.x * self.y

    def add_rectangle(self, rectangle):
        """Attempt to add a rectangle to this field increasing the packed area
        as little as possible.  To do this, it goes over all of the other
        rectangles, attempts to add to bottom left or top right corner, then
        checks for collisions.  If a position is found that does not create a
        collision and does not increase the area of the Field, it is used.
        Otherwise, the "optimal" solution found is used.  This is very time
        intensive, but we should never be dealing with a great deal of images."""
        if not self.rectangles:
            self.rectangles.append(PositionedRectangle(0, 0, rectangle))
        attempts = []
        for rect in self.rectangles:
            for placement in (self.bottom_left, self.top_right):
                result = placement(rect, rectangle)
                if res is 0:
                    placement(rect, rectangle, place=True)
                    return
                # if we didn't have a collision
                if res is not None:
                    attempts.append((result, placement, rect))
        attempts.sort()
        result, placement, rect = attempts[0]
        print "Area increasing from %d to %d" % (self.area(), result)
        placement(rect, rectangle, place=True)

    def bottom_left(self, placed, new, place=False):
        """Attempt to place a new rectangle on the bottom left corner of a
        previously placed rectangle.  Return the amt that the overall area of
        the field would increase, or None if a collision is detected."""

    def bottom_left(self, placed, new, place=False):
        pass

def autopack(*files):
    """Autopack a bunch of image files into a reasonably optimized Field."""
    pass


