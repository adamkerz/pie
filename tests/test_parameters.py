import pytest


@pytest.mark.parametrize('pie_tasks_path',['parameters'],indirect=['pie_tasks_path'])
def test_parameter_suggests_default(pie,capsys,pie_tasks_path,pie_mock_input):
    pie_mock_input.set_return('')
    pie.main(['parameter_default_value'])
    out,err=capsys.readouterr()
    assert pie_mock_input.input_str=="Please enter a value for v (default: 'foo'): "
    assert out=='foo\n'

    # reset input
    pie_mock_input.input_str=None
    pie_mock_input.set_return('bar')
    out,err=capsys.readouterr()
    pie.main(['parameter_default_value'])
    out,err=capsys.readouterr()
    assert pie_mock_input.input_str=="Please enter a value for v (default: 'foo'): "
    assert out=='bar\n'


@pytest.mark.parametrize('pie_tasks_path',['parameters'],indirect=['pie_tasks_path'])
def test_options_parameter_from_command_line_options(pie,capsys,pie_tasks_path,pie_input_forbidden):
    pie.main(['-o','v=3','options_parameter'])
    out,err=capsys.readouterr()
    assert out=='3\n'

@pytest.mark.parametrize('pie_tasks_path',['parameters'],indirect=['pie_tasks_path'])
def test_options_parameter_from_command_line_task(pie,capsys,pie_tasks_path,pie_input_forbidden):
    pie.main(['options_parameter(3)'])
    out,err=capsys.readouterr()
    assert out=='3\n'

@pytest.mark.parametrize('pie_tasks_path',['parameters'],indirect=['pie_tasks_path'])
def test_options_parameter_persist_between_tasks(pie,capsys,pie_tasks_path,pie_input_forbidden):
    pie.main(['options_parameter(3)','options_parameter_default_value'])
    out,err=capsys.readouterr()
    assert out=='3\n3\n'


@pytest.mark.parametrize('pie_tasks_path',['parameters'],indirect=['pie_tasks_path'])
def test_options_parameter_suggests_default(pie,capsys,pie_tasks_path,pie_mock_input):
    pie_mock_input.set_return('')
    pie.main(['options_parameter_default_value'])
    out,err=capsys.readouterr()
    assert pie_mock_input.input_str=="Please enter a value for v (default: 'foo'): "
    assert out=='foo\n'

    # reset input, but since we are using options parameters, the previous default is now stored in options, so no prompting should occur
    pie_mock_input.input_str=None
    pie_mock_input.set_return('bar')
    out,err=capsys.readouterr()
    pie.main(['options_parameter_default_value'])
    out,err=capsys.readouterr()
    assert pie_mock_input.input_str is None
    assert out=='foo\n'


@pytest.mark.parametrize('pie_tasks_path',['parameters'],indirect=['pie_tasks_path'])
def test_options_parameter_uses_default(pie,capsys,pie_tasks_path,pie_input_forbidden):
    pie.main(['options_parameter_default_value_use_default'])
    out,err=capsys.readouterr()
    assert out=='foo\n'

@pytest.mark.parametrize('pie_tasks_path',['parameters'],indirect=['pie_tasks_path'])
def test_options_parameter_multiple_parameters_uses_default(pie,capsys,pie_tasks_path,pie_input_forbidden):
    pie.main(['options_parameter_multiple_parameters_use_default(bar)'])
    out,err=capsys.readouterr()
    assert out=='foo\n'
