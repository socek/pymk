from time import sleep
import pymk.error as Perror
from pymk import extra
from pymk.tests.base import PymkTestCase

class FileDoesNotExistsDependencyTest(PymkTestCase):
    def test_make(self):
        self._template('one_task_dependency_1', 'mkfile.py')
        self._import_mkfile()

        self._args.task.append('task_2')
        self._pymk_runtask(['task_2'])
        self._pymk_runtask(['task_2', 'task_2'])
        self._pymk_runtask(['task_2', 'task_2', 'task_2'])

    def test_uptodate(self):
        self._template('one_task_dependency_1', 'mkfile.py')
        self._template('one_task_dependency_1', 'test.txt')
        self._import_mkfile()

        self._add_task('task_2')
        self._pymk_runtask([])
        self._pymk_runtask([])

class FileChangedDependencyTest(PymkTestCase):

    def test_FileChanged_dependency_make_fail(self):
        self._template('one_task_dependency_2', 'mkfile.py')
        self._import_mkfile()

        self._add_task('task_3')

        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file([])

    def test_FileChanged_dependency_make_fail_2(self):
        self._template('one_task_dependency_2', 'mkfile.py')
        self.touch('test.txt', None)
        self._import_mkfile()

        self._add_task('task_3')

        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file([])

    def test_FileChanged_dependency_make_faile_3(self):
        self._template('one_task_dependency_3', 'mkfile.py')
        self._import_mkfile()

        self._add_task('task_4')

        self.assertRaises(Perror.CouldNotCreateFile, self._pymk)
        self._check_output_file([])

    def test_FileChanged_dependency_make_once(self):
        self._template('one_task_dependency_3', 'mkfile.py')
        self._import_mkfile()

        self._add_task('task_4')

        self.touch('test.txt', None)
        self._pymk_runtask(['task_4'])
        self._pymk_runtask(['task_4'])

    def test_FileChanged_dependency_make_twice(self):
        self._template('one_task_dependency_3', 'mkfile.py')
        self._import_mkfile()

        self._add_task('task_4')

        self.touch('test.txt', None)
        self._pymk_runtask(['task_4'])

        self.touch('test.txt')
        self._pymk_runtask(['task_4', 'task_4'])

        sleep(0.001)
        self._pymk_runtask(['task_4', 'task_4'])

class AlwaysRebuildDependencyTest(PymkTestCase):
    def test_success(self):
        self._template('three_task_dependency_always1', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_16a')

        self._pymk_runtask(['task_16c', 'task_16b', 'task_16a'])
        self._pymk_runtask(['task_16c', 'task_16b', 'task_16a', 'task_16a'])
        self._pymk_runtask(['task_16c', 'task_16b', 'task_16a', 'task_16a', 'task_16a'])

    def test_dependency_rebuild(self):
        self._template('three_task_dependency_always1', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_16a')

        self._pymk_runtask(['task_16c', 'task_16b', 'task_16a'])
        self.touch('c.out')
        self._pymk_runtask(['task_16c', 'task_16b', 'task_16a', 'task_16b', 'task_16a'])
        self._pymk_runtask(['task_16c', 'task_16b', 'task_16a', 'task_16b', 'task_16a', 'task_16a'])
