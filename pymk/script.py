import os
import sys
import logging
from pymk.task import TASKS
from pymk.error import NoMkfileFound, CommandError, BadTaskName

def run():
    cmd = {
        'tasks' : [],
        'options' : [],
    }
    def parse_command():
        for element in sys.argv[1:]:
            if element.startswith('-'):
                cmd['options'].append(element[1:])
            else:
                cmd['tasks'].append(element)
    def start_loggin():
        FORMAT = '%(message)s'
        if 'd' in cmd['options']:
            logging.basicConfig(level=logging.DEBUG, format=FORMAT)
        else:
            logging.basicConfig(level=logging.INFO, format=FORMAT)
        return logging.getLogger('pymk')
    def append_python_path():
        sys.path.append(os.getcwd())
    def import_mkfile():
        if not os.path.exists('mkfile.py'):
            logger.info("No mkfile.py file found!")
            raise NoMkfileFound()
        import mkfile
    def run_tasks():
        if len(sys.argv) == 1:
            text = 'Avalible tasks:\n\t'
            text += '\n\t'.join(TASKS.keys())
            logger.info(text)
        else:
            for task in cmd['tasks']:
                try:
                    TASKS[task]().run()
                except KeyError:
                    raise BadTaskName(task)
    #---------------------------------------------------------------------------
    try:
        parse_command()
        logger = start_loggin()
        append_python_path()
        import_mkfile()
        run_tasks()
    except NoMkfileFound, er:
        logger.info(er)
        return 1
    except CommandError, er:
        logger.info(er)
        return 2
    except BadTaskName, er:
        logger.info(er)
        return 3
