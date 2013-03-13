=================
4.4.2 Run command
=================
.. module:: extra.cmd

.. function:: run_cmd(args[, show_output=False])

    Run external program.

    :param args: list of arguments or string for external program (with the path on the begining)
    :param show_output: show output of the command to stdout
    :return: stdout and stderr of the program in a tuple
