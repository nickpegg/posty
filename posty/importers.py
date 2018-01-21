"""
Functions to import from various other static site generators
"""
# Refactoring idea: make this into its own sub-package and use a plugin system

import abc
import os
import shutil
import yaml

from .exceptions import UnableToImport
from .model import ABC


class Importer(ABC):
    """
    Base class for all importers

    :param site:
        Site object for the destination

    :param src_path:
        Path to the thing to import
    """
    def __init__(self, site, src_path):
        self.site = site
        self.src_path = src_path

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError

    def ensure_directories(self):
        for _dir in ('media', 'templates', 'pages', 'posts'):
            path = os.path.join(self.site.site_path, _dir)
            if not os.path.exists(path):
                os.mkdir(path)
            elif not os.path.isdir(path):
                raise UnableToImport(
                    '{} exists but is not a directory'.format(path)
                )


class Posty1Importer(Importer):
    """
    Importer to pull from a Posty 1.x site
    """
    def run(self):
        self.ensure_directories()

        self.import_media()
        self.import_templates()
        self.import_pages()
        self.import_posts()

    def import_media(self):
        self._copy_files('_media', 'media')

    def import_templates(self):
        self._copy_files('_templates', 'templates')

    def import_pages(self):
        src_dir = os.path.join(self.src_path, '_pages')
        dst_dir = os.path.join(self.site.site_path, 'pages')

        for page in os.listdir(src_dir):
            src_file = os.path.join(src_dir, page)
            dst_file = os.path.join(dst_dir, page)

            new_page = self._convert_page(open(src_file).read())
            with open(dst_file, 'w') as fh:
                fh.write(new_page)

    def import_posts(self):
        src_dir = os.path.join(self.src_path, '_posts')
        dst_dir = os.path.join(self.site.site_path, 'posts')

        for post in os.listdir(src_dir):
            src_file = os.path.join(src_dir, post)
            dst_file = os.path.join(dst_dir, post)

            new_post = self._convert_post(open(src_file).read())
            with open(dst_file, 'w') as fh:
                fh.write(new_post)

    def _copy_files(self, src, dst):
        """
        Copy all the files in ``src_dir`` into ``dst_dir``. Each given dir
        should be relative to the source/destination sites

        :param src:
            Relative path to copy files from in the source Posty 1 site

        :param dst:
            Relative path to copy files to in the destination Posty 2 site
        """
        src_dir = os.path.join(self.src_path, src)
        dst_dir = os.path.join(self.site.site_path, dst)

        for _file in os.listdir(src_dir):
            src_path = os.path.join(src_dir, _file)
            dst_path = os.path.join(dst_dir, _file)
            print("Copying {} to {}".format(src_path, dst_path))
            if os.path.isfile(src_path):
                shutil.copy(src_path, dst_path)
            elif os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path)
            else:
                print(("  Looks like {} isn't a file nor dir, "
                       "not copying.").format(src_path))

    def _convert_page(self, old_page):
        """
        Converts an old Posty 1.x page into a new-style one. Notably just
        throws away any existing `url`
        """
        old_page = old_page.replace("\r\n", "\n")
        docs = old_page.split("---\n")
        new_page = ''

        meta = yaml.load(docs[1])
        if 'url' in meta.keys():
            del meta['url']
        new_page += yaml.dump(meta, default_flow_style=False)

        new_page += "---\n"
        new_page += docs[2]

        return new_page

    def _convert_post(self, old_post):
        """
        Converts an old Posty post (a string) into a new-style post with a
        blurb and updated metadata. Returns a string containing the three YAML
        documents.

        :param old_post:
            A string containing the contents of an old post file
        """
        old_post = old_post.replace("\r\n", "\n")
        docs = old_post.split("---\n")
        new_post = ''

        # Convert the metadata
        meta = yaml.load(docs[1])
        meta.setdefault('tags', [])
        new_post += yaml.dump(meta, default_flow_style=False)

        # Create a blurb out of the first paragraph
        body = docs[2].strip().split("\n\n")
        blurb = body[0]
        rest_of_post = "\n\n".join(body[1:])

        new_post += "---\n"
        new_post += blurb

        # Drop in the rest of the post
        new_post += "\n---\n"
        new_post += rest_of_post

        return new_post
