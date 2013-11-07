import logging
import os
from urlparse import urlparse, parse_qs

from pymk.dependency import InnerFileExists, InnerFileChanged, AlwaysRebuild
from pymk.dependency import Dependency, InnerLink
from pymk.error import TaskAlreadyExists, NoDependencysInAClass
from pymk.error import NotADependencyError, BadTaskPath


logger = logging.getLogger('pymk')


class _GetTask(object):

    def __init__(self, url):
        self.url = url

    def parse_url(self):
        url = urlparse(self.url)
        path = url.path
        args = parse_qs(url.query)
        return path, args

    def check_if_task_name_exists(self, path):
        if not path in TaskType.tasks:
            raise BadTaskPath(path)

    def get_task(self, path):
        return TaskType.tasks[path]

    def __call__(self):
        path, args = self.parse_url()
        self.check_if_task_name_exists(path)
        task = self.get_task(path)
        task._args = args
        return task


class TaskType(type):
    tasks = {}
    args = {}
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if getattr(cls, '_no_singleton', False):
            return super(TaskType, cls).__call__(*args, **kwargs)
        if cls not in cls._instances:
            cls._instances[cls] = super(
                TaskType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def check_if_task_exists(cls, name):
        if name in list(cls.tasks):
            raise TaskAlreadyExists(name)

    @classmethod
    def assign_recipe_if_able(basecls, cls):
        from pymk.recipe import RecipeType
        recipe = RecipeType.getRecipeForModule(cls.__module__)
        if recipe:
            cls.assign_recipe(recipe)

    @classmethod
    def get_task(self, url):
        return _GetTask(url)()

    def __init__(cls, name, bases, dct):
        def validate_dependency(cls):
            if cls.dependencys is None:
                raise NoDependencysInAClass(cls)
            if cls.recipe is None:
                for dependency in cls().dependencys:
                    if not issubclass(type(dependency), Dependency):
                        raise NotADependencyError(dependency, cls)
        #----------------------------------------------------------------------
        if not 'base' in dct or not dct['base']:
            TaskType.assign_recipe_if_able(cls)
            TaskType.check_if_task_exists(cls().getPath())
            TaskType.tasks[cls().getPath()] = cls
            cls.base = False
            validate_dependency(cls)

    @classmethod
    def init(cls):
        """Init new task collection."""
        cls.tasks = {}
        cls.args = {}


class Task(object):

    """Base of all taks."""

    base = True

    __metaclass__ = TaskType

    dependencys = None
    output_file = None
    help = ''
    hide = False
    hide_graph = False

    name = None
    path = None
    detailed = []
    _runned = False
    _args = {}
    _error = False
    recipe = None

    @classmethod
    def getName(cls):
        """getName() -> str
        Returns name of the tasks provided by class value name, or just
        classname if name == None.
        """
        if cls.name:
            return cls.name
        else:
            return cls.__name__

    @classmethod
    def getPath(cls):
        """getPath(cls) -> str
        Returns path (for using in command line) of the tasks provided by class
        value path, or just classname if path == None.
        """
        if cls.path:
            return cls.path
        else:
            return '/' + cls.__name__.lower()

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
        for dependency in cls().dependencys:
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
            if cls().output_file:
                if not os.path.exists(cls().output_file):
                    return True
                else:
                    return False
            if len(cls().dependencys) == 0:
                return True
            return False

    @classmethod
    def run(cls,
            log_uptodate=True,
            force=False,
            dependency_force=False,
            parent=None):
        """run(log_uptodate = True): -> bool
        Test dependency of this task, and rebuild it if nessesery.
        """
        def build_with_args_or_not(cls):
            try:
                cls().build(cls._args)
            except TypeError:
                cls().build()
        #----------------------------------------------------------------------
        cls.running_list_element = {
            'type': 'task',
            'data': cls,
            'runned': None,
            'childs': [],
        }
        if parent:
            parent.running_list_element[
                'childs'].append(cls.running_list_element)
        else:
            from pymk.graph import running_list
            running_list.append(cls.running_list_element)
        if cls.test_dependencys(force and dependency_force) or force:
            logger.info(" * Building '%s'" % (cls.getName()))
            try:
                build_with_args_or_not(cls)
            except Exception:
                cls._error = True
                raise
            finally:
                runned = cls._set_runned(True)
            return runned
        else:
            if log_uptodate:
                logger.info(" * '%s' is up to date" % (cls.getName()))
            return cls._set_runned(False)

    @classmethod
    def assign_recipe(cls, recipe):
        cls.recipe = recipe

    @property
    def settings(self):
        return self.recipe().settings

    @property
    def paths(self):
        return self.recipe().paths

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
            datalog.write('"%s" [%s];\n' %
                          (cls.getName(), cls.get_graph_details()))

    @classmethod
    def get_graph_details(cls):
        shape = 'box'
        color = 'white'
        types = [type(dependency) for dependency in cls().dependencys]
        if AlwaysRebuild in types:
            shape = 'circle'
            color = 'grey'
        if cls._get_runned():
            color = 'green'
        if cls._error:
            color = 'red'

        return 'shape=%s, regular=1,style=filled,fillcolor=%s' % (shape, color)

    def get_task(self, url):
        return TaskType.get_task(url)
