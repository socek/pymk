from mock import patch, MagicMock

from pymk import compare_version
from pymk.tests.base import PymkTestCase
from pymk.script import init_recipe
from pymk.error import CommandError, BadTaskPath
from pymk.task import TaskType, _GetTask


class _GetTaskTest(PymkTestCase):

    def test_parse_task_name(self):
        name, args = _GetTask('/something/elo').parse_url()
        self.assertEqual('/something/elo', name)
        self.assertEqual({}, args)

        name, args = _GetTask('/something/elo?elo=10').parse_url()
        self.assertEqual('/something/elo', name)
        self.assertEqual({'elo': ['10']}, args)

        name, args = _GetTask('/something/elo/?elo=10&zbychu=12').parse_url()
        self.assertEqual('/something/elo/', name)
        self.assertEqual({'elo': ['10'], 'zbychu': ['12']}, args)

        name, args = _GetTask(
            '/something/elo/?elo=10&zbychu=12,10&zbychu=ccc').parse_url()
        self.assertEqual('/something/elo/', name)
        self.assertEqual({'elo': ['10'], 'zbychu': ['12,10', 'ccc']}, args)

    @patch.object(TaskType, 'tasks', {})
    def test_check_if_task_name_exists_fail(self):
        data = _GetTask('/something/elo')
        self.assertRaises(
            BadTaskPath, data.check_if_task_name_exists, '/something/elo')

    @patch.object(TaskType, 'tasks', {})
    def test_check_if_task_name_exists_success(self):
        TaskType.tasks['/something/elo'] = 1
        data = _GetTask('/something/elo')
        result = data.check_if_task_name_exists('/something/elo')
        self.assertEqual(None, result)

    @patch.object(TaskType, 'tasks', {})
    def test_get_task(self):
        TaskType.tasks['/something/elo'] = 2
        data = _GetTask('/something/elo')
        self.assertEqual(2, data.get_task('/something/elo'))

    @patch.object(TaskType, 'tasks', {})
    def test_call(self):
        mock = MagicMock()
        TaskType.tasks['/something/elo'] = mock
        data = _GetTask('/something/elo?elo=10')
        task = data()
        self.assertEqual(mock, task)
        self.assertEqual({'elo': ['10']}, mock._args)


class GraphTest(PymkTestCase):

    def test_error_in_task(self):
        taskname = '/taska'
        self._template('task_graph_error', 'mkfile.py')
        self._import_mkfile()
        self._add_task(taskname)

        self.assertRaises(CommandError, self._pymk_runtask, [])
        task = TaskType.tasks[taskname]
        self.assertTrue(task._error)
        self.assertEqual(
            'shape=circle, regular=1,style=filled,fillcolor=red', task.get_graph_details())


class InitRecipe(PymkTestCase):

    @patch('pymk.script.RecipeType')
    def test_init_recipe(self, RecipeType):
        self.assertTrue(init_recipe('something'))
        RecipeType.getRecipeForModule.assert_called_once_with('something')
        value = RecipeType.getRecipeForModule.return_value
        value.assert_called_once_with()

    @patch('pymk.script.RecipeType')
    def test_init_recipe_with_no_recipe(self, RecipeType):
        RecipeType.getRecipeForModule.return_value = None
        self.assertFalse(init_recipe('something'))
        RecipeType.getRecipeForModule.assert_called_once_with('something')


class CompareVersion(PymkTestCase):

    def test_greater(self):
        self.assertEqual(-1, compare_version('0.3.9', '0.4.0'))
        self.assertEqual(-1, compare_version('0.3.9.1', '0.4.0'))
        self.assertEqual(-1, compare_version('0.3.9.2-custome', '0.4.0'))
        self.assertEqual(-1, compare_version('0.3.9.3.custome', '0.4.0'))
        self.assertEqual(-1, compare_version('0.4.0', '0.4.0.custome'))
        self.assertEqual(-1, compare_version('0.4.0', '0.4.0-custome'))

    def test_equal(self):
        self.assertEqual(0, compare_version('0.4.0', '0.4.0'))

    def test_lower(self):
        self.assertEqual(1, compare_version('0.4.0', '0.3.9'))
        self.assertEqual(1, compare_version('0.4.0', '0.3.9.1'))
        self.assertEqual(1, compare_version('0.4.0', '0.3.9.2-custome'))
        self.assertEqual(1, compare_version('0.4.0', '0.3.9.3.custome'))
        self.assertEqual(1, compare_version('0.4.0.custome', '0.4.0', ))
        self.assertEqual(1, compare_version('0.4.0-custome', '0.4.0'))
