import os
import logging
import pytest
from pathlib import Path

from posty.renderer import HtmlRenderer
from posty.site import Site

from ..fixtures import site  # noqa

logger = logging.getLogger(__name__)


@pytest.fixture
def renderer(site: Site) -> HtmlRenderer:  # noqa
    site.load()
    return HtmlRenderer(site)


def test_it_at_least_doesnt_crash(renderer: HtmlRenderer) -> None:
    # Renders like this are annoying to test. Maybe we can verify what data
    # is getting passed to the jinja templates, but meh.
    #
    # Just make sure it doesn't raise and exception or whatever
    renderer.render_site()


def test_jinja_in_markdown(renderer: HtmlRenderer) -> None:
    """
    If we have jinja inside of our markdown, make sure it gets rendered as
    expected! This allows folks to use Jinja filters inside markdown!
    """
    renderer.ensure_output_path()

    test_page = renderer.site.page("jinja-in-markdown")
    renderer.render_page(test_page, template_name="simple_page.html")

    output_path = os.path.join(renderer.output_path, "jinja-in-markdown/index.html")
    contents = open(output_path).read()

    assert contents == (
        "<p>We should be able to put jinja inside of our "
        "templates and have it render totally normally!</p>"
    )


def test_unlimited_posts_per_page(renderer: HtmlRenderer) -> None:
    """
    If Config.num_posts_per_page is <0, then we should render all posts on the first
    page.
    """

    # Sanity check, num_posts_per_page = 1 should only have the first post on the main
    # page
    renderer.site.config.num_posts_per_page = 1
    renderer.render_site()

    index_page = Path(renderer.output_path, "index.html").read_text()
    assert len(renderer.site.posts) > 1
    assert renderer.site.posts[0].title in index_page
    for post in renderer.site.posts[1:]:
        assert post.title not in index_page

    # New behavior, all posts on the first page
    renderer.site.config.num_posts_per_page = -1
    renderer.render_site()

    index_page = Path(renderer.output_path, "index.html").read_text()
    for post in renderer.site.posts:
        assert post.title in index_page
