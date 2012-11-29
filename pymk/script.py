import os
import sys
import logging
from pymk.task import TASKS
from pymk.error import NoMkfileFound

def run():
    def start_loggin():
        FORMAT = '%(message)s'
        logging.basicConfig(level=logging.INFO, format=FORMAT)
        return logging.getLogger('pymk')
    def append_python_path():
        sys.path.append(os.getcwd())
    def import_mkfile():
        if not os.path.exists('mkfile.py'):
            logger.info("No mkfile.py file found!")
            raise NoMkfileFound()
        import mkfile
    def parse_command():
        if len(sys.argv) == 1:
            text = 'Avalible tasks:\n\t'
            text += '\n\t'.join(TASKS.keys())
            logger.info(text)
        else:
            for task in sys.argv[1:]:
                TASKS[task]().run()
    #---------------------------------------------------------------------------
    try:
        logger = start_loggin()
        append_python_path()
        import_mkfile()
        parse_command()
    except NoMkfileFound:
        return 1
