======================
4.1 Task
======================

.. module:: task

4.1.1 Overall
=============

.. class:: Dependency

.. note::

    This attributes and methods are basic task configuration.

.. attribute:: Task.dependencys

    List of all dependecys. This attribute must be reimplemented.

.. attribute:: Task.output_file

    Path to a file which will be created. This file will be checked testing which file is newwer.

.. attribute:: Task.name

    Set this attribute If you want to have different name then the class name (for example like this '/install/something').

.. method:: Task.build()

    What to do with this task to rebuild it. This method needs to be reimplemented after inheriting.

4.1.2 Dependency methods
========================

.. note::

    This methods creates dependency, that can be used in different tasks.

.. classmethod:: Task.dependency_FileExists()

    Dependency that will run this task if not crated before.

    :return: dependency

.. classmethod:: Task.dependency_FileChanged()

    Dependency that will run this task if file is newwer then task.output_file.

    :return: dependency

.. classmethod:: Task.dependency_Link()

    This is a fake dependency. Using this dependency will link one task to another. This task will be runned (like it
    would be run manualy) before task linked to.

    :return: dependency

4.1.3 Inner methods
===================

.. note::

    This methods describe how the inner mechanizm works. This section is only for advaced users.

.. classmethod:: Task.name()

    :return: name of the tasks provided by class value _name, or just classname if _name is ``None``.
    :rtype: str

.. classmethod:: Task._get_runned()

    Was this task runned.

.. classmethod:: Task._set_runned(value)

    Sets runned flag.

    :param value: bool flag

.. classmethod:: Task.test_dependencys([dependency_force=False])

    Test all dependency of the task and rebuild the dependency tasks.

    :param dependency_force: force dependency of task to rebuild
    :return: ``True`` if this task needs to be rebuilded.
    :rtype: bool


.. classmethod:: Task.run([log_uptodate=True, force=False, dependency_force=False, parent=None])

    Test dependency of this task, and rebuild it if nessesery.

    :param log_uptodate: show 'task is up to date' information
    :param force: force task to rebuild
    :param dependency_force: force dependency of task to rebuild
    :param parent: parent task which invoked this one
    :return: ``True`` if this task needs to be rebuilded.
    :rtype: bool

4.1.4 Graph specyfic methods
============================

.. note::

    This methods are responsible for drawing a graph.

.. classmethod:: Task.write_graph_detailed(datalog)

    Writes graph data (in dot language) to datalog file pipe.

.. classmethod:: Task.get_graph_details()

    Returns graph data details (in dot language) of task object.

    :rtype: str
