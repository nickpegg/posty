import datetime
import os

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


def test_new_page(site):    # noqa
    site.new_page()
    new_page_path = os.path.join(site.site_path, 'pages', 'new-page.yaml')
    assert os.path.exists(new_page_path)

    site.new_page('Neato page')
    new_page_path = os.path.join(site.site_path, 'pages', 'neato-page.yaml')
    assert os.path.exists(new_page_path)


def test_new_post(site):    # noqa
    date = datetime.date.today()

    site.new_post()
    filename = '{}_new-post.yaml'.format(date)
    expected_path = os.path.join(site.site_path, 'posts', filename)
    assert os.path.exists(expected_path)

    site.new_post('Neato Post')
    filename = '{}_neato-post.yaml'.format(date)
    expected_path = os.path.join(site.site_path, 'posts', filename)
    assert os.path.exists(expected_path)
