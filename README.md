# Nanohubtools

A set of tools/apps to run on nanohub

## Installation


```bash
pip install nanohub-remote
```

## Usage


```python

import nanohub-remote as nr
auth_data = {
  'client_id': XXXXXXXX,
  'client_secret': XXXXXXXX,
  'grant_type': 'password',
  'username': XXXXXXXX,
  'password': XXXXXXXX
}

# to get username and password, register on nanohub.org (https://nanohub.org/register/)
# to get client id and secret, create a web application (https://nanohub.org/developer/api/applications/new), use "https://127.0.0.1" as Redirect URL

session = nr.session(auth_data)

```

## Available Nanohub Points
