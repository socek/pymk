from pymk.tests.base import BaseTestTask
from pymk.dependency import AlwaysRebuild
from json import dump


class task_args2_a(BaseTestTask):

    name = 'Task A'
    path = '/taska'

    dependencys = [
        AlwaysRebuild(),
    ]

    def build(self, args):
        fp = open('ta.out', 'w')
        dump(args, fp)
        fp.close()

        super(task_args2_a, self).build(args)

class task_args2_b(BaseTestTask):

    name = 'Task B'
    path = '/taskb'

    dependencys = [
        task_args2_a.dependency_Link(),
        AlwaysRebuild(),
    ]

    def build(self, args):
        fp = open('tb.out', 'w')
        dump(args, fp)
        fp.close()

        super(task_args2_b, self).build(args)

class task_args2_c(BaseTestTask):

    name = 'Task C'
    path = '/taskc'

    dependencys = [
        task_args2_b.dependency_Link(),
        AlwaysRebuild(),
    ]

    def build(self, args):
        fp = open('tc.out', 'w')
        dump(args, fp)
        fp.close()

        super(task_args2_c, self).build(args)
