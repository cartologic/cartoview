# -*- coding: utf-8 -*-
import os
from os import R_OK, access


class ReqInstallerException(Exception):
    pass


class ReqInstaller(object):
    def __init__(self, reqfile, target=None):
        if not os.path.exists(reqfile):
            raise ReqInstallerException("requirement file doesn't exists!")
        if not access(reqfile, R_OK):
            raise ReqInstallerException("can not read requirement file!")
        self.file = reqfile
        self.requirements = []
        self.target = target

    def install_all(self, *args, **kwargs):
        from subprocess import call
        command = ["pip", "install", "-r", self.file]
        if self.target:
            command.extend(["-t", self.target])
        call(command)
