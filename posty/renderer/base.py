import abc
from future.utils import with_metaclass
import os


class Renderer(with_metaclass(abc.ABCMeta)):
    def __init__(self, site, output_path='build'):
        self.site = site
        self.output_path = os.path.join(site.site_path, output_path)

    @abc.abstractmethod
    def render_site(self):
        raise NotImplementedError

    # Helper methods
    def ensure_output_path(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
