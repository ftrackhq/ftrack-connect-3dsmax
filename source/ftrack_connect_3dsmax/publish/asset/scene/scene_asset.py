# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack

import ftrack_connect_pipeline.asset


def filter_instances(pyblish_context):
    '''Return scene instances from *pyblish_context*.'''
    match = set(['scene', 'ftrack'])
    return filter(
        lambda instance: match.issubset(instance.data['families']),
        pyblish_context
    )


class PublishScene(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of 3dsmax scene.'''

    def get_options(self):
        '''Return global options.'''
        options = [
            {
                'type': 'group',
                'label': '3dsMax binary',
                'name': 'max_binary',
                'options': []
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
                    'name': 'normals_write',
                    'label': 'Normals write',
                    'type': 'boolean',
                    'value': True
                }]
            }
        ]

        default_options = super(PublishScene, self).get_options()

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
        return []
