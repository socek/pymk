class PymkError(Exception):
    """Base exception for pymk. Do nothing special.
    """


class CouldNotCreateFile(PymkError):
    """Raised when there is a file in dependency, but mkfile do not defines how to build it."""
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return 'Error: Could not create file %s' % (self.filename)


class TaskAlreadyExists(PymkError):
    """Raised when task of that name already exits. Tasks can not be ovverided."""
    def __init__(self, task_name):
        self.task_name = task_name

    def __str__(self):
        return 'Error: Task name already exists "%s".' % (self.task_name)


class NoMkfileFound(PymkError):
    """Raised when the folder in which pymk was used do not have mkfile.py"""


class CommandError(PymkError):
    """Raised when external command returns error."""
    def __init__(self, number, text):
        self.number = number
        self.text = text

    def __str__(self):
        return 'Error: Command error (%d): %s' % (self.number, self.text)


class BadTaskName(PymkError):
    """Raised when inputed task name do not exists in mkfile (or was not add as a task with @AddTask)"""
    def __init__(self, taskname):
        self.taskname = taskname

    def __str__(self):
        return 'Error: Bad task name: %s' % (self.taskname)


class WrongArgumentValue(PymkError):
    """Raised when argument has a list of values, but inputet value is not in this list."""
    def __init__(self, description):
        self.description = description


class TaskMustHaveOutputFile(PymkError):
    """Raised when task has no output_file setted, but the dependency assigned to
    that task (or to task that this task is assigned as dependency) need this value."""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Error: Taks must have output_file setted: %s' % (self.name)


class NoDependencysInAClass(PymkError):
    """NoDependencysInAClass is raised when no depedencys attribute was provided,
    or this attribute has wrong name."""
    def __init__(self, cls):
        self.cls = cls

    def __str__(self):
        return 'Error: Class %s has no "dependencys" attribute or it has wrong name.' % (self.cls.__name__)


class NotADependencyError(PymkError):
    """NotADependencyError is raised when some object in dependency list are not
    an object inherited from pymk.dependency.Dependency."""

    def __init__(self, dependency, task):
        self.dependency = dependency
        self.task = task

    def __str__(self):
        return 'Error: Object "%s" of a task "%s" is not a dependency!' % (str(self.dependency.__name__), self.task.__name__)
