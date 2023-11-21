"""

An implementation of Unix's 'tee' command in Python

Implementing the Unix tee in Python allows output to be written to a file as well as the terminal. The output of stderr can also 

Example usage:

    import sys
    from tee4py import tee

    with open('output.log','w') as f, open('output.err','w') as g:
        with tee(f, g): 
            print('This will be output to stdout and output.log')
            print('This will be output to stderr and output.err',file=sys.stderr)
        print('This will be output to terminal only\n')

The second argument to tee (g) can be a file handle or boolean. A value of True means that stderr will go to the same file as stdout, while False means it wont be piped to a file. 


"""

import sys
import io
import traceback

class tee(object):
    def __init__(self,log_file,pipe_stderr=True):
        self._log = log_file

        if pipe_stderr == True:
            self._pipe_stderr = 'logfile'
            self._stderr_file = open(self._log.name,'a') # open same file and append stderr to it
        elif pipe_stderr == False:
            self._pipe_stderr = None
        elif isinstance(pipe_stderr, io.IOBase):
            self._pipe_stderr = 'file'
            self._stderr_file = pipe_stderr
        else:
            raise Exception('Unknown type for pipe_stderr')

    def __enter__(self):
        self._enter = True
        self._stdout = sys.stdout
        self._write = self._log.write
        self._log.write = self._write_wrap
        sys.stdout = self._log

        if self._pipe_stderr is not None:
            # piping stderr to file
            self._stderr = sys.stderr
            self._stderr_write = self._stderr_file.write
            self._stderr_file.write = self._write_wrap_stderr
            sys.stderr = self._stderr_file

        return self

    def _exit(self):
        sys.stdout = self._stdout
        if self._pipe_stderr is not None:
            sys.stderr = self._stderr
            if self._pipe_stderr == 'logfile':
                self._stderr_file.close()

    def __exit__(self, exctype, excinst, exctb):
        self._exit()

    def _write_wrap_stderr(self, message):
        if self._pipe_stderr == 'logfile':
            self.flush() # ensures an order is preserved
        self._stderr.write(message)
        self._stderr_write(message)

    def _write_wrap(self, message):
        self._stdout.write(message)
        self._write(message)

    def write(self,message):
        if not hasattr(self,'_enter'):
            self.__enter__()
        self._log.write(message+"\n")

    def close(self):
        self._exit()

    def flush(self):
        sys.stdout.flush()

def get_exception(func):
    def get_exception_wrap(*args,**kwargs):
        try:
            r = func(*args,**kwargs)
            return r
        except (Exception,SystemExit) as e:
            exc = e
            trb = traceback.format_exception(etype=type(exc), value=exc, tb = exc.__traceback__)
            err = "".join(trb)
            sys.stderr.write(err)
            sys.exit()

    return get_exception_wrap
