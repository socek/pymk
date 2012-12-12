import unittest
import os
import sys
import shutil
import tempfile
import logging

from pymk.script import import_mkfile, run_tasks, TaskData

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
        logging.getLogger('pymk').info('=== (%s) %s ===' %(self.__class__.__name__, self._testMethodName))

    def tearDown(self):
        sys.path.remove(self._actual_path)
        os.chdir(self._normal_path)
        shutil.rmtree(self._actual_path)
        self._actual_path = None
        if 'mkfile' in sys.modules:
            del sys.modules['mkfile']
            del self._mkfile
        self._mkfile = None

    def _template(self, name, out_path = None, vars = {}):
        template_path = os.path.join(self._normal_path, 'pymk', 'tests', 'tmpl', name + '.tpl')
        template = open(template_path).read()
        out_data = template %vars
        if not out_path:
            out_path = name
        out_file = open(out_path, 'w')
        out_file.write(out_data)
        out_file.close()

    def _import_mkfile(self):
        TaskData.init()
        self._mkfile = import_mkfile()

    def _pymk(self):
        return run_tasks(self._mkfile, self._args)

    def _pymk_runtask(self):
        self.assertEqual(self._pymk(), 'run tasks')

    def _check_output_file(self, test_data):
        try:
            data = open('a.out').read().strip().split('\n')
        except IOError:
            data = []
        self.assertEqual(data, test_data)

    def _add_task(self, task):
        self._args.task.append(task)
