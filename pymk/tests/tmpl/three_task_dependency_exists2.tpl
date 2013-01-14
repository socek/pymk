from pymk.task import BaseTask, AddTask
from pymk.extra import touch

@AddTask
class task_9c(BaseTask):
    output_file = 'c.out'

    dependencys = []

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
        touch(cls.output_file)

@AddTask
class task_9b(BaseTask):
    output_file = 'b.out'

    dependencys = [
        task_9c.dependency_FileChanged,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
        touch(cls.output_file)

@AddTask
class task_9a(BaseTask):

    dependencys = [
        task_9b.dependency_FileExists,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
