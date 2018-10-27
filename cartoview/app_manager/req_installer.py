# -*- coding: utf-8 -*-
import os
from os import R_OK, access


class ReqFileException(Exception):
    message = "requirement file doesn't exists!"


class ReqFilePermissionException(Exception):
    message = "can not read requirement file!"


class ReqInstaller(object):
    def __init__(self, reqfile, target=None):
        if not os.path.exists(reqfile):
            raise ReqFileException()
        if not access(reqfile, R_OK):
            raise ReqFilePermissionException()
        self.file = reqfile
        self.requirements = []
        self.target = target

    def install_all(self, *args, **kwargs):
        from subprocess import call
        command = ["pip", "install", "-r", self.file]
        if self.target:
            command.extend(["-t", self.target])
        call(command)
