import click

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
- templates -> jinja2 HTML templates go here, a base set has been provided
- static -> Static files go here

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
def build(output):
    """
    Build a Posty site as rendered HTML
    """
    site = Site()
    site.build(output_path=output)


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
