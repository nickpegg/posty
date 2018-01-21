Config File
===========

Posty uses a simple YAML file for its config. Don't worry, Posty will validate
your config and let you know if anything's missing or wrong.


Example Config
--------------
This is an example config file, which is what you get in the skeleton site when
you run ``posty init``.

::

  author: you!
  title: My website
  description: Thoughts and stuff

  # URL of where this site will be hosted, must end with a /
  base_url: http://example.org/

  num_top_tags: 5
  num_posts_per_page: 5

  # Set rss or atom to False if you do not want to generate those feeds
  feeds:
    rss: True
    atom: True

  # Backward compatibility tunables
  compat:
    redirect_posty1_urls: False


Config Variables
----------------
These are all of the config variables that Posty will recognize. It will ignore
any others that you set, so if you wanted to pass any extra config to your
templates for example, you can do so!

These config variables are all accessible in the templates via
``{{ site.config }}``.


* ``author`` [required] - Your name. This gets used in the copyright string if
  you choose to add that to your templates.
* ``title`` [required] - The title for your site
* ``description`` - An optional description of your site
* ``base_url`` - The location at which your Posty-powered website will be
  hosted. So if it'll be hosted at https://example.org/blog/, then that should
  be the value set here. This value **must** have a trailing slash.
* ``num_top_tags`` - The number of tags to include in the 'top tags' list
* ``num_posts_per_page`` - When generating HTML files containing posts from the
  entire list of posts, Posty will break them up into files containing this
  number of posts
* ``feeds.rss`` - Set to ``true`` to generate an RSS feed XML file
* ``feeds.atom`` - Set to ``true`` to generate an Atom feed XML file


Compatibility Config
~~~~~~~~~~~~~~~~~~~~

* ``compat.redirect_posty1_urls`` - If set to ``true``, Posty will generate
  HTML files which redirect from an old Posty 1.x post URL to Posty 2.x post
  URLs. Use this when you are converting a Posty 1.x site to 2.x.
