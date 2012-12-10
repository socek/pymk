import os
import sys
import logging
from pymk.task import TASKS
from pymk.error import NoMkfileFound, CommandError, BadTaskName, WrongArgumentValue
import argparse

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
        return logging.getLogger('pymk')

    def append_python_path():
        sys.path.append(os.getcwd())

    def import_mkfile():
        if not os.path.exists('mkfile.py'):
            print "No mkfile.py file found!"
            raise NoMkfileFound()
        import mkfile

    def run_tasks(args):
        def list_all_tasks():
            text = 'Avalible tasks:\n\t'
            text += '\n\t'.join(TASKS.keys())
            logger.info(text)
        def run_default_task_or_list_all_tasks():
            try:
                import mkfile
                mkfile._DEFAULT.run()
            except AttributeError:
                list_all_tasks()
        def run_all_inputet_tasks():
            for task in args.task:
                try:
                    TASKS[task].run()
                except KeyError:
                    raise BadTaskName(task)
        #-----------------------------------------------------------------------
        if args.all:
            list_all_tasks()
        elif len(args.task) == 0:
            run_default_task_or_list_all_tasks()
        else:
            run_all_inputet_tasks()
    #---------------------------------------------------------------------------
    try:
        append_python_path()
        import_mkfile()
    except NoMkfileFound, er:
        return 1

    try:
        args = parse_command()
        logger = start_loggin(args)
        run_tasks(args)
    except CommandError, er:
        logger.info(er)
        return 2
    except BadTaskName, er:
        logger.info(er)
        return 3
