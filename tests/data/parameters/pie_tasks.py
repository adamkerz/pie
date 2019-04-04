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
def parameter_default_value(v='foo'):
    print(v)

@task([OptionsParameter('v')])
def options_parameter_default_value(v='foo'):
    print(v)

@task([OptionsParameter('v',use_default=True)])
def options_parameter_default_value_use_default(v='foo'):
    print(v)

@task([OptionsParameter('a'),OptionsParameter('b',use_default=True),])
def options_parameter_multiple_parameters_use_default(a,b='foo'):
    print(b)
