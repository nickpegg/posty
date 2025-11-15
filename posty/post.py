import datetime
import os.path
import yaml
from dataclasses import dataclass, field
from urllib.parse import urljoin
from typing import Any

from .config import Config
from .exceptions import InvalidObject
from .model import Model
from .util import slugify


@dataclass
class Post(Model):
    """
    Representation of a post
    """

    title: str
    date: datetime.date
    blurb: str
    body: str
    _config: Config | None
    slug: str = ""
    tags: list[str] = field(default_factory=list)

    @classmethod
    def from_yaml(cls, file_contents: str, config: Config | None = None) -> "Post":
        """
        Returns a Post from the given file_contents
        """
        parts = file_contents.split("---\n")
        if not parts[0]:
            # nothing before the first ---
            parts.pop(0)

        post = yaml.safe_load(parts[0])

        if len(parts[1:]) == 1:
            # Post that has no blurb, just a body
            post["blurb"] = parts[1]
            post["body"] = parts[1]
        elif len(parts[1:]) == 2:
            # Post with a blurb and a separate body
            post["blurb"] = parts[1]
            post["body"] = "\n".join(parts[1:])
        else:
            raise InvalidObject("Got too many YAML documents in post")

        post["blurb"] = post["blurb"].strip()
        post["body"] = post["body"].strip()

        return cls(
            title=post.get("title", ""),
            slug=post.get("slug", ""),
            date=post.get("date"),
            tags=post.get("tags", ""),
            blurb=post.get("blurb", ""),
            body=post.get("body", ""),
            _config=config,
        )

    def to_yaml(self) -> str:
        """
        Returns the YAML and text representation of this Post. This is the
        reverse of ``from_yaml()``
        """
        metadata = {
            "title": self.title,
            "date": self.date,
            "tags": self.tags,
        }
        body = self.body

        output = yaml.dump(metadata, default_flow_style=False)

        if self.blurb != self.body:
            output += "---\n"
            output += self.blurb.strip()
            output += "\n"

            body = body.replace(self.blurb, "")

        output += "---\n"
        output += body.strip()

        return output

    def validate(self) -> None:
        if self.title == "":
            raise InvalidObject("Must have a title")

        if self.body == "":
            raise InvalidObject("Must have a body")

        if self.slug == "":
            self.slug = slugify(self.title)

    def url(self) -> Any:
        path = "{}/{:02d}/{}/".format(self.date.year, self.date.month, self.slug)
        return urljoin(self.config.base_url, path)

    def path_on_disk(self) -> str:
        return os.path.join(
            str(self.date.year),
            "{:02d}".format(self.date.month),
            self.slug,
        )
