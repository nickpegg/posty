import datetime
import os
import pytest

from posty.config import Config
from posty.exceptions import InvalidObject
from posty.post import Post

from .fixtures import config  # noqa


@pytest.fixture
def post_contents() -> str:
    path = os.path.join(
        os.path.dirname(__file__), "fixtures", "site", "posts", "multi-paragraph.yaml"
    )
    return open(path).read()


@pytest.fixture
def post(config: Config, post_contents: str) -> Post:  # noqa
    """
    Basic post
    """
    return Post.from_yaml(post_contents, config=config)


class TestValidation(object):
    def test_basic_case(self, post: Post) -> None:
        post.validate()  # Should not raise an exception

        assert post.date == datetime.date(2017, 1, 14)
        assert post.title == "Multi-paragraph Post"
        assert post.slug == "multi-paragraph-post"
        assert sorted(post.tags) == ["blah", "test"]

    def test_no_title(self, post: Post) -> None:
        post.title = ""
        with pytest.raises(InvalidObject):
            post.validate()


def test_url(post: Post) -> None:
    year = post.date.year
    month = post.date.month
    expected_url = "http://example.org/test/{}/{:02d}/{}/".format(
        year, month, post.slug
    )

    assert post.url() == expected_url


def test_to_yaml(post: Post, post_contents: str) -> None:
    assert post_contents.strip() == post.to_yaml()
