from pymk.task import BaseTask, AddTask
from pymk.extra import touch

@AddTask
class task_12c(BaseTask):
    output_file = 'c.out'

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
        touch(cls.output_file)

@AddTask
class task_12b(BaseTask):
    output_file = 'b.out'

    conditions = [
        task_12c.condition_FileChanged,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
        touch(cls.output_file)

@AddTask
class task_12a(BaseTask):
    output_file = 'a.out'

    conditions = [
        task_12b.condition_FileChanged,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
