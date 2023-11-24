Tee4Py is a python class which replicates the behaviour of the 'tee' Unix command. The tee command enables output to be written to the standard output (stdout) while simultaneously written to a file. 


## Installation

Tee4Py is avalible as a pip package through pypi and as such can be installed with:

```bash
pip install tee4py
```

Tee4Py only uses modules from the standard python library, meaning it has no dependencies. 


## Usage

The Tee4Py package has been desgined to work in the same way that redirect_stdout and redirect_stderr are (from the contextlib module). For example, to print the output to both the standard output and to a file you will need to do the following

```python
from tee4py import tee

with open('output.log','w') as f:
    with tee(f, True):
        print('This will be output to terminal and output.log')
print('This will be output to terminal only\n')

```

The second argument to the tee class specifies what to do with the standard error (stderr). The default value is True, meaning that stderr will also be piped to output.log. Changing this to False means that stderr will not be piped to the file, and will only be displayed in the terminal. 

```python
import sys
from tee4py import tee

with open('output.log','w') as f:
    with tee(f, False):
        print('This will be output to terminal and output.log')
        print('This will not go to output.log',file=sys.stderr)
print('This will be output to terminal only\n')

```

This second argument can also be a file handle to output stderr to its own specific file

```python
import sys
from tee4py import tee

with open('output.log','w') as f, open('output.err','w') as g:
    with tee(f, g): 
        print('This will be output to stdout and output.log')
        print('This will be output to stderr and output.err',file=sys.stderr)
print('This will be output to terminal only\n')

```

To ensure that tee4py can correctly apply tee to the output of subprocesses, the following approach must be followed

```python
import subprocess 
from tee4py import tee, get_stdout, get_stderr, subprocess_handle

with open('output_subprocess.log','w') as f:
    with tee(f):
        print('Doing something in python before subprocess')
        sp = subprocess.Popen('echo Output from subprocess',shell=True,stdout=get_stdout(),stderr=get_stderr())
        subprocess_handle(sp)
        RC = sp.wait()
        print('Doing something after subprocess')

```

Notice that stdout and stderr in subprocess.Popen are set using the get_stdout and get_stderr functions, while the subprocess is passed to subprocess_handle to ensure that the output is written to the file as well as stdout. 

The tee class can also be used in the following way

```python
from tee4py import tee

with open('output.log','w') as f:
    tee_object = tee(f)
    tee_object.write('This will be output to terminal and output.log')
    tee_object.close()
print('This will be output to terminal only\n')

```

## Citation

If you use tee4py in your work, please reference it with the following:
<pre>
@Misc{tee4py,
author = "Rhydian lewis",
title = "tee4py",
howpublished = "\url{https://gitlab.com/RhydianL/tee4py}",
year = "2023"}
<\pre>




