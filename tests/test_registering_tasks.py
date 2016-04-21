import pytest


from .utils import *


@pytest.mark.parametrize('pie_tasks_path',[dataPath/'hidden_task'],indirect=['pie_tasks_path'])
def test_missing_task(pie,capsys,pie_tasks_path):
    pie.main(['-L'])
    out,err=capsys.readouterr()
    assert out=='visible\n'
