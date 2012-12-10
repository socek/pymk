import os
import fnmatch
def find_files(directory, pattern):
    """find_files(directory, pattern) - None
    Yields path with founded files.

    @param directory: directory in which start search
    @param pattern: patter which will be used for searc
    """
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

from subprocess import Popen, PIPE
from pymk.error import CommandError
def run_cmd(args, show_output=False):
    """run_cmd(args, show_output=False) -> stdout, stderr
    Run external program.

    @param args: list of arguments for external program (with the path on the begining)
    @param show_output: show output of the command to stdout
    @return: stdout and stderr of the program
    """
    if show_output:
        spp = Popen(args, shell=True)
    else:
        spp = Popen(args, stdout=PIPE, stderr=PIPE, shell=True)
    try:
        error = spp.wait()
        if error != 0:
            if show_output:
                raise CommandError(error, '')
            else:
                raise CommandError(error, spp.stderr.read())
    except KeyboardInterrupt:
        pass
    return spp.stdout, spp.stderr

import os
def touch(path):
    """touch(filename) -> None
    Updates file access and modified times specified by path.
    """
    fhandle = file(path, 'a')
    try:
        os.utime(path, None)
    finally:
        fhandle.close()
