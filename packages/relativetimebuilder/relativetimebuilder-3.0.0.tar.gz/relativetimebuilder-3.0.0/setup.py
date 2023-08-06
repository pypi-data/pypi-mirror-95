from os import path
from setuptools import setup, find_packages

with open(path.join('relativetimebuilder', 'version.py')) as f:
    exec(f.read())

THIS_DIRECTORY = path.abspath(path.dirname(__file__))
with open(path.join(THIS_DIRECTORY, 'README.rst')) as f:
    README_TEXT = f.read()

setup(
    name='relativetimebuilder',
    version=__version__,
    description='A library for using the dateutil relativedeltas for calendar precision with aniso8601',
    long_description=README_TEXT,
    long_description_content_type='text/x-rst',
    author='Brandon Nielsen',
    author_email='nielsenb@jetfuse.net',
    url='https://bitbucket.org/nielsenb/relativetimebuilder',
    install_requires=[
        'aniso8601>=9.0.0, <10.0.0',
        'python-dateutil>=2.7.3'
    ],
    packages=find_packages(),
    test_suite='relativetimebuilder',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='iso8601 dateutil aniso8601 datetime',
    project_urls={
        'Documentation': 'https://relativetimebuilder.readthedocs.io/',
        'Source': 'https://bitbucket.org/nielsenb/relativetimebuilder',
        'Tracker': 'https://bitbucket.org/nielsenb/relativetimebuilder/issues'
    }
)
