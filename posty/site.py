import os.path

from .config import Config


class Site(object):
    def __init__(self, site_path):
        self.site_path = site_path

        self._config = None

    @property
    def config(self):
        if not self._config:
            config_path = os.path.join(self.site_path, 'config.yml')
            self._config = Config(config_path)
            self._config.load()
        return self._config

    def build(self, output_path='build'):
        # TODO: implement
        print('Not implemented yet!')
