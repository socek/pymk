from pymk.task import BaseTask, AddTask


@AddTask
class task_5(BaseTask):
    output_file = 'a.out'

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
