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

    def test_no_condition(self):
        self._template('one_task', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_1')

        self._pymk_runtask(['task_1'])
        self._pymk_runtask(['task_1', 'task_1'])
        self._pymk_runtask(['task_1', 'task_1', 'task_1'])

    def test_no_condition_with_outputfile(self):
        self._template('one_task_with_outputfile', 'mkfile.py')
        self._import_mkfile()
        self._add_task('task_5')

        self._pymk_runtask(['task_5'])
        self._pymk_runtask(['task_5'])
        extra.touch('a.out')
        self._pymk_runtask(['task_5'])
