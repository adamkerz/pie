import os
import sys

from pie import *


OS='win' if os.name=='nt' else 'nix'
PYVER='py3' if sys.version_info>=(3,0) else 'py2'
VENV=venv('.venv-test-'+PYVER+'-'+OS)


@task
def setup():
    create_venv()
    update_packages()


@task
def create_venv():
    VENV.create()


@task
def update_packages():
    with VENV:
        pip(r'install -U pip')
        pip(r'install -U -r requirements.test.txt')


@task
def test():
    with VENV:
        env.set('PYTHONDONTWRITEBYTECODE','1')
        # cmd(r'python -c "from pathlib import Path; [p.unlink() for p in Path().glob(\"**/*.pyc\")]"')
        cmd(r'python -m pytest -s tests -vv')
