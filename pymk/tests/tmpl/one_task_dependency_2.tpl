from pymk.task import BaseTask, AddTask
from pymk.dependency import FileChanged

@AddTask
class task_3(BaseTask):

    dependencys = [
        FileChanged('test.txt'),
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
