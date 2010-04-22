#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Pyxies main library;  builds sprites from images."""

import os
import re
import glob
from packer import *

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

def autopack(*images, **kwargs):
    """Takes a list of PIL images, creates a Rectangle from them, orders them
    in a specific order, then packs them and returns the field.  Pass `fieldcls`
    to customize which field you want to use."""
    fieldcls = kwargs.get('fieldcls', Field)
    packtype = kwargs.get('packtype', 'Greedy')
    rects = [Rectangle(*i.size, data=i) for i in images]
    if packtype in ('Greedy', 'Vertical', 'Horizontal'):
        rects.sort(key=rectangle_sort, reverse=True)
    f = fieldcls()
    for rect in rects:
        f.add_rectangle(rect)
    return f

def slugify(name):
    """Slugify's a filename into something that is suitable for a css class name."""
    nonchr = re.compile(r'[^-_\w]')
    name = '-'.join(name.split(".")[:-1])
    return nonchr.sub('-', name)

class Sprite(object):
    """A class representing a sprite sheet."""

    css_template = """.%(name)s {
    background: transparent url(%(path)s) -%(x)dpx -%(y)dpx no-repeat;
    width: %(w)dpx; height: %(h)dpx;
}"""

    html_body_template = """<html>\n    <head><style type="text/css">
    %(css)s
    div { border: 1px solid red; }
    </style></head>
    <body>
        <h2>old: %(count)d reqs @ %(old)s, new: %(new)s</h2>
        %(body)s
    </body>\n</html>"""

    html_img_template = """<h4>file "%(filename)s"</h4><div class="%(cls)s"></div>"""

    sass_template = """\
=%(name)s
    background: transparent url(%(path)s) -%(x)dpx -%(y)dpx no-repeat
    width: %(w)dpx
    height: %(h)dpx

=%(name)s-bg
    background: transparent url(%(path)s) -%(x)dpx -%(y)dpx no-repeat

=%(name)s-bgr
    background: transparent url(%(path)s) right -%(y)dpx no-repeat
"""

    def __init__(self, field):
        self.field = field
        self.img = Image.new("RGBA", (field.x, field.y))
        self._draw()

    def _draw(self):
        for pos in self.field.rectangles:
            self.img.paste(pos.rect.data, (pos.x, pos.y))

    def show(self):
        self.img.show()

    def write(self, filename):
        if filename.endswith('gif'):
            transparency = None
            for r in self.field.rectangles:
                if 'transparency' in r.rect.data.info:
                    transparency = r.rect.data.info['transparency']
                    break
            if transparency is not None:
                self.img.save(filename, transparency=transparency)
                self.filename = filename
                return
        self.img.save(filename)
        self.filename = filename

    def sass(self, spriteurl=None):
        if not spriteurl and not hasattr(self, "filename"):
            print "Please write this sprite to an image or provide a spriteurl."""
            return
        rules = []
        spriteurl = spriteurl if spriteurl else self.filename
        for pos in self.field.rectangles:
            rect = pos.rect
            context = dict(
                name=slugify(rect.data.filename),
                path=spriteurl,
                x=pos.x, y=pos.y,
                w=rect.x, h=rect.y
            )
            rules.append(self.sass_template % context)
        return '\n'.join(rules)

    def css(self, spriteurl=None):
        if not hasattr(self, "filename"):
            print "Please write this sprite to an image first."""
            return
        spriteurl = spriteurl if spriteurl else self.filename
        rules = []
        for pos in self.field.rectangles:
            rect = pos.rect
            context = dict(
                name=slugify(rect.data.filename),
                path=spriteurl,
                x=pos.x, y=pos.y,
                w=rect.x, h=rect.y
            )
            rules.append(self.css_template % context)
        return '\n'.join(rules)

    def html(self):
        if not hasattr(self, "filename"):
            print "Please write this sprite to an image first."""
            return
        css = self.css()
        imgs = []
        paths = []
        for pos in self.field.rectangles:
            rect = pos.rect
            imgs.append(self.html_img_template % dict(
                filename=rect.data.filename,
                cls=slugify(rect.data.filename)
            ))
            paths.append(rect.data.filename)
        oldsize = human_size(filesize(*paths))
        newsize = human_size(filesize(self.filename))
        return self.html_body_template % dict(
            css=css,
            body='\n'.join(imgs),
            count=len(paths),
            old=oldsize,
            new=newsize
        )

def sprite_from_glob(*glob_exprs):
    filenames = []
    for expr in glob_exprs:
        filenames += glob.glob(expr)
    return sprite_from_paths(*filenames)

def sprite_from_paths(*paths):
    images = [Image.open(f) for f in paths]
    field = autopack(*images)
    return Sprite(field)

# utils
def filesize(*paths):
    total = 0
    for f in paths:
        total += os.path.getsize(f)
    return total

def human_size(bytes):
    """Takes bits per second and returns a string w/ appropriate units."""
    units = ['b', 'Kb', 'Mb']
    # order of magnitude
    reduce_factor = 1024.0
    oom = 0
    while bytes /(reduce_factor**(oom+1)) >= 1:
        oom += 1
    return '%0.1f %s' % (bytes/reduce_factor**oom, units[oom])

