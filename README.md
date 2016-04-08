# pie - Python Interactive Executor
Used to execute tasks written in Python from the command line with interactive prompting if needed.

I like [fabric](http://www.fabfile.org/) and use it for some Linux build and deployment scripts, however, at work, where we are in a Windows environment, we only use fabric's @task decorator to give us a nicer way of calling python code from the command line. We have hacked host definitions, a powershell context and use lots of 'venv\scripts\activate' in the tasks.

I also want a way for people who check out one of my python packages to be able to configure an environment to build, test and even run that project without having to first install fabric or other dependencies.

Other downsides of fabric (ie. because fabric is not focussed on solving these problems) are a very simple task argument interpreter, no interactive prompting for required or optional parameters and no ...

Finally, fabric is not py3 compatible and also depends on pycrypto - a binary package that must be built with Visual C on Windows if installed from pip (there is a third party build available for Windows).

pie is a single module so that it can be used without being installed - useful to bootstrap required build, test and run virtual environments and for launching other processes within them.


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


Use???

    class Lookup:
        def __init__(self,**entries):
            self.__dict__.update(entries)
