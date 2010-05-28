.. pyxie documentation master file, created by sphinx-quickstart.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pyxie
-----------

.. automodule:: pyxie
.. highlight:: sh

You can install pyxie with pip::

    pip install pyxie

You can fork pyxie `from its git repository
<http://github.com/shopwiki/pyxie/>`_::

    git clone http://github.com/shopwiki/pyxie.git

.. highlight:: python

Usage
-----

Pyxie is both a python module called ``pyxie``, which contains sprite
generation, packing logic, and some sprite-related utility functions,
as well as a script also called ``pyxie`` which is usable both as an ad-hoc
sprite generator and as a shell interpreter with which you could write
sprite-generating "pyxie scripts".

A lot of help is available by running ``pyxie --help``::

    Usage: pyxie [opts] spritefile <images>

    Options:
      --version             show program's version number and exit
      --help                show this help message and exit
      -c CSS, --css=CSS     css output file (default stdout)
      --sass                output style as sass mixins
      --sprite-url=SPRITE_URL
                            url to the sprite
      -h HTML, --html=HTML  html output file (default none)
      -y YPADDING, --ypadding=YPADDING
                            add vertical padding to vertically packed images
      -x XPADDING, --xpadding=XPADDING
                            add horizontal padding to horizontally packed images
      -i IMAGES, --images=IMAGES
                            read images to use from a text file
      --sh                  script mode

      Packing Styles:
        Change the way that Pyxie packs images (for use in different contexts)

        --greedy            default operation;  greedy algorithm to pack as tight
                            as possible
        --vertical          pack images vertically only (for x-repeat)
        --horizontal        pack images horizontally only (for y-repeat)
        --box               pack images in a box (for corners)
        --alternating       pack images vertically, alternating left/right
                            alignment
        --pack-help         extended information on pack styles
        --align-bottom      
        --align-right       

.. toctree::
    :maxdepth: 1

    generating_sprites
    extending

