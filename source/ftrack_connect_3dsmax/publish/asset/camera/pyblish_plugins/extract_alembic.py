# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack

import os
import uuid
import math
import pyblish.api


class ExtractCameraAlembic(pyblish.api.InstancePlugin):
    '''Extract camera as alembic.'''

    order = pyblish.api.ExtractorOrder

    families = ['ftrack', 'camera']
    match = pyblish.api.Subset

    def exocortex_alembic_available(self):
        '''Check if Exocortex Crate Alembic plugin is available.
        Currently, we check if the AlembicCameraProperties modifier exists.
        '''
        import MaxPlus
        return MaxPlus.Core.EvalMAXScript(
            'findItem modifier.classes AlembicCameraProperties != 0'
        ).Get()

    def deselect_all(self):
        '''Deselect all nodes.'''
        import MaxPlus
        MaxPlus.SelectionManager.ClearNodeSelection()

    def process(self, instance):
        '''Process instance.'''
        import MaxPlus

        if not self.exocortex_alembic_available():
            self.log.warning('Exocortex plugin not available')
            return

        # Save and clear the selection, select our camera.
        saved_selection = MaxPlus.SelectionManager.GetNodes()
        self.deselect_all()
        MaxPlus.Core.EvalMAXScript('select ${0}'.format(str(instance)))

        # Extract options.
        context_options = instance.context.data['options'].get(
            'alembic', {}
        )
        self.log.debug(
            'Started extracting camera {0!r} with options '
            '{1!r}.'.format(
                instance.name, context_options
            )
        )

        # Prepare alembic export args.
        job_args = [
            'exportSelected=true',
            'flattenHierarchy=false'
        ]

        if  context_options.get('include_animation', False):
            ticks_per_frame = MaxPlus.Core.EvalMAXScript('ticksperframe').GetInt()
            current_start_frame =  MaxPlus.Animation.GetAnimRange().Start() / ticks_per_frame
            current_end_frame =  MaxPlus.Animation.GetAnimRange().End() / ticks_per_frame
            sampling = context_options.get('sampling', 1.0)

            job_args.append('in={0}'.format(context_options.get('start_frame', current_start_frame)))
            job_args.append('out={0}'.format(context_options.get('end_frame', current_end_frame)))
            job_args.append('subStep={0}'.format(int(math.ceil(sampling))))
        else:
            job_args.append('in=0')
            job_args.append('out=0')

        # Export the alembic file.
        temporary_path = os.path.join(
            MaxPlus.PathManager.GetTempDir(), uuid.uuid4().hex + '.abc')

        cmd = 'ExocortexAlembic.createExportJobs(@"filename={0};{1}")'.format(
            temporary_path,
            ';'.join(job_args)
        )
        MaxPlus.Core.EvalMAXScript(cmd)

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
        self.deselect_all()
        MaxPlus.SelectionManager.SelectNodes(saved_selection)


pyblish.api.register_plugin(ExtractCameraAlembic)

