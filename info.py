
import os
import subprocess
import json
import datetime
import requests
import sys


def minion_info():

    saltcall = "salt-call.bat" if sys.platform == "win32" else "salt-call"
    codec = "cp1251" if sys.platform == "win32" else "UTF-8"

    proc = subprocess.run(args=[saltcall,"grains.items","--out=json"], stdout=subprocess.PIPE)

    tmp_str = proc.stdout.decode(codec)

    tmp = json.loads(tmp_str)

    info = tmp['local']

    uuid = ''
    if sys.platform != "win32" :
        uuid = info['uuid']
    else:
        proc_uuid = subprocess.run(args=["wmic","csproduct","get","uuid"], stdout=subprocess.PIPE)
        tmp_uuid = proc_uuid.stdout.decode(codec)
        s = tmp_uuid.splitlines()[2]
        uuid = s.lower().strip()
        

    data = dict(
        node_name = info['nodename'],
        serialnumber = info['serialnumber'],
        biosversion = info['biosversion'],
        # biosreleasedate = datetime.datetime.strptime(info['biosreleasedate'],"%m/%d/%Y").strftime('%Y-%m-%d'),
        room = info['room'],
        manufacturer = info['manufacturer'],
        cpu_model = info['cpu_model'],
        productname = info['productname'],
        fio_user = info.get('fio_user',''),
        user_phone = info.get('user_phone',''),
        type = info['type'],
        type_dep = info['type_dep'],
        department = info['department'],
        saltversion = info['saltversion'],
        mem_total = info['mem_total'],
        os = info['os'],
        osfullname = info['osfullname'],
        osrelease = info['osrelease']
    )

    biosreleasedate = ''
    if sys.platform == "win32" :
        proc_bd = subprocess.run(args=["wmic","bios","get","releasedate"], stdout=subprocess.PIPE)
        tmp_str = proc_bd.stdout.decode(codec)
        date_str = tmp_str.splitlines()[2][0:8]
        biosreleasedate = datetime.datetime.strptime(date_str,"%Y%m%d").strftime('%Y-%m-%d')
    else:
        biosreleasedate = datetime.datetime.strptime(info['biosreleasedate'],"%m/%d/%Y").strftime('%Y-%m-%d')

    data['biosreleasedate'] = biosreleasedate
    

    hwaddr_interfaces = info['hwaddr_interfaces']
    hwaddr_interfaces.pop('lo',None)
    hwaddr_interfaces.pop('Software Looopback Interface 1',None)
    # print('interfaces === ',hwaddr_interfaces)

    ip_interfaces = info['ip_interfaces']
    ip_interfaces.pop('lo',None)
    ip_interfaces.pop('Software Looopback Interface 1',None)
    # print('ip === ',ip_interfaces)

    networks = {}
    for interface in hwaddr_interfaces.keys():
        networks[interface]={
            'mac' : hwaddr_interfaces[interface],
            'ips' : ip_interfaces[interface]
        }
        # print(interface)
    # print('networks === ', networks)
    data['network'] = networks

    return dict(
        uuid = uuid,
        data = data
    )