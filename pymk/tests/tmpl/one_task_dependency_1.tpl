from pymk.task import BaseTask, AddTask
from pymk.dependency import FileDoesNotExists

@AddTask
class task_2(BaseTask):

    dependencys = [
        FileDoesNotExists('test.txt'),
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
