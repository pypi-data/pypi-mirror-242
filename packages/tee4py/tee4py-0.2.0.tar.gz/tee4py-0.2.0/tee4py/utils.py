import traceback
import sys
import subprocess

def get_stdout():
    if not hasattr(sys.stdout,'_iamtee'):
        return None
    else:
        return subprocess.PIPE
    
def get_stderr():
    if not hasattr(sys.stderr,'_iamtee'): #stderr not captured
        return None
    elif not hasattr(sys.stdout,'_iamtee'): #stdout not captured
        return None
    elif sys.stderr.name == sys.stdout.name: # stderr goes to the same file as stdout
        return subprocess.STDOUT
    else: # is a different file
        return subprocess.PIPE

def _text_mode(sp):
    if hasattr(sp,'text_mode'):
        return sp.text_mode
    else:
        return sp.encoding or sp.errors or sp.universal_newlines

def _reader(sp, name, queue):
    pipe = getattr(sp,name)

    try:
        with pipe:
            if _text_mode(sp):
                for line in iter(pipe.readline, ""):
                    queue.put((name,line))
            else:
                for line in iter(pipe.readline, b''):
                    queue.put((name,line.decode()))  
 
    finally:
        queue.put(None)

def subprocess_handle(sp):
    # probably need to confirm it is a pipe
    stdout = get_stdout()
    stderr = get_stderr()

    if stdout is None:
        return
    
    sys.stdout.flush() # make sure verythign has been flushed to file
    if stderr is subprocess.PIPE:
        # add imports here to avoid possible issues
        from threading import Thread
        from queue import Queue 

        sys.stderr.flush()

        q = Queue()
        Thread(target=_reader, args=[sp,'stdout',q]).start()
        Thread(target=_reader, args=[sp,'stderr',q]).start()

        for _ in range(2):
            for name,line in iter(q.get, None):
                outfile = sys.stderr if name=='stderr' else sys.stdout
                print(line,end='',file=outfile)

    else:
        if _text_mode(sp):
            for stdout_line in iter(sp.stdout.readline, ""):
                print(stdout_line,end='')
        else:
            for stdout_line in iter(sp.stdout.readline, b''):
                print(stdout_line.decode(),end='')            

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
