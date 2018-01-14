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
)
