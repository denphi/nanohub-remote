#  Copyright 2025 HUBzero Foundation, LLC.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

#  HUBzero is a registered trademark of Purdue University.

#  Authors:
#  Daniel Mejia (denphi), Purdue University (denphi@denphi.com)


import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import re
import xml.etree.ElementTree as ET
import copy
from time import sleep, time
from .params import ParamsFactory, Params, Boolean
from .output import OutputFactory, Output


class Session():
    """
    Base class for managing a session with the nanoHUB API.

    Attributes:
        credentials (dict): Dictionary containing authentication credentials.
        headers (dict): Dictionary of HTTP headers to be sent with requests.
        authenticated (bool): Flag indicating if the session is authenticated.
        session (requests.Session): Persistent HTTP session object.
    """
    credentials = {}
    headers = {}
    authenticated = False

    def __init__(self, credentials, **kwargs):
        """
        Initialize the Session.

        Args:
            credentials (dict): Authentication credentials.
            **kwargs: Additional arguments.
                url (str): Base URL for the API. Defaults to "https://nanohub.org/api".
                timeout (int): Request timeout in seconds. Defaults to 5.
                max_retries (int): Maximum number of retries for failed requests. Defaults to 3.
                pool_connections (int): Number of connection pool. Defaults to 10.
                pool_maxsize (int): Maximum size of the pool. Defaults to 10.
        """
        self.credentials = credentials
        self.url = kwargs.get("url", "https://nanohub.org/api")
        self.timeout = kwargs.get("timeout", 5)

        # Create a requests.Session with retry logic and connection pooling
        self._session = requests.Session()

        # Configure retry strategy
        max_retries = kwargs.get("max_retries", 3)
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
        )

        # Configure connection pooling
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=kwargs.get("pool_connections", 10),
            pool_maxsize=kwargs.get("pool_maxsize", 10)
        )

        self._session.mount("http://", adapter)
        self._session.mount("https://", adapter)

        self.clearSession()
        self.validateSession()

    def clearSession(self):
        """
        Clear the current session and reset authentication state.
        """
        if self.credentials["grant_type"] == "personal_token":
            self.authenticated = True
            self.access_token = self.credentials["token"]
            self.headers = {
                'Authorization': 'Bearer '+ self.access_token,
                'Referer': self.url
            }
            # Update session headers
            self._session.headers.update(self.headers)
            self.refresh_token = self.credentials["token"]
            self.expires_in = 14400
        else:
            self.authenticated = False
            self.headers = {}
            # Clear session headers
            self._session.headers.clear()
            self.access_token = ""
            self.refresh_token = ""
            self.expires_in = 0

    def getUrl(self, entry_point):
        """
        Construct the full URL for a given API entry point.

        Args:
            entry_point (str): The API endpoint path.

        Returns:
            str: The full URL.
        """
        return self.url + "/" + entry_point

    def requestPost(self, url, **kwargs):
        """
        Perform a POST request to the API.

        Args:
            url (str): The API endpoint.
            **kwargs: Additional arguments for the request (data, json, headers, timeout).

        Returns:
            requests.Response: The response object.
        """
        data = kwargs.get("data", {})
        json_data = kwargs.get("json", None)
        headers = kwargs.get("headers", None)
        timeout = kwargs.get("timeout", self.timeout)

        # Use session's headers if not explicitly provided
        if headers is not None:
            return self._session.post(self.getUrl(url), data=data, json=json_data, headers=headers, timeout=timeout)
        else:
            return self._session.post(self.getUrl(url), data=data, json=json_data, timeout=timeout)

    def requestGet(self, url, **kwargs):
        """
        Perform a GET request to the API.

        Args:
            url (str): The API endpoint.
            **kwargs: Additional arguments for the request (data, headers, timeout).

        Returns:
            requests.Response: The response object.
        """
        data = kwargs.get("data", {})
        headers = kwargs.get("headers", None)
        timeout = kwargs.get("timeout", self.timeout)

        # Use session's headers if not explicitly provided
        # GET requests send parameters as query params; bodies are ignored by servers.
        if headers is not None:
            return self._session.get(self.getUrl(url), params=data, headers=headers, timeout=timeout)
        else:
            return self._session.get(self.getUrl(url), params=data, timeout=timeout)

    def requestPut(self, url, **kwargs):
        """
        Perform a PUT request to the API.

        Args:
            url (str): The API endpoint.
            **kwargs: Additional arguments for the request (data, json, headers, timeout).

        Returns:
            requests.Response: The response object.
        """
        data = kwargs.get("data", None)
        json_data = kwargs.get("json", None)
        headers = kwargs.get("headers", None)
        timeout = kwargs.get("timeout", self.timeout)

        # Use session's headers if not explicitly provided
        if headers is not None:
            return self._session.put(self.getUrl(url), data=data, json=json_data, headers=headers, timeout=timeout)
        else:
            return self._session.put(self.getUrl(url), data=data, json=json_data, timeout=timeout)

    def requestDelete(self, url, **kwargs):
        """
        Perform a DELETE request to the API.

        Args:
            url (str): The API endpoint.
            **kwargs: Additional arguments for the request (data, headers, timeout).

        Returns:
            requests.Response: The response object.
        """
        data = kwargs.get("data", {})
        headers = kwargs.get("headers", None)
        timeout = kwargs.get("timeout", self.timeout)

        # Use session's headers if not explicitly provided
        if headers is not None:
            return self._session.delete(self.getUrl(url), data=data, headers=headers, timeout=timeout)
        else:
            return self._session.delete(self.getUrl(url), data=data, timeout=timeout)

    def requestPatch(self, url, **kwargs):
        """
        Perform a PATCH request to the API.

        Args:
            url (str): The API endpoint.
            **kwargs: Additional arguments for the request (data, json, headers, timeout).

        Returns:
            requests.Response: The response object.
        """
        data = kwargs.get("data", None)
        json_data = kwargs.get("json", None)
        headers = kwargs.get("headers", None)
        timeout = kwargs.get("timeout", self.timeout)

        # Use session's headers if not explicitly provided
        if headers is not None:
            return self._session.patch(self.getUrl(url), data=data, json=json_data, headers=headers, timeout=timeout)
        else:
            return self._session.patch(self.getUrl(url), data=data, json=json_data, timeout=timeout)

    def validateTokenRequest(self, request, timestamp):
        """
        Validate the response from a token request and update session state.

        Args:
            request (requests.Response): The response from the token request.
            timestamp (int): The current timestamp.

        Raises:
            ConnectionError: If the response contains errors.
            AttributeError: If expected fields are missing in the response.
        """
        auth_json = request.json()
        if 'errors' in auth_json:
            raise ConnectionError(json.dumps(auth_json['errors']))
        if 'access_token' in auth_json:
            self.access_token = auth_json['access_token']
        else:
            raise AttributeError('access_token')
        if 'expires_in' in auth_json:
            self.expires_in = timestamp + int(auth_json['expires_in']) - 1
        else:
            raise AttributeError('expires_in')
        if 'refresh_token' in auth_json:
            self.refresh_token = auth_json['refresh_token']
        self.headers = {'Authorization': 'Bearer '+self.access_token}
        # Update session headers with new token
        self._session.headers.update(self.headers)
        self.authenticated = True

    def validateSession(self):
        """
        Ensure the session is valid and authenticated. Refreshes token if necessary.

        Raises:
            ConnectionError: If authentication fails or token is missing.
        """
        if self.credentials["grant_type"] == "personal_token":
            return

        timestamp = int(time())
        if self.authenticated is True:
            if self.expires_in > timestamp:
                if (self.refresh_token != ""):
                    try:
                        refresh_token = {
                            'client_id': self.credentials['client_id'],
                            'client_secret': self.credentials['client_secret'],
                            'grant_type': 'refresh_token',  # Fixed: should be 'refresh_token', not self.credentials['refresh_token']
                            'refresh_token': self.refresh_token,
                        }
                        request = self.requestPost(
                            'developer/oauth/token',
                            data=refresh_token,
                            headers={},
                            timeout=self.timeout
                        )
                        self.validateTokenRequest(request, timestamp)
                    except (requests.RequestException, ValueError, KeyError, AttributeError) as e:
                        # Clear session on any request, JSON parsing, or token validation error
                        self.clearSession()
                else:
                    self.clearSession()
        if self.authenticated is False:
            try:
                request = self.requestPost(
                    'developer/oauth/token',
                    data=self.credentials,
                    headers={},
                    timeout=self.timeout
                )
                self.validateTokenRequest(request, timestamp)
            except AttributeError as e:
                self.clearSession()
                raise ConnectionError(f"Authentication Token not found: {str(e)}")
            except ConnectionError as ce:
                self.clearSession()
                raise ce
            except (requests.RequestException, ValueError, KeyError) as e:
                self.clearSession()
                raise ConnectionError(f"Invalid Authentication: {str(e)}")

    def close(self):
        """
        Close the underlying requests.Session and release resources.

        This should be called when the Session is no longer needed, or use
        the Session as a context manager.
        """
        if hasattr(self, '_session'):
            self._session.close()

    def __enter__(self):
        """
        Enter context manager.

        Returns:
            Session: The session instance.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit context manager and close session.

        Args:
            exc_type: Exception type if an error occurred.
            exc_val: Exception value if an error occurred.
            exc_tb: Exception traceback if an error occurred.
        """
        self.close()
        return False

    def __del__(self):
        """
        Destructor to ensure session is closed when object is garbage collected.
        """
        try:
            self.close()
        except Exception:
            pass


