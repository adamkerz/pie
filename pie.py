"""
pie - Python Interactive Executor
Enables a user to execute predefined tasks that may accept parameters and options from the command line without any other required packages.
Great for bootstrapping a development environment, and then interacting with it.
"""
__VERSION__='0.0.1'

import os
import re
import subprocess
import sys
from functools import wraps


# environment constants
WINDOWS=(os.name=='nt')
PY3=(sys.version_info>=(3,0))

# the function used to prompt for input
PROMPT_FN=input if PY3 else raw_input



# ----------------------------------------
# configuration
# ----------------------------------------
class Lookup(object):
    """
    A class that can be used like a dictionary with more succinct syntax:
        l=Lookup(name='example',value='good')
        print(l.name)
        l.newValue=2
    """
    def __init__(self,**entries):
        self.__dict__.update(entries)


# options is a lookup object where predefined options (in code) can be placed, as well as provided on the command line.
options=Lookup()


# context is used to keep track of what context a command is being executed within.
#     with venv('venv/build'):
#         cmd('python -m pip')
context=Lookup()



# ----------------------------------------
# tasks
# ----------------------------------------
# tasks is a dictionary of registered tasks, where key=name. Tasks are possibly from within submodules where name=module.task.
tasks={}

def task(parameters=[]):
    """
    A (function that returns a) decorator that converts a simple Python function into a pie task.
     - parameters is a list of objects (use Lookup) with the following attributes:
         name - name of the param
         type - descriptive type of the param
         conversionFn - a function that will take a string and convert it to the desired type
    """
    def decorator(taskFn):
        # wrap the function
        @wraps(taskFn)
        def wrapper(*args,**kwargs):
            # args might be a tuple, but we want to append to it
            args=list(args)
            # go through parameters and make sure they're all there, otherwise inject or prompt for them
            for i,p in enumerate(parameters):
                if len(args)<=i:
                    # TODO: use a default value if provided - would be best to use the default value as provided with the function definition, rather than add a 'default' key in parameters dicts.
                    # prompt for a missing value
                    promptStr=p['prompt'] if 'prompt' in p else 'Please enter a value for {}: '.format(p['name'])
                    v=PROMPT_FN(promptStr)
                    args.append(v)
                # and apply the conversionFn
                if 'conversionFn' in p: args[i]=p['conversionFn'](args[i])
            return taskFn(*args,**kwargs)

        # then register the task
        tasks[taskFn.__name__]={'fn':wrapper,'desc':taskFn.__doc__,'params':parameters}
        return wrapper

    # check in case we were called as a decorator eg. @task (without the function call)
    if callable(parameters):
        # this means that parameters is actually the function to decorate
        taskFn=parameters
        # but parameters is used in the wrapper and assumed to be a list, so set it as an empty list (as we weren't provided any parameters)
        parameters=[]
        return decorator(taskFn)

    # otherwise return the decorator function
    return decorator



# ----------------------------------------
# operations
# ----------------------------------------
def cmd(c):
    """
    Executes a system command
    """
    subprocess.call(c,shell=True)


def pip(c,pythonCmd='python'):
    """
    Runs a pip command
    """
    cmd('{} -m pip {}'.format(pythonCmd,c))


class venv(object):
    """
    A context class used to execute commands within a virtualenv
    """
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



# ----------------------------------------
# Command line functionality
# ----------------------------------------
class Argument(object):
    def execute(self):
        raise NotImplemented()

    def __repr__(self):
        return self.__class__.__name__


class Version(Argument):
    def execute(self):
        print('pie v{}'.format(__VERSION__))

    def __repr__(self):
        return 'Version: {}'.format(__VERSION__)


class CreateBatchFile(Argument):
    def execute(self):
        if WINDOWS:
            with open('pie.bat','w') as fout:
                fout.write('@echo off\npython -c "import pie; pie.main()" %*\n')
        else:
            with open('pie','w') as fout:
                fout.write('python -c "import pie; pie.main()" %*\n')


class ListTasks(Argument):
    def __init__(self,includeDescription=True):
        self.includeDescription=includeDescription

    def execute(self):
        for k in sorted(tasks.keys()):
            v=tasks[k]
            if self.includeDescription:
                desc=v['desc'] or ''
                print('{:30} {:.70}'.format(k,desc.replace('\n',' ')))
            else:
                print(k)


class Help(Argument):
    def execute(self):
        print('Usage:    pie [ -v | -h | -b | -l | -L ]')
        print('          pie [ -o <name>=<value> | <task>[(<args>...)] ]...')
        print('Version:  v{}'.format(__VERSION__))
        print('')
        print('  -v      Display version')
        print('  -h      Display this help')
        print('  -b      Create batch file shortcut')
        print('  -l      List available tasks with description')
        print('  -L      List available tasks with name only')
        print('  -o      Sets an option with name to value')
        print('  <task>  Runs a task passing through arguments if required')
        print('')
        print('The order of -o and <task> options matters - each will be executed in the order given on the command line.')


class Option(Argument):
    def __init__(self,name,value):
        self.name=name
        self.value=value

    def execute(self):
        setattr(options,self.name,self.value)

    def __repr__(self):
        return 'Option: {}={}'.format(self.name,self.value)


class Task(Argument):
    def __init__(self,name,args=[],kwargs={}):
        self.name=name
        self.args=args
        self.kwargs=kwargs

    def execute(self):
        tasks[self.name]['fn'](*self.args,**self.kwargs)

    def __repr__(self):
        return 'Task: {}(args={},kwargs={})'.format(self.name,self.args,self.kwargs)



# ----------------------------------------
# Command line parsing
# ----------------------------------------
TASK_RE=re.compile(r'(?P<name>[^()]+)(\((?P<args>.*)\))?')
def parseArguments(args):
    # skip the name of the command
    i=1
    parsed=[]
    while i<len(args):
        arg=args[i]
        if arg.startswith('-'):
            # although we say that these options are check that incompatible options aren't used together
            if arg=='-v':
                parsed.append(Version())
            elif arg=='-h':
                parsed.append(Help())
            elif arg=='-b':
                parsed.append(CreateBatchFile())
            elif arg=='-l':
                parsed.append(ListTasks())
            elif arg=='-L':
                parsed.append(ListTasks(includeDescription=False))
            elif arg=='-o':
                name,value=args[i+1].split('=')
                parsed.append(Option(name,value))
                i+=1
            else:
                raise Exception('Unknown ')
        else:
            mo=TASK_RE.match(arg)
            if mo:
                args=mo.group('args')
                args=args.split(',') if args else []
                # TODO: add further parsing to handle keyword arguments
                parsed.append(Task(mo.group('name'),args=args,kwargs={}))
            else:
                raise Exception('Unknown task format: {}'.format(arg))
        i+=1
    return parsed



# ----------------------------------------
# entry point
# ----------------------------------------
def main():
    args=parseArguments(sys.argv)
    if args:
        import pie_tasks
        for a in args:
            a.execute()
            # print(repr(a))
    else:
        Help().execute()


if __name__=='__main__':
    # import pie so that both we and any pie_tasks code that imports pie are referring to the same module variables
    import pie
    pie.main()
