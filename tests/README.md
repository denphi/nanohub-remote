# Testing Guide

This directory contains unit tests for the nanohub-remote library.

## Running Tests

### Run all tests
```bash
pytest
```

### Run with coverage report
```bash
pytest --cov=nanohubremote --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_session.py
```

### Run specific test class
```bash
pytest tests/test_session.py::TestSessionMethods
```

### Run specific test
```bash
pytest tests/test_session.py::TestSessionMethods::test_request_get
```

### Run with verbose output
```bash
pytest -v
```

## Test Structure

```
tests/
├── __init__.py
├── README.md
└── test_session.py       # Session class tests
```

## Test Coverage

Current test coverage for Session class:

- ✅ Session initialization with different auth types
- ✅ Custom configuration (URL, timeout, retries, connection pooling)
- ✅ HTTP methods (GET, POST, PUT, DELETE, PATCH)
- ✅ Request with custom headers and timeouts
- ✅ JSON and form data support
- ✅ OAuth authentication flow
- ✅ Token validation and refresh
- ✅ Error handling
- ✅ Context manager support
- ✅ Resource cleanup
- ✅ Tools class methods
- ✅ Sim2L class methods

## Writing New Tests

### Example Test

```python
import unittest
from unittest.mock import Mock, patch
from nanohubremote.session import Session

class TestMyFeature(unittest.TestCase):
    """Test my new feature."""

    def setUp(self):
        """Set up test fixtures."""
        self.credentials = {
            'grant_type': 'personal_token',
            'token': 'test_token'
        }
        self.session = Session(self.credentials)

    @patch('requests.Session.get')
    def test_my_feature(self, mock_get):
        """Test my feature."""
        # Setup mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'value'}
        mock_get.return_value = mock_response

        # Execute
        result = self.session.requestGet('endpoint')

        # Assert
        self.assertEqual(result.status_code, 200)
        mock_get.assert_called_once()
```

## Test Markers

Use markers to categorize tests:

```python
@pytest.mark.unit
def test_unit_test():
    pass

@pytest.mark.integration
def test_integration_test():
    pass

@pytest.mark.slow
def test_slow_test():
    pass
```

Run tests by marker:
```bash
pytest -m unit
pytest -m integration
pytest -m "not slow"
```

## Mocking Guidelines

1. **Mock external dependencies**: Use `@patch` to mock requests, file I/O, etc.
2. **Don't mock the code under test**: Only mock dependencies
3. **Use specific mocks**: Mock at the lowest level possible
4. **Verify interactions**: Use `assert_called_once()`, `assert_called_with()`, etc.

## Code Coverage

To view detailed coverage report:
```bash
pytest --cov=nanohubremote --cov-report=html
open htmlcov/index.html
```

Target coverage: 80%+

## Continuous Integration

Tests are automatically run on:
- Pull requests
- Commits to main branch
- Scheduled nightly builds

## Troubleshooting

### Tests fail with import errors
```bash
pip install -e .
```

### Missing test dependencies
```bash
pip install -r requirements-dev.txt
```

### Mock not working as expected
- Check that you're patching the right location
- Use `patch.object()` for class methods
- Verify the patch path matches the import path

## Best Practices

1. **One assertion per test**: Each test should verify one thing
2. **Descriptive test names**: Use clear, descriptive names
3. **Arrange-Act-Assert**: Structure tests clearly
4. **Independent tests**: Tests should not depend on each other
5. **Clean up**: Use `setUp()` and `tearDown()` or fixtures
6. **Mock external calls**: Don't make real API calls in unit tests

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
