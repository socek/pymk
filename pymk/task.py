import os
import logging
from pymk.error import TaskAlreadyExists, TaskMustHaveOutputFile, NoDependencysInAClass

logger = logging.getLogger('pymk')


class TaskData(object):
    """Info about collected tasks."""
    TASKS = None
    _all_tasks = []

    @classmethod
    def initTasks(cls):
        for subcls in BaseTask.__subclasses__():
            if not subcls in cls._all_tasks:
                cls._all_tasks.append(subcls)
                if subcls.dependencys == None:
                    raise NoDependencysInAClass(subcls)

    @classmethod
    def init(cls):
        """Init new task collection."""
        cls.TASKS = {}


class BaseTask(object):
    """Base of all taks."""
    dependencys = None
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
    def test_dependencys(cls, dependency_force=False):
        """test_dependencys() -> bool
        Test all dependency of the task and rebuild the dependency tasks.
        Return True if this task needs to be rebuilded.
        """
        make_rebuild = False
        for dependency in cls.dependencys:
            cond = dependency(cls, dependency_force=dependency_force)
            make_rebuild = make_rebuild or cond
            cls.running_list_element['childs'].append({
                'type': 'dependency',
                'data': dependency,
                'runned': cond,
                'childs': [],
            })
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
    def run(cls, log_uptodate=True, force=False, dependency_force=False, parent=None):
        """run(log_uptodate = True): -> bool
        Test dependency of this task, and rebuild it if nessesery.
        """
        cls.running_list_element = {
            'type': 'task',
            'data': cls,
            'runned': None,
            'childs': [],
        }
        if parent:
            parent.running_list_element['childs'].append(cls.running_list_element)
        else:
            from pymk.graph import running_list
            running_list.append(cls.running_list_element)
        if cls.test_dependencys(force and dependency_force) or force:
            logger.info(" * Building '%s'" % (cls.name()))
            try:
                cls().build()
            finally:
                cls.running_list_element['runned'] = True
            return True
        else:
            if log_uptodate:
                logger.info(" * '%s' is up to date" % (cls.name()))
            cls.running_list_element['runned'] = False
            return False

    @classmethod
    def build(cls):
        """build() -> None
        What to do with this task to rebuild it. This method needs to be reimplemented after inheriting.
        """

    @classmethod
    def dependency_FileExists(cls, task, dependency_force=False):
        """dependency_FileExists(cls, task) -> bool
        Dependency that will run this task if not crated before.
        """
        if dependency_force:
            cls.run(True, True, True, task)
            return True
        if cls.output_file:
            if os.path.exists(cls.output_file):
                cls.run(False, parent=task)
                return False
            else:
                cls.run(parent=task)
                return True
        else:
            raise TaskMustHaveOutputFile(cls.name())

    @classmethod
    def dependency_FileChanged(cls, task, dependency_force=False):
        """dependency_FileChanged(cls, task) -> bool
        Dependency that will run this task if nessesery and return True if file is newwer then task.output_file.
        """
        if dependency_force:
            cls.run(True, True, True, parent=task)
        ret = cls.run(False, parent=task)
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
