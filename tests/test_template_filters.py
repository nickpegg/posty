from posty import template_filters

from .fixtures import site  # noqa


def test_markdown():
    """
    Really basic test. No need to test markdown itself, just our use of it
    """
    fenced = "```\nfarts.\n```"
    result = template_filters.markdown(fenced)
    assert result == "<pre><code>farts.\n</code></pre>"


def test_media_url_func(site):  # noqa
    func = template_filters.media_url_func(site)
    assert func('jawn') == '/test/media/jawn'
