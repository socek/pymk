from pymk.task import BaseTask, AddTask
from pymk.extra import touch

@AddTask
class task_7c(BaseTask):
    output_file = 'c.out'

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
        touch(cls.output_file)

@AddTask
class task_7b(BaseTask):
    output_file = 'b.out'

    conditions = [
        task_7c.condition_FileChanged,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
        touch(cls.output_file)

@AddTask
class task_7a(BaseTask):
    output_file = 'a.out'

    conditions = [
        task_7b.condition_FileExists,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
