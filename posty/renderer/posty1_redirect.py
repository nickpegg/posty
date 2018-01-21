import jinja2
import os

from posty.util import slugify_posty1
from .base import Renderer


class Posty1RedirectRenderer(Renderer):
    """
    Renderer which creates pages to redirect old Posty1 URLs to new Posty2 URLs

    Old Posty1 post URLs are in the form of:
    /:year/:month/:old_slug.html

    Posty2 URLs are in the form of:
    /:year/:month/:slug/index.html
    """
    def render_site(self):
        template_path = os.path.join(self.site.site_path,
                                     'templates/redirect.html')
        template = jinja2.Template(open(template_path).read())

        for post in self.site.payload['posts']:
            old_dir = os.path.join(
                self.output_path,
                str(post['date'].year),
                str(post['date'].month)
            )
            if not os.path.exists(old_dir):
                os.makedirs(old_dir)

            old_slug = slugify_posty1(post['title'])
            redirect_filename = os.path.join(old_dir,
                                             '{}.html'.format(old_slug))

            with open(redirect_filename, 'w') as redirect:
                redirect.write(template.render(url=post.url()))
