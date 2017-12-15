from pie import *


@task
def setup():
    createVenvs()
    updatePackages()


@task
def createVenv():
    venv('.venv-test').create()


@task
def updatePackages():
    with venv('.venv-test'):
        pip(r'install -U pip')
        pip(r'install -U -r requirements.test.txt')


@task
def test():
    with venv(r'.venv-test'):
        cmd(r'python -m pytest -s tests')
