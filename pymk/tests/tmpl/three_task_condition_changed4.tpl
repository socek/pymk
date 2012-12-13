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

    conditions = [
        task_15c.condition_FileChanged,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()

@AddTask
class task_15a(BaseTask):

    conditions = [
        task_15b.condition_FileChanged,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
