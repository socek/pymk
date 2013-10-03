import unittest
from pymk import error


class ErrorsTests(unittest.TestCase):

    def test_CouldNotCreateFile(self):
        er = error.CouldNotCreateFile('filename')
        self.assertEqual(str, type(str(er)))

    def test_TaskAlreadyExists(self):
        er = error.TaskAlreadyExists('task name')
        self.assertEqual(str, type(str(er)))

    def test_CommandError(self):
        er = error.CommandError(1, 'task name')
        self.assertEqual(str, type(str(er)))

    def test_BadTaskName(self):
        er = error.BadTaskPath('task name')
        self.assertEqual(str, type(str(er)))

    def test_WrongArgumentValue(self):
        er = error.WrongArgumentValue('description')
        self.assertEqual(str, type(str(er)))

    def test_TaskMustHaveOutputFile(self):
        er = error.TaskMustHaveOutputFile('name')
        self.assertEqual(str, type(str(er)))

    def test_NoDependencysInAClass(self):
        er = error.NoDependencysInAClass(error.NoDependencysInAClass)
        self.assertEqual(str, type(str(er)))

    def test_NotADependencyError(self):
        er = error.NotADependencyError(
            error.NoDependencysInAClass, error.NoDependencysInAClass)
        self.assertEqual(str, type(str(er)))

    def test_RecipeAlreadyExists(self):
        er = error.RecipeAlreadyExists('name')
        self.assertEqual(str, type(str(er)))

    def test_WrongPymkVersion(self):
        er = error.WrongPymkVersion('pymk_version', 'mkfile_version')
        self.assertEqual(str, type(str(er)))
