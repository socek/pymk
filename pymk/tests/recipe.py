import os
import sys
from mock import patch, MagicMock
from contextlib import nested

from pymk.tests.base import PymkTestCase
from pymk.recipe import Recipe, RecipeType
from pymk.error import RecipeAlreadyExists


class RecipeExample(Recipe):
    singleton = False

    def create_settings(self):
        self.set_path('home', ['/tmp', ])


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
        self.assertRaises(RecipeAlreadyExists, RecipeType.check_if_recipe_exists, 'something')

    def test_check_if_recipe_exists_false(self):
        self.assertEqual(None, RecipeType.check_if_recipe_exists('something'))

    def test_getRecipeForModule(self):
        self.assertEqual(None, RecipeType.getRecipeForModule('something'))

    def test_getRecipeForModule_with_module(self):
        RecipeType.recipes['something'] = 1
        self.assertEqual(1, RecipeType.getRecipeForModule('something'))

