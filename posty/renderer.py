import jinja2
import json
import os

from . import template_filters

# Route reference
# /               Posts
# /page/:page/    Posts page #:page
# /tag/:tag/      Posts matching tag :tag
# /tag/:tag/page/:page/   Posts matching tag :tag, page #:page
#
# /:year/:month/:slug/    Single post
#
# /:slug/         Page matching :slug


# Paths to templates, relative to the site root dir
TEMPLATES = {
    'page': 'templates/page.html',
    'post': 'templates/post.html',
    'posts': 'templates/posts.html',
}


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

    def render_site_posts(self):
        """
        Renders all of the multi-post pages, N per page
        """
        # Bucket posts into lists of N length
        pass

    def render_site_tags(self):
        """
        Renders all of the per-tag multi-post pages, N per page
        """
        # Bucket all posts by tag
        # For each tag, render pages of posts
        pass

    def render_page(self, page):
        """
        :param page: a Page object
        """
        self.ensure_output_path()

        dst_dir = os.path.join(self.output_path, page.path_on_disk())
        dst_file = os.path.join(dst_dir, 'index.html')

        os.makedirs(dst_dir, exist_ok=True)
        template = self.jinja_env.get_template('page.html')

        with open(dst_file, 'w') as f:
            f.write(template.render(site=self.site, page=page))

    def render_post(self, post):
        """
        :param post: a Post object
        """
        pass
