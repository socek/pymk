import signal

from subprocess import Popen, PIPE

from pymk.error import CommandError, CommandAborted


class SignalHandlingType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                SignalHandlingType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SignalHandling(object):

    __metaclass__ = SignalHandlingType

    def __init__(self):
        self.do_init()

    def do_init(self):
        self.aborted = False
        for _signal in [
            signal.SIGABRT,
            signal.SIGFPE,
            signal.SIGILL,
            signal.SIGINT,
            signal.SIGSEGV,
            signal.SIGTERM
        ]:
            signal.signal(_signal, self.on_signal)

    def send_signal(self, spp, signal):
        try:
            if spp.poll() == None:
                spp.send_signal(signal)
        except OSError:
            pass

    def on_signal(self, signum, frame):
        self.aborted = True
        for spp in Process.all_elements:
            self.send_signal(spp, signum)


class Process(object):
    all_elements = []

    def __init__(self, args, show_output=False):
        self.prepere_args(args)
        self.show_output = show_output
        self.run()
        self.append_proccess()
        try:
            self.wait_for_termination()
        finally:
            self.end_proccess()

    def prepere_args(self, args):
        if type(args) in (str,  unicode):
            self.args = [args, ]
        else:
            self.args = args

    def run(self):
        if self.show_output:
            self.spp = Popen(self.args, shell=True)
        else:
            self.spp = Popen(self.args, stdout=PIPE, stderr=PIPE, shell=True)

    def wait_for_termination(self):
        error = self.spp.wait()
        if SignalHandling().aborted:
            raise CommandAborted()
        if error != 0:
            self.raise_error(error)

    def raise_error(self, error):
        if self.show_output:
            raise CommandError(error, '')
        else:
            raise CommandError(error, self.spp.stderr.read())

    def append_proccess(self):
        self.all_elements.append(self.spp)

    def end_proccess(self):
        SignalHandling().send_signal(self.spp, signal.SIGTERM)
        self.all_elements.remove(self.spp)


def run(args, show_output=False):
    process = Process(args, show_output)
    return process.spp.stdout, process.spp.stderr
