from pymk.task import Task


class task_0(Task):

    dependencys = []

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()

SETTINGS = {
    'default task' : task_0,
}
