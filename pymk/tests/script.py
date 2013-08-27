from mock import patch

from pymk import compare_version
from pymk.tests.base import PymkTestCase
from pymk.script import parse_task_name, init_recipe
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

        name, args = parse_task_name(
            '/something/elo/?elo=10&zbychu=12,10&zbychu=ccc')
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
