import os
import logging
from pymk.error import TaskAlreadyExists, NoDependencysInAClass, NotADependencyError
from pymk.dependency import InnerFileExists, InnerFileChanged, AlwaysRebuild, Dependency, InnerLink

logger = logging.getLogger('pymk')


class TaskMeta(type):
    tasks = {}
    args = {}
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(TaskMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def __init__(cls, name, bases, dct):
        def check_if_task_exists(name):
            if name in list(TaskMeta.tasks):
                raise TaskAlreadyExists(name)

        def validate_dependency(cls):
            if cls.dependencys == None:
                raise NoDependencysInAClass(cls)
            for dependency in cls.dependencys:
                if not issubclass(type(dependency), Dependency):
                    raise NotADependencyError(dependency, cls)
        #-----------------------------------------------------------------------
        if name != 'Task':
            check_if_task_exists(name)
            TaskMeta.tasks[cls().getName()] = cls
            validate_dependency(cls)

    @classmethod
    def init(cls):
        """Init new task collection."""
        cls.tasks = {}
        cls.args = {}


class Task(object):

    """Base of all taks."""

    __metaclass__ = TaskMeta

    dependencys = None
    output_file = None
    help = ''
    hide = False
    hide_graph = False

    name = None
    detailed = []
    _runned = False
    _args = {}
    _error = False

    @classmethod
    def getName(cls):
        """getName() -> str
        Returns name of the tasks provided by class value _name, or just classname if _name == None.
        """
        if cls.name:
            return cls.name
        else:
            return cls.__name__

    @classmethod
    def _set_runned(cls, value):
        cls._runned = value
        return cls._runned

    @classmethod
    def _get_runned(cls):
        try:
            return cls._runned
        except KeyError:
            return False

    @classmethod
    def test_dependencys(cls, dependency_force=False):
        """test_dependencys() -> bool

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
        def build_with_args_or_not(cls):
            try:
                cls().build(cls._args)
            except TypeError:
                cls().build()
        #-----------------------------------------------------------------------
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
            logger.info(" * Building '%s'" % (cls.getName()))
            try:
                build_with_args_or_not(cls)
            except Exception as er:
                cls._error = True
                raise er
            finally:
                runned = cls._set_runned(True)
            return runned
        else:
            if log_uptodate:
                logger.info(" * '%s' is up to date" % (cls.getName()))
            return cls._set_runned(False)

    @classmethod
    def dependency_FileExists(cls):
        return InnerFileExists(cls)

    @classmethod
    def dependency_FileChanged(cls):
        return InnerFileChanged(cls)

    @classmethod
    def dependency_Link(cls):
        return InnerLink(cls)

    # -- graph specyfic --
    @classmethod
    def write_graph_detailed(cls, datalog):
        if not cls.hide_graph and not cls.name in cls.detailed:
            cls.detailed.append(cls.getName())
            datalog.write('"%s" [%s];\n' % (cls.getName(), cls.get_graph_details()))

    @classmethod
    def get_graph_details(cls):
        shape = 'box'
        color = 'white'
        if AlwaysRebuild in [type(dependency) for dependency in cls.dependencys]:
            shape = 'circle'
            color = 'grey'
        if cls._get_runned():
            color = 'green'
        if cls._error:
            color = 'red'

        return 'shape=%s, regular=1,style=filled,fillcolor=%s' % (shape, color)
