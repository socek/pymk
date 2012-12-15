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

class FindFilesTest(PymkTestCase):

    def setUp(self):
        super(FindFilesTest, self).setUp()

        os.mkdir('first')
        os.mkdir('second')
        os.mkdir('third')

        extra.touch('file1.test')
        extra.touch('file2.test')
        extra.touch('file3.notest')

        for filename in ['file3.test', 'file4.test', 'file5.notest']:
            path = os.path.join('first', filename)
            extra.touch(path)

        for filename in ['file6.test', 'file7.test', 'file8.notest']:
            path = os.path.join('second', filename)
            extra.touch(path)

        for filename in ['file9.test', 'file10.test', 'file11.notest']:
            path = os.path.join('third', filename)
            extra.touch(path)

    def test_nothing_found(self):
        self.assertEqual([], list(extra.find_files('.', '*.py')))

    def test_found_all_tests(self):
        should_found = [
            './file2.test',
            './file1.test',
            './third/file10.test',
            './third/file9.test',
            './second/file7.test',
            './second/file6.test',
            './first/file4.test',
            './first/file3.test'
        ]
        self.assertEqual(should_found, list(extra.find_files('.', '*.test')))

class RunCmdTest(PymkTestCase):

    def test_success(self):
        ret = extra.run_cmd(['ls -al'])
        self.assertEqual(file, type(ret[0]))
        self.assertEqual(file, type(ret[1]))

    def test_show_output(self):
        ret = extra.run_cmd(['ls', '*.py'], show_output=True)
        self.assertEqual(None, ret[0])
        self.assertEqual(None, ret[1])

    def test_fail(self):
        self.assertRaises(Perror.CommandError, extra.run_cmd, ['ls *.py'])
