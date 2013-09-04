import os
from time import sleep, time
from mock import patch, call, MagicMock
from contextlib import nested
from subprocess import PIPE

import pymk.error as Perror
from pymk import extra
from pymk.tests.base import PymkTestCase
from pymk.error import CommandAborted


class TouchTest(PymkTestCase):
    test_file = 'testme.file'

    def test_new_file(self):
        actual_time = int(time())
        extra.touch(self.test_file)
        file_time = int(os.path.getmtime(self.test_file))
        self.assertTrue(os.path.exists(self.test_file))
        self.assertEqual(actual_time, file_time)

    def test_change_time(self):
        extra.touch(self.test_file)
        first_file_time = os.path.getmtime(self.test_file)

        sleep(0.01)
        extra.touch(self.test_file)
        second_file_time = os.path.getmtime(self.test_file)

        self.assertNotEqual(first_file_time, second_file_time)


class FindFilesTest(PymkTestCase):

    def setUp(self):
        super(FindFilesTest, self).setUp()

        os.mkdir('first')
        os.mkdir('second')
        os.mkdir('third')

        extra.touch('file1.test')
        extra.touch('file2.test')
        extra.touch('file3.notest')

        for filename in ['file3.test', 'file4.test', 'file5.notest']:
            path = os.path.join('first', filename)
            extra.touch(path)

        for filename in ['file6.test', 'file7.test', 'file8.notest']:
            path = os.path.join('second', filename)
            extra.touch(path)

        for filename in ['file9.test', 'file10.test', 'file11.notest']:
            path = os.path.join('third', filename)
            extra.touch(path)

    def test_nothing_found(self):
        self.assertEqual([], list(extra.find_files('.', '*.py')))

    def test_found_all_tests(self):
        should_found = [
            './file2.test',
            './file1.test',
            './third/file10.test',
            './third/file9.test',
            './second/file7.test',
            './second/file6.test',
            './first/file4.test',
            './first/file3.test'
        ]
        self.assertEqual(should_found, list(extra.find_files('.', '*.test')))


class RunCmdTest(PymkTestCase):

    def test_success(self):
        ret = extra.run_cmd(['ls -al'])
        self.assertEqual(file, type(ret[0]))
        self.assertEqual(file, type(ret[1]))

    def test_show_output(self):
        ret = extra.run_cmd(['ls', '*.py'], show_output=True)
        self.assertEqual(None, ret[0])
        self.assertEqual(None, ret[1])

    def test_fail(self):
        self.assertRaises(Perror.CommandError, extra.run_cmd, ['ls *.py'])

    def test_fail_with_show_enabled(self):
        self.assertRaises(
            Perror.CommandError, extra.run_cmd, ['ls *.py'], True)

    def test_providing_string(self):
        ret = extra.run_cmd('ls', '*.py')
        self.assertEqual(None, ret[0])
        self.assertEqual(None, ret[1])


class SignalHandlingTest(PymkTestCase):

    def setUp(self):
        super(SignalHandlingTest, self).setUp()
        self.handler = extra.cmd.SignalHandling()

    @patch('pymk.extra.cmd.signal')
    def test_init(self, signal):
        self.handler.do_init()

        self.assertEqual(
            call(signal.SIGABRT, self.handler.on_signal), signal.signal.call_args_list[0])
        self.assertEqual(
            call(signal.SIGFPE, self.handler.on_signal), signal.signal.call_args_list[1])
        self.assertEqual(
            call(signal.SIGILL, self.handler.on_signal), signal.signal.call_args_list[2])
        self.assertEqual(
            call(signal.SIGINT, self.handler.on_signal), signal.signal.call_args_list[3])
        self.assertEqual(
            call(signal.SIGSEGV, self.handler.on_signal), signal.signal.call_args_list[4])
        self.assertEqual(
            call(signal.SIGTERM, self.handler.on_signal), signal.signal.call_args_list[5])
        self.assertFalse(self.handler.aborted)

    def test_send_signal(self):
        spp = MagicMock()
        spp.poll.return_value = None
        signal = MagicMock()
        self.handler.send_signal(spp, signal)

        spp.send_signal.assert_called_once(signal)

    def test_send_signal_with_oserror(self):
        spp = MagicMock()
        spp.poll.return_value = None
        spp.send_signal.side_effect = OSError()
        signal = MagicMock()
        self.handler.send_signal(spp, signal)

        spp.send_signal.assert_called_once(signal)

    @patch('pymk.extra.cmd.Process')
    def test_on_signal(self, Process):
        Process.all_elements = [MagicMock()]
        signum = MagicMock()
        frame = MagicMock()

        self.handler.aborted = False
        with patch.object(self.handler, 'send_signal') as send_signal:
            self.handler.on_signal(signum, frame)

            send_signal.assert_called_once_with(
                Process.all_elements[0], signum)
            self.assertTrue(self.handler.aborted)

        self.handler.aborted = False


