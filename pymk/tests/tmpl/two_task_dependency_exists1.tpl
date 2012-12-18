from pymk.task import BaseTask, AddTask
from pymk.extra import touch

@AddTask
class task_6b(BaseTask):
    output_file = 'b.out'

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
        touch(cls.output_file)

@AddTask
class task_6a(BaseTask):
    output_file = 'a.out'

    dependencys = [
        task_6b.dependency_FileExists,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
