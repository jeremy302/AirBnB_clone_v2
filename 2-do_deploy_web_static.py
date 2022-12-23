#!/usr/bin/python3
''' <TODO> doc for code '''
import os
from datetime import datetime
from fabric.api import local, runs_once, put, run, env

env.hosts = ["52.3.240.48", "54.157.141.179"]

@runs_once
def do_pack():
    ''' <TODO> doc for code '''
    os.path.isdir("versions") or os.mkdir("versions")
    now = datetime.now()
    filename = ("versions/web_static_{}{}{}{}{}{}.tgz".
                format(now.year, now.month, now.day, now.hour,
                       now.minute, now.second))
    try:
        print('Packing web_static to {}'.format(filename))
        local("tar -cvzf {} web_static".format(filename))
        size = os.path.getsize(filename)
        print('web_static packed: {} -> {} Bytes'.format(filename, size))
    except Exception:
        return None
    return filename


def do_deploy(archive_path):
    ''' <TODO> doc for code '''
    if not os.path.exists(archive_path):
        return False
    basename = os.path.basename(archive_path)
    target_dir = '/data/web_static/releases/{}/'.format(
        basename.split('.tgz')[0])

    try:
        put(archive_path, "/tmp/{}".format(basename))
        run("mkdir -p {}".format(target_dir))
        run("tar -xzf /tmp/{} -C {}".format(basename, target_dir))
        run("rm -rf /tmp/{}".format(basename))
        run("mv {}web_static/* {}".format(target_dir, basename))
        run("rm -rf {}web_static".format(target_dir))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(target_dir))
        print('New version deployed!')
        return True
    except Exception:
        pass
    return True
