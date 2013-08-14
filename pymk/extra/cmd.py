import signal
from subprocess import Popen, PIPE
from pymk.error import CommandError, CommandAborted

_all_subprocesses = []
_aborted = False


def send_signal(spp, signal):
    try:
        if spp.poll() == None:
            spp.send_signal(signal)
    except OSError:
        pass


def on_signal(signum, frame):
    global _aborted
    _aborted = True
    for spp in _all_subprocesses:
        send_signal(spp, signum)


def init_signal_handling():
    for _signal in [
        signal.SIGABRT,
        signal.SIGFPE,
        signal.SIGILL,
        signal.SIGINT,
        signal.SIGSEGV,
        signal.SIGTERM
    ]:
        signal.signal(_signal, on_signal)


def run_cmd(args, show_output=False):
    def make_args(args):
        if type(args) == str or type(args) == unicode:
            return [args, ]
        else:
            return args

    def run_program(args, show_output):
        if show_output:
            return Popen(args, shell=True)
        else:
            return Popen(args, stdout=PIPE, stderr=PIPE, shell=True)

    def wait_for_termination(spp, show_output):
        error = spp.wait()
        if _aborted:
            raise CommandAborted()
        if error != 0:
            if show_output:
                raise CommandError(error, '')
            else:
                raise CommandError(error, spp.stderr.read())
    #-------------------------------------------------------------------------
    args = make_args(args)
    spp = run_program(args, show_output)
    _all_subprocesses.append(spp)
    try:
        wait_for_termination(spp, show_output)
    finally:
        send_signal(spp, signal.SIGTERM)
        _all_subprocesses.remove(spp)
    return spp.stdout, spp.stderr
