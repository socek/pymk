import os
import logging
from pymk.error import TaskAlreadyExists

TASKS = {}
logger = logging.getLogger('pymk')

class BaseTask(object):
    conditions = []
    name = None
    output_file = None

    @classmethod
    def test_conditions(cls):
        make_rebuild = True
        if cls.output_file:
            if not os.path.exists(cls.output_file):
                return True
        for condition in cls.conditions:
            make_rebuild = condition(cls)
            if make_rebuild:
                break
        return make_rebuild

    @classmethod
    def run(cls):
        if cls.test_conditions():
            logger.info(" * Building '%s'" %(cls.name))
            cls.build()
            return True
        else:
            logger.info(" * '%s' is up to date" %(cls.name))
            return False

    @classmethod
    def build(cls):
        pass

    @classmethod
    def condition_FileExists(cls, task):
        if cls.output_file:
            if os.path.exists(cls.output_file):
                return False
            else:
                cls.run()
                return True
        else:
            cls.run()
            return True

    @classmethod
    def condition_FileChanged(cls, task):
        if cls.output_file:
            from pymk.condition import FileChanged
            return FileChanged(cls.output_file, cls)(task)
        else:
            cls.run()
            return True

def AddTask(cls):
    """
    Adds task to task list."
    """
    if cls.name:
        name = cls.name
    else:
        name = cls.__name__
    if TASKS.has_key(name):
        raise TaskAlreadyExists(name)
    TASKS[name] = cls
    return cls
