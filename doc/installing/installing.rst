..
    :copyright: Copyright (c) 2016 ftrack

.. _installing:

*********************************
Installing ftrack connect 3ds max
*********************************

Using ftrack Connect
====================

The primary way of installing and launching the 3ds Max integration is
through the ftrack Connect package. Go to
`ftrack Connect package <https://www.ftrack.com/portfolio/connect>`_ and
download it for your platform.

.. seealso::

    Once ftrack Connect package is installed please follow this
    :ref:`article <using/launching>` to launch 3ds Max with the ftrack
    integration.

Installing with pip
===================

.. highlight:: bash

Installation is simple with `pip <http://www.pip-installer.org/>`_::

    pip install ftrack-connect-3dsmax

.. note::

    This project is not yet available on PyPi.

Building from source
====================

You can also build manually from the source for more control. First obtain a
copy of the source by either downloading the
`zipball <https://bitbucket.org/ftrack/ftrack-connect-3dsmax/get/master.zip>`_ or
cloning the public repository::

    git clone git@bitbucket.org:ftrack/ftrack-connect-3dsmax.git

Then you can build and install the package into your current Python
site-packages folder::

    python setup.py install

Alternatively, just build locally and manage yourself::

    python setup.py build

Building documentation from source
----------------------------------

To build the documentation from source::

    python setup.py build_sphinx

Then view in your browser::

    file:///path/to/ftrack-connect-3dsmax/build/doc/html/index.html

Dependencies
============

* `Python <http://python.org>`_ >= 2.6, < 3
* `ftrack connect <https://bitbucket.org/ftrack/ftrack-connect>`_ >= 0.1.2, < 2
* `3ds Max <http://www.autodesk.com/products/3ds-max/overview>`_ >= 2016 SP3, <= 2017
* `Visual C++ 2015 Redistributable <https://www.microsoft.com/en-us/download/details.aspx?id=48145>`_

Additional For building
-----------------------

* `Sphinx <http://sphinx-doc.org/>`_ >= 1.2.2, < 2
* `sphinx_rtd_theme <https://github.com/snide/sphinx_rtd_theme>`_ >= 0.1.6, < 1
