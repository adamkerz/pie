import pytest


@pytest.mark.parametrize('pie_tasks_path',['venv_context'],indirect=['pie_tasks_path'])
def test_venv_context(pie,pie_tasks_path,pie_mock_cmd):
    pie.main(['venvContext'])
    # TODO: only correct on Windows
    assert len(pie_mock_cmd.cmds)==1
    assert pie_mock_cmd.cmds[0][0][0]==r'cmd /c "first\Scripts\activate.bat && cmd /c "second\Scripts\activate.bat && blah""'
