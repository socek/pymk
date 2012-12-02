import os
import logging
from pymk.error import TaskAlreadyExists

TASKS = {}
logger = logging.getLogger('pymk')

class BaseTask(object):
    conditions = []
    _name = None
    output_file = None

    @classmethod
    def name(cls):
        if cls._name:
            return cls.name
        else:
            return cls.__name__

    @classmethod
    def test_conditions(cls):
        make_rebuild = False
        for condition in cls.conditions:
            cond = condition(cls)
            make_rebuild = make_rebuild or cond
        if make_rebuild:
            return make_rebuild
        else:
            if cls.output_file:
                if not os.path.exists(cls.output_file):
                    return True
                else:
                    return False
            if len(cls.conditions) == 0:
                return True


    @classmethod
    def run(cls, log_uptodate = True):
        if cls.test_conditions():
            logger.info(" * Building '%s'" %(cls.name()))
            cls.build()
            return True
        else:
            if log_uptodate:
                logger.info(" * '%s' is up to date" %(cls.name()))
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
        ret = cls.run(False)
        if cls.output_file:
            from pymk.condition import FileChanged
            return FileChanged(cls.output_file, cls)(task)
        else:
            return ret

def AddTask(cls):
    """
    Adds task to task list."
    """
    name = cls.name()
    if TASKS.has_key(name):
        raise TaskAlreadyExists(name)
    TASKS[name] = cls
    return cls
