import shutil
import subprocess
from pathlib import Path

import pytest


dataPath=Path(__file__).parent/'data'



def test_module_tasks():
    testPath=dataPath/'module_tasks'
    shutil.copy('pie.py',str(testPath))
    o=subprocess.check_output(r'cd {} && python pie.py -l'.format(testPath),shell=True)
    print(o)
    assert o!=''

    # how to catch error when running the command
    # try:
        # o=subprocess.check_output(r'cd {} && python pie.py -l'.format(testPath),shell=True)
    # except subprocess.CalledProcessError as e:
        # print(e.returncode,e.cmd,e.output)
