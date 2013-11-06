import sys
import argparse
import logging
import os

from pymk import VERSION
from pymk import error
from pymk.extra.cmd import SignalHandling
from pymk.graph import draw_graph
from pymk.recipe import RecipeType
from pymk.task import TaskType


log = logging.getLogger('pymk')


def make_graph(args, is_graphviz):
    from pymk.graph import draw_done_task_graph

    def make_task_list():
        if len(args.task) == 0:
            return False
        else:
            try:
                return [TaskType.tasks[task] for task in args.task]
            except KeyError:
                return False
        return tasks
    #-------------------------------------------------------------------------
    if is_graphviz:
        tasks = make_task_list()

        if tasks:
            draw_done_task_graph(args.graph, tasks)
        else:
            draw_graph(args.graph)
    else:
        log.error('ERROR: No dot executable found!')


def check_for_graphviz(args):
    from pymk.extra import run
    if args.graph:
        try:
            run('which dot')
            return True
        except error.CommandError:
            pass
    return False


def append_python_path(cwd=None):
    if cwd:
        sys.path.append(cwd)
    else:
        sys.path.append(os.getcwd())


def import_mkfile(name='mkfile'):
    if not os.path.exists('%s.py' % (name,)):
        raise error.NoMkfileFound()
    if 'mkfile' in sys.modules:
        module = __import__(name, globals(), locals())
        reload(module)
    else:
        module = __import__(name, globals(), locals())
    return module


def init_recipe(name):
    recipe = RecipeType.getRecipeForModule(name)
    if recipe:
        recipe()
        return True
    return False


def run_all_inputet_tasks(urls, force, dependency_force):
    def gather_tasks(urls):
        tasks = []

        for url in urls:
            tasks.append(TaskType.get_task(url))
        return tasks

    tasks = gather_tasks(urls) #this needs to be 2 phased
    for task in tasks:
        if not task._get_runned():
            task.run(
                force=force,
                dependency_force=dependency_force,
            )
    return 'run tasks'


def run_tasks(mkfile, args):
    def list_all_tasks():
        text = 'Avalible tasks:\n'
        task_names_size = 4
        task_path_size = 4
        for name, task in TaskType.tasks.items():
            if not task.hide:
                if len(task.getName()) > task_names_size:
                    task_names_size = len(task.getName())
                if len(task.getPath()) > task_path_size:
                    task_path_size = len(task.getPath())
        task_names_size += 2
        task_path_size += 2
        template = '  %-' + \
            str(task_names_size) + 's %-' + str(task_path_size) + 's %s\n'
        text += template % ('Name', 'Path', 'Help')
        text += template % ('----', '----', '----')
        for name, task in TaskType.tasks.items():
            if not task.hide:
                text += template % (
                    task.getName(),
                    task.getPath(),
                    task.help,
                )

        log.info(text)
        return 'list all'

    def run_default_task_or_list_all_tasks():
        try:
            if args.graph:
                return 'do graph of all'
            else:
                recipe = RecipeType.getRecipeForModule('mkfile')
                task = recipe().getDefaultTask()
                task.run(
                    force=args.force, dependency_force=args.dependency_force)
                return 'run default'
        except (AttributeError, TypeError):
            return list_all_tasks()
    #-----------------------------------------------------------------------
    if args.all:
        return list_all_tasks()
    elif len(args.task) == 0:
        return run_default_task_or_list_all_tasks()
    else:
        return run_all_inputet_tasks(
            args.task,
            args.force,
            args.dependency_force
        )


def show_tasks_paths(arg_path):
    for name, task in TaskType.tasks.items():
        if task.getPath().startswith(arg_path):
            print task.getPath()


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
                            help='Set log level from "debug" or "info".')
        parser.add_argument('-a', '--all', dest='all', action='store_true',
                            help='Show all tasks avalible.')
        parser.add_argument('-f', '--force', dest='force', action='store_true',
                            help='Force task to rebuild.')
        parser.add_argument('-g', '--graph', dest='graph',
                            help='Draw a graph of tasks to a file.')
        parser.add_argument('-p', '--paths', dest='paths', const='', nargs='?',
                            help='Show tasks paths')
        parser.add_argument(
            '-v', '--version', dest='version', action='store_true',
            help='Show version of pymk.')
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
            raise error.WrongArgumentValue(
                'Wrong argument for log! Avalible are: "debug" and "info".')
    #-------------------------------------------------------------------------

    try:
        SignalHandling()
        args = parse_command()
        if args.version:
            args.log = 'info'
            start_loggin(args)
            log.info('Pymk version %s' % (VERSION,))
            return 0
        else:
            start_loggin(args)
            append_python_path()
            module = import_mkfile('mkfile')
            init_recipe('mkfile')
            is_graphviz = check_for_graphviz(args)
    except error.NoMkfileFound as er:
        log.error("No mkfile.py file found!")
        return 1
    except error.NotADependencyError as er:
        log.error(er)
        return 7

    if args.paths is not None:
        start_loggin(args)
        show_tasks_paths(args.paths)
        return 0
    else:
        try:
            run_tasks(module, args)
        except error.CommandError as er:
            log.error(er)
            return 2
        except error.BadTaskPath as er:
            log.error(er)
            return 3
        except error.TaskMustHaveOutputFile as er:
            log.error(er)
            return 4
        except error.CouldNotCreateFile as er:
            log.error(er)
            return 5
        except (KeyboardInterrupt, error.CommandAborted) as er:
            log.error('\rCommand aborted!')
            return 6
        finally:
            if args.graph:
                make_graph(args, is_graphviz)

if __name__ == '__main__':
    run()
