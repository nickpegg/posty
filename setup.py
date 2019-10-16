from setuptools import setup, find_packages

setup(
    name='posty',
    version='2.0.3',
    author='Nick Pegg',
    author_email='nick@nickpegg.com',
    url='https://github.com/nickpegg/posty',
    description='A static site generator',
    long_description="""
A simple static site generator tool. Reads in a series of posts and pages
containing YAML metadata and Markdown text, and renders them as HTML.
""",

    packages=find_packages(exclude=['tests', 'tests.*']),
    package_data={'posty': ['skel/*/**']},
    scripts=['bin/posty'],

    python_requires='>=3.5',
    install_requires=[
        'awesome-slugify>=1.6.5',
        'click>=6.7,<7.0',
        'feedgen>=0.6.1',
        'future>=0.16.0',
        'Jinja2>=2.10',
        'Markdown>=2.6.11',
        'pytz>=2017.3',
        'PyYAML>=5.1',
    ],
)
