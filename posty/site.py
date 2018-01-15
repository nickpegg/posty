from collections import Counter
import copy
import json
import os.path
import yaml

from .config import Config
from .util import slugify


class Site(object):
    def __init__(self, site_path='.'):
        self.site_path = site_path

        self._config = None
        self.payload = {
            'pages': [],
            'posts': [],
            'tags': [],
        }

    @property
    def config(self):
        if not self._config:
            config_path = os.path.join(self.site_path, 'config.yml')
            self._config = Config(config_path)
            self._config.load()
        return self._config

    def build(self, output_path='build'):
        raise NotImplementedError
        self.load()
        self.render()

    def load(self):
        """
        Load the site from files on disk into our internal representation
        """
        self._load_pages()
        self._load_posts()

    def _load_pages(self):
        pages = []
        page_dir = os.path.join(self.site_path, 'pages')
        for filename in os.listdir(page_dir):
            contents = open(os.path.join(page_dir, filename)).read()
            _, meta_yaml, body = contents.split("---\n")
            page = yaml.load(meta_yaml)

            page['body'] = body.strip()
            page.setdefault('parent')
            page.setdefault('slug', slugify(page['title']))

            pages.append(page)
        self.payload['pages'] = sorted(pages, key=lambda x: x['title'].lower())

    def _load_posts(self):
        posts = []
        tags = []

        # Load each post
        post_dir = os.path.join(self.site_path, 'posts')
        for filename in os.listdir(post_dir):
            contents = open(os.path.join(post_dir, filename)).read()
            parts = contents.split("---\n")

            post = yaml.load(parts[0])
            post.setdefault('tags', [])
            post.setdefault('slug', slugify(post['title']))

            if len(parts[1:]) == 1:
                post['blurb'] = parts[1]
                post['body'] = parts[1]
            elif len(parts[1:]) == 2:
                post['blurb'] = parts[1]
                post['body'] = "\n".join(parts[1:])
            else:
                raise RuntimeError(
                    "Got too many YAML documents in {}".format(filename)
                )

            post['blurb'] = post['blurb'].strip()
            post['body'] = post['body'].strip()

            for tag in post['tags']:
                tags.append(tag)

            posts.append(post)
        self.payload['posts'] = sorted(posts, key=lambda x: x['date'],
                                       reverse=True)

        # uniquify tags and sort by frequency (descending)
        self.payload['tags'] = [t for t, c in Counter(tags).most_common()]

    def render(self, output_path='build'):
        """
        Renders the site as JSON and HTML
        """
        raise NotImplementedError   # TODO: implement

    def post(self, slug):
        """
        Returns a post by its slug

        :param slug:
            slug of the post to find

        :returns:
            A post dict

        :raises RuntimeError:
            if no post could be found
        """
        for post in self.payload['posts']:
            if slug == slugify(post['title']):
                return post
        else:
            raise RuntimeError(
                'Unable to find post {}. Available posts: {}'.format(
                    slug,
                    [slugify(p['title']) for p in self.payload['pages']]
                )
            )

    def page(self, slug):
        """
        Returns a page by its slug

        :param slug:
            slug of the page to find

        :returns:
            A page dict

        :raises RuntimeError:
            if no page could be found
        """
        for page in self.payload['pages']:
            if slug == page.get('slug') or slug == slugify(page['title']):
                return page
        else:
            raise RuntimeError(
                'Unable to find post {}. Available posts: {}'.format(
                    slug,
                    [p.get('slug') or slugify(p['title'])
                        for p in self.payload['title']]
                )
            )

    def to_json(self):
        payload = copy.deepcopy(self.payload)

        for post in payload['posts']:
            post['date'] = post['date'].isoformat()

        return json.dumps(payload)
