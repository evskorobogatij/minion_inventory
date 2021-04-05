
import subprocess
from sys import platform

def soft_list():
    soft = []

    if platform == "linux" :
        proc = subprocess.run(args=["rpm","-qa", "--queryformat=%{NAME}==%{SIZE}==%{VERSION}==%{INSTALLTIME}\n"], stdout=subprocess.PIPE)
        tmp_str = proc.stdout.decode('UTF-8')
        tmp_pkg_list = tmp_str.splitlines()
        
        for tmp_pkg in tmp_pkg_list:
            name, size, version, installed_at = tmp_pkg.split("==")
            pkg_info = dict(
                name  = name,
                size = size,
                version = version,
                installed_at = installed_at
            )
            soft.append(pkg_info)

    return soft


