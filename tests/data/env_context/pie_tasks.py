import os

from pie import *


@task
def envContext():
    e={'MY_VAL':'test','HOME':'something','PATH':None}

    def _print_env():
        for k in e:
            print('{}: {}'.format(k,os.environ.get(k,'unset')))

    _print_env()
    with env(e):
        _print_env()
    _print_env()
