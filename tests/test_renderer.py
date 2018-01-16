import json
import os
import pytest

from posty.renderer import Renderer

from .fixtures import site  # noqa


@pytest.fixture     # noqa
def renderer(site):
    site.load()
    return Renderer(site)


def test_it_at_least_doesnt_crash(renderer):
    # Renders like this are annoying to test. Maybe we can verify what data
    # is getting passed to the jinja templates, but meh.
    #
    # Just make sure it doesn't raise and exception or whatever
    renderer.render_site()


def test_render_site_json(renderer):     # noqa
    """
    Verify that Site.render() spits out a valid JSON file
    """
    renderer.render_site_json()

    json_path = os.path.join(renderer.output_path, 'site.json')
    blob = json.load(open(json_path))
    assert blob['title'] == 'Test website'

    assert len(blob['pages']) > 0
    assert len(blob['posts']) > 0
    assert len(blob['tags']) > 0
