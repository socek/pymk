from pymk.task import BaseTask, AddTask
from pymk.extra import touch

@AddTask
class task_15c(BaseTask):

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()

@AddTask
class task_15b(BaseTask):

    dependencys = [
        task_15c.dependency_FileChanged,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()

@AddTask
class task_15a(BaseTask):

    dependencys = [
        task_15b.dependency_FileChanged,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
