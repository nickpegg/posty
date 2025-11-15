import os.path
import pytest
import shutil
import tempfile
from typing import Generator

from posty.config import Config
from posty.site import Site


@pytest.fixture
def config() -> Config:
    config_path = os.path.join(os.path.dirname(__file__), "site", "config.yml")
    return Config.from_yaml(config_path)


@pytest.fixture
def posty1_site_path() -> str:
    return os.path.join(os.path.dirname(__file__), "posty1_site")


@pytest.fixture
def empty_posty_site() -> Generator[Site, None, None]:
    path = tempfile.mkdtemp(suffix="posty-test")
    cfg = Config(
        config_path=os.path.join(path, "config.yml"),
        author="Test Author",
        title="Test Blog",
    )
    site = Site(path, config=cfg)
    yield site
    shutil.rmtree(path)


@pytest.fixture
def site() -> Generator[Site, None, None]:
    fixture_path = os.path.join(os.path.dirname(__file__), "site")

    path = os.path.join(tempfile.mkdtemp(suffix="posty-test"), "site")
    shutil.copytree(fixture_path, path)
    site = Site(path)

    yield site

    shutil.rmtree(path)
