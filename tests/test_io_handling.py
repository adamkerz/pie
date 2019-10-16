import os

import pytest


@pytest.mark.parametrize('pie_tasks_path',['io_handling'],indirect=['pie_tasks_path'])
def test_output_to_stdout(pie,capfd,pie_tasks_path):
    pie.main(['output_to_stdout'])
    out,err=capfd.readouterr()
    out=out.replace(os.linesep,'\n')
    assert out=='alpha\n'

@pytest.mark.parametrize('pie_tasks_path',['io_handling'],indirect=['pie_tasks_path'])
def test_output_to_stderr(pie,capfd,pie_tasks_path):
    errorcode=pie.main(['output_to_stderr'])
    out,err=capfd.readouterr()
    err=err.replace(os.linesep,'\n')
    assert err.endswith('beta\n')

@pytest.mark.parametrize('pie_tasks_path',['io_handling'],indirect=['pie_tasks_path'])
def test_python_exception(pie,capfd,pie_tasks_path):
    errorcode=pie.main(['python_exception'])
    out,err=capfd.readouterr()
    out=out.replace(os.linesep,'\n')
    assert out=='gamma\n'
    err=err.replace(os.linesep,'\n')
    assert err.startswith('Traceback')
    assert 'NameError: name \'ff\' is not defined' in err
