from pie import *


@task()
def asdf(v):
    """Test task."""
    print('whoo'+v)


@task()
def noDesc():
    pass


@task()
def a_long_long_long_long_long_long_task_name():
    """And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    And a super duper long (but repetitive) description too.
    """
    print('long')


@task(parameters=[dict(name='v',conversionFn=int)])
def params(v):
    """Test param prompting and injection."""
    print('sum: {}'.format(v+2))


@task
def testCmd():
    cmd('echo hi')


def not_a_task():
    pass


@task
def useVenv():
    with venv('venv'):
        # cmd('python')
        pip('install humanize==0.5.1')
