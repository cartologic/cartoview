# -*- coding: utf-8 -*-
import os
from os import R_OK, access

try:
    from pip import main
except:
    from pip._internal import main


class ReqInstaller(object):
    def __init__(self, reqfile):
        self.file = reqfile
        self.requirements = []
        self.preprocess_reqfile()

    def _install_req(self, package, *args, **kwargs):
        main_args = ['install', package]
        main_args.extend(self._get_flags(*args, **kwargs))
        main(main_args)

    def _get_flags(self, *args, **kwargs):
        flags = []
        for k, v in kwargs.iteritems():
            if k == "no_cache" and v:
                flags.append("--no-cache-dir")
        return flags

    def preprocess_reqfile(self):
        if not os.path.exists(self.file):
            raise Exception("requirement file doesn't exists!")
        if not access(self.file, R_OK):
            raise Exception("can not read requirement file!")
        with open(self.file, 'r') as reqfile:
            lines = reqfile.readlines()
            self.requirements = [x.strip(" ") for x in lines]

    def install_all(self, *args, **kwargs):
        for package in self.requirements:
            self._install_req(package, *args, **kwargs)
