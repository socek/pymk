import os
import sys
from pymk.task import TASKS

def run():
    sys.path.append(os.getcwd())
    try:
        import mkfile
    except ImportError:
        print "No mkfile.py file found!"
        return 1

    if len(sys.argv) == 1:
        print 'Avalible tasks:'
        print '\t' + '\n\t'.join(TASKS.keys())
    else:
        for task in sys.argv[1:]:
            TASKS[task]().run()
