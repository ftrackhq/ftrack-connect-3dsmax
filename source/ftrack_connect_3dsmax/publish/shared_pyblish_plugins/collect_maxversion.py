# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack

import pyblish.api
import MaxPlus


class CollectMaxVersion(pyblish.api.ContextPlugin):
    '''Collect 3dsmax version.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add 3dsmax version information.'''

        context.data['software'] = {
            'name': '3dsmax',
            'version': MaxPlus.Core.EvalMAXScript('getFileVersion "$max/3dsmax.exe"').Get()
        }

        self.log.debug('Collected 3dsmax version information.')


pyblish.api.register_plugin(CollectMaxVersion)
