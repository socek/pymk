=============
1. About pymk
=============

1.1 Why reimplement makefile?
=============================
Setting dependency in makefile is not flexible. Supports only "if file is newear,
then rebuild". Pymk can have in it's dependency whatever python code you want.
Event if you want to check something using network.

1.2 Advantage of pymk
=====================
* more flexible dependency
* can use python code for dependecy
* simpler debbuging
* can draw tasks graphs (which is very helpful for debbuging)

1.3 Website
===========
Pymk do not have any special project website, by we have a github projcet here:
https://github.com/socek/pymk

1.4 Install
===========
You can install using easy_install:

>>> easy_install pymk

or pip:

>>> pip install pymk
