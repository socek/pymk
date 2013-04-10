from pymk.task import Task
from pymk.dependency import FileChanged

class task_linka(Task):

    output_file = 'a.out'

    dependencys = [
        FileChanged('a.dep.txt'),
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()

class task_linkb(Task):

    output_file = 'a.out'

    dependencys = [
        FileChanged('b.dep.txt'),
        task_linka.dependency_Link(),
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
