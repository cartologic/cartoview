from django.test import TestCase

from cartoview import get_current_version
from cartoview.version import get_version, json_version_info


class CartoviewVersionModule(TestCase):
    def test_json_version_info(self):
        version_text = json_version_info()
        self.assertTrue(isinstance(version_text, str))
        cond1 = "current_version" in version_text
        cond2 = "backward_versions" in version_text
        self.assertTrue(cond1 and cond2)

    def test_get_version(self):
        stable = (1, 8, 5, 'final', 0)
        unstable = (1, 8, 5, 'unstable', 0)
        rc = (1, 8, 5, 'rc', 0)
        beta = (1, 8, 5, 'beta', 0)
        version = get_version(stable)
        self.assertEqual(version, '1.8.5')
        version = get_version(rc)
        self.assertEqual(version, '1.8.5rc0')
        version = get_version(beta)
        self.assertEqual(version, '1.8.5b0')
        version = get_version(unstable)
        self.assertTrue("dev" in version)
        _version = get_current_version()
        self.assertNotEqual(_version, '')
