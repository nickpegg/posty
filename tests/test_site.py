import os.path

from posty.site import Site


# Site path that points to the skeleton site
# TODO: make this part of a site fixture instead
SITE_PATH = os.path.join(os.path.dirname(__file__), '../posty/skel')


def test_site_loads_config():
    s = Site(SITE_PATH)
    assert s.config['title'] == 'My website'
