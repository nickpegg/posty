import os
import pytest

from posty.renderer import RssRenderer
from posty.site import Site

from ..fixtures import site  # noqa


@pytest.fixture
def renderer(site: Site) -> RssRenderer:  # noqa
    site.load()
    return RssRenderer(site)


def test_basic_case(renderer: RssRenderer) -> None:
    """
    Simple check to see that it spits out a RSS file without bombing out
    """
    renderer.render_site()

    rss_path = os.path.join(renderer.output_path, "rss.xml")
    assert os.path.exists(rss_path)
