from future.standard_library import install_aliases
install_aliases()   # noqa

from markdown import markdown as md
from urllib.parse import urljoin


# Jinja2 template filters

def markdown(text):
    """
    Returns the rendered version of the given Markdown text
    """
    return md(text, tab_length=2,
              extensions=['markdown.extensions.fenced_code'])


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
