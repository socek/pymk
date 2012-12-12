from pymk.task import BaseTask, AddTask
from pymk.condition import FileChanged

@AddTask
class task_3(BaseTask):

    conditions = [
        FileChanged('test.txt'),
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
