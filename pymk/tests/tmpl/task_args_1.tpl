from pymk.tests.base import BaseTestTask
from json import dump

class task_args1_a(BaseTestTask):

    name = '/taska'

    dependencys = [
    ]

    def build(self, args):
        fp = open('ta.out', 'w')
        dump(args, fp)
        fp.close()

        super(task_args1_a, self).build(args)
