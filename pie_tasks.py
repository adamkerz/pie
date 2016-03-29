from pathlib import Path

from pie import *


@task
def setup():
    createDirectories()
    createVenv()
    updateTestPackages()


@task
def createVenvs():
    cmd(r'python -m virtualenv venvs\test')


@task
def updatePackages():
    with venv(r'venvs\test'):
        # update pip
        pip(r'install -U -i http://sirpypi/packages/simple/ --trusted-host sirpypi pip')
        # and update other requirements
        pip(r'install -U -i http://sirpypi/packages/simple/ --trusted-host sirpypi -r requirements.test.txt')


@task
def test():
    with venv(r'venvs\test'):
        cmd(r'py.test -s test')
