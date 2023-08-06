h5utils Package
===============

**h5utils** is a python package adding extra functionality missing from MIT/nanoComp's h5utils (which is not a python package and is available at https://github.com/NanoComp/h5utils).
.

HDF5_ (Hierarchical Data Format 5) is a file format for storing scientific data.

The tools in the h5utils package allow converting other formats from and to HDF5 and to visualize HDF5 files.

They include:

* h5tovts, which converts HDF5 files to structured VTK files for
  visualization with VTK-aware programs. This is particularly useful to visualize HDF5 output files from MPB_.

.. _MPB: https://mpb.readthedocs.io/
.. _HDF5: https://www.hdfgroup.org/solutions/hdf5/
.. _MITH5TOOLS: https://github.com/NanoComp/h5utils

For more documentation, please see https://h5utils.readthedocs.io.

Installation:
-------------

.. code:: bash

	pip install h5utils

Usage:
------
To convert an .h5 files to .vts, simply run:

.. code:: bash

    h5tovts example.h5

For more help:

.. code:: bash

    h5tovts --help
