import pytest


@pytest.mark.parametrize('pie_tasks_path',['missing_task'],indirect=['pie_tasks_path'])
def test_missing_task(pie,capsys,pie_tasks_path):
    pie.main(['missing'])
    out,err=capsys.readouterr()
    assert out.startswith('Task missing could not be found.')
