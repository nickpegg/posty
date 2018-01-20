from .fixtures import site  # noqa


def test_site_loads_config(site):   # noqa
    assert site.config['title'] == 'Test website'


def test_page_sorting(site):    # noqa
    """
    Ensure pages are sorted alphabetically by their title
    """
    last = ''
    for page in site.payload['pages']:
        assert last < page['title']
        last = page['title']


def test_post_sorting(site):    # noqa
    """
    Ensure posts are sorted in reverse chronological order
    """
    last = None
    for post in site.payload['posts']:
        if last is None:
            last = post['date']
            continue

        assert last >= post['date']
        last = post['date']


def test_copyright(site):   # noqa
    site.load()
    assert site.copyright == 'Copyright 2010 - 2017, Jimbo Jawn'
