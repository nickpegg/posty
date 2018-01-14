import os.path
import pytest
import shutil


@pytest.fixture
def posty1_site_path():
    return os.path.join(os.path.dirname(__file__), 'posty1_site')


@pytest.fixture
def empty_posty_site():
    path = tempfile.mkdtemp(suffix='posty-test')
    yield Site(path)
    shutil.rmtree(path)
