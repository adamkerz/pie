import pytest


@pytest.mark.parametrize('pie_tasks_path',['hidden_task'],indirect=['pie_tasks_path'])
def test_missing_task(pie,capsys,pie_tasks_path):
    pie.main(['-L'])
    out,err=capsys.readouterr()
    assert out=='visible\n'
