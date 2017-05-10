# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack

import os
import uuid
import math
import pyblish.api

class ExtractGeometryAlembic(pyblish.api.InstancePlugin):
    '''Extract geometry as alembic.'''

    order = pyblish.api.ExtractorOrder

    families = ['ftrack', 'geometry']
    match = pyblish.api.Subset

    def exocortexAlembicAvailable(self):
        '''Check if Exocortex Crate Alembic plugin is available.
        Currently, we check if the AlembicCameraProperties modifier exists.
        '''
        import MaxPlus
        return MaxPlus.Core.EvalMAXScript(
            'findItem modifier.classes AlembicCameraProperties != 0'
        ).Get()

    def exocortexExportAlembic(self, file_path, options):
        '''Export an Alembic archive.'''
        import MaxPlus

        job_args = ['exportSelected=true']

        if options.get('alembicNormalsWrite'):
            job_args.append('normals=true')
        else:
            job_args.append('normals=false')

        if options.get('alembicUVWrite'):
            job_args.append('uvs=true')
        else:
            job_args.append('uvs=false')

        if options.get('alembicFlattenHierarchy'):
            job_args.append('flattenHierarchy=true')
        else:
            job_args.append('flattenHierarchy=false')

        if options.get('alembicAnimation'):
            job_args.append('in={0}'.format(options['frameStart']))
            job_args.append('out={0}'.format(options['frameEnd']))
            steps = options.get('samplesPerFrame', 1.0)
            job_args.append('subStep={0}'.format(int(math.ceil(steps))))
        else:
            job_args.append('in=0')
            job_args.append('out=0')

        argsString = ';'.join(job_args)
        cmd = 'ExocortexAlembic.createExportJobs(@"filename={0};{1}")'.format(
            file_path, argsString)

        MaxPlus.Core.EvalMAXScript(cmd)

    def process(self, instance):
        '''Process instance.'''
        import MaxPlus

        if not self.exocortexAlembicAvailable():
            self.log.warning('Exocortex plugin not available')
            return

        # Save and clear the selection.
        saved_selection = MaxPlus.SelectionManager.GetNodes()
        MaxPlus.Core.EvalMAXScript('max select none')
        MaxPlus.Core.EvalMAXScript('select ${0}'.format(str(instance)))

        # Extract options.
        context_options = instance.context.data['options'].get(
            'alembic', {}
        )
        self.log.debug(
            'Started extracting geometry {0!r} with options '
            '{1!r}.'.format(
                instance.name, context_options
            )
        )

        ticks_per_frame = MaxPlus.Core.EvalMAXScript('ticksperframe').GetInt()
        current_start_frame =  MaxPlus.Animation.GetAnimRange().Start() / ticks_per_frame
        current_end_frame =  MaxPlus.Animation.GetAnimRange().End() / ticks_per_frame

        animation = context_options.get('include_animation', False)
        uv_write = context_options.get('uv_write', True)
        normals_write = context_options.get('normals_write', True)
        start_frame = context_options.get('start_frame', current_start_frame)
        end_frame = context_options.get('end_frame', current_end_frame)
        flatten_hierarchy = context_options.get('flatten_hierarchy', False)
        sampling = context_options.get('sampling', 1.0)

        # Export the alembic file.
        temporary_path = os.path.join(
            MaxPlus.PathManager.GetTempDir(), uuid.uuid4().hex + '.abc'
        )

        self.exocortexExportAlembic(
            file_path=temporary_path,
            options={
                'alembicNormalsWrite': normals_write,
                'alembicUVWrite': uv_write,
                'alembicFlattenHierarchy': flatten_hierarchy,
                'alembicAnimation': animation,
                'frameStart': start_frame,
                'frameEnd': end_frame,
                'samplesPerFrame': sampling
            })

        # Save component info.
        name = instance.name
        new_component = {
            'name': '{0}.alembic'.format(name),
            'path': temporary_path,
        }

        instance.data['ftrack_components'].append(new_component)
        self.log.debug(
            'Extracted {0!r} from {1!r}'.format(new_component, instance.name)
        )

        # Restore the selection.
        MaxPlus.Core.EvalMAXScript('max select none')
        MaxPlus.SelectionManager.SelectNodes(saved_selection)

pyblish.api.register_plugin(ExtractGeometryAlembic)
