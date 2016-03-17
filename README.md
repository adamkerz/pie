# pie
Python Interactive Executor - used to execute tasks written in Python from the command line with interactive prompting if needed.

pie will be a single module so that it can be used without being installed - useful for all python projects that create build, test, run virtualenvs.


Examples:

> python -m pie
Created pie.[bat|sh]

> pie createVenv

> pie local.runserver

> pie -o role=prod server.deployWebsite

> pie configurable('with',params=3)

> pie configurable('with')
Please enter a value for params (int): 3

> pie configurable
Enter a first value: with
Please enter a value for params (int): 3



Example Code:

from pie import *

pie.options.roles={'local':{'someVal':'test'},
                   'prod':{'someVal':'real'},}

@global
def globalSetupFn():
    venv...?


@task(parameters=[dict(name='first',type='str',conversionFn=str,prompt='Enter a first value'),
                  dict(name='params',type='int',conversionFn=int)])
def configurable(first,params):
    env=pie.options.roles[pie.options.role]
    cmd('echo {}'.format(env['someVal'])
    with venv('venvs/build'):
        cmd('python -m pip list')
        pip('list')

@task(parameters[dict(name='env',type='injected',conversionFn=lambda:pie.options.roles[pie.options.role])]
def anotherTask(env):
    env['someVal']


Use:???
class Lookup:
    def __init__(self,**entries):
        self.__dict__.update(entries)
