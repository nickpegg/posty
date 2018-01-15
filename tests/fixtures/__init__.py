import os.path
import pytest
import shutil
import tempfile

from posty.site import Site


@pytest.fixture
def posty1_site_path():
    return os.path.join(os.path.dirname(__file__), 'posty1_site')


@pytest.fixture
def empty_posty_site():
    path = tempfile.mkdtemp(suffix='posty-test')
    yield Site(path)
    shutil.rmtree(path)


@pytest.fixture
def site():
    fixture_path = os.path.join(os.path.dirname(__file__), 'site')

    path = os.path.join(tempfile.mkdtemp(suffix='posty-test'), 'site')
    site = Site(path)
    shutil.copytree(fixture_path, path)

    yield site

    shutil.rmtree(path)
