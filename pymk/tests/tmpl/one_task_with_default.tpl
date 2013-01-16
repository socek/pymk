from pymk.task import BaseTask, AddTask


@AddTask
class task_0(BaseTask):

    dependencys = []

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()

_DEFAULT=task_0
