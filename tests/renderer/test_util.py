from posty.renderer import util

from ..fixtures import site  # noqa


def test_markdown():
    """
    Really basic test. No need to test markdown itself, just our use of it
    """
    fenced = "```\nfarts.\n```"
    result = util.markdown(fenced)
    assert result == "<pre><code>farts.\n</code></pre>"


def test_media_url_func(site):  # noqa
    func = util.media_url_func(site)
    assert func('jawn') == 'http://example.org/test/media/jawn'


def test_absolute_url_func(site):   # noqa
    func = util.absolute_url_func(site)
    assert func('jawn/bot') == 'http://example.org/test/jawn/bot'
