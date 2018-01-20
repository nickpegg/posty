from collections import Counter
import datetime
import os.path
import shutil

from .config import Config
from .exceptions import PostyError
from .page import Page
from .post import Post
from .renderer import HtmlRenderer, JsonRenderer, RssRenderer, AtomRenderer
from .util import slugify


class Site(object):
    def __init__(self, site_path='.', config_path=None):
        self.site_path = site_path

        if config_path:
            self.config_path = config_path
        else:
            self.config_path = os.path.join(site_path, 'config.yml')

        self._config = None
        self.payload = {
            'pages': [],
            'posts': [],
            'tags': [],
        }

        self.loaded = False

    @property
    def config(self):
        if not self._config:
            config_path = os.path.join(self.config_path)
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
        self.payload['base_url'] = self.config['base_url']
        self.payload['num_top_tags'] = self.config['num_top_tags']

        self._load_pages()
        self._load_posts()
        self.loaded = True

    def render(self, output_path='build'):
        """
        Render the site with the various renderers
        """
        HtmlRenderer(self, output_path=output_path).render_site()
        JsonRenderer(self, output_path=output_path).render_site()

        if self.config['feeds']['rss']:
            RssRenderer(self, output_path=output_path).render_site()
        if self.config['feeds']['atom']:
            AtomRenderer(self, output_path=output_path).render_site()

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
                        for p in self.payload['pages']]
                )
            )

    @property
    def copyright(self):
        """
        Returns a string of the copyright info, based on the configured author
        and the years of the first and last post
        """
        if not self.loaded:
            raise PostyError('You must run load() on this site first!')

        first_post = self.payload['posts'][-1]
        last_post = self.payload['posts'][0]

        copyright = 'Copyright {start} - {end}, {author}'.format(
            author=self.config['author'],
            start=first_post['date'].year,
            end=last_post['date'].year
        )

        return copyright

    def new_post(self, name="New Post"):
        """
        Create a new post in the site directory from the skeleton post
        """
        post_dir = os.path.join(self.site_path, 'posts')
        if not os.path.exists(post_dir):
            raise PostyError('You must initialize the site first')

        date = datetime.date.today()
        filename = '{}_{}.yaml'.format(date, slugify(name))
        post_path = os.path.join(post_dir, filename)

        skel_path = os.path.join(os.path.dirname(__file__),
                                 'skel/posts/1970-01-01_new-post.yaml')

        shutil.copy(skel_path, post_path)

    def new_page(self, name="New Page"):
        """
        Create a new page in the site directory from the skeleton page
        """
        page_dir = os.path.join(self.site_path, 'pages')
        if not os.path.exists(page_dir):
            raise PostyError('You must initialize the site first')

        filename = '{}.yaml'.format(slugify(name))
        page_path = os.path.join(page_dir, filename)

        skel_path = os.path.join(os.path.dirname(__file__),
                                 'skel/pages/new-page.yaml')

        shutil.copy(skel_path, page_path)
