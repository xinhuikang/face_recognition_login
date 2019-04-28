from datetime import date
import unittest

from employees.utils import calculate_age


class UtilsTests(unittest.TestCase):

    def test_calculate_age(self):
        self.assertIs(calculate_age(date.today(), date(2017, 12, 10)), 0)
        self.assertIs(calculate_age(date.today(), date(2017, 2, 10)), 1)
import webm
webm.FFMPEG_PATH