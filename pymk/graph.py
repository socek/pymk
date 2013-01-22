from pymk.task import TaskData
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
    for task in TaskData._all_tasks:
        for dep in task.dependencys:
            dep.write_graph_detailed(datalog)
            datalog.write('"%s" -> %s %s;\n' % (dep.name, task.name(), dep.extra))
        task.write_graph_detailed(datalog)

    datalog.write('}\n')
    print datalog.name
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
            # if data['runned']:
                # depShow._details = depShow._details.replace('white', 'red')
                # depShow.extra = depShow.extra.replace(']', ',color=red]')
            data['data'].write_graph_detailed(datalog)
            if parent_data:
                datalog.write('"%s" -> %s %s;\n' % (data['data'].name, parent_data.name, data['data'].extra))

    datalog.write('digraph {\n')
    for task_data in running_list:
        print_data(task_data)

    datalog.write('}\n')
    datalog.seek(0)
    run_dot(datalog, filename)
