from pathlib import Path

import pytest

from .conftest import _venv_module,_venv_activate_cmd,_venv_python_cmd


@pytest.mark.parametrize('pie_tasks_path',['venv_context'],indirect=['pie_tasks_path'])
def test_venv_context(pie,is_win,pie_tasks_path,pie_mock_cmd):
    pie.main(['venvContext'])

    cwd=Path().absolute()
    venv_path=pie_tasks_path/'.venv-pie'
    first_activate_cmd=_venv_activate_cmd(is_win,cwd/'first')
    second_activate_cmd=_venv_activate_cmd(is_win,cwd/'second')
    shell_cmd='cmd /c "' if is_win else 'bash -c "source '

    assert len(pie_mock_cmd.cmds)==1
    assert pie_mock_cmd.cmds[0][0][0]==r'{}"{}" && {}"{}" && blah""'''.format(shell_cmd,first_activate_cmd,shell_cmd,second_activate_cmd)


@pytest.mark.parametrize('pie_tasks_path',['cd_context'],indirect=['pie_tasks_path'])
def test_cd_context(pie,capsys,pie_tasks_path,pie_mock_cmd):
    pie.main(['cdContext'])
    cwd=Path().absolute()
    assert len(pie_mock_cmd.cmds)==0
    out,err=capsys.readouterr()
    assert out=='{}\n{}\n'.format(cwd.parent,cwd)


@pytest.mark.parametrize('pie_tasks_path',['env_context'],indirect=['pie_tasks_path'])
def test_env_context(pie,capsys,pie_tasks_path,pie_mock_cmd):
    pie.main(['envContext'])

    out_vars={'MY_VAL':['test'],'HOME':['something'],'PATH':['unset']}
    out,err=capsys.readouterr()
    # extent out_vars with the output from the pie_task
    for l in out.split('\n'):
        if l=='': continue
        k,v=l.split(': ',1)
        out_vars[k].append(v)
    # assert that the value we set matches the middle value printed,
    #        that the first and third values printed match (ie. the context was reverted)
    #        and that the first value does not match the second
    for k,v in out_vars.items():
        assert v[0]==v[2]
        assert v[1]==v[3]
        assert v[0]!=v[1]
