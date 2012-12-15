import unittest
import logging
import task
import condition
import extra

all_test_cases = [
    task.TaskTest,
    condition.FileDoesNotExistsConditionTest,
    condition.FileChangedConditionTest,
    task.TaskConditionFileExistsTest,
    task.TaskConditionFileChangedTest,
    extra.TouchTest,
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
