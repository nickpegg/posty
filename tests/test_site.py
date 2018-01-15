import json
import os.path

from .fixtures import site  # noqa


def test_site_loads_config(site):   # noqa
    assert site.config['title'] == 'Test website'


def test_render_json(site):     # noqa
    """
    Verify that Site.render() spits out a valid JSON file
    """
    site.load()
    site.render()

    json_path = os.path.join(site.site_path, 'build', 'site.json')
    blob = json.load(open(json_path))
    assert blob['title'] == 'Test website'

    assert len(blob['pages']) > 0
    assert len(blob['posts']) > 0
    assert len(blob['tags']) > 0
