# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack

import MaxPlus
import ftrack_connect_pipeline.asset

def filter_instances(pyblish_context):
    '''Return geometry instances from *pyblish_context*.'''
    match = set(['geometry', 'ftrack'])
    return filter(
        lambda instance: match.issubset(instance.data['families']),
        pyblish_context
    )


class PublishGeometry(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of 3dsmax geometries.'''

    def get_options(self):
        '''Return global options.'''
        options = [
            {
                'type': 'group',
                'label': '3dsMax binary',
                'name': 'max_binary',
                'options': [{
                    'name': 'reference',
                    'label': 'Reference',
                    'type': 'boolean',
                }, {
                    'name': 'history',
                    'label': 'History',
                    'type': 'boolean',
                }, {
                    'name': 'channels',
                    'label': 'Channels',
                    'type': 'boolean',
                    'value': True
                }, {
                    'name': 'expressions',
                    'label': 'Expressions',
                    'type': 'boolean',
                    'value': True
                }, {
                    'name': 'constraints',
                    'label': 'Constraints',
                    'type': 'boolean',
                    'value': True
                }, {
                    'name': 'shaders',
                    'label': 'Shaders',
                    'type': 'boolean',
                    'value': True
                }]
            },
            {
                'type': 'group',
                'label': 'Alembic',
                'name': 'alembic',
                'options': [{
                    'name': 'include_animation',
                    'label': 'Include animation',
                    'type': 'boolean',
                    'value': True
                }, {
                    'name': 'uv_write',
                    'label': 'UV write',
                    'type': 'boolean',
                    'value': True
                }, {
                    'name': 'world_space',
                    'label': 'World space',
                    'type': 'boolean',
                    'value': True
                }, {
                    'name': 'write_visibility',
                    'label': 'Write visibility',
                    'type': 'boolean',
                    'value': True
                }]
            },
            {
                'type': 'group',
                'label': 'Geometry options',
                'name': 'geometry_options',
                'options': [{
                    'name': 'lock',
                    'label': 'Lock',
                    'type': 'boolean'
                }, {
                    'name': 'bake',
                    'label': 'Bake',
                    'type': 'boolean'
                }]
            }
        ]

        default_options = super(Geometry, self).get_options()

        return default_options + options

    def get_publish_items(self):
        '''Return list of items that can be published.'''
        options = []
        for instance in filter_instances(self.pyblish_context):
            options.append(
                {
                    'label': instance.name,
                    'name': instance.id,
                    'value': instance.data.get('publish', False)
                }
            )

        return options

    def get_item_options(self, name):
        '''Return options for publishable item with *name*.'''
        return []

    def get_scene_selection(self):
        '''Return a list of instance ids for scene selection.'''

        # Build a set with the selection to check quickly if a node is selected.
        selection = set()
        for n in MaxPlus.SelectionManager.GetNodes():
            selection.add(n.GetName())

        # Return list of instance ids for selected items in scene that match the
        # family.
        return [
            instance.id for instance in filter_instances(self.pyblish_context)
            if instance.name in selection
        ]
