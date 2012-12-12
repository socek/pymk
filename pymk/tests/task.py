import unittest
import tempfile
import os
import sys
import shutil

from pymk.script import append_python_path, import_mkfile, run_tasks
import pymk.error as Perror

class ArgsMockup(object):
    def __init__(self):
        self.all = False
        self.task = []

class PymkTestCase(unittest.TestCase):
    def setUp(self):
        self._normal_path = os.getcwd()
        self._actual_path = tempfile.mkdtemp()
        sys.path.append(self._actual_path)
        os.chdir(self._actual_path)
        self._args = ArgsMockup()

    def tearDown(self):
        sys.path.remove(self._actual_path)
        os.chdir(self._normal_path)
        shutil.rmtree(self._actual_path)
        self._actual_path = None

    def _template(self, name, out_path = None, vars = {}):
        template_path = os.path.join(self._normal_path, 'pymk', 'tests', 'tmpl', name + '.tpl')
        template = open(template_path).read()
        out_data = template %vars
        if not out_path:
            out_path = name
        out_file = open(out_path, 'w')
        out_file.write(out_data)
        out_file.close()

    def _pymk(self):
        return run_tasks(self._args)

class TaskTest(PymkTestCase):

    def test_no_mkfile(self):
        self.assertRaises(Perror.NoMkfileFound, import_mkfile)

    def test_empty_mkfile(self):
        self._template('empty', 'mkfile.py')
        import_mkfile()
        self.assertEqual(self._pymk(), 'list all')

    def test_bad_task_name(self):
        self._template('empty', 'mkfile.py')
        import_mkfile()
        self._args.task.append('bad_task_name')

        self.assertRaises(Perror.BadTaskName, self._pymk)
