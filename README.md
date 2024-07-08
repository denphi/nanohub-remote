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


```python

import nanohubremote as nr
auth_data = {
  'client_id': XXXXXXXX,
  'client_secret': XXXXXXXX,
  'grant_type': 'password',
  'username': XXXXXXXX,
  'password': XXXXXXXX
}

# to get username and password, register on nanohub.org (https://nanohub.org/register/)
# to get client id and secret, create a web application (https://nanohub.org/developer/api/applications/new), use "https://127.0.0.1" as Redirect URL

session = nr.Session(auth_data)

```

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




