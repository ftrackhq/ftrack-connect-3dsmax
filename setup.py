# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os
import re
import shutil
import sys

from setuptools.command.test import test as TestCommand
from setuptools import setup, find_packages, Command
from pkg_resources import parse_version


import subprocess
# Define paths

PLUGIN_NAME = 'ftrack-connect-3dsmax-{0}'

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

RESOURCE_PATH = os.path.join(ROOT_PATH, 'resource')

SOURCE_PATH = os.path.join(ROOT_PATH, 'source')

README_PATH = os.path.join(ROOT_PATH, 'README.rst')

BUILD_PATH = os.path.join(ROOT_PATH, 'build')

STAGING_PATH = os.path.join(BUILD_PATH, PLUGIN_NAME)

EXOCORTEX_PLUGIN_PATH = os.path.join(RESOURCE_PATH, 'ExocortexCrate')

MAX_SCRIPTS_PATH = os.path.join(RESOURCE_PATH, 'scripts')

HOOK_PATH = os.path.join(RESOURCE_PATH, 'hook')

# Parse package version
with open(os.path.join(
    SOURCE_PATH, 'ftrack_connect_3dsmax', '_version.py')
) as _version_file:
    VERSION = re.match(
        r'.*__version__ = \'(.*?)\'', _version_file.read(), re.DOTALL
    ).group(1)


# Update staging path with the plugin version
STAGING_PATH = STAGING_PATH.format(VERSION)


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


class BuildPlugin(Command):
    '''Build plugin.'''

    description = 'Download dependencies and build plugin .'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        '''Run the build step.'''
        # Clean staging path
        shutil.rmtree(STAGING_PATH, ignore_errors=True)

        # Copy scripts files
        shutil.copytree(
            MAX_SCRIPTS_PATH,
            os.path.join(STAGING_PATH, 'resource', 'scripts')
        )

        # Copy plugin files
        shutil.copytree(
            EXOCORTEX_PLUGIN_PATH,
            os.path.join(STAGING_PATH, 'resource', 'ExocortexCrate')
        )

        # Copy hook files
        shutil.copytree(
            HOOK_PATH,
            os.path.join(STAGING_PATH, 'hook')
        )

        # Install local dependencies
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install','.','--target',
            os.path.join(STAGING_PATH, 'dependencies')]
        )


        # Generate plugin zip
        shutil.make_archive(
            os.path.join(
                BUILD_PATH,
                PLUGIN_NAME.format(VERSION)
            ),
            'zip',
            STAGING_PATH
        )

# Configuration.
setup(
    name='ftrack connect 3dsmax',
    version=VERSION,
    description='3ds Max integration with ftrack.',
    long_description=open(README_PATH).read(),
    keywords='ftrack, connect, connector, 3dsmax, autodesk',
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
        'lowdown >= 0.1.0, < 1'
    ],
    install_requires=[
        'appdirs',
        'qtext @ git+https://bitbucket.org/ftrack/qtext/get/0.2.2.zip#egg=QtExt-0.2.2',
        'ftrack-connector-legacy @ git+https://bitbucket.org/ftrack/ftrack-connector-legacy/get/1.0.0.zip#egg=ftrack-connector-legacy-1.0.0',

    ],
    tests_require=[
        'pytest >= 2.3.5, < 3'
    ],
    cmdclass={
        'test': PyTest,
        'build_plugin': BuildPlugin,
    },
    python_requires=">=2.7.9, <3"
)
