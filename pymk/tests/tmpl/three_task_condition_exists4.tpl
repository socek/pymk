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

    conditions = [
        task_11c.condition_FileExists,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()

@AddTask
class task_11a(BaseTask):

    conditions = [
        task_11b.condition_FileExists,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
