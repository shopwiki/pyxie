#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Pyxies main library;  builds sprites from images."""

import os
from packer import Rectangle, Field

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



