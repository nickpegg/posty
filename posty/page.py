from dataclasses import dataclass
from urllib.parse import urljoin
from typing import Any
import yaml

from .config import Config
from .exceptions import InvalidObject
from .model import Model
from .util import slugify


@dataclass
class Page(Model):
    """
    Representation of a page
    """

    title: str
    body: str
    slug: str = ""

    # Name of the parent page
    parent: str | None = None

    _config: Config | None = None

    @classmethod
    def from_yaml(cls, file_contents: str, config: Config | None = None) -> "Page":
        """
        Return a Page from the given file_contents
        """
        parts = file_contents.split("---\n")
        if not parts[0]:
            # nothing before the first ---
            parts.pop(0)

        meta_yaml, body = parts
        payload = yaml.safe_load(meta_yaml)
        payload["body"] = body.strip()

        return cls(
            title=payload["title"],
            body=payload["body"],
            _config=config,
        )

    def to_yaml(self) -> str:
        """
        Returns a string of the YAML and text representation of this Post.
        This is the reverse of from_yaml
        """
        metadata = {"title": self.title}
        if self.parent:
            metadata["parent"] = self.parent
        output = yaml.dump(metadata, default_flow_style=False)
        output += "---\n"
        output += self.body

        return output

    def validate(self) -> None:
        """
        Validate that the page is correct.

        :raises: InvalidObject
        """
        if self.title == "":
            raise InvalidObject("This Page is missing a title")
        if self.body == "":
            raise InvalidObject("This Page is missing a body")

        if self.slug == "":
            self.slug = slugify(self.title)

    def url(self) -> Any:
        path = "{}/".format(self.slug)
        return urljoin(self.config.base_url, path)

    def path_on_disk(self) -> str:
        return self.slug