class Tools(Session):
    """
    Class for interacting with standard nanoHUB tools (Rappture-based).
    """
    periodicelement = [
        ('Hydrogen', 'H'),
        ('Helium', 'He'),
        ('Lithium', 'Li'),
        ('Beryllium', 'Be'),
        ('Boron', 'B'),
        ('Carbon', 'C'),
        ('Nitrogen', 'N'),
        ('Oxygen', 'O'),
        ('Fluorine', 'F'),
        ('Neon', 'Ne'),
        ('Sodium', 'Na'),
        ('Magnesium', 'Mg'),
        ('Aluminium', 'Al'),
        ('Silicon', 'Si'),
        ('Phosphorus', 'P'),
        ('Sulfur', 'S'),
        ('Chlorine', 'Cl'),
        ('Argon', 'Ar'),
        ('Potassium', 'K'),
        ('Calcium', 'Ca'),
        ('Scandium', 'Sc'),
        ('Titanium', 'Ti'),
        ('Vanadium', 'V'),
        ('Chromium', 'Cr'),
        ('Manganese', 'Mn'),
        ('Iron', 'Fe'),
        ('Cobalt', 'Co'),
        ('Nickel', 'Ni'),
        ('Copper', 'Cu'),
        ('Zinc', 'Zn'),
        ('Gallium', 'Ga'),
        ('Germanium', 'Ge'),
        ('Arsenic', 'As'),
        ('Selenium', 'Se'),
        ('Bromine', 'Br'),
        ('Krypton', 'Kr'),
        ('Rubidium', 'Rb'),
        ('Strontium', 'Sr'),
        ('Yttrium', 'Y'),
        ('Zirconium', 'Zr'),
        ('Niobium', 'Nb'),
        ('Molybdenum', 'Mo'),
        ('Technetium', 'Tc'),
        ('Ruthenium', 'Ru'),
        ('Rhodium', 'Rh'),
        ('Palladium', 'Pd'),
        ('Silver', 'Ag'),
        ('Cadmium', 'Cd'),
        ('Indium', 'In'),
        ('Tin', 'Sn'),
        ('Antimony', 'Sb'),
        ('Tellurium', 'Te'),
        ('Iodine', 'I'),
        ('Xenon', 'Xe'),
        ('Caesium', 'Cs'),
        ('Barium', 'Ba'),
        ('Lanthanum', 'La'),
        ('Cerium', 'Ce'),
        ('Praseodymium', 'Pr'),
        ('Neodymium', 'Nd'),
        ('Promethium', 'Pm'),
        ('Samarium', 'Sm'),
        ('Europium', 'Eu'),
        ('Gadolinium', 'Gd'),
        ('Terbium', 'Tb'),
        ('Dysprosium', 'Dy'),
        ('Holmium', 'Ho'),
        ('Erbium', 'Er'),
        ('Thulium', 'Tm'),
        ('Ytterbium', 'Yb'),
        ('Lutetium', 'Lu'),
        ('Hafnium', 'Hf'),
        ('Tantalum', 'Ta'),
        ('Tungsten', 'W'),
        ('Rhenium', 'Re'),
        ('Osmium', 'Os'),
        ('Iridium', 'Ir'),
        ('Platinum', 'Pt'),
        ('Gold', 'Au'),
        ('Mercury', 'Hg'),
        ('Thallium', 'Tl'),
        ('Lead', 'Pb'),
        ('Bismuth', 'Bi'),
        ('Polonium', 'Po'),
        ('Astatine', 'At'),
        ('Radon', 'Rn'),
        ('Francium', 'Fr'),
        ('Radium', 'Ra'),
        ('Actinium', 'Ac'),
        ('Thorium', 'Th'),
        ('Protactinium', 'Pa'),
        ('Uranium', 'U'),
        ('Neptunium', 'Np'),
        ('Plutonium', 'Pu'),
        ('Americium', 'Am'),
        ('Curium', 'Cm'),
        ('Berkelium', 'Bk'),
        ('Californium', 'Cf'),
        ('Einsteinium', 'Es'),
        ('Fermium', 'Fm'),
        ('Mendelevium', 'Md'),
        ('Nobelium', 'No'),
        ('Lawrencium', 'Lr'),
        ('Rutherfordium', 'Rf'),
        ('Dubnium', 'Db'),
        ('Seaborgium', 'Sg'),
        ('Bohrium', 'Bh'),
        ('Hassium', 'Hs'),
        ('Meitnerium', 'Mt')
    ]
    discardtags = ["phase", "group", "option", "image", "note", "field"]

    def __init__(self, credentials, **kwargs):
        self.cached_schema = None
        self.cached_toolname = None
        Session.__init__(self, credentials, **kwargs)

    def list(self, filters=[]):
        """
        List available tools.

        Args:
            filters (list): List of tool aliases to filter by.

        Returns:
            list: List of tool dictionaries.
        """
        request = self.requestGet('tools/list', data={})
        tools_request = request.json()
        tools = []
        if 'tools' in tools_request:
            for tool in tools_request['tools']:
                if len(filters) == 0 or tool['alias'] in filters:
                    tools.append(tool)
        return tools

    def info(self, toolname, version="current"):
        """
        Get information about a tool.

        Args:
            toolname (str): Name of the tool.
            version (str): Tool version. Defaults to "current".

        Returns:
            dict: Tool information.
        """
        raise ConnectionError('Method is deprecated')
        request = self.requestPost('tools/info?tool='+toolname, data={})
        info_request = request.json()
        return info_request

    def getResults(self, session_id, **kwargs):
        """
        Get results for a specific session.

        Args:
            session_id (str): The session ID.
            **kwargs: Additional arguments (timeout, verbose).

        Returns:
            list: List of Output objects.

        Raises:
            ConnectionError: If not connected.
            AttributeError: If results are not available.
        """
        timeout = kwargs.get("timeout", 60)
        self.validateSession()
        if (self.authenticated is False):
            raise ConnectionError('not connected')
        verbose = kwargs.get("verbose", False)
        status = self.checkStatus(session_id, verbose=verbose, timeout=timeout)
        if verbose:
            print(status)
        if 'success' in status and status['success']:
            if 'status' in status:
                if 'finished' in status:
                    if status['finished'] and status['run_file'] != "":
                        results_json = {
                            'session_num': session_id,
                            'run_file': status['run_file']
                        }
                        xml = ET.fromstring(self.loadResults(results_json))
                        outputs = xml.find('output')
                        outputs = [OutputFactory.builder(o) for o in outputs]
                        outputs = [o for o in outputs if o is not None]
                        return outputs
                else:
                    return []

        raise AttributeError('results are not available')

    def loadResults(self, results_json, **kwargs):
        """
        Load results from the server.

        Args:
            results_json (dict): JSON containing session info.
            **kwargs: Additional arguments (timeout).

        Returns:
            str: XML string of results.
        """
        timeout = kwargs.get("timeout", 30)
        self.validateSession()
        if (self.authenticated is False):
            raise ConnectionError('not connected')
        request = self.requestPost(
            'tools/output', data=results_json, timeout=timeout)
        result_json = request.json()
        if 'output' in result_json:
            return result_json['output']
        else:
            return ''

    def checkStatus(self, session_id, **kwargs):
        """
        Check the status of a session.

        Args:
            session_id (str): The session ID.
            **kwargs: Additional arguments (timeout, verbose).

        Returns:
            dict: Status dictionary.
        """
        timeout = kwargs.get("timeout", 30)
        self.validateSession()
        if (self.authenticated is False):
            raise ConnectionError('not connected')
        status_json = self.requestPost(
            'tools/status', data={'session_num': str(session_id)}, timeout=timeout)
        verbose = kwargs.get("verbose", False)
        if verbose:
            print(status_json)
        return status_json.json()

    def getSession(self, driver_json, **kwargs):
        """
        Start a tool session.

        Args:
            driver_json (dict): Driver configuration for the tool.
            **kwargs: Additional arguments (timeout).

        Returns:
            str: The session ID.

        Raises:
            ConnectionError: If launch fails.
        """
        timeout = kwargs.get("timeout", 30)
        self.validateSession()
        if (self.authenticated is False):
            raise ConnectionError('not connected')
        request = self.requestPost(
            '/tools/run', data=driver_json, timeout=timeout)
        run_json = request.json()
        if 'session' in run_json:
            return run_json['session']
        else:
            msg = 'launch_tool failed ({0}): {1}\n'.format(
                run_json['code'], run_json['message'])
            raise ConnectionError(msg)

    def getRapptureSchema(self, toolname, force=False, **kwargs):
        """
        Get the Rappture XML schema for a tool.

        Args:
            toolname (str): Name of the tool.
            force (bool): Force refresh of cached schema.
            **kwargs: Additional arguments (timeout).

        Returns:
            str: Rappture XML schema.
        """
        timeout = kwargs.get("timeout", 30)
        self.validateSession()
        if (self.authenticated is False):
            raise ConnectionError('not connected')
        if (self.cached_schema is not None and self.cached_toolname == toolname and force is False):
            return self.cached_schema
        else:
            request = self.requestPost(
                'tools/' + toolname + '/rappturexml', data={}, timeout=timeout)
            rappturexml = request.text
            self.cached_schema = rappturexml
            self.cached_toolname = toolname
        return rappturexml

    def getToolInputs(self, toolname, **kwargs):
        """
        Get tool input parameters from the schema.

        Args:
            toolname (str): Name of the tool.
            **kwargs: Additional arguments (timeout).

        Returns:
            dict: Dictionary of input parameters.
        """
        timeout = kwargs.get("timeout", 30)
        xml = ET.fromstring(self.getRapptureSchema(toolname, timeout=timeout))
        inputs = xml.find('input')
        params = {}
        for elem in inputs.iter():
            id = ''
            if 'id' in elem.attrib:
                id = elem.attrib['id']
            if elem.tag not in Tools.discardtags and id != "":
                if id not in params:
                    descriptiont = ""
                    labelt = ""
                    about = elem.find("about")
                    description = elem.find('description')
                    if description is not None:
                        descriptiont = description.text
                    if (about is not None):
                        description = about.find('description')
                        if description is not None:
                            descriptiont = description.text
                        label = about.find("label")
                        if (label is not None):
                            labelt = label.text

                    param = {"type": elem.tag, "description": descriptiont}
                    param['id'] = id
                    param['label'] = labelt
                    param['units'] = elem.find('units')
                    if param['units'] is not None:
                        param['units'] = param['units'].text
                    param['default'] = elem.find('default')
                    if param['default'] is not None:
                        param['default'] = param['default'].text
                    param['min'] = elem.find('min')
                    if param['min'] is not None:
                        param['min'] = param['min'].text
                    param['max'] = elem.find('max')
                    if param['max'] is not None:
                        param['max'] = param['max'].text
                    param['current'] = elem.find('current')
                    if param['current'] is not None:
                        param['current'] = param['current'].text
                    options = elem.findall('option')
                    opt_list = []
                    for option in options:
                        lvalue = option.find("value")
                        opt_val = ['', '']
                        if (lvalue is not None):
                            if (lvalue.text != ""):
                                opt_val[0] = lvalue.text
                                opt_val[1] = lvalue.text
                        labout = option.find("about")
                        if (labout is not None):
                            llabel = labout.find("label")
                            if (llabel is not None):
                                if (llabel.text != ""):
                                    opt_val[0] = llabel.text
                                    if opt_val[1] == '':
                                        opt_val[1] = llabel.text
                        opt_list.append((opt_val[0], opt_val[1]))
                    param['options'] = opt_list

                    if param['type'] == "periodicelement":
                        param['type'] = 'choice'
                        param['options'] = Tools.periodicelement
                    if len(param['options']) > 0:
                        if param['default'] not in [p[1] for p in param['options']]:
                            param['default'] = param['options'][0][1]
                    if param['type'] == "string":
                        if param['default'] is not None:
                            if '\n' in param['default'].strip():
                                param['type'] = "text"
                    params[id] = param
        return params

    def getToolLayout(self, toolname, **kwargs):
        """
        Get the layout of the tool's user interface.

        Args:
            toolname (str): Name of the tool.
            **kwargs: Additional arguments (timeout).

        Returns:
            dict: Layout dictionary.
        """
        timeout = kwargs.get("timeout", 30)
        xml = ET.fromstring(self.getRapptureSchema(toolname, timeout=timeout))
        params = {}
        for elem in ["input", "output"]:
            input = xml.find(elem)
            if input is not None:
                param = {"type": "group"}
                param['id'] = ''
                param['label'] = ''
                param['layout'] = ''
                param['children'] = self.getToolLayoutParams(input)
                if (len([c for c in param['children'] if c["type"] not in ["group", "tab"]]) == 0 or param['layout'] == "vertical"):
                    param['type'] = 'tab'
                    param['layout'] = 'horizontal'
                params[elem] = param
        return params

    def getToolLayoutParams(self, group, **kwargs):
        """
        Recursively parse layout parameters.

        Args:
            group (xml.etree.ElementTree.Element): XML element representing a group.
            **kwargs: Additional arguments.

        Returns:
            list: List of layout parameters.
        """
        params = []
        for elem in group:
            id = ''
            if 'id' in elem.attrib:
                id = elem.attrib['id']
            about = elem.find("about")
            labelt = None
            enablet = None
            layoutt = "vertical"
            if (about is not None):
                label = about.find("label")
                if (label is not None):
                    labelt = label.text
                enable = about.find("enable")
                if (enable is not None):
                    enablet = enable.text
                layout = about.find("layout")
                if (layout is not None):
                    layoutt = layout.text

            if (elem.tag == "phase"):
                for p in elem:
                    params += self.getToolLayoutParams(p)
            elif (elem.tag == "group"):
                param = {"type": "tab"}
                param['label'] = labelt
                param['enable'] = enablet
                param['layout'] = layoutt
                param['children'] = self.getToolLayoutParams(elem)
                if (len([c for c in param['children'] if c["type"] not in ["group", "tab"]]) > 0 or param['layout'] == "vertical"):
                    param['type'] = 'group'
                    param['layout'] = 'horizontal'
                params.append(param)
            else:
                if elem.tag not in Tools.discardtags and id != "":
                    param = {"type": elem.tag}
                    if param['type'] == "periodicelement":
                        param['type'] = 'choice'
                    param['id'] = id
                    param['label'] = labelt
                    param['enable'] = enablet
                    if param['enable'] is not None:
                        restrictions = re.findall(
                            r"\(([a-zA-Z][a-zA-Z0-9_]+)\) +?([=!><]+) +?([a-zA-Z0-9_\"]+) ?([\&\|]*)?", param['enable'])
                        param['enable'] = []
                        for restriction in restrictions:
                            r = restriction[2]
                            if (r in ["\"yes\"", "\"true\"", "\"on\"", "yes", 1, "si", True, "true", "on"]):
                                r = True
                            elif (r in ["\"no\"", "\"false\"", "\"off\"", "no", 0, "no", False, "false", "off"]):
                                r = False
                            param['enable'].append({
                                'operand': restriction[0],
                                'operator': restriction[1],
                                'value': r,
                                'condition': restriction[3]
                            })
                    params.append(param)
        return params

    def getToolParameters(self, toolname, **kwargs):
        """
        Get tool parameters as Params objects.

        Args:
            toolname (str): Name of the tool.
            **kwargs: Additional arguments (timeout).

        Returns:
            dict: Dictionary of Params objects, keyed by parameter ID.
        """
        timeout = kwargs.get("timeout", 30)
        inputs = self.getToolInputs(toolname, timeout=timeout)
        params = {}
        for k, v in inputs.items():
            params[k] = ParamsFactory.builder(v)
        return params

    def submitTool(self, parameters, **kwargs):
        """
        Submit a tool for execution.

        Args:
            parameters (dict): Dictionary of parameter values.
            **kwargs: Additional arguments (toolname, wait_results, wait_time, wait_limit, verbose, timeout).

        Returns:
            dict: Dictionary containing job_id and results (if waited).
        """
        timeout = kwargs.get("timeout", 30)

        if not isinstance(parameters, dict):
            raise ValueError("parameters object is no valid")

        for k, p in parameters.items():
            if not isinstance(p, Params):
                raise ValueError(
                    str(k) + " is no a valid Parameter object, " + str(p))

        toolname = kwargs.get("toolname", None)
        wait_results = kwargs.get("wait_results", False)
        wait_time = float(kwargs.get("wait_time", 2.0))
        wait_limit = int(time()) + kwargs.get("wait_limit", 300)
        verbose = kwargs.get("verbose", False)
        results = None
        if toolname is None:
            toolname = self.cached_toolname
        xml = ET.fromstring(self.getRapptureSchema(toolname, timeout=timeout))
        driver_str = self.generateDriver(xml, parameters)
        driver_json = {'app': toolname, 'xml': driver_str}
        job_id = self.getSession(driver_json, timeout=timeout)
        if (wait_results):
            while (results is None):
                if(verbose):
                    print(time(), "-", wait_limit)
                if (time() > wait_limit):
                    raise TimeoutError("limit of " + str(wait_limit) +
                                       "sec have been reached, use methods checkStatus("+job_id+") / getResults("+job_id+")")
                sleep(wait_time)
                try:
                    results = self.getResults(
                        job_id, verbose=verbose, timeout=timeout)
                except AttributeError as e:
                    pass
                except Exception as e:
                    raise e
        return {'job_id': job_id, 'results': results}

    def generateDriver(self, schema, parameters):
        """
        Generate the driver XML for tool submission.

        Args:
            schema (xml.etree.ElementTree.Element): The tool schema.
            parameters (dict): The parameter values.

        Returns:
            str: The driver XML string.
        """
        xml = schema
        for elem in xml.iter():
            if elem.tag == "structure":
                edefault = elem.find("default")
                if edefault is not None:
                    params = edefault.find("parameters")
                    if params is not None:
                        current = ET.Element("current")
                        current.insert(0, copy.copy(params))
                        elem.insert(0, current)

        for id, parameter in parameters.items():
            for elem in xml.iter():
                if 'id' in elem.attrib:
                    if elem.tag not in Tools.discardtags:
                        if (elem.attrib['id'] == id):
                            current = ET.Element("current")
                            current.text = str(parameter.value)
                            elem.insert(0, current)

        for elem in xml.iter():
            if 'id' in elem.attrib:
                if elem.tag not in Tools.discardtags:
                    if elem.find("current") is None:
                        units = ""
                        if elem.find("units") is not None:
                            units = elem.find("units").text
                        if elem.find("default") is not None:
                            current = ET.Element("current")
                            if units != "" and units not in elem.find("default").text:
                                current.text = elem.find(
                                    "default").text + units
                            else:
                                current.text = elem.find("default").text
                            elem.insert(0, current)

        driver_str = '<?xml version="1.0"?>\n' + ET.tostring(xml).decode()
        return driver_str


