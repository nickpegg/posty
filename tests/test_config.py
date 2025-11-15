import os.path
import pytest

from posty.config import Config
from posty.exceptions import InvalidConfig


@pytest.fixture
def config() -> Config:
    path = os.path.join(os.path.dirname(__file__), "fixtures/site/config.yml")
    c = Config.from_yaml(path)
    return c


def test_config_at_least_loads(config: Config) -> None:
    """
    Make sure the config can load with our skeleton config and it looks
    somewhat correct when we access it like a Mapping
    """
    assert config.title == "Test website"
    assert config.num_top_tags == 5
    assert config.compat.redirect_posty1_urls is True


class TestCleanConfig(object):
    def test_no_title(self, config: Config) -> None:
        config.title = ""
        with pytest.raises(InvalidConfig):
            config.__post_init__()

    def test_no_author(self, config: Config) -> None:
        config.author = ""
        with pytest.raises(InvalidConfig):
            config.__post_init__()

    def test_defaults(self) -> None:
        config = Config(
            config_path="/does/not/exist",
            title="Test title",
            author="Test author",
        )

        assert config.description == ""
        assert config.compat.redirect_posty1_urls is False
        assert config.base_url == "/"
