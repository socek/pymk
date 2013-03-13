=============
1. About pymk
=============

1.1. What is pymk
=================
``pymk`` is a program that provides the sam functionality that ``GNU make`` does,
but the ``makefile`` (``mkfile.py``) is a python script. Code of ``mkfile.py``
is clean, and it can do more things then ``makefile`` (like check all files from
all folders and subfolders with specific name).

1.2 Why reimplement makefile?
=============================
Setting dependency in makefile is not flexible. Supports only "if file is newear,
then rebuild". Pymk can have in it's dependency whatever python code you want.
Event if you want to check something using network.

1.3 Advantage of pymk
=====================
* more flexible dependency
* can use python code for dependecy
* simpler debbuging
* can draw tasks graphs (which is very helpful for debbuging)

1.4 Website
===========
Pymk do not have any special project website, by we have a github projcet here:
https://github.com/socek/pymk
