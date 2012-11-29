class PymkError(Exception): pass

class CouldNotCreateFile(PymkError):

    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return 'Could not create file %s' %(self.filename)
