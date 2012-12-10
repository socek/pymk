Introduction
============

pymk is a script that provides the sam functionality that "makefile" does, but
make the "makefile" (mkfile.py) in python. Code of mkfile.py is cleared, and it
can do more things (like check all files from all folders and subfolders named
"migrations").

Example
=======
from pymk.task import BaseTask, AddTask
from pymk.condition import FileChanged, FileDoesNotExists
from pymk.extra import find_files, run_cmd, touch
import os
import sys
from shutil import rmtree
import logging
logger = logging.getLogger('pymk')

@AddTask
class clear(BaseTask):

    @classmethod
    def build(cls):
        for filename in find_files('src', '*.pyc'):
            os.unlink(filename)
            logger.debug('Deleted: %s' %(filename,))

class bootstrap(BaseTask):
    output_file = 'bin/buildout'

    @classmethod
    def build(cls):
        run_cmd(['./bin/buildout'], True)

@AddTask
class buildout(BaseTask):
    output_file = 'bin/py'

    conditions = [
        bootstrap.condition_FileChanged,
        FileChanged('src/setup.py'),
    ]

    @classmethod
    def build(cls):
        run_cmd(['./bin/buildout'], True)
        touch('./bin/py')

@AddTask
class player(BaseTask):
    conditions = [buildout.condition_FileChanged]

    @classmethod
    def build(cls):
        run_cmd(['./bin/player --debug'], True)

@AddTask
class client(BaseTask):
    conditions = [buildout.condition_FileChanged]

    @classmethod
    def build(cls):
        run_cmd(['./bin/client'], True)

@AddTask
class cleardb(BaseTask):
    @classmethod
    def build(cls):
        from glob import glob
        for egg in glob('eggs/*'):
            sys.path.append(egg)
        from src.paramba.lib.config import start_configs, PATHS
        start_configs()
        rmtree(PATHS['db'])
