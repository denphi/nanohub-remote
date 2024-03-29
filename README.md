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
</table>
A set of tools/apps to run on nanohub

## Installation


```bashv
pip install nanohub-remote
```

## Usage


```python

import nanohub.remote as nr
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




