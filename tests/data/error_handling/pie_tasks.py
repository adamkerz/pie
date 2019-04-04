from pie import *


@task
def cmd_no_failure():
    cmd('python -c "print(\'alpha\')"')


@task
def cmd_failure_non_existent():
    cmd('non_existent')
    cmd('python -c "print(\'beta\')"')


@task
def cmd_failure_error_code():
    cmd('python -c "import sys; sys.exit(3)"')
    cmd('python -c "print(\'gamma\')"')
