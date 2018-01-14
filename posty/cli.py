import click
import os
import shutil

from .site import Site


@click.group()
def cli():
    pass


@cli.command()
def init():
    """
    Initialize a Posty site
    """
    skel_path = os.path.join(os.path.dirname(__file__), 'skel')

    for d in os.listdir(skel_path):
        src = os.path.join(skel_path, d)
        if not os.path.exists(d):
            shutil.copytree(src, d)

    click.echo('Posty initialized!')
    click.echo("""
Directories:
- posts -> Put all of your blog posts here
- pages -> Put all of your static pages here
- templates -> jinja2 HTML templates go here, a base set has been provided
- static -> Static files go here
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
    click.echo(path)
    # TODO: write this


if __name__ == '__main__':
    cli()
