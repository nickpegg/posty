import os
import pytest

from .fixtures import posty1_site_path, empty_posty_site    # noqa
from posty.importers import Posty1Importer


class TestPosty1Importer(object):
    @pytest.fixture
    def importer(self, posty1_site_path, empty_posty_site):     # noqa
        return Posty1Importer(empty_posty_site, posty1_site_path)

    @pytest.fixture
    def importer_with_directories(self, importer):
        importer.ensure_directories()
        return importer

    def test_ensure_directories(self, importer):
        importer.ensure_directories()

        dirs = ('posts', 'pages', 'media', 'templates')
        for _dir in dirs:
            path = os.path.join(importer.site.site_path, _dir)
            assert os.path.isdir(path)

    def test_import_media(self, importer_with_directories):
        """
        All media should be copied verbatim
        """
        importer = importer_with_directories
        importer.import_media()

        src_path = os.path.join(importer.src_path, '_media')
        dst_path = os.path.join(importer.site.site_path, 'media')
        for f in os.listdir(src_path):
            src_file = open(os.path.join(src_path, f)).read()
            dst_file = open(os.path.join(dst_path, f)).read()
            assert src_file == dst_file

    def test_import_templates(self, importer_with_directories):
        """
        all templates should be copied verbatim
        """
        importer = importer_with_directories
        importer.import_templates()

        src_path = os.path.join(importer.src_path, '_templates')
        dst_path = os.path.join(importer.site.site_path, 'templates')
        for f in os.listdir(src_path):
            src_file = open(os.path.join(src_path, f)).read()
            dst_file = open(os.path.join(dst_path, f)).read()
            assert src_file == dst_file

    def test_import_pages(self, importer_with_directories):
        """
        all pages should be copies verbatim
        """
        importer = importer_with_directories
        importer.import_pages()

        # Ensure `url` is not set on any pages
        site = importer.site
        site._load_pages()
        for page in site.payload['pages']:
            assert page.get('url') is None

    def test_import_posts(self, importer_with_directories):
        """
        all posts should be copied over with blurbs created from their first
        paragraphs
        """
        importer = importer_with_directories
        importer.import_posts()

        site = importer.site
        site._load_posts()

        num_posts = len(os.listdir(os.path.join(importer.src_path, '_posts')))
        assert num_posts == len(site.payload['posts'])

        post = site.post('single-paragraph-post')
        assert post['title'] == 'Single paragraph post'
        assert post['blurb'] == post['body']
        assert post['body'] == ('This is a post that just has a single '
                                'paragraph')

        post = site.post('multi-paragraph-post')
        assert post['title'] == 'Multi-paragraph Post'
        assert post['blurb'] == ('This is a post that has multiple paragraphs,'
                                 ' where the first paragraph should get '
                                 'converted into a blurb.')
        assert post['body'] == """
This is a post that has multiple paragraphs, where the first paragraph should get converted into a blurb.

This is the second paragraph, which should be hidden from the blurb.

And a third paragraph, also outside the blurb.
        """.strip()     # noqa

    def test_it_at_least_runs(self, importer):
        importer.run()
