from pymk.task import Task
from pymk.dependency import FileChanged

class task_21(Task):

    output_file = 'a.out'

    dependencys = [
        FileChanged(['test.txt', 'test2.txt']),
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
