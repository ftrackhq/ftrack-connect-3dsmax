# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack

import os
import uuid
import pyblish.api


class ExtractCameraMaxBinary(pyblish.api.InstancePlugin):
    '''Extract camera as max binary.'''

    order = pyblish.api.ExtractorOrder

    families = ['ftrack', 'camera']
    match = pyblish.api.Subset

    def deselect_all(self):
        '''Deselect all nodes.'''
        import MaxPlus
        MaxPlus.SelectionManager.ClearNodeSelection()

    def process(self, instance):
        '''Process instance.'''
        import MaxPlus

        # Get the options.
        context_options = instance.context.data['options'].get(
            'max_binary', {}
        )
        self.log.debug(
            'Started extracting camera {0!r} with options '
            '{1!r}.'.format(
                instance.name, context_options
            )
        )

        # Save the selection and select our camera.
        saved_selection = MaxPlus.SelectionManager.GetNodes()
        self.deselect_all()
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
        self.deselect_all()
        MaxPlus.SelectionManager.SelectNodes(saved_selection)


pyblish.api.register_plugin(ExtractCameraMaxBinary)
