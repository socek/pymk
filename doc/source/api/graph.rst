==========
5.1. Graph
==========
.. module:: graph

5.1.1 color description
=======================
.. glossary::

    dark green
        this dependency accured
    green
        this task was runned
    red
        this task failed

5.1.2 api reference
===================
.. function:: run_dot(pipe, filename)

    Run dot program, which transfers dot language to graph image.

    :param pipe: Pipe with do script.
    :param filename: Path to a file in which the image will be created.

.. function:: draw_graph(filename)

    Draw graph to a filename from the mkfile (that should be already imported).

    :param filename: Path to a file in which the image will be created.

.. function:: draw_done_task_graph(filename, tasks)

    Draw graph of done tasks to a filename.

    :param filename: Path to a file in which the image will be created.
    :param task: Task which will be drawed.
