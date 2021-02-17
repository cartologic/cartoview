# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import re

from future import standard_library

standard_library.install_aliases()
req_file_regex = re.compile(r'^(req|requirement)s?\.txt')


class ReqFileException(Exception):
    message = "requirement file doesn't exists!"


class ReqFilePermissionException(Exception):
    message = "can not read requirement file!"


class ReqInstaller(object):
    def __init__(self, app_dir, target=None):
        self._app_dir = app_dir
        self.req_file = None
        self.target = target
        self.find_req_file()

    def find_req_file(self):
        if not os.path.exists(self._app_dir):
            raise ReqFileException()
        for root, dirs, files in os.walk(self._app_dir):
            for name in files:
                if req_file_regex.match(name):
                    self.req_file = os.path.join(root, name)
                    break
            else:
                continue
            break
        if not self.req_file or not os.path.exists(self.req_file):
            raise ReqFileException()
        if not os.access(self.req_file, os.R_OK):
            raise ReqFilePermissionException()

    def install_all(self, *args, **kwargs):
        from subprocess import call
        command = ["pip", "install", "-r", self.req_file]
        if self.target:
            command.extend(["-t", self.target])
        call(command)
