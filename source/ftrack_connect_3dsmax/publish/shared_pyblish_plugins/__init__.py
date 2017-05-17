# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack


def register():
    '''Register shared pyblish plugins.'''
    import ftrack_connect_3dsmax.publish.shared_pyblish_plugins.collect
    import ftrack_connect_3dsmax.publish.shared_pyblish_plugins.collect_maxversion
    import ftrack_connect_3dsmax.publish.shared_pyblish_plugins.extract_maxbinary
    import ftrack_connect_3dsmax.publish.shared_pyblish_plugins.extract_alembic
