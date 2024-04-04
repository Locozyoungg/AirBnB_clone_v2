#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive
from the contents of the web_static folder of
your AirBnB Clone repo
"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Creates a .tgz archive from web_static folder
    """

    # Create the folder versions if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Create the name of the archive
    now = datetime.now()
    archive_name = "web_static_" + now.strftime("%Y%m%d%H%M%S") + ".tgz"

    # Compress web_static into the archive
    result = local("tar -cvzf versions/{} web_static".format(archive_name))

    # Check if the archiving was successful
    if result.failed:
        return None
    else:
        return "versions/{}".format(archive_name)
