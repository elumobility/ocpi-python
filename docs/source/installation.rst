Installation
============


Install library
~~~~~~~~~~~~~~~

OCPI Python is available from GitHub. To install it, run:

.. code-block:: sh

    uv pip install git+https://github.com/elumobility/ocpi-python.git

Install supported ASGI-server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure to install any ASGI-server supported by FastAPI. Let's install `uvicorn` as an example:

.. code-block:: sh

    uv pip install uvicorn

Requirements
~~~~~~~~~~~~

| Package | Version |
|---------|---------|
| Python | >=3.11 |
| Pydantic | >=2.0.0, <3.0.0 |
| pydantic-settings | >=2.0.0 |
| FastAPI | >=0.115.0, <1.0.0 |
| httpx | >=0.27.0 |

Next steps
~~~~~~~~~~

That's it! Once installed, you are ready to create your first OCPI application.
See :doc:`tutorial/index` for more.
