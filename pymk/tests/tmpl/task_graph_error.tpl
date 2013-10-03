from pymk.tests.base import BaseTestTask
from pymk.dependency import AlwaysRebuild
from pymk.extra import run

class task_graph1_a(BaseTestTask):

    path = '/taska'

    dependencys = [
        AlwaysRebuild(),
    ]

    def build(self, args):
        run('rm /tmp/this_file_do_not_exists')
        super(task_graph1_a, self).build(args)

