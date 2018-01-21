from future.standard_library import install_aliases
install_aliases()   # noqa

import os
from urllib.parse import urljoin

from .feed import FeedRenderer


class RssRenderer(FeedRenderer):
    """
    Renderer that outputs a RSS feed XML file
    """
    filename = 'rss.xml'

    def url(self):
        """
        Return the URL to this feed file
        """
        return urljoin(self.site.config['base_url'], self.filename)

    def output(self):
        """
        Output the RSS feed file
        """
        self.ensure_output_path()
        dst = os.path.join(self.output_path, self.filename)
        self.feed.rss_file(dst, pretty=True)
