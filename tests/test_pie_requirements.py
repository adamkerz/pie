import os
import sys

import pytest

from .conftest import _venv_module,_venv_activate_cmd,_venv_python_cmd


@pytest.mark.parametrize('pie_tasks_path',['pie_requirements'],indirect=['pie_tasks_path'])
def test_no_venv(pie,capsys,pie_tasks_path):
    r=pie.main(['test'])
    out,err=capsys.readouterr()
    assert err.startswith('.venv-pie not found. You can create it with the -R argument.')
    assert r==1


@pytest.mark.parametrize('pie_tasks_path',['pie_requirements'],indirect=['pie_tasks_path'])
def test_create_venv(pie,capsys,is_win,is_py3,pie_tasks_path,pie_mock_cmd):
    pie.main(['-R'])
    out,err=capsys.readouterr()

    venv_path=pie_tasks_path/'.venv-pie'
    venv_activate_cmd=_venv_activate_cmd(is_win,venv_path)
    venv_python_cmd=_venv_python_cmd(is_win,venv_path)

    assert len(pie_mock_cmd.cmds)==3
    assert pie_mock_cmd.cmds[0][0][0]=='"{}" -m {} --system-site-packages "{}"'.format(sys.executable,_venv_module(is_py3),venv_path)
    assert pie_mock_cmd.cmds[1][0][0].endswith('"{}" && "{}" -m pip install -U pip"'.format(venv_activate_cmd,venv_python_cmd))
    assert pie_mock_cmd.cmds[2][0][0].endswith('"{}" && "{}" -m pip install -r requirements.pie.txt"'.format(venv_activate_cmd,venv_python_cmd))


@pytest.mark.parametrize('pie_tasks_path',['pie_requirements'],indirect=['pie_tasks_path'])
def test_update_venv(pie,capsys,is_win,pie_tasks_path,pie_mock_cmd):
    pie.main(['-r'])
    out,err=capsys.readouterr()

    venv_path=pie_tasks_path/'.venv-pie'
    venv_activate_cmd=_venv_activate_cmd(is_win,venv_path)
    venv_python_cmd=_venv_python_cmd(is_win,venv_path)

    assert len(pie_mock_cmd.cmds)==2
    assert pie_mock_cmd.cmds[0][0][0].endswith('"{}" && "{}" -m pip install -U pip"'.format(venv_activate_cmd,venv_python_cmd))
    assert pie_mock_cmd.cmds[1][0][0].endswith('"{}" && "{}" -m pip install -r requirements.pie.txt"'.format(venv_activate_cmd,venv_python_cmd))


@pytest.mark.parametrize('pie_tasks_path',['pie_requirements'],indirect=['pie_tasks_path'])
def test_use_venv(pie,capsys,is_win,pie_tasks_path,pie_mock_cmd):
    venv_path=pie_tasks_path/'.venv-pie'
    try:
        if not venv_path.exists(): venv_path.mkdir()
        pie.main(['test'])
        out,err=capsys.readouterr()

        venv_activate_cmd=_venv_activate_cmd(is_win,venv_path)
        venv_python_cmd=_venv_python_cmd(is_win,venv_path)

        assert len(pie_mock_cmd.cmds)==1
        assert pie_mock_cmd.cmds[0][0][0].endswith('"{}" && python pie.py test"'.format(venv_activate_cmd,venv_python_cmd))
    finally:
        if venv_path.exists(): venv_path.rmdir()


@pytest.mark.parametrize('pie_tasks_path',['pie space requirements'],indirect=['pie_tasks_path'])
def test_create_venv__space_in_path(pie,capsys,is_win,pie_tasks_path,pie_mock_cmd):

    def get_short_path_name(long_name):
        """
        Gets the short path name of a given long path.
        http://stackoverflow.com/a/23598461/200291
        """
        import ctypes
        from ctypes import wintypes
        _GetShortPathNameW=ctypes.windll.kernel32.GetShortPathNameW
        _GetShortPathNameW.argtypes=[wintypes.LPCWSTR,wintypes.LPWSTR,wintypes.DWORD]
        _GetShortPathNameW.restype=wintypes.DWORD

        # GetShortPathName is used by first calling it without a destination buffer.
        # It will return the number of characters you need to make the destination buffer. You then call it again with a buffer of that size.
        # If, due to a TOCTTOU problem, the return value is still larger, keep trying until you've got it right. So:
        output_buf_size=0
        while True:
            output_buf=ctypes.create_unicode_buffer(output_buf_size)
            needed=_GetShortPathNameW(long_name,output_buf,output_buf_size)
            if output_buf_size>=needed:
                return output_buf.value
            else:
                output_buf_size=needed

    venv_path=pie_tasks_path/'.venv-pie'
    old_sys_prefix=sys.prefix
    try:
        if not venv_path.exists(): venv_path.mkdir()
        # windows only: turn the venv_path into a short version (the path must exist for this)
        venv_short_path=get_short_path_name(str(venv_path)) if is_win else str(venv_path)
        # set the sys.prefix to emulate the venv being active
        sys.prefix=venv_short_path

        pie.main(['test'])
        out,err=capsys.readouterr()

        # we expect that the PieVenv detected that it's already active and just executed the command in the pie_task file
        assert pie_mock_cmd.cmds[0][0][0]=='blah'
    finally:
        sys.prefix=old_sys_prefix
        if venv_path.exists(): venv_path.rmdir()
