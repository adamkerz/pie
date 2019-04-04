import pytest


@pytest.mark.parametrize('pie_tasks_path',['no_pie_tasks','package_tasks','module_tasks'],indirect=['pie_tasks_path'])
def test_help(pie,capsys,pie_tasks_path):
    pie.main(['-h'])
    out,err=capsys.readouterr()
    assert out.startswith('Usage')


@pytest.mark.parametrize('pie_tasks_path',['no_pie_tasks'],indirect=['pie_tasks_path'])
def test_list_no_pie_tasks(pie,capsys,pie_tasks_path):
    r=pie.main(['-l'])
    out,err=capsys.readouterr()
    assert err.startswith('pie_tasks could not be found.')
    assert r==1


@pytest.mark.parametrize('pie_tasks_path',['error_importing_pie_tasks'],indirect=['pie_tasks_path'])
def test_list_error_importing_pie_tasks(pie,capsys,pie_tasks_path):
    r=pie.main(['-l'])
    out,err=capsys.readouterr()
    assert err.startswith('An error occurred when importing pie_tasks:')
    assert r==1


@pytest.mark.parametrize('pie_tasks_path',['package_tasks','module_tasks'],indirect=['pie_tasks_path'])
def test_list(pie,capsys,pie_tasks_path):
    pie.main(['-l'])
    out,err=capsys.readouterr()
    assert not out.startswith('Usage')
