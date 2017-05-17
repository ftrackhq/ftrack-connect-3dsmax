# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack

import pyblish.api


class CollectLightRigs(pyblish.api.ContextPlugin):
    '''Collect light rigs from 3DS Max.'''

    order = pyblish.api.CollectorOrder

    # From Max's SDK headers.
    LIGHT_SUPERCLASS_ID = 0x0030

    def __contains_lights_as_children(self, node):
        '''Return true if a node or any of its children is a light.'''
        for n in node.Children:
            if self.__contains_lights_as_children(n):
                return True

        return node.Object.SuperClassID == self.LIGHT_SUPERCLASS_ID

    def process(self, context):
        '''Process *context* and add max light rig instances.'''
        import MaxPlus

        # Build a set with the selection to check quickly if a node is selected.
        selection = set()
        for n in MaxPlus.SelectionManager.GetNodes():
            selection.add(n.GetName())

        self.log.debug('Started collecting light rigs from scene.')

        root = MaxPlus.Core.GetRootNode()
        for node in root.Children:
            if self.__contains_lights_as_children(node):
                name = node.GetName()
                instance = context.create_instance(
                    name, families=['ftrack', 'light']
                )

                instance.data['publish'] = name in selection
                instance.data['ftrack_components'] = []

                self.log.debug(
                    'Collected geometry instance {0!r} {1!r}.'.format(
                        name, instance
                    )
                )
