Introduction
============

pymk is a script that provides the sam functionality that "makefile" does, but
the "makefile" (mkfile.py) is a python script. Code of mkfile.py is clean, and
it can do more things (like check all files from all folders and subfolders named
"migrations").

Why reimplement makefile?
=========================
Setting dependency in makefile is not flexible. Supports only "if file is newear,
then rebuild". Pymk can have in it's dependency whatever python code you want.
Event if you want to check something using network.

Documentation
=============
Full documentation can be found here: http://pythonhosted.org/Pymk/

Tutorial
========
First, we need to make an empty "mkfile.py". Pymk will try to search for a list
of taks and will find nothing.
::
    $ touch mkfile.py
    $ pymk
    Avalible tasks:

Now we need to make simple task. Put this in mkfile.py
::
    from pymk.task import Task

    class task(Task):
        dependencys = []
        def build(cls):
            print 'Hello'

And now we can execute
::
    $ pymk
    Avalible tasks:
        task
    $ pymk task
     * Building 'task'
    Hello

If you want pymk to run some task by default, just put this line at the end of
the mkfile.py
::
    SETTINGS = {
        'default task' : task,
    }

And run
::
    $ pymk
    * Building 'task'
   Hello

Ok, but now our task are build every time we make it. We need to make a file in
our script, and point which file we are creating. Out mkfile.py should look like
this
::
    from pymk.task import Task
    from pymk.extra import touch

    class task(Task):
        dependencys = []

        output_file = 'a.out'

        def build(cls):
            touch(cls.output_file)

    SETTINGS = {
        'default task' : task,
    }

And then we execute
::
    $ pymk
     * Building 'task'
    $ pymk
    * 'task' is up to date
    $ ls a.out
    a.out

And now we start playing. We need some dependency. Here's the file
::
    from pymk.task import Task
    from pymk.dependency import FileChanged

    class task(Task):
        output_file = 'a.out'

        dependencys = [
            FileChanged('b.out'),
        ]

        def build(cls):
            fp = open(cls.output_file, 'a')
            fp.write('bulded!\n')
            fp.close()

    SETTINGS = {
        'default task' : task,
    }

We can now try:
::
    $ pymk
    Could not create file b.out
    $ ls
    mkfile.py  mkfile.pyc

But this will not work becouse of absance of b.out file. So we will create it
and try again.
::
    $ touch b.out
    $ pymk
     * Building 'task'
    $ ls
    a.out  b.out  mkfile.py  mkfile.pyc
    $ pymk
     * 'task' is up to date
    $ touch b.out
    $ pymk
     * Building 'task'

As we can see, a.out will be created when b.out will be changed. This dependency
is implemented for files that can changed by external programs (or programmers).
If we need a task depedency, like "if task changed, rebuild me" we can make something
like that
::
    from pymk.task import Task

    class secon_task(Task):
        output_file = 'b.out'

        dependencys = []

        def build(cls):
            fp = open(cls.output_file, 'a')
            fp.write('bulded!\n')
            fp.close()

    class task(Task):
        output_file = 'a.out'

        dependencys = [
            secon_task.dependency_FileChanged(),
        ]

        def build(cls):
            fp = open(cls.output_file, 'a')
            fp.write('bulded!\n')
            fp.close()

    SETTINGS = {
        'default task' : task,
    }

And new can run this:
::
    $ rm *.out # if something was left before
    $ pymk
     * Building 'secon_task'
     * Building 'task'
    $ pymk
     * 'task' is up to date
    $ touch b.out
    $ pymk
     * Building 'task'
