from pymk.task import BaseTask, AddTask


@AddTask
class task_1(BaseTask):

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
