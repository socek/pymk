from pymk.task import Task
from pymk.recipe import Recipe


class RecipeMy(Recipe):
    pass


class task_20_with_recipe(Task):

    dependencys = [int]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
