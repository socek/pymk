from pymk.task import Task
from pymk.extra import touch

class task_14c(Task):
    output_file = 'c.out'

    dependencys = []

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
        touch(self.output_file)

class task_14b(Task):

    dependencys = [
        task_14c.dependency_FileChanged(),
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
        touch(self.output_file)

class task_14a(Task):

    dependencys = [
        task_14b.dependency_FileChanged(),
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
