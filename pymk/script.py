import os
import sys
import logging
from pymk.task import TaskMeta
from pymk.error import NoMkfileFound, CommandError, BadTaskName, WrongArgumentValue, TaskMustHaveOutputFile, CouldNotCreateFile, NotADependencyError
from pymk.graph import draw_graph
from pymk.extra import run_cmd
import argparse
from urlparse import urlparse, parse_qs


log = logging.getLogger('pymk')


def make_graph(args, is_graphviz):
    from pymk.graph import draw_done_task_graph

    def make_task_list():
        if len(args.task) == 0:
            return False
        else:
            try:
                return [TaskMeta.tasks[task] for task in args.task]
            except KeyError:
                return False
        return tasks
    #---------------------------------------------------------------------------
    if is_graphviz:
        tasks = make_task_list()

        if tasks:
            draw_done_task_graph(args.graph, tasks)
        else:
            draw_graph(args.graph)
    else:
        log.error('ERROR: No dot executable found!')


def check_for_graphviz(args):
    if args.graph:
        try:
            run_cmd('which dot')
            return True
        except CommandError:
            pass
    return False


def append_python_path(cwd=None):
    if cwd:
        sys.path.append(cwd)
    else:
        sys.path.append(os.getcwd())


def import_mkfile():
    if not os.path.exists('mkfile.py'):
        raise NoMkfileFound()
    if 'mkfile' in sys.modules:
        module = __import__("mkfile", globals(), locals())
        reload(module)
    else:
        module = __import__("mkfile", globals(), locals())
    return module

def parse_task_name(task):
    url = urlparse(task)
    name = url.path
    args = parse_qs(url.query)
    return name, args

def run_all_inputet_tasks(tasks, force, dependency_force):
    def check_if_task_name_exists(name):
        if not name in TaskMeta.tasks:
            raise BadTaskName(task)
    def run_task(name, force, dependency_force):
        get_task(name).run(
            force=force,
            dependency_force=dependency_force,
        )
    def get_task(name):
        return TaskMeta.tasks[name]
    #---------------------------------------------------------------------------
    tasks = [ parse_task_name(task) for task in tasks ]
    #First check all tasks names, then run tasks.
    for name, args in tasks:
        check_if_task_name_exists(name)
        get_task(name)._args = args

    for name, args in tasks:
        if not get_task(name)._get_runned():
            run_task(name, force, dependency_force)
    return 'run tasks'


def run_tasks(mkfile, args):
    def list_all_tasks():
        text = 'Avalible tasks:\n'
        task_names_size = 0
        for name, task in TaskMeta.tasks.items():
            if not task.hide:
                if len(name) > task_names_size:
                    task_names_size = len(name)
        task_names_size += 2
        template = '\t%-' + str(task_names_size) + 's %s\n'
        for name, task in TaskMeta.tasks.items():
            if not task.hide:
                text += template % (task.getName(), task.help)

        log.info(text)
        return 'list all'

    def run_default_task_or_list_all_tasks():
        try:
            if args.graph:
                return 'do graph of all'
            else:
                mkfile.SETTINGS['default task'].run(force=args.force,
                                                    dependency_force=args.dependency_force)
                return 'run default'
        except (AttributeError, KeyError):
            return list_all_tasks()
    #-----------------------------------------------------------------------
    if args.all:
        return list_all_tasks()
    elif len(args.task) == 0:
        return run_default_task_or_list_all_tasks()
    else:
        return run_all_inputet_tasks(args.task, args.force, args.dependency_force)


def run():
    """run() -> error code
    Parse command line args and do the task provided. More info with inputing "pymk -h"

    @return:
     1. no mkfile.py found or it is corrupted
     2. error in external program
     3. wrong task name
     4. provided task has no output_file, which is needed becouse of dependencys
     5. could not create a file that is in depedency
     6. command aborted (by keyboard)
    """
    def parse_command():
        parser = argparse.ArgumentParser()
        parser.add_argument('task', nargs='*',
                            help='List of task to do.')
        parser.add_argument('-l', '--log', dest='log', default='info',
                            help='Ser log level from "debug" or "info".')
        parser.add_argument('-a', '--all', dest='all', action='store_true',
                            help='Show all tasks avalible.')
        parser.add_argument('-f', '--force', dest='force', action='store_true',
                            help='Force task to rebuild.')
        parser.add_argument('-g', '--graph', dest='graph',
                            help='Draw a graph of tasks to a file.')
        parser.add_argument(
            '-d', '--dependency-force', dest='dependency_force', action='store_true',
            help='Force depedency to rebuild (use only with --force).')
        return parser.parse_args()

    def start_loggin(args):
        FORMAT = '%(message)s'
        if args.log == 'debug':
            logging.basicConfig(level=logging.DEBUG, format=FORMAT)
        elif args.log == 'info':
            logging.basicConfig(level=logging.INFO, format=FORMAT)
        else:
            raise WrongArgumentValue(
                'Wrong argument for log! Avalible are: "debug" and "info".')
    #-------------------------------------------------------------------------

    try:
        args = parse_command()
        start_loggin(args)
        append_python_path()
        module = import_mkfile()
        is_graphviz = check_for_graphviz(args)
    except NoMkfileFound as er:
        log.error("No mkfile.py file found!")
        return 1
    except NotADependencyError as er:
        log.error(er)
        return 7

    try:
        run_tasks(module, args)
    except CommandError as er:
        log.error(er)
        return 2
    except BadTaskName as er:
        log.error(er)
        return 3
    except TaskMustHaveOutputFile as er:
        log.error(er)
        return 4
    except CouldNotCreateFile as er:
        log.error(er)
        return 5
    except KeyboardInterrupt:
        log.error('\rCommand aborted!')
        return 6
    finally:
        if args.graph:
            make_graph(args, is_graphviz)
