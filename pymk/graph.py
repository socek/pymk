from pymk.dependency import AlwaysRebuild, FileChanged, FileDoesNotExists
from pymk.task import TaskData
from tempfile import TemporaryFile
from subprocess import Popen

datalog = TemporaryFile('wr')
running_list = []


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
            self._details = 'shape=circle,regular=1,style=filled,fillcolor=white,label="%s"' % (
                self._name.replace('/', '\\n')
            )
            self.extra = '[shape=dot]'
        elif _type == FileDoesNotExists:
            self._name = self.dep.filename
            self._details = 'shape=triangle, regular=1,style=filled,fillcolor=white,label="%s"' % (
                self._name.replace('/', '/\\n')
            )
            self.extra = '[shape=dot]'
        elif _type == AlwaysRebuild:
            self._name = 'Always\\nRebuild'
            self._details = 'shape=diamond, regular=1,style=filled,fillcolor=white,label="%s"' % (
                self._name.replace('/', '/\\n')
            )
            self.extra = '[shape=dot]'
        else:
            self._name = self.dep.im_self.__name__
            if self.dep.im_func.__name__ == 'dependency_FileChanged':
                self.extra = '[shape=dot,label="C"]'
            elif self.dep.im_func.__name__ == 'dependency_FileExists':
                self.extra = '[shape=dot,label="E"]'
            self._details = ''


class TaskShow(Show):
    def __init__(self, task):
        self._name = task.__name__
        self.always_rebuild = False
        self.runned = False

    def print_detailed(self):
        shape = 'box'
        color = 'white'
        if self.always_rebuild:
            shape = 'hexagon'
            color = 'grey'
        if self.runned:
            color = 'red'

        self._details = 'shape=%s, regular=1,style=filled,fillcolor=%s' %(shape, color)
        return super(TaskShow, self).print_detailed()


def run_dot(pipe, filename):
    filepipe = open(filename, 'w')
    spp = Popen(['dot', '-x', '-Tpng'], stdin=pipe, stdout=filepipe)
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


def draw_done_task_graph(filename):
    def print_data(data, parent_data=None):
        if data['type'] == 'task':
            taskShow = TaskShow(data['data'])
            if data['runned']:
                taskShow.runned = True
            for child in data['childs']:
                print_data(child, taskShow)
            taskShow.print_detailed()
        else:
            depShow = DependencyShow(data['data'])
            if data['runned']:
                depShow._details = depShow._details.replace('white', 'red')
                depShow.extra = depShow.extra.replace(']', ',color=red]')
            depShow.print_detailed()
            if parent_data:
                datalog.write('%s -> %s %s;\n' % (depShow.name, parent_data.name, depShow.extra))


    datalog.write('digraph {\n')
    for task_data in running_list:
        print_data(task_data)

    datalog.write('}\n')
    datalog.seek(0)
    run_dot(datalog, filename)
