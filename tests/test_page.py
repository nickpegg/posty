import os
import pytest

from posty.config import Config
from posty.exceptions import InvalidObject
from posty.page import Page

from .fixtures import config  # noqa


@pytest.fixture
def page_contents() -> str:
    path = os.path.join(
        os.path.dirname(__file__), "fixtures", "site", "pages", "test.yaml"
    )
    return open(path).read()


@pytest.fixture
def page(config: Config, page_contents: str) -> Page:  # noqa
    """
    Basic top-level page (has no parent)
    """
    return Page.from_yaml(page_contents, config=config)


class TestValidation(object):
    def test_basic_case(self, page: Page) -> None:
        page.validate()  # Should not raise an exception

        assert page.title == "Test"
        assert page.slug == "test"

    def test_no_title(self, page: Page) -> None:
        page.title = ""
        with pytest.raises(InvalidObject):
            page.validate()


def test_url(page: Page) -> None:
    expected_url = "http://example.org/test/{}/".format(page.slug)

    assert page.url() == expected_url


def test_to_yaml(page: Page, page_contents: str) -> None:
    assert page_contents.strip() == page.to_yaml()
