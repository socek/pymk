from pymk.task import BaseTask, AddTask
from pymk.extra import touch

@AddTask
class task_15c(BaseTask):

    dependencys = []

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()

@AddTask
class task_15b(BaseTask):

    dependencys = [
        task_15c.dependency_FileChanged(),
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()

@AddTask
class task_15a(BaseTask):

    dependencys = [
        task_15b.dependency_FileChanged(),
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
