# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack

import os
import uuid
import pyblish.api


class ExtractGeometryMaxBinary(pyblish.api.InstancePlugin):
    '''Extract geometry as max binary.'''

    order = pyblish.api.ExtractorOrder

    families = ['ftrack', 'geometry']
    match = pyblish.api.Subset

    def deselect_all(self):
        '''Deselect all nodes.'''
        import MaxPlus
        MaxPlus.SelectionManager.ClearNodeSelection()

    def select_hierarchy(self, node):
        '''Select a node and all its children.'''
        import MaxPlus
        MaxPlus.SelectionManager.SelectNode(node, False)
        for c in node.Children:
            self.select_hierarchy(c)

    def process(self, instance):
        '''Process instance.'''
        import MaxPlus

        # Get the options.
        context_options = instance.context.data['options'].get(
            'max_binary', {}
        )
        self.log.debug(
            'Started extracting geometry {0!r} with options '
            '{1!r}.'.format(
                instance.name, context_options
            )
        )

        # Save and clear the selection.
        saved_selection = MaxPlus.SelectionManager.GetNodes()
        self.deselect_all()

        # Select our node and all its children.
        node = MaxPlus.INode.GetINodeByName(str(instance))
        self.select_hierarchy(node)

        # Write the Max scene.
        temporary_path = os.path.join(
            MaxPlus.PathManager.GetTempDir(), uuid.uuid4().hex + '.max')
        MaxPlus.FileManager.SaveSelected(temporary_path)

        # Save component info.
        name = instance.name
        new_component = {
            'name': '{0}.maxbinary'.format(name),
            'path': temporary_path,
        }

        instance.data['ftrack_components'].append(new_component)

        self.log.debug(
            'Extracted {0!r} from {1!r}'.format(new_component, instance.name)
        )

        # Restore the selection.
        self.deselect_all()
        MaxPlus.SelectionManager.SelectNodes(saved_selection)


pyblish.api.register_plugin(ExtractGeometryMaxBinary)
