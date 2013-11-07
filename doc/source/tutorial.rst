===========
2. Tutorial
===========

2.1 Firs mkfile.py
==================

First, we need to make an empty "mkfile.py". Pymk will try to search for a list
of taks and will find nothing.

>>> touch mkfile.py
>>> pymk
Avalible tasks:
  Name   Path   Help
  ----   ----   ----

Now we need to make simple task. Put this in mkfile.py
::

    from pymk.task import Task

    class task(Task):
        dependencys = []
        def build(self, args):
            print 'Hello'

And now we can execute

>>> pymk
Avalible tasks:
  Name   Path    Help
  ----   ----    ----
  task   /task
>>> pymk /task
 * Building 'task'
Hello

Ok, but now our task are build every time we change it. We need to make a file in
our script, and point which file we are creating. Out mkfile.py should look like
this
::

    from pymk.task import Task
    from pymk.extra import touch

    class task(Task):
        dependencys = []

        output_file = 'a.out'

        def build(self, args):
            touch(self.output_file)

And then we execute

>>> pymk /task
* Building 'task'
>>> pymk /task
* 'task' is up to date
>>> ls a.out
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

        def build(self, args):
            fp = open(self.output_file, 'a')
            fp.write('bulded!\n')
            fp.close()


.. image:: ./images/tutorial_phase_4.png

This is how the graph will draw our mkfile. Now we can try:

>>> pymk /task
Could not create file b.out
>>> ls
mkfile.py  mkfile.pyc

But this will not work becouse of absance of b.out file. So we will create it
and try again.

>>> touch b.out
>>> pymk
 * Building 'task'
>>> ls
a.out  b.out  mkfile.py  mkfile.pyc
>>> pymk
 * 'task' is up to date
>>> touch b.out
>>> pymk
 * Building 'task'

As we can see, a.out will be created when b.out will be changed. This dependency
is implemented for files that can changed by external programs (or programmers).
And this is good moment for describing the -g option for pymk (make a graph).

2.2 Making tasks graphs
=======================
We will change the mkfile a little bit, so we will have two dependencys.
::

    from pymk.task import Task
    from pymk.dependency import FileChanged

    class task(Task):
        output_file = 'a.out'

        dependencys = [
            FileChanged('b.out'),
            FileChanged('c.out'),
        ]

        def build(self, args):
            fp = open(self.output_file, 'a')
            fp.write('bulded!\n')
            fp.close()

>>> pymk -g graph.png

.. image:: ./images/tutorial_phase_5.png

As we can see, our tasks depends on two files. Our task will rebuild when at least
one of thoes files will be never then our output file. The "C" stands for "change"
near the arrow. If we run this:

>>> touch b.out
>>> touch c.out
>>> pymk -g graph.png /task

.. image:: ./images/tutorial_phase_5_run1.png

The dark green color means "this dependency accured".
The green color means "this task was runned".
The red color means "this task failed".
If we run this again:

>>> pymk -g graph.png /task

.. image:: ./images/tutorial_phase_5_run2.png

No task was builded, because no depedency accured. If we change one of this file,
then only one dependency will be red.

>>> touch c.out
>>> pymk -g graph.png /task

.. image:: ./images/tutorial_phase_5_run3.png


2.3 Task dependency with another task
=====================================

If we need a task depedency, like "if task changed, rebuild me" we can make something
like that
::

    from pymk.task import Task
    from pymk.dependency import FileChanged


    class secon_task(Task):
        output_file = 'b.out'

        dependencys = [
            FileChanged('d.out'),
        ]

        def build(self, args):
            fp = open(self.output_file, 'a')
            fp.write('bulded!\n')
            fp.close()

    class task(Task):
        output_file = 'a.out'

        dependencys = [
            secon_task.dependency_FileChanged(),
            FileChanged('c.out')
        ]

        def build(self, args):
            fp = open(self.output_file, 'a')
            fp.write('bulded!\n')
            fp.close()


.. image:: ./images/tutorial_phase_6.png

And new can run this:

>>> rm *.out # if something was left before
>>> touch c.out d.out
>>> pymk /task
 * Building 'secon_task'
 * Building 'task'

.. image:: ./images/tutorial_phase_6_run1.png

>>> pymk /task
 * 'task' is up to date

.. image:: ./images/tutorial_phase_6_run2.png

>>> touch d.out
>>> pymk /task
 * Building 'secon_task'
 * Building 'task'

.. image:: ./images/tutorial_phase_6_run3.png

But what if we want to do "task" only once, after the "second_task" is created
and not when the task is rebuilded? We can use FileExists.
::

    from pymk.task import Task
    from pymk.dependency import FileChanged

    class secon_task(Task):
        output_file = 'b.out'

        dependencys = [
            FileChanged('d.out'),
        ]

        def build(self, args):
            fp = open(self.output_file, 'a')
            fp.write('bulded!\n')
            fp.close()

    class task(Task):
        output_file = 'a.out'

        dependencys = [
            secon_task.dependency_FileExists(),
            FileChanged('c.out')
        ]

        def build(self, args):
            fp = open(self.output_file, 'a')
            fp.write('bulded!\n')
            fp.close()


.. image:: ./images/tutorial_phase_7.png


>>> rm *.out
>>> touch c.out d.out
>>> pymk /task
 * Building 'secon_task'
 * Building 'task'

.. image:: ./images/tutorial_phase_7_run1.png

>>> touch d.out
>>> pymk /task
 * Building 'secon_task'
 * 'task' is up to date

