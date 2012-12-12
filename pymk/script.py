import os
import sys
import logging
from pymk.task import TaskData
from pymk.error import NoMkfileFound, CommandError, BadTaskName, WrongArgumentValue
import argparse

log = logging.getLogger('pymk')

def append_python_path(cwd = None):
    """append_python_path(cwd) -> None
    Append provided (or actual cwd if not provided) path to python path.
    """
    if cwd:
        sys.path.append(cwd)
    else:
        sys.path.append(os.getcwd())

def import_mkfile():
    if not os.path.exists('mkfile.py'):
        log.error("No mkfile.py file found!")
        raise NoMkfileFound()
    if 'mkfile' in sys.modules:
        module = __import__("mkfile", globals(), locals())
        reload(module)
    else:
        module = __import__("mkfile", globals(), locals())
    return module

def run_tasks(mkfile, args):
    def list_all_tasks():
        text = 'Avalible tasks:\n\t'
        text += '\n\t'.join(TaskData.TASKS.keys())
        log.info(text)
        return 'list all'
    def run_default_task_or_list_all_tasks():
        try:
            mkfile._DEFAULT.run()
            return 'run default'
        except AttributeError:
            return list_all_tasks()
    def run_all_inputet_tasks():
        for task in args.task:
            try:
                TaskData.TASKS[task].run()
            except KeyError:
                raise BadTaskName(task)
        return 'run tasks'
    #-----------------------------------------------------------------------
    if args.all:
        return list_all_tasks()
    elif len(args.task) == 0:
        return run_default_task_or_list_all_tasks()
    else:
        return run_all_inputet_tasks()

def run():
    """run() -> error code
    Parse command line args and do the task provided. More info with inputing "pymk -h"

    @return:
     1. no mkfile.py found or it is corrupted
     2. error in external program
     3. wrong task name
    """
    def parse_command():
        parser = argparse.ArgumentParser()
        parser.add_argument('task', nargs='*',
                            help='List of task to do.')
        parser.add_argument('-l', '--log', dest='log', default='info',
                            help='Ser log level from "debug" or "info".')
        parser.add_argument('-a', '--all', dest='all', action='store_true',
                            help='Show all tasks avalible.')
        return parser.parse_args()

    def start_loggin(args):
        FORMAT = '%(message)s'
        if args.log == 'debug':
            logging.basicConfig(level=logging.DEBUG, format=FORMAT)
        elif args.log == 'info':
            logging.basicConfig(level=logging.INFO, format=FORMAT)
        else:
            raise WrongArgumentValue('Wrong argument for log! Avalible are: "debug" and "info".')
    #---------------------------------------------------------------------------
    try:
        args = parse_command()
        start_loggin(args)
        append_python_path()
        TaskData.init()
        module = import_mkfile()
    except NoMkfileFound, er:
        return 1

    try:
        run_tasks(module, args)
    except CommandError, er:
        log.info(er)
        return 2
    except BadTaskName, er:
        log.info(er)
        return 3
