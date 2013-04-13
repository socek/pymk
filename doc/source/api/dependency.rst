=================================
4.2 Dependency
=================================
.. module:: dependecy

4.2.1 Avalible depedencys
=========================

* .. class:: FileChanged

    Dependency returns true if file provided was changed. If task argument is provided, then run that task if it should be done.

    :param path: Path or list of paths.

* .. class:: FileDoesNotExists

    Dependency returns ture if file does not exists.

    :param path: Path or list of paths.

* .. class:: AlwaysRebuild

    Dependency will always make a task rebuild.

4.2.2.1 Dependency class
==========================

.. class:: Dependency

.. method:: Dependency.__call__(task[, dependency_force=False])

    Method that will be called to check if dependency need to be rebuilded (if
    it is a task), and return True if task assigned will have to rebuild.

    .. note::

        Use this to make a dependency test, but put your code into the do_test
        method if you have your own dependency.

    :param task: task in which the dependency is listed
    :param dependency_force: force dependency of task to rebuild
    :rtype: bool
    :return: was task runned

.. method:: Dependency.do_test(task[, dependency_force=False])

    Method that will be called to check if dependency need to be rebuilded (if
    it is a task), and return True if task assigned will have to rebuild.

    .. note::

        This method is only for inheritance. If you have your own Dependancy, make
        you code here instead of in __call__.


4.2.2.2 Graph specyfic methods
==============================

.. note::

    This methods are responsible for drawing a graph.

.. method:: Dependency.extra()

    Options for the links (like adding comments, or changing color)
    :rtype: str

.. method:: Dependency.get_graph_details()

    Returns graph data details (in dot language) of task object.

    :rtype: str

.. method:: Dependency.write_graph_detailed(datalog)

    Writes graph data (in dot language) to datalog file pipe.

.. method:: Dependency.get_graph_name()

    Returns name of dependency

    :rtype: str

.. method:: Dependency._get_shape_color()

    Returns shape of dependency.

    :rtype: str

.. method:: Dependency._get_text_color()

    Returns color of text.

    :rtype: str

4.2.3 InnerDependency
=====================

.. class InnerDependency::

.. note::

    This class is a base class for all the dependency that will be used as a
    task-to-task dependency.

.. method:: Dependency.__init__(parent)

    :param parent: Task from which the dependency was creted.
