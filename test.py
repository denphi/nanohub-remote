from mysecrets import auth_data
import nanohub.remote as nr
import nanohub.remote.params as p
#a = nr.Session(auth_data)
a = nr.Tools(auth_data)
params = a.getToolParameters('pntoy')
#for k,p in params.items():
#  print(p)
print(params['p_len'])
params['p_len'].current = "6um"
job_id = a.submitTool(params, wait_results=True, wait_time=2.0, wait_limit=60)
print(job_id)
job_id = {'job_id':'1558396', 'results':None}


