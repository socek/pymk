from pymk.task import BaseTask, AddTask
from pymk.condition import FileDoesNotExists

@AddTask
class task_2(BaseTask):

    conditions = [
        FileDoesNotExists('test.txt'),
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
