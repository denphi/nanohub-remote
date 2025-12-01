Installation
============

PyPI Installation
-----------------

Install the latest stable version from PyPI:

.. code-block:: bash

   pip install nanohub-remote

With Optional Dependencies
---------------------------

For development and testing:

.. code-block:: bash

   pip install nanohub-remote[dev]

For testing only:

.. code-block:: bash

   pip install nanohub-remote[test]

From Source
-----------

Install from GitHub source:

.. code-block:: bash

   git clone https://github.com/denphi/nanohub-remote.git
   cd nanohub-remote
   pip install -e .

Requirements
------------

Core Dependencies
~~~~~~~~~~~~~~~~~

* Python 3.8+
* requests >= 2.25.0
* urllib3 >= 1.26.0
* fs >= 2.4.0

Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~

Development and Testing:

* pytest >= 7.0.0
* pytest-cov >= 4.0.0
* pytest-mock >= 3.10.0
* black >= 23.0.0
* flake8 >= 6.0.0
* mypy >= 1.0.0

Verification
------------

Verify the installation:

.. code-block:: python

   import nanohubremote as nr
   print(nr.__version__)

Run tests:

.. code-block:: bash

   pytest
