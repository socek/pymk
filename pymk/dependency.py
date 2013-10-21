import os

from pymk import error


class Dependency(object):

    """Base of all dependencys."""
    detailed = []

    def __init__(self):
        self.runned = False

    def __call__(self, task, dependency_force=False):
        """__call__(self, task, dependency_force) -> bool
        Method that will be called to check if dependency need to be rebuilded (if
        it is a task), and return True if task assigned will have to rebuild.
        """
        self.runned = self.do_test(task, dependency_force)
        return self.runned

    # === graph specyfic ===
    def extra(self):
        return ''

    def get_graph_name(self):
        return '"' + str(self.name) + '"'

    def get_graph_details(self):
        return ''

    def _get_shape_color(self):
        if self.runned:
            return 'darkgreen'
        else:
            return 'white'

    def _get_text_color(self):
        return 'black'

    def write_graph_detailed(self, datalog):
        if not self.name in self.detailed:
            self.detailed.append(self.name)
            datalog.write('"%s" [fillcolor=%s,fontcolor=%s,%s];\n' % (
                self.name,
                self._get_shape_color(),
                self._get_text_color(),
                self.get_graph_details())
            )


class FileDependency(Dependency):

    def __init__(self, filenames):
        def convert_filenames(filenames):
            if type(filenames) in [str, unicode]:
                return [filenames]
            else:
                return filenames
        super(FileDependency, self).__init__()
        self.filenames = convert_filenames(filenames)

    @property
    def name(self):
        if len(self.filenames) == 1:
            return self.filenames[0]
        else:
            return 'Many files'

    def compare_mtime(self, first, second):
        if os.path.getmtime(first) > os.path.getmtime(second):
            return True
        else:
            return False


class FileChanged(FileDependency):

    """Dependency returns true if file provided was changed. If task argument is
    provided, then run that task if it should be done."""

    def __init__(self, filenames, task=None):
        super(FileChanged, self).__init__(filenames)
        self.task = task

    def make_dependent_file(self):
        if self.task is None:
            filenames = ', '.join(self.filenames)
            raise error.CouldNotCreateFile(filenames)
        else:
            self.task.run(False)
        return True

    def check_dependent_file(self, task):
        try:
            result = False
            for filename in self.filenames:
                result |= self.compare_mtime(filename, task().output_file)
            return result
        except OSError:
            return self.make_dependent_file()

    def do_test(self, task, dependency_force=False):
        def raise_error_if_task_has_no_output_file(task):
            if task is None:
                return
            if task().output_file is None:
                raise error.TaskMustHaveOutputFile(task.getName())
        #----------------------------------------------------------------------
        raise_error_if_task_has_no_output_file(task)
        raise_error_if_task_has_no_output_file(self.task)

        if dependency_force:
            return True

        if os.path.exists(task().output_file):
            return self.check_dependent_file(task)
        else:
            for filename in self.filenames:
                if not os.path.exists(filename):
                    raise error.CouldNotCreateFile(filename)
            return True

    # === graph specyfic ===
    def extra(self):
        if self.runned:
            return '[label="C",color="blue"]'
        else:
            return '[label="C"]'

    def get_graph_details(self):
        return 'shape=hexagon,regular=1,style=filled,label="%s"' % (
            self.name.replace('/', '\\n')
        )


class FileDoesNotExists(FileDependency):

    """Dependency returns ture if file does not exists."""

    def do_test(self, task, dependency_force=False):
        if dependency_force:
            return True

        for filename in self.filenames:
            if not os.path.exists(filename):
                return True
        return False

    # === graph specyfic ===
    def extra(self):
        if self.runned:
            return '[label="NE",color="blue"]'
        else:
            return '[label="NE"]'

    def get_graph_details(self):
        return 'shape=triangle, regular=1,style=filled,label="%s"' % (
            self.name.replace('/', '\\n')
        )


class AlwaysRebuild(Dependency):

    """Dependency will always make a task rebuild."""

    def __init__(self):
        super(AlwaysRebuild, self).__init__()

    def do_test(self, task, dependency_force=False):
        return True

    # === graph specyfic ===
    def extra(self):
        if self.runned:
            return '[label="A",color="blue"]'
        else:
            return '[label="A"]'

    @property
    def name(self):
        return id(self)

    def get_graph_details(self):
        return 'shape=diamond, regular=1,style=filled,fillcolor=blue,fontcolor=yellow,label="Always\\nRebuild"'


class InnerDependency(Dependency):

    def __init__(self, parent):
        super(InnerDependency, self).__init__()
        self.parent = parent

    # === graph specyfic ===
    @property
    def name(self):
        return self.parent.getName()


class InnerFileExists(InnerDependency):

    def do_test(self, task, dependency_force=False):
        if dependency_force:
            self.parent.run(True, True, True, task)
            return True
        if self.parent().output_file:
            if os.path.exists(self.parent().output_file):
                self.parent.run(False, parent=task)
                return False
            else:
                self.parent.run(parent=task)
                return True
        else:
            raise error.TaskMustHaveOutputFile(self.parent.getName())

    # === graph specyfic ===
    def extra(self):
        if self.runned:
            return '[label="E",color="blue"]'
        else:
            return '[label="E"]'


class InnerFileChanged(InnerDependency):

    def do_test(self, task, dependency_force=False):
        if dependency_force:
            self.parent.run(True, True, True, parent=task)
        ret = self.parent.run(False, parent=task)
        return FileChanged(self.parent().output_file, self.parent)(task) or ret

    # === graph specyfic ===
    def extra(self):
        if self.runned:
            return '[label="C",color="blue"]'
        else:
            return '[label="C"]'


class InnerLink(InnerDependency):

    def do_test(self, task, dependency_force=False):
        self.parent.run(False, parent=task)
        return False

    def extra(self):
        return '[label="L"]'
