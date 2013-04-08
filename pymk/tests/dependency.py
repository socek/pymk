from time import sleep
import StringIO
import pymk.error as Perror
from pymk.dependency import FileChanged, FileDoesNotExists, AlwaysRebuild, InnerFileExists, InnerFileChanged
from pymk.tests.base import PymkTestCase
from pymk.task import Task


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

    def test_graph(self):
        dep = FileDoesNotExists('')

        self.assertEqual(str, type(dep.extra()))
        self.assertEqual(str, type(dep.get_graph_name()))
        self.assertEqual(str, type(dep.get_graph_details()))

        dep.runned = True

        self.assertEqual(str, type(dep.extra()))
        self.assertEqual(str, type(dep.get_graph_name()))
        self.assertEqual(str, type(dep.get_graph_details()))

        output = StringIO.StringIO()
        dep.write_graph_detailed(output)
        self.assertNotEqual(0, len(output.getvalue().strip()))

    def test_check_force(self):
        dep = FileDoesNotExists('filename')
        self.assertTrue(dep.do_test(None, True))

    def test_two_files(self):
        file1 = 'test.txt'
        file2 = 'test2.txt'
        taskname = 'task_22'
        self._template('one_task_dependency_5', 'mkfile.py')
        self._import_mkfile()

        self._add_task(taskname)

        self._pymk_runtask([taskname])
        self._pymk_runtask([taskname, taskname])

        self.touch(file1, None)
        self._pymk_runtask([taskname, taskname, taskname])

        self.touch(file2, None)
        self._pymk_runtask([taskname, taskname, taskname])


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

    def test_FileChanged_two_files(self):
        file1 = 'test.txt'
        file2 = 'test2.txt'
        self._template('one_task_dependency_4', 'mkfile.py')
        self._import_mkfile()

        self._add_task('task_21')

        self.touch(file1, None)
        self.touch(file2, None)

        self._pymk_runtask(['task_21'])
        self._pymk_runtask(['task_21'])

        self.touch(file1)
        self._pymk_runtask(['task_21', 'task_21'])

        self.touch(file2)
        self._pymk_runtask(['task_21', 'task_21', 'task_21'])
        self._pymk_runtask(['task_21', 'task_21', 'task_21'])

    def test_graph(self):
        dep = FileChanged('filename')

        self.assertEqual(str, type(dep.extra()))
        self.assertEqual(str, type(dep.get_graph_name()))
        self.assertEqual(str, type(dep.get_graph_details()))
        dep.runned = True

        self.assertEqual(str, type(dep.extra()))
        self.assertEqual(str, type(dep.get_graph_name()))
        self.assertEqual(str, type(dep.get_graph_details()))

        output = StringIO.StringIO()
        dep.write_graph_detailed(output)
        self.assertNotEqual(0, len(output.getvalue().strip()))

    def test_check_force(self):
        dep = FileChanged('filename')
        self.assertTrue(dep.do_test(None, True))

    def test_no_output_file(self):
        class TaskA(Task):
            output_file = 'something'
            dependencys = []

        class TaskB(Task):
            dependencys = []

        dep = FileChanged('filename', TaskB)
        self.assertRaises(Perror.TaskMustHaveOutputFile, dep.do_test, TaskA)

    def test_no_output_file2(self):
        class TaskBa(Task):
            output_file = 'something'
            dependencys = []

        class TaskBb(Task):
            dependencys = []
        dep = FileChanged('filename', TaskBa)
        self.assertRaises(Perror.TaskMustHaveOutputFile, dep.do_test, TaskBb)


class AlwaysRebuildDependencyTest(PymkTestCase):

    def test_success(self):
        self._template('three_task_dependency_always1', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_16a')

        self._pymk_runtask(['task_16c', 'task_16b', 'task_16a'])
        self._pymk_runtask(['task_16c', 'task_16b', 'task_16a', 'task_16a'])
        self._pymk_runtask(
            ['task_16c', 'task_16b', 'task_16a', 'task_16a', 'task_16a'])

    def test_dependency_rebuild(self):
        self._template('three_task_dependency_always1', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_16a')

        self._pymk_runtask(['task_16c', 'task_16b', 'task_16a'])
        self.touch('c.out')
        self._pymk_runtask(
            ['task_16c', 'task_16b', 'task_16a', 'task_16b', 'task_16a'])
        self._pymk_runtask(['task_16c', 'task_16b', 'task_16a',
                           'task_16b', 'task_16a', 'task_16a'])

    def test_graph(self):
        dep = AlwaysRebuild()

        self.assertEqual(str, type(dep.extra()))
        self.assertEqual(str, type(dep.get_graph_name()))
        self.assertEqual(str, type(dep.get_graph_details()))

        dep.runned = True

        self.assertEqual(str, type(dep.extra()))
        self.assertEqual(str, type(dep.get_graph_name()))
        self.assertEqual(str, type(dep.get_graph_details()))

        output = StringIO.StringIO()
        dep.write_graph_detailed(output)
        self.assertNotEqual(0, len(output.getvalue().strip()))


class InnerFileExistsTest(PymkTestCase):

    def test_graph(self):
        dep = InnerFileExists(Task)

        self.assertEqual(str, type(dep.extra()))
        self.assertEqual(str, type(dep.get_graph_name()))

        dep.runned = True

        self.assertEqual(str, type(dep.extra()))
        self.assertEqual(str, type(dep.get_graph_name()))


class InnerFileChangedTest(PymkTestCase):

    def test_graph(self):
        dep = InnerFileChanged(Task)

        self.assertEqual(str, type(dep.extra()))
        self.assertEqual(str, type(dep.get_graph_name()))

        dep.runned = True

        self.assertEqual(str, type(dep.extra()))
        self.assertEqual(str, type(dep.get_graph_name()))
