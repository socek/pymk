from subprocess import Popen, PIPE
from pymk.error import CommandError
def run_cmd(args, show_output=False):
    """run_cmd(args, show_output=False) -> stdout, stderr
    Run external program.

    @param args: list of arguments for external program (with the path on the begining)
    @param show_output: show output of the command to stdout
    @return: stdout and stderr of the program
    """
    if show_output:
        spp = Popen(args, shell=True)
    else:
        spp = Popen(args, stdout=PIPE, stderr=PIPE, shell=True)
    try:
        error = spp.wait()
        if error != 0:
            if show_output:
                raise CommandError(error, '')
            else:
                raise CommandError(error, spp.stderr.read())
    finally:
        try:
            if spp.poll() == None:
                spp.kill()
        except OSError:
            pass
    return spp.stdout, spp.stderr
