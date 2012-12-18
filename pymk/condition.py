import os
from pymk import error

class BaseCondition(object):
    """Base of all conditions."""
    def __call__(self, task):
        """__call__(self, task) -> bool
        Method that will be called to check if condition need to be rebuilded (if
        it is a task), and return True if task assigned will have to rebuild.
        """

class FileChanged(BaseCondition):
    """Condition returns true if file provided was changed. If task argument is
    provided, then run that task if it should be done."""
    def __init__(self, filename, task=None):
        self.filename = filename
        self.task = task

    def __call__(self, task):
        if task.output_file:
            if self.task and not self.task.output_file:
                raise error.TaskMustHaveOutputFile(self.task.name())
            if os.path.exists(task.output_file):
                try:
                    if os.path.getmtime(self.filename) > os.path.getmtime(task.output_file) :
                        return True
                    else:
                        return False
                except OSError:
                    if self.task:
                        self.task.run(False)
                        return True
                    else:
                        raise error.CouldNotCreateFile(self.filename)
            else:
                if os.path.exists(self.filename):
                    return True
                else:
                    raise error.CouldNotCreateFile(self.filename)
        else:
            raise error.TaskMustHaveOutputFile(task.name())

class FileDoesNotExists(BaseCondition):
    """Condition returns ture if file does not exists."""

    def __init__(self, filename):
        self.filename = filename

    def __call__(self, task):
        return not os.path.exists(self.filename)

class AlwaysRebuild(BaseCondition):
    """Condition will always make a task rebuild."""

    def __call__(self, task):
        return True
