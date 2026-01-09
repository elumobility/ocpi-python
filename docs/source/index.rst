Welcome to OCPI Python's documentation!
========================================

A modern, production-ready Python implementation of the Open Charge Point Interface (OCPI) protocol built on FastAPI.

Open Charge Point Interface (OCPI) is an open protocol used for connections
between charging station operators and service providers.

**Supported OCPI versions:** 2.3.0, 2.2.1, 2.1.1

**OCPI Documentation:**
`[2.3.0] <https://github.com/ocpi/ocpi/tree/release-2.3.0-bugfixes>`_,
`[2.2.1] <https://github.com/ocpi/ocpi/tree/release-2.2.1-bugfixes>`_,
`[2.1.1] <https://github.com/ocpi/ocpi/tree/release-2.1.1-bugfixes>`_

.. note::

   It's assumed that you are familiar with the OCPI
   (Open Charge Point Interface) protocol.
   It is recommended to refer to the official OCPI documentation
   for a comprehensive understanding of the protocol
   specifications and guidelines.

.. toctree::
   :maxdepth: 3

   installation
   tutorial/index
   api/index

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Credits
-------

This library is based on the excellent work from `extrawest/extrawest_ocpi <https://github.com/extrawest/extrawest_ocpi>`_,
with significant enhancements including OCPI 2.3.0 support, Pydantic v2 migration, and comprehensive test coverage.
