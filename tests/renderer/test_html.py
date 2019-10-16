import os
import pytest

from posty.renderer import HtmlRenderer

from ..fixtures import site  # noqa


@pytest.fixture
def renderer(site):     # noqa
    site.load()
    return HtmlRenderer(site)


def test_it_at_least_doesnt_crash(renderer):
    # Renders like this are annoying to test. Maybe we can verify what data
    # is getting passed to the jinja templates, but meh.
    #
    # Just make sure it doesn't raise and exception or whatever
    renderer.render_site()


def test_jinja_in_markdown(renderer):
    """
    If we have jinja inside of our markdown, make sure it gets rendered as
    expected! This allows folks to use Jinja filters inside markdown!
    """
    renderer.ensure_output_path()

    test_page = renderer.site.page('jinja-in-markdown')
    renderer.render_page(test_page, template_name='simple_page.html')

    output_path = os.path.join(renderer.output_path,
                               'jinja-in-markdown/index.html')
    contents = open(output_path).read()

    assert contents == ('<p>We should be able to put jinja inside of our '
                        'templates and have it render totally normally!</p>')
