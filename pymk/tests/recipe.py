import os

from pymk.tests.base import PymkTestCase
from pymk.recipe import Recipe


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
