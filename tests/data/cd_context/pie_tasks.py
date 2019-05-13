import os

from pie import *


@task
def cdContext():
    with cd('..'):
        print(os.getcwd())
    print(os.getcwd())
