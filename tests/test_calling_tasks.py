import pytest


@pytest.mark.parametrize('pie_tasks_path',['missing_task'],indirect=['pie_tasks_path'])
def test_missing_task(pie,capsys,pie_tasks_path):
    r=pie.main(['missing'])
    out,err=capsys.readouterr()
    assert err.startswith('Task missing could not be found.')
    assert r==1
