#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Pyxie's image packing implementation.  Based on greedy algorithm described
in this stack overflow question:

http://stackoverflow.com/questions/1213394/algorithm-needed-for-packing-\
    rectangles-in-a-fairly-optimal-way

Start with the largest rectangle.  Add the next largest rectangle to the place
that extends the pack region as little as possible.  Repeat until you have
placed the smallest rectangle.

The coordinate system used here has the origin (0, 0) at the top-left.
"""

__all__ = ['Rectangle', 'Field', 'VerticalField']

class Rectangle(object):
    def __init__(self, x, y, data=None):
        self.x, self.y = x, y
        self.data = data

    def __repr__(self):
        return '<Rectangle %d, %d>' % (self.x, self.y)

class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

class Line(object):
    """A very simplistic grid line class, where all lines are either vertical
    or horizontal."""
    def __init__(self, p1, p2):
        """Make sure that p1.x is the left-most top-most point in the line."""
        if p1.x == p2.x: # vertical
            self.vertical = True
            if p1.y < p2.y: self.p1, self.p2 = p1, p2
            else: self.p1, self.p2 = p2, p1
        elif p1.y == p2.y: # horizontal
            self.vertical = False
            if p1.x < p2.x: self.p1, self.p2 = p1, p2
            else: self.p1, self.p2 = p2, p1
        else:
            raise Exception("Line objects can only have horizontal or vertical lines.")

    def overlap(self, p1, p2):
        """Return True if there's any overlap between this line and _region_,
        which is assumed to be a span if we are horizontal and a range if are
        vertical.  There is overlap if any of the points of either line exists
        within the other line."""
        if self.vertical:
            y1, y2 = self.p1.y, self.p2.y
            return (p1 > y1 and p1 < y2) or (p2 > y1 and p2 < y2) or\
                    (y1 > p1 and y1 < p2) or (y2 > p1 and y2 < p2)
        x1, x2 = self.p1.x, self.p2.x
        return (p1 > x1 and p1 < x2) or (p2 > x1 and p2 < x2) or\
                (x1 > p1 and x1 < p2) or (x2 > p1 and x2 < p2)

    def __contains__(self, p):
        """Return whether or not this line contains a point p."""
        if self.vertical: # vertical line
            if p.x == self.p1.x and p.y >= self.p1.y and p.y <= self.p2.y:
                return True
            return False
        else:
            if p.y == self.p1.y and p.x >= self.p1.x and p.x <= self.p2.x:
                return True
            return False

    def __repr__(self):
        return '<Line (%d, %d) -> (%d, %d) %s >' % (self.p1.x, self.p1.y,
                self.p2.x, self.p2.y, '|' if self.vertical else '-')


class PositionedRectangle(object):
    """A rectangle positioned within a field.  Has the coordinates of the
    rectangle and whether or not there's another rectangle positioned at
    its top-right or bottom-left corner."""
    def __init__(self, x, y, rect):
        self.x, self.y, self.rect = x, y, rect
        self.bl, self.tr = None, None

    def __contains__(self, point):
        """This positioned rectangle contains point (x,y) if x is between
        the left-most x and the right-most x, and y is between the top-most
        y and bottoom-most y."""
        if (point.x > self.x) and (point.x < (self.x + self.rect.x)) and\
           (point.y > self.y) and (point.y < (self.y + self.rect.y)):
           return True
        return False

    def __repr__(self):
        return '<pRect @ (%d, %d), %dx%d (tr/bl: %r, %r)>' % (self.x, self.y,
                self.rect.x, self.rect.y, self.tr, self.bl)

class Field(object):
    def __init__(self):
        self.x, self.y = 0, 0
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
            self.x, self.y = self.calculate_bounds()
            return
        attempts = []
        for rect in self.rectangles:
            for placement in (self.bottom_left, self.top_right):
                result = placement(rect, rectangle)
                if result is 0:
                    placement(rect, rectangle, place=True)
                    return
                # if we didn't have a collision
                if result is not None:
                    attempts.append((result, -self.rectangles.index(rect), placement, rect))
        attempts.sort()
        if not attempts:
            import ipdb; ipdb.set_trace();
        result, blah, placement, rect = attempts[0]
        #print "Area increasing from %d to %d" % (self.area(), result)
        placement(rect, rectangle, place=True)
        self.x, self.y = self.calculate_bounds()

    def bottom_left(self, placed, new, place=False):
        """Attempt to place a new rectangle on the bottom left corner of a
        previously placed rectangle.  Return the amt that the overall area of
        the field would increase, or None if a collision is detected."""
        if place:
            self.mark_corners(placed.x, placed.y + placed.rect.y, new)
            self.rectangles.append(PositionedRectangle(placed.x, placed.y + placed.rect.y, new))
            self.x, self.y = self.calculate_bounds()
            return
        if placed.bl:
            return None
        # the corner we're adding it to is here:
        corner = (placed.x, placed.y + placed.rect.y)
        if not self.collision(corner, new):
            return self.new_area(corner, new)


    def top_right(self, placed, new, place=False):
        if place:
            self.mark_corners(placed.x + placed.rect.x, placed.y, new)
            self.rectangles.append(PositionedRectangle(placed.x + placed.rect.x, placed.y, new))
            self.x, self.y = self.calculate_bounds()
            return
        if placed.tr:
            return None
        corner = (placed.x + placed.rect.x, placed.y)
        if not self.collision(corner, new):
            return self.new_area(corner, new)

    def mark_corners(self, x, y, rect):
        """Find all of the rectangles whose top-right or bottom-left corner are
        "occupied" by the new rectangle, and mark them appropriately."""
        left = Line(Point(x, y), Point(x, y + rect.y))
        top = Line(Point(x, y), Point(x + rect.x, y))
        # print "Adding rectangle %r to %d, %d (t/l: %s, %s)" % (rect, x, y, top, left)
        # for every rectangle, if the top right or bottom left corners are in
        # these lines, mark them as blocked
        for pos in self.rectangles:
            if not pos.tr:
                p = Point(pos.x + pos.rect.x, pos.y)
                if p in top or p in left:
                    pos.tr = True
            if not pos.bl:
                p = Point(pos.x, pos.y + pos.rect.y)
                if p in top or p in left:
                    pos.bl = True
        return True


    def new_area(self, corner, new):
        """Return the new area of the field given a rectangle is positioned
        with its top left corner at `corner`."""
        if isinstance(corner, tuple):
            corner = Point(*corner)
        x, y = self.calculate_bounds(self.rectangles + [PositionedRectangle(corner.x, corner.y, new)])
        return x * y

    def calculate_bounds(self, rectangles=None):
        """Calculate x/y bounds for a field with the given rectangles.  If
        rectangles is None, calculate it for self's rectangles."""
        if rectangles is None:
            rectangles = self.rectangles
        def span(rectangles):
            # only rectangles without another positioned in the top right
            possibilities = [r for r in rectangles if not r.tr]
            return max([(r.x + r.rect.x) for r in possibilities])
        def range(rectangles):
            # only rectangles without another positioned in the bottom left
            possibilities = [r for r in rectangles if not r.bl]
            return max([(r.y + r.rect.y) for r in possibilities])
        return span(rectangles), range(rectangles)

    def collision(self, corner, new):
        def collide(rect, top, left):
            """If any of these lines intersect with any other rectangles, it's
            a collision."""
            # if the x components and y components of the rectangle overlap, then
            # the rectangles overlap;  if they don't, then they don't.

            # first, we need to check an edge case:
            # it's possible for the rectangle to overlap in some way, but only
            # at the top-left corner;  so we check that if the top left corners
            # are the same, and if they are, return false
            #+-------+-+
            #|       | |
            #+-------+ |
            #+---------+
            if top.p1.x == rect.x and top.p1.y == rect.y:
                return True

            # if the top-left point is the same, and the left & top lines go in
            # the same direction, they collide
            if not top.overlap(rect.x, rect.x + rect.rect.x):
                return False
            if not left.overlap(rect.y, rect.y + rect.rect.y):
                return False
            return True

        p = Point(*corner)
        # lines representing the top, bottom, and left line of where this rectangle would be
        left = Line(Point(p.x, p.y), Point(p.x, p.y + new.y))
        # bottom = Line(Point(p.x, p.y + new.y), Point(p.x + new.x, p.y + new.y))
        top = Line(Point(p.x, p.y), Point(p.x + new.x, p.y))
        for rect in self.rectangles:
            if collide(rect, top, left):
                return True
        return False

