# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os
import getpass
import sys
import logging
import re

import ftrack
import ftrack_connect.application



def on_discover_3dsmax_integration(session, event):

    cwd = os.path.dirname(__file__)
    sources = os.path.abspath(os.path.join(cwd, '..', 'dependencies'))
    ftrack_connect_3dsmax_resource_path = os.path.abspath(os.path.join(cwd, '..', 'resource'))
    max_startup_dir = os.path.abspath(os.path.join(ftrack_connect_3dsmax_resource_path, 'scripts', 'startup'))
    max_startup_script = os.path.join(max_startup_dir, 'initftrack.ms')
    sys.path.append(sources)

    from ftrack_connect_3dsmax import __version__ as integration_version

    entity = event['data']['context']['selection'][0]
    task = session.get('Context', entity['entityId'])

    data = {
        'integration': {
                "name": 'ftrack-connect-3dsmax',
                'version': integration_version
        },
        'env': {
            'PATH.append': max_startup_dir,
            'FTRACK_TASKID.set': task['id'],
            'FTRACK_SHOTID.set': task['parent']['id'],
            'LOGNAME.set': session._api_user,
            'FTRACK_APIKEY.set': session._api_key,
            'FS.set': task['parent']['custom_attributes'].get('fstart', '1.0'),
            'FE.set': task['parent']['custom_attributes'].get('fend', '100.0')
        },
        'launch_arguments': ['-U', 'MAXScript', max_startup_script]
    }

    return data
