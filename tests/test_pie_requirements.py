import os
import sys

import pytest

from .conftest import _venv_module,_venv_activate_cmd,_venv_python_cmd


@pytest.mark.parametrize('pie_tasks_path',['pie_requirements'],indirect=['pie_tasks_path'])
def test_no_venv(pie,capsys,pie_tasks_path):
    r=pie.main(['test'])
    out,err=capsys.readouterr()
    assert err.startswith('.venv-pie not found. You can create it with the -R argument.')
    assert r==1


@pytest.mark.parametrize('pie_tasks_path',['pie_requirements'],indirect=['pie_tasks_path'])
def test_create_venv(pie,capsys,is_win,is_py3,pie_tasks_path,pie_mock_cmd):
    pie.main(['-R'])
    out,err=capsys.readouterr()

    venv_path=pie_tasks_path/'.venv-pie'
    venv_activate_cmd=_venv_activate_cmd(is_win,venv_path)
    venv_python_cmd=_venv_python_cmd(is_win,venv_path)

    assert len(pie_mock_cmd.cmds)==3
    assert pie_mock_cmd.cmds[0][0][0]=='"{}" -m {} --system-site-packages "{}"'.format(sys.executable,_venv_module(is_py3),venv_path)
    assert pie_mock_cmd.cmds[1][0][0].endswith('"{}" && "{}" -m pip install -U pip"'.format(venv_activate_cmd,venv_python_cmd))
    assert pie_mock_cmd.cmds[2][0][0].endswith('"{}" && "{}" -m pip install -r requirements.pie.txt"'.format(venv_activate_cmd,venv_python_cmd))


@pytest.mark.parametrize('pie_tasks_path',['pie_requirements'],indirect=['pie_tasks_path'])
def test_update_venv(pie,capsys,is_win,pie_tasks_path,pie_mock_cmd):
    pie.main(['-r'])
    out,err=capsys.readouterr()

    venv_path=pie_tasks_path/'.venv-pie'
    venv_activate_cmd=_venv_activate_cmd(is_win,venv_path)
    venv_python_cmd=_venv_python_cmd(is_win,venv_path)

    assert len(pie_mock_cmd.cmds)==2
    assert pie_mock_cmd.cmds[0][0][0].endswith('"{}" && "{}" -m pip install -U pip"'.format(venv_activate_cmd,venv_python_cmd))
    assert pie_mock_cmd.cmds[1][0][0].endswith('"{}" && "{}" -m pip install -r requirements.pie.txt"'.format(venv_activate_cmd,venv_python_cmd))


@pytest.mark.parametrize('pie_tasks_path',['pie_requirements'],indirect=['pie_tasks_path'])
def test_use_venv(pie,capsys,is_win,pie_tasks_path,pie_mock_cmd):
    venv_path=pie_tasks_path/'.venv-pie'
    try:
        if not venv_path.exists(): venv_path.mkdir()
        pie.main(['test'])
        out,err=capsys.readouterr()

        venv_activate_cmd=_venv_activate_cmd(is_win,venv_path)
        venv_python_cmd=_venv_python_cmd(is_win,venv_path)

        assert len(pie_mock_cmd.cmds)==1
        assert pie_mock_cmd.cmds[0][0][0].endswith('"{}" && python pie.py test"'.format(venv_activate_cmd,venv_python_cmd))
    finally:
        venv_path.rmdir()
