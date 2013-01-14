from pymk.task import BaseTask, AddTask


@AddTask
class task_0(BaseTask):

    dependencys = []

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()

_DEFAULT=task_0
