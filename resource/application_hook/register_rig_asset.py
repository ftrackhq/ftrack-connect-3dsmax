# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack

import functools

import ftrack_api
import ftrack_connect_pipeline.asset

from ftrack_connect_3dsmax.publish.asset.rig import rig_asset

FTRACK_ASSET_TYPE = 'rig'


def create_asset_publish():
    '''Return asset publisher.'''
    return rig_asset.PublishRig(
        description='publish 3dsmax rig to ftrack.',
        enable_scene_as_reference=False,
        asset_type_short=FTRACK_ASSET_TYPE
    )


def register_asset_plugin(session, event):
    '''Register asset plugin.'''
    rig = ftrack_connect_pipeline.asset.Asset(
        identifier=FTRACK_ASSET_TYPE,
        label='Rig',
        icon='extension',
        create_asset_publish=create_asset_publish
    )
    rig.register(session)


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    session.event_hub.subscribe(
        'topic=ftrack.pipeline.register-assets',
        functools.partial(register_asset_plugin, session)
    )
