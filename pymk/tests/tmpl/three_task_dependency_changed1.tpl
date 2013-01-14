from pymk.task import BaseTask, AddTask
from pymk.extra import touch

@AddTask
class task_12c(BaseTask):
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
class task_12b(BaseTask):
    output_file = 'b.out'

    dependencys = [
        task_12c.dependency_FileChanged,
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

    dependencys = [
        task_12b.dependency_FileChanged,
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
