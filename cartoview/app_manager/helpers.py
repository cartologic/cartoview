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
            logger.error(e)
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


def get_perm(fname):
    return stat.S_IMODE(os.lstat(fname)[stat.ST_MODE])


def make_writeable_recursive(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in [os.path.join(root, d) for d in dirs]:
            os.chmod(dir, get_perm(dir) | stat.S_IRUSR |  # noqa
                     stat.S_IRGRP | stat.S_IROTH)
        for file in [os.path.join(root, f) for f in files]:
            os.chmod(file, get_perm(file) | stat.S_IRUSR |  # noqa
                     stat.S_IRGRP | stat.S_IROTH)
