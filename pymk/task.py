import os
import logging
from pymk.error import TaskAlreadyExists, TaskMustHaveOutputFile

logger = logging.getLogger('pymk')

class TaskData(object):
    """Info about collected tasks."""
    TASKS = None

    @classmethod
    def init(cls):
        """Init new task collection."""
        cls.TASKS = {}

class BaseTask(object):
    """Base of all taks."""
    dependencys = []
    _name = None
    output_file = None

    @classmethod
    def name(cls):
        """name() -> str
        Returns name of the tasks provided by class value _name, or just classname if _name == None.
        """
        if cls._name:
            return cls._name
        else:
            return cls.__name__

    @classmethod
    def test_dependencys(cls):
        """test_dependencys() -> bool
        Test all dependency of the task and rebuild the dependency tasks.
        Return True if this task needs to be rebuilded.
        """
        make_rebuild = False
        for dependency in cls.dependencys:
            cond = dependency(cls)
            make_rebuild = make_rebuild or cond
        if make_rebuild:
            return make_rebuild
        else:
            if cls.output_file:
                if not os.path.exists(cls.output_file):
                    return True
                else:
                    return False
            if len(cls.dependencys) == 0:
                return True
            return False


    @classmethod
    def run(cls, log_uptodate=True, force=False):
        """run(log_uptodate = True): -> bool
        Test dependency of this task, and rebuild it if nessesery.
        """
        if force or cls.test_dependencys():
            logger.info(" * Building '%s'" %(cls.name()))
            cls.build()
            return True
        else:
            if log_uptodate:
                logger.info(" * '%s' is up to date" %(cls.name()))
            return False

    @classmethod
    def build(cls):
        """build() -> None
        What to do with this task to rebuild it. This method needs to be reimplemented after inheriting.
        """

    @classmethod
    def dependency_FileExists(cls, task):
        """dependency_FileExists(cls, task) -> bool
        Dependency that will run this task if not crated before.
        """
        if cls.output_file:
            if os.path.exists(cls.output_file):
                cls.run(False)
                return False
            else:
                cls.run()
                return True
        else:
            raise TaskMustHaveOutputFile(cls.name())

    @classmethod
    def dependency_FileChanged(cls, task):
        """dependency_FileChanged(cls, task) -> bool
        Dependency that will run this task if nessesery and return True if file is newwer then task.output_file.
        """
        ret = cls.run(False)
        from pymk.dependency import FileChanged
        return FileChanged(cls.output_file, cls)(task) or ret

def AddTask(cls):
    """
    Decorator that adds task to task list.
    """
    name = cls.name()
    if name in TaskData.TASKS:
        raise TaskAlreadyExists(name)
    TaskData.TASKS[name] = cls
    return cls
