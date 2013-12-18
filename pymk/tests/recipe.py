import os
from contextlib import nested
from mock import patch, MagicMock

from pymk.error import RecipeAlreadyExists, WrongPymkVersion
from pymk.recipe import Recipe, RecipeType, DownloadRecipe
from pymk.task import TaskType, Task
from pymk.tests.base import PymkTestCase


class RecipeExample(Recipe):
    singleton = False

    def create_settings(self):
        self.set_path('home', ['/tmp', ])
        self.settings['one'] = 1
        self.settings['two'] = 2


class TaskExample(Task):
    dependencys = []

    def build(self):
        pass  # pragma: no cover


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

    def test_init_with_parent(self):
        self.recipe.settings['one'] = 3

        recipe = RecipeExample(self.recipe)

        self.assertEqual(self.recipe.settings, recipe.settings)
        self.assertEqual(self.recipe.paths, recipe.paths)
        self.assertEqual(self.recipe.settings['one'], 1)

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

    def test_name(self):
        self.recipe.settings['name'] = 'my name'
        self.assertEqual('my name', self.recipe.name())

    def test_import_wrapper(self):
        with nested(
                patch('__builtin__.globals'),
                patch('__builtin__.locals'),
                patch('__builtin__.__import__'),
        ) as (_globals, _locals, _import):
            self.recipe.import_wrapper('name')
            _import.assert_called_once_with(
                'name', _globals.return_value, _locals.return_value, [''])

    def test_add_recipe(self):
        task = MagicMock()
        with nested(
                patch.dict(RecipeType.recipes, {'pymkmodules.name': task}),
                patch.object(self.recipe, 'import_wrapper'),
        ) as (recipes, import_wrapper):
            self.recipe.add_recipe('name')

            import_wrapper.assert_called_once_with('pymkmodules.name')
            self.assertTrue(task in self.recipe.recipes)
            task.assert_called_once_with(self.recipe)

    def test_add_recipe_no_recipe(self):
        task = MagicMock()
        with nested(
                patch.dict(RecipeType.recipes, {}),
                patch.object(self.recipe, 'import_wrapper'),
        ) as (recipes, import_wrapper):
            self.recipe.add_recipe('name')
            import_wrapper.assert_called_once_with('pymkmodules.name')
            self.assertFalse(task in self.recipe.recipes)
            self.assertEqual(0, task.call_count)


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


class DownloadRecipeTest(PymkTestCase):

    def setUp(self):
        super(DownloadRecipeTest, self).setUp()
        self.downloader = DownloadRecipe('name', 'url')

    @patch('pymk.recipe.DownloadRecipe')
    def test_download_from_recipe(self, DownloadRecipe):
        recipe = RecipeExample()
        recipe.download_recipe('name', 'url')

        DownloadRecipe.assert_called_once_with('name', 'url')
        DownloadRecipe.return_value.run.assert_called_once_with()

    def test_init(self):
        self.assertEqual('name', self.downloader.name)
        self.assertEqual('url', self.downloader.url)

    @patch('pymk.recipe.os.path.exists')
    def test_run_exists(self, existsmock):
        existsmock.return_value = True
        with patch.object(self.downloader, 'create_pymkmodules_path') as create_pymkmodules_path:
            with patch.object(self.downloader, 'download') as download:
                self.downloader.run()

                self.assertEqual(0, download.call_count)
                create_pymkmodules_path.assert_called_once_with()
                existsmock.assert_called_once_with(
                    '%s/%s.egg' % (self.downloader.modules_path, self.downloader.name))

    @patch('pymk.recipe.os.path.exists')
    def test_run_not_exists(self, existsmock):
        existsmock.return_value = False
        with patch.object(self.downloader, 'create_pymkmodules_path') as create_pymkmodules_path:
            with patch.object(self.downloader, 'download') as download:
                self.downloader.run()

                download.assert_called_once_with()
                create_pymkmodules_path.assert_called_once_with()
                existsmock.assert_called_once_with(
                    '%s/%s.egg' % (self.downloader.modules_path, self.downloader.name))

    @patch('pymk.recipe.os.path.exists')
    def test_create_pymkmodules_path_exists(self, existsmock):
        existsmock.return_value = True
        with patch('pymk.recipe.os.mkdir') as mkdirmock:
            self.downloader.create_pymkmodules_path()

            existsmock.assert_called_once_with(self.downloader.modules_path)
            self.assertEqual(0, mkdirmock.call_count)

    @patch('pymk.recipe.os.path.exists')
    def test_create_pymkmodules_path_not_exists(self, existsmock):
        existsmock.return_value = False
        with patch('pymk.recipe.os.mkdir') as mkdirmock:
            self.downloader.create_pymkmodules_path()

            existsmock.assert_called_once_with(self.downloader.modules_path)
            mkdirmock.assert_called_once_with(self.downloader.modules_path)

    @patch('pymk.recipe.log')
    def test_download(self, log):
        with patch('pymk.recipe.download') as download:
            with patch('pymk.recipe.extract_egg') as extract_egg:
                self.downloader.download()

                destination_egg_path = self.downloader.destination_path + \
                    '.zip'

                self.assertEqual(2, log.info.call_count)
                download.assert_called_once_with(
                    self.downloader.url, destination_egg_path)

                extract_egg.assert_called_once_with(
                    destination_egg_path, self.downloader.destination_path)
