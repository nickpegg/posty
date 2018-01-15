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


def test_page_sorting(site):    # noqa
    """
    Ensure pages are sorted alphabetically by their title
    """
    last = ''
    for page in site.payload['pages']:
        assert last < page['title']
        last = page['title']


def test_post_sorting(site):    # noqa
    """
    Ensure posts are sorted in reverse chronological order
    """
    last = None
    for post in site.payload['posts']:
        if last is None:
            last = post['date']
            next

        assert last >= post['date']
        last = post['date']
