import os

from pymk.tests.base import PymkTestCase
from pymk.extra import touch, find_files


class FindFilesTest(PymkTestCase):

    def setUp(self):
        super(FindFilesTest, self).setUp()

        os.mkdir('first')
        os.mkdir('second')
        os.mkdir('third')

        touch('file2.test')
        touch('file1.test')
        touch('file3.notest')

        for filename in ['file3.test', 'file4.test', 'file5.notest']:
            path = os.path.join('first', filename)
            touch(path)

        for filename in ['file6.test', 'file7.test', 'file8.notest']:
            path = os.path.join('second', filename)
            touch(path)

        for filename in ['file9.test', 'file10.test', 'file11.notest']:
            path = os.path.join('third', filename)
            touch(path)

    def test_nothing_found(self):
        self.assertEqual([], list(find_files('.', '*.py')))

    def test_found_all_tests(self):
        should_found = [
            './file1.test',
            './file2.test',
            './third/file10.test',
            './third/file9.test',
            './second/file7.test',
            './second/file6.test',
            './first/file4.test',
            './first/file3.test'
        ]
        self.assertEqual(should_found, list(find_files('.', '*.test')))
