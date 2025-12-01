# Nanohub remote
# Stats

<table>
    <tr>
        <td>Latest Release</td>
        <td>
            <a href="https://pypi.org/project/nanohub-remote/"/>
            <img src="https://badge.fury.io/py/nanohub-remote.svg"/>
        </td>
    </tr>
    <tr>
        <td>PyPI Downloads</td>
        <td>
            <a href="https://pepy.tech/project/nanohub-remote"/>
            <img src="https://pepy.tech/badge/nanohub-remote/month"/>
            <img src="https://pepy.tech/badge/nanohub-remote"/>
        </td>
    </tr>
    <tr>
        <td>Nanohub Tutorial</td>
        <td>
            <a href='https://nanohub.org/tools/nhremote/invoke/5' target='_blank'><img src='https://img.shields.io/badge/nhremote-nanoHUB-5CA0BC.svg?style=&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHdpZHRoPSI3OS43IiBoZWlnaHQ9IjgzIj48ZyBmaWxsPSIjRkZGIj48cGF0aCBkPSJtMzYgNDEgMS0zaDRsMSAzdjhsMSAxIDEgMWgydi05YzAtMyAwLTUtMi02bC01LTItNSAyLTIgNnY5aDRWNDF6Ii8+PHBhdGggZD0iTTcxIDM5Yy0zIDAtNiAxLTcgNGgtM2MwLTQtMS03LTMtMTBsNC0zIDQgMWE3IDcgMCAxIDAtNy01bC0zIDMtNy01di0xbDItNWgxYTggOCAwIDEgMC01LTJsLTIgNmEyMSAyMSAwIDAgMC0xMSAwbC0xLTNhNyA3IDAgMSAwLTQgMnYybDEgMWMtNCAxLTcgNC05IDdsLTMtMmE4IDggMCAxIDAtMiA0bDMgMmEyMSAyMSAwIDAgMC0xIDEwaC0xbC0zIDFhNyA3IDAgMSAwIDEgNGw0LTFjMSAzIDIgNiA1IDhsLTEgMS00IDQtMy0xYTggOCAwIDEgMCA3IDRsNC01YzMgMyA2IDQgMTEgNHY1Yy0zIDEtNCAzLTQgNiAwIDQgMyA3IDYgNyA0IDAgNy0zIDctNyAwLTMtMi02LTUtNnYtNWMzIDAgNy0yIDEwLTR2MWw0IDNhOCA4IDAgMSAwIDE1IDVjMC01LTQtOC04LThoLTRsLTMtMy0xLTFjMy0zIDQtNiA1LTEwaDRhNyA3IDAgMCAwIDE0LTFjMC00LTMtNy03LTd6bS01LTE3YTIgMiAwIDEgMSAwIDUgMiAyIDAgMCAxIDAtNXpNMTAgMzJhNCA0IDAgMSAxIDAtOCA0IDQgMCAwIDEgMCA4ek04IDUyYTIgMiAwIDEgMSAwLTUgMiAyIDAgMCAxIDAgNXptOCAyMmE0IDQgMCAxIDEgMC04IDQgNCAwIDAgMSAwIDh6bTQ3LTlhNCA0IDAgMSAxIDAgOCA0IDQgMCAwIDEgMC04ek01MiA2YTQgNCAwIDEgMSAwIDggNCA0IDAgMCAxIDAtOHpNMjggMTZhMiAyIDAgMSAxIDAtNCAyIDIgMCAwIDEgMCA0em0xMSAxMmExNSAxNSAwIDEgMSAwIDMwIDE1IDE1IDAgMCAxIDAtMzB6bTQgNDdhMiAyIDAgMSAxLTUgMCAyIDIgMCAwIDEgNSAwem0yOC0yNmEzIDMgMCAxIDEgMC02IDMgMyAwIDAgMSAwIDZ6Ii8+PC9nPjwvc3ZnPg=='></a>
        </td>
    </tr>
</table>
A set of tools/apps to run on nanohub

## Installation


```bashv
pip install nanohub-remote
```

## Usage

### Basic Authentication

```python
import nanohubremote as nr

# Option 1: OAuth Password Grant (requires web application)
auth_data = {
  'client_id': 'XXXXXXXX',
  'client_secret': 'XXXXXXXX',
  'grant_type': 'password',
  'username': 'your_username',
  'password': 'your_password'
}

# Option 2: Personal Access Token (recommended)
auth_data = {
  'grant_type': 'personal_token',
  'token': 'your_personal_token'
}

# to get username and password, register on nanohub.org (https://nanohub.org/register/)
# to get client id and secret, create a web application (https://nanohub.org/developer/api/applications/new), use "https://127.0.0.1" as Redirect URL
# to get a personal token, go to https://nanohub.org/developer/api/tokens

# Create a session
session = nr.Session(auth_data)

# Or use as a context manager (recommended - automatically cleans up resources)
with nr.Session(auth_data) as session:
    # Your code here
    pass
```

### Session Configuration

The Session class supports advanced configuration options:

```python
session = nr.Session(
    auth_data,
    url="https://nanohub.org/api",  # Custom API URL
    timeout=10,                       # Request timeout in seconds (default: 5)
    max_retries=5,                    # Maximum retries for failed requests (default: 3)
    pool_connections=20,              # Connection pool size (default: 10)
    pool_maxsize=20                   # Max pool size (default: 10)
)
```

### HTTP Methods

The Session class provides methods for all standard HTTP verbs:

```python
with nr.Session(auth_data) as session:
    # GET request
    response = session.requestGet('tools/list')
    tools = response.json()

    # POST request with form data
    response = session.requestPost('endpoint', data={'key': 'value'})

    # POST request with JSON
    response = session.requestPost('endpoint', json={'key': 'value'})

    # PUT request
    response = session.requestPut('resource/123', json={'status': 'updated'})

    # DELETE request
    response = session.requestDelete('resource/123')

    # PATCH request
    response = session.requestPatch('resource/123', json={'field': 'new_value'})
```

### Features

- **Connection Pooling**: Reuses HTTP connections for better performance
- **Automatic Retries**: Automatically retries failed requests (configurable)
- **Token Management**: Handles OAuth token refresh automatically
- **Context Manager**: Use `with` statement for automatic resource cleanup
- **Persistent Headers**: Headers are maintained across all requests

## Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=nanohubremote --cov-report=html

# Run specific test file
pytest tests/test_session.py
```

See [tests/README.md](tests/README.md) for detailed testing documentation.

## Available Nanohub Points

## Tools

```python
TOOLNAME = '' # valid Nanoohub tool name e.g. pntoy
tool = nr.Tool(auth_data)

# Get Available input parameters
params = tool.getToolParameters(TOOLNAME)

# Submit a simulation experiment
job_id = tool.submitTool(params)

# Check Status
status = tool.checkStatus(job_id['job_id'])

# Get Results
results = tool.getResults(job_id['job_id'])

# Submit an wait for results
results = tool.submitTool(params, wait_results=True)
```

## Sim2Ls

```python
TOOLNAME = '' # valid Nanoohub tool name e.g. pntoy
s2l = nr.Sim2L(auth_data)

# Get Available input parameters
params = s2l.getToolParameters(TOOLNAME)

# Submit a simulation experiment
job_id = s2l.submitTool(params)

# Check Status
status = s2l.checkStatus(job_id['job_id'])

# Get Results
results = s2l.getResults(job_id['job_id'])

# Submit an wait for results
results = s2l.submitTool(params, wait_results=True)
```




