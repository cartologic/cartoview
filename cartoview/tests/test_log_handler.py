from django.test import TestCase
from cartoview.log_handler import get_logger
from logging import Logger, DEBUG


class CartoviewHomeViewTest(TestCase):

    def test_get_logger(self):
        logger = get_logger(__name__)
        self.assertEqual(isinstance(logger, Logger), True)
        self.assertEqual(logger.name, __name__)
        self.assertEqual(logger.level, DEBUG)
