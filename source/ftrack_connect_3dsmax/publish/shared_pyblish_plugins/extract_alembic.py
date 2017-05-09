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

        jobArgs = ['exportSelected=false']

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

        ticks = MaxPlus.Core.EvalMAXScript('ticksperframe').GetInt()
        current_start_frame =  MaxPlus.Animation.GetAnimRange().Start() / ticks
        current_end_frame =  MaxPlus.Animation.GetAnimRange().End() / ticks

        # Extract options.
        context_options = instance.context.data['options'].get(
            'alembic', {}
        )
        animation = context_options.get('include_animation', False)
        uv_write = context_options.get('uv_write', True)
        normals_write = context_options.get('normals_write', True)
        start_frame = context_options.get('start_frame', current_start_frame)
        end_frame = context_options.get('end_frame', current_end_frame)
        sampling = context_options.get('sampling', 1.0)

        # Export the alembic file.
        temporary_path = os.path.join(
            MaxPlus.PathManager.GetTempDir(), uuid.uuid4().hex + '.abc'
        )

        self.exocortexExportAlembic(
            filePath=temporary_path,
            options={
                'alembicNormalsWrite' : normals_write,
                'alembicUVWrite' : uv_write,
                'alembicAnimation' : animation,
                'frameStart' : start_frame,
                'frameEnd' : end_frame,
                'samplesPerFrame' : sampling
            })

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
