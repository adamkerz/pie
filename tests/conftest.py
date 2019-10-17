import os
import sys
from pathlib import Path

import pytest


dataPath=Path(__file__).parent/'data'


def _remove_from_sys_path(*args):
    for p in args:
        while True:
            try:
                sys.path.remove(p)
            except ValueError:
                break


# helper functions
_venv_module=lambda is_py3: 'venv' if is_py3 else 'virtualenv'
_venv_bin_dir=lambda is_win,venv_path: venv_path/(r'Scripts' if is_win else 'bin')
_venv_activate_cmd=lambda is_win,venv_path: _venv_bin_dir(is_win,venv_path)/(r'activate.bat' if is_win else 'activate')
_venv_python_cmd=lambda is_win,venv_path: _venv_bin_dir(is_win,venv_path)/'python'


@pytest.fixture(scope='session')
def is_win():
    return os.name=='nt'

@pytest.fixture(scope='session')
def is_py3():
    return sys.version_info>=(3,0)


@pytest.fixture(scope='function')
def pie():
    """Makes sure pie is freshly imported from cwd, then removes cwd from the path to allow pie_tasks to be imported from wherever we choose"""
    if 'pie' in sys.modules: del sys.modules['pie']
    cwd=str(Path.cwd())
    sys.path.insert(0,cwd)
    import pie
    # remove any references to the cwd (which has a pie_tasks.py file)
    _remove_from_sys_path(cwd)
    return pie


@pytest.fixture(scope='function')
def pie_mock_cmd(pie):
    class MockCmd(object):
        def __init__(self,pie):
            self.cmds=[]
            pie.CmdExecutor.cmd_fn=self.mock

        def mock(self,*args,**kwargs):
            self.cmds.append((args,kwargs))
            return 0

    return MockCmd(pie)


@pytest.fixture(scope='function')
def pie_mock_input(pie):
    class MockInput(object):
        def __init__(self,pie):
            self.input_str=None
            self.ret=None
            pie.Parameter.INPUT_FN=self.mock

        def set_return(self,ret):
            self.ret=ret

        def mock(self,s):
            self.input_str=s
            return self.ret

    return MockInput(pie)


@pytest.fixture(scope='function')
def pie_input_forbidden(pie):
    def input_forbidden(s):
        raise Exception('Input forbidden')
    pie.Parameter.INPUT_FN=input_forbidden


@pytest.fixture(scope='function')
def pie_tasks_path(request):
    """Makes sure pie_tasks has not been imported, and changes the cwd to the test data dir, ensuring that a relative cwd reference is on the path."""
    if 'pie_tasks' in sys.modules: del sys.modules['pie_tasks']
    p=dataPath/request.param
    cwd=Path.cwd()
    os.chdir(str(p))
    # clean up any cwd references on sys path
    _remove_from_sys_path('','.')
    # and just add one at the start
    sys.path.insert(0,'')
    def fin():
        """Change back to the old cwd"""
        os.chdir(str(cwd))
    request.addfinalizer(fin)
    return p