class VerticalField(Field):
    """A field that only packs itself vertically."""
    def __init__(self, padding=0):
        super(VerticalField, self).__init__()
        self.padding = padding

    def add_rectangle(self, rectangle):
        """Add a rectangle to this field underneath the previous rectangle."""
        if not self.rectangles:
            self.rectangles.append(PositionedRectangle(0, 0, rectangle))
            self.x, self.y = self.calculate_bounds()
            return
        self.bottom_left(self.rectangles[-1], rectangle, place=True)
        self.x, self.y = self.calculate_bounds()

    def bottom_left(self, placed, new, place=False):
        """Attempt to place a new rectangle on the bottom left corner of a
        previously placed rectangle.  Return the amt that the overall area of
        the field would increase, or None if a collision is detected."""
        # self.mark_corners(placed.x, placed.y + placed.rect.y, new)
        self.rectangles.append(PositionedRectangle(placed.x, placed.y + placed.rect.y + self.padding, new))
        self.x, self.y = self.calculate_bounds()

class HorizontalField(Field):
    """A field that only packs itself horizontally."""
    def __init__(self, padding=0):
        super(HorizontalField, self).__init__()
        self.padding = padding

    def add_rectangle(self, rectangle):
        """Add a rectangle to this field underneath the previous rectangle."""
        if not self.rectangles:
            self.rectangles.append(PositionedRectangle(0, 0, rectangle))
            self.x, self.y = self.calculate_bounds()
            return
        self.top_right(self.rectangles[-1], rectangle, place=True)
        self.x, self.y = self.calculate_bounds()

    def top_right(self, placed, new, place=False):
        """Place a rectangle off the top right of a previous one, with
        applied x-padding."""
        self.rectangles.append(PositionedRectangle(placed.x + placed.rect.x + self.padding, 0, new))
        self.x, self.y = self.calculate_bounds()


