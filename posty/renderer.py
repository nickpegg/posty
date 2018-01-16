from future.standard_library import install_aliases
install_aliases()   # noqa

from collections import defaultdict
import jinja2
import json
import os
from urllib.parse import urljoin

from . import template_filters, util

# Route reference
# /               Posts
# /page/:page/    Posts page #:page
# /tag/:tag/      Posts matching tag :tag
# /tag/:tag/page/:page/   Posts matching tag :tag, page #:page
#
# /:year/:month/:slug/    Single post
#
# /:slug/         Page matching :slug


class Renderer(object):
    def __init__(self, site, output_path='build'):
        """
        :param site:
            a Site object to build

        :param output_path:
            path relative to the Site's path to put rendered HTML files into
        """
        self.site = site
        self.output_path = os.path.join(site.site_path, output_path)

        template_path = os.path.join(site.site_path, 'templates')
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_path),
        )
        self.set_jinja_filters()

    def set_jinja_filters(self):
        """
        Set some known filters on the jinja environment
        """
        filters = self.jinja_env.filters
        filters['markdown'] = template_filters.markdown
        filters['media_url'] = template_filters.media_url_func(self.site)

    def ensure_output_path(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def render_file(self, path, template, **kwargs):
        with open(path, 'w') as f:
            f.write(template.render(**kwargs))

    def render_site(self):
        """
        Given a Site object, render all of its components

        :param site: a loaded Site object
        """
        for post in self.site.payload['posts']:
            self.render_post(post)

        for page in self.site.payload['pages']:
            self.render_page(page)

        self.render_site_posts()
        self.render_site_tags()
        self.render_site_json()

    def render_site_json(self):
        self.ensure_output_path()

        json_path = os.path.join(self.output_path, 'site.json')
        payload = {
            'pages': [],
            'posts': [],
        }

        for page in self.site.payload['pages']:
            p = page.as_dict()
            p['body'] = template_filters.markdown(p['body'])
            payload['pages'].append(p)

        for post in self.site.payload['posts']:
            p = post.as_dict()
            p['blurb'] = template_filters.markdown(p['blurb'])
            p['body'] = template_filters.markdown(p['body'])
            p['date'] = post['date'].isoformat()
            payload['posts'].append(p)

        for k, v in self.site.payload.items():
            if k not in {'posts', 'pages'}:
                payload[k] = v

        # markdown-render each post and page
        with open(json_path, 'w') as f:
            f.write(json.dumps(payload))

    def render_posts(self, posts, prefix=''):
        """
        Render a list of posts as sets of pages where each page has
        ``num_posts_per_page`` posts. Each page of posts will be rendered to
        the path page/:page/index.html relative to the Renderer output_path

        If ``prefix`` is given, add that will be put in between the output_path
        and page path. For example if the prefix is 'tags/foo/' then a page
        path would look like 'tags/foo/page/:page/index.html'
        """
        if prefix and prefix[-1] != '/':
            prefix += '/'

        template = self.jinja_env.get_template('posts.html')
        groups = util.bucket(posts, self.site.config['num_posts_per_page'])

        base_page_url = self.site.config['base_url']
        if prefix:
            base_page_url = urljoin(base_page_url, prefix)
        base_page_url = urljoin(base_page_url, 'page/')

        output_path = os.path.join(self.output_path, prefix)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Render the first group as index.html
        posts = groups.pop(0)
        dst_file = os.path.join(output_path, 'index.html')
        next_page_url = None
        if len(groups) > 0:
            next_page_url = urljoin(base_page_url, str(2) + '/')
        self.render_file(dst_file, template, site=self.site.payload,
                         posts=posts, next_page_url=next_page_url)

        # Render the rest
        last_page = len(groups) + 1
        for page, posts in enumerate(groups, start=2):
            dst_path = os.path.join(output_path, 'page', str(page) + '/')
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)

            dst_file = os.path.join(dst_path, 'index.html')

            if page == 2:
                prev_page_url = urljoin(self.site.config['base_url'], prefix)
            else:
                prev_page_url = urljoin(base_page_url, str(page - 1) + '/')
            next_page_url = None
            if page != last_page:
                next_page_url = urljoin(base_page_url, str(page + 1) + '/')

            self.render_file(
                dst_file,
                template,
                site=self.site.payload,
                posts=posts,
                prev_page_url=prev_page_url,
                next_page_url=next_page_url
            )

    def render_site_posts(self):
        """
        Renders all of the multi-post pages, N per page
        """
        self.ensure_output_path()
        self.render_posts(self.site.payload['posts'])

    def render_site_tags(self):
        """
        Renders all of the per-tag multi-post pages, N per page
        """
        self.ensure_output_path()

        # Bucket all posts by tag
        tag_buckets = defaultdict(list)
        for post in self.site.payload['posts']:
            for tag in post['tags']:
                tag_buckets[tag].append(post)

        # For each tag, render pages of posts
        for tag, posts in tag_buckets.items():
            self.render_posts(posts, prefix='tag/{}/'.format(tag))

    def render_page(self, page):
        """
        :param page: a Page object
        """
        self.ensure_output_path()

        dst_dir = os.path.join(self.output_path, page.path_on_disk())
        dst_file = os.path.join(dst_dir, 'index.html')

        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        template = self.jinja_env.get_template('page.html')

        self.render_file(dst_file, template, site=self.site.payload, page=page)

    def render_post(self, post):
        """
        :param post: a Post object
        """
        self.ensure_output_path()

        dst_dir = os.path.join(self.output_path, post.path_on_disk())
        dst_file = os.path.join(dst_dir, 'index.html')

        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        template = self.jinja_env.get_template('post.html')

        self.render_file(dst_file, template, site=self.site.payload, post=post)
