import os
import sys
from pymk import VERSION, compare_version
from pymk.error import TaskAlreadyExists
from pymk.download import download, extract_egg


class RecipeType(type):
    recipes = {}
    args = {}
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                RecipeType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def __init__(cls, name, bases, dct):
        def check_if_recipe_exists(name):
            if name in list(RecipeType.recipes):
                raise TaskAlreadyExists(name)  # TODO: make it's own error

        def assign_recipe_to_tasks():
            from pymk.task import Task
            module = sys.modules[cls.__module__]
            for name in dir(module):
                obj = getattr(module, name)
                try:
                    if issubclass(obj, Task) and not obj.base:
                        obj.assign_recipe(cls)
                except TypeError:
                    pass

        #----------------------------------------------------------------------
        if not 'base' in dct or not dct['base']:
            check_if_recipe_exists(cls.__module__)
            RecipeType.recipes[cls.getName()] = cls
            assign_recipe_to_tasks()

    @classmethod
    def getRecipeForModule(cls, name):
        return RecipeType.recipes.get(name)


class Recipe(object):

    default_task = None
    base = True
    __metaclass__ = RecipeType

    def __init__(self):
        self.settings = {
            'minimal pymk version': VERSION,
            # 'name': None,
            'version': '0.0.0',
        }
        self.recipes = []

        self.create_settings()
        self.validate_settings()
        # self.gather_modules()
        self.gather_recipes()

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

    # def gather_modules(self):
    #     pass

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
