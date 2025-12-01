Session
=======

.. automodule:: nanohubremote.session
   :members:
   :undoc-members:
   :show-inheritance:

Session Class
-------------

.. autoclass:: nanohubremote.session.Session
   :members:
   :undoc-members:
   :special-members: __init__, __enter__, __exit__

The Session class provides core HTTP functionality with:

* Persistent connections via requests.Session
* Automatic retry logic
* Connection pooling
* Token management
* Context manager support

HTTP Methods
------------

GET Request
~~~~~~~~~~~

.. automethod:: nanohubremote.session.Session.requestGet

POST Request
~~~~~~~~~~~~

.. automethod:: nanohubremote.session.Session.requestPost

PUT Request
~~~~~~~~~~~

.. automethod:: nanohubremote.session.Session.requestPut

DELETE Request
~~~~~~~~~~~~~~

.. automethod:: nanohubremote.session.Session.requestDelete

PATCH Request
~~~~~~~~~~~~~

.. automethod:: nanohubremote.session.Session.requestPatch

Session Management
------------------

.. automethod:: nanohubremote.session.Session.validateSession
.. automethod:: nanohubremote.session.Session.clearSession
.. automethod:: nanohubremote.session.Session.close

Example Usage
-------------

.. code-block:: python

   from nanohubremote import Session

   auth_data = {
       'grant_type': 'personal_token',
       'token': 'your_token'
   }

   # Using context manager
   with Session(auth_data) as session:
       response = session.requestGet('tools/list')
       tools = response.json()

   # Manual management
   session = Session(auth_data, max_retries=5, timeout=10)
   try:
       response = session.requestPost('endpoint', json={'data': 'value'})
   finally:
       session.close()
