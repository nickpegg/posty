import abc
import copy
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from posty.site import Site


class Renderer(metaclass=abc.ABCMeta):
    """
    Base class that all renderers inherit off of. Each child class must
    implement ``render_site()`` with their own rendering logic.
    """

    def __init__(self, site: "Site", output_path: str = "build") -> None:
        self.site = copy.deepcopy(site)
        self.output_path = os.path.join(site.site_path, output_path)

    @abc.abstractmethod
    def render_site(self) -> None:
        raise NotImplementedError

    # Helper methods
    def ensure_output_path(self) -> None:
        """
        Ensure that the output directory ``self.output_path`` exists
        """
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
