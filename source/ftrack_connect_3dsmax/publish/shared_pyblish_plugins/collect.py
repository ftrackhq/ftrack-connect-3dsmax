# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack

import pyblish.api


class CollectScene(pyblish.api.ContextPlugin):
    '''Collect 3dsmax scene.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add scene instances.'''
        self.log.debug('Started collecting geometry from scene.')

        instance = context.create_instance(
            'scene', families=['ftrack', 'scene']
        )
        instance.data['publish'] = True
        instance.data['ftrack_components'] = []
        self.log.debug('Collected scene instance {0!r}.'.format(instance))


pyblish.api.register_plugin(CollectScene)
