from pymk.task import BaseTask, AddTask
from pymk.extra import touch

@AddTask
class task_11c(BaseTask):

    dependencys = []

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()

@AddTask
class task_11b(BaseTask):

    dependencys = [
        task_11c.dependency_FileExists(),
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()

@AddTask
class task_11a(BaseTask):

    dependencys = [
        task_11b.dependency_FileExists(),
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
