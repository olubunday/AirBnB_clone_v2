#!/usr/bin/python3
"""Module to make tarball from a local directory"""


import datetime
import fabric.api
import os
import os.path


def do_pack():
    """Bundle and compress the local static web files"""

    if not os.path.isdir('versions'):
        os.mkdir('versions')
    target = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    target = 'versions/web_static_' + target + '.tgz'
    fabric.api.local('tar -cvzf ' + target + ' web_static')
    return target
