#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import env, local, run
from datetime import datetime
from os.path import isfile, join

env.hosts = ["104.196.168.90", "35.196.46.172"]  # Web server IP addresses
env.user = "ubuntu"  # SSH username


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    try:
        # Delete out-of-date archives in local versions folder
        local("ls -ltr versions | awk '{print $9}' | head -n -{} | xargs -I{{}} rm versions/{{}}"
              .format(number + 1))

        # Delete out-of-date archives in remote /data/web_static/releases folder
        releases_path = "/data/web_static/releases/"
        run("ls -ltr {} | awk '{{print $9}}' | head -n -{} | xargs -I{{}} rm -rf {}{{}}"
            .format(releases_path, number + 1, releases_path))
        return True
    except:
        return False
