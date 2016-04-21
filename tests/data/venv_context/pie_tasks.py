from pie import *

@task
def venvContext():
    with venv('first'):
        with venv('second'):
            cmd('blah')
