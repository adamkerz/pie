import os

import pytest


@pytest.mark.parametrize('pie_tasks_path',['venv_context'],indirect=['pie_tasks_path'])
def test_venv_context(pie,pie_tasks_path,pie_mock_cmd):
    pie.main(['venvContext'])
    cwd=os.getcwd()
    first_activate=r'{}\first\Scripts\activate.bat'.format(cwd)
    second_activate=r'{}\second\Scripts\activate.bat'.format(cwd)
    # TODO: only correct on Windows
    assert len(pie_mock_cmd.cmds)==1
    assert pie_mock_cmd.cmds[0][0][0]==r'cmd /c "{} && cmd /c "{} && blah""'.format(first_activate,second_activate)


@pytest.mark.parametrize('pie_tasks_path',['cd_context'],indirect=['pie_tasks_path'])
def test_cd_context(pie,capsys,pie_tasks_path,pie_mock_cmd):
    pie.main(['cdContext'])
    cwd=os.getcwd()
    assert len(pie_mock_cmd.cmds)==0
    out,err=capsys.readouterr()
    assert out=='{}\n{}\n'.format(os.path.dirname(cwd),cwd)


@pytest.mark.parametrize('pie_tasks_path',['env_context'],indirect=['pie_tasks_path'])
def test_env_context(pie,capsys,pie_tasks_path,pie_mock_cmd):
    pie.main(['envContext'])

    out_vars={'MY_VAL':['test'],'HOME':['something'],'COMPUTERNAME':['unset']}
    out,err=capsys.readouterr()
    for l in out.split('\n'):
        if l=='': continue
        k,v=l.split(': ',1)
        out_vars[k].append(v)
    for k,v in out_vars.items():
        assert v[0]==v[2]
        assert v[1]==v[3]
        assert v[0]!=v[1] # this may fail on *nix for COMPUTERNAME
