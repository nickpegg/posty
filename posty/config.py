import os.path
import yaml
from dataclasses import dataclass, field

from .exceptions import InvalidConfig


@dataclass
class FeedConfig:
    rss: bool = True
    atom: bool = True


@dataclass
class CompatConfig:
    redirect_posty1_urls: bool = False


@dataclass
class Config:
    """
    Config object that gets passed around to various other objects. Loads
    config from a given YAML file.

    :param path:
        Path to a YAML file to read in as config
    """

    config_path: str

    author: str
    title: str
    description: str = ""
    base_url: str = "/"

    num_top_tags: int = 5
    num_posts_per_page: int = 5
    feeds: FeedConfig = field(default_factory=FeedConfig)
    compat: CompatConfig = field(default_factory=CompatConfig)

    def __post_init__(self) -> None:
        """
        Validate and clean the already-loaded config
        """
        if self.author == "":
            raise InvalidConfig(self, "You must set an author")

        if self.title == "":
            raise InvalidConfig(self, "You must set a title")

        if not self.base_url.endswith("/"):
            raise InvalidConfig(self, "base_url must end with /")

    @classmethod
    def from_yaml(cls, path: str = "config.yml") -> "Config":
        if not os.path.exists(path):
            raise ValueError("Unable to read config at {}".format(path))

        with open(path) as f:
            payload = yaml.safe_load(f)

        payload["config_path"] = path

        feed_conf = None
        if "feeds" in payload:
            feed_conf = FeedConfig(**payload["feeds"])
            del payload["feeds"]

        compat_conf = None
        if "compat" in payload:
            compat_conf = CompatConfig(**payload["compat"])
            del payload["compat"]

        new_config = cls(**payload)

        if feed_conf is not None:
            new_config.feeds = feed_conf
        if compat_conf is not None:
            new_config.compat = compat_conf

        return new_config
