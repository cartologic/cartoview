import os
import shutil
import tempfile

from django.test import TestCase

from cartoview.apps_handler.req_installer import ReqFileException, ReqInstaller


class ReqInstallerTest(TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.req_file = os.path.join(self.tmp_dir, 'req.txt')
        self.target_dir = os.path.join(self.tmp_dir, 'libs')

    def test_req_installer(self):
        with open(self.req_file, "w") as f:
            f.write("pipenv")
        req_installer = ReqInstaller(self.tmp_dir, self.target_dir)
        req_installer.install_all()
        self.assertTrue(len(os.listdir(self.target_dir)) > 0)
        self.assertRaises(ReqFileException, ReqInstaller, "/dummy_path")

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
