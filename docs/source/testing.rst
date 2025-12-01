Testing
=======

The nanohub-remote library includes a comprehensive test suite.

Running Tests
-------------

Run all tests:

.. code-block:: bash

   pytest

Run with coverage report:

.. code-block:: bash

   pytest --cov=nanohubremote --cov-report=html

Run specific test file:

.. code-block:: bash

   pytest tests/test_session.py

Test Coverage
-------------

The test suite includes:

* 25+ unit tests
* 100% pass rate
* Mock-based testing (no real API calls)
* Coverage reporting

Test Organization
-----------------

.. code-block:: text

   tests/
   ├── __init__.py
   ├── test_session.py      # Session class tests
   └── README.md            # Testing documentation

Writing Tests
-------------

Example test structure:

.. code-block:: python

   import unittest
   from unittest.mock import Mock, patch
   from nanohubremote.session import Session

   class TestMyFeature(unittest.TestCase):
       def setUp(self):
           self.credentials = {
               'grant_type': 'personal_token',
               'token': 'test_token'
           }
           self.session = Session(self.credentials)

       @patch('requests.Session.get')
       def test_my_feature(self, mock_get):
           mock_response = Mock()
           mock_response.status_code = 200
           mock_get.return_value = mock_response

           result = self.session.requestGet('endpoint')

           self.assertEqual(result.status_code, 200)
           mock_get.assert_called_once()

See tests/README.md for more details.
