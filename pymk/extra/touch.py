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
