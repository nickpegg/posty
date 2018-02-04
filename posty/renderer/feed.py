import abc
from datetime import datetime, time

from feedgen.feed import FeedGenerator
import pytz

from .base import Renderer
from .util import markdown_func


class FeedRenderer(Renderer):
    """
    Base class for all feed Renderers (RSS, Atom)
    """
    def render_site(self):
        config = self.site.config

        self.feed = FeedGenerator()
        self.feed.id(config['base_url'])
        self.feed.title(config['title'])
        self.feed.author({'name': config['author']})
        self.feed.copyright(self.site.copyright)
        self.feed.link(href=config['base_url'], rel='alternate')

        self.feed.link(href=self.url(), rel='self')

        if config['description']:
            self.feed.description(config['description'])
        else:
            self.feed.description(config['title'])

        # Set pubDate to the last post's date
        pub_date = datetime.combine(
            self.site.payload['posts'][0]['date'],
            time(tzinfo=pytz.utc),
        )
        self.feed.pubDate(pub_date)

        self.render_posts()
        self.output()

    def render_posts(self):
        """
        Add each post to the feed
        """
        for post in reversed(self.site.payload['posts']):
            entry = self.feed.add_entry()
            entry.id(post.url())
            entry.link(href=post.url())
            entry.title(post['title'])

            pub_date = datetime.combine(
                post['date'],
                time(tzinfo=pytz.utc),
            )
            entry.published(pub_date)

            markdown = markdown_func(self.site)
            entry.summary(markdown(post['blurb']))
            entry.content(markdown(post['body']))

    @abc.abstractmethod
    def output(self):
        """
        This method must be implemented by child classes. It gets called during
        render_site to output the specific file, such as the RSS file or Atom
        file
        """
        raise NotImplementedError

    @abc.abstractmethod
    def url(self):
        """
        Return the URL to this feed file
        """
        raise NotImplementedError
