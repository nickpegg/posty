from posty.renderer import util
from posty.site import Site

from ..fixtures import site  # noqa


def test_markdown(site: Site) -> None:  # noqa
    """
    Really basic test. No need to test markdown itself, just our use of it
    """
    fenced = "```\nfarts.\n```"
    result = util.markdown_func(site)(fenced)
    assert result == "<pre><code>farts.\n</code></pre>"


def test_media_url_func(site: Site) -> None:  # noqa
    func = util.media_url_func(site)
    assert func("jawn") == "http://example.org/test/media/jawn"


def test_absolute_url_func(site: Site) -> None:  # noqa
    func = util.absolute_url_func(site)
    assert func("jawn/bot") == "http://example.org/test/jawn/bot"


def test_jinja_in_markdown(site: Site) -> None:  # noqa
    """
    If we have jinja inside of our markdown, make sure it gets rendered as
    expected! This allows folks to use Jinja filters inside markdown!
    """
    site.load()
    test_page = site.page("jinja-in-markdown")
    contents = util.markdown_func(site)(test_page.body)

    assert contents == (
        "<p>We should be able to put jinja inside of our "
        "templates and have it render totally normally!</p>"
    )
