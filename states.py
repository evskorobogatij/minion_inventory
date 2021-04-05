import subprocess
import json
import sys

def states_list():
    saltcall = "salt-call.bat" if sys.platform == "win32" else "salt-call"
    codec = "cp1251" if sys.platform == "win32" else "UTF-8"
    proc = subprocess.run(args=[saltcall,"state.show_states","--out=json"], stdout=subprocess.PIPE)
    tmp_str = proc.stdout.decode(codec)
    tmp = json.loads(tmp_str)
    states = tmp['local']
    return states