import os
import pytest

from posty.exceptions import InvalidObject
from posty.page import Page

from .fixtures import config    # noqa


@pytest.fixture     # noqa
def page(config):
    """
    Basic top-level page (has no parent)
    """
    path = os.path.join(os.path.dirname(__file__), 'fixtures', 'site', 'pages',
                        'test.yaml')
    contents = open(path).read()
    return Page.from_yaml(contents, config=config)


def test_validation(page):
    page.validate()     # Should not raise an exception

    assert 'parent' in page.keys()
    assert page['title'] == 'Test'
    assert page['slug'] == 'test'


def test_no_title(page):
    del page['title']
    with pytest.raises(InvalidObject):
        page.validate()


def test_no_parent(page):
    del page['parent']
    assert 'parent' not in page.payload.keys()

    page.validate()

    assert 'parent' in page.payload.keys()
