import pytest


@pytest.mark.parametrize('pie_tasks_path',['parameters'],indirect=['pie_tasks_path'])
def test_listing_tasks(pie,capsys,pie_tasks_path):
    pie.main(['-l'])
    out,err=capsys.readouterr()
    tasks=set([t.strip(' ') for t in out.strip('\n').split('\n')])
    expected=set(['no_function_call_decorator','function_call_decorator','one_parameter','options_parameter','parameter_default_value','options_parameter_default_value'])
    assert tasks==expected


@pytest.mark.parametrize('pie_tasks_path',['parameters'],indirect=['pie_tasks_path'])
def test_options_parameter_from_command_line_options(pie,capsys,pie_tasks_path):
    pie.main(['-o','v=3','options_parameter'])
    out,err=capsys.readouterr()
    assert out=='3\n'

@pytest.mark.parametrize('pie_tasks_path',['parameters'],indirect=['pie_tasks_path'])
def test_options_parameter_from_command_line_task(pie,capsys,pie_tasks_path):
    pie.main(['options_parameter(3)'])
    out,err=capsys.readouterr()
    assert out=='3\n'

@pytest.mark.parametrize('pie_tasks_path',['parameters'],indirect=['pie_tasks_path'])
def test_options_parameter_persist_between_tasks(pie,capsys,pie_tasks_path):
    pie.main(['options_parameter(3)','options_parameter_default_value'])
    out,err=capsys.readouterr()
    assert out=='3\n3\n'
