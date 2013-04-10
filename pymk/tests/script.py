from pymk.tests.base import PymkTestCase
from pymk.script import parse_task_name


class TaskNameParseTest(PymkTestCase):

    def test_parse_task_name(self):
        name, args = parse_task_name('/something/elo')
        self.assertEqual('/something/elo', name)
        self.assertEqual({}, args)

        name, args = parse_task_name('/something/elo?elo=10')
        self.assertEqual('/something/elo', name)
        self.assertEqual({'elo' : ['10']}, args)

        name, args = parse_task_name('/something/elo/?elo=10&zbychu=12')
        self.assertEqual('/something/elo/', name)
        self.assertEqual({'elo' : ['10'], 'zbychu' : ['12']}, args)

        name, args = parse_task_name('/something/elo/?elo=10&zbychu=12,10&zbychu=ccc')
        self.assertEqual('/something/elo/', name)
        self.assertEqual({'elo' : ['10'], 'zbychu' : ['12,10', 'ccc']}, args)
