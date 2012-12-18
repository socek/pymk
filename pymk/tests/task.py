import os
from time import sleep
from pymk import extra
from pymk.script import import_mkfile
from pymk.tests.base import PymkTestCase
import pymk.error as Perror

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

    def test_no_dependency(self):
        self._template('one_task', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_1')

        self._pymk_runtask(['task_1'])
        self._pymk_runtask(['task_1', 'task_1'])
        self._pymk_runtask(['task_1', 'task_1', 'task_1'])

    def test_no_dependency_with_outputfile(self):
        self._template('one_task_with_outputfile', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_5')

        self._pymk_runtask(['task_5'])
        self._pymk_runtask(['task_5'])
        self.touch('a.out')
        self._pymk_runtask(['task_5'])

class TaskForcing(PymkTestCase):

    def test_forcing_file_changed(self):
        self._template('three_task_with_force', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_17a')

        self._pymk_runtask(['task_17c', 'task_17b', 'task_17a'])
        self._pymk_runtask(['task_17c', 'task_17b', 'task_17a'])

        self._args.force = True
        self._pymk_runtask(['task_17c', 'task_17b', 'task_17a', 'task_17a'])
        self._pymk_runtask(['task_17c', 'task_17b', 'task_17a', 'task_17a', 'task_17a'])

    def test_dependency_forcing_file_changed(self):
        self._template('three_task_with_force', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_17a')

        self._args.dependency_force = True
        self._pymk_runtask(['task_17c', 'task_17b', 'task_17a'])
        self._pymk_runtask(['task_17c', 'task_17b', 'task_17a'])

        self._args.force = True
        self._pymk_runtask(['task_17c', 'task_17b', 'task_17a', 'task_17c', 'task_17b', 'task_17a'])
        self._pymk_runtask(['task_17c', 'task_17b', 'task_17a', 'task_17c', 'task_17b', 'task_17a', 'task_17c', 'task_17b', 'task_17a'])

    def test_forcing_file_exist(self):
        self._template('three_task_with_force_2', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_18a')

        self._pymk_runtask(['task_18c', 'task_18b', 'task_18a'])
        self._pymk_runtask(['task_18c', 'task_18b', 'task_18a'])

        self._args.force = True
        self._pymk_runtask(['task_18c', 'task_18b', 'task_18a', 'task_18a'])
        self._pymk_runtask(['task_18c', 'task_18b', 'task_18a', 'task_18a', 'task_18a'])

    def test_dependency_forcing_file_exist(self):
        self._template('three_task_with_force_2', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_18a')

        self._args.dependency_force = True
        self._pymk_runtask(['task_18c', 'task_18b', 'task_18a'])
        self._pymk_runtask(['task_18c', 'task_18b', 'task_18a'])

        self._args.force = True
        self._pymk_runtask(['task_18c', 'task_18b', 'task_18a', 'task_18c', 'task_18b', 'task_18a'])
        self._pymk_runtask(['task_18c', 'task_18b', 'task_18a', 'task_18c', 'task_18b', 'task_18a', 'task_18c', 'task_18b', 'task_18a'])

class TaskDependencyFileExistsTest(PymkTestCase):
    def test_make_no_outputfile(self):
        self._template('three_task_dependency_exists2', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_9a')

        self._pymk_runtask(['task_9c', 'task_9b', 'task_9a'])
        self._pymk_runtask(['task_9c', 'task_9b', 'task_9a'])
        self.touch('b.out')
        self._pymk_runtask(['task_9c', 'task_9b', 'task_9a'])

    def test_make_no_outputfile_fail1(self):
        self._template('three_task_dependency_exists3', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_10a')

        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file([])

        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file([])

        self.touch('b.out')
        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file([])

    def test_make_no_outputfile_fail2(self):
        self._template('three_task_dependency_exists4', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_11a')

        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file([])

        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file([])

        self.touch('b.out')
        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file([])

    def test_make(self):
        self._template('two_task_dependency_exists1', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_6a')

        self._pymk_runtask(['task_6b', 'task_6a'])
        self._pymk_runtask(['task_6b', 'task_6a'])
        self.touch('b.out')
        self._pymk_runtask(['task_6b', 'task_6a'])

    def test_make_2(self):
        self._template('three_task_dependency_exists1', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_7a')

        self._pymk_runtask(['task_7c', 'task_7b', 'task_7a'])
        self._pymk_runtask(['task_7c', 'task_7b', 'task_7a'])
        self.touch('b.out')
        self._pymk_runtask(['task_7c', 'task_7b', 'task_7a'])

        self.touch('c.out')
        self._pymk_runtask(['task_7c', 'task_7b', 'task_7a', 'task_7b'])

        self._remove_task('task_7a')
        self._add_task('task_7b')
        self._pymk_runtask(['task_7c', 'task_7b', 'task_7a', 'task_7b'])

        self._remove_task('task_7b')
        self._add_task('task_7a')
        self._pymk_runtask(['task_7c', 'task_7b', 'task_7a', 'task_7b'])

    def test_uptodate(self):
        self._template('two_task_dependency_exists1', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_6a')
        self.touch('b.out', None)

        self._pymk_runtask(['task_6a'])
        self._pymk_runtask(['task_6a'])
        self._pymk_runtask(['task_6a'])

class TaskDependencyFileChangedTest(PymkTestCase):
    def test_make_once(self):
        self._template('two_task_dependency_changed1', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_8a')

        self._pymk_runtask(['task_8b', 'task_8a'])
        self._pymk_runtask(['task_8b', 'task_8a'])
        self._pymk_runtask(['task_8b', 'task_8a'])

    def test_make_twice(self):
        self._template('two_task_dependency_changed1', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_8a')

        self._pymk_runtask(['task_8b', 'task_8a'])
        self.touch('b.out')
        self._pymk_runtask(['task_8b', 'task_8a', 'task_8a'])
        self._pymk_runtask(['task_8b', 'task_8a', 'task_8a'])

    def test_make_when_depedency_lost(self):
        self._template('two_task_dependency_changed1', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_8a')

        self._pymk_runtask(['task_8b', 'task_8a'])
        os.unlink('b.out')
        self._pymk_runtask(['task_8b', 'task_8a', 'task_8b', 'task_8a'])
        self._pymk_runtask(['task_8b', 'task_8a', 'task_8b', 'task_8a'])

    def test_make_three_tasks(self):
        self._template('three_task_dependency_changed1', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_12a')

        self._pymk_runtask(['task_12c', 'task_12b', 'task_12a'])
        self._pymk_runtask(['task_12c', 'task_12b', 'task_12a'])

        self.touch('b.out')
        self._pymk_runtask(['task_12c', 'task_12b', 'task_12a', 'task_12a'])
        self._pymk_runtask(['task_12c', 'task_12b', 'task_12a', 'task_12a'])

        self.touch('c.out')
        self._pymk_runtask(['task_12c', 'task_12b', 'task_12a', 'task_12a', 'task_12b', 'task_12a'])
        self._pymk_runtask(['task_12c', 'task_12b', 'task_12a', 'task_12a', 'task_12b', 'task_12a'])

        os.unlink('b.out')
        self._pymk_runtask(['task_12c', 'task_12b', 'task_12a', 'task_12a', 'task_12b', 'task_12a', 'task_12b', 'task_12a'])
        self._pymk_runtask(['task_12c', 'task_12b', 'task_12a', 'task_12a', 'task_12b', 'task_12a', 'task_12b', 'task_12a'])

    def test_make_three_tasks_fail1(self):
        self._template('three_task_dependency_changed2', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_13a')

        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file(['task_13c', 'task_13b'])

        self.touch('b.out')
        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file(['task_13c', 'task_13b'])

        self.touch('c.out')
        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file(['task_13c', 'task_13b', 'task_13b'])

        os.unlink('b.out')
        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file(['task_13c', 'task_13b', 'task_13b', 'task_13b'])

    def test_make_three_tasks_fail2(self):
        self._template('three_task_dependency_changed3', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_14a')

        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file(['task_14c'])

        self.touch('b.out')
        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file(['task_14c'])

        self.touch('c.out')
        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file(['task_14c'])

        os.unlink('b.out')
        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file(['task_14c'])

    def test_make_three_tasks_fail3(self):
        self._template('three_task_dependency_changed4', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_15a')

        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file(['task_15c'])

        self.touch('b.out')
        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file(['task_15c', 'task_15c'])

        self.touch('c.out')
        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file(['task_15c', 'task_15c', 'task_15c'])

        os.unlink('b.out')
        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file(['task_15c', 'task_15c', 'task_15c', 'task_15c'])

    def test_uptodate(self):
        self._template('two_task_dependency_changed1', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_8a')
        self.touch('b.out', None)

        self._pymk_runtask(['task_8a'])
        self._pymk_runtask(['task_8a'])
        self._pymk_runtask(['task_8a'])
