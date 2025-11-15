import os
import pytest

from posty.renderer import Posty1RedirectRenderer
from posty.site import Site
from posty.util import slugify_posty1

from ..fixtures import site  # noqa


@pytest.fixture
def renderer(site: Site) -> Posty1RedirectRenderer:  # noqa
    site.load()
    return Posty1RedirectRenderer(site)


def test_it_at_least_doesnt_crash(renderer: Posty1RedirectRenderer) -> None:
    renderer.render_site()


def test_redirects_exist(renderer: Posty1RedirectRenderer) -> None:
    renderer.render_site()
    for post in renderer.site.posts:
        path = os.path.join(
            renderer.output_path,
            str(post.date.year),
            str(post.date.month),
            "{}.html".format(slugify_posty1(post.title)),
        )
        assert os.path.exists(path)
