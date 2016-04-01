import pytest


from .utils import *


@pytest.mark.parametrize('pie_tasks_path',[dataPath/'missing_task'],indirect=['pie_tasks_path'])
def test_missing_task(pie,capsys,pie_tasks_path):
    pie.main(['missed'])
    out,err=capsys.readouterr()
    assert out.startswith('Task missing could not be found.')
