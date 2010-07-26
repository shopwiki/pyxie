Using Pyxie
-----------

Concepts
========

Pyxie allows you to customize various aspects of the sprite output, including
padding around sprite elements, alignment of sprite elements and the packing
style of those elements.

Padding
~~~~~~~

Padding is given in a number of pixels and can be customized for the x and y
directions independently.  You might want to add padding if you have situations
where:

* you are worried about off-by-one-errors
* you will be using sprites as backgrounds and need translucent spacing between
  sprite elements

Alignment
~~~~~~~~~

Sprite element alignment determines how sprite elements are aligned with
relation to the sprite image itself.  The standard alignment is to align along
the top and left sides of the image.  However, sometimes you need to use images
for various backgrounds that must be aligned along other edges of the image
border.  You can specify an alignment of *left* or *right*, but for the most 
part using or writing a custom packing style will be easier to manage.

Packing Styles
~~~~~~~~~~~~~~

Packing styles dictate what strategy Pyxie uses to pack sprite elements into
one sprite image.  The default style is *greedy*, where it tries to pack
sprite elements into the smallest sheet possible by sorting the sprite elements
by size and using a simple greedy algorithm to increase the size of the sprite
sheet as little as possible at each step.

While this is probably the best strategy for most image sprite needs, it fails
for a number of image uses like repeating background strips, right-aligned or
bottom-aligned backgrounds, or backgrounds meant to go to the corners of a box.
Pyxie comes with these packing styles:

*   **greedy** - packs images as tightly as possible (speed-optimized) with
    no regards to alignment with the sprite itself or the rest of the image.

*   **vertical** - packs images vertically.  The default alignment with the
    sprite image is left-aligned, changeable with the --align-right option.
    For sprites with x-repeat, make sure their widths are all identical.

*   **horizontal** - packs images horizontally.  The default vertical
    alignment for the sprite image is top, changeable with the
    --align-bottom option.  For sprites with y-repeat, make sure their
    heights are all identical.

*   **box** - packs 4 images in a box, useful for 'corner' sprites where the
    background position is required for background placement.  Make sure to
    supply --xpadding and --ypadding sufficient to hide the rest of the
    sprite image from showing up in the middle of your content.

*   **alternating** - packs images vertically, alternating between left and
    right alignment.  Useful for button style sprites where there's a left
    and a right, but no top/bottom alignment;  this allows you to pack many
    such buttons into one sprite.

This information is available by running ``pyxie --pack-help``.

Command Line Usage
==================

You can get a full help options with ``pyxie --help`` and extra help on pack
styles with ``pyxie --pack-help``.

Output
~~~~~~

Pyxie has a few different files to output.  Pyxie requires that the path for
the sprite image itself be provided on the command line.  Pyxie will guess the
format based on the extention of this output path.

By default, styles for sprite usage are output to ``stdout``.  You can send
this output to a file instead with ``-c``, which takes the path as an argument.
You can make this style output sass mixins instead of css classes by supplying
``--sass`` with no arguments.

Pyxie can also output a sample HTML file with embedded CSS as a sample for how
the sprites look with ``-h``.

Shell Interpreter Usage
=======================

To use pyxie as a shell interpreter and create "sprite definition scripts",
simply add the following to the top of your sprite script::

    #!/usr/bin/env pyxie --sh <options> <sprite-file>
    
    path/to/image1
    path/to/image2
    path/to/image3

Note that pack styles like ``box`` and ``alternating`` rely on the order of
the images in order to position them correctly in the resultant sprite.

