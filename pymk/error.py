class PymkError(Exception):
    """Base exception for pymk. Do nothing special.
    """

class CouldNotCreateFile(PymkError):
    """Raised when there is a file in dependency, but mkfile do not defines how to build it."""
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return 'Could not create file %s' %(self.filename)

class TaskAlreadyExists(PymkError):
    """Raised when task of that name already exits. Tasks can not be ovverided."""
    def __init__(self, task_name):
        self.task_name = task_name

    def __str__(self):
        return 'Task name already exists "%s".' %(self.task_name)

class NoMkfileFound(PymkError):
    """Raised when the folder in which pymk was used do not have mkfile.py"""

class CommandError(PymkError):
    """Raised when external command returns error."""
    def __init__(self, number, text):
        self.number = number
        self.text = text

    def __str__(self):
        return 'Command error (%d): %s' %(self.number, self.text)

class BadTaskName(PymkError):
    """Raised when inputed task name do not exists in mkfile (or was not add as a task with @AddTask)"""
    def __init__(self, taskname):
        self.taskname = taskname

    def __str__(self):
        return 'Bad task name: %s' %(self.taskname)

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
        return 'Taks must have output_file setted: %s' %(self.name)
