from pymk.task import BaseTask, AddTask
from pymk.extra import touch
from pymk.dependency import AlwaysRebuild

@AddTask
class task_16c(BaseTask):
    output_file = 'c.out'

    dependencys = []

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
        touch(self.output_file)

@AddTask
class task_16b(BaseTask):
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

@AddTask
class task_16a(BaseTask):
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
