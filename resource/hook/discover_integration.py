# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack


import functools
import getpass
import sys
import pprint
import logging
import re
import os
import ftrack_api


def on_discover_integration(session, event):

    cwd = os.path.dirname(__file__)
    sources = os.path.abspath(os.path.join(cwd, '..', 'dependencies'))
    ftrack_connect_3dsmax_resource_path = os.path.abspath(os.path.join(cwd, '..',  'resource'))
    maxStartupDir = os.path.abspath(os.path.join(ftrack_connect_3dsmax_resource_path, 'scripts', 'startup'))
    maxStartupScript = os.path.join(maxStartupDir, 'initftrack.ms')
    sys.path.append(sources)


    from ftrack_connect_3dsmax import __version__ as integration_version

    entity = event['data']['context']['selection'][0]
    task = session.get('Context', entity['entityId'])

    data = {
        'integration': {
            "name": 'ftrack-connect-3dsmax',
            'version': integration_version,
            'env': {
                'PATH':maxStartupDir,
                'PYTHONPATH.prepend':sources,
                'FTRACK_TASKID.set': task['id'],
                'FTRACK_SHOTID.set': task['parent']['id'],
                'FS.set': task['parent']['custom_attributes'].get('fstart', '1.0'),
                'FE.set': task['parent']['custom_attributes'].get('fend', '100.0')
            },
            'launch_arguments': ['-U', 'MAXScript', maxStartupScript]
        }
    }

    return data



def register(session):

    '''Subscribe to application launch events on *registry*.'''

    if not isinstance(session, ftrack_api.session.Session):
        return

    handle_event = functools.partial(
        on_discover_integration,
        session
    )

    session.event_hub.subscribe(
        'topic=ftrack.connect.application.launch'
        ' and data.application.identifier=3ds-max*'
        ' and data.application.version <= 2020',
        handle_event
    )

    session.event_hub.subscribe(
        'topic=ftrack.connect.application.discover'
        ' and data.application.identifier=3ds-max*'
        ' and data.application.version <= 2020',
        handle_event

    )