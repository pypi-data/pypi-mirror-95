"""UNS library command line interface setup script."""
# pylama:ignore=D203,D102
import re

from os.path import join, dirname
from setuptools import setup, find_packages


# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'uns', '__init__.py')) as v_file:
    package_version = re.compile('.*__version__ = \'(.*?)\'', re.S).\
        match(v_file.read()).group(1)


dependencies = [
    'easycli >= 1.7.3',
    'requests',
]


setup(
    name='uns',
    version=package_version,
    py_modules=find_packages(),
    install_requires=dependencies,
    include_package_data=True,
    license='MIT',
    entry_points={
        'console_scripts': [
            'uns = uns.cli:UNS.quickstart',
        ]
    }
)