class BoxField(Field):
    """A field that packs itself into a box, ie for rounded corner use."""
    def __init__(self, xpadding=0, ypadding=0):
        super(BoxField, self).__init__()
        self.xpadding = xpadding
        self.ypadding = ypadding

    def add_rectangle(self, rectangle):
        """Add a rectangle to this field.  Note that this field only packs
        in boxes, starting from the top left and going clockwise."""
        if not self.rectangles:
            self.rectangles.append(PositionedRectangle(0, 0, rectangle))
        elif len(self.rectangles) == 1: # top right
            tl = self.rectangles[0]
            self.rectangles.append(PositionedRectangle(tl.rect.x + self.xpadding, 0, rectangle))
        elif len(self.rectangles) == 2: # bottom right
            tl, tr = self.rectangles
            # find the max value we'd need to get the vertical padding we want
            # even if that padding is from the top-left rectangle
            maxy = max([tl.rect.y, tr.rect.y])
            # adjust the x positioning so that the bottom right corner of this
            # rectangle goes into the bottom right
            xadjust = tr.rect.x - rectangle.x
            self.rectangles.append(PositionedRectangle(tr.x,  maxy + self.ypadding, rectangle))
        elif len(self.rectangles) == 3: # bottom left
            br = self.rectangles[-1]
            # get a height adjustment so that the bottom-left corner of this
            # rectangle goes into the bottom-left corner
            yadjust = br.rect.y - rectangle.y
            self.rectangles.append(PositionedRectangle(0, br.y + yadjust, rectangle))
        else:
            raise Exception("BoxField can only accept 4 rectangles;  "
                    "You've packed too many images!")
        self.x, self.y = self.calculate_bounds()

class AlternatingField(Field):
    """A field that packs vertically, alternating from left ot right.  This
    is useful for buttons that have a left-side and a right side."""
    def __init__(self, padding=0):
        super(AlternatingField, self).__init__()
        self.padding = padding

    def add_rectangle(self, rectangle):
        """Rectangles must be sorted width-wise for this!"""
        if not self.rectangles:
            self.rectangles.append(PositionedRectangle(0, 0, rectangle))
            self.align = 'right'
        elif self.align == 'right':
            # align this rectangle along the right edge;  the max width of the
            # sprite is already determined by the first rectangle, which must be
            # the widest rectangle
            xpos = self.x - rectangle.x
            self.rectangles.append(PositionedRectangle(xpos, self.y + self.padding, rectangle))
            self.align = 'left'
        elif self.align == 'left':
            self.rectangles.append(PositionedRectangle(0, self.y + self.padding, rectangle))
            self.align = 'right'

        self.x, self.y = self.calculate_bounds()

