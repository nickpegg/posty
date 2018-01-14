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


# TODO: Create a `posty_site` fixture that is a copy of the fixture sitting
# inside a tempdir. That way the fixture files are read-only.
