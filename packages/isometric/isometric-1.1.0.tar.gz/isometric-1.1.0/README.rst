=========
isometric
=========

Overview
--------

Geometry on an isometric grid. 

Installation
------------

To install isometric, you can use `pip`. Open your terminal and run:

.. code-block:: bash

    pip install isometric

Usage
-----

.. code-block:: python

    import isometric as iso

    d = iso.Description(x = 2, y = -3, z = 7)
    print(d) # Description(x=2, y=-3, z=7)
    print(d.tare_x()) # Description(x=0, y=-5, z=5)
    print(d.tare_y()) # Description(x=5, y=0, z=10)
    print(d.tare_z()) # Description(x=-5, y=-10, z=0)
    print(d.projected_abscissa()) # -4.330127018922193
    print(d.projected_ordinate()) # 7.5
    print(d.projected_radius()) # 8.660254037844387
    print(d.projected_angle()) # 2.0943951023931953

    v = iso.Vector(x = 2, y = -3, z = 7)
    print(v == iso.Vector(*d)) # True
    print(v) # Vector(projected_abscissa=-4.330127018922193, projected_ordinate=7.5)
    print(v.tare_x()) # Description(x=0, y=-5, z=5)
    print(v.projected_abscissa()) # -4.330127018922193
    print(v.rotate(1)) # Vector(projected_abscissa=4.330127018922193, projected_ordinate=7.5)
    print(v.rotate(1).tare_x()) # Description(x=0, y=5, z=10)
    print(v * -3) # Vector(projected_abscissa=12.990381056766578, projected_ordinate=-22.5)
    print(v ** 2) # 75.0
    print(v ** 3) # Vector(projected_abscissa=-324.7595264191645, projected_ordinate=562.5)

    w = iso.Vector(1, 1, 0)
    print(v + w) # Vector(projected_abscissa=-4.330127018922193, projected_ordinate=6.5)
    print(v * w) # -7.5

In the isometric plane the x-axis points at 8 o'clock, the y-axis point at 4 o'clock and the z-axis points at 12 o'clock.

License
-------

This project is licensed under the MIT License.

Links
-----

* `Download <https://pypi.org/project/isometric/#files>`_
* `Source <https://github.com/johannes-programming/isometric>`_ 

Credits
-------
- Author: Johannes Programming
- Email: johannes-programming@posteo.org

Thank you for using isometric!