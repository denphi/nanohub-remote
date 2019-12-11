#  Copyright 2019 HUBzero Foundation, LLC.

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


import sys, json, time
import requests
import json, os       
import time 
import xml.etree.ElementTree as ET
import copy
from .params import ParamsFactory

class Session():
  credentials = {}
  headers = {}
  authenticated = False
  
  def __init__(self, credentials, **kwargs):
    self.credentials = credentials
    self.url = kwargs.get("url", "https://nanohub.org/api")
    self.clearSession()
    self.validateSession()
    
  def clearSession(self):
    self.authenticated = False
    self.headers = {}
    self.access_token = ""
    self.refresh_token = ""
    self.expires_in = 0
    
  def getUrl(self, entry_point):
    return self.url + "/" + entry_point
    

  def validateTokenRequest( self, request, timestamp):
    auth_json = request.json()
    if 'errors' in auth_json:
      raise ConnectionError(json.dumps(auth_json['errors']))   
    if 'access_token' in auth_json:
      self.access_token = auth_json['access_token']
    else :
      raise AttributeError('access_token')
    if 'expires_in' in auth_json:
      self.expires_in = timestamp + int(auth_json['expires_in']) - 1
    else :
      raise AttributeError('expires_in')
    if 'refresh_token' in auth_json:
      self.refresh_token = auth_json['refresh_token']
    self.headers = {'Authorization': 'Bearer '+self.access_token}
    self.authenticated = True  
    
  def validateSession(self):
    timestamp = int(time.time())
    if self.authenticated == True:
      if self.expires_in > timestamp : 
        if (self.refresh_token != ""):
          try : 
            refresh_token = {
              'client_id' : self.credentials['client_id'],
              'client_secret' : self.credentials['client_secret'],
              'grant_type' : self.credentials['refresh_token'],
              'refresh_token' : self.refresh_token,
            }
            request = requests.post(self.getUrl('developer/oauth/token'), data=refresh_token, headers={})
            self.validateTokenRequest(request, timestamp)
          except:
            self.clearSession();
        else:
          self.clearSession();        
    if self.authenticated == False:
      try :
        request = requests.post(self.getUrl('developer/oauth/token'), data=self.credentials, headers={})
        self.validateTokenRequest(request, timestamp)
      except AttributeError:
        self.clearSession()
        raise ConnectionError("Authentication Token not found")
      except ConnectionError as ce:
        self.clearSession()        
        raise ce
      except:
        self.clearSession()
        raise ConnectionError("invalid Authentication")


