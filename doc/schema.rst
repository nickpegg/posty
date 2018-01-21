Post and Page Schema
====================

A site is made up of two main components: :ref:`pages` and :ref:`posts`. Each
type of file consists of two parts: a YAML header and the actual content. See
below for the format of each.

Like the :doc:`config file <config>`, you can set extra keys in the metadata which will
simply be passed along, enabling you to use them in your templates.


.. _pages:

Pages
-----

Pages are the simplest object. These are located in the ``pages/`` directory
in your site root. They are simply some YAML metadata, followed by three
dashes, followed my the Markdown content of the page itself.

When a page is rendered into HTML, its URL will be ``:title_slug/index.html``
relative to your site's :ref:`base_url <config_variables>`.

Example
~~~~~~~
::

  title: About Me
  ---
  This is a page. Write what you want here!

Required Metadata Fields
~~~~~~~~~~~~~~~~~~~~~~~~
* ``title`` - The title of the page


.. _posts:

Posts
-----

Posts are a little bit more complex. They have three sections separated by
``---``: the YAML metadata, a blurb (or summary), and the body.

The 'blurb' is the start of your post, usually a single paragraph. It gets
stored on to the Post object as the ``blurb`` field and is most useful when
you have a list of posts and only want to show the blurb, but then have readers
click a link to view the entire post.

The next section in the file, the ``body``, is a separate piece from the blurb
and Posty behind the scenes will combine the two when rendering a full-post
HTML file.

If you do not have a ``---`` separating a blurb from a body, then it will just
be considered to be just the body as a whole. The ``blurb`` field on the Post
object will just be set to be the ``body`` so that the field is still populated
with something.

All posts will be rendered into HTML files with URLs that look like
``:year/:zero_padded_month/:slug/index.html`` relative to the
:ref:`base_url <config_variables>`.

Additionally a series of HTML files will be rendered with a certain number of
posts per file (controlled by :ref:`num_posts_per_page <config_variables>`) in
reverse-chronological order. The first page will be rendered as ``index.html``
and following pages will be rendered as ``page/:page_num/index.html``.

.. _post_tags:
Tags
~~~~

If a post has a list of :ref:`tags <post_optional_metadata>` associated with
it, these tags will be collected and rendered into lists of posts similar to
the main list. They follow the same URL pattern as the main list but are
prefixed with ``tags/:tag_name/``, e.g.: ``tags/foo/page/2/``.

Example
~~~~~~~
::

  title: New Post
  date: 1970-01-01
  tags:
      - tag1
      - tag2
  ---
  This the the summary/first paragraph of your new post
  ---
  This is the rest of the post.

  Write what you want here!

Blurb-less Example
~~~~~~~~~~~~~~~~~~
::

  title: New Post
  date: 1970-01-01
  tags:
      - tag1
      - tag2
  ---
  This the the summary/first paragraph of your new post

  This is the rest of the post.

  Write what you want here!

Required Metadata Fields
~~~~~~~~~~~~~~~~~~~~~~~~
* ``title`` - The title of the post
* ``date`` - The date of the post, formatted as ``YYYY-MM-DD``

.. _post_optional_metadata:

Optional Metadata Fields
~~~~~~~~~~~~~~~~~~~~~~~~
* ``tags`` - A list of :ref:`tags <post_tags>` to be associated with the post.
