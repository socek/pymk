import unittest
import logging
from . import task
from . import dependency
from . import extra
from . import error
from . import script

all_test_cases = [
    task.TaskTest,
    task.TaskDependencyFileExistsTest,
    task.TaskDependencyFileChangedTest,
    task.TaskForcing,
    task.TaskDependencyLinkTest,
    task.TaskNameTest,

    dependency.FileDoesNotExistsDependencyTest,
    dependency.FileChangedDependencyTest,
    dependency.AlwaysRebuildDependencyTest,
    dependency.InnerFileExistsTest,
    dependency.InnerFileChangedTest,

    extra.TouchTest,
    extra.FindFilesTest,
    extra.RunCmdTest,

    error.ErrorsTests,

    script.TaskNameParseTest,
    script.GraphTest,
]


def get_all_test_suite():
    logging.basicConfig(level=logging.INFO, format="%(asctime)-15s:%(message)s", filename='test.log')
    logging.getLogger('pymk').info('\n\t*** TESTING STARTED ***')
    suite = unittest.TestLoader()
    prepered_all_test_cases = []
    for test_case in all_test_cases:
        prepered_all_test_cases.append(
            suite.loadTestsFromTestCase(test_case)
        )
    return unittest.TestSuite(prepered_all_test_cases)
