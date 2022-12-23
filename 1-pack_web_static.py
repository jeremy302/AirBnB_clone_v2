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
    return None
