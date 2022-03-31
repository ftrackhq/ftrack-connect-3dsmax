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

cwd = os.path.dirname(__file__)
sources = os.path.abspath(os.path.join(cwd, '..', 'dependencies'))
ftrack_connect_3dsmax_resource_path = os.path.abspath(os.path.join(cwd, '..',  'resource'))



def on_discover_max_integration(session, event):
    
    sys.path.append(sources)

    from ftrack_connect_3dsmax import __version__ as integration_version

    data = {
        'integration': {
            'name': 'ftrack-connect-3dsmax',
            'version': integration_version
        }
    }

    return data

def on_launch_max_integration(session, event):
    max_base_data = on_discover_max_integration(session, event)

    maxStartupDir = os.path.abspath(os.path.join(ftrack_connect_3dsmax_resource_path, 'scripts', 'startup'))
    maxStartupScript = os.path.join(maxStartupDir, 'initftrack.ms')

    max_base_data['integration']['env'] = {
        'PATH':maxStartupDir,
        'PYTHONPATH.prepend':sources
    }
    max_base_data['integration']['launch_arguments'] =  ['-U', 'MAXScript', maxStartupScript]

    selection = event['data'].get('context', {}).get('selection', [])
    
    if selection:
        task = session.get('Context', selection[0]['entityId'])
        max_base_data['integration']['env']['FTRACK_TASKID.set'] =  task['id']
        max_base_data['integration']['env']['FTRACK_SHOTID.set'] =  task['parent']['id']
        max_base_data['integration']['env']['FS.set'] = task['parent']['custom_attributes'].get('fstart', '1.0')
        max_base_data['integration']['env']['FE.set'] = task['parent']['custom_attributes'].get('fend', '100.0')

    return max_base_data


def register(session):

    '''Subscribe to application launch events on *registry*.'''

    if not isinstance(session, ftrack_api.session.Session):
        return

    handle_discover_event = functools.partial(
        on_discover_max_integration,
        session
    )

    session.event_hub.subscribe(
        'topic=ftrack.connect.application.discover'
        ' and data.application.identifier=3ds-max*'
        ' and data.application.version <= 2020',
        handle_discover_event

    )

    handle_launch_event = functools.partial(
        on_launch_max_integration,
        session
    )    

    session.event_hub.subscribe(
        'topic=ftrack.connect.application.launch'
        ' and data.application.identifier=3ds-max*'
        ' and data.application.version <= 2020',
        handle_launch_event
    )

