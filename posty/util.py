"""
Various utility functions
"""

from slugify import slugify as awesome_slugify


def slugify(text):
    """
    Returns a slugified version of the given ``text``
    """
    return awesome_slugify(text, to_lower=True)


def slugify_posty1(text):
    """
    Returns a Posty 1.x compatible slugified version of ``text``
    """
    return str(text).strip().lower().replace(' ', '_').replace('#', '_')
