import abc
import copy
from future.utils import with_metaclass
import os


class Renderer(with_metaclass(abc.ABCMeta)):
    """
    Base class that all renderers inherit off of. Each child class must
    implement ``render_site()`` with their own rendering logic.
    """
    def __init__(self, site, output_path='build'):
        self.site = copy.deepcopy(site)
        self.output_path = os.path.join(site.site_path, output_path)

    @abc.abstractmethod
    def render_site(self):
        raise NotImplementedError

    # Helper methods
    def ensure_output_path(self):
        """
        Ensure that the output directory ``self.output_path`` exists
        """
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