class ProccessTest(PymkTestCase):

    def setUp(self):
        super(ProccessTest, self).setUp()
        extra.cmd.Process.all_elements = []
        with patch.object(extra.cmd.Process, '__init__', return_value=None):
            self.proccess = extra.cmd.Process()
            self.proccess.spp = MagicMock()

    def tearDown(self):
        super(ProccessTest, self).tearDown()
        extra.cmd.Process.all_elements = []

    def test_init(self):
        with nested(
                patch.object(extra.cmd.Process, 'run'),
                patch.object(extra.cmd.Process, 'wait_for_termination'),
                patch.object(extra.cmd.Process, 'append_proccess'),
                patch.object(extra.cmd.Process, 'end_proccess'),
        ) as (run, wait_for_termination, append_proccess, end_proccess):
            process = extra.cmd.Process('something')
            self.assertEqual(['something', ], process.args)
            self.assertFalse(process.show_output)
            run.assert_called_once_with()
            append_proccess.assert_called_once_with()
            end_proccess.assert_called_once_with()

    def test_init_with_exception(self):
        with nested(
                patch.object(extra.cmd.Process, 'run'),
                patch.object(extra.cmd.Process, 'wait_for_termination'),
                patch.object(extra.cmd.Process, 'append_proccess'),
                patch.object(extra.cmd.Process, 'end_proccess'),
        ) as (run, wait_for_termination, append_proccess, end_proccess):
            wait_for_termination.side_effect = Exception('Boom!')

            self.assertRaises(Exception, extra.cmd.Process, 'something')
            run.assert_called_once_with()
            append_proccess.assert_called_once_with()
            end_proccess.assert_called_once_with()

    def test_prepere_args(self):
        self.proccess.prepere_args(['args', 'args2'])
        self.assertEqual(['args', 'args2'], self.proccess.args)

    def test_prepere_args_no_list(self):
        self.proccess.prepere_args('args')
        self.assertEqual(['args'], self.proccess.args)

    @patch('pymk.extra.cmd.Popen')
    def test_run(self, Popen):
        self.proccess.args = 'args'
        self.proccess.show_output = False

        self.proccess.run()

        Popen.assert_called_once_with(
            'args', stdout=PIPE, stderr=PIPE, shell=True)

    @patch('pymk.extra.cmd.Popen')
    def test_run_with_output(self, Popen):
        self.proccess.args = 'args'
        self.proccess.show_output = True

        self.proccess.run()

        Popen.assert_called_once_with('args', shell=True)

    @patch('pymk.extra.cmd.SignalHandling')
    def test_wait_for_termination_no_error(self, SignalHandling):
        SignalHandling.return_value.aborted = False
        self.proccess.spp.wait.return_value = 0
        with patch.object(self.proccess, 'raise_error') as raise_error:
            self.proccess.wait_for_termination()
            self.assertEqual(0, raise_error.call_count)

    @patch('pymk.extra.cmd.SignalHandling')
    def test_wait_for_termination_with_error(self, SignalHandling):
        SignalHandling.return_value.aborted = False
        self.proccess.spp.wait.return_value = 5
        with patch.object(self.proccess, 'raise_error') as raise_error:
            self.proccess.wait_for_termination()
            raise_error.assert_called_once_with(5)

    @patch('pymk.extra.cmd.SignalHandling')
    def test_wait_for_termination_with_abort(self, SignalHandling):
        SignalHandling.return_value.aborted = True
        self.proccess.spp.wait.return_value = 5
        with patch.object(self.proccess, 'raise_error') as raise_error:
            self.assertRaises(CommandAborted, self.proccess.wait_for_termination)
            self.assertEqual(0, raise_error.call_count)
