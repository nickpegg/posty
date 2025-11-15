"""
Various utility functions
"""

from slugify import slugify as awesome_slugify

from typing import TypeVar, cast

T = TypeVar("T")


def slugify(text: str) -> str:
    """
    Returns a slugified version of the given ``text``
    """
    return cast(str, awesome_slugify(text, to_lower=True))


def slugify_posty1(text: str) -> str:
    """
    Returns a Posty 1.x compatible slugified version of ``text``
    """
    return str(text).strip().lower().replace(" ", "_").replace("#", "_")


def bucket(_list: list[T], size: int) -> list[list[T]]:
    """
    Bucket the list ``_list`` into chunks of up to size ``size``

    Example:
    bucket([1,2,3,4,5], 2) -> [[1,2], [3,4], [5]]
    """
    buckets = []
    _list = list(_list)

    if size < 0:
        return [_list]

    while len(_list) > 0:
        bucket = _list[:size]
        buckets.append(bucket)

        # Pop ``size`` elements off the front of iterable
        # Thankfully, list.pop(0) is an O(1) operation
        for i in range(0, len(bucket)):
            _list.pop(0)

    return buckets
