from pymk.task import BaseTask, AddTask
from pymk.extra import touch

@AddTask
class task_9c(BaseTask):
    output_file = 'c.out'

    dependencys = []

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
        touch(self.output_file)

@AddTask
class task_9b(BaseTask):
    output_file = 'b.out'

    dependencys = [
        task_9c.dependency_FileChanged,
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
        touch(self.output_file)

@AddTask
class task_9a(BaseTask):

    dependencys = [
        task_9b.dependency_FileExists,
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
