from future.standard_library import install_aliases
install_aliases()   # noqa

import os
from urllib.parse import urljoin

from .feed import FeedRenderer


class AtomRenderer(FeedRenderer):
    filename = 'atom.xml'

    def url(self):
        """
        Return the URL to this feed file
        """
        return urljoin(self.site.config['full_url'], self.filename)

    def output(self):
        """
        Output the RSS feed file
        """
        self.ensure_output_path()
        dst = os.path.join(self.output_path, self.filename)
        self.feed.atom_file(dst, pretty=True)
