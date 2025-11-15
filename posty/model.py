import abc
from typing import Any

from .config import Config


class ABC(metaclass=abc.ABCMeta):
    pass


class Model(ABC):
    """
    Base class for objects representing things stored as YAML, such as a Post
    or a Page

    :param payload:
        A dict representing the backing payload for this object

    :param config:
        A Config object
    """

    _config: Config | None

    def __post_init__(self) -> None:
        self.validate()

    @property
    def config(self) -> Config:
        if self._config is None:
            self._config = Config.from_yaml()
        return self._config

    @classmethod
    @abc.abstractmethod
    def from_yaml(cls, file_contents: str, config: Config | None = None) -> "Model":
        """
        Load an object from its YAML file representation
        """
        raise NotImplementedError

    @abc.abstractmethod
    def validate(self) -> None:
        """
        This should be implemented by the child class to verify that all fields
        that are expected exist on the payload, and set any that aren't
        """
        raise NotImplementedError

    @abc.abstractmethod
    def url(self) -> Any:
        """
        Returns the URL path to this resource
        """
        raise NotImplementedError

    @abc.abstractmethod
    def path_on_disk(self) -> str:
        """
        Returns the relative path on disk to the object, for rendering purposes
        """
        raise NotImplementedError
