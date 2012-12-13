from time import sleep
import pymk.error as Perror
from pymk import extra
from pymk.script import import_mkfile
from pymk.tests.base import PymkTestCase

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
        self._pymk_runtask(['task_1'])
        self._pymk_runtask(['task_1', 'task_1'])
        self._pymk_runtask(['task_1', 'task_1', 'task_1'])


class FileDoesNotExistsConditionTest(PymkTestCase):
    def test_make(self):
        self._template('one_task_condition_1', 'mkfile.py')
        self._import_mkfile()

        self._args.task.append('task_2')
        self._pymk_runtask(['task_2'])
        self._pymk_runtask(['task_2', 'task_2'])
        self._pymk_runtask(['task_2', 'task_2', 'task_2'])

    def test_uptodate(self):
        self._template('one_task_condition_1', 'mkfile.py')
        self._template('one_task_condition_1', 'test.txt')
        self._import_mkfile()

        self._add_task('task_2')
        self._pymk_runtask([])
        self._pymk_runtask([])

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
        self._pymk_runtask(['task_4'])
        self._pymk_runtask(['task_4'])

    def test_FileChanged_condition_make_twice(self):
        self._template('one_task_condition_3', 'mkfile.py')
        self._import_mkfile()

        self._add_task('task_4')

        extra.touch('test.txt')
        self._pymk_runtask(['task_4'])

        sleep(0.01)
        extra.touch('test.txt')
        self._pymk_runtask(['task_4', 'task_4'])

        sleep(0.01)
        self._pymk_runtask(['task_4', 'task_4'])
