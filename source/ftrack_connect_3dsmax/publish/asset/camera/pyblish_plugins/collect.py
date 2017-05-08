# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import pyblish.api
import MaxPlus


class CollectCameras(pyblish.api.ContextPlugin):
    '''Collect cameras from 3DS Max.'''

    order = pyblish.api.CollectorOrder

    MAX_CAMERA_CLASS_ID = 32

    def __create_camera_instances(self, node, context, selection):
        if node.Object.SuperClassID == self.MAX_CAMERA_CLASS_ID:
            name = node.GetName()
            instance = context.create_instance(
                name, families=['ftrack', 'camera']
            )

            instance.data['publish'] = name in selection
            instance.data['ftrack_components'] = []

            self.log.debug(
                'Collected camera instance {0!r} {1!r}.'.format(
                    name, instance
                )
            )

        for c in node.Children:
            self.__create_camera_instances(c, context, selection)

    def process(self, context):
        '''Process *context* and add max camera instances.'''

        # Build a set with the selection to check quickly if a node is selected.
        selection = set()
        for n in MaxPlus.SelectionManager.GetNodes():
            selection.add(n.GetName())

        self.log.debug('Started collecting camera from scene.')

        root = MaxPlus.Core.GetRootNode()
        for c in root.Children:
            self.__create_camera_instances(c, context, selection)
