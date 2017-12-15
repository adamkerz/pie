import os

import pytest


from .utils import *


@pytest.mark.parametrize('pie_tasks_path',[dataPath/'pie_requirements'],indirect=['pie_tasks_path'])
def test_no_venv(pie,capsys,pie_tasks_path):
    pie.main(['test'])
    out,err=capsys.readouterr()
    assert out.startswith('.venv-pie not found. You can create it with the -R argument.')


@pytest.mark.parametrize('pie_tasks_path',[dataPath/'pie_requirements'],indirect=['pie_tasks_path'])
def test_create_venv(pie,capsys,pie_tasks_path):
    m=MockCmd(pie)
    pie.main(['-R'])
    out,err=capsys.readouterr()
    # TODO: improve checking, it's possible the wrong venv could be activated and we wouldn't detect it
    assert len(m.cmds)==3
    assert m.cmds[0][0][0]=='python -m virtualenv --system-site-packages ".venv-pie"'
    assert m.cmds[1][0][0].endswith('python -m pip install -U pip"')
    assert m.cmds[2][0][0].endswith('python -m pip install -r requirements.pie.txt"')


@pytest.mark.parametrize('pie_tasks_path',[dataPath/'pie_requirements'],indirect=['pie_tasks_path'])
def test_update_venv(pie,capsys,pie_tasks_path):
    m=MockCmd(pie)
    pie.main(['-r'])
    out,err=capsys.readouterr()
    # TODO: improve checking, it's possible the wrong venv could be activated and we wouldn't detect it
    assert len(m.cmds)==2
    assert m.cmds[0][0][0].endswith('python -m pip install -U pip"')
    assert m.cmds[1][0][0].endswith('python -m pip install -r requirements.pie.txt"')


@pytest.mark.parametrize('pie_tasks_path',[dataPath/'pie_requirements'],indirect=['pie_tasks_path'])
def test_use_venv(pie,capsys,pie_tasks_path):
    venv_path=pie_tasks_path/'.venv-pie'
    # TODO: make sure this is cleaned up after running, even if the task fails
    if not venv_path.exists(): venv_path.mkdir()
    m=MockCmd(pie)
    pie.main(['test'])
    out,err=capsys.readouterr()
    # TODO: Windows only
    assert len(m.cmds)==1
    assert m.cmds[0][0][0].endswith('.venv-pie\\Scripts\\activate.bat && python pie.py test"')
    venv_path.rmdir()
