Importing From Other Static Site Generators
===========================================

Posty 1.x
---------

The ``posty import posty1`` command lets you import from an old Posty 1.x site
into a new Posty 2.x site. This command should be ran from a directory which
will house your new Posty 2.x site.

It doesn't matter if this Posty 2.x site directory has been initialized or not,
but you will need to make sure that a :doc:`valid config <config>` exists in
your site directory.

CLI Example
~~~~~~~~~~~
::

  # From within your Posty 2.x site directory (empty or not)
  posty import posty1 /path/to/your/posty1_site

Import Process
~~~~~~~~~~~~~~
Here's what happens when you run the ``posty import posty1`` command:

#. All of your media files are copied from ``old_site/_media/`` to
   ``new_site/media/``.
#. All of your templates are copied from ``old_site/_templates/`` to
   ``new_site/templates/``.
#. All of your pages are copied from ``old_site/_pages/`` to
   ``new_site/pages/``.
#. All of your posts are copied and converted from ``old_site/_posts/`` to
   ``new_site/posts/``.

In each post, the first paragraph of each body will be converted into a
:ref:`blurb <posts>`, so it's a good idea to inspect each post to make sure it
was converted to your liking.

Additionally it's a good idea to check that your templates will work with
Posty 2.x. See :doc:`templating` for more info on what variables are available.
