from time import sleep

import StringIO
from mock import patch, MagicMock

import pymk.error as Perror
from pymk.dependency import FileChanged, FileDoesNotExists, AlwaysRebuild, InnerFileExists, InnerFileChanged, Dependency, FileDependency
from pymk.task import Task
from pymk.tests.base import PymkTestCase
from pymk.dependency import InnerLink


class FileDoesNotExistsDependencyTest(PymkTestCase):

    def test_make(self):
        self._template('one_task_dependency_1', 'mkfile.py')
        self._import_mkfile()

        self._args.task.append('/task_2')
        self._pymk_runtask(['task_2'])
        self._pymk_runtask(['task_2', 'task_2'])
        self._pymk_runtask(['task_2', 'task_2', 'task_2'])

    def test_uptodate(self):
        self._template('one_task_dependency_1', 'mkfile.py')
        self._template('one_task_dependency_1', 'test.txt')
        self._import_mkfile()

        self._add_task('/task_2')
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

        self._add_task('/' + taskname)

        self._pymk_runtask([taskname])
        self._pymk_runtask([taskname, taskname])

        self.touch(file1, None)
        self._pymk_runtask([taskname, taskname, taskname])

        self.touch(file2, None)
        self._pymk_runtask([taskname, taskname, taskname])

    def test_extra(self):
        depedency = Dependency()
        self.assertEqual('', depedency.extra())

    def test_get_graph_details(self):
        depedency = Dependency()
        self.assertEqual('', depedency.get_graph_details())

    def test_get_shape_color(self):
        depedency = Dependency()
        depedency.runned = False
        self.assertEqual('white', depedency._get_shape_color())

    def test_get_shape_color_after_run(self):
        depedency = Dependency()
        depedency.runned = True
        self.assertEqual('darkgreen', depedency._get_shape_color())


class FileDependencyTest(PymkTestCase):

    filename = 'something.txt'

    def setUp(self):
        super(FileDependencyTest, self).setUp()
        self.dep = FileDependency(self.filename)

    def test_init(self):
        self.assertEqual([self.filename, ], self.dep.filenames)

    def test_name(self):
        self.assertEqual('something.txt', self.dep.name)

    def test_name_many_files(self):
        self.dep = FileDependency([self.filename, 'filename2.txt'])
        self.assertEqual('Many files', self.dep.name)

    @patch('pymk.dependency.os.path.getmtime')
    def test_compare_mtime(self, getmtime):
        getmtime.return_value = 1
        self.assertFalse(self.dep.compare_mtime('1', '2'))
        self.assertEqual(2, getmtime.call_count)
        getmtime.assert_called_with('2')
        self.assertEqual(('1',), getmtime.mock_calls[0][1])
        self.assertEqual(('2',), getmtime.mock_calls[1][1])

    @patch('pymk.dependency.os.path.getmtime')
    def test_compare_mtime_true(self, getmtime):
        def side_effect_1(*args, **kwargs):
            return 1

        def side_effect_2(*args, **kwargs):
            getmtime.side_effect = side_effect_1
            return 2
        getmtime.side_effect = side_effect_2

        self.assertTrue(self.dep.compare_mtime('1', '2'))
        self.assertEqual(2, getmtime.call_count)
        getmtime.assert_called_with('2')
        self.assertEqual(('1',), getmtime.mock_calls[0][1])
        self.assertEqual(('2',), getmtime.mock_calls[1][1])


class FileChangedDependencyTest(PymkTestCase):

    def test_check_dependent_file_no_file(self):
        dep = FileChanged('something', MagicMock())
        with patch.object(dep, 'compare_mtime') as compare_mtime:
            with patch.object(dep, 'make_dependent_file') as make_dependent_file:
                compare_mtime.side_effect = OSError()

                dep.check_dependent_file(MagicMock())
                make_dependent_file.assert_called_once_with()

    def test_check_dependent_file(self):
        dep = FileChanged('something', MagicMock())
        with patch.object(dep, 'compare_mtime') as compare_mtime:
            result = dep.check_dependent_file(MagicMock())
            compare_mtime.called_once_with('something')
            self.assertEqual(compare_mtime.return_value.__ror__(), result)

    def test_FileChanged_dependency_make_fail(self):
        self._template('one_task_dependency_2', 'mkfile.py')
        self._import_mkfile()

        self._add_task('/task_3')

        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file([])

    def test_FileChanged_dependency_make_fail_2(self):
        self._template('one_task_dependency_2', 'mkfile.py')
        self.touch('test.txt', None)
        self._import_mkfile()

        self._add_task('/task_3')

        self.assertRaises(Perror.TaskMustHaveOutputFile, self._pymk)
        self._check_output_file([])

    def test_FileChanged_dependency_make_faile_3(self):
        self._template('one_task_dependency_3', 'mkfile.py')
        self._import_mkfile()

        self._add_task('/task_4')

        self.assertRaises(Perror.CouldNotCreateFile, self._pymk)
        self._check_output_file([])

    def test_FileChanged_dependency_make_once(self):
        self._template('one_task_dependency_3', 'mkfile.py')
        self._import_mkfile()

        self._add_task('/task_4')

        self.touch('test.txt', None)
        self._pymk_runtask(['task_4'])
        self._pymk_runtask(['task_4'])

    def test_FileChanged_dependency_make_twice(self):
        self._template('one_task_dependency_3', 'mkfile.py')
        self._import_mkfile()

        self._add_task('/task_4')

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

        self._add_task('/task_21')

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

    def test_make_dependent_file(self):
        task = MagicMock()
        depedency = FileChanged('name', task)

        self.assertTrue(depedency.make_dependent_file())
        task.run.called_once_with(False)

    def test_CouldNotCreateFile(self):
        depedency = FileChanged('name')
        self.assertRaises(
            Perror.CouldNotCreateFile, depedency.make_dependent_file)


class AlwaysRebuildDependencyTest(PymkTestCase):

    def test_success(self):
        self._template('three_task_dependency_always1', 'mkfile.py')
        self._import_mkfile()
        self._add_task('/task_16a')

        self._pymk_runtask(['task_16c', 'task_16b', 'task_16a'])
        self._pymk_runtask(['task_16c', 'task_16b', 'task_16a', 'task_16a'])
        self._pymk_runtask(
            ['task_16c', 'task_16b', 'task_16a', 'task_16a', 'task_16a'])

    def test_dependency_rebuild(self):
        self._template('three_task_dependency_always1', 'mkfile.py')
        self._import_mkfile()
        self._add_task('/task_16a')

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


class InnerLinkTest(PymkTestCase):

    def setUp(self):
        super(InnerLinkTest, self).setUp()
        self.parent = MagicMock()
        self.dep = InnerLink(self.parent)

    def test_do_test(self):
        self.assertFalse(self.dep.do_test('1'))
        self.parent.run.assert_called_once_with(False, parent='1')

    def test_extra(self):
        self.assertEqual('[label="L"]', self.dep.extra())
