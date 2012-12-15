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
