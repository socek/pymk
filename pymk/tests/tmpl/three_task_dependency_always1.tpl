from pymk.task import Task
from pymk.extra import touch
from pymk.dependency import AlwaysRebuild

class task_16c(Task):
    output_file = 'c.out'

    dependencys = []

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
        touch(self.output_file)

class task_16b(Task):
    output_file = 'b.out'

    dependencys = [
        task_16c.dependency_FileChanged(),
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
        touch(self.output_file)

class task_16a(Task):
    output_file = 'a.out'

    dependencys = [
        task_16b.dependency_FileChanged(),
        AlwaysRebuild(),
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
