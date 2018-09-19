from pie import *


@task
def no_function_call_decorator():
    pass

@task()
def function_call_decorator():
    pass


@task([Parameter('v')])
def one_parameter(v):
    print(v)

@task([OptionsParameter('v')])
def options_parameter(v):
    print(v)


@task([Parameter('v')])
def parameter_default_value(v='default'):
    print(v)

@task([OptionsParameter('v')])
def options_parameter_default_value(v='default'):
    print(v)
