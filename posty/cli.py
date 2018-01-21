import click
import os
import shutil

from .site import Site
from .importers import Posty1Importer


@click.group()
def cli():
    pass


@cli.command()
def init():
    """
    Initialize a Posty site
    """
    site = Site()
    site.init()

    click.echo('Posty initialized!')
    click.echo("""
Directories:
- posts -> Put all of your blog posts here
- pages -> Put all of your static pages here
- templates -> jinja2 HTML templates go here
- media -> Static files go here; JS, CSS, images, etc.

There is also a config file at config.yml that you should adjust to your
liking, like setting the site title and such.
    """)


@cli.command()
@click.option(
    '-o',
    '--output',
    help='Output directory',
    default='build'
)
@click.option(
    '-c',
    '--config',
    type=click.Path(exists=True),
    help='Path to your config file',
)
def build(output, config):
    """
    Build a Posty site as rendered HTML
    """
    site = Site()
    site.load()
    site.render(output_path=output)

    # Finally, copy media into the build directory
    shutil.copytree('media', os.path.join(output, 'media'))


@cli.group(name='new')
def _new():
    """
    Create a new post or page
    """
    pass


@_new.command()
@click.option(
    '--name',
    help='Name of the new page',
    default='New Page',
)
def page(name):
    """
    Create a new page from the template
    """
    site = Site()
    site.new_page(name=name)


@_new.command()
@click.option(
    '--name',
    help='Name of the new post',
    default='New Post',
)
def post(name):
    """
    Create a new page from the template
    """
    site = Site()
    site.new_post(name=name)


@cli.group(name='import')
def _import():
    """
    Import a site from another static site generator
    """
    pass


@_import.command()
@click.argument('path')
def posty1(path):
    """
    Import a Posty 1.x site from PATH
    """
    click.echo('Importing from {}...'.format(path))
    Posty1Importer(Site(), path).run()
    click.echo('Done!')
    click.echo((
        "In each of your posts, I've made blurbs using the first paragraph. "
        'Adjust to your own taste.'
    ))
    click.echo('You will also need to make sure to update your templates.')


if __name__ == '__main__':
    cli()
