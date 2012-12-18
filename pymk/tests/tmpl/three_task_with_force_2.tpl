from pymk.task import BaseTask, AddTask
from pymk.extra import touch

@AddTask
class task_18c(BaseTask):
    output_file = 'c.out'

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
        touch(cls.output_file)

@AddTask
class task_18b(BaseTask):
    output_file = 'b.out'

    dependencys = [
        task_18c.dependency_FileExists,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
        touch(cls.output_file)

@AddTask
class task_18a(BaseTask):
    output_file = 'a.out'

    dependencys = [
        task_18b.dependency_FileExists,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
