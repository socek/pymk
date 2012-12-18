import unittest
import logging
import task
import condition
import extra

all_test_cases = [
    task.TaskTest,
    task.TaskConditionFileExistsTest,
    task.TaskConditionFileChangedTest,

    condition.FileDoesNotExistsConditionTest,
    condition.FileChangedConditionTest,
    condition.AlwaysRebuildConditionTest,
    
    extra.TouchTest,
    extra.FindFilesTest,
    extra.RunCmdTest,
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
