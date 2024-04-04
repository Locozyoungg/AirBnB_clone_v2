#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['192.168.1.100', '192.168.1.101']  # Replace with your web server IPs
env.user = '172.17.0.18 '
env.key_filename = '/home/ssh/'


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not exists(archive_path):
        return False

    filename = archive_path.split('/')[-1]
    folder_name = '/data/web_static/releases/' + filename.split('.')[0]

    try:
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(folder_name))
        run('tar -xzf /tmp/{} -C {}'.format(filename, folder_name))
        run('rm /tmp/{}'.format(filename))
        run('mv {}/web_static/* {}'.format(folder_name, folder_name))
        run('rm -rf {}/web_static'.format(folder_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(folder_name))
        return True
    except Exception as e:
        return False
