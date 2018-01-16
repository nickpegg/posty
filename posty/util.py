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


def bucket(_list, size):
    """
    Bucket the list ``_list`` into chunks of up to size ``size``

    Example:
    bucket([1,2,3,4,5], 2) -> [[1,2], [3,4], [5]]
    """
    buckets = []
    _list = list(_list)

    while len(_list) > 0:
        bucket = _list[:size]
        buckets.append(bucket)

        # Pop ``size`` elements off the front of iterable
        # Thankfully, list.pop(0) is an O(1) operation
        for i in range(0, len(bucket)):
            _list.pop(0)

    return buckets
