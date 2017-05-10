# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack

import pyblish.api


class CollectGeometries(pyblish.api.ContextPlugin):
    '''Collect geometries from 3DS Max.'''

    order = pyblish.api.CollectorOrder

    # From Max's SDK headers.
    GEN_DERIVOB_SUPERCLASS_ID   = 0x0002
    GEOM_SUPERCLASS_ID          = 0x0010
    SHAPE_SUPERCLASS_ID         = 0x0040
    UTILITY_CLASS_ID_PART_A     = 0x1020
    BONE_CLASS_ID               = (0x28bf6e8d, 0x2ecca840)

    def __contains_geom_as_children(self, node):
        for n in node.Children:
            if self.__contains_geom_as_children(n):
                return True

        obj = node.Object
        superclass_id = obj.SuperClassID

        if superclass_id == self.GEOM_SUPERCLASS_ID:
            class_id = obj.ClassID

            if class_id.GetPartA() == self.UTILITY_CLASS_ID_PART_A:
                return False # Skip utility classes.

            if (class_id.GetPartA(), class_id.GetPartB()) == self.BONE_CLASS_ID:
                return False # Skip bones.

            return True
        elif superclass_id == self.SHAPE_SUPERCLASS_ID:
            return True
        elif superclass_id == self.GEN_DERIVOB_SUPERCLASS_ID:
            return True
        else:
            return False

    def process(self, context):
        '''Process *context* and add max geometry instances.'''
        import MaxPlus

        # Build a set with the selection to check quickly if a node is selected.
        selection = set()
        for n in MaxPlus.SelectionManager.GetNodes():
            selection.add(n.GetName())

        self.log.debug('Started collecting geometry from scene.')

        root = MaxPlus.Core.GetRootNode()
        for node in root.Children:
            if self.__contains_geom_as_children(node):
                name = node.GetName()
                instance = context.create_instance(
                    name, families=['ftrack', 'geometry']
                )

                instance.data['publish'] = name in selection
                instance.data['ftrack_components'] = []

                self.log.debug(
                    'Collected geometry instance {0!r} {1!r}.'.format(
                        name, instance
                    )
                )
