===============
3. Command line
===============

3.1 Using pymk command
======================

    >>> pymk taskname taskname2 taskname3

    Runs task with specyfic names. If no task is inputed, and no default task is
    setted in settings, then pymk will print list of all tasks.

3.2 Graph options
=================

    ``pymk`` can draw a graph of task. If the '-g' with filename options is inputed,
    the graph will be drawn in that file. If no task is inputed, the graph will be
    drawn from all of the task.

    >>> pymk -g graph.png

    But if task is inputed, then the graph will be drawn with information on what
    task was run, and what not.

    >>> pymk -g grpah.png taskname


3.3 Command help
================
::

    >>> pymk -h
    usage: pymk [-h] [-l LOG] [-a] [-f] [-g GRAPH] [-d] [task [task ...]]

    positional arguments:
      task                  List of task to do.

    optional arguments:
      -h, --help            show this help message and exit
      -l LOG, --log LOG     Ser log level from "debug" or "info".
      -a, --all             Show all tasks avalible.
      -f, --force           Force task to rebuild.
      -g GRAPH, --graph GRAPH
                            Draw a graph of tasks to a file.
      -d, --dependency-force
                            Force depedency to rebuild (use only with --force).

