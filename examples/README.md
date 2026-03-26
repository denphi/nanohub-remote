# nanohub-remote Examples

This directory contains example notebooks and Python scripts demonstrating how to use the `nanohubremote` library.

## Session Examples

### Basic Session Usage
- **`basic_session.ipynb`** / **`basic_session.py`**
  - Personal token authentication
  - Simple GET requests
  - POST requests with JSON
  - Error handling

### Session Management
- **`session_management.ipynb`** / **`session_management.py`**
  - Managing authentication state
  - URL construction helpers
  - Custom configuration (timeouts, retries, connection pooling)
  - Session reuse for multiple requests

## Tool Examples

### Rappture Tools
- **`pntoy.ipynb`** - Example using the pntoy (PN Junction) tool
- **`st4pnjunction.ipynb`** - Example using the st4pnjunction tool
- **`database.ipynb`** - Database integration example

## Getting Started

1. Install the library:
   ```bash
   pip install nanohub-remote
   ```

2. Set up authentication:
   - For personal token: Get your token from https://nanohub.org/developer/api
   - For OAuth: Create an application at https://nanohub.org/developer/api/applications/new

3. Run an example:
   ```bash
   python basic_session.py
   ```
   
   Or open a notebook in Jupyter:
   ```bash
   jupyter notebook basic_session.ipynb
   ```

## Authentication

All examples use placeholder credentials. Replace with your actual credentials:

```python
# Personal Token
auth_data = {
    'grant_type': 'personal_token',
    'token': 'your_actual_token_here'
}

# OAuth
auth_data = {
    'client_id': 'your_client_id',
    'client_secret': 'your_client_secret',
    'grant_type': 'password',
    'username': 'your_username',
    'password': 'your_password'
}
```

## Documentation

For more information, see the [full documentation](https://nanohub-remote.readthedocs.io/).
