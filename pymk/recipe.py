import sys

import logging
import os
from glob import glob
from smallsettings import Settings, Paths

from pymk import VERSION, compare_version
from pymk.dependency import Dependency
from pymk.download import download, extract_egg
from pymk.error import WrongPymkVersion, BadTaskPath, NotADependencyError, RecipeAlreadyExists
from pymk.task import Task


log = logging.getLogger('pymk')


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
    def is_not_a_base_class(cls, task):
        return hasattr(task, 'base') and not task.base

    @classmethod
    def assign_recipe_to_task_if_able(cls, recipe, task):
        try:
            if issubclass(task, Task) and cls.is_not_a_base_class(task):
                task.assign_recipe(recipe)
        except TypeError:
            # class do not have a base value
            pass

    @classmethod
    def assign_recipe_to_tasks(cls, recipe):
        #----------------------------------------------------------------------
        module = sys.modules[recipe.__module__]
        for name in dir(module):
            task = getattr(module, name)
            cls.assign_recipe_to_task_if_able(recipe, task)

    @classmethod
    def getRecipeForModule(cls, name):
        return RecipeType.recipes.get(name)


class Recipe(object):

    default_task = None
    base = True
    __metaclass__ = RecipeType
    singleton = True

    def __init__(self, parent=None):
        self.settings = Settings({
            'minimal pymk version': VERSION,
        })
        self.paths = Paths()
        self.recipes = []

        self.create_settings()
        self.validate_settings()
        self.gather_recipes()
        self.refresh_modules()
        self.validate_pymkmodules()
        self.validate_tasks()

        if parent is not None:
            parent.settings.update(self.settings)
            self.settings = parent.settings

            parent.paths.update(self.paths)
            self.paths = parent.paths

        self.post_action()

    def validate_pymkmodules(self):
        if os.path.exists('pymkmodules') and not os.path.exists('pymkmodules/__init__.py'):
            open('pymkmodules/__init__.py', 'a').close()

    def assign_main_path(self, path):
        self.paths['main'] = os.path.dirname(path)

    @classmethod
    def getName(cls):
        return cls.__module__

    def getTask(self, path):
        self._getTaskType().get_task(path)

    def _getTaskType(self):
        from pymk.task import TaskType
        return TaskType

    def getDefaultTask(self):
        if self.default_task is None:
            return None
        else:
            try:
                return self._getTaskType().get_task(self.default_task)
            except KeyError:
                raise BadTaskPath(self.default_task)

    def validate_settings(self):
        min_pymk_version = self.settings['minimal pymk version']
        if compare_version(VERSION, min_pymk_version) == -1:
            raise WrongPymkVersion(VERSION, min_pymk_version)

    def create_settings(self):
        pass

    def post_action(self):
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

    def refresh_modules(self):
        sys.path[0:0] = ['pymkmodules'] + glob('pymkmodules/*.egg')

    def download_recipe(self, name, url):
        download_recipe = DownloadRecipe(name, url)
        return download_recipe.run()

    def import_wrapper(self, name):
        return __import__(name, globals(), locals(), [''])

    def add_recipe(self, name):
        name = '.'.join(['pymkmodules', name])
        self.import_wrapper(name)
        if name in RecipeType.recipes:
            recipe = RecipeType.recipes[name]
            recipe(self)
            self.recipes.append(recipe)

    def name(self):
        return self.settings['name']

    def validate_tasks(self):
        for path, task in self._getTaskType().tasks.items():
            for dependency in task().dependencys:
                if not issubclass(type(dependency), Dependency):
                    raise NotADependencyError(dependency, task)


class DownloadRecipe(object):
    modules_path = 'pymkmodules'

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.destination_path = os.path.join(
            self.modules_path, self.name + '.egg')

    def run(self):
        self.create_pymkmodules_path()
        if not os.path.exists(self.destination_path):
            self.download()

    def create_pymkmodules_path(self):
        if not os.path.exists(self.modules_path):
            os.mkdir(self.modules_path)

    def download(self):
        destination_egg_path = self.destination_path + '.zip'
        log.info("Downloading %s..." % (self.name,))
        download(self.url, destination_egg_path)
        log.info("Extracting %s..." % (self.name,))
        extract_egg(destination_egg_path, self.destination_path)
