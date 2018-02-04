from __future__ import absolute_import

import json
import os

from .base import Renderer
from .util import markdown_func


class JsonRenderer(Renderer):
    """
    Renderer that outputs a JSON representation of the Site to ``site.json``
    within the output directory
    """
    def render_site(self):
        """
        Render the Site to ``site.json``
        """
        self.ensure_output_path()

        json_path = os.path.join(self.output_path, 'site.json')
        payload = {
            'pages': [],
            'posts': [],
        }

        markdown = markdown_func(self.site)

        for page in self.site.payload['pages']:
            p = page.as_dict()
            p['body'] = markdown(p['body'])
            payload['pages'].append(p)

        for post in self.site.payload['posts']:
            p = post.as_dict()
            p['blurb'] = markdown(p['blurb'])
            p['body'] = markdown(p['body'])
            p['date'] = post['date'].isoformat()
            payload['posts'].append(p)

        for k, v in self.site.payload.items():
            if k not in {'posts', 'pages'}:
                payload[k] = v

        with open(json_path, 'w') as f:
            f.write(json.dumps(payload))
