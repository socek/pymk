import os
import fnmatch
def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

from subprocess import Popen, PIPE
from pymk.error import CommandError
def run_cmd(args, show_output=False):
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
def touch(filename):
    fhandle = file(filename, 'a')
    try:
        os.utime(filename, None)
    finally:
        fhandle.close()
