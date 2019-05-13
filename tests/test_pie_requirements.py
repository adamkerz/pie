import os

import pytest


@pytest.mark.parametrize('pie_tasks_path',['pie_requirements'],indirect=['pie_tasks_path'])
def test_no_venv(pie,capsys,pie_tasks_path):
    r=pie.main(['test'])
    out,err=capsys.readouterr()
    assert err.startswith('.venv-pie not found. You can create it with the -R argument.')
    assert r==1


@pytest.mark.parametrize('pie_tasks_path',['pie_requirements'],indirect=['pie_tasks_path'])
def test_create_venv(pie,capsys,pie_tasks_path,pie_mock_cmd):
    pie.main(['-R'])
    out,err=capsys.readouterr()
    # TODO: improve checking, it's possible the wrong venv could be activated and we wouldn't detect it
    assert len(pie_mock_cmd.cmds)==3
    # TODO: more specific testing for py2/3
    venv_path=os.path.join(os.getcwd(),'.venv-pie')

    assert pie_mock_cmd.cmds[0][0][0]=='python -m virtualenv --system-site-packages "{}"'.format(venv_path) or pie_mock_cmd.cmds[0][0][0]=='python -m venv --system-site-packages "{}"'.format(venv_path)
    assert pie_mock_cmd.cmds[1][0][0].endswith('python -m pip install -U pip"')
    assert pie_mock_cmd.cmds[2][0][0].endswith('python -m pip install -r requirements.pie.txt"')


@pytest.mark.parametrize('pie_tasks_path',['pie_requirements'],indirect=['pie_tasks_path'])
def test_update_venv(pie,capsys,pie_tasks_path,pie_mock_cmd):
    pie.main(['-r'])
    out,err=capsys.readouterr()
    # TODO: improve checking, it's possible the wrong venv could be activated and we wouldn't detect it
    assert len(pie_mock_cmd.cmds)==2
    assert pie_mock_cmd.cmds[0][0][0].endswith('python -m pip install -U pip"')
    assert pie_mock_cmd.cmds[1][0][0].endswith('python -m pip install -r requirements.pie.txt"')


@pytest.mark.parametrize('pie_tasks_path',['pie_requirements'],indirect=['pie_tasks_path'])
def test_use_venv(pie,capsys,pie_tasks_path,pie_mock_cmd):
    venv_path=pie_tasks_path/'.venv-pie'
    # TODO: make sure this is cleaned up after running, even if the task fails
    if not venv_path.exists(): venv_path.mkdir()
    pie.main(['test'])
    out,err=capsys.readouterr()
    # TODO: Windows only
    assert len(pie_mock_cmd.cmds)==1
    assert pie_mock_cmd.cmds[0][0][0].endswith('.venv-pie\\Scripts\\activate.bat && python pie.py test"')
    venv_path.rmdir()
