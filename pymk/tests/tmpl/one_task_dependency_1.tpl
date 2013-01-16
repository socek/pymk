from pymk.task import BaseTask, AddTask
from pymk.dependency import FileDoesNotExists

@AddTask
class task_2(BaseTask):

    dependencys = [
        FileDoesNotExists('test.txt'),
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
