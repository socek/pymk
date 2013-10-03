from mock import patch, call, MagicMock
from contextlib import nested
from subprocess import PIPE
import signal

import pymk.error as Perror
from pymk import extra
from pymk.tests.base import PymkTestCase
from pymk.error import CommandAborted, CommandError


class RunCmdTest(PymkTestCase):

    def test_success(self):
        ret = extra.run(['ls -al'], False)
        self.assertEqual(file, type(ret[0]))
        self.assertEqual(file, type(ret[1]))

    def test_show_output(self):
        ret = extra.run(['ls', '*.py'], show_output=True)
        self.assertEqual(None, ret[0])
        self.assertEqual(None, ret[1])

    def test_fail(self):
        self.assertRaises(Perror.CommandError, extra.run, ['ls *.py'], False)

    def test_fail_with_show_enabled(self):
        self.assertRaises(
            Perror.CommandError, extra.run, ['ls *.py'], True)

    def test_providing_string(self):
        self.assertRaises(CommandError, extra.run, 'ls *.py', False)

    @patch('pymk.extra.cmd.Process')
    def test_run_function(self, Process):
        ret = extra.run([1, 2, 3], True, 'env')

        Process.assert_called_once_with([1, 2, 3], True, env='env')
        spp = Process.return_value.spp

        self.assertEqual((spp.stdout, spp.stderr), ret)


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
        mysignal = MagicMock()
        self.handler.send_signal(spp, mysignal)

        spp.send_signal.assert_called_once(mysignal)

    def test_send_signal_with_oserror(self):
        spp = MagicMock()
        spp.poll.return_value = None
        spp.send_signal.side_effect = OSError()
        mysignal = MagicMock()
        self.handler.send_signal(spp, mysignal)

        spp.send_signal.assert_called_once(mysignal)

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
            self.assertTrue(process.show_output)
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
        self.proccess.env = None

        self.proccess.run()

        Popen.assert_called_once_with(
            'args', stdout=PIPE, stderr=PIPE, shell=True, env=None)

    @patch('pymk.extra.cmd.Popen')
    def test_run_with_output(self, Popen):
        self.proccess.args = 'args'
        self.proccess.show_output = True
        self.proccess.env = 'env'

        self.proccess.run()

        Popen.assert_called_once_with('args', shell=True, env='env')

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
            self.assertRaises(
                CommandAborted, self.proccess.wait_for_termination)
            self.assertEqual(0, raise_error.call_count)

    @patch('pymk.extra.cmd.CommandError')
    def test_raise_error_with_output(self, CommandError):
        self.proccess.show_output = True
        CommandError.return_value = Exception()

        self.assertRaises(Exception, self.proccess.raise_error, 5)
        CommandError.assert_called_once_with(5, '')

    @patch('pymk.extra.cmd.CommandError')
    def test_raise_error_without_output(self, CommandError):
        self.proccess.show_output = False
        CommandError.return_value = Exception()

        self.assertRaises(Exception, self.proccess.raise_error, 5)
        CommandError.assert_called_once_with(
            5, self.proccess.spp.stderr.read.return_value)

    def test_append_proccess(self):
        self.proccess.append_proccess()

        self.assertEqual([self.proccess.spp, ], self.proccess.all_elements)

    @patch('pymk.extra.cmd.SignalHandling')
    def test_end_proccess(self, SignalHandling):
        self.proccess.all_elements.append(self.proccess.spp)

        self.proccess.end_proccess()

        SignalHandling.return_value.send_signal.assert_called_once_with(
            self.proccess.spp, signal.SIGTERM)
        self.assertEqual([], self.proccess.all_elements)
