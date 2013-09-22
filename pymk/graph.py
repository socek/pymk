from pymk.task import TaskType
from pymk.dependency import AlwaysRebuild
from tempfile import TemporaryFile, NamedTemporaryFile
from subprocess import Popen

datalog = TemporaryFile('wr')
running_list = []


def run_dot(pipe, filename):
    filepipe = open(filename, 'w')
    spp = Popen(['dot', '-x', '-Tpng'], stdin=pipe, stdout=filepipe)
    spp.wait()


def draw_graph(filename):
    datalog = NamedTemporaryFile('wr', delete=False)
    datalog.write('digraph {\n')
    for task in TaskType.tasks.values():
        for dep in task.dependencys:
            if type(dep) == AlwaysRebuild:
                continue
            dep.write_graph_detailed(datalog)
            datalog.write('"%s" -> "%s" %s;\n' % (dep.name, task.getName(), dep.extra()))
        task.write_graph_detailed(datalog)

    datalog.write('}\n')
    datalog.seek(0)
    run_dot(datalog, filename)


def draw_done_task_graph(filename, tasks):
    def write_task_to_datalog(datalog, task, parent=None):
        if hasattr(task, 'dependencys'):
            for dep in task().dependencys:
                if type(dep) == AlwaysRebuild:
                    continue
                if hasattr(dep, 'parent'):
                    write_task_to_datalog(datalog, dep.parent)
                else:
                    dep.write_graph_detailed(datalog)
                datalog.write('"%s" -> %s %s;\n' % (dep.name, task.getName(), dep.extra()))
        task.write_graph_detailed(datalog)
    #---------------------------------------------------------------------------
    datalog = NamedTemporaryFile('wr', delete=False)
    datalog.write('digraph {\n')
    for task in tasks:
        write_task_to_datalog(datalog, task)

    datalog.write('}\n')
    datalog.seek(0)
    run_dot(datalog, filename)
