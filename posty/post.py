from future.standard_library import install_aliases
install_aliases()   # noqa

import os.path
from urllib.parse import urljoin
import yaml

from .exceptions import InvalidObject
from .model import Model
from .util import slugify


class Post(Model):
    @classmethod
    def from_yaml(cls, file_contents, config=None):
        """
        Returns a Post from the given file_contents
        """
        parts = file_contents.split("---\n")
        if not parts[0]:
            # nothing before the first ---
            parts.pop(0)

        post = yaml.load(parts[0])

        if len(parts[1:]) == 1:
            # Post that has no blurb, just a body
            post['blurb'] = parts[1]
            post['body'] = parts[1]
        elif len(parts[1:]) == 2:
            # Post with a blurb and a separate body
            post['blurb'] = parts[1]
            post['body'] = "\n".join(parts[1:])
        else:
            raise InvalidObject('Got too many YAML documents in post')

        post['blurb'] = post['blurb'].strip()
        post['body'] = post['body'].strip()

        return cls(post, config=config)

    def validate(self):
        required_fields = ('title', 'date', 'blurb', 'body')
        for field in required_fields:
            if field not in self.payload.keys():
                raise InvalidObject(
                    'Post is missing a {} field in the metadata'.format(field)
                )

        self.payload.setdefault('tags', [])
        self.payload.setdefault('slug', slugify(self.payload['title']))

    def url(self):
        path = '{}/{:02d}/{}/'.format(
            self.payload['date'].year,
            self.payload['date'].month,
            self.payload['slug']
        )
        return urljoin(self.config['base_url'], path)

    def full_url(self):
        return urljoin(self.config['full_url'], self.url())

    def path_on_disk(self):
        return os.path.join(
            str(self.payload['date'].year),
            '{:02d}'.format(self.payload['date'].month),
            self.payload['slug'],
        )
