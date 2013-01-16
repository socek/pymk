from pymk.task import BaseTask, AddTask


@AddTask
class task_1(BaseTask):

    dependencys = []
    
    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.__class__.__name__)
        fp.write('\n')
        fp.close()
