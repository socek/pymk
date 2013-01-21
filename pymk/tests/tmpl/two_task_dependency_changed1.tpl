from pymk.task import BaseTask, AddTask
from pymk.extra import touch

@AddTask
class task_8b(BaseTask):
    output_file = 'b.out'

    dependencys = []

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
        touch(self.output_file)

@AddTask
class task_8a(BaseTask):
    output_file = 'a.out'

    dependencys = [
        task_8b.dependency_FileChanged(),
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
