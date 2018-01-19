import pytest

from posty.renderer import HtmlRenderer

from ..fixtures import site  # noqa


@pytest.fixture     # noqa
def renderer(site):
    site.load()
    return HtmlRenderer(site)


def test_it_at_least_doesnt_crash(renderer):
    # Renders like this are annoying to test. Maybe we can verify what data
    # is getting passed to the jinja templates, but meh.
    #
    # Just make sure it doesn't raise and exception or whatever
    renderer.render_site()
