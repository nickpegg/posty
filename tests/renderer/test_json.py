import json
import os
import pytest

from posty.renderer import JsonRenderer

from ..fixtures import site   # noqa


@pytest.fixture
def renderer(site):     # noqa
    site.load()
    return JsonRenderer(site)


def test_render_site(renderer):     # noqa
    """
    Verify that Site.render() spits out a valid JSON file
    """
    renderer.render_site()

    json_path = os.path.join(renderer.output_path, 'site.json')
    blob = json.load(open(json_path))
    assert blob['config']['title'] == 'Test website'

    assert len(blob['pages']) > 0
    assert len(blob['posts']) > 0
    assert len(blob['tags']) > 0
