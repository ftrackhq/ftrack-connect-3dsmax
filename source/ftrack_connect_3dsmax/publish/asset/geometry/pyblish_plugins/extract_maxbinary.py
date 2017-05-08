# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os
import uuid
import pyblish.api


class ExtractGeometryMaxBinary(pyblish.api.InstancePlugin):
    '''Extract geometry as max binary.'''

    order = pyblish.api.ExtractorOrder

    families = ['ftrack', 'geometry']
    match = pyblish.api.Subset

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

        # Save the selection and select our geometry root node.
        saved_selection = MaxPlus.SelectionManager.GetNodes()
        MaxPlus.Core.EvalMAXScript('max select none')
        MaxPlus.Core.EvalMAXScript('select ${0}'.format(str(instance)))

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
        MaxPlus.Core.EvalMAXScript('max select none')
        MaxPlus.SelectionManager.SelectNodes(saved_selection)


pyblish.api.register_plugin(ExtractGeometryMaxBinary)
