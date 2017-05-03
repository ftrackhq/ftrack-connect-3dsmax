# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os
import uuid
import pyblish.api
import MaxPlus

class ExtractCameraAlembic(pyblish.api.InstancePlugin):
    '''Extract camera as alembic.'''

    order = pyblish.api.ExtractorOrder

    families = ['ftrack', 'camera']
    match = pyblish.api.Subset

    def exocortexAlembicAvailable(self):
        '''Check if Exocortex Crate Alembic plugin is available.
        Currently, we check if the AlembicCameraProperties modifier exists.
        '''
        return MaxPlus.Core.EvalMAXScript(
            'findItem modifier.classes AlembicCameraProperties != 0'
        ).Get()

    def process(self, instance):
        '''Process instance.'''

        context_options = instance.context.data['options'].get(
            'alembic', {}
        )
        self.log.debug(
            'Started extracting camera {0!r} with options '
            '{1!r}.'.format(
                instance.name, context_options
            )
        )

        # Save and clear the selection.
        savedSelection = MaxPlus.SelectionManager.GetNodes()
        MaxPlus.Core.EvalMAXScript('max select none')

        camera = str(instance)
        MaxPlus.Core.EvalMAXScript('select {0}'.format(camera))

        # timeSliderRange = MaxPlus.Animation.GetAnimRange()
        # print range.Start() / 160 # Each frame in Max is 160 units.
        # print range.End() / 160

        jobArgs = [
            'exportSelected=true'
            # 'flattenHierarchy=true'
            # 'in={0}'.format(options['frameStart'])
            # 'out={0}'.format(options['frameEnd'])
            # 'subStep={0}'.format(int(math.ceil(steps)))
        ]

        temporaryPath = os.path.join(
            MaxPlus.PathManager.GetTempDir() + uuid.uuid4().hex + '.abc')

        argsString = ';'.join(jobArgs)
        cmd = 'ExocortexAlembic.createExportJobs(@"filename={0};{1}")'.format(
            temporaryPath,
            argsString
        )
        # MaxPlus.Core.EvalMAXScript(cmd)

        # Restore the selection.
        MaxPlus.SelectionManager.SelectNodes(savedSelection)


pyblish.api.register_plugin(ExtractCameraAlembic)
