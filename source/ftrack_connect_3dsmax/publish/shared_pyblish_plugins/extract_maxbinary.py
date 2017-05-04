# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os
import uuid
import pyblish.api

class ExtractSceneMaxBinary(pyblish.api.InstancePlugin):
    '''Extract scene as max binary.'''

    order = pyblish.api.ExtractorOrder

    families = ['ftrack', 'scene']
    match = pyblish.api.Subset

    def process(self, instance):
        '''Process *instance* and extract scene.'''
        import MaxPlus

        context_options = instance.context.data['options'].get(
            'max_binary', {}
        )

        self.log.debug(
            'Started extracting scene {0!r} with options '
            '{1!r}.'.format(
                instance.name, context_options
            )
        )

        temporary_path = os.path.join(
            MaxPlus.PathManager.GetTempDir(), uuid.uuid4().hex + '.max')
        MaxPlus.FileManager.Save(temporary_path, False, False)

        name = instance.name
        new_component = {
            'name': '{0}.maxbinary'.format(name),
            'path': temporary_path,
        }

        instance.data['ftrack_components'].append(new_component)

        self.log.debug(
            'Extracted {0!r} from {1!r}'.format(new_component, instance.name)
        )


pyblish.api.register_plugin(ExtractSceneMaxBinary)
