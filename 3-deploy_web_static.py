#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
"""

from fabric.api import local, env
from os.path import isfile
from datetime import datetime

env.hosts = ["104.196.168.90", "35.196.46.172"]  # Web server IP addresses
env.user = "ubuntu"  # SSH username


def do_pack():
    """
    Creates a compressed archive of web_static folder
    """
    try:
        now = datetime.now()
        archive_name = "web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))
        local("mkdir -p versions")
        local("tar -cvzf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to a web server
    """
    if not isfile(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]
        if put(archive_path, "/tmp/{}".format(file_name)).failed:
            return False
        run("mkdir -p /data/web_static/releases/{}/".format(name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(file_name, name))
        run("rm /tmp/{}".format(file_name))
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(name, name))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ "
            "/data/web_static/current".format(name))
        return True
    except:
        return False


def deploy():
    """
    Calls do_pack() and do_deploy() functions
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
