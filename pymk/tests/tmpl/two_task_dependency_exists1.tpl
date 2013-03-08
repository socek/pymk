from pymk.task import Task
from pymk.extra import touch

class task_6b(Task):
    output_file = 'b.out'

    dependencys = []

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
        touch(self.output_file)

class task_6a(Task):
    output_file = 'a.out'

    dependencys = [
        task_6b.dependency_FileExists(),
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
