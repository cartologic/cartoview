import os
import shutil
import tempfile

from django.test import TestCase

from cartoview.app_manager.req_installer import (ReqFileException,
                                                 ReqInstaller)


class ReqInstallerTest(TestCase):
    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False)
        self.tmp_dir = tempfile.mkdtemp()

    def test_req_installer(self):
        with open(self.tmp_file.name, "w") as f:
            f.write("pipenv")
        req_installer = ReqInstaller(self.tmp_file.name, self.tmp_dir)
        req_installer.install_all()
        self.assertTrue(len(os.listdir(self.tmp_dir)) > 0)
        self.assertRaises(ReqFileException, ReqInstaller, "/dummy_path")

    def tearDown(self):
        os.remove(self.tmp_file.name)
        shutil.rmtree(self.tmp_dir)
