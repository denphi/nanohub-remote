Advanced Usage
==============

This page covers advanced patterns and configurations.

Custom Session Configuration
-----------------------------

Complete Configuration
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import nanohubremote as nr

   auth_data = {
       'grant_type': 'personal_token',
       'token': 'your_token'
   }

   # Fully configured session
   session = nr.Session(
       auth_data,
       url="https://nanohub.org/api",  # Custom API endpoint
       timeout=30,                       # 30 second timeout
       max_retries=10,                   # Retry up to 10 times
       pool_connections=50,              # Large connection pool
       pool_maxsize=50                   # Large pool max size
   )

   try:
       # Your code here
       pass
   finally:
       session.close()

Production-Ready Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import nanohubremote as nr
   import logging

   # Setup logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   # Configuration from environment or config file
   config = {
       'auth': {
           'grant_type': 'personal_token',
           'token': os.environ.get('NANOHUB_TOKEN')
       },
       'session': {
           'timeout': 60,
           'max_retries': 5,
           'pool_connections': 20,
           'pool_maxsize': 20
       }
   }

   # Create session with error handling
   try:
       session = nr.Session(config['auth'], **config['session'])
       logger.info("Session created successfully")
   except Exception as e:
       logger.error(f"Failed to create session: {e}")
       raise

Concurrent Requests
-------------------

Using Threading
~~~~~~~~~~~~~~~

.. code-block:: python

   import nanohubremote as nr
   from concurrent.futures import ThreadPoolExecutor
   import threading

   auth_data = {
       'grant_type': 'personal_token',
       'token': 'your_token'
   }

   # Create session with larger pool for concurrency
   session = nr.Session(
       auth_data,
       pool_connections=50,
       pool_maxsize=50
   )

   # Fetch multiple endpoints concurrently
   endpoints = ['users/profile', 'status', 'citations/list']

   with ThreadPoolExecutor(max_workers=10) as executor:
       results = list(executor.map(lambda ep: session.requestGet(ep).json(), endpoints))

   session.close()

   # Process results
   for result in results:
       print(f"Result: {result}")

Async Pattern (with sync session)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import nanohubremote as nr
   import asyncio
   from concurrent.futures import ThreadPoolExecutor

   auth_data = {
       'grant_type': 'personal_token',
       'token': 'your_token'
   }

   class AsyncNanoHubClient:
       def __init__(self, auth_data):
           self.session = nr.Session(auth_data, pool_connections=50)
           self.executor = ThreadPoolExecutor(max_workers=10)

       async def get_async(self, endpoint):
           """Async wrapper for GET request"""
           loop = asyncio.get_event_loop()
           response = await loop.run_in_executor(
               self.executor,
               self.session.requestGet,
               endpoint
           )
           return response.json()

       def close(self):
           self.session.close()
           self.executor.shutdown()

   # Usage
   async def main():
       client = AsyncNanoHubClient(auth_data)
       try:
           # Concurrent async requests
           results = await asyncio.gather(
               client.get_async('users/profile'),
               client.get_async('citations/list'),
               client.get_async('status')
           )
           return results
       finally:
           client.close()

   # Run async code
   results = asyncio.run(main())

Retry Strategies
----------------

Custom Retry Logic
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   import nanohubremote as nr
   from requests.exceptions import RequestException

   auth_data = {
       'grant_type': 'personal_token',
       'token': 'your_token'
   }

   def request_with_custom_retry(session, endpoint, max_attempts=5):
       """Custom retry with exponential backoff"""
       for attempt in range(max_attempts):
           try:
               response = session.requestGet(endpoint)
               response.raise_for_status()
               return response.json()
           except RequestException as e:
               if attempt == max_attempts - 1:
                   raise
               wait_time = 2 ** attempt  # Exponential backoff
               print(f"Attempt {attempt + 1} failed, retrying in {wait_time}s...")
               time.sleep(wait_time)

   with nr.Session(auth_data) as session:
       data = request_with_custom_retry(session, 'users/profile')

Rate Limiting
-------------

Simple Rate Limiter
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   import nanohubremote as nr

   class RateLimitedSession:
       def __init__(self, auth_data, requests_per_second=2):
           self.session = nr.Session(auth_data)
           self.min_interval = 1.0 / requests_per_second
           self.last_request = 0

       def _wait_if_needed(self):
           elapsed = time.time() - self.last_request
           if elapsed < self.min_interval:
               time.sleep(self.min_interval - elapsed)
           self.last_request = time.time()

       def get(self, endpoint):
           self._wait_if_needed()
           return self.session.requestGet(endpoint)

       def post(self, endpoint, **kwargs):
           self._wait_if_needed()
           return self.session.requestPost(endpoint, **kwargs)

       def close(self):
           self.session.close()

   # Usage
   auth_data = {'grant_type': 'personal_token', 'token': 'your_token'}
   rate_limited = RateLimitedSession(auth_data, requests_per_second=1)

   try:
       for i in range(10):
           response = rate_limited.get('endpoint')
           print(f"Request {i+1} completed")
   finally:
       rate_limited.close()

Caching Responses
-----------------

Simple Cache
~~~~~~~~~~~~

