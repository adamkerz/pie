"""
pie - Python Interactive Executor
Enables a user to execute predefined tasks that may accept parameters and options from the command line without any other required packages.
Great for bootstrapping a development environment, and then interacting with it.
"""
__VERSION__='0.0.1'

import sys,os
import subprocess
from functools import wraps


WINDOWS=(os.name=='nt')
PY3=(sys.version_info>=(3,0))


"""
A class that can be used like a dictionary with more succinct syntax:
    l=Lookup(name='example',value='good')
    print(l.name)
    l.newValue=2
"""
class Lookup(object):
    def __init__(self,**entries):
        self.__dict__.update(entries)


"""
options is a lookup object where predefined options (in code) can be placed, as well as provided on the command line.
"""
options=Lookup()


"""
context is used to keep track of what context a command is being executed within.
    with venv('venv/build'):
        cmd('python -m pip')
"""
context=Lookup()


"""
A decorator that converts a simple Python function into a pie task.
 - parameters is a list of objects (use Lookup) with the following attributes:
     name - name of the param
     type - descriptive type of the param
     conversionFn - a function that will take a string and convert it to the desired type
"""
def task(parameters=[]):
    def decorator(taskFn):
        @wraps(taskFn)
        def wrapper(*args,**kwargs):
            # go through parameters and make sure they're all there, otherwise inject or prompt for them

            return taskFn(*args,**kwargs)
        return wrapper
    return decorator


"""
Executes a system command
"""
def cmd(c):
    subprocess.call(c,shell=True)


"""
Runs a pip command
"""
def pip(c):
    cmd('python -m pip {}'.format(c))


"""
A context class used to execute commands within a virtualenv
"""
class venv(object):
    def __init__(self,path):
        self.path=path

    # make this a context manager
    def __enter__(self):
        # push onto pie.context
        return self

    def __exit__(self,exc_type,exc_value,traceback):
        # pop from pie.context
        if exc_type is None:
            pass
        else:
            raise Exception('I dunno')# TODO



if __name__=='__main__':
    
    if WINDOWS:
        with open('pie.bat','w') as fout:
            fout.write('@echo off\npython -m pie %*\n')
    else:
        with open('pie','w') as fout:
            fout.write('python -m pie %*\n')

