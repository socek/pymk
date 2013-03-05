from pymk.task import Task
from pymk.dependency import FileDoesNotExists

class task_2(Task):

    dependencys = [
        FileDoesNotExists('test.txt'),
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
