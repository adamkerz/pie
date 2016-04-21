import pytest


from .utils import *


@pytest.mark.parametrize('pie_tasks_path',[dataPath/'no_pie_tasks',dataPath/'package_tasks',dataPath/'module_tasks'],indirect=['pie_tasks_path'])
def test_help(pie,capsys,pie_tasks_path):
    pie.main(['-h'])
    out,err=capsys.readouterr()
    assert out.startswith('Usage')


@pytest.mark.parametrize('pie_tasks_path',[dataPath/'no_pie_tasks'],indirect=['pie_tasks_path'])
def test_list_no_pie_tasks(pie,capsys,pie_tasks_path):
    pie.main(['-l'])
    out,err=capsys.readouterr()
    assert out.startswith('pie_tasks could not be found.')


@pytest.mark.parametrize('pie_tasks_path',[dataPath/'error_importing_pie_tasks'],indirect=['pie_tasks_path'])
def test_list_error_importing_pie_tasks(pie,capsys,pie_tasks_path):
    pie.main(['-l'])
    out,err=capsys.readouterr()
    assert out.startswith('An error occurred when importing pie_tasks:')


@pytest.mark.parametrize('pie_tasks_path',[dataPath/'package_tasks',dataPath/'module_tasks'],indirect=['pie_tasks_path'])
def test_list(pie,capsys,pie_tasks_path):
    pie.main(['-l'])
    out,err=capsys.readouterr()
    assert not out.startswith('Usage')
