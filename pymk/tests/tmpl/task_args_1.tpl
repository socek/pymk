from pymk.task import Task
from json import dump

class task_args1_a(Task):

    _name = '/taska'

    dependencys = [
    ]

    def build(self, args):
        fp = open('ta.out', 'w')
        dump(args, fp)
        fp.close()

        fp = open('a.out', 'a')
        fp.write(self.name())
        fp.write('\n')
        fp.close()
