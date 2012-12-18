from pymk.task import BaseTask, AddTask
from pymk.extra import touch

@AddTask
class task_11c(BaseTask):

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()

@AddTask
class task_11b(BaseTask):

    dependencys = [
        task_11c.dependency_FileExists,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()

@AddTask
class task_11a(BaseTask):

    dependencys = [
        task_11b.dependency_FileExists,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
