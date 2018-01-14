import collections.abc
import os.path
import yaml


class Config(collections.abc.MutableMapping):
    def __init__(self, path):
        self.path = path
        self.config = {}

    def load(self):
        """
        Load the YAML config from the given path, return the config object
        """
        if not os.path.exists(self.path):
            raise RuntimeError('Unable to read config at {}'.format(self.path))

        self.config = yaml.load(open(self.path).read())
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
