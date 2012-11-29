class PymkError(Exception): pass

class CouldNotCreateFile(PymkError):
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return 'Could not create file %s' %(self.filename)

class TaskAlreadyExists(PymkError):
    def __init__(self, task_name):
        self.task_name = task_name

    def __str__(self):
        return 'Task name already exists "%s".' %(self.task_name)

class NoMkfileFound(Exception): pass

class CommandError(PymkError):
    def __init__(self, number, text):
        self.number = number
        self.text = text

    def __str__(self):
        return 'Command error (%d): %s' %(self.number, self.text)
