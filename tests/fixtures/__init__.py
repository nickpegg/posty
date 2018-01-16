import os.path
import pytest
import shutil
import tempfile

from posty.config import Config
from posty.site import Site


@pytest.fixture
def config():
    config_path = os.path.join(os.path.dirname(__file__), 'site', 'config.yml')
    return Config(path=config_path).load()


@pytest.fixture
def posty1_site_path():
    return os.path.join(os.path.dirname(__file__), 'posty1_site')


@pytest.fixture
def empty_posty_site():
    path = tempfile.mkdtemp(suffix='posty-test')
    site = Site(path)
    site._config = Config()
    yield site
    shutil.rmtree(path)


@pytest.fixture
def site():
    fixture_path = os.path.join(os.path.dirname(__file__), 'site')

    path = os.path.join(tempfile.mkdtemp(suffix='posty-test'), 'site')
    site = Site(path)

    shutil.copytree(fixture_path, path)

    yield site

    shutil.rmtree(path)
