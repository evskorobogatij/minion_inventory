import os
import subprocess
import json
import datetime
import re
from sys import platform


def monitors_list():

    monitors_info = []

    if platform == "linux":
        proc = subprocess.run(args=["/usr/sbin/hwinfo","--monitor"], stdout=subprocess.PIPE)
        tmp_str = proc.stdout.decode('UTF-8')
        monitors = re.split(r'\d{2}\:\s\w+\s\d{2}\.\d',tmp_str)
        monitors.pop(0)
        for monitor in monitors:
            model_reg = re.findall(r'Model\:\s\"(.+)\"\n',monitor)
            if model_reg : 
                model = model_reg[0]
            vendor_reg = re.findall(r'Vendor\:\s(.+)\n',monitor)
            if vendor_reg :
                vendor = vendor_reg[0]
            serial_reg = re.findall(r'Serial\sID\:\s\"(.+)\"\n',monitor)
            if serial_reg :
                serial = serial_reg[0]
            year = re.findall(r'Year\sof\sManufacture\:\s(\d{4})',monitor)[0]
            week = re.findall(r'Week\sof\sManufacture\:\s(\d{2})',monitor)[0]
            monitors_info.append(dict(
                vendor = vendor,
                model = model,
                serial = serial,
                year = year,
                week = week
            ))

    return monitors_info