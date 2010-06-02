About CSS Sprites
-----------------

The `basics of CSS sprites <http://www.alistapart.com/articles/sprites>`_ are
covered well all over the internet, and follow the use of sprites in earlier 
applications of computer graphics:  a large image sheet contains sub-images 
for use in isolation of eachother.  On the web, sprites have many applications,
like grouping icons in different states (hover/click) or even grouping graphic
resources of all different types together for transport on one request.

Why use sprites?
~~~~~~~~~~~~~~~~

As a site grows and starts to use a lot of images, the number of requests per
pageview on the media server starts to rise.  Using many requests instead of
one has a few negative performance side-effects:

* user agents can only issue a limited number of simultaneous requests to the
  same domain, which might cause a delay in loading media for the user
* there is an overhead associated for both user and server in generating and
  fielding requests

There are other multi-image issues, like load latency causing issues with hover
effects, but for the most part there are other less-problematic workarounds to
these issues.

Using `CSS sprites <http://www.alistapart.com/articles/sprites>`_ solves the
load and latency problems caused by fielding too many requests, but it does so
at the expense of other complications:

* sprite creation & usage isn't as convenient or straight forward
* sprite sheets are more difficult to modify than the originals; sprites that
  change dimensions can throw off the whole sheet

Why use pyxie?
~~~~~~~~~~~~~~

There are a number of `bookmarklets <http://spriteme.org/>`_ and even other
`standalone tools <http://spritegen.website-performance.org/>`_ available to
assist in the generation of sprites and associated pre-calculated style sheets
for their use, so why was Pyxie created, and why would anyone want to use it?

The first and weakest reason is that **pyxie is python**.  If you are looking
into dynamically generating sprites and your backend is already written in
python, pyxie is usable as a library and therefore probably going to be more
convenient.  If you need to modify the behavior of your sprite library for
some reason, say to slightly modify the output, and you are very familiar with
python, this might be a compelling reason.

Another reason you might want to use pyxie is that pyxie **supports Sass 
output**, which is not a very common feature (and perhaps also not a common 
need).  If you are already using `Sass <http://sasslang.org>`_ for your styles,
you might want to use the sass output as it will reduce the size of your CSS
output by not including sprite classes that don't have any use in any of
your actual styles.

Finally, pyxie allows you to easily write **sprite generation scripts** with
its shell interpreter mode.  This ties down each sprite to a single file that
contains both the configuration and packing modes of pyxie and the images used
in that sprite, and allows you to grow or shrink them effortlessly.

