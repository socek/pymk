from pymk.dependency import AlwaysRebuild, FileChanged, FileDoesNotExists
from pymk.task import TaskData
from tempfile import TemporaryFile
from subprocess import Popen, PIPE

datalog = TemporaryFile('w+r')


class Show(object):
    detailed = []

    extra = ''

    @property
    def name(self):
        return '"' + self._name + '"'

    def print_detailed(self):
        if not self.name in self.detailed:
            self.detailed.append(self.name)
            datalog.write('%s [%s];\n' % (self.name, self._details))


class DependencyShow(Show):

    def __init__(self, dependency):
        self.dep = dependency

        _type = type(self.dep)
        if _type == FileChanged:
            self._name = self.dep.filename
            self._details = 'shape=circle, regular=1,style=filled,fillcolor=white,label="%s"' % (
                self._name.replace('/', '\\n')
            )
            self.extra = '[style=bold,color=red]'
        elif _type == FileDoesNotExists:
            self._name = self.dep.filename
            self._details = 'shape=circle, regular=1,style=filled,fillcolor=red,label="%s"' % (
                self._name.replace('/', '/\\n')
            )
            self.extra = '[style=bold,color=blue]'
        else:
            self._name = self.dep.im_self.__name__
            if self.dep.im_func.__name__ == 'dependency_FileChanged':
                self.extra = '[style=bold,color=red]'


class TaskShow(Show):
    def __init__(self, task):
        self._name = task.__name__
        self.always_rebuild = False

    def print_detailed(self):
        if self.always_rebuild:
            self._details = 'shape=box, regular=1,style=filled,fillcolor=grey'
        else:
            self._details = 'shape=box, regular=1,style=filled,fillcolor=white'
        return super(TaskShow, self).print_detailed()


def run_dot(pipe, filename):
    filepipe = open(filename, 'w')
    spp = Popen(['dot', '-x' ,'-Tpng'], stdin=pipe, stdout=filepipe)
    spp.wait()

def draw_graph(filename):
    datalog.write('digraph {\n')
    for task in TaskData._all_tasks:
        taskShow = TaskShow(task)
        for dep in task.dependencys:
            if type(dep) == AlwaysRebuild:
                taskShow.always_rebuild = True
            else:
                depShow = DependencyShow(dep)
                depShow.print_detailed()
                datalog.write('%s -> %s %s;\n' % (depShow.name, taskShow.name, depShow.extra))
        taskShow.print_detailed()

    datalog.write('}\n')
    datalog.seek(0)
    run_dot(datalog, filename)
