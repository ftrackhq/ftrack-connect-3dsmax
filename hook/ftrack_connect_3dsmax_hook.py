# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os
import getpass
import sys
import logging
import re

import ftrack
import ftrack_connect.application
from ftrack_connect.session import get_shared_session

maxStartupDir = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), '..', 'ftrack_connect_3dsmax', 'scripts',
        'startup'
    )
)
maxStartupScript = os.path.join(maxStartupDir, 'initftrack.ms')



class LaunchAction(object):
    '''ftrack connect 3ds Max discover and launch action.'''

    identifier = 'ftrack-connect-launch-3dsmax'

    def __init__(self, applicationStore, launcher):
        '''Initialise action with *applicationStore* and *launcher*.

        *applicationStore* should be an instance of
        :class:`ftrack_connect.application.ApplicationStore`.

        *launcher* should be an instance of
        :class:`ftrack_connect.application.ApplicationLauncher`.

        '''
        super(LaunchAction, self).__init__()

        self.logger = logging.getLogger(
            __name__ + '.' + self.__class__.__name__
        )

        self.applicationStore = applicationStore
        self.launcher = launcher
        self.session = launcher.session

    def register(self):
        '''Override register to filter discover actions on logged in user.'''
        ftrack.EVENT_HUB.subscribe(
            'topic=ftrack.action.discover and source.user.username={0}'.format(
                getpass.getuser()
            ),
            self.discover
        )

        ftrack.EVENT_HUB.subscribe(
            'topic=ftrack.action.launch and source.user.username={0} '
            'and data.actionIdentifier={1}'.format(
                getpass.getuser(), self.identifier
            ),
            self.launch
        )

        ftrack.EVENT_HUB.subscribe(
            'topic=ftrack.connect.plugin.debug-information',
            self.get_version_information
        )

    def is_valid_selection(self, selection):
        '''Return true if the selection is valid.'''
        if (
            len(selection) != 1 or
            selection[0]['entityType'] not in ['task', 'Component']
        ):
            return False


        ftrack_entity = None
        entity = selection[0]

        if entity['entityType'] == 'task':
            ftrack_entity = self.session.get('Task', entity['entityId'])

        elif entity['entityType'] == 'Component':
            ftrack_entity = self.session.get('Component', entity['entityId'])

        if ftrack_entity and ftrack_entity.entity_type not in ['Task', 'FileComponent']:
            return False


        return True

    def discover(self, event):
        '''Return discovered applications.'''

        if not self.is_valid_selection(event['data'].get('selection', [])):
            return

        items = []
        applications = self.applicationStore.applications
        applications = sorted(
            applications,
            key=lambda application: application['label']
        )

        for application in applications:
            applicationIdentifier = application['identifier']
            label = application['label']
            items.append({
                'actionIdentifier': self.identifier,
                'label': label,
                'variant': application.get('variant', None),
                'description': application.get('description', None),
                'icon': application.get('icon', 'default'),
                'applicationIdentifier': applicationIdentifier
            })

        return {
            'items': items
        }

    def launch(self, event):
        '''Handle launch *event*.'''
        applicationIdentifier = (
            event['data']['applicationIdentifier']
        )

        applicationIdentifier = event['data']['applicationIdentifier']
        context = event['data'].copy()
        context['source'] = event['source']

        return self.launcher.launch(
            applicationIdentifier, context
        )

    def get_version_information(self, event):
        '''Return version information.'''
        import ftrack_connect_3dsmax
        return dict(
            name='ftrack connect 3ds max',
            version=ftrack_connect_3dsmax.__version__
        )


class ApplicationStore(ftrack_connect.application.ApplicationStore):
    '''Discover and store 3ds Max on this host.'''

    def _discoverApplications(self):
        '''Return a list of applications that can be launched from this host.

        An application should be of the form:

            dict(
                'identifier': 'name_version',
                'label': 'Name',
                'variant': 'version',
                'description': 'description',
                'path': 'Absolute path to the file',
                'version': 'Version of the application',
                'icon': 'URL or name of predefined icon'
            )

        '''
        applications = []

        if sys.platform == 'win32':
            prefix = ['C:\\', 'Program Files.*']

            version_expression = re.compile(
                r'3ds Max (?P<version>[\d.]+)'
            )

            applications.extend(self._searchFilesystem(
                expression=prefix + ['Autodesk', '3ds Max.+', '^3dsmax.exe$'],
                versionExpression=version_expression,
                label='3ds Max',
                variant='{version}',
                applicationIdentifier='3ds_max_{version}',
                icon='3ds_max',
                launchArguments=['-U', 'MAXScript', maxStartupScript]
            ))

        return applications


class ApplicationLauncher(ftrack_connect.application.ApplicationLauncher):
    '''Launch 3ds Max.'''

    def _getApplicationEnvironment(self, application, context):
        '''Modify and return environment with 3ds Max added.'''
        environment = super(
            ApplicationLauncher, self
        )._getApplicationEnvironment(
            application, context
        )

        ftrack_connect.application.appendPath(
            maxStartupDir,
            'PATH',
            environment
        )

        entity = context['selection'][0]
        if entity['entityType'] != 'Component':

            task = self.session.get(
                'Task', entity['entityId']
            )

        else:
            component = self.session.get(
                'Component', entity['entityId']
            )
            self.logger.info(component['version'].items())
            task = component['version']['asset']['parent']

        task_parent = task['parent']
        task_parent_attributes = task_parent['custom_attributes']

        try:
            environment['FS'] = str(int(task_parent_attributes['fstart']))
        except Exception:
            environment['FS'] = '1'

        try:
            environment['FE'] = str(int(task_parent_attributes['fend']))
        except Exception:
            environment['FE'] = '1'

        environment['FTRACK_TASKID'] = task['id']
        environment['FTRACK_SHOTID'] = task_parent['id']


        pypath = environment['PYTHONPATH'].split(';')
        if pypath:
            import imp
            modulesToRemove = ['PySide', 'PySide2']
            pathsToRemove = []
            for m in modulesToRemove:
                try:
                    modulePath = imp.find_module(m)[1]
                    pathsToRemove.append(os.path.dirname(modulePath))
                except ImportError:
                    pass

            for i, path in enumerate(pypath):
                if path in pathsToRemove:
                    pypath.pop(i)

        environment['PYTHONPATH'] = ';'.join(pypath)

        return environment


def register(registry, **kw):
    '''Register hooks.'''

    # Validate that registry is an instance of ftrack.Registry. If not,
    # assume that register is being called from a new or incompatible API and
    # return without doing anything.
    if registry is not ftrack.EVENT_HANDLERS:
        return

    applicationStore = ApplicationStore()
    launcher = ApplicationLauncher(applicationStore)

    # Create action and register to respond to discover and launch events.
    action = LaunchAction(applicationStore, launcher)
    action.register()
