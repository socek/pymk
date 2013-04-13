from pymk.tests.base import PymkTestCase
from pymk.script import parse_task_name
from pymk.error import CommandError
from pymk.task import TaskMeta


class TaskNameParseTest(PymkTestCase):

    def test_parse_task_name(self):
        name, args = parse_task_name('/something/elo')
        self.assertEqual('/something/elo', name)
        self.assertEqual({}, args)

        name, args = parse_task_name('/something/elo?elo=10')
        self.assertEqual('/something/elo', name)
        self.assertEqual({'elo': ['10']}, args)

        name, args = parse_task_name('/something/elo/?elo=10&zbychu=12')
        self.assertEqual('/something/elo/', name)
        self.assertEqual({'elo': ['10'], 'zbychu': ['12']}, args)

        name, args = parse_task_name('/something/elo/?elo=10&zbychu=12,10&zbychu=ccc')
        self.assertEqual('/something/elo/', name)
        self.assertEqual({'elo': ['10'], 'zbychu': ['12,10', 'ccc']}, args)


class GraphTest(PymkTestCase):

    def test_error_in_task(self):
        taskname = '/taska'
        self._template('task_graph_error', 'mkfile.py')
        self._import_mkfile()
        self._add_task(taskname)

        self.assertRaises(CommandError, self._pymk_runtask, [])
        task = TaskMeta.tasks[taskname]
        self.assertTrue(task._error)
        self.assertEqual('shape=circle, regular=1,style=filled,fillcolor=red', task.get_graph_details())
