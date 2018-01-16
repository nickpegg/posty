from future.standard_library import install_aliases
install_aliases()   # noqa

import os.path
from urllib.parse import urljoin
import yaml

from .exceptions import InvalidObject
from .model import Model
from .util import slugify


class Page(Model):
    @classmethod
    def from_yaml(cls, file_contents, config=None):
        """
        Return a Page from the given file_contents
        """
        parts = file_contents.split("---\n")
        if not parts[0]:
            # nothing before the first ---
            parts.pop(0)

        meta_yaml, body = parts
        payload = yaml.load(meta_yaml)
        payload['body'] = body.strip()

        return cls(payload, config=config)

    def validate(self):
        required_fields = ('title', 'body')
        for field in required_fields:
            if field not in self.payload.keys():
                raise InvalidObject('This Page does not have a {} set'.format(
                    field))

        self.payload.setdefault('parent')
        self.payload.setdefault('slug', slugify(self.payload['title']))

    def url(self):
        path = '{}/'.format(self.payload['slug'])
        return urljoin(self.config['base_url'], path)

    def path_on_disk(self):
        return self.payload['slug']
