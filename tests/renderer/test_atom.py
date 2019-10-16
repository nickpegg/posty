import os
import pytest

from posty.renderer import AtomRenderer

from ..fixtures import site  # noqa


@pytest.fixture
def renderer(site):     # noqa
    site.load()
    return AtomRenderer(site)


def test_basic_case(renderer):
    """
    Simple check to see that it spits out a Atom file without bombing out
    """
    renderer.render_site()

    rss_path = os.path.join(renderer.output_path, 'atom.xml')
    assert os.path.exists(rss_path)
