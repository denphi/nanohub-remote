"""
Unit tests for Session class.

Tests the core Session functionality including:
- Session initialization
- Request methods (GET, POST, PUT, DELETE, PATCH)
- Authentication and token refresh
- Connection pooling and retry logic
- Context manager support
- Resource cleanup
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
from time import time

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nanohubremote.session import Session, Tools, Sim2L


class TestSessionInitialization(unittest.TestCase):
    """Test Session initialization and configuration."""

    def test_session_init_with_personal_token(self):
        """Test session initialization with personal token."""
        credentials = {
            'grant_type': 'personal_token',
            'token': 'test_token_123'
        }
        session = Session(credentials)

        self.assertTrue(session.authenticated)
        self.assertEqual(session.access_token, 'test_token_123')
        self.assertEqual(session.headers['Authorization'], 'Bearer test_token_123')
        self.assertIsNotNone(session._session)

    def test_session_init_with_custom_url(self):
        """Test session initialization with custom URL."""
        credentials = {
            'grant_type': 'personal_token',
            'token': 'test_token'
        }
        custom_url = "https://custom.nanohub.org/api"
        session = Session(credentials, url=custom_url)

        self.assertEqual(session.url, custom_url)

    def test_session_init_with_custom_timeout(self):
        """Test session initialization with custom timeout."""
        credentials = {
            'grant_type': 'personal_token',
            'token': 'test_token'
        }
        session = Session(credentials, timeout=10)

        self.assertEqual(session.timeout, 10)

    def test_session_init_with_custom_retry(self):
        """Test session initialization with custom retry settings."""
        credentials = {
            'grant_type': 'personal_token',
            'token': 'test_token'
        }
        session = Session(credentials, max_retries=5)

        # Session should be created successfully
        self.assertIsNotNone(session._session)

    def test_session_init_with_connection_pool_settings(self):
        """Test session initialization with connection pool settings."""
        credentials = {
            'grant_type': 'personal_token',
            'token': 'test_token'
        }
        session = Session(credentials, pool_connections=20, pool_maxsize=20)

        # Session should be created successfully
        self.assertIsNotNone(session._session)


class TestSessionMethods(unittest.TestCase):
    """Test Session HTTP methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.credentials = {
            'grant_type': 'personal_token',
            'token': 'test_token_123'
        }
        self.session = Session(self.credentials)

    def test_get_url(self):
        """Test URL construction."""
        url = self.session.getUrl('tools/list')
        self.assertEqual(url, 'https://nanohub.org/api/tools/list')

    @patch('requests.Session.get')
    def test_request_get(self, mock_get):
        """Test GET request method."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'ok'}
        mock_get.return_value = mock_response

        response = self.session.requestGet('test/endpoint')

        self.assertEqual(response.status_code, 200)
        mock_get.assert_called_once()

    @patch('requests.Session.post')
    def test_request_post(self, mock_post):
        """Test POST request method."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'created'}
        mock_post.return_value = mock_response

        response = self.session.requestPost('test/endpoint', data={'key': 'value'})

        self.assertEqual(response.status_code, 200)
        mock_post.assert_called_once()

    @patch('requests.Session.post')
    def test_request_post_with_json(self, mock_post):
        """Test POST request with JSON data."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        response = self.session.requestPost('test/endpoint', json={'key': 'value'})

        self.assertEqual(response.status_code, 200)
        # Verify json parameter was passed
        call_kwargs = mock_post.call_args[1]
        self.assertEqual(call_kwargs['json'], {'key': 'value'})

    @patch('requests.Session.put')
    def test_request_put(self, mock_put):
        """Test PUT request method."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_put.return_value = mock_response

        response = self.session.requestPut('test/endpoint', json={'key': 'updated'})

        self.assertEqual(response.status_code, 200)
        mock_put.assert_called_once()

    @patch('requests.Session.delete')
    def test_request_delete(self, mock_delete):
        """Test DELETE request method."""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        response = self.session.requestDelete('test/endpoint')

        self.assertEqual(response.status_code, 204)
        mock_delete.assert_called_once()

    @patch('requests.Session.patch')
    def test_request_patch(self, mock_patch):
        """Test PATCH request method."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_patch.return_value = mock_response

        response = self.session.requestPatch('test/endpoint', json={'field': 'value'})

        self.assertEqual(response.status_code, 200)
        mock_patch.assert_called_once()

    @patch('requests.Session.get')
    def test_request_with_custom_headers(self, mock_get):
        """Test request with custom headers."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        custom_headers = {'X-Custom-Header': 'value'}
        response = self.session.requestGet('test/endpoint', headers=custom_headers)

        # Verify custom headers were passed
        call_kwargs = mock_get.call_args[1]
        self.assertEqual(call_kwargs['headers'], custom_headers)

    @patch('requests.Session.get')
    def test_request_with_custom_timeout(self, mock_get):
        """Test request with custom timeout."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = self.session.requestGet('test/endpoint', timeout=30)

        # Verify custom timeout was passed
        call_kwargs = mock_get.call_args[1]
        self.assertEqual(call_kwargs['timeout'], 30)


class TestSessionAuthentication(unittest.TestCase):
    """Test Session authentication and token management."""

    @patch('requests.Session.post')
    def test_oauth_authentication(self, mock_post):
        """Test OAuth authentication flow."""
        # Mock the OAuth token response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'oauth_token_123',
            'expires_in': 3600,
            'refresh_token': 'refresh_token_123'
        }
        mock_post.return_value = mock_response

        credentials = {
            'grant_type': 'password',
            'client_id': 'test_client',
            'client_secret': 'test_secret',
            'username': 'test_user',
            'password': 'test_pass'
        }

        session = Session(credentials)

        self.assertTrue(session.authenticated)
        self.assertEqual(session.access_token, 'oauth_token_123')
        self.assertEqual(session.refresh_token, 'refresh_token_123')

    def test_validate_token_request_success(self):
        """Test successful token validation."""
        credentials = {
            'grant_type': 'personal_token',
            'token': 'test_token'
        }
        session = Session(credentials)

        mock_response = Mock()
        mock_response.json.return_value = {
            'access_token': 'new_token',
            'expires_in': 3600,
            'refresh_token': 'new_refresh'
        }

        timestamp = int(time())
        session.validateTokenRequest(mock_response, timestamp)

        self.assertEqual(session.access_token, 'new_token')
        self.assertTrue(session.authenticated)

    def test_validate_token_request_with_errors(self):
        """Test token validation with errors."""
        credentials = {
            'grant_type': 'personal_token',
            'token': 'test_token'
        }
        session = Session(credentials)

        mock_response = Mock()
        mock_response.json.return_value = {
            'errors': [{'message': 'Invalid token'}]
        }

        timestamp = int(time())

        with self.assertRaises(ConnectionError):
            session.validateTokenRequest(mock_response, timestamp)

    def test_validate_token_request_missing_access_token(self):
        """Test token validation with missing access_token."""
        credentials = {
            'grant_type': 'personal_token',
            'token': 'test_token'
        }
        session = Session(credentials)

        mock_response = Mock()
        mock_response.json.return_value = {
            'expires_in': 3600
        }

        timestamp = int(time())

        with self.assertRaises(AttributeError):
            session.validateTokenRequest(mock_response, timestamp)

    def test_clear_session(self):
        """Test clearing session state."""
        credentials = {
            'grant_type': 'personal_token',
            'token': 'test_token'
        }
        session = Session(credentials)

        # Session should be authenticated initially
        self.assertTrue(session.authenticated)

        # Change to non-personal token type
        session.credentials['grant_type'] = 'password'
        session.clearSession()

        # Session should be cleared
        self.assertFalse(session.authenticated)
        self.assertEqual(session.access_token, '')
        self.assertEqual(session.headers, {})


class TestSessionContextManager(unittest.TestCase):
    """Test Session context manager functionality."""

    def test_context_manager_enter_exit(self):
        """Test session as context manager."""
        credentials = {
            'grant_type': 'personal_token',
            'token': 'test_token'
        }

        with Session(credentials) as session:
            self.assertIsNotNone(session)
            self.assertTrue(session.authenticated)

    def test_context_manager_closes_session(self):
        """Test that context manager closes session on exit."""
        credentials = {
            'grant_type': 'personal_token',
            'token': 'test_token'
        }

        session = Session(credentials)
        session.close = Mock()

        with session:
            pass

        session.close.assert_called_once()

    def test_manual_close(self):
        """Test manual session close."""
        credentials = {
            'grant_type': 'personal_token',
            'token': 'test_token'
        }

        session = Session(credentials)
        session.close()

        # Should not raise an error
        self.assertIsNotNone(session)


class TestToolsClass(unittest.TestCase):
    """Test Tools class (inherits from Session)."""

    def setUp(self):
        """Set up test fixtures."""
        self.credentials = {
            'grant_type': 'personal_token',
            'token': 'test_token'
        }

    @patch('requests.Session.get')
    def test_tools_list(self, mock_get):
        """Test Tools.list() method."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'tools': [
                {'alias': 'tool1', 'name': 'Tool 1'},
                {'alias': 'tool2', 'name': 'Tool 2'}
            ]
        }
        mock_get.return_value = mock_response

        tools = Tools(self.credentials)
        tool_list = tools.list()

        self.assertEqual(len(tool_list), 2)
        self.assertEqual(tool_list[0]['alias'], 'tool1')

    @patch('requests.Session.get')
    def test_tools_list_with_filter(self, mock_get):
        """Test Tools.list() with filter."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'tools': [
                {'alias': 'tool1', 'name': 'Tool 1'},
                {'alias': 'tool2', 'name': 'Tool 2'},
                {'alias': 'tool3', 'name': 'Tool 3'}
            ]
        }
        mock_get.return_value = mock_response

        tools = Tools(self.credentials)
        tool_list = tools.list(filters=['tool1', 'tool3'])

        self.assertEqual(len(tool_list), 2)
        aliases = [t['alias'] for t in tool_list]
        self.assertIn('tool1', aliases)
        self.assertIn('tool3', aliases)
        self.assertNotIn('tool2', aliases)


class TestSim2LClass(unittest.TestCase):
    """Test Sim2L class (inherits from Session)."""

    def setUp(self):
        """Set up test fixtures."""
        self.credentials = {
            'grant_type': 'personal_token',
            'token': 'test_token'
        }

    @patch('requests.Session.get')
    def test_sim2l_list(self, mock_get):
        """Test Sim2L.list() method."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'tool': {
                'sim1': {'name': 'Simulation 1'},
                'sim2': {'name': 'Simulation 2'}
            }
        }
        mock_get.return_value = mock_response

        sim2l = Sim2L(self.credentials)
        sim_list = sim2l.list()

        self.assertEqual(len(sim_list), 2)


if __name__ == '__main__':
    unittest.main()
