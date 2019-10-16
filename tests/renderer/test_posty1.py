import os
import pytest

from posty.renderer import Posty1RedirectRenderer
from posty.util import slugify_posty1

from ..fixtures import site  # noqa


@pytest.fixture
def renderer(site):     # noqa
    site.load()
    return Posty1RedirectRenderer(site)


def test_it_at_least_doesnt_crash(renderer):
    renderer.render_site()


def test_redirects_exist(renderer):
    renderer.render_site()
    for post in renderer.site.payload['posts']:
        path = os.path.join(
            renderer.output_path,
            str(post['date'].year),
            str(post['date'].month),
            '{}.html'.format(slugify_posty1(post['title'])),
        )
        assert os.path.exists(path)
