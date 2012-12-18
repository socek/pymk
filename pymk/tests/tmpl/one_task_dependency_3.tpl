from pymk.task import BaseTask, AddTask
from pymk.dependency import FileChanged

@AddTask
class task_4(BaseTask):

    output_file = 'a.out'

    dependencys = [
        FileChanged('test.txt'),
    ]

    @classmethod
    def build(cls):
        fp = open('a.out', 'a')
        fp.write(cls.__name__)
        fp.write('\n')
        fp.close()
