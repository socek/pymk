import os
from contextlib import nested
from mock import patch, MagicMock

from pymk.error import RecipeAlreadyExists, WrongPymkVersion
from pymk.recipe import Recipe, RecipeType
from pymk.task import TaskType, Task
from pymk.tests.base import PymkTestCase


class RecipeExample(Recipe):
    singleton = False

    def create_settings(self):
        self.set_path('home', ['/tmp', ])


class TaskExample(Task):
    dependencys = []

    def build(self):
        pass


class RecipeTest(PymkTestCase):

    def setUp(self):
        super(RecipeTest, self).setUp()
        self.recipe = RecipeExample()

    def test_set_path(self):
        self.recipe.set_path('path', ['%(home)s', 'elf', 'samantha'])

        self.assertEqual(
            os.path.join('/tmp', 'elf', 'samantha'),
            self.recipe.paths['path']
        )

    def test_set_path_no_list(self):
        self.recipe.set_path('path', '/something')

        self.assertEqual('/something', self.recipe.paths['path'])

    def test_set_setting(self):
        self.recipe.settings['name'] = 'my name'
        self.recipe.set_setting('something', ':%(name)s:')

        self.assertEqual(':my name:', self.recipe.settings['something'])

    def test_getName(self):
        self.assertEqual('pymk.tests.recipe', self.recipe.getName())

    def test_assign_main_path(self):
        self.recipe.assign_main_path(__file__)
        self.assertEqual(
            os.path.dirname(__file__), self.recipe.paths['main'])

    def test_getDefaultTask_no_task(self):
        self.recipe.default_task = None
        task = self.recipe.getDefaultTask()
        self.assertEqual(None, task)

    @patch.object(TaskType, 'tasks', {})
    def test_getDefaultTask(self):
        TaskType.tasks['default'] = MagicMock()
        self.recipe.default_task = 'default'

        task = self.recipe.getDefaultTask()
        self.assertEqual(TaskType.tasks['default'], task)

    @patch('pymk.recipe.compare_version')
    def test_validate_settings_equal(self, compare_version):
        compare_version.return_value = 0
        self.recipe.settings['minimal pymk version'] = MagicMock()
        with patch('pymk.recipe.VERSION') as VERSION:
            self.assertEqual(None, self.recipe.validate_settings())
            compare_version.assert_called_once_with(
                VERSION, self.recipe.settings['minimal pymk version'])

    @patch('pymk.recipe.compare_version')
    def test_validate_settings_greater(self, compare_version):
        compare_version.return_value = 1
        self.recipe.settings['minimal pymk version'] = MagicMock()
        with patch('pymk.recipe.VERSION') as VERSION:
            self.assertEqual(None, self.recipe.validate_settings())
            compare_version.assert_called_once_with(
                VERSION, self.recipe.settings['minimal pymk version'])

    @patch('pymk.recipe.compare_version')
    def test_validate_settings_lower(self, compare_version):
        compare_version.return_value = -1
        self.recipe.settings['minimal pymk version'] = MagicMock()
        with patch('pymk.recipe.VERSION') as VERSION:
            self.assertRaises(WrongPymkVersion, self.recipe.validate_settings)
            compare_version.assert_called_once_with(
                VERSION, self.recipe.settings['minimal pymk version'])


class RecipeTypeTest(PymkTestCase):

    def _init_patchers(self):
        super(RecipeTypeTest, self)._init_patchers()
        self.patchers['recipes'] = patch.object(RecipeType, 'recipes', {})
        self.patchers['args'] = patch.object(RecipeType, 'args', {})
        self.patchers['_instances'] = patch.dict(RecipeType._instances, {})

    def test_init(self):
        with nested(
                patch.object(RecipeType, 'check_if_recipe_exists'),
                patch.object(RecipeType, 'assign_recipe_to_tasks'),
        ) as (check_if_recipe_exists, assign_recipe_to_tasks):
            RecipeType.getName = MagicMock()
            RecipeType('RecipeExample', (), {})

            check_if_recipe_exists.assert_called_once_with('pymk.tests.recipe')
            assign_recipe_to_tasks.assert_called_once()
            self.assertTrue(
                RecipeType.getName.return_value in RecipeType.recipes)

    def test_init_base_class(self):
        with nested(
                patch.object(RecipeType, 'check_if_recipe_exists'),
                patch.object(RecipeType, 'assign_recipe_to_tasks'),
        ) as (check_if_recipe_exists, assign_recipe_to_tasks):
            RecipeType('RecipeExample', (), {'base': True})

            self.assertEqual(0, check_if_recipe_exists.call_count)
            self.assertEqual(0, assign_recipe_to_tasks.call_count)
            self.assertEqual({}, RecipeType.recipes)

    def test_check_if_recipe_exists_true(self):
        RecipeType.recipes['something'] = 1
        self.assertRaises(
            RecipeAlreadyExists, RecipeType.check_if_recipe_exists, 'something')

    def test_check_if_recipe_exists_false(self):
        self.assertEqual(None, RecipeType.check_if_recipe_exists('something'))

    def test_getRecipeForModule(self):
        self.assertEqual(None, RecipeType.getRecipeForModule('something'))

    def test_getRecipeForModule_with_module(self):
        RecipeType.recipes['something'] = 1
        self.assertEqual(1, RecipeType.getRecipeForModule('something'))

    def test_is_not_a_base_class_no_base(self):
        task = object()
        self.assertFalse(RecipeType.is_not_a_base_class(task))

    def test_is_not_a_base_class_base_is_true(self):
        task = MagicMock()
        task.base = True
        self.assertFalse(RecipeType.is_not_a_base_class(task))

    def test_is_not_a_base_class_base_is_false(self):
        task = MagicMock()
        task.base = False
        self.assertTrue(RecipeType.is_not_a_base_class(task))

    def test_assign_recipe_to_task_if_able_do_assign(self):
        task = TaskExample
        recipe = MagicMock()
        with nested(
                patch.object(RecipeType, 'is_not_a_base_class'),
                patch.object(task, 'assign_recipe'),
        ) as (is_not_a_base_class, assign_recipe):
            is_not_a_base_class.return_value = True
            RecipeType.assign_recipe_to_task_if_able(recipe, task)

            is_not_a_base_class.assert_called_once_with(task)
            assign_recipe.assert_called_once_with(recipe)

    def test_assign_recipe_to_task_if_able_base_class(self):
        task = TaskExample
        recipe = MagicMock()
        with nested(
                patch.object(RecipeType, 'is_not_a_base_class'),
                patch.object(task, 'assign_recipe'),
        ) as (is_not_a_base_class, assign_recipe):
            is_not_a_base_class.return_value = False
            RecipeType.assign_recipe_to_task_if_able(recipe, task)

            is_not_a_base_class.assert_called_once_with(task)
            self.assertEqual(0, assign_recipe.call_count)

    def test_assign_recipe_to_task_if_able_wrong_class(self):
        task = TaskExample()
        recipe = MagicMock()
        with nested(
                patch.object(RecipeType, 'is_not_a_base_class'),
                patch.object(task, 'assign_recipe'),
        ) as (is_not_a_base_class, assign_recipe):
            RecipeType.assign_recipe_to_task_if_able(recipe, task)

            self.assertEqual(0, is_not_a_base_class.call_count)
            self.assertEqual(0, assign_recipe.call_count)
