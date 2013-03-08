from pymk.task import Task
from pymk.dependency import FileChanged

class task_3(Task):

    dependencys = [
        FileChanged('test.txt'),
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
