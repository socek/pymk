===========
5.2. Script
===========
.. module:: script

.. function:: make_graph(args, is_graphviz)

    Make a graph depend on what command line options was inputed.

    :param args: Command line args created by OptParser.
    :param is_graphviz: Is graphiz avalible. If not, do nothing.

.. function:: check_for_graphviz(args)

    Check for dot command, but only if command line wanted graph.

    :param args: Command line args created by OptParser.
    :return: True if command line setted the graph argument and there is a dot command.

.. function:: append_python_path([cwd=None])

    Append provided (or actual cwd if not provided) path to python path.

    :parametr cwd: path which will be appended

.. function:: run_tasks(mkfile, args)

    Run tasks from imported mkfile with command line arguments.

    :param mkfile: mkfile.py module
    :param args: Command line args created by OptParser.
    :return: Text representing what have been done:
        * 'list all' - printed list of all tasks
        * 'run tasks' - run inputed task
        * 'do graph of all' - made graph of all tasks
        * 'run default' - run default task

.. function:: run()

    Main function of the program. Parse command line args and do the task provided.
    More info :doc:`../commandline` or with inputing "pymk -h".

    :return:
     Errors:
         0. Everything is ok.
         1. no mkfile.py found or it is corrupted
         2. error in external program
         3. wrong task name
         4. provided task has no output_file, which is needed becouse of dependencys
         5. could not create a file that is in depedency
         6. command aborted (by keyboard)
