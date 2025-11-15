from __future__ import absolute_import

import json
import os
from dataclasses import asdict
from typing import Any

from posty.renderer.base import Renderer
from posty.renderer.util import markdown_func


class JsonRenderer(Renderer):
    """
    Renderer that outputs a JSON representation of the Site to ``site.json``
    within the output directory
    """

    def render_site(self) -> None:
        """
        Render the Site to ``site.json``
        """
        self.ensure_output_path()

        json_path = os.path.join(self.output_path, "site.json")
        payload: dict[str, Any] = {
            "pages": [],
            "posts": [],
        }

        markdown = markdown_func(self.site)

        for page in self.site.pages:
            p = asdict(page)
            p["body"] = markdown(p["body"])
            payload["pages"].append(p)

        for post in self.site.posts:
            p = asdict(post)
            p["blurb"] = markdown(p["blurb"])
            p["body"] = markdown(p["body"])
            p["date"] = post.date.isoformat()
            payload["posts"].append(p)

        payload["tags"] = self.site.tags
        payload["config"] = asdict(self.site.config)

        with open(json_path, "w") as f:
            f.write(json.dumps(payload))