class Tools(Session):
  periodicelement = [
    ('Hydrogen','H'),
    ('Helium','He'),
    ('Lithium','Li'),
    ('Beryllium','Be'),
    ('Boron','B'),
    ('Carbon','C'),
    ('Nitrogen','N'),
    ('Oxygen','O'),
    ('Fluorine','F'),
    ('Neon','Ne'),
    ('Sodium','Na'),
    ('Magnesium','Mg'),
    ('Aluminium','Al'),
    ('Silicon','Si'),
    ('Phosphorus','P'),
    ('Sulfur','S'),
    ('Chlorine','Cl'),
    ('Argon','Ar'),
    ('Potassium','K'),
    ('Calcium','Ca'),
    ('Scandium','Sc'),
    ('Titanium','Ti'),
    ('Vanadium','V'),
    ('Chromium','Cr'),
    ('Manganese','Mn'),
    ('Iron','Fe'),
    ('Cobalt','Co'),
    ('Nickel','Ni'),
    ('Copper','Cu'),
    ('Zinc','Zn'),
    ('Gallium','Ga'),
    ('Germanium','Ge'),
    ('Arsenic','As'),
    ('Selenium','Se'),
    ('Bromine','Br'),
    ('Krypton','Kr'),
    ('Rubidium','Rb'),
    ('Strontium','Sr'),
    ('Yttrium','Y'),
    ('Zirconium','Zr'),
    ('Niobium','Nb'),
    ('Molybdenum','Mo'),
    ('Technetium','Tc'),
    ('Ruthenium','Ru'),
    ('Rhodium','Rh'),
    ('Palladium','Pd'),
    ('Silver','Ag'),
    ('Cadmium','Cd'),
    ('Indium','In'),
    ('Tin','Sn'),
    ('Antimony','Sb'),
    ('Tellurium','Te'),
    ('Iodine','I'),
    ('Xenon','Xe'),
    ('Caesium','Cs'),
    ('Barium','Ba'),
    ('Lanthanum','La'),
    ('Cerium','Ce'),
    ('Praseodymium','Pr'),
    ('Neodymium','Nd'),
    ('Promethium','Pm'),
    ('Samarium','Sm'),
    ('Europium','Eu'),
    ('Gadolinium','Gd'),
    ('Terbium','Tb'),
    ('Dysprosium','Dy'),
    ('Holmium','Ho'),
    ('Erbium','Er'),
    ('Thulium','Tm'),
    ('Ytterbium','Yb'),
    ('Lutetium','Lu'),
    ('Hafnium','Hf'),
    ('Tantalum','Ta'),
    ('Tungsten','W'),
    ('Rhenium','Re'),
    ('Osmium','Os'),
    ('Iridium','Ir'),
    ('Platinum','Pt'),
    ('Gold','Au'),
    ('Mercury','Hg'),
    ('Thallium','Tl'),
    ('Lead','Pb'),
    ('Bismuth','Bi'),
    ('Polonium','Po'),
    ('Astatine','At'),
    ('Radon','Rn'),
    ('Francium','Fr'),
    ('Radium','Ra'),
    ('Actinium','Ac'),
    ('Thorium','Th'),
    ('Protactinium','Pa'),
    ('Uranium','U'),
    ('Neptunium','Np'),
    ('Plutonium','Pu'),
    ('Americium','Am'),
    ('Curium','Cm'),
    ('Berkelium','Bk'),
    ('Californium','Cf'),
    ('Einsteinium','Es'),
    ('Fermium','Fm'),
    ('Mendelevium','Md'),
    ('Nobelium','No'),
    ('Lawrencium','Lr'),
    ('Rutherfordium','Rf'),
    ('Dubnium','Db'),
    ('Seaborgium','Sg'),
    ('Bohrium','Bh'),
    ('Hassium','Hs'),
    ('Meitnerium','Mt')        
  ]
  discardtags = ["phase", "group", "option", "image", "note", "field"]  
  
  def __init__(self, credentials, **kwargs):
    self.cached_schema = None
    self.cached_toolname = None
    Session.__init__(self, credentials, **kwargs);
    
  def list(self, filters=[]):
    request = requests.get(self.getUrl('tools/list'), data={}, headers=self.headers)
    tools_request = request.json()
    tools = []
    if 'tools' in tools_request:
      for tool in tools_request['tools']:
        if len(filters)==0 or tool['alias'] in filters:
          tools.append(tool)
    return tools
      
  def info(self, toolname, version="current"):
    raise ConnectionError('Method is deprecated')
    request = requests.post(self.getUrl('tools/info?tool='+toolname), data={}, headers=self.headers)
    info_request = request.json()
    return info_request
  
  def getResults(self, session_id):
    self.validateSession() 
    if (self.authenticated == False):
      raise ConnectionError('not connected')
    status = self.checkStatus(session_id)
    if 'success' in status and status['success']:
      if 'status' in status:
        if 'finished' in status:
          if status['finished'] and status['run_file'] != "":
            results_json = {
              'session_num': session_id,
              'run_file': status['run_file']
            }
            return self.loadResults(results_json)
    raise AttributeError('results are not available')


  def loadResults(self, results_json):
    self.validateSession() 
    request = requests.post(self.getUrl('tools/output'), data=results_json, headers=self.headers)
    result_json = request.json()
    if 'output' in result_json:
        return result_json['output'];
    else:
        return '';
                        
  def checkStatus(self, session_id):
    self.validateSession() 
    if (self.authenticated == False):
      raise ConnectionError('not connected')
    status_json = requests.post(self.getUrl('tools/status'), data={'session_num': str(session_id)}, headers=self.headers)
    return status_json.json()

  def getSession(self, driver_json):
    self.validateSession() 
    if (self.authenticated == False):
      raise ConnectionError('not connected')
    request = requests.post(self.getUrl('/tools/run'), data=driver_json, headers=self.headers)
    run_json = request.json()
    if 'session' in run_json:
      return run_json['session']
    else:
      msg = 'launch_tool failed ({0}): {1}\n'.format(run_json['code'], run_json['message'])
      raise ConnectionError(msg)

  def getRapptureSchema(self, toolname, force=True):
    self.validateSession()
    if (self.authenticated == False):
      raise ConnectionError('not connected')
    if (self.cached_schema is not None and self.cached_toolname == toolname and force == False):
      return self.cached_schema
    else:
      request = requests.post(self.getUrl('tools/' + toolname + '/rappturexml'), data={}, headers=self.headers)
      rappturexml = request.text
      self.cached_schema = rappturexml
      self.cached_toolname = toolname
    return rappturexml;

  def getToolInputs(self, toolname):
    xml = ET.fromstring(self.getRapptureSchema(toolname))
    inputs = xml.find('input')
    params = {}
    for elem in inputs.iter():
      id = ''
      if 'id' in elem.attrib:
          id = elem.attrib['id']
      if elem.tag not in Tools.discardtags and id != "":
        if id not in params:
          about = elem.find("about")
          description = ""
          labelt = ""
          if (about is not None):
            description = about.find('description')
            if description is not None:
              description = description.text        
            label = about.find("label")
            if (label is not None):
              labelt = label.text 

          param = {"type": elem.tag, "description" : description}
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

          if param['type'] == "periodicelement" :
            param['type'] = 'choice'
            param['options'] = Tools.periodicelement
          if len(param['options']) > 0:
            if param['default'] not in [p[1] for p in param['options']]:
              param['default'] = param['options'][0][1]
          if param['type'] == "string":
            if param['default'] is not None:
              if '\n' in param['default'].strip():
                param['type'] = "text"
          params [id] = param
    return params;
    
  def getToolParameters(self, toolname):
    inputs = self.getToolInputs(toolname)
    params = {}
    for k,v in inputs.items():
      params[k] = ParamsFactory.builder(v);
    return params

  def submitTool(self, parameters, toolname=None):
    if toolname is None:
      toolname = self.cached_toolname
    xml = ET.fromstring(self.getRapptureSchema(toolname))
    driver_str = self.generateDriver(xml, parameters)
    driver_json = {'app': toolname, 'xml': driver_str}
    session_id = self.getSession(driver_json)
    return session_id;


  def generateDriver(self, schema, parameters):
    xml = schema        
    for elem in xml.iter():
      if elem.tag == "structure":
        edefault = elem.find("default")
        if edefault is not None:
          params = edefault.find("parameters")
          if params is not None:                   
            current = ET.Element("current")
            current.insert(0, copy.copy(params))
            elem.insert(0,current)
    
    for id, parameter in parameters.items():
      for elem in xml.iter():
        if 'id' in elem.attrib:
          if elem.tag not in Tools.discardtags:
            if (elem.attrib['id'] == id):
              current = ET.Element("current")
              current.text = str(parameter.value)
              elem.insert(0,current)

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
                current.text = elem.find("default").text + units
              else:
                current.text = elem.find("default").text
              elem.insert(0,current)
          
    driver_str  = '<?xml version="1.0"?>\n' + ET.tostring(xml).decode()
    return driver_str;   
 
#class setInterval :
#    def __init__(self,interval,action) :
#        self.interval=interval
#        self.action=action
#        self.stopEvent=threading.Event()
#        thread=threading.Thread(target=self.__setInterval)
#        thread.start()
#
#    def __setInterval(self) :
#        nextTime=time.time()+self.interval
#        while not self.stopEvent.wait(nextTime-time.time()) :
#            nextTime+=self.interval
#            self.action()
#
#    def cancel(self) :
#        self.stopEvent.set()        

    