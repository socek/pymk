import os
from time import sleep, time
import pymk.error as Perror
from pymk import extra
from pymk.tests.base import PymkTestCase

class TouchTest(PymkTestCase):
    test_file = 'testme.file'

    def test_new_file(self):
        actual_time = int(time())
        extra.touch(self.test_file)
        file_time = int(os.path.getmtime(self.test_file))
        self.assertTrue(os.path.exists(self.test_file))
        self.assertEqual(actual_time, file_time)

    def test_change_time(self):
        extra.touch(self.test_file)
        first_file_time = os.path.getmtime(self.test_file)

        sleep(0.01)
        extra.touch(self.test_file)
        second_file_time = os.path.getmtime(self.test_file)

        self.assertNotEqual(first_file_time, second_file_time)
