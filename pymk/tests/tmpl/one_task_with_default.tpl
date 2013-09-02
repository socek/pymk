from pymk.task import Task
from pymk.recipe import Recipe

class MyRecipe(Recipe):
    default_task = 'task_0'

class task_0(Task):

    dependencys = []

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()

