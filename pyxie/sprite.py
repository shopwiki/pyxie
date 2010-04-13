#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Pyxies main library;  builds sprites from images."""

import os
import glob
from packer import Rectangle, Field

try:
    import Image
except ImportError:
    print "Error importing PIL; PIL is required for pyxie to work.  Original exception:"
    import sys, traceback
    traceback.print_exc()
    sys.exit(-1)

def rectangle_sort(rect):
    """Creates a key with which to sort rectangles.  This key is:
        (area, width, filename)
    That is, largest area first, with a tiebreak on the width, and
    finally a tiebreak there on the filename."""
    img = rect.data
    area = img.size[0] * img.size[1]
    width = img.size[0]
    return (area, width, os.path.basename(img.filename))

def autopack(*images):
    """Takes a list of PIL images, creates a Rectangle from them, orders them
    in a specific order, then packs them and returns the field."""
    rects = [Rectangle(*i.size, data=i) for i in images]
    rects.sort(key=rectangle_sort, reverse=True)
    f = Field()
    for rect in rects:
        f.add_rectangle(rect)
    return f

class Sprite(object):
    """A class representing a sprite sheet."""
    def __init__(self, field):
        self.field = field
        self.img = Image.new("RGBA", (field.x, field.y))
        self._draw()

    def _draw(self):
        for pos in self.field.rectangles:
            self.img.paste(pos.rect.data, (pos.x, pos.y))

    def show(self):
        self.img.show()

def sprite_from_glob(*glob_exprs):
    filenames = []
    for expr in glob_exprs:
        filenames += glob.glob(expr)
    images = [Image.open(f) for f in filenames]
    field = autopack(*images)
    return Sprite(field)

