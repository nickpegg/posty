import datetime
import os
import pytest

from posty.exceptions import InvalidObject
from posty.post import Post

from .fixtures import config    # noqa


@pytest.fixture     # noqa
def post(config):
    """
    Basic post
    """
    path = os.path.join(os.path.dirname(__file__), 'fixtures', 'site', 'posts',
                        'multi-paragraph.yaml')
    contents = open(path).read()
    return Post.from_yaml(contents, config=config)


def test_validation(post):
    post.validate()     # Should not raise an exception

    assert post['date'] == datetime.date(2017, 1, 14)
    assert post['title'] == 'Multi-paragraph Post'
    assert post['slug'] == 'multi-paragraph-post'
    assert sorted(post['tags']) == ['blah', 'test']


def test_no_title(post):
    del post['title']
    with pytest.raises(InvalidObject):
        post.validate()


def test_no_tags(post):
    del post['tags']
    post.validate()
    assert post['tags'] == []
