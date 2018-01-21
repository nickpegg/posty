Quickstart
==========

To get started, create yourself an empty directory, cd into it, and then run
``posty init`` to create a site skeleton.

::

  mkdir my_site
  cd my_site
  posty init


Posty will create the skeleton and give you some basic information:

::

  Posty initialized!

  Directories:
  - posts -> Put all of your blog posts here
  - pages -> Put all of your static pages here
  - templates -> jinja2 HTML templates go here
  - media -> Static files go here; JS, CSS, images, etc.

  There is also a config file at config.yml that you should adjust to your
  liking, like setting the site title and such.

Below are some introductions to some of these things. Once you have everything
sorted and some pages and posts written, you just run the ``posty build``
command. This will render your site and place all of the resulting files into
the ``build/`` directory. The contents of that directory can then be uploaded
to your location of choice for hosting.


Config
------

You will want to adjust the config file ``config.yml`` to your liking,
especially setting the ``title``, ``author``, and ``base_url`` for the site.
The ``base_url`` is especially important and should be the URL at which your
site will eventually be hosted, for example: ``https://yourwebsite.com/blog/``.

See :doc:`config` for more information about the config file options.


Content
-------

Content is stored in two directories, ``posts`` and ``pages``. Each file in
these directories are YAML metadata and a Markdown body, separated by a
``---``. A couple of examples have been provided for you by the ``posty init``
command, but you should check out :doc:`schema` for information about what
these types of files should look like.

The CLI has some commands available to easily create new pages and posts. Here
are some examples:

::

  $ posty new page --name "About me"
  $ cat pages/about-me.yaml
  parent: None
  title: About me
  ---
  This is your new page. Write what you want here!

::

  $ posty new post --name "A nifty blog post"
  $ cat posts/2018-01-20_a-nifty-blog-post.yaml
  date: 2018-01-20
  tags:
  - tag1
  - tag2
  title: A nifty blog post
  ---
  This the the summary/first paragraph of your new post
  ---
  This is the rest of the post.

  Write what you want here


Templates
---------

The ``templates/`` directory is where you put all of your HTML templates. These
will be rendered by `Jinja`_. See :doc:`templating` for more information about
what these templates should look like.


Static files
------------

The ``media/`` directory is where you should put all of your static files, such
as JavaScript, CSS, images, etc. When you run ``posty build``, it simply copies
this directory over to your ``build/`` directory.

To help with accessing these files, there is a Jinja filter available in
templates called ``media_url``. It will translate any path relative to the
``media`` directory into a full absolute URL. It's used like so:

::

  <link rel="stylesheet" href="{{ 'css/index.css' | media_url }}" />




.. _Jinja: http://jinja.pocoo.org/docs/
