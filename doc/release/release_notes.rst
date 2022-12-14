..
    :copyright: Copyright (c) 2016 ftrack

.. _release/release_notes:

*************
Release Notes
*************

.. release:: 0.5.0
    :date: 2021-09-08

    .. change:: changed
        :tags: Api

        Update pyside signal signature for pyside2 compatiblity.

    .. change:: changed
        :tags: Internal

        Rename scene asset option from import to open to match behaviour.

    .. change:: changed
        :tags: Hook

        Update hook for application-launcher.

    .. change:: changed
        :tags: Setup

        Provide dependency to ftrack-connector-legacy module.

.. warning::

    From this version the support for ftrack-connect 1.X is dropped, and
    only ftrack-conenct 2.0 will be supported up to the integration EOL.


.. release:: 0.4.3
    :date: 2020-01-21

    ..change:: changed
        :tags: Setup

        Pip compatibility for version 19.3.0 or higher

.. release:: 0.4.2
    :date: 2019-07-10

    .. change:: fix

        Fix QStringListModel compatibility for PySide2 5.9+.

.. release:: 0.4.1
    :date: 2019-01-17

    .. change:: new

        Added Exocortex plugin build for Max 2018

.. release:: 0.4.0
    :date: 2019-01-02

    .. change:: changed
        :tags: Internal

        Convert code to standalone ftrack-connect plugin.

.. release:: 0.3.1
    :date: 2018-05-03

    .. change:: fixed

        3DSMax < 2017 hangs during publish. 

.. release:: 0.3.0
    :date: 2017-09-12

    .. change:: new

        Added Max 2018 compatibility.

    .. change:: fixed

        Fixed Max 2016 hang when starting from ftrack connect.

.. release:: 0.2.11
    :date: 2016-12-01

    .. change:: fixed
        :tags: Performance

        Scanning for new asset versions at scene startup is very slow.

.. release:: 0.2.10
    :date: 2016-09-23

    .. change:: fixed

        Environment variables sometimes causes 3DS Max to error when launched
        with ftrack plugin loaded.

.. release:: 0.2.9
    :date: 2016-09-16

    .. change:: fixed

        DLL Loading fails as require to have Vistual Studio redistributable
        packages.

    .. change:: fixed

        Nested assets do not appear in Asset Manager Dialog.

    .. change:: new

        Rig assets can now be imported as Object X-Refs.

.. release:: 0.2.8
    :date: 2016-08-09

    .. change:: changed
        :tags: documentation

        Improved screenshots in documentation articles.

.. release:: 0.2.7
    :date: 2016-08-04

    .. change:: fixed

        Clean up and moved to ftrack repository.

.. release:: 0.2.6
    :date: 2016-07-19

    .. change:: fixed

        Scene asset import now uses Open instead of MergeMaxFiles.

    .. change:: fixed

        Made scene assets change version consistent with ftrack connect Maya.

    .. change:: fixed

        Fixed layout spacing of some ftrack dialogs in 3ds Max 2017.

.. release:: 0.2.5
    :date: 2016-07-15

    .. change:: fixed

        Importing scene assets was not clearing the previously open Max scene.

    .. change:: new

        Don't initialize the connector if the 3ds Max version is not supported.

.. release:: 0.2.4
    :date: 2016-07-1

    .. change:: fixed

        Fixed bug when versioning up and down some assets.

    .. change:: new

        Ftrack helper objects are now frozen and transforms are locked.

.. release:: 0.2.3
    :date: 2016-06-23

    .. change:: fixed

        Fixed publishing of Alembic assets when frame steps is not 1.

    .. change:: fixed

        Small UI fixes and tweaks.

.. release:: 0.2.2
    :date: 2016-06-22

    .. change:: fixed

        Fixed version change of Alembic assets using the Asset Manager dialog.

    .. change:: new

        Check for outdated assets when opening scenes and offer the user the
        option to update them.

    .. change:: new

        Added usage tracking on application startup.

.. release:: 0.2.1
    :date: 2016-06-17

    .. change:: new

        Initial beta release of ftrack connect 3ds Max plugin.
