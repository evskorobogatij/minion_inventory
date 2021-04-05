import os
import subprocess
import json
import datetime
import re
from sys import platform


def printer_list():
    printers_info = []

    if platform=="linux":
        proc = subprocess.run(args=["/usr/sbin/hwinfo","--printer"], stdout=subprocess.PIPE)
        tmp_str = proc.stdout.decode('UTF-8')
        printers = re.split(r'\d{2}\:\s\w+\s\d{2}\.\d',tmp_str)
        printers.pop(0)        
        for printer in printers:
            model_reg = re.findall(r'Model\:\s\"(.+)\"\n',printer)
            if model_reg :
                model = model_reg[0]
            vendor_reg = re.findall(r'Vendor\:\s.*\"(.+)\"\n',printer)
            if vendor_reg :
                vendor = vendor_reg[0]
            serial_reg = re.findall(r'Serial\sID\:\s\"(.+)\"\n',printer)
            if serial_reg :
                serial = serial_reg[0]

            printers_info.append(dict(
                vendor = vendor,
                model = model,
                serial = serial
            ))

    return printers_info