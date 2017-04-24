# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os
import re
import glob

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


ROOT_PATH = os.path.dirname(
    os.path.realpath(__file__)
)

RESOURCE_PATH = os.path.join(
    ROOT_PATH, 'resource'
)

SOURCE_PATH = os.path.join(
    ROOT_PATH, 'source'
)

README_PATH = os.path.join(ROOT_PATH, 'README.rst')

with open(os.path.join(
    SOURCE_PATH, 'ftrack_connect_3dsmax', '_version.py')
) as _version_file:
    VERSION = re.match(
        r'.*__version__ = \'(.*?)\'', _version_file.read(), re.DOTALL
    ).group(1)


# Custom commands.
class PyTest(TestCommand):
    '''Pytest command.'''

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        '''Import pytest and run.'''
        import pytest
        errno = pytest.main(self.test_args)
        raise SystemExit(errno)


def get_files_from_folder(folder):
    '''Get all files in a folder in resource folder.'''
    plugin_directory = os.path.join(RESOURCE_PATH, folder)
    plugin_data_files = []

    for root, directories, files in os.walk(plugin_directory):
        files_list = []
        if files:
            for filename in files:
                files_list.append(
                    os.path.join(root, filename)
                )

        if files_list:
            destination_folder = root.replace(
                RESOURCE_PATH, 'ftrack_connect_3dsmax/ftrack_connect_3dsmax'
            )
            plugin_data_files.append(
                (destination_folder, files_list)
            )

    return plugin_data_files

data_files = []

for child in os.listdir(
    RESOURCE_PATH
):
    if os.path.isdir(os.path.join(RESOURCE_PATH, child)) and child != 'hook':
        data_files += get_files_from_folder(child)

data_files.append(
    (
        'ftrack_connect_3dsmax/hook',
        glob.glob(os.path.join(ROOT_PATH, 'hook', '*.py'))
    )
)


# Configuration.
setup(
    name='ftrack connect 3dsmax',
    version=VERSION,
    description='3ds Max integration with ftrack.',
    long_description=open(README_PATH).read(),
    keywords='',
    url='https://bitbucket.org/ftrack/ftrack-connect-3dsmax',
    author='ftrack',
    author_email='support@ftrack.com',
    license='Apache License (2.0)',
    packages=find_packages(SOURCE_PATH),
    package_dir={
        '': 'source'
    },
    setup_requires=[
        'sphinx >= 1.2.2, < 2',
        'sphinx_rtd_theme >= 0.1.6, < 2',
        'lowdown >= 0.1.0, < 1',
    ],
    install_requires=[
        'clique==1.3.1',
        'pyblish-base >= 1.4.3',
    ],
    tests_require=[
        'pytest >= 2.3.5, < 3'
    ],
    cmdclass={
        'test': PyTest
    },
    data_files=data_files
)
