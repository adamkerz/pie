import sys
from pathlib import Path

import pytest


dataPath=Path(__file__).parent/'data'


@pytest.fixture(scope='function')
def pie():
    """Makes sure pie is freshly imported from cwd, then removes cwd from the path to allow pie_tasks to be imported from wherever we choose"""
    if 'pie' in sys.modules: del sys.modules['pie']
    cwd=str(Path.cwd())
    sys.path.insert(0,cwd)
    import pie
    # remove any common references to the cwd (which has a pie_tasks.py file)
    for p in ('','.',cwd):
        while True:
            try:
                sys.path.remove(p)
            except ValueError:
                break
    return pie


@pytest.fixture(scope='function')
def pie_tasks_path(request):
    """Makes sure pie_tasks has not been imported, and prepends the requested path to sys.path."""
    if 'pie_tasks' in sys.modules: del sys.modules['pie_tasks']
    p=request.param
    sys.path.insert(0,str(p))
    def fin():
        """Ensure the requested path is removed from sys.path"""
        while True:
            try:
                sys.path.remove(str(p))
            except ValueError:
                break
    request.addfinalizer(fin)
    return p


# TODO: better name and way?
class MockCmd(object):
    def __init__(self,pie):
        self.cmds=[]
        pie.CMD_FN=self.mock

    def mock(self,*args,**kwargs):
        self.cmds.append((args,kwargs))
        return 0

