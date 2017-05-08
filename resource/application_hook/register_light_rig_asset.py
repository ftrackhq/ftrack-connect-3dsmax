# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack

import functools

import ftrack_api
import ftrack_connect_pipeline.asset

from ftrack_connect_3dsmax.publish.asset.light_rig import light_rig_asset

FTRACK_ASSET_TYPE = 'lgt'

def create_asset_publish():
    '''Return asset publisher.'''
    return light_rig_asset.PublishLightRig(
        description='publish 3dsmax light rig to ftrack.',
        enable_scene_as_reference=False,
        asset_type_short=FTRACK_ASSET_TYPE
    )


def register_asset_plugin(session, event):
    '''Register asset plugin.'''
    light_rig = ftrack_connect_pipeline.asset.Asset(
        identifier=FTRACK_ASSET_TYPE,
        label='Light Rig',
        icon='wb-incandescent',
        create_asset_publish=create_asset_publish
    )
    light_rig.register(session)


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    session.event_hub.subscribe(
        'topic=ftrack.pipeline.register-assets',
        functools.partial(register_asset_plugin, session)
    )
