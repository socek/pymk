import os
from pymk import error


class BaseDependency(object):
    """Base of all dependencys."""
    detailed = []

    def __init__(self):
        self.extra = ''
        self.runned = False

    def __call__(self, task, dependency_force=False):
        """__call__(self, task, dependency_force) -> bool
        Method that will be called to check if dependency need to be rebuilded (if
        it is a task), and return True if task assigned will have to rebuild.
        """
        self.runned = self.do_test(task, dependency_force)
        return self.runned

    # === graph specyfic ===
    def get_graph_name(self):
        return '"' + self.name + '"'

    def get_graph_details(self):
        return ''

    def _get_shape_color(self):
        if self.runned:
            return 'red'
        else:
            return 'white'

    def write_graph_detailed(self, datalog):
        if not self.name in self.detailed:
            self.detailed.append(self.name)
            datalog.write('"%s" [fillcolor=%s,%s];\n' % (self.name, self._get_shape_color(), self.get_graph_details()))

class FileChanged(BaseDependency):
    """Dependency returns true if file provided was changed. If task argument is
    provided, then run that task if it should be done."""

    def __init__(self, filename, task=None):
        super(FileChanged, self).__init__()
        self.filename = filename
        self.task = task
        self.extra = '[label="C"]'

    def do_test(self, task, dependency_force=False):
        if dependency_force:
            return True
        if task.output_file:
            if self.task and not self.task.output_file:
                raise error.TaskMustHaveOutputFile(self.task.name())
            if os.path.exists(task.output_file):
                try:
                    if os.path.getmtime(self.filename) > os.path.getmtime(task.output_file):
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

    # === graph specyfic ===
    @property
    def name(self):
        return self.filename

    def get_graph_details(self):
        return 'shape=hexagon,regular=1,style=filled,label="%s"' % (
            self.name.replace('/', '\\n')
        )


class FileDoesNotExists(BaseDependency):
    """Dependency returns ture if file does not exists."""

    def __init__(self, filename):
        super(FileDoesNotExists, self).__init__()
        self.filename = filename
        self.extra = '[label="NE"]'

    def do_test(self, task, dependency_force=False):
        if dependency_force:
            return True
        return not os.path.exists(self.filename)

    # === graph specyfic ===
    @property
    def name(self):
        return self.filename

    def get_graph_details(self):
        return 'shape=triangle, regular=1,style=filled,label="%s"' % (
            self.name.replace('/', '\\n')
        )

class AlwaysRebuild(BaseDependency):
    """Dependency will always make a task rebuild."""

    def __init__(self):
        super(AlwaysRebuild, self).__init__()
        self.extra = '[label="A",color="red"]'

    def do_test(self, task, dependency_force=False):
        return True

    # === graph specyfic ===
    @property
    def name(self):
        return id(self)

    def get_graph_details(self):
        return 'shape=diamond, regular=1,style=filled,fillcolor=red,label="Always\\nRebuild"'


class InnerDependency(BaseDependency):

    def __init__(self, parent):
        super(InnerDependency, self).__init__()
        self.parent = parent

    # === graph specyfic ===
    @property
    def name(self):
        return self.parent.__name__


class InnerFileExists(InnerDependency):

    def __init__(self, parent):
        super(InnerFileExists, self).__init__(parent)
        self.extra = '[label="E"]'

    def do_test(self, task, dependency_force=False):
        if dependency_force:
            self.parent.run(True, True, True, task)
            return True
        if self.parent.output_file:
            if os.path.exists(self.parent.output_file):
                self.parent.run(False, parent=task)
                return False
            else:
                self.parent.run(parent=task)
                return True
        else:
            raise error.TaskMustHaveOutputFile(self.parent.name())


class InnerFileChanged(InnerDependency):

    def __init__(self, parent):
        super(InnerFileChanged, self).__init__(parent)
        self.extra = '[label="C"]'

    def do_test(self, task, dependency_force=False):
        if dependency_force:
            self.parent.run(True, True, True, parent=task)
        ret = self.parent.run(False, parent=task)
        return FileChanged(self.parent.output_file, self.parent)(task) or ret
