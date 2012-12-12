import unittest
import tempfile
import os
import sys
import shutil
import logging

from pymk.script import append_python_path, import_mkfile, run_tasks, TaskData
from pymk import extra
import pymk.error as Perror
from time import sleep

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

class TaskTest(PymkTestCase):

    def test_no_mkfile(self):
        self.assertRaises(Perror.NoMkfileFound, import_mkfile)

    def test_empty_mkfile(self):
        self._template('empty', 'mkfile.py')
        self._import_mkfile()
        self.assertEqual(self._pymk(), 'list all')

    def test_bad_task_name(self):
        self._template('empty', 'mkfile.py')
        self._import_mkfile()
        self._add_task('bad_task_name')

        self.assertRaises(Perror.BadTaskName, self._pymk)

    def test_default_task(self):
        self._template('one_task_with_default', 'mkfile.py')
        self._import_mkfile()
        self.assertEqual(self._pymk(), 'run default')

        self._check_output_file(['task_0'])

    def test_no_condition(self):
        self._template('one_task', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_1')
        self._pymk_runtask()
        self._pymk_runtask()
        self._pymk_runtask()

        self._check_output_file(['task_1', 'task_1', 'task_1'])

class FileDoesNotExistsConditionTest(PymkTestCase):
    def test_make(self):
        self._template('one_task_condition_1', 'mkfile.py')
        self._import_mkfile()

        self._args.task.append('task_2')
        self._pymk_runtask()
        self._check_output_file(['task_2'])

        self._pymk_runtask()
        self._check_output_file(['task_2', 'task_2'])

        self._pymk_runtask()
        self._check_output_file(['task_2', 'task_2', 'task_2'])

    def test_uptodate(self):
        self._template('one_task_condition_1', 'mkfile.py')
        self._template('one_task_condition_1', 'test.txt')
        self._import_mkfile()

        self._add_task('task_2')
        self._pymk_runtask()
        self._check_output_file([])
        self._pymk_runtask()
        self._check_output_file([])

class FileChangedConditionTest(PymkTestCase):

    def test_FileChanged_condition_make_fail(self):
        self._template('one_task_condition_2', 'mkfile.py')
        self._import_mkfile()

        self._add_task('task_3')

        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file([])

    def test_FileChanged_condition_make_fail_2(self):
        self._template('one_task_condition_2', 'mkfile.py')
        extra.touch('test.txt')
        self._import_mkfile()

        self._add_task('task_3')

        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file([])

    def test_FileChanged_condition_make_faile_3(self):
        self._template('one_task_condition_3', 'mkfile.py')
        self._import_mkfile()

        self._add_task('task_4')

        self.assertRaises(Perror.CouldNotCreateFile, self._pymk)
        self._check_output_file([])

    def test_FileChanged_condition_make_once(self):
        self._template('one_task_condition_3', 'mkfile.py')
        self._import_mkfile()

        self._add_task('task_4')

        extra.touch('test.txt')
        self._pymk_runtask()
        self._check_output_file(['task_4'])
        self._pymk_runtask()
        self._check_output_file(['task_4'])

    def test_FileChanged_condition_make_twice(self):
        self._template('one_task_condition_3', 'mkfile.py')
        self._import_mkfile()

        self._add_task('task_4')

        extra.touch('test.txt')
        self._pymk_runtask()
        self._check_output_file(['task_4'])

        sleep(0.01)
        extra.touch('test.txt')
        self._pymk_runtask()
        self._check_output_file(['task_4', 'task_4'])

        sleep(0.01)
        self._pymk_runtask()
        self._check_output_file(['task_4', 'task_4'])
