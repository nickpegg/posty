from future.standard_library import install_aliases
install_aliases()   # noqa

import jinja2
from markdown import markdown as md
from urllib.parse import urljoin

# Jinja2 template filters

# TODO: Since each of these functions take a site and return the actual
# function we want, we'd probably be better off just making some sort of filter
# generator class with a ``generate()`` method that returns a jinja filters
# dict


def markdown_func(site):
    """
    Returns a filter function which will return the rendered version of the
    given Markdown text.

    This is done in two passes. First the content is rendered as Jinja, which
    allows the use of the other filters found here, like ``media_url`` and
    ``absolute_url``. Then, the result of that is rendered as markdown.
    """
    def markdown(text):
        jinja_env = jinja2.Environment()
        jinja_env.filters['media_url'] = media_url_func(site)
        jinja_env.filters['absolute_url'] = absolute_url_func(site)

        jinja_rendered = jinja_env.from_string(text).render()

        return md(
            jinja_rendered,
            tab_length=2,
            extensions=['markdown.extensions.fenced_code']
        )

    return markdown


def media_url_func(site):
    """
    Returns a filter function that returns a full media URL for the given file,
    scoped to the given Site object.

    For example, if the Site has its base_url set to '/foo/' then:
    img/my_picture.jpg -> /foo/media/img/my_picture.jpg
    """
    def media_url(path):
        base_path = urljoin(site.config['base_url'], 'media/')
        return urljoin(base_path, path)

    return media_url


def absolute_url_func(site):
    """
    Returns a markdown filter function that returns an absolute URL for the
    given relative URL, simply concatenating config['base_url'] with the URL.
    """
    def absolute_url(path):
        return urljoin(site.config['base_url'], path)

    return absolute_url
