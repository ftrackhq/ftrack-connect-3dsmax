# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack

import pyblish.api
import MaxPlus


class CollectRigs(pyblish.api.ContextPlugin):
    '''Collect rigs from 3DS Max.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add a max rig instance.'''
        self.log.debug('Started collecting geometry from scene.')

        instance = context.create_instance(
            'rig', families=['ftrack', 'rig']
        )
        instance.data['publish'] = True
        instance.data['ftrack_components'] = []
        self.log.debug('Collected scene instance {0!r}.'.format(instance))
