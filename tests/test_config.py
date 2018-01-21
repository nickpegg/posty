import os.path
import pytest

from posty.config import Config
from posty.exceptions import InvalidConfig


@pytest.fixture
def config():
    path = os.path.join(os.path.dirname(__file__), 'fixtures/site/config.yml')
    c = Config(path).load()
    return c


def test_config_at_least_loads(config):
    """
    Make sure the config can load with our skeleton config and it looks
    somewhat correct when we access it like a Mapping
    """
    assert config['title'] == 'Test website'
    assert config['num_top_tags'] == 5
    assert config['compat']['redirect_posty1_urls'] is True


class TestCleanConfig(object):
    def test_no_title(self, config):
        del config['title']
        with pytest.raises(InvalidConfig):
            config.clean_config()

    def test_no_description(self, config):
        del config['description']
        config.clean_config()   # shouldn't raise an exception
        assert config['description'] == ''

    def test_no_compat(self, config):
        del config['compat']
        config.clean_config()
        assert config['compat']['redirect_posty1_urls'] is False

    def test_no_base_url(self, config):
        del config['base_url']
        config.clean_config()
        assert config['base_url'] == '/'

    def test_no_author(self, config):
        del config['author']

        with pytest.raises(InvalidConfig):
            config.clean_config()
