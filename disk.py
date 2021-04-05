import subprocess
import json
import sys

def disk_info():
    saltcall = "salt-call.bat" if sys.platform == "win32" else "salt-call"
    codec = "cp1251" if sys.platform == "win32" else "UTF-8"
    proc = subprocess.run(args=[saltcall,"disk.usage","--out=json"], stdout=subprocess.PIPE)
    tmp_str = proc.stdout.decode(codec)
    tmp = json.loads(tmp_str)
    disk_info = tmp['local']

    return disk_info