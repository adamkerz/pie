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
