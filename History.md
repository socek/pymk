0.2.0 / 2013-??-??
==================

  * "dependency" is now always needed in BastTask class. Now if it is not an list,
    pymk will fail. It is becouse of often,  hidden, TYPO errors.
  * no need of adding @classmethod decorator in build function
  * added template functionality with jinja2
  * added generating of graph
  * changed all dependencys to classes
    WARNING: This is not backward compatible!
  * added help feature
  * changed generathing data from decorator to metaclass.
  * added hidding tasks.
  * added settings instead of _DEFAULT value.

0.1.4 / 2012-12-20
==================

  * Fixed aborting pymk by keyboard.
  * Changed description.

0.1.3 / 2012-12-18
==================

  * Added forcing of tasks.

0.1.2 / 2012-12-18
==================

  * Changed "condition" name to "dependency".
  * Reverted "Changed behavior of running test. Now, if no output_file provided, the task
    will always be build." This will be managet by special dependency AlwaysRebuild.
  * Added AlwaysRebuild dependency which will always rebuild assigned task.
  * Fixed closing subprocess when pymk gets abort signal.

0.1.1 / 2012-12-15
==================

  * Changed behavior of running test. Now, if no output_file provided, the task
    will always be build.
  * Changed behavior of condition_FileExists function. Now it will rebuild depedency,
    if needed.

0.1.0 / 2012-12-15
==================

  * Working module with FileExists and FileChanged conditions.
