import os
from pymk import error

class BaseCondition(object):

    def __call__(self, task):
        pass

class FileChanged(BaseCondition):
    def __init__(self, filename, task=None):
        self.filename = filename
        self.task = task

    def __call__(self, task):
        try:
            if os.path.getmtime(self.filename) > os.path.getmtime(task.output_file) :
                return True
            else:
                return False
        except OSError:
            if self.task:
                self.task().run()
                return True
            else:
                raise error.CouldNotCreateFile(self.filename)

class FileDoesNotExists(BaseCondition):
    def __init__(self, filename):
        self.filename = filename

    def __call__(self, task):
        return not os.path.exists(self.filename)

class OutputFileDoesNotExists(BaseCondition):
    def __call__(self, task):
        return not os.path.exists(task.output_file)
