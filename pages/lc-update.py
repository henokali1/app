import pickle
import requests
import ast
import json
import time
min_mc = 1000000000

x = requests.get('https://api2.lunarcrush.com/v2/assets?data=market&type=fast&key=85dyw1kasu88y5cscmge2r')
d={}
data=json.loads(x.text)['data']
for i in data:
	mc=i['mc']
	if mc>min_mc:
		d[i['s']]=i['gs']

srtd = sorted(d.items(), key=lambda x: x[1])
s=[]

for i in range(-1,-6,-1):
	s.append(srtd[i])


ts = str(int(time.time()))
nv={ts: s}
print(nv)	


with open('/home/ubuntu/app/pages/lc-log.pickle', 'rb') as handle:
    old_val = pickle.load(handle)
old_val.append(nv)
with open('/home/ubuntu/app/pages/lc-log.pickle', 'wb') as handle:
    pickle.dump(old_val, handle, protocol=pickle.HIGHEST_PROTOCOL)
