from subprocess import Popen, PIPE
from pymk.error import CommandError


def run_cmd(args, show_output=False):
    """run_cmd(args, show_output=False) -> stdout, stderr
    Run external program.

    @param args: list of arguments or string for external program (with the path on the begining)
    @param show_output: show output of the command to stdout
    @return: stdout and stderr of the program
    """
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
        if error != 0:
            if show_output:
                raise CommandError(error, '')
            else:
                raise CommandError(error, spp.stderr.read())

    def kill_process(spp):
        try:
            if spp.poll() == None:
                spp.kill()
        except OSError:
            pass
    #---------------------------------------------------------------------------
    args = make_args(args)
    spp = run_program(args, show_output)
    try:
        wait_for_termination(spp, show_output)
    finally:
        kill_process(spp)
    return spp.stdout, spp.stderr
