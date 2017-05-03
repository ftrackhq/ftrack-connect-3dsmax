# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os
import uuid
import pyblish.api
import MaxPlus


class ExtractCameraMaxBinary(pyblish.api.InstancePlugin):
    '''Extract camera as max binary.'''

    order = pyblish.api.ExtractorOrder

    families = ['ftrack', 'camera']
    match = pyblish.api.Subset

    def process(self, instance):
        '''Process instance.'''

        savedSelection = MaxPlus.SelectionManager.GetNodes()

        # 'max select none'
        # 'select {node}'

        MaxPlus.SelectionManager.SelectNodes(savedSelection)

pyblish.api.register_plugin(ExtractCameraMaxBinary)
