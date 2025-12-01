# Testing Documentation

## Overview

This document describes the testing infrastructure for the nanohub-remote library.

## Test Suite

The test suite includes comprehensive unit tests for the Session class improvements:

- **25 unit tests** covering all new functionality
- **100% pass rate**
- **Mock-based testing** - no real API calls needed
- **Fast execution** - all tests run in under 1 second

## Test Coverage

### Session Class Tests

#### Initialization (5 tests)
- ✅ Personal token authentication
- ✅ Custom API URL
- ✅ Custom timeout settings
- ✅ Custom retry configuration
- ✅ Connection pool configuration

#### HTTP Methods (9 tests)
- ✅ GET requests
- ✅ POST requests with form data
- ✅ POST requests with JSON
- ✅ PUT requests
- ✅ DELETE requests
- ✅ PATCH requests
- ✅ Custom headers support
- ✅ Custom timeout per request
- ✅ URL construction

#### Authentication (5 tests)
- ✅ OAuth authentication flow
- ✅ Token validation success
- ✅ Token validation with errors
- ✅ Missing access token handling
- ✅ Session clearing

#### Context Manager (3 tests)
- ✅ Enter/exit functionality
- ✅ Automatic resource cleanup
- ✅ Manual close

#### Inherited Classes (3 tests)
- ✅ Tools.list() method
- ✅ Tools.list() with filters
- ✅ Sim2L.list() method

## Running Tests

### Quick Start
```bash
# Install dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=nanohubremote
```

### Detailed Options
```bash
# Run specific test file
pytest tests/test_session.py

# Run specific test class
pytest tests/test_session.py::TestSessionMethods

# Run specific test
pytest tests/test_session.py::TestSessionMethods::test_request_get

# Generate HTML coverage report
pytest --cov=nanohubremote --cov-report=html
open htmlcov/index.html

# Run with short traceback
pytest --tb=short

# Stop on first failure
pytest -x
```

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── README.md               # Testing guide
└── test_session.py         # Session class unit tests
    ├── TestSessionInitialization
    ├── TestSessionMethods
    ├── TestSessionAuthentication
    ├── TestSessionContextManager
    ├── TestToolsClass
    └── TestSim2LClass
```

## Mocking Strategy

Tests use `unittest.mock` to isolate the code under test:

```python
@patch('requests.Session.get')
def test_request_get(self, mock_get):
    """Test GET request method."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    response = self.session.requestGet('endpoint')

    self.assertEqual(response.status_code, 200)
    mock_get.assert_called_once()
```

### What We Mock
- External HTTP calls (`requests.Session` methods)
- Time-dependent operations
- OAuth token responses

### What We Don't Mock
- The Session class itself
- Internal logic and state management
- Request parameter handling

## Continuous Integration

Tests should be integrated into CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements-dev.txt
      - run: pip install -e .
      - run: pytest --cov=nanohubremote
```

## Coverage Goals

- **Overall target**: 80%+ code coverage
- **Critical paths**: 100% coverage for authentication and request methods
- **Current coverage**: Session class improvements have comprehensive test coverage

## Adding New Tests

When adding new functionality:

1. **Write tests first** (TDD approach)
2. **Follow naming convention**: `test_<feature_name>`
3. **One concept per test**: Keep tests focused
4. **Use descriptive names**: Test names should describe what they test
5. **Mock external dependencies**: Don't make real API calls
6. **Clean up resources**: Use `setUp()` and `tearDown()`

### Example Template

```python
class TestNewFeature(unittest.TestCase):
    """Test description for new feature."""

    def setUp(self):
        """Set up test fixtures."""
        self.credentials = {
            'grant_type': 'personal_token',
            'token': 'test_token'
        }
        self.session = Session(self.credentials)

    def test_new_feature(self):
        """Test specific behavior."""
        # Arrange
        expected = 'some_value'

        # Act
        result = self.session.some_method()

        # Assert
        self.assertEqual(result, expected)
```

## Best Practices

1. **Arrange-Act-Assert**: Structure tests clearly
2. **Independent tests**: No dependencies between tests
3. **Fast tests**: Use mocks to avoid slow operations
4. **Clear assertions**: One primary assertion per test
5. **Descriptive failures**: Tests should clearly indicate what failed
6. **Maintain tests**: Update tests when code changes

## Troubleshooting

### Import Errors
```bash
# Install package in development mode
pip install -e .
```

### Mock Not Working
- Verify patch path matches import location
- Use `@patch` at the point of use, not definition
- Check mock is being called correctly

### Slow Tests
- Ensure external calls are mocked
- Check for accidental real API calls
- Use `--durations=10` to find slow tests

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [unittest.mock guide](https://docs.python.org/3/library/unittest.mock.html)
- [Coverage.py documentation](https://coverage.readthedocs.io/)
- [Test Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)

## Summary

The test suite provides:
- ✅ Comprehensive coverage of Session improvements
- ✅ Fast, reliable, isolated tests
- ✅ Easy to run and maintain
- ✅ Clear documentation
- ✅ Foundation for future testing
