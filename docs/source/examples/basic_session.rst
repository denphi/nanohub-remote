Basic Session Examples
======================

This page demonstrates basic session usage and HTTP methods.

Creating a Session
------------------

Personal Token Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import nanohubremote as nr

   # Setup authentication
   auth_data = {
       'grant_type': 'personal_token',
       'token': 'your_personal_token_here'
   }

   # Create session with context manager (recommended)
   with nr.Session(auth_data) as session:
       print(f"Session authenticated: {session.authenticated}")

OAuth Authentication
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   auth_data = {
       'client_id': 'your_client_id',
       'client_secret': 'your_client_secret',
       'grant_type': 'password',
       'username': 'your_username',
       'password': 'your_password'
   }

   with nr.Session(auth_data) as session:
       print("OAuth session created")

GET Requests
------------

Simple GET
~~~~~~~~~~

.. code-block:: python

   with nr.Session(auth_data) as session:
       response = session.requestGet('users/profile')

       if response.status_code == 200:
           data = response.json()
           print(f"User: {data.get('name')}")

GET with Parameters
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   with nr.Session(auth_data) as session:
       # Parameters in data dict
       response = session.requestGet('endpoint', data={'param': 'value'})
       result = response.json()

POST Requests
-------------

POST with Form Data
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   with nr.Session(auth_data) as session:
       data = {
           'field1': 'value1',
           'field2': 'value2'
       }
       response = session.requestPost('endpoint', data=data)
       print(f"Status: {response.status_code}")

POST with JSON
~~~~~~~~~~~~~~

.. code-block:: python

   with nr.Session(auth_data) as session:
       payload = {
           'name': 'Test',
           'value': 123,
           'enabled': True
       }
       response = session.requestPost('endpoint', json=payload)
       result = response.json()

PUT Requests
------------

Update Resource
~~~~~~~~~~~~~~~

.. code-block:: python

   with nr.Session(auth_data) as session:
       resource_id = '123'
       updates = {
           'status': 'active',
           'updated_at': '2024-12-01'
       }

       response = session.requestPut(
           f'resource/{resource_id}',
           json=updates
       )

       if response.status_code == 200:
           print("Resource updated successfully")

DELETE Requests
---------------

Delete Resource
~~~~~~~~~~~~~~~

.. code-block:: python

   with nr.Session(auth_data) as session:
       resource_id = '123'
       response = session.requestDelete(f'resource/{resource_id}')

       if response.status_code == 204:
           print("Resource deleted successfully")

PATCH Requests
--------------

Partial Update
~~~~~~~~~~~~~~

.. code-block:: python

   with nr.Session(auth_data) as session:
       resource_id = '123'
       changes = {
           'field_to_update': 'new_value'
       }

       response = session.requestPatch(
           f'resource/{resource_id}',
           json=changes
       )

       updated_resource = response.json()

Custom Configuration
--------------------

Timeout and Retries
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Custom timeout and retry settings
   session = nr.Session(
       auth_data,
       timeout=30,      # 30 second timeout
       max_retries=10   # Retry up to 10 times
   )

   try:
       response = session.requestGet('slow/endpoint')
   finally:
       session.close()

Connection Pooling
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Larger connection pool for concurrent requests
   session = nr.Session(
       auth_data,
       pool_connections=50,
       pool_maxsize=50
   )

   try:
       # Make multiple concurrent requests
       responses = []
       for i in range(10):
           response = session.requestGet(f'endpoint/{i}')
           responses.append(response)
   finally:
       session.close()

Error Handling
--------------

Basic Error Handling
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from requests.exceptions import RequestException, Timeout

   with nr.Session(auth_data) as session:
       try:
           response = session.requestGet('endpoint')
           response.raise_for_status()
           data = response.json()
       except Timeout:
           print("Request timed out")
       except RequestException as e:
           print(f"Request failed: {e}")
       except ValueError:
           print("Invalid JSON response")

Comprehensive Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   with nr.Session(auth_data) as session:
       try:
           response = session.requestPost('endpoint', json={'data': 'value'})

           # Check status code
           if response.status_code == 200:
               result = response.json()
           elif response.status_code == 401:
               print("Authentication failed")
           elif response.status_code == 404:
               print("Endpoint not found")
           else:
               print(f"Request failed with status {response.status_code}")

       except ConnectionError:
           print("Connection to server failed")
       except Timeout:
           print("Request timed out")
       except RequestException as e:
           print(f"Unexpected error: {e}")

Custom Headers
--------------

.. code-block:: python

   with nr.Session(auth_data) as session:
       # Custom headers for specific request
       custom_headers = {
           'X-Custom-Header': 'custom-value',
           'Accept': 'application/json'
       }

       response = session.requestGet(
           'endpoint',
           headers=custom_headers
       )

Session Reuse
-------------

.. code-block:: python

   # Reuse session for multiple requests
   with nr.Session(auth_data) as session:
       # Request 1
       profile = session.requestGet('users/profile').json()

       # Request 2
       citations = session.requestGet('citations/list').json()

       # Request 3
       status = session.requestGet('status').json()

       # Connection is reused automatically for better performance
