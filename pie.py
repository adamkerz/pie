"""
pie - Python Interactive Executor
Enables a user to execute predefined tasks that may accept parameters and options from the command line without any other required packages.
Great for bootstrapping a development environment, and then interacting with it.
"""
__VERSION__='0.0.1'

import os
import subprocess
import sys
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
tasks is a dictionary of registered tasks, where key=name. Tasks are possibly from within submodules where name=module.task.
"""
tasks={}


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

class Argument(object):
    def __init__(self,type):
        self.type=type

    def execute(self):
        raise NotImplemented()


class Option(Argument):
    def __init__(self,name,value):
        super(Option,self).__init__('option')
        self.name=name
        self.value=value

    def execute(self):
        options[self.name]=self.value


class Task(Argument):
    def __init__(self,name,args=[],kwargs={}):
        super(Option,self).__init__('task')
        self.name=name
        self.args=args
        self.kwargs=kwargs

    def execute(self):
        # TODO: check task arg requirements and prompt - OR - can this be done by the @task decorator?
        tasks[self.name](*self.args,**self.kwargs)


def parseArguments(args):
    # skip the name of the command
    i=1
    parsed=[]
    while i<len(args):
        arg=args[i]
        if arg=='-o':
            name,value=args[i+1].split('=')
            parsed.append(Option(name,value))
            i+=1
        else:
            parsed.append(Task(arg))
        i+=1
    return parsed


def main(args):
    print(parseArguments(args))


if __name__=='__main__':
    main(sys.argv)

    if WINDOWS:
        with open('pie.bat','w') as fout:
            fout.write('@echo off\npython -m pie %*\n')
    else:
        with open('pie','w') as fout:
            fout.write('python -m pie %*\n')

