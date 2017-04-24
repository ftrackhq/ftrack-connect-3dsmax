# :coding: utf-8
# :copyright: Copyright (c) 2017 ftrack


import ftrack_connect_pipeline.application_plugin

import ftrack_connect_3dsmax.publish._version


class MaxPlugin(
    ftrack_connect_pipeline.application_plugin.BaseApplicationPlugin
):
    '''Define the 3dsmax plugin.'''

    def get_plugin_information(self):
        '''Return plugin information.'''
        return {
            'application_id': '3dsmax',
            'plugin_version': ftrack_connect_3dsmax.publish._version.__version__
        }

    def register_assets(self):
        '''Register assets.'''

        super(MaxPlugin, self).register_assets()

        # Call super class to register shared pipeline assets.
        import ftrack_connect_3dsmax.publish.shared_pyblish_plugins
        import ftrack_connect_pipeline.shared_pyblish_plugins

        ftrack_connect_3dsmax.publish.shared_pyblish_plugins.register()
        ftrack_connect_pipeline.shared_pyblish_plugins.register()
