.. _io:

===
I/O
===
.. currentmodule:: pyntcloud

As mentioned in the introduction, 3D point clouds could be obtained from many
different sources, each one with its own file format.

In addition to file formats used by each manufacturer, point clouds may also be
stored in generic binary and ascii formats using different programming languages.

PyntCloud provides reading and writing routines for many common 3D file and
generic array formats (more formats will be added in the near future):

-   .asc / .pts / .txt / .csv / .xyz (see 'Note about ASCII files' below)
-   `.las <https://www.asprs.org/committee-general/laser-las-file-format-exchange-activities.html>`__
-   `.npy / .npz <https://docs.scipy.org/doc/numpy-dev/neps/npy-format.html>`__
-   `.obj <https://en.wikipedia.org/wiki/Wavefront_.obj_file>`__
-   `.off <https://en.wikipedia.org/wiki/OFF_(file_format)>`__ (with color support)
-   `.pcd <http://pointclouds.org/documentation/tutorials/pcd_file_format.php#pcd-file-format>`__
-   `.ply <https://en.wikipedia.org/wiki/PLY_(file_format)>`__

Reading
=======

.. automethod:: PyntCloud.from_file
    :noindex:

.. code-block:: python

    from pyntcloud import PyntCloud
    my_point_cloud = PyntCloud.from_file("some_file.ply")

Writing
=======

.. automethod:: PyntCloud.to_file

.. code-block:: python

    # my_point_cloud is a PyntCloud instance
    my_point_cloud.to_file("out_file.obj", internal=["points", "mesh"])

Alternative ways for creating PyntClouds
========================================

Even though PyntCloud includes readers for some of the most common 3D file formats,
there are many other formats and sources that you can use to store point cloud data.

That's why although PyntCloud will include support for other file formats, it will
never cover all.

The good news is that as long as you can **load the data into Python**, you can create
a PyntCloud instance manually.

The key thing to understand is that you can't just plug in the raw data into the
PyntCloud constructor; there are some restrictions.

These restrictions are covered in :ref:`points`.

As long as you can adapt your data to these restrictions, you will be able
to construct a PyntCloud from formats that are not covered in *from_file*.

Note about ASCII files
======================

There are many formats englobed in these kinds of files: .asc, .txt, .pts, ...

Normally, the first 3 columns represent the X,Y,Z coordinates of the point and
the rest of the columns represent some scalar field associated to that point
(Maybe R,G,B values, or Nx,Ny,Nz, etc). But there is no official format specification.

Given all the possibilities that this brings, `PyntCloud.from_file` accepts keyword
arguments in order to let the user adjust the loading for every possibility.

Internally, PyntCloud.from_file is just calling the pandas function
`.read_csv <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html>`__ when
you give it a valid ascii format.

So check the linked documentation to explore all the possible arguments in order to
adjust them to read your ascii file.

For example, given a *example.pts* file with this content:

.. code-block:: python

    8
    -0.037829 0.12794 0.004474
    -0.044779 0.128887 0.001904
    -0.068009 0.151244 0.037195
    -0.002287 0.13015 0.02322
    -0.022605 0.126675 0.007155
    -0.025107 0.125921 0.006242
    -0.03712 0.127449 0.001795
    0.033213 0.112692 0.027686

You can construct a PyntCloud as follows:

.. code-block:: python

    import pandas as pd
    from pyntcloud import PyntCloud

    cloud = PyntCloud.from_file("example.pts",
                                sep=" ",
                                header=0,
                                names=["x","y","z"])
