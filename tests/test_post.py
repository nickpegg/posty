import datetime
import os
import pytest

from posty.exceptions import InvalidObject
from posty.post import Post

from .fixtures import config    # noqa


@pytest.fixture
def post_contents():
    path = os.path.join(os.path.dirname(__file__), 'fixtures', 'site', 'posts',
                        'multi-paragraph.yaml')
    return open(path).read()


@pytest.fixture
def post(config, post_contents):    # noqa
    """
    Basic post
    """
    return Post.from_yaml(post_contents, config=config)


class TestValidation(object):
    def test_basic_case(self, post):
        post.validate()     # Should not raise an exception

        assert post['date'] == datetime.date(2017, 1, 14)
        assert post['title'] == 'Multi-paragraph Post'
        assert post['slug'] == 'multi-paragraph-post'
        assert sorted(post['tags']) == ['blah', 'test']

    def test_no_title(self, post):
        del post['title']
        with pytest.raises(InvalidObject):
            post.validate()

    def test_no_tags(self, post):
        del post['tags']
        post.validate()
        assert post['tags'] == []


def test_url(post):
    year = post['date'].year
    month = post['date'].month
    expected_url = 'http://example.org/test/{}/{:02d}/{}/'.format(year, month,
                                                                  post['slug'])

    assert post.url() == expected_url


def test_to_yaml(post, post_contents):
    assert post_contents.strip() == post.to_yaml()
