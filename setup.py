from distutils.core import setup

setup(
    name='Posty',
    version='2.0',
    author='Nick Pegg',
    author_email='nick@nickpegg.com',
    url='https://github.com/nickpegg/posty',
    description='A static site generator',
    long_description=open('README.md').read(),

    packages=['posty'],
    package_data={'posty': ['skel/*/.keep']},
    scripts=['bin/posty'],

    python_requires='>=2.7',
    install_requires=[
        'awesome-slugify>=1.6.5,<1.7.0',
        'click>=6.7,<7.0',
        'future>=0.16.0,<0.17.0',
        'Jinja2>=2.10,<3.0',
        'Markdown>=2.6.11,<2.7.0',
        'PyYAML>=3.12,<4.0',
    ],
)
