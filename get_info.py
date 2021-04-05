
import os
import subprocess
import json
import datetime
import requests
import sys

from info import minion_info
from soft import soft_list
from disk import disk_info
from states import states_list
from monitor import monitors_list
from printer import printer_list

SALT_MONITOR_POINT = os.environ.get('SALT_MONITOR_POINT')

if(not SALT_MONITOR_POINT):
    print('Необходимо задать переменную SALT_MONITOR_POINT')
    sys.exit()


uuid, data = minion_info().values()
print("UUID = ",uuid)

# print('DATA === ',data)

data['pkg_info'] = soft_list()
data['disk_info'] = disk_info()
data['states'] = states_list()
data['monitors'] = monitors_list()
data['printers'] = printer_list()

uri = "%s/api/minion/%s" % (SALT_MONITOR_POINT, uuid)

print(uri)
print('STATES===',data['states'] )
response = requests.post( uri , data=json.dumps(data))

#print(response.json())

print(response.status_code)

