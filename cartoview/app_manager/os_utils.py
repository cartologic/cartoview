# -*- coding: utf-8 -*-
import os
import stat

from cartoview.log_handler import get_logger

world_permission = 0o777
logger = get_logger(__name__)


def create_direcotry(path, mode=0o777):
    # please read the following section
    # https://docs.python.org/2/library/os.html#mkdir-modebits
    if not os.path.exists(path):
        try:
            previous_mask = os.umask(0)
            os.makedirs(path, mode=mode)
        except OSError as e:
            logger.error(e.message)
        finally:
            # set the previous mask back
            os.umask(previous_mask)


def change_path_permission(path, mode=world_permission):
    os.chmod(path, mode)


def octal_permissions(protection_bits):
    # this return octal permission
    return oct(stat.S_IMODE(protection_bits))


def get_path_permission(path):
    ''' on platforms that do not support symbolic links,
    lstat is an alias for stat()
    so we return a tuple of both
    '''
    lst = os.lstat(path)
    st = os.stat(path)
    permission = octal_permissions(lst.st_mode), octal_permissions(st.st_mode)
    return permission


def create_apps_dir(apps_dir=None):
    if not apps_dir or not os.path.isdir(apps_dir):
        from django.conf import settings
        apps_dir = getattr(settings, 'APPS_DIR', None)
    if not os.path.exists(apps_dir):
        create_direcotry(apps_dir)
        if not os.access(apps_dir, os.W_OK):
            change_path_permission(apps_dir)
