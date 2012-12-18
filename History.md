0.1.2 / 2012-12-18
==================

  * Reverted "Changed behavior of running test. Now, if no output_file provided, the task
    will always be build." This will be managet by special condition AlwaysRebuild.
  * Added AlwaysRebuild condition which will always rebuild assigned task.
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
