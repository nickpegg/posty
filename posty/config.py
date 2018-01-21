import os.path
import sys
import yaml

from .exceptions import InvalidConfig


if sys.version_info >= (3, 3):
    from collections.abc import MutableMapping
else:
    from collections import MutableMapping


class Config(MutableMapping):
    """
    Config object that gets passed around to various other objects. Loads
    config from a given YAML file.

    :param path:
        Path to a YAML file to read in as config
    """
    def __init__(self, path='config.yml'):
        self.path = path
        self.config = {}

    def load(self):
        """
        Load the YAML config from the given path, return the config object
        """
        if not os.path.exists(self.path):
            raise InvalidConfig(
                self,
                'Unable to read config at {}'.format(self.path)
            )

        self.config = yaml.load(open(self.path).read())
        self.clean_config()
        return self

    def __len__(self):
        return len(self.config)

    def __iter__(self):
        return iter(self.config)

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value

    def __delitem__(self, key):
        del self.config[key]

    def clean_config(self):
        """
        Validate and clean the already-loaded config
        """
        c = self.config

        if not c.get('author'):
            raise InvalidConfig(self, 'You must set an author')

        if not c.get('title'):
            raise InvalidConfig(self, 'You must set a title')

        c.setdefault('description', '')
        c.setdefault('base_url', '/')

        if not c['base_url'].endswith('/'):
            raise InvalidConfig(self, 'base_url must end with /')

        c.setdefault('num_top_tags', 5)
        c.setdefault('num_posts_per_page', 5)

        c.setdefault('feeds', {})
        c['feeds'].setdefault('rss', True)
        c['feeds'].setdefault('atom', True)

        c.setdefault('compat', {})
        c['compat'].setdefault('redirect_posty1_urls', False)
