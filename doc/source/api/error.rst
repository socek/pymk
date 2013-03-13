==========
4.3 Errors
==========
.. module:: error

* .. class:: CouldNotCreateFile

    Raised when there is a file in dependency, but mkfile do not defines how to build it.

* .. class:: TaskAlreadyExists

    Raised when task of that name already exits. Tasks can not be ovverided.

* .. class:: NoMkfileFound

    Raised when the folder in which pymk was used do not have mkfile.py

* .. class:: CommandError

    Raised when external command returns error.

* .. class:: BadTaskName

    Raised when inputed task name do not exists in mkfile (or was not add as a task with @AddTask)

* .. class:: WrongArgumentValue

    Raised when argument has a list of values, but inputet value is not in this list.

* .. class:: TaskMustHaveOutputFile

    Raised when task has no output_file setted, but the dependency assigned to
    that task (or to task that this task is assigned as dependency) need this value.

* .. class:: NoDependencysInAClass

    Raised when no depedencys attribute was provided, or this attribute has wrong name.

* .. class:: NotADependencyError

    NotADependencyError is raised when some object in dependency list are not
    an object inherited from pymk.dependency.Dependency.
