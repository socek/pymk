class PymkError(Exception):

    """Base exception for pymk. Do nothing special.
    """


class CouldNotCreateFile(PymkError):

    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return 'Error: Could not create file %s' % (self.filename)


class TaskAlreadyExists(PymkError):

    def __init__(self, task_name):
        self.task_name = task_name

    def __str__(self):
        return 'Error: Task name already exists "%s".' % (self.task_name)


class RecipeAlreadyExists(PymkError):

    def __init__(self, recipe_name):
        self.recipe_name = recipe_name

    def __str__(self):
        return 'Error: Recipe name already exists "%s".' % (self.recipe_name)


class NoMkfileFound(PymkError):
    pass


class CommandError(PymkError):

    def __init__(self, number, text):
        self.number = number
        self.text = text

    def __str__(self):
        return 'Error: Command error (%d): %s' % (self.number, self.text)


class CommandAborted(PymkError):
    pass


class BadTaskPath(PymkError):

    def __init__(self, taskpath):
        self.taskpath = taskpath

    def __str__(self):
        return 'Error: Bad task path: %s' % (self.taskpath)


class WrongArgumentValue(PymkError):

    def __init__(self, description):
        self.description = description


class TaskMustHaveOutputFile(PymkError):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Error: Taks must have output_file setted: %s' % (self.name)


class NoDependencysInAClass(PymkError):

    def __init__(self, cls):
        self.cls = cls

    def __str__(self):
        return 'Error: Class %s has no "dependencys" attribute or it has wrong name.' % (self.cls.__name__)


class NotADependencyError(PymkError):

    def __init__(self, dependency, task):
        self.dependency = dependency
        self.task = task

    def __str__(self):
        return 'Error: Object "%s" of a task "%s" is not a dependency!' % (str(self.dependency.__name__), self.task.__name__)


class WrongPymkVersion(PymkError):

    def __init__(self, pymk_version, mkfile_version):
        self.pymk_version = pymk_version
        self.mkfile_version = mkfile_version

    def __str__(self):
        return 'Error: mkfile need greater version (%s) of pymk (%s). Please update.' % (self.mkfile_version, self.pymk_version)
