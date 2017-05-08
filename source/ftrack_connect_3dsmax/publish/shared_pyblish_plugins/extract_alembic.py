# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os
import uuid
import pyblish.api

class ExtractSceneAlembic(pyblish.api.InstancePlugin):
    '''Extract scene as alembic.'''

    order = pyblish.api.ExtractorOrder

    families = ['ftrack', 'scene']
    match = pyblish.api.Subset

    def exocortexAlembicAvailable(self):
        '''Check if Exocortex Crate Alembic plugin is available.
        Currently, we check if the AlembicCameraProperties modifier exists.
        '''
        import MaxPlus
        return MaxPlus.Core.EvalMAXScript(
            'findItem modifier.classes AlembicCameraProperties != 0'
        ).Get()

    def exocortexExportAlembic(self, filePath, options):
        '''Export an Alembic archive.'''
        import MaxPlus

        jobArgs = []

        if options.get('alembicExportMode') == 'Selection':
            jobArgs.append('exportSelected=true')

            # Check if the selection is empty and abort if it is.
            if MaxPlus.SelectionManager.GetNodes().GetCount() == 0:
                raise RuntimeError('Selection is empty')
        else:
            jobArgs.append('exportSelected=false')

        if options.get('alembicNormalsWrite'):
            jobArgs.append('normals=true')
        else:
            jobArgs.append('normals=false')

        if options.get('alembicUVWrite'):
            jobArgs.append('uvs=true')
        else:
            jobArgs.append('uvs=false')

        if options.get('alembicFlattenHierarchy'):
            jobArgs.append('flattenHierarchy=true')
        else:
            jobArgs.append('flattenHierarchy=false')

        if options.get('alembicAnimation'):
            jobArgs.append('in={0}'.format(options['frameStart']))
            jobArgs.append('out={0}'.format(options['frameEnd']))
            steps = options.get('samplesPerFrame', 1.0)
            jobArgs.append('subStep={0}'.format(int(math.ceil(steps))))
        else:
            jobArgs.append('in=0')
            jobArgs.append('out=0')

        argsString = ';'.join(jobArgs)
        cmd = 'ExocortexAlembic.createExportJobs(@"filename={0};{1}")'.format(
            filePath, argsString)

        MaxPlus.Core.EvalMAXScript(cmd)

    def process(self, instance):
        '''Process instance.'''
        import MaxPlus

        if not self.exocortexAlembicAvailable():
            self.log.warning('Exocortex plugin not available')
            return

        temporary_path = os.path.join(
            MaxPlus.PathManager.GetTempDir(), uuid.uuid4().hex + '.abc'
        )

        # TODO PASS OPTIONS
        self.exocortexExportAlembic(temporary_path, {})

        name = instance.name

        new_component = {
            'name': '{0}.alembic'.format(name),
            'path': temporary_path,
        }

        instance.data['ftrack_components'].append(new_component)
        self.log.debug(
            'Extracted {0!r} from {1!r}'.format(new_component, instance.name)
        )

pyblish.api.register_plugin(ExtractSceneAlembic)
