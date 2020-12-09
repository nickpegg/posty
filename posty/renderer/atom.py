from future.standard_library import install_aliases

import os
from urllib.parse import urljoin

from .feed import FeedRenderer

install_aliases()   # noqa


class AtomRenderer(FeedRenderer):
    """
    Renderer that outputs an Atom feed XML file
    """
    filename = 'atom.xml'

    def url(self):
        """
        Return the URL to this feed file
        """
        return urljoin(self.site.config['base_url'], self.filename)

    def output(self):
        """
        Output the Atom feed file
        """
        self.ensure_output_path()
        dst = os.path.join(self.output_path, self.filename)
        self.feed.atom_file(dst, pretty=True)
