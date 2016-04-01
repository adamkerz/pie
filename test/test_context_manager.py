import pytest


from .utils import *


@pytest.mark.parametrize('pie_tasks_path',[dataPath/'venv_context'],indirect=['pie_tasks_path'])
def test_venv_context(pie,pie_tasks_path):
    m=MockCmd(pie)
    pie.main(['venvContext'])
    # TODO: only correct on Windows
    assert len(m.cmds)==1
    assert m.cmds[0][0][0]==r'first\Scripts\activate.bat && second\Scripts\activate.bat && blah'