##############################

class Sim2L(Session):
    """
    Class for interacting with Sim2L tools (Jupyter-based).
    """

    def __init__(self, credentials, **kwargs):
        self.cached_schema = None
        self.cached_toolname = None
        self.endpoint = kwargs.get("endpoint", "results", )

        Session.__init__(self, credentials, **kwargs)

    def list(self, filters=[]):
        """
        List available Sim2L tools.

        Args:
            filters (list): List of tool aliases to filter by.

        Returns:
            list: List of tool dictionaries.
        """
        request = self.requestGet(self.endpoint + '/simtools/get', data={})
        tools_request = request.json()
        tools = []
        if 'tool' in tools_request:
            for tool, data in tools_request['tool'].items():
                if len(filters) == 0 or tool in filters:
                    tools.append(data)
        return tools

    def info(self, toolname, version="current"):
        """
        Get information about a Sim2L tool.

        Args:
            toolname (str): Name of the tool.
            version (str): Tool version. Defaults to "current".

        Returns:
            dict: Tool information.
        """
        url_path = toolname
        if (version != "current"):
            url_path += "/" + version
        request = self.requestGet(self.endpoint + '/simtools/get/'+url_path, data={})
        tools_request = request.json()
        if 'tool' in tools_request:
            return tools_request["tool"]
        elif 'tools' in tools_request:
            return tools_request["tools"][0]
        else:
            raise Exception("Schema not found")

    def getSchema(self, toolname, force=False, **kwargs):
        """
        Get the schema for a Sim2L tool.

        Args:
            toolname (str): Name of the tool.
            force (bool): Force refresh of cached schema.
            **kwargs: Additional arguments (timeout).

        Returns:
            dict: Tool schema.
        """
        timeout = kwargs.get("timeout", 30)
        self.validateSession()
        if (self.authenticated is False):
            raise ConnectionError('not connected')
        if (self.cached_schema is not None and self.cached_toolname == toolname and force is False):
            return self.cached_schema
        else:
            json_info = self.info(toolname)
            if "inputs" in json_info:
                self.cached_schema = json_info
                self.cached_toolname = toolname
            else:
                raise Exception("Schema not found")
        return self.cached_schema

    def getToolInputs(self, toolname, **kwargs):
        """
        Get tool input parameters from the schema.

        Args:
            toolname (str): Name of the tool.
            **kwargs: Additional arguments (timeout).

        Returns:
            dict: Dictionary of input parameters.
        """
        timeout = kwargs.get("timeout", 30)
        schema = self.getSchema(toolname, timeout=timeout)
        params = {}
        for id, value in schema["inputs"].items():
            param = dict(value)
            if "options" in param:
                param["type"] = "choice"
                if param["value"] not in param["options"]:
                    param["value"] = param["options"][0]
            else:
                param["type"] = param["type"].lower()
                if param["type"] == "text":
                    param["type"] = "string"
            param["id"] = id
            if "value" in param:
                param["default"] = param["value"]
                param["current"] = param["default"]
                del param["value"]
            params[id] = param
        return params

    def getToolLayout(self, toolname, **kwargs):
        """
        Get the layout of the tool's user interface.

        Args:
            toolname (str): Name of the tool.
            **kwargs: Additional arguments.

        Returns:
            dict: Empty dictionary (Sim2L tools handle layout differently).
        """
        params = {}
        return params

    def getToolLayoutParams(self, group, **kwargs):
        """
        Recursively parse layout parameters.

        Args:
            group: Group element.
            **kwargs: Additional arguments.

        Returns:
            list: Empty list.
        """
        params = []
        return params

    def getToolParameters(self, toolname, **kwargs):
        """
        Get tool parameters as Params objects.

        Args:
            toolname (str): Name of the tool.
            **kwargs: Additional arguments (timeout).

        Returns:
            dict: Dictionary of Params objects.
        """
        timeout = kwargs.get("timeout", 30)
        inputs = self.getToolInputs(toolname, timeout=timeout)
        params = {}
        for k, v in inputs.items():
            v["disable_fix"] = True
            params[k] = ParamsFactory.builder(v)
        return params

    def generateDriver(self, schema, parameters):
        """
        Generate the driver dictionary for tool submission.

        Args:
            schema (dict): The tool schema.
            parameters (dict): The parameter values.

        Returns:
            dict: The driver dictionary.
        """
        inputs = schema["inputs"]
        driver = {}
        for k, v in inputs.items():
            if k in parameters:
                if isinstance(parameters[k], Boolean):
                    driver[k] = (parameters[k].current == "yes")
                else:
                    driver[k] = parameters[k].current
            else:
                driver[k] = v["default"]
        return driver

    def submitTool(self, parameters, **kwargs):
        """
        Submit a tool for execution.

        Args:
            parameters (dict): Dictionary of parameter values.
            **kwargs: Additional arguments (toolname, wait_results, wait_time, wait_limit, verbose, timeout, cores, cutoff, venue).

        Returns:
            dict: Dictionary containing job_id and results (if waited).
        """
        timeout = kwargs.get("timeout", 30)

        if not isinstance(parameters, dict):
            raise ValueError("parameters object is no valid")

        for k, p in parameters.items():
            if not isinstance(p, Params):
                raise ValueError(
                    str(k) + " is no a valid Parameter object, " + str(p))

        toolname = kwargs.get("toolname", None)
        wait_results = kwargs.get("wait_results", False)
        wait_time = float(kwargs.get("wait_time", 2.0))
        wait_limit = int(time()) + kwargs.get("wait_limit", 300)
        verbose = kwargs.get("verbose", False)
        results = None
        if toolname is None:
            toolname = self.cached_toolname
        schema = self.getSchema(toolname, timeout=timeout)
        driver_json = {
            'name': schema['name'],
            'revision': schema['revision'],
            'inputs': self.generateDriver(schema, parameters),
            'outputs': list(schema['outputs'].keys()),
            'cores': kwargs.get('cores', 1),
            'cutoff': kwargs.get('cutoff', 15),
            'venue': kwargs.get('venue', "")
        }
        job_id = self.getSession(driver_json, timeout=timeout)

        if (wait_results):
            while (results is None):
                if(verbose):
                    print(time(), "-", wait_limit)
                if (time() > wait_limit):
                    raise TimeoutError("limit of " + str(wait_limit) +
                                       "sec have been reached, use methods checkStatus("+job_id+") / getResults("+job_id+")")
                sleep(wait_time)
                try:
                    results = self.getResults(
                        job_id, verbose=verbose, timeout=timeout)
                except AttributeError as e:
                    pass
                except Exception as e:
                    raise e
        return {'job_id': job_id, 'results': results}

    def getSession(self, driver_json, **kwargs):
        """
        Start a tool session.

        Args:
            driver_json (dict): Driver configuration for the tool.
            **kwargs: Additional arguments (timeout).

        Returns:
            str: The session ID.

        Raises:
            ConnectionError: If launch fails.
        """
        timeout = kwargs.get("timeout", 30)
        self.validateSession()
        if (self.authenticated is False):
            raise ConnectionError('not connected')
        request = self.requestPost(
            self.endpoint + '/simtools/run',
            data=json.dumps(driver_json),
            timeout=timeout
        )
        run_json = request.json()
        if 'id' in run_json:
            return run_json['id']
        else:
            msg = 'launch_tool failed ({0}): {1}\n'.format(
                run_json['code'], run_json['message'])
            raise ConnectionError(msg)

    def checkStatus(self, session_id, **kwargs):
        """
        Check the status of a session.

        Args:
            session_id (str): The session ID.
            **kwargs: Additional arguments (timeout, verbose).

        Returns:
            dict: Status dictionary.
        """
        timeout = kwargs.get("timeout", 30)
        self.validateSession()
        if (self.authenticated is False):
            raise ConnectionError('not connected')
        status_json = self.requestPost(
            self.endpoint + '/simtools/run/' + str(session_id), data={}, timeout=timeout)
        verbose = kwargs.get("verbose", False)
        if verbose:
            print(status_json.text)
        return status_json.json()

    def getResults(self, session_id, **kwargs):
        """
        Get results for a specific session.

        Args:
            session_id (str): The session ID.
            **kwargs: Additional arguments (timeout, verbose).

        Returns:
            list: List of Output objects.

        Raises:
            ConnectionError: If not connected.
        """
        timeout = kwargs.get("timeout", 60)
        self.validateSession()
        if (self.authenticated is False):
            raise ConnectionError('not connected')
        verbose = kwargs.get("verbose", False)
        status = self.checkStatus(session_id, verbose=verbose, timeout=timeout)
        if verbose:
            print(status)
        if 'status' in status:
            if 'outputs' in status:
                schema = self.getSchema(self.cached_toolname, timeout=timeout)
                if status['status'] in ["INDEXED", "CACHEDRESULTS"] or len(status['outputs']) > 0:
                    if schema is None:
                        return [Output(id=k, type=type(o), value=o, label=k) for k, o in status['outputs'].items()]
                    else:
                        outs = []
                        for k, o in status['outputs'].items():
                            out = Output(id=k, type=type(o), value=o, label=k)
                            if k in schema['outputs']:
                                out.type = schema['outputs'][k]["type"]
                                out.description = schema['outputs'][k]["description"]
                            outs.append(out)
                        return outs
        else:
            msg = 'tool failed ({0}): {1}\n'.format(
                status['code'], status['message'])
            raise ConnectionError(msg)
        raise AttributeError('results are not available')

Sim2l = Sim2L
