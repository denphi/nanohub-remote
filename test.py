from mysecrets import auth_data
import nanohub.remote as nr
import nanohub.remote.params as p
#a = nr.Session(auth_data)
a = nr.Tools(auth_data)
params = a.getToolParameters('pntoy')
#for k,p in params.items():
#  print(p)
print(params['p_len'])
params['p_len'].current = "33um"
job_id = a.submitTool(params)
#print()
(a.checkStatus(job_id))
(a.getResults(job_id))

