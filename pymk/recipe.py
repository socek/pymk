import os
import sys

from pymk import VERSION, compare_version
from pymk.error import RecipeAlreadyExists
from pymk.download import download, extract_egg
from pymk.task import Task


class RecipeType(type):
    recipes = {}
    args = {}
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls.singleton:
            if cls not in cls._instances:
                cls._instances[cls] = super(
                    RecipeType, cls).__call__(*args, **kwargs)
            return cls._instances[cls]
        else:
            return super(RecipeType, cls).__call__(*args, **kwargs)

    def __init__(cls, name, bases, dct):
        if not 'base' in dct or not dct['base']:
            RecipeType.check_if_recipe_exists(cls.__module__)
            RecipeType.recipes[cls.getName()] = cls
            RecipeType.assign_recipe_to_tasks(cls)

    @classmethod
    def check_if_recipe_exists(cls, name):
        if name in list(cls.recipes):
            raise RecipeAlreadyExists(name)

    @classmethod
    def assign_recipe_to_tasks(cls, recipe):
        def is_not_a_base_class(task):
            return hasattr(task, 'base') and not task.base
        #----------------------------------------------------------------------
        module = sys.modules[recipe.__module__]
        for name in dir(module):
            task = getattr(module, name)
            try:
                if issubclass(task, Task) and is_not_a_base_class(task):
                    task.assign_recipe(recipe)
            except TypeError:
                # class do not have a base value
                pass

    @classmethod
    def getRecipeForModule(cls, name):
        return RecipeType.recipes.get(name)


class Recipe(object):

    default_task = None
    base = True
    __metaclass__ = RecipeType
    singleton = True

    def __init__(self):
        self.settings = {
            'minimal pymk version': VERSION,
            'version': '4.0.0',
        }
        self.paths = {}
        self.recipes = []

        self.create_settings()
        self.validate_settings()
        self.gather_recipes()

    def assign_main_path(self, path):
        self.paths['main'] = os.path.dirname(path)

    @classmethod
    def getName(cls):
        return cls.__module__

    def getDefaultTask(self):
        from pymk.task import TaskType
        if self.default_task is None:
            return None
        else:
            return TaskType.tasks[self.default_task]

    def validate_settings(self):
        min_pymk_version = self.settings['minimal pymk version']
        if compare_version(VERSION, min_pymk_version) == -1:
            raise RuntimeError(  # TODO: make this seperate exception class
                'Bad pymk version. Please update pymk to use this recipe.')

    def create_settings(self):
        pass

    def set_setting(self, name, value):
        parsed_value = value % self.settings
        self.settings[name] = parsed_value

    def set_path(self, name, values):
        if type(values) not in (list, tuple):
            values = [values, ]
        parsed_values = []
        for value in values:
            parsed_values.append(
                value % self.paths
            )
        self.paths[name] = os.path.join(*parsed_values)

    def gather_recipes(self):
        pass

    def download_recipe(self, name, url):
        if not os.path.exists('pymkmodules'):
            os.mkdir('pymkmodules')
        destination_path = os.path.join('pymkmodules', name + '.egg')
        if not os.path.exists(destination_path):
            destination_egg_path = destination_path + '.zip'
            print "Downloading %s..." % (name,)
            download(url, destination_egg_path)
            print "Extracting %s..." % (name,)
            extract_egg(destination_egg_path, destination_path)

    def add_recipe(self, name):
        name = '.'.join(['pymkmodules', name])
        __import__(name, globals(), locals(), [''])
        if name in RecipeType.recipes:
            recipe = RecipeType.recipes[name]
            recipe()
            self.recipes.append(recipe)

    def name(self):
        return self.settings['name']
