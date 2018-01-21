Templating
==========

Posty uses `Jinja`_ for its templates. Your templates should live in the
``templates/`` directory in your site root.


Template Files
--------------
page.html  post_base.html  post.html  posts.html  redirect.html

There are a few required templates to be able to generate a site. Each of these
should live in the `templates/` directory in your site root.

page.html
~~~~~~~~~
This renders a single Page.

The following variables are available:

* :ref:`var_site`
* :ref:`var_page`

post.html
~~~~~~~~~
Renders a single Post.

These variables are available:

* :ref:`var_site`
* :ref:`var_post`

posts.html
~~~~~~~~~~
Renders a list of Posts. This is used both for rendering N number of posts in
a series as pages, as well as rendering the same thing for each tag.

These variables are available:

* :ref:`var_site`
* :ref:`var_posts`
* :ref:`var_next_page_url`
* :ref:`var_prev_page_url`

redirect.html
~~~~~~~~~~~~~
This is a special optional template that is used if Posty 1.x URL compatibility
is turned on. The only variable passed in is a ``url`` which is the real URL
of the post.

This is provided for you if you run ``posty init`` and it's unlikely that
you'll need to modify it.


Template Variables
------------------
These are the variables and the fields available on each that you can use in
your templates. Note that not all variables are available in all tempaltes,
see above for which ones are.

.. _var_site:

site
~~~~
This is a representation of the site as a whole. Note that if you're trying to
access a list of posts, you should likely use the

It has the following fields available on it:

* ``pages`` - The list of all Pages on the site
* ``posts`` - The list of all Posts on the site, in reverse chronological order
* ``tags`` - The list of all tags found in Posts on the site
* ``config`` - The configuration loaded from the :doc:`config`. See
  :ref:`config_variables` for details on what fields are available.
* ``copyright`` - The copyright string for the site, based on the year of your
  earliest post, the year of the latest post, and the ``author`` set in the
  :doc:`config`.

.. _var_page:

page
~~~~
The representation of the :ref:`page` being rendered.

It has these fields and functions available on it:

* ``title`` - The title of the page
* ``body`` - The body text of the page
* ``parent`` - The parent page to this page. Will be ``None`` if this is a
  top-level page.
* ``slug`` - The slugified title of the page, as used in the URL
* ``url()`` - Function which returns the absolute URL to this page

.. _var_post:

post
~~~~
The represenatation of the :ref:`post` being rendererd.

It has these fields and functions available on it:

* ``title``
* ``date``
* ``tags`` - The list of tags for this post
* ``blurb`` - The blurb (summary) of this post as defined in the YAML file. If
  no blurb was set, then this is identical to the body.
* ``body`` - The body of this post as defined in the YAML file. This will
  include the ``blurb`` if one was set in the YAML file.
* ``slug`` - The slugified title of this post, as used in the URL
* ``url()`` - Function which returns the absolute URL to this post


.. _var_posts:

posts
~~~~~
A list of :ref:`var_post` objects.

.. _var_next_page_url:

next_page_url
~~~~~~~~~~~~~
If not null, provides the absolute URL to the next page of post items.

.. _var_prev_page_url:

prev_page_url
~~~~~~~~~~~~~
If not null, provides the absolute URL to the previous page of post items.


Jinja Filters
-------------

These functions are available as `Jinja filters`_ in all templates.

markdown
~~~~~~~~
This filter takes text and returns the Markdown-rendered version of it.

Usage: ``{{ post.body | markdown }}``


.. _media_url:

media_url
~~~~~~~~~
This filter takes a URL relative to the ``media/`` directory and returns an
abosulte URL to that thing.

For example, if your ``base_url`` in your config is https://example.org/site/:

::

  {{ "css/index.css" | media_url }}

Returns ``https://example.org/site/media/css/index.css``.


absolute_url
~~~~~~~~~~~~
This filter works in a similar way to :ref:`media_url`, but instead returning
the absolute URL for an arbitrary relative URL. It does this by concatenating
the ``base_url`` from config with the given relative URL.

This is handy if you're directly linking to a page from some other page or a
post.

Usage: ``{{ "/some-page-name/" | absolute_url }}``


.. _Jinja: http://jinja.pocoo.org/docs/
.. _Jinja filters: http://jinja.pocoo.org/docs/templates/#filters
