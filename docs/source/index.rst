nanohub-remote Documentation
=============================

A Python library for interacting with nanoHUB APIs, featuring improved session management,
connection pooling, automatic retries, and comprehensive HTTP method support.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api/index
   examples/index
   testing
   changelog

Features
--------

* **Session Management**: Persistent sessions with connection pooling
* **HTTP Methods**: GET, POST, PUT, DELETE, PATCH support
* **Automatic Retries**: Configurable retry logic for failed requests
* **Context Managers**: Automatic resource cleanup
* **JSON Support**: Native JSON handling for all HTTP methods
* **Comprehensive Testing**: 25+ unit tests with full coverage

Quick Example
-------------

.. code-block:: python

   import nanohubremote as nr

   # Create authenticated session
   auth_data = {
       'grant_type': 'personal_token',
       'token': 'your_token_here'
   }

   with nr.Session(auth_data) as session:
       # List available tools
       response = session.requestGet('tools/list')
       tools = response.json()

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
