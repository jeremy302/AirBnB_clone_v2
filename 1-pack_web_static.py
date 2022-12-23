#!/usr/bin/python3
''' <TODO> doc for code '''
import os
from datetime import datetime
from fabric.api import local, runs_once


@runs_once
def do_pack():
    ''' <TODO> doc for code '''
    os.path.isdir("versions") or os.mkdir("versions")
    now = datetime.now()
    filename = ("versions/web_static_{}{}{}{}{}{}.tgz".
                format(now.year, now.month, now.day, now.hour,
                       now.minute, now.second))
    try:
        print("Packing web_static to {}".format(filename))
        local("tar -fczv {} web_static".format(filename))
        size = os.path.getsize(filename)
        print("web_static packed: {} -> {} Bytes".format(filename, size))
    except Exception:
        return None
    return filename
