import os
import logging
from pymk.error import TaskAlreadyExists, NoDependencysInAClass, NotADependencyError
from pymk.dependency import InnerFileExists, InnerFileChanged, AlwaysRebuild, BaseDependency

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
                for dependency in subcls.dependencys:
                    if not issubclass(type(dependency), BaseDependency):
                        raise NotADependencyError(dependency, subcls)

    @classmethod
    def init(cls):
        """Init new task collection."""
        cls.TASKS = {}


class BaseTask(object):
    """Base of all taks."""
    dependencys = None
    _name = None
    output_file = None
    detailed = []
    _runned = {}
    help = ''

    @classmethod
    def name(cls):
        """name() -> str
        Returns name of the tasks provided by class value _name, or just classname if _name == None.
        """
        return cls.__name__

    @classmethod
    def _set_runned(cls, value):
        cls._runned[cls.__name__] = value
        return cls._runned[cls.__name__]

    @classmethod
    def _get_runned(cls):
        try:
            return cls._runned[cls.__name__]
        except KeyError:
            return False

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
                return cls._set_runned(True)
        else:
            if log_uptodate:
                logger.info(" * '%s' is up to date" % (cls.name()))
            return cls._set_runned(False)

    @classmethod
    def build(cls):
        """build() -> None
        What to do with this task to rebuild it. This method needs to be reimplemented after inheriting.
        """

    @classmethod
    def dependency_FileExists(cls):
        """dependency_FileExists(cls) -> bool
        Dependency that will run this task if not crated before.
        """
        return InnerFileExists(cls)

    @classmethod
    def dependency_FileChanged(cls):
        """dependency_FileChanged(cls, task) -> bool
        Dependency that will run this task if nessesery and return True if file is newwer then task.output_file.
        """
        return InnerFileChanged(cls)

    # -- graph specyfic --
    @classmethod
    def write_graph_detailed(cls, datalog):
        if not cls.name in cls.detailed:
            cls.detailed.append(cls.name())
            datalog.write('"%s" [%s];\n' % (cls.name(), cls.get_graph_details()))

    @classmethod
    def get_graph_details(cls):
        shape = 'box'
        color = 'white'
        if AlwaysRebuild in [type(dependency) for dependency in cls.dependencys]:
            shape = 'circle'
            color = 'grey'
        if cls._get_runned():
            color = 'red'

        return 'shape=%s, regular=1,style=filled,fillcolor=%s' % (shape, color)


def AddTask(cls):
    """
    Decorator that adds task to task list.
    """
    name = cls.name()
    if name in TaskData.TASKS:
        raise TaskAlreadyExists(name)
    TaskData.TASKS[name] = cls
    return cls
