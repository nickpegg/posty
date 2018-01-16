from collections import Counter
import copy
import json
import os.path
import shutil

from .config import Config
from .exceptions import PostyError
from .page import Page
from .post import Post
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

    def init(self):
        """
        Initialize a new Posty site at the gien path
        """
        skel_path = os.path.join(os.path.dirname(__file__), 'skel')
        for thing in os.listdir(skel_path):
            src = os.path.join(skel_path, thing)
            dst = os.path.join(self.site_path, thing)
            if os.path.exists(dst):
                print("{} already exists, not overwriting".format(thing))
            else:
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                elif os.path.isfile(src):
                    shutil.copy(src, dst)

    def load(self):
        """
        Load the site from files on disk into our internal representation
        """
        self.payload['title'] = self.config['title']
        self.payload['description'] = self.config['description']
        self._load_pages()
        self._load_posts()

    def _load_pages(self):
        pages = []
        page_dir = os.path.join(self.site_path, 'pages')
        for filename in os.listdir(page_dir):
            contents = open(os.path.join(page_dir, filename)).read()
            pages.append(Page.from_yaml(contents, config=self._config))

        self.payload['pages'] = sorted(pages, key=lambda x: x['title'].lower())

    def _load_posts(self):
        posts = []
        tags = []

        # Load each post
        post_dir = os.path.join(self.site_path, 'posts')
        for filename in os.listdir(post_dir):
            contents = open(os.path.join(post_dir, filename)).read()
            post = Post.from_yaml(contents, config=self._config)

            posts.append(post)
            tags.extend(post['tags'])

        self.payload['posts'] = sorted(posts, key=lambda x: x['date'],
                                       reverse=True)

        # uniquify tags and sort by frequency (descending)
        self.payload['tags'] = [t for t, c in Counter(tags).most_common()]

    def post(self, slug):
        """
        Returns a post by its slug

        :param slug:
            slug of the post to find

        :returns:
            A post dict

        :raises PostyError:
            if no post could be found
        """
        for post in self.payload['posts']:
            post_slug = post['slug'] or slugify(post['title'])
            if slug == post_slug:
                return post
        else:
            raise PostyError(
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

        :raises PostyError:
            if no page could be found
        """
        for page in self.payload['pages']:
            page_slug = page.get('slug') or slug == slugify(page['title'])
            if slug == page_slug:
                return page
        else:
            raise PostyError(
                'Unable to find post {}. Available posts: {}'.format(
                    slug,
                    [p.get('slug') or slugify(p['title'])
                        for p in self.payload['title']]
                )
            )

    def to_json(self):
        payload = copy.deepcopy(self.payload)

        # Turn Post and Page objects into their dict representations
        payload['posts'] = [p.as_dict() for p in payload['posts']]
        payload['pages'] = [p.as_dict() for p in payload['pages']]

        for post in payload['posts']:
            post['date'] = post['date'].isoformat()

        return json.dumps(payload)
