from pymk.task import BaseTask, AddTask
from pymk.extra import touch

@AddTask
class task_14c(BaseTask):
    output_file = 'c.out'

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
        touch(cls.output_file)

@AddTask
class task_14b(BaseTask):

    conditions = [
        task_14c.condition_FileChanged,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
        touch(cls.output_file)

@AddTask
class task_14a(BaseTask):

    conditions = [
        task_14b.condition_FileChanged,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