.. image:: ./images/tutorial_phase_7_run2.png


2.4 Command task
================
Sometimes task will run program instead of creating files (like run deveopers web
server). For this task the "AlwaysRebuild" dependency is created. When used this
dependency the task will be always rebuilded.
::

    from pymk.task import Task
    from pymk.dependency import FileChanged, AlwaysRebuild

    class secon_task(Task):
        output_file = 'b.out'

        dependencys = [
            FileChanged('d.out'),
        ]

        def build(self, args):
            fp = open(self.output_file, 'a')
            fp.write('bulded!\n')
            fp.close()

    class task(Task):
        output_file = 'a.out'

        dependencys = [
            secon_task.dependency_FileExists(),
            FileChanged('c.out'),
            AlwaysRebuild(),
        ]

        def build(self, args):
            fp = open(self.output_file, 'a')
            fp.write('bulded!\n')
            fp.close()


.. image:: ./images/tutorial_phase_8.png

The shape and the color of the task with "AlwaysRebuild" dependency changed on the
graph and the "AlwaysRebuild" dependency is not shown. Now, we can run it.

>>> rm *.out
>>> touch c.out d.out
>>> pymk /task
 * Building 'secon_task'
 * Building 'task'

.. image:: ./images/tutorial_phase_8_run1.png

>>> pymk /task
 * Building 'task'

.. image:: ./images/tutorial_phase_8_run2.png


2.4 Task arguments
==================
Task tan take arguments. And it can be named. This small example will show how
to use it. Name can be like url paths.
::

    from pymk.task import Task
    from pymk.dependency import AlwaysRebuild

    class task(Task):

        path = '/this/name'

        dependencys = [
            AlwaysRebuild(),
        ]

        def build(self, args):
            print args

We can use this task name like that:

>>> pymk /this/name
 * Building '/this/name'
{}

Arguments can be passet like the URL get params.

>>>  pymk /this/name?var=1
 * Building '/this/name'
{'var': ['1']}

>>> pymk "/this/name?var=1&var=2&var2=3"
 * Building '/this/name'
{'var': ['1', '2'], 'var2': ['3']}

2.5 Recipes
===========
Recipes can provide you with some basic configuration.

2.5.1 Default task
==================
::

    from pymk.recipe import Recipe
    from pymk.task import Task
    from pymk.dependency import AlwaysRebuild


    class RecipeMy(Recipe):

        default_task = '/this/name'


    class task(Task):

        path = '/this/name'

        dependencys = [
            AlwaysRebuild(),
        ]

        def build(self, args):
            print args

>>> pymk
 * Building 'task'
{}

2.5.2 Settings
==============
Pymk use SmallSettings module for settings. For more info about settings please go to https://github.com/socek/smallsettings
Recipe has 2 vars for settings. Recipe.settings and Recipe.paths. Both of this properties are avalible in the task class.
::

    from pymk.recipe import Recipe
    from pymk.task import Task
    from pymk.dependency import AlwaysRebuild


    class RecipeMy(Recipe):

        default_task = '/this/name'

        def create_settings(self):
            super(RecipeMy, self).create_settings()
            self.settings['elo'] = 10
            self.settings['2elo'] = '<%(elo)d 20>'
            self.paths['root'] = '/tmp'
            self.paths['my'] = ['%(root)s', 'somedir', 'file']


    class task(Task):

        path = '/this/name'

        dependencys = [
            AlwaysRebuild(),
        ]

        def build(self, args):
            print self.settings['elo'], self.settings['2elo']
            print self.paths['root'], self.paths['my']

>>> pymk
 * Building 'task'
10 <10 20>
/tmp /tmp/somedir/file

2.6 External modules
====================
Pymk can download external modules. But the external modules need to be imported in the task, not globally, or it will crashe.
::

    from pymk.recipe import Recipe
    from pymk.task import Task
    from pymk.dependency import AlwaysRebuild


    class RecipeMy(Recipe):

        default_task = '/this/name'

        def gather_recipes(self):
            self.download_recipe('pyrg', 'https://pypi.python.org/packages/2.6/p/pyrg/pyrg-0.2.6-py2.6.egg#md5=95b391580e63d097a40c15de11943723')


    class task(Task):

        path = '/this/name'

        dependencys = [
            AlwaysRebuild(),
        ]

        def build(self, args):
            import pyrg
            print pyrg


>>> pymk
Downloading pyrg...
Extracting pyrg...
 * Building 'task'
<module 'pyrg' from 'pymkmodules/pyrg.egg/pyrg.py'>

2.6.1 Additional recipes
========================
When you need to split tasks in to seperate files, you can create pymkmodules directory and store this files there. It is good practice for all thoes files to have it's own recipe.

pymkmodules/mymodule.py
-----------------------
::

    from pymk.task import Task
    from pymk.dependency import AlwaysRebuild


    class task(Task):

        path = '/that/name'

        dependencys = [
            AlwaysRebuild(),
        ]

        def build(self, args):
            print 'that!'


mkfile.py
---------
::

    from pymk.recipe import Recipe
    from pymk.task import Task
    from pymk.dependency import AlwaysRebuild


    class RecipeMy(Recipe):

        def gather_recipes(self):
            self.add_recipe('mymodule')


    class task(Task):

        path = '/this/name'

        @property
        def dependencys(self):
            return [
                self.get_task('/that/name').dependency_Link(),
                AlwaysRebuild(),
            ]

        def build(self, args):
            print 'hello'


>>> pymk /this/name
 * Building 'task'
that!
 * Building 'task'
hello