.. code-block:: python

   import nanohubremote as nr
   from functools import lru_cache
   import json

   auth_data = {
       'grant_type': 'personal_token',
       'token': 'your_token'
   }

   class CachedNanoHubClient:
       def __init__(self, auth_data):
           self.session = nr.Session(auth_data)

       @lru_cache(maxsize=100)
       def get_cached(self, endpoint):
           """Cache GET requests"""
           response = self.session.requestGet(endpoint)
           # Convert to string for caching (responses aren't hashable)
           return response.json()

       def invalidate_cache(self):
           """Clear cache"""
           self.get_cached.cache_clear()

       def close(self):
           self.session.close()

   # Usage
   client = CachedNanoHubClient(auth_data)
   try:
       # First call - hits API
       data1 = client.get_cached('users/profile')

       # Second call - returns cached result
       data2 = client.get_cached('users/profile')

       # Clear cache
       client.invalidate_cache()
   finally:
       client.close()

Logging and Debugging
----------------------

Request Logging
~~~~~~~~~~~~~~~

.. code-block:: python

   import nanohubremote as nr
   import logging

   # Setup logging
   logging.basicConfig(
       level=logging.DEBUG,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )

   # Enable requests library debugging
   import http.client as http_client
   http_client.HTTPConnection.debuglevel = 1

   auth_data = {
       'grant_type': 'personal_token',
       'token': 'your_token'
   }

   with nr.Session(auth_data) as session:
       # Requests will be logged
       response = session.requestGet('users/profile')

Custom Logging Wrapper
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import nanohubremote as nr
   import logging
   import time

   logger = logging.getLogger(__name__)

   class LoggedSession:
       def __init__(self, auth_data):
           self.session = nr.Session(auth_data)

       def request_get(self, endpoint):
           logger.info(f"GET {endpoint}")
           start_time = time.time()
           try:
               response = self.session.requestGet(endpoint)
               elapsed = time.time() - start_time
               logger.info(f"GET {endpoint} - {response.status_code} ({elapsed:.2f}s)")
               return response
           except Exception as e:
               elapsed = time.time() - start_time
               logger.error(f"GET {endpoint} failed after {elapsed:.2f}s: {e}")
               raise

       def close(self):
           self.session.close()

Error Recovery
--------------

Graceful Degradation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import nanohubremote as nr
   from requests.exceptions import Timeout, ConnectionError
   import logging

   logger = logging.getLogger(__name__)

   auth_data = {
       'grant_type': 'personal_token',
       'token': 'your_token'
   }

   def get_profile_with_fallback(session):
       """Try to get profile with fallback"""
       try:
           # Try primary endpoint
           response = session.requestGet('users/profile', timeout=5)
           return response.json()
       except Timeout:
           logger.warning("Primary endpoint timed out, using fallback")
           try:
               # Try fallback endpoint or cached data
               response = session.requestGet('users/profile/cached', timeout=10)
               return response.json()
           except Exception as e:
               logger.error(f"Fallback also failed: {e}")
               # Return empty or default data
               return {}
       except ConnectionError as e:
           logger.error(f"Connection failed: {e}")
           return {}

Session Pool Management
-----------------------

Session Pool
~~~~~~~~~~~~

.. code-block:: python

   import nanohubremote as nr
   from queue import Queue

   class SessionPool:
       def __init__(self, auth_data, pool_size=5):
           self.pool = Queue(maxsize=pool_size)
           for _ in range(pool_size):
               session = nr.Session(auth_data)
               self.pool.put(session)

       def get_session(self):
           """Get session from pool"""
           return self.pool.get()

       def return_session(self, session):
           """Return session to pool"""
           self.pool.put(session)

       def close_all(self):
           """Close all sessions in pool"""
           while not self.pool.empty():
               session = self.pool.get()
               session.close()

   # Usage
   auth_data = {'grant_type': 'personal_token', 'token': 'your_token'}
   pool = SessionPool(auth_data, pool_size=10)

   try:
       session = pool.get_session()
       try:
           response = session.requestGet('users/profile')
       finally:
           pool.return_session(session)
   finally:
       pool.close_all()

Session State Management
------------------------

The ``Session`` class provides methods to manage authentication state and helper utilities.

Managing Authentication
~~~~~~~~~~~~~~~~~~~~~~~

You can check the current authentication status and clear the session if needed.

.. code-block:: python

   import nanohubremote as nr

   auth_data = {
       'grant_type': 'personal_token',
       'token': 'your_token'
   }

   with nr.Session(auth_data) as session:
       # Check if authenticated
       if session.authenticated:
           print("Session is authenticated")

       # Get the current access token
       token = session.access_token

       # Clear session state (resets authentication)
       session.clearSession()
       print(f"Authenticated after clear: {session.authenticated}")  # False

URL Construction
~~~~~~~~~~~~~~~~

The ``getUrl`` helper method allows you to construct full API URLs using the session's base URL. This is useful for debugging or logging.

.. code-block:: python

   with nr.Session(auth_data) as session:
       # Construct full URL for an endpoint
       url = session.getUrl('users/profile')
       print(f"Full URL: {url}")
       # Output: https://nanohub.org/api/users/profile

Raw API Access
--------------

While ``Tools`` and ``Project`` classes provide convenient wrappers, you can use the ``Session`` object directly to access any nanoHUB API endpoint, including those not covered by specific helper classes (e.g., user profile, citations).

.. code-block:: python

   with nr.Session(auth_data) as session:
       # Access User Profile API
       response = session.requestGet('users/profile')
       if response.status_code == 200:
           profile = response.json()
           print(f"User: {profile.get('name')}")

       # Access Citations API
       response = session.requestGet('citations/list', data={'limit': 5})
       if response.status_code == 200:
           citations = response.json()
           for citation in citations:
               print(f"Title: {citation.get('title')}")
