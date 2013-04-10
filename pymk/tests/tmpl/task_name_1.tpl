from pymk.task import Task


class task_namea(Task):

    _name = '/something/usful'

    output_file = 'a.out'

    dependencys = [
    ]

    def build(self):
        fp = open('a.out', 'a')
        fp.write(self.name())
        fp.write('\n')
        fp.close()
