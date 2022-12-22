#!/usr/bin/python3
''' create archive '''
import os
from datetime import datetime
from fabric.api import local, runs_once


@runs_once
def do_pack():
    ''' creates archive'''
    os.path.isdir("versions") or os.mkdir("versions")
    now = datetime.now()
    filename = f"versions/web_static_{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}.tgz"
    try:
        print(f"Packing web_static to {filename}")
        local(f"tar -fczv {filename} web_static")
        size = os.path.getsize(filename)
        print(f"web_static packed: {filename} -> {size} Bytes")
    except Exception:
        return None
    return filename
