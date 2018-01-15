import os.path

from posty.config import Config


def test_config_at_least_loads():
    """
    Make sure the config can load with our skeleton config and it looks
    somewhat correct when we access it like a Mapping
    """
    path = os.path.join(os.path.dirname(__file__), '../posty/skel/config.yml')
    c = Config(path).load()

    assert c['title'] == 'My website'
    assert c['num_top_tags'] == 5
    assert c['compat']['redirect_posty1_urls'] is False
