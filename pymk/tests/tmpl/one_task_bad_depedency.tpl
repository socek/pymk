from pymk.task import Task


class task_20(Task):

    dependencys = [int]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
