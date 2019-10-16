from pie import *


@task
def output_to_stdout():
    cmd('python -c "print(\'alpha\')"')


@task
def output_to_stderr():
    cmd('python -c "from __future__ import print_function; import sys; print(\'beta\', file=sys.stderr)"')


@task
def python_exception():
    cmd('python -c "print(\'gamma\'); x=ff"')
