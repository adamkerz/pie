import os

import pytest


@pytest.mark.parametrize('pie_tasks_path',['error_handling'],indirect=['pie_tasks_path'])
def test_cmd_no_failure(pie,capfd,pie_tasks_path):
    pie.main(['cmd_no_failure'])
    out,err=capfd.readouterr()
    out=out.replace(os.linesep,'\n')
    assert out=='alpha\n'

@pytest.mark.parametrize('pie_tasks_path',['error_handling'],indirect=['pie_tasks_path'])
def test_cmd_failure_non_existent(pie,capfd,is_win,pie_tasks_path):
    errorcode=pie.main(['cmd_failure_non_existent'])
    out,err=capfd.readouterr()
    assert not out.endswith('beta\n')
    assert errorcode==1 if is_win else 127

@pytest.mark.parametrize('pie_tasks_path',['error_handling'],indirect=['pie_tasks_path'])
def test_cmd_failure_error_code(pie,capfd,pie_tasks_path):
    errorcode=pie.main(['cmd_failure_error_code'])
    out,err=capfd.readouterr()
    assert not out.endswith('gamma\n')
    assert errorcode==3

