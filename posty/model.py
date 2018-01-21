import abc
from future.utils import with_metaclass
import sys

from .config import Config


if sys.version_info >= (3, 3):
    from collections.abc import MutableMapping
else:
    from collections import MutableMapping


class ABC(with_metaclass(abc.ABCMeta)):
        pass


class Model(ABC, MutableMapping):
    """
    Base class for objects representing things stored as YAML, such as a Post
    or a Page

    :param payload:
        A dict representing the backing payload for this object

    :param config:
        A Config object
    """
    def __init__(self, payload, config=None):
        self.payload = payload

        if config is None:
            self.config = Config().load()
        else:
            self.config = config

        self.validate()

    @classmethod
    @abc.abstractmethod
    def from_yaml(cls, file_contents, config=None):
        """
        Load an object from its YAML file representation
        """
        raise NotImplementedError

    def __len__(self):
        return len(self.payload)

    def __iter__(self):
        return iter(self.payload)

    def __getitem__(self, key):
        return self.payload[key]

    def __setitem__(self, key, value):
        self.payload[key] = value

    def __delitem__(self, key):
        del self.payload[key]

    def as_dict(self):
        """
        Return a true dict representation of this object, suitable for
        serialization into JSON or YAML
        """
        return self.payload

    @abc.abstractmethod
    def validate(self):
        """
        This should be implemented by the child class to verify that all fields
        that are expected exist on the payload, and set any that aren't
        """
        raise NotImplementedError

    @abc.abstractmethod
    def url(self):
        """
        Returns the URL path to this resource
        """
        raise NotImplementedError

    @abc.abstractmethod
    def path_on_disk(self):
        """
        Returns the relative path on disk to the object, for rendering purposes
        """
        raise NotImplementedError
