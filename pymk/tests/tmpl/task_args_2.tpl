from pymk.task import Task
from pymk.dependency import AlwaysRebuild
from json import dump

class task_args2_a(Task):

    _name = '/taska'

    dependencys = [
        AlwaysRebuild(),
    ]

    def build(self, args):
        fp = open('ta.out', 'w')
        dump(args, fp)
        fp.close()

        fp = open('a.out', 'a')
        fp.write(self.name())
        fp.write('\n')
        fp.close()

class task_args2_b(Task):

    _name = '/taskb'

    dependencys = [
        task_args2_a.dependency_Link(),
        AlwaysRebuild(),
    ]

    def build(self, args):
        print 'build'
        fp = open('tb.out', 'w')
        dump(args, fp)
        fp.close()

        fp = open('a.out', 'a')
        fp.write(self.name())
        fp.write('\n')
        fp.close()

class task_args2_c(Task):

    _name = '/taskc'

    dependencys = [
        task_args2_b.dependency_Link(),
        AlwaysRebuild(),
    ]

    def build(self, args):
        fp = open('tc.out', 'w')
        dump(args, fp)
        fp.close()

        fp = open('a.out', 'a')
        fp.write(self.name())
        fp.write('\n')
        fp.close()
